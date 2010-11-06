#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
import cgi
import logging
import os
import datetime

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import base
import models


class LeadListing(base.BasePage):
  
  def get(self):
    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    Q_SIZE = 100
    self.template = "lead_listing.html"
    cursor = self.request.get("cursor", "")
    pg = self.request.get("pg", 1)
    
    q = models.Lead.all().filter("account =", self.account).order("-date_created")
    if cursor:
      q.with_cursor(cursor)
    leads = q.fetch(Q_SIZE)
    
    if len(leads) < Q_SIZE:
      self.ctx['next_link'] = None
    else:
      self.ctx['this_cursor'] = cursor
      self.ctx['next_cursor'] = q.cursor()
      self.ctx['next_pg'] = "%s" % (int(pg) + 1)
      self.ctx['next_link'] = "%s?cursor=%s&pg=%s" % \
        (self.request.path, self.ctx['next_cursor'], self.ctx['next_pg'])

    if cursor:
      self.ctx['top_link'] = self.request.path
    else:
      self.ctx['top_link'] = None

    self.ctx['leads'] = leads
    self.ctx['pg'] = pg
    self.ctx['set_size'] = str(Q_SIZE)

    self.render_page()

  def post(self):
    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    act = self.request.get("action")
    key = self.request.get("key")
    page = self.request.get("page")
    this_cursor = self.request.get("this_cursor")
    lead = models.Lead.get(key)
    if not lead:
      logging.warning("No lead for key %s." % key)
      return 

    if act == 'mail hardcopy':
      lead.date_hard_copy_mailed = datetime.datetime.now()
      logging.info("Lead %s flagged for hard copy mailed." % lead.email)
      lead.put()
    elif act == 'close lead':
      lead.date_closed = datetime.datetime.now()
      logging.info("Lead %s flagged for closed." % lead.email)
      lead.put()
    else:
      logging.warning("Invalid action %s." % act)
      return

    self.redirect("%s?pg=%s&cursor=%s" % (self.request.path, page, this_cursor))


class EmailAttachment(base.BasePage):
  def get(self):
    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    self.template = "file_upload.html"
    q = models.Attachment.all().filter("account =", self.account)
    q.order("-date_created")
    self.ctx['attachment'] = q.get()
    self.render_page()

  def post(self):
    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    upload = self.request.POST['file']
    # catch empty uploads since 'upload' truth eval is always False
    try:
      upload.filename
    except AttributeError:
      logging.warning("No file uploaded.")
      self.redirect("")
      return

    # add to datastore
    attachment = models.Attachment(
      account = self.account,
      data = upload.file.read(),
      filename = upload.filename,
      mime = upload.type,
      )
    attachment.put()
    logging.info("Attachment %s successfully uploaded for %s." % \
                   (upload.filename, self.user))

    self.redirect("")

    
class EmailTemplates(base.BasePage):
  
  def get(self):
    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    class DummyEmailTemplate(object):
      def __init__(self, body):
        self.subject = models.EmailTemplate.DFLT_SUBJECT
        self.body = body
      def key(self):
        return ""

    # first template
    q = models.EmailTemplate.all().filter('account =', self.account)
    q.filter('is_first_response =', True)
    q.order('-date_created')
    email_template_1 = q.get()
    if not email_template_1:
      email_template_1 = DummyEmailTemplate(models.EmailTemplate.DFLT_BODY_FIRST)

    # auto template
    q2 = models.EmailTemplate.all().filter('account =', self.account)
    q2.filter('is_first_response =', False)
    q2.order('-date_created')
    email_template_auto = q2.get()
    if not email_template_auto:
      email_template_auto = DummyEmailTemplate(models.EmailTemplate.DFLT_BODY_AUTO)

    self.template = "email_templates.html"
    self.ctx['forms'] = [
      {
        'title': 'First Email Template',
        'name': 'first',
        'key': email_template_1.key(),
        'subject': email_template_1.subject,
        'body': email_template_1.body,
       },
      {
        'title': 'Automatic Responder Email Template',
        'name': 'auto',
        'key': email_template_auto.key(),
        'subject': email_template_auto.subject,
        'body': email_template_auto.body,
        },
      ]
    
    self.render_page()

  def post(self):
    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    key = self.request.get("key", None)
    subject = cgi.escape(self.request.get("subject"))
    body = cgi.escape(self.request.get("body"))
    is_first = self.request.get("name") == 'first'

    if not key:
      template = models.EmailTemplate(account=self.account)
    else:
      template = models.EmailTemplate.get(key)
      if not template:
        logging.error("Missing template for %s." % key)
        return

    template.subject = subject
    template.body = body
    template.is_first_response = is_first

    template.put()
    self.redirect("")

    
class FileDownload(webapp.RequestHandler):
  def get(self, key):
    # don't do account access verification
    file = models.Attachment.get(key)
    
    h = self.response.headers
    h['Content-Disposition'] = 'attachment; filename=%s' % file.filename
    h['Content-Type'] = file.mime

    self.response.out.write(file.data)

    
app = webapp.WSGIApplication([
    (r'/user/lead_listing', LeadListing),
    (r'/user/email_attachment', EmailAttachment),
    (r'/user/email_templates', EmailTemplates),
    (r'/user/download/(.+)', FileDownload),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

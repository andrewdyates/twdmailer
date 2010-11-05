#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import base
import models


class LeadListing(base.BasePage):
  
  def get(self):

    Q_SIZE = 30
    self.template = "lead_listing.html"

    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    this_cursor = self.request.get("cursor", None)
    prev_cursor = self.request.get("last", None)
    
    q = models.Lead.all().filter("account =", self.account).order("-date_created")
    if this_cursor:
      q.with_cursor(this_cursor)

    leads = q.fetch(Q_SIZE)
    
    if len(leads) < Q_SIZE:
      next_cursor = None
    else:
      next_cursor = q.cursor()

    for lead in leads:
      logging.info(lead.email)
      lead.status = "Hello"

    next_link = None
      
    self.ctx['leads'] = leads
    self.ctx['next_link'] = "#"
    self.ctx['prev_link'] = "#"
    self.ctx['set_size'] = "%s" % Q_SIZE
    next_link = None
    prev_link = None
    self.render_page()


class EmailAttachment(base.BasePage):
  def get(self):
    self.content += "Stubbed. Display attachment and allow upload of new attachment."
    self.render_page()

    
class EmailTemplates(base.BasePage):
  def get(self):
    self.content += "Stubbed. Create form to change 2 email templates and confirmation message."
    self.render_page()

    
app = webapp.WSGIApplication([
    (r'/user/lead_listing', LeadListing),
    (r'/user/email_attachment', EmailAttachment),
    (r'/user/email_templates', EmailTemplates),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

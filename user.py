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

    Q_SIZE = 100
    self.template = "lead_listing.html"

    # this should be middleware in base.BasePage
    if not self.account:
      self.render_page()
      return

    cursor = self.request.get("cursor", None)
    pg = self.request.get("pg", 1)
    next_pg = "%s" % (int(pg) + 1)
    
    q = models.Lead.all().filter("account =", self.account).order("-date_created")
    if cursor:
      q.with_cursor(cursor)
    leads = q.fetch(Q_SIZE)
    
    if len(leads) < Q_SIZE:
      self.ctx['next_link'] = None
    else:
      next_cursor = q.cursor()
      self.ctx['next_link'] = "%s?cursor=%s&pg=%s" % \
        (self.request.path, next_cursor, next_pg)

    if cursor:
      self.ctx['top_link'] = self.request.path
    else:
      self.ctx['top_link'] = None

    self.ctx['leads'] = leads
    self.ctx['pg'] = pg
    self.ctx['set_size'] = str(Q_SIZE)

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

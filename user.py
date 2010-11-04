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
    """FIX THIS"""
    self.content += "STUBBED. FIX CODE<br />"

    
    if not self.account:
      # break
      self.render_page()
      return
    
    q = models.Lead.all().filter("account =", self.account).order("-date_created")
    cursor = self.request.get("cursor")
    if cursor:
      q.with_cursor(cursor)

    Q_SIZE = 30
    results = q.fetch(Q_SIZE)
    next_cursor = q.cursor()
    
    if not results and not cursor:
      self.content += "<p>No leads yet submitted.</p>"
    else:
      self.content += "<table><tr><th>email</th><th>date created</th></tr>"
      for r in results:
        self.content += "<tr><td>%s</td><td>%s</td>" % (r.email, r.date_created)
      self.content += "</table>"
      next_url = os.environ['PATH_INFO'] + "?cursor=%s" % next_cursor
      
      if results and len(results) == Q_SIZE:
        self.content += '<a href="%s">Next %s</a><br />' % (next_url, Q_SIZE)
      
      self.content += '<a href="%s">Return to Top of Results</a><br />' % os.environ['PATH_INFO']

    self.render_page()


class EmailAttachment(base.BasePage):
  def get(self):
    self.content += "Stubbed. Display attachment and allow upload of new attachment."
    self.render_page()

    
class EmailTemplates(base.BasePage):
  def get(self):
    self.content += "Stubbed. Create form to change 2 email templates."
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

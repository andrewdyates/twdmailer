#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Submit:
* Accept POST of new Lead submission.
* Assign to Account based on url
"""
import cgi
import datetime
import logging
import os
import urllib

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import mailer


# WARNING: "From" email must be authorized sender
# See: http://code.google.com/appengine/docs/python/mail/sendingmail.html
TMPL_DIR = os.path.join(os.path.dirname(__file__), "templates")
  

class Main(webapp.RequestHandler):

  def post(self, action_path):

    # CREATE LEAD
    # ==============
    lead_email = self.request.get("email", None)
    if lead_email:
      logging.info("New Lead Submission: %s" % lead_email)
    else:
      logging.error("No email for lead submission.")
      return 

    action_path = urllib.unquote(action_path)
    account = models.Account.all().filter("action_path =", action_path).get()
    if not account:
      logging.error("Invalid Account Action Path '%s'" % action_path)
      return

    lead_ctx = {}
    for key in self.request.arguments():
      if key not in models.Lead.PROTECTED:
        value = u', '.join([cgi.escape(v) for v in self.request.get_all(key)])
        lead_ctx[str(key)] = value or None
    
    # note: 'email' is required property
    lead = models.Lead(account=account, **lead_ctx)
    if not models.Lead.all().filter("email =", lead_ctx['email']).get():
      lead.put()
    else:
      logging.warning("Email %s already submitted." % lead_ctx['email'])
      return

    # GENERATE ADMIN EMAIL
    # ==============
    account_email_body = template.render(
      TMPL_DIR + "/new_lead_email.txt",
      {'lead_ctx': lead_ctx},
      )
    mail.send_mail(
      sender=mailer.BOT_EMAIL,
      to=account.user.email(),
      subject='Mail Hard Copy to New Lead',
      body=account_email_body,
      )

    # GENERATE USER EMAIL
    # ===================
    mailer.mail_lead(
      account = account,
      to_email = lead.email,
      mail_name='first',
      )
    lead.date_last_auto_ping = datetime.datetime.now()
    lead.num_auto_ping += 1
    lead.put()
    
    self.response.out.write("Thank you for your inquiry.")

    
app = webapp.WSGIApplication([
    (r'/submit/(.+?)/?', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

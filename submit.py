#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Submit:
* Accept POST of new Lead submission.
* Assign to Account based on url
"""
import cgi
import urllib
import logging
import os

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import models


# WARNING: "From" email must be authorized sender
# See: http://code.google.com/appengine/docs/python/mail/sendingmail.html
BOT_EMAIL = "mailer@twdmailer.appspotmail.com"
TMPL_PATH = os.path.join(os.path.dirname(__file__), 'templates/')


class Main(webapp.RequestHandler):

  def post(self, action_path):

    lead_email = self.request.get("email", None)
    # TODO: maybe do some email format checking here
    if lead_email:
      logging.info("New Lead Submission: %s" % lead_email)
    else:
      logging.warning("No email for lead submission.")

    action_path = urllib.unquote(action_path)
    # try fetching 2, if >1 returns, then log warning
    account = models.Account.all().filter("action_path =", action_path).get()
    if not account:
      raise ValueError("Invalid Account Action Path '%s'" % action_path)

    lead_ctx = {}
    for key in self.request.arguments():
      value = u', '.join([cgi.escape(v) for v in self.request.get_all(key)])
      lead_ctx[str(key)] = value or None
      
    # note: email is required property
    lead = models.Lead(account=account, **lead_ctx)

    if not models.Lead.all().filter("email =", lead_ctx['email']).get():
      lead.put()
      models.LeadStatus(lead=lead, key_name=lead_ctx['email']).put()
    else:
      logging.warning("Email %s already submitted.")
      return

    # email account
    account_email_body = template.render(
      TMPL_PATH + "/new_lead_email.txt",
      {'lead_ctx': lead_ctx},
      )

    mail.send_mail(
      sender=BOT_EMAIL,
      to=account.user.email(),
      subject='Mail Hard Copy to New Lead',
      body=account_email_body,
      )
    
    # email lead with attachment
    # NOTE: should pull from db for account
    lead_email_body = template.render(
      TMPL_PATH + "/default_response_email.txt",
      {'lead': lead},
      )
    # should pull from db for account
    attachment = ("sample.pdf", open(TMPL_PATH + "/sample.pdf").read())
    mail.send_mail(
      sender=BOT_EMAIL,
      to=lead.email,
      reply_to=account.user.email(),
      subject='Inquiry Response',
      body=lead_email_body,
      attachments=[attachment],
      )
    
    # display confirmation page, include back link
    # this message should also be from financial advisor
    self.response.out.write("Thank you for your inquiry.")

    
app = webapp.WSGIApplication([
    (r'/submit/(.+?)/?', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

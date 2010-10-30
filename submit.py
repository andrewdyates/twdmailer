#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Submit:
* Accept POST of new Lead submission.
* Assign to Account based on url
"""
import cgi
import logging
import os

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import models

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


class Main(webapp.RequestHandler):

  def post(self, action_path):
    logging.info("New Lead; email: %s" % self.request.get("email", None))
    
    account = models.Account.all().filter("action_path =", action_path).get()
    if not account:
      raise ValueError("Invalid Account Action Path '%s'" % account)
    
    lead = models.Lead(**{
        'account': account,
        'email': cgi.escape(self.request.get('email', '')),
        'first_name': cgi.escape(self.request.get('first_name', '')),
        'last_name': cgi.escape(self.request.get('last_name', '')),
        'phone_number': cgi.escape(self.request.get('phone_number', '')),
        'postal_address': cgi.escape(self.request.get('postal_address', '')),
        })
    lead.put()

    # email account
    account_email_body = template.render(
      TEMPLATE_DIR + "/new_lead_email.txt",
      {'lead': lead},
      )
    mail.send_mail(**{
        'to': account.user.email(),
        'subject': 'Mail Hard Copy to New Lead',
        'body': account_email_body,
        })
    
    # email lead with attachment
    # should pull from db for account
    lead_email_body = template.render(
      TEMPLATE_DIR + "/default_response_email.txt",
      {'lead': lead},
      )
    # should pull from db for account
    attachment = ("sample.pdf", open(TEMPLATE_DIR + "/sample.pdf").read())
    mail.send_mail(**{
        'to': lead.email,
        'reply_to': account.user.email(),
        'subject': 'Inquiry Response',
        'body': lead_email_body,
        'attachments': [attachment]
        })
    
    # display confirmation page, include back link
    self.response.out.write("Thank you for your inquiry, %s." % lead.first_name)



    
# ===============
app = webapp.WSGIApplication([
    (r'/submit/(.+)/?', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

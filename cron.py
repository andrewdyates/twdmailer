#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Cron: automated scheduled tasks.
Not yet debugged.
"""
import datetime
import logging
import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
# import taskqueue

import mailer
import models

MAX_MAIL = 3
RESULT_SIZE = 100

class Default(webapp.RequestHandler):
  def get(self):

    # get cursor if taskqueue
    logging.info("Default Cron Job Activated.")

    q = models.Lead.all()
    q.filter("num_auto_ping <=", MAX_MAIL)
    q.filter("date_closed =", None)

    # WARNING: this should really be in some queue with a transaction
    leads = q.fetch(RESULT_SIZE)
    logging.info("Sending %s emails in cron." % len(leads))
    for lead in leads:
      logging.info("Email #%s to %s." % (lead.num_auto_ping, lead.email))
      lead.num_auto_ping += 1
      lead.date_last_auto_ping = datetime.datetime.now()
      mailer.mail_lead(
        account = lead.account,
        to_email = lead.email,
        mail_name = 'auto',
        )
    db.put(leads) 
    
    # submit self to task queue with cursor if appropriate
    # CALCULATE CURSOR AND SUBMIT TO TASK QUEUE

  
    
app = webapp.WSGIApplication([
    (r'.*', Default),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

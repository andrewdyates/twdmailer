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
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
# import taskqueue

import models

MAX_MAIL = 3
RESULT_SIZE = 100

class Default(webapp.RequestHandler):
  def get(self):

    # get cursor if taskqueue
    
    logging.info("Default Cron Job Activated.")

    q = models.Lead.all()
    q.filter("num_auth_ping <=", MAX_MAIL)
    q.filter("date_closed =", None)

    # this should probably be done in a transaction
    leads = q.fetch(RESULT_SIZE)
    for lead in leads:
      # send followup email
      logging.debug("Email #%s to %s." % (lead.num_auth_ping, lead.email))
      r.num_auth_ping += 1
      r.date_last_auto_ping = datetime.datetime.now()
      # select template and attachments
      q2 = models.Attachment.all().filter('account =', lead.account)
      q2.order('-date_created')
      attachment = q2.get()
      
      lead.account
    db.put(leads)
    
    # submit self to task queue with cursor if appropriate
    # CALCULATE CURSOR AND SUBMIT TO TASK QUEUE


def email_lead(lead):
  
    
app = webapp.WSGIApplication([
    (r'.*', Default),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

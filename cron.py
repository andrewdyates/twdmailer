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


class Default(webapp.RequestHandler):
  def get(self):

    # get cursor if taskqueue
    
    logging.info("Default Cron Job Activated.")
    # select all LeadStatus with num_auto_ping < 3 not suspended or closed

    # BREAK
    return
    q = models.LeadStatus.all()
    q.filter("num_auth_ping <=", 3)
    q.filter("date_closed =", None)
    q.filter("date_suspend_auto_mailer =", None)

    results = q.fetch(100)
    
    for r in results:
      account = r.lead.account
      email = r.lead.email
      # send followup email
      logging.debug("Email %s from %s" % (email, account.user))
      # increment LeadStatus by 1
      r.num_auth_ping += 1
      r.date_last_auto_ping = datetime.datetime.now()
    

    # submit self to task queue with cursor if appropriate
      

    
app = webapp.WSGIApplication([
    (r'.*', Default),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

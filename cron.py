#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""Cron: automated scheduled tasks."""

import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Default(webapp.RequestHandler):
  def get(self):
    logging.debug("Default Cron Job Activated.")

    
app = webapp.WSGIApplication([
    (r'.*', Default),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

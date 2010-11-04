#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


REDIRECT_URI = "/user/lead_listing"

class Main(webapp.RequestHandler):
  def get(self):
    self.redirect(REDIRECT_URI)
    
app = webapp.WSGIApplication([
    (r'/?', Main),
    ], debug=False)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

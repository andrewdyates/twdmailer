#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
  def get(self):
    _w = self.response.out.write
    _w('<p>You have been logged out.</p>')
    _w('<p><a href="/">Main Page</a></p>')

    
app = webapp.WSGIApplication([
    (r'.*', MainPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

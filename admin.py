#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Admin: Account Crud.
"""

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
  def get(self):
    _w = self.response.out.write
    _w('<html><head><title>Toledo Web Design Mailer: Admin</title></head><body>')
    _w('List User Pages.\n')
    _w('</body></html>')

    
app = webapp.WSGIApplication([
    (r'.*', MainPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Submit:
* Accept POST of new Lead submission.
* Assign to Account based on url
"""

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
  # this should be POST
  def get(self, account):
    _w = self.response.out.write
    self.response.headers['Content-Type'] = 'text/plain'
    _w('Accepted Lead POST for Account %s.\n' % account)
    for var in self.response.arguments():
      _w("%s = %s\n" % (var, self.response.get_all(var))
    
app = webapp.WSGIApplication([
    (r'/submit/(.+)/?', MainPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

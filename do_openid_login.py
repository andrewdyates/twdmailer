#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""OpenID Login. To Be Implemented."""

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Open ID Login page\n')
    self.response.out.write(users.create_login_url())
    self.response.out.write('\n===\n')
    self.response.out.write(users.create_logout_url('/'))

    
app = webapp.WSGIApplication([
    (r'.*', MainPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

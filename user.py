#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""User:
* Must be logged in as active user account
* Admin can view any user page
* View List of lead pages
* If Admin, include suspension / activation link
* Lead pages include demographics and status information
"""

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
  def get(self):
    _w = self.response.out.write
    self.response.headers['Content-Type'] = 'text/plain'
    user = users.get_current_user()
    _w('Hello User %s.\n' % user)

class LeadPage(webapp.RequestHandler):
  def get(self, lead):
    _w = self.response.out.write
    self.response.headers['Content-Type'] = 'text/plain'
    _w('Lead %s.\n' % lead)

    
app = webapp.WSGIApplication([
    (r'/user/?', MainPage),
    (r'/user/lead/(.+)/?', LeadPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

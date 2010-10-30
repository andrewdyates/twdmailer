#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""OpenID Login. To Be Implemented."""

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


TMPL_PATH = os.path.join(os.path.dirname(__file__), 'templates/')

class Main(webapp.RequestHandler):
  def get(self):
    _w = self.response.out.write
    auth = {
      'user': users.get_current_user(),
      'login_url': users.create_login_url(os.environ['PATH_INFO']),
      'logout_url': users.create_logout_url('/logged_out'),
      }
    title = "Log in with OpenID"
    default_openid_url = "gmail.com"
    _w(template.render(TMPL_PATH + "login.html", locals()))

    
app = webapp.WSGIApplication([
    (r'.*', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

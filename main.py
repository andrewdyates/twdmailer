#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
  def get(self):
    _w = self.response.out.write
    self.response.headers['Content-Type'] = 'text/plain'
    _w('Hello, webapp World!\n')
    _w('User: %s\n' % users.get_current_user())
    _w("logout: " + users.create_logout_url('/no') + "\n")
    _w("login: " + users.create_login_url('/') + "\n")
    user = users.get_current_user()
    if user:
      _w("user.nickname(): %s\n" % user.nickname())
      _w("user.email(): %s\n" % user.email())
      _w("user.user_id(): %s\n" % user.user_id())
      _w("user.federated_identity(): %s\n" % user.federated_identity())
      _w("user.federated_provider(): %s\n" % user.federated_provider())
      _w("is_current_user_admin(): %s\n" % users.is_current_user_admin())
    else:
      _w("No User Login")

    _w('\n===\n')

    for k, v in os.environ.items():
      _w("%s = %s\n" % (k, v))

    
app = webapp.WSGIApplication([
    (r'.*', MainPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

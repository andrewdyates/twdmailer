#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Super: Bootstrap application by adding current user as an Account
with admin access.
"""
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import models

PATH = os.path.join(os.path.dirname(__file__), 'templates/super.html')


def add_su_account():
  """Add logged-in (super) user as an admin Account."""
  user = users.get_current_user()
  # check to see if user already exists
  if models.Account.all().filter("user =", user).get():
    raise ValueError("Account for user %s already exists." % user)
  su = models.Account(
    title = user.nickname(),
    action_path = user.nickname(),
    user = user,
    is_admin = True,
    )
  su.put()
  return su
  
class Main(webapp.RequestHandler):
  def get(self, message=None):
    _w = self.response.out.write
    try:
      su = add_su_account()
    except ValueError, e:
      msg = "ERROR: %s" % e
    else:
      msg = "SUCCESS: Admin Account '%s' created." % su.title
    _w(template.render(PATH, {'msg': msg, 'user': users.get_current_user()}))

    
app = webapp.WSGIApplication([
    (r'.*', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)
  
if __name__ == '__main__':
  main()

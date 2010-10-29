#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Super: Create Admin Accounts.
"""

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import models

  
class MainPage(webapp.RequestHandler):
  """Print admin promotion form."""

  def get(self, message=None):
    """Print admin promotion form."""
    _w = self.response.out.write
    path = os.path.join(os.path.dirname(__file__), 'templates/super.html')
    _w(template.render(path, locals()))

  def post(self):
    """Create or update Account with admin status."""
    email = self.request.get("email")
    user = users.User(email=email)
    query = models.Account.all().filter("user =", user)
    account = query.get()
    
    if not account:
      try:
        account = models.Account(user=user, is_admin=True)
      except db.BadValueError, e:
        self.get(message="Error: %s" % e)
      else:
        account.put()
        self.get(message="Account %s created as admin." % email)
    else:
      if account.is_admin:
        self.get(message="Account %s is already an admin." % email)
      else:
        Account.is_admin = True
        account.put()
        self.get(message="Account %s is now an admin." % email)

    
app = webapp.WSGIApplication([
    (r'.*', MainPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

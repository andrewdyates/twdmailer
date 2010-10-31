#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""OpenID Login Auto Redirect: gmail.com"""

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Main(webapp.RequestHandler):
  def get(self):
    continue_url = self.request.GET.get('continue') or '/'
    openid_url = 'gmail.com'
    self.redirect(users.create_login_url(continue_url, None, openid_url))

    
app = webapp.WSGIApplication([
    (r'.*', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

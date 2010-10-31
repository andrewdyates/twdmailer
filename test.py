#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""Sample test form to confirm submit handler functionality."""

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


TMLT_PATH = os.path.join(os.path.dirname(__file__), 'templates')

class Main(webapp.RequestHandler):
  
  def get(self):
    _w = self.response.out.write
    user = users.get_current_user()
    ctx = {
      'action_path': user.nickname(),
      }
    _w(template.render(TMLT_PATH + "/test_form.html", ctx))


app = webapp.WSGIApplication([
    (r'.*', Main),
    ], debug=True)

def main():
  run_wsgi_app(app)
  
if __name__ == '__main__':
  main()

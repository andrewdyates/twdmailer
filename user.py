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
import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import models


TMPL_PATH = os.path.join(os.path.dirname(__file__), 'templates/')

class MainPage(webapp.RequestHandler):
  def get(self):
    _w = self.response.out.write
    user = users.get_current_user()
    auth = {
      'user': user,
      'login_url': users.create_login_url(os.environ['PATH_INFO']),
      'logout_url': users.create_logout_url('/logged_out'),
      'is_admin': users.is_current_user_admin(),
      }
    title = "%s User Page" % user
    content = ""

    # get Account for user
    q = models.Account.all().filter("user =", user).filter("is_active =", True)
    account = q.get()
    if not account:
      logging.warning("Logged in user %s does not have an account. Try /super?" % user)
      content += "<p>No active account exists for user %s." + \
        "Contact an administrator to activate your account.</p>"
      q = models.Account.all().filter("user =", user).filter("is_active", False)
      if not q.get():
        new_account = models.Account(
          title = user.nickname(),
          action_path = user.nickname(),
          user = user,
          is_active = False,
          )
        new_account.put()
        logging.info("Inactive Account for user %s created." % user)
      # BREAK
      return 

    content = "<h1>%s User Page</h1>" % user
    
    # list leads
    content += "<h3>Leads</h3>"
    q = models.Lead.all().filter("account =", account).order("-date_created")
    cursor = self.request.get("cursor")
    if cursor:
      q.with_cursor(cursor)

    Q_SIZE = 30
    results = q.fetch(Q_SIZE)
    next_cursor = q.cursor()
    
    if not results and not cursor:
      content += "<p>No leads yet submitted.</p>"
    else:
      content += "<table><tr><th>email</th><th>date created</th></tr>"
      for r in results:
        content += "<tr><td>%s</td><td>%s</td>" % (r.email, r.date_created)
      content += "</table>"
      next_url = os.environ['PATH_INFO'] + "?cursor=%s" % next_cursor
      
      if results and len(results) == Q_SIZE:
        content += '<a href="%s">Next %s</a><br />' % (next_url, Q_SIZE)
      
      content += '<a href="%s">Return to Top of Results</a><br />' % os.environ['PATH_INFO']

      
    
    # settings page for attachments, email contents
    ctx = {'auth': auth, 'content': content, 'title': title}
    _w(template.render(TMPL_PATH + "base.html", ctx))


class LeadPage(webapp.RequestHandler):
  def get(self, lead):
    _w = self.response.out.write
    self.response.headers['Content-Type'] = 'text/plain'
    _w('Lead %s.\n' % lead)

    
app = webapp.WSGIApplication([
    (r'/?', MainPage),
    (r'/user/lead/(.+)/?', LeadPage),
    ], debug=True)

def main():
  run_wsgi_app(app)

if __name__ == '__main__':
  main()

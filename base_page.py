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


TMPL_DIR = os.path.join(os.path.dirname(__file__), "templates")


class BasePage(webapp.RequestHandler):

  def __init__(self, *args, **kwds):
    """Initialize an empty page."""
    super(BasePage, self).__init__(*args, **kwds)
    self.template_name = "base.html"
    self.content = ""
    self.message = ""
    self.title = self.get_default_title()
    self.auth = None
    self.account = None
    self.ctx = {}
    self.page = self.get_page_slug()
    self.user = users.get_current_user()
    # generate contexts
    self.make_auth_ctx()
    self.make_account_ctx(self.user)

  @classmethod
  def get_page_slug(cls):
    """Return string slug for URI.

    Returns:
      str: slug of current URI
    """
    uri = os.environ['PATH_INFO']
    slug = uri.partition('?')[0].partition('#')[0]
    slug = slug.lstrip('/')
    slug = slug.replace('/', '__')
    return slug

  @classmethod
  def get_default_title(cls):
    """Return default title from page slug.

    Returns:
      str: title generated from slug name
    """
    slug = cls.get_page_slug()
    title = slug.rpartition('__')[2]
    title = ' '.join([w.capitalize() for w in title.split('_')])
    return title
    
  def make_auth_ctx(self):
    """Fetch and configure self.auth for current user."""
    if "Development" in os.environ['SERVER_SOFTWARE']:
      super_url = "http://%s%s" % (os.environ['HTTP_HOST'], "/_ah/admin")
    else:
      super_url = "https://appengine.google.com/dashboard?&app_id=%s" % \
        os.environ['APPLICATION_ID']
    self.auth = {
      'user': self.user,
      'login_url': users.create_login_url(os.environ['PATH_INFO']),
      'logout_url': users.create_logout_url('/logged_out'),
      'is_super': users.is_current_user_admin(),
      'super_url': super_url,
      }
    
  def make_account_ctx(self, user):
    """Fetch and verify self.account for current user."""
    q = models.Account.all().filter("user =", user).filter("is_active =", True)
    account = q.get()
    if account:
      self.account = account
    else:
      logging.warning("No active account exists for logged in user %s." % user)
      self.message += "No active account exists for user %s. " % user
      if users.is_current_user_admin():
        self.message += '<a href="/super/bootstrap_superuser">' + \
          "<br />Bootstrap Superuser to create an account.</a>"
      else:
        self.message += "<br />Contact an administrator to activate your account."
      # create default inactive account for this user if it does not exist
      q = models.Account.all().filter('user =', user).filter('is_active', False)
      if not q.get():
        new_account = models.Account(
          title = user.nickname(),
          action_path = user.nickname(),
          user = user,
          is_active = False,
          )
        new_account.put()
        logging.info("Inactive Account for user %s created." % user)
        
  def render_page(self):
    ctx = {
      'auth': self.auth,
      'content': self.content,
      'title': self.title,
      'message': self.message,
      'page': self.page,
      }
    ctx.update(self.ctx)
    _w = self.response.out.write
    _w(template.render("%s/%s" % (TMPL_DIR, self.template_name), ctx))

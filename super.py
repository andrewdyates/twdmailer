#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
"""Super: Bootstrap application by adding current user as an Account
with admin access.
"""
import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import base
import models


class BootstrapSuperuser(base.BasePage):
  """Add logged-in (super) user as super Account."""
  def get(self):
    account = models.Account.all().filter("user =", self.user).get()
    if self.account:
      if account.is_active:
        self.message += "Active account %s already exists." % self.user
      else:
        account.is_active = True
        account.put()
        msg = "SUCCESS: Account for %s activated." % self.user
        # overwrite possible "No active account exists" message
        self.message = "SUCCESS: Account for %s activated." % self.user
        logging.info(msg)
    else:
      logging.warning("base.BasePage makes stub user, so this shouldn't run.")
    self.render_page()

    
class ManageAccounts(base.BasePage):
  def get(self):
    self.content += "Stubbed. List accounts here."
    self.render_page()

    
class TestForms(base.BasePage):
  def get(self):
    self.template = "test_form.html"
    self.ctx = {
      'action_path': self.user.nickname(),
      }
    self.render_page()

    
app = webapp.WSGIApplication([
    (r'/super/bootstrap_superuser', BootstrapSuperuser),
    (r'/super/manage_accounts', ManageAccounts),
    (r'/super/test_forms', TestForms),
    ], debug=True)

def main():
  run_wsgi_app(app)
  
if __name__ == '__main__':
  main()

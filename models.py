#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
# Copyright © 2010 Andrew D. Yates
import os

from google.appengine.ext import db


TMPL_DIR = os.path.join(os.path.dirname(__file__), "templates")


class Account(db.Model):
  """Authenticated login like clients and admins."""
  # action_path should be unique
  action_path = db.StringProperty()
  user = db.UserProperty(required=True)
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_updated = db.DateTimeProperty(auto_now=True)
  is_active = db.BooleanProperty(default=True)


class Lead(db.Expando):
  """Submitted user contact information."""
  PROTECTED = (
    'date_created',
    'date_updated',
    'date_hard_copy_mailed',
    'date_closed',
    'date_last_auto_ping',
    'num_auto_ping',
    )
  email = db.EmailProperty(required=True)
  account = db.ReferenceProperty(Account, required=True)
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_updated = db.DateTimeProperty(auto_now=True)
  date_hard_copy_mailed = db.DateTimeProperty()
  date_closed = db.DateTimeProperty()
  date_last_auto_ping = db.DateTimeProperty()
  num_auto_ping = db.IntegerProperty(default=0)


class Attachment(db.Model):
  """An email attachment file."""
  DFLT_FILENAME = "sample.pdf"
  DFLT_MIME = "application/pdf"
  DFLT_DATA = open(os.path.join(TMPL_DIR, DFLT_FILENAME)).read()
  account = db.ReferenceProperty(Account, required=True)
  data = db.BlobProperty(required=True)
  filename = db.StringProperty(required=True)
  mime = db.StringProperty(required=True)
  date_created = db.DateTimeProperty(auto_now_add=True)

  
class EmailTemplate(db.Model):
  """A stock automated email message."""
  DFLT_SUBJECT = "Follow Up"
  DFLT_BODY_FIRST_FILE = os.path.join(TMPL_DIR, "default_response_email.txt")
  DFLT_BODY_AUTO_FILE = os.path.join(TMPL_DIR, "default_ping_email.txt")
  DFLT_BODY_FIRST = open(DFLT_BODY_FIRST_FILE).read()
  DFLT_BODY_AUTO = open(DFLT_BODY_AUTO_FILE).read()
  account = db.ReferenceProperty(Account, required=True)
  subject = db.StringProperty()
  body = db.TextProperty()
  is_first_response = db.BooleanProperty()
  date_updated = db.DateTimeProperty(auto_now=True)
  date_created = db.DateTimeProperty(auto_now_add=True)

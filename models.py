#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

from google.appengine.ext import db


class Account(db.Model):
  """Authenticated login like clients and admins."""
  name = db.StringProperty()
  email = db.UserProperty(required=True)
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_updated = db.DateTimeProperty(auto_now=True)
  is_active = db.BooleanProperty(default=True)
  is_admin = db.BooleanProperty(default=False)


class Lead(db.Expando):
  """Submitted user contact information."""
  email = db.EmailProperty(required=True)
  account = db.ReferenceProperty(Account, required=True)
  first_name = db.StringProperty()
  last_name = db.StringProperty()
  phone_number = db.PhoneNumberProperty()
  postal_address = db.PostalAddressProperty()
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_updated = db.DateTimeProperty(auto_now=True)
  date_deleted = db.DateTimeProperty()

  # lead status
  date_hard_copy_mailed = db.DateTimeProperty()
  date_suspend_auto_mailer = db.DateTimeProperty()
  date_closed = db.DateTimeProperty()
  date_slowed_ping = db.DateTimeProperty()
  date_last_auto_ping = db.DateTimeProperty()
  num_auto_ping = db.IntegerProperty()
  notes = db.TextProperty()


class Attachment(db.Model):
  """An email attachment file."""
  account = db.ReferenceProperty(Account, required=True)
  data = db.BlobProperty(required=True)
  filename = db.StringProperty(required=True)
  date_created = db.DateTimeProperty(auto_now_add=True)

  
class EmailMessage(db.Model):
  """A stock automated email message."""
  account = db.ReferenceProperty(Account)
  sequence_num = db.IntegerProperty()
  is_default = db.BooleanProperty(default=False)
  reply_to = db.EmailProperty()
  subject = db.StringProperty(default="Follow Up")
  attachment = db.ReferenceProperty(Attachment)
  body = db.TextProperty(required=True)
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_updated = db.DateTimeProperty(auto_now=True)
__author__ = 'pdiazv'

#from enum import Enum
from google.appengine.ext import ndb

class Activity(ndb.Model):
    type = ndb.StringProperty(required=True)


class ReferenceTracker(ndb.Model):
    name = ndb.StringProperty(required=True)
    auth_url = ndb.StringProperty()


class NimbbleUser(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)


class NimbbleTracker(ndb.Model):
    name = ndb.StringProperty()           # strava, runtastic...
    token = ndb.StringProperty()          # the auth token to make api calls.
    client_id = ndb.StringProperty()      # the id of the user to auth against the tracker api

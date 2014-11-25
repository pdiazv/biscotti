__author__ = 'pdiazv'

#from enum import Enum
from google.appengine.ext import ndb

class Activity(ndb.Model):
    type = ndb.StringProperty(required=True)

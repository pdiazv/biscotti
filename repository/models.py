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
    group = ndb.StringProperty()
    pic = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def delete_all(cls):
        ndb.delete_multi(cls.query().fetch(keys_only=True))


class NimbbleTracker(ndb.Model):
    name = ndb.StringProperty(required=True)           # strava, runtastic...
    token = ndb.StringProperty()          # the auth token to make api calls.
    client_id = ndb.StringProperty()      # the id of the user to auth against the tracker api

    @classmethod
    def delete_all(cls):
        ndb.delete_multi(cls.query().fetch(keys_only=True))

    @classmethod
    def add_all(cls, trackers):
        ndb.put_multi(trackers)

class NimbbleActivity(ndb.Model):
    datetime = ndb.DateTimeProperty(required=True)
    type = ndb.StringProperty(required=True)   #run-bike
    source = ndb.StringProperty(required=True) #strava-runtastics
    distance = ndb.FloatProperty()
    duration = ndb.TimeProperty()
    points = ndb.FloatProperty()
    data = ndb.JsonProperty()


    def serialize(self):
        user = self.key.parent().get()

        act_dic = self.to_dict()
        act_dic['user'] = user.to_dict()
        act_dic['user']['id'] = user.key.id()

        return act_dic


    @classmethod
    def delete_all(cls):
        ndb.delete_multi(cls.query().fetch(keys_only=True))

    @classmethod
    def add_all(cls, activities):
        ndb.put_multi(activities)
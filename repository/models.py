#from enum import Enum
import math
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
    picture = ndb.StringProperty()
    points = ndb.FloatProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def delete_all(cls):
        ndb.delete_multi(cls.query().fetch(keys_only=True))

    def updateScore(self):
        activities = NimbbleActivity.query(ancestor=self.key, projection=[NimbbleActivity.points]).fetch()
        self.points = sum([activity.points for activity in activities])
        self.put()



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
    source_id = ndb.StringProperty()
    source_url = ndb.StringProperty()
    distance = ndb.FloatProperty()
    duration = ndb.FloatProperty()
    duration_str = ndb.StringProperty()
    points = ndb.FloatProperty()
    data = ndb.JsonProperty()

    def get_user_dic(self):
        user = self.key.parent().get()
        user_dic = user.to_dict()
        user_dic['id'] = user.key.id()
        return user_dic

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
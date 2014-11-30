__author__ = 'pdiazv'

from business.trackers import strava
from repository import context

class TrackerManager(object):

    def list(self):
        return [
            {'name': 'strava', 'auth_url': strava.StravaTracker().get_auth_url()},
            {'name': 'runtastic', 'auth_url': ''},
            {'name': 'fitbit', 'auth_url': ''},
        ]


    def user_trackers(self, user_id):
        return context.UserContext().get_user_trackers(user_id)
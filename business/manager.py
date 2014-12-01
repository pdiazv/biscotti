__author__ = 'pdiazv'

from business.trackers import strava
from repository import context

class TrackerManager(object):

    def list(self, user_id):
        tracker_names = self.tracker_names()
        user_trackers = self.user_trackers(user_id)

        tracker_data = []

        for tracker_name in tracker_names:
            tracker = self.get_tracker(tracker_name, user_id, user_trackers)
            tracker_data.append(tracker)

        return tracker_data


    def sample_data(self, tracker_name, user_id):
        if tracker_name == 'strava':
            return strava.StravaTracker().sample_data(user_id)

        return {
            'athlete': {},
            'activities': []
        }


    def get_tracker(self, tracker_name, user_id, user_trackers):
        return {
            'name': tracker_name,
            'active': tracker_name in user_trackers,
            'auth_url': self.get_auth_url(tracker_name, user_id),
            'sample_url': self.get_sample_url(tracker_name, user_id)
        }


    def get_auth_url(self, tracker_name, user_id):
        if tracker_name == 'strava':
            return strava.StravaTracker().get_auth_url()

        return '#'


    def get_sample_url(self, tracker_name, user_id):
        return '#'


    def user_trackers(self, user_id):
        return context.UserContext().get_user_trackers(user_id)


    def tracker_names(self):
        return [
            'strava',
            'runtastic',
            'BodyMedia',
            'DailyMile',
            'FatSecret',
            'Fitbug',
            'Garmin',
            'Nike+',
            'Jawbone UP',
            'Moves',
        ]
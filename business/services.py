from business.trackers import strava
from business.calculators import StravaActivityCalculator
from repository import context
from datetime import datetime

class SyncService(object):

    def sync(self, tracker_id, user_id):

        if tracker_id != 'strava':
            return

        user = context.UserCtxManager().get(user_id)
        StravaSyncService().sync(user)

        user.updateScore()



class StravaSyncService(object):

    def sync(self, user):
        calc = StravaActivityCalculator()
        data = strava.StravaSampleDataProvider().get_activities(user.key.id())

        for activity in data:
            self.AddStravaActivity(user.key, calc, activity)


    def AddStravaActivity(self, user_key, calc, sv_activity):

        activity = {
            'datetime': datetime.strptime(sv_activity['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
            'type': sv_activity['type'],
            'source': 'strava',
            'distance': self.convert_to_miles(sv_activity['distance']),
            'duration': sv_activity['moving_time'],
            'duration_str': self.get_duration_str(sv_activity['moving_time']),
            'source_id': sv_activity['external_id'],
            'source_url': 'https://www.strava.com/activities/{0}'.format(sv_activity['id']),
            'points': calc.calculate(sv_activity)
        }

        context.ActivityContext().add(user_key, activity)
        return activity


    def convert_to_miles(self, distance):
        return distance * 0.000621371

    def get_duration_str(self, time):
        hours, rem_secs = time / 3600, time % 3600
        mins, secs = rem_secs / 60, rem_secs % 60

        return '{0:02d}:{1:02d}:{2:02d}'.format(hours, mins, secs)







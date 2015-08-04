from business.trackers import strava
from business.calculators import StravaActivityCalculator
from repository import context
from datetime import datetime

class SyncService(object):

    def sync(self, tracker_id, user_id):

        if tracker_id != 'strava':
            return;

        user = context.UserCtxManager().get(user_id)
        StravaSyncService().sync(user)

        user.updateScore()



class StravaSyncService(object):

    def sync(self, user):

        calc = StravaActivityCalculator()
        data = strava.StravaSampleDataProvider().get_activities(user.key.id())

        [self.AddStravaActivity(user.key, calc, activity) for activity in data]


    def AddStravaActivity(self, user_key, calc, sv_activity):

        activity = {
            'datetime': datetime.strptime(sv_activity['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
            'type': sv_activity['type'],
            'source': 'strava',
            'distance': self.convert_to_miles(sv_activity['distance']),
            'duration': self.convert_to_hours(sv_activity['moving_time']),
            'source_id': sv_activity['external_id'],
            'source_url': 'https://www.strava.com/activities/{0}'.format(sv_activity['id']),
            'points': calc.calculate(sv_activity)
        }

        context.ActivityContext().add(user_key, activity)


    def convert_to_miles(self, distance):
        return distance * 0.000621371

    def convert_to_hours(self, time):
        return time / 3600






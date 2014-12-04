__author__ = 'pdiazv'

from django.core.urlresolvers import reverse
from stravalib.client import Client
from business import conf
from repository import context
import json


class StravaTracker(object):

    auth_view = 'strava_auth'

    def get_auth_url(self):
        client = Client()

        path = reverse('{0}:{1}'.format(conf.auth_namespace, self.auth_view))
        redirect_to = '{0}{1}'.format(conf.auth_domain, path)

        return client.authorization_url(client_id=conf.strava['client_id'], redirect_uri=redirect_to)


    def sample_data(self, user_id):
        return StravaSampleDataProvider().get_data(user_id)

    def add_tracker(self, user_id, code):
        client = Client()
        token = client.exchange_code_for_token(
            client_id=conf.strava['client_id'],
            client_secret=conf.strava['secret'],
            code=code)

        client.access_token = token
        athlete = client.get_athlete()

        return context.UserContext().add_tracker(user_id, {
            'name': 'strava',
            'token': token,
            'client_id': str(athlete.id)
        })


class StravaSampleDataProvider(object):
    def get_data(self, user_id):
        nimbble_tracker = context.UserContext().get_tracker('strava', user_id)

        client = Client(nimbble_tracker.token)
        athlete = client.get_athlete()
        activities = client.get_activities()

        athlete['raw'] = json.dumps(athlete, indent=4)

        return {
            'athlete': athlete,
            'activities': self.get_activity_list(activities),
        }

    def get_activity_list(self, activities):
        result = []
        for act in activities:
            act['raw'] = json.dumps(act, indent=4)
            result.append(act)

        return result
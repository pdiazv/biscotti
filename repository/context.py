
from datetime import datetime, timedelta
from repository.models import NimbbleUser, NimbbleTracker, NimbbleActivity


class DemoContext(object):

    def parse_sample_data(self, data):

        NimbbleUser.delete_all()
        NimbbleActivity.delete_all()
        NimbbleTracker.delete_all()

        for record in data:
            user_key = self.add_employee(record['employee'])
            self.add_activities(user_key, record['activities'])
            self.add_trackers(user_key, record['trackers'])

        return {
            'user_count': NimbbleUser.query().count(limit=200),
            'activity_count': NimbbleActivity.query().count(limit=5000),
            'tracker_count': NimbbleTracker.query().count(limit=5000)
        }


    def add_employee(self, data):
        return UserCtxManager().add(**data)


    def add_activities(self, user_key, data):
        acts = [self.get_activity(user_key, activity) for activity in data]
        NimbbleActivity.add_all(acts)


    def add_trackers(self, user_key, data):
        trackers = [self.get_tracker(user_key, tracker) for tracker in data]
        NimbbleTracker.add_all(trackers)


    def get_activity(self, user_key, data):
        nimbble_activity = NimbbleActivity(parent=user_key)

        data['datetime'] = datetime.strptime(data['dateStr'], '%m/%d/%Y')
        data['duration'] = datetime.strptime(data['durationStr'], '%H:%M:%S').time()
        del data['dateStr']
        del data['durationStr']

        nimbble_activity.populate(**data)

        return nimbble_activity


    def get_tracker(self, user_key, data):
        nimbble_tracker = NimbbleTracker(parent=user_key)
        nimbble_tracker.populate(**data)

        return nimbble_tracker


class UserContext(object):

    def get_user(self, user_id):
        return UserCtxManager().get(user_id)

    def get_random_user(self):
        return UserCtxManager().get_random_user()
        
    def add_user(self, user):
        key = UserCtxManager().add(**user)
        return key.id()

    def get_tracker(self, name, user_id):
        user = self.get_user(user_id)
        return TrackerCtxManager().get(user.key, name)

    def get_user_trackers(self, user_id, limit=50):
        user = self.get_user(user_id)
        return TrackerCtxManager().list_by_user(user.key, limit)

    def add_tracker(self, user_id, tracker):
        user = self.get_user(user_id)
        return TrackerCtxManager().add(user.key, tracker)



class ActivityContext(object):

    def recent(self, *args, **kwargs):

        end_date = datetime.today()
        if 'end_date' in kwargs:
            end_date = datetime.strptime(kwargs['end_date'], '%m/%d/%Y')

        starting_date = end_date - timedelta(days=30)
        if 'starting_date' in kwargs:
            starting_date = datetime.strptime(kwargs['starting_date'], '%m/%d/%Y')

        query = NimbbleActivity.query()
        query.filter(NimbbleActivity.datetime >= starting_date and NimbbleActivity.datetime <= end_date)


        limit = kwargs['limit'] if 'limit' in kwargs else 15

        return query.order(-NimbbleActivity.datetime).fetch(limit=limit)

    def by_user(self, user_key, limit=15):
        query = NimbbleActivity.query(ancestor=user_key)
        return query.order(-NimbbleActivity.datetime).fetch(limit=limit)

    def by_group(self, group, limit=14):
        user_ids = NimbbleUser.query(NimbbleUser.group == group).fetch(keys_only=True)
        activities_by_user = [NimbbleActivity.query(ancestor=user_id).fetch() for user_id in user_ids]
        all_activities = sorted([j for i in activities_by_user for j in i], key=lambda x: x.datetime, reverse=True)
        return all_activities[:limit]

import random
class UserCtxManager(object):

    def get(self, user_id):
        return NimbbleUser.get_by_id(id=user_id)

    def get_random_user(self):
        rnum = random.randrange(0,50)
        nnum = 0

        for u in NimbbleUser.query().iter():
            if nnum == rnum:
                return u
            nnum += 1

    def add(self, *args, **kwargs):
        existing = NimbbleUser.query().filter(NimbbleUser.name == kwargs['name']).get()

        if existing:
            return existing.key

        user = NimbbleUser()
        user.populate(**kwargs)

        key = user.put()
        return key


class TrackerCtxManager(object):

    def get(self, user_key, name):
        query = NimbbleTracker.query(ancestor=user_key)

        return query.filter(NimbbleTracker.name == name).get()


    def add(self, user_key, tracker):
        nimbble_tracker = NimbbleTracker.get_by_id(tracker['name'], parent=user_key)

        if not nimbble_tracker:
            nimbble_tracker = NimbbleTracker(parent=user_key, id=tracker['name'])

        nimbble_tracker.name = tracker['name']
        nimbble_tracker.token = tracker['token']
        nimbble_tracker.client_id = tracker['client_id']

        return nimbble_tracker.put()


    def list_by_user(self, user_key, limit):
        trackers = NimbbleTracker.query(ancestor=user_key).fetch(limit=limit)

        names = []
        [names.append(tracker.name) for tracker in trackers]

        return names
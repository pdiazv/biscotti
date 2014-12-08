
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

        data['datetime'] = datetime.strptime(data['datetime'], '%m/%d/%Y')
        data['duration'] = datetime.strptime(data['duration'], '%H:%M:%S').time()
        nimbble_activity.populate(**data)

        return nimbble_activity


    def get_tracker(self, user_key, data):
        nimbble_tracker = NimbbleTracker(parent=user_key)
        nimbble_tracker.populate(**data)

        return nimbble_tracker


class UserContext(object):

    def get_user(self, user_id):
        return UserCtxManager().get(user_id)


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

        return query.order(-NimbbleActivity.datetime).fetch(limit=15)

    def by_user(self, user_key):
        query = NimbbleActivity.query(ancestor=user_key)
        return query.order(-NimbbleActivity.datetime).fetch(limit=15)


class UserCtxManager(object):
    def get(self, user_id):
        return NimbbleUser.get_by_id(id=user_id)


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
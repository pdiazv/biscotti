
from datetime import datetime
from repository.models import NimbbleUser, NimbbleTracker, NimbbleActivity



class DemoContext(object):
    def add_employee(self, data):
        return UserManager().add(**data)


    def add_activities(self, user_id, data):
        [self.add_activity(user_id, activity) for activity in data]


    def add_activity(self, user_id, data):
        user = UserManager().get(user_id)
        nimbble_activity = NimbbleActivity(parent=user.key)

        data['datetime'] = datetime.strptime(data['datetime'], '%m/%d/%Y')
        data['duration'] = datetime.strptime(data['duration'], '%H:%M:%S').time()
        nimbble_activity.populate(**data)

        nimbble_activity.put()


class UserContext(object):

    def get_user(self, user_id):
        return UserManager().get(user_id)


    def add_user(self, *args, **kwargs):
        return UserManager().add(kwargs)


    def get_tracker(self, name, user_id):
        user = self.get_user(user_id)
        return TrackerManager().get(user.key, name)


    def get_user_trackers(self, user_id, limit=50):
        user = self.get_user(user_id)
        return TrackerManager().list_by_user(user.key, limit)


    def add_tracker(self, user_id, tracker):
        user = self.get_user(user_id)
        return TrackerManager().add(user.key, tracker)



class UserManager(object):
    def get(self, user_id):
        return NimbbleUser.get_by_id(id=user_id)


    def add(self, *args, **kwargs):
        existing = NimbbleUser.query().filter(NimbbleUser.name == kwargs['name']).get()

        if existing:
            return existing.key.id()

        user = NimbbleUser()
        user.populate(**kwargs)

        key = user.put()
        return key.id()



class TrackerManager(object):

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
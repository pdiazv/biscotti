__author__ = 'pdiazv'

from repository.models import NimbbleUser, NimbbleTracker


class UserContext(object):

    def get_user(self, user_id):
        return NimbbleUser.get_by_id(id=user_id)


    def get_user_trackers(self, user_id, limit=50):
        user = self.get_user(user_id)
        trackers = NimbbleTracker.query(ancestor=user.key).fetch(limit=limit)

        names = []
        [names.append(tracker.name) for tracker in trackers]

        return names


    def add_user(self, *args, **kwargs):
        existing = NimbbleUser.query().filter(NimbbleUser.name == kwargs['name']).get()

        if existing:
            return existing.key.id()

        user = NimbbleUser()
        user.populate(**kwargs)

        key = user.put()
        return key.id()


    def add_tracker(self, user_id, tracker):
        user = self.get_user(user_id)

        nimbble_tracker = NimbbleTracker.get_by_id(tracker['name'], parent=user.key)

        if not nimbble_tracker:
            nimbble_tracker = NimbbleTracker(parent=user.key, id=tracker['name'])

        nimbble_tracker.name = tracker['name']
        nimbble_tracker.token = tracker['token']
        nimbble_tracker.client_id = tracker['client_id']

        return nimbble_tracker.put()



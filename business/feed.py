from repository import context, cache

class ActivityFeed(object):

    cache_key = 'recent:global'

    def recent(self, *args, **kwargs):
        nimbble_cache = cache.NimbbleCache()
        result = nimbble_cache.getItem(self.cache_key)

        if result:
            return result

        activities = context.ActivityContext().recent(**kwargs)
        result = [activity.serialize() for activity in activities]

        nimbble_cache.setItem(self.cache_key, result)

        return result


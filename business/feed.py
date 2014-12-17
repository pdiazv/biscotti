from repository import context, cache

class ActivityFeed(object):


    def recent(self, *args, **kwargs):
        cache_key = 'recent:' + kwargs['namespace'] if 'namespace' in kwargs else 'global'
        nimbble_cache = cache.NimbbleCache()
        result = nimbble_cache.getItem(cache_key)

        if result:
            return result

        activities = context.ActivityContext().recent(**kwargs)
        result = [activity.serialize() for activity in activities]

        nimbble_cache.setItem(cache_key, result)

        return result

    def activities_by_user(self, user_key):
        cache_key = 'user:' + str(user_key.id())
        nimbble_cache = cache.NimbbleCache()
        result = nimbble_cache.getItem(cache_key)

        if result:
            return result

        activities = context.ActivityContext().by_user(user_key)
        result = [activity.serialize() for activity in activities]

        nimbble_cache.setItem(cache_key, result)

        return result

    def activities_by_group(self, group):
        cache_key = 'group:' + str(group)
        nimbble_cache = cache.NimbbleCache()
        result = nimbble_cache.getItem(cache_key)

        if result:
            return result

        activities = context.ActivityContext().by_group(group)
        result = [activity.serialize() for activity in activities]

        nimbble_cache.setItem(cache_key, result)

        return result      

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

    def activities_by_user(self, user_key, limit=15, namespace='local'):
        cache_key = 'user:{0}:{1}'.format(namespace, str(user_key.id()))
        nimbble_cache = cache.NimbbleCache()
        result = nimbble_cache.getItem(cache_key)

        if result:
            return result

        activities = context.ActivityContext().by_user(user_key, limit)
        result = [activity.serialize() for activity in activities]

        nimbble_cache.setItem(cache_key, result)

        return result

    def activities_by_group(self, group, limit=15, namespace='local'):
        cache_key = 'group:{0}:{1}'.format(namespace, str(group))
        nimbble_cache = cache.NimbbleCache()
        result = nimbble_cache.getItem(cache_key)

        if result:
            return result

        activities = context.ActivityContext().by_group(group, limit)
        result = [activity.serialize() for activity in activities]

        nimbble_cache.setItem(cache_key, result)

        return result      

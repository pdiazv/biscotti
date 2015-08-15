from repository import context, cache
from datetime import datetime, timedelta

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

    def recent_leaderboard(self, *args, **kwargs):
        kwargs['limit'] = 25
        kwargs['starting_date'], kwargs['end_date'] = self.get_dates()

        activities = context.ActivityContext().recent(**kwargs)
        result = {}

        for activity in activities:
            user_dic = activity.get_user_dic()
            user_name = user_dic['name']

            if user_name not in result:
                result[user_name] = user_dic
                result[user_name]['points'] = activity.points
            else:
                result[user_name]['points'] += activity.points

        return {
            'start_date': kwargs['starting_date'],
            'end_date': kwargs['end_date'],
            'records': result.items()[:3]
        }


    def get_dates(self):
        today = datetime.today()
        day_idx = (today.weekday() + 1) % 7         # Sunday 0, Monday 1,...

        if day_idx == 0:
            next_satuday = today+timedelta(days=6)
            return today.strftime('%m/%d/%Y'), next_satuday.strftime('%m/%d/%Y')

        sunday = today - timedelta(days=day_idx-1)
        next_satuday = sunday+timedelta(days=6)
        return sunday.strftime('%m/%d/%Y'), next_satuday.strftime('%m/%d/%Y')



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

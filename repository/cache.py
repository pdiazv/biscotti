
from google.appengine.api import memcache

class NimbbleCache(object):

    def setItem(self, key, value, time=3600):
        # default cache time to 1 hour
        memcache.add(key, value, time=time)


    def getItem(self, key):
        return memcache.get(key)
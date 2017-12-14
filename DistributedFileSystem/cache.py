import os
from collections import deque
from threading import Timer

class Cache:

    CACHE_MAX_SIZE = 5

    #Cache is implemented as a dict
    #Key = Filename
    #Value = Data
    cache = {}

    #Used deque as it allows me to pop a list from the left, i.e. the oldest key
    #in the cache will be purged, and the other elements are shifted left.
    keys = deque()

    def __init__(self):
        #Refresh the cache every two minutes
        Timer(120, self.refresh_cache).start()

    #Seach for a key in the cache
    def search(self, key):
        if key in self.cache:
            return True
        else:
            return False

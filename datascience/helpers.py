import datetime
import inspect
from pandas import notnull, isnull, to_datetime
from collections import defaultdict

def to_dateprint(date, timestamp=False):
    if isnull(date): return ''
    return to_datetime(date).strftime('%m/%d/%Y %H:%M:%S' if timestamp else '%m/%d/%Y')

class memoize(object):
    @classmethod
    def clear(cls):
        cls.MEMOIZE_CACHE.clear()
    
    MEMOIZE_CACHE = defaultdict(dict)
    def __init__(self, *args, **kwargs):
        if (len(args)==1) and inspect.isroutine(args[0]):
            self.func = args[0]
            self.ttl = None
        else:
            self.func = None
            self.ttl = kwargs.get('ttl')
        
    def __call__(self, *args, **kwargs):
        if notnull(self.func):
            name = self.func.__module__ + self.func.__qualname__
            key = (args, frozenset(kwargs.items()))
            if key not in self.MEMOIZE_CACHE[name]:
                self.MEMOIZE_CACHE[name][key] = self.func(*args, **kwargs), datetime.datetime.now()
            return self.MEMOIZE_CACHE[name][key][0]
        
        else:
            self.func = args[0]
            name = self.func.__module__ + self.func.__qualname__
            def memoized_func(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                if key in self.MEMOIZE_CACHE[name]:
                    result, timestamp = self.MEMOIZE_CACHE[name][key]
                    if notnull(self.ttl) and ((datetime.datetime.now() - timestamp).total_seconds() < self.ttl):
                        return result
                self.MEMOIZE_CACHE[name][key] = (self.func(*args, **kwargs), datetime.datetime.now())
                return self.MEMOIZE_CACHE[name][key][0]
    
            return memoized_func
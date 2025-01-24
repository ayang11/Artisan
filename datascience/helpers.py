from collections import defaultdict
import datetime
import inspect
import os

from pandas import notnull, isnull, to_datetime, read_excel, Series

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
        
def artisan_folder(*args):
    return os.path.join('C:\\','users','yanga','desktop','artisan',*args)

def _read_file(section = 'Europe Economy', old=False):
    if old:
        if section == 'Europe Economy':
            filename=artisan_folder('Intra-Europe LCC and Network Carriers 3 days - Truncated.xlsx')
        elif section in ('Intercontinental Economy','Intercontinental Business'):
            filename=artisan_folder('Inter-Continental Network Airlines 3 days - Truncated.xlsx')
    else:
        if section == 'Europe Economy':
            filename=artisan_folder('Intra-Europe LCC and Network Carriers 60 days - Truncated.xlsx')
        elif section in ('Intercontinental Economy','Intercontinental Business'):
            filename=artisan_folder('Inter-Continental Network Airlines 60 days - Truncated.xlsx')
        
    dm = read_excel(filename, sheet_name=section)
    dm = dm[notnull(dm['Airline Name'])]
    return dm

@memoize
def read_file(section = 'Europe Economy', combine=True):
    if combine:
        a = _read_file(section, old=False)
        b = _read_file(section, old=True)
        return a.merge(b, on=('Airline Code','Origin Code','Destination Code'), suffixes=('','_old'))
    else:
        return _read_file(section, old=False)

def origins_list(section):return dict(Series(read_file(section)['Origin Name'].values,read_file(section)['Origin Code'].values).dropna().items())
def destinations_list(section): return dict(Series(read_file(section)['Destination Name'].values,read_file(section)['Destination Code'].values).dropna().items())
def airports_list(section):
    a = origins_list(section)
    a.update(destinations_list(section))
    return a
def airlines_list(section): return dict(Series(read_file(section)['Airline Name'].values,read_file(section)['Airline Code'].values).dropna().items())
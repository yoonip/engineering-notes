from collections import OrderedDict

def solution(cacheSize, cities):
    cache = OrderedDict()
    time = 0
    for city in cities:
        city = city.lower()
        if city in cache:
            cache.move_to_end(city)
            time += 1
        else:
            time += 5
            if cacheSize:
                cache[city] = None
                if len(cache) > cacheSize:
                    cache.popitem(last=False)
    return time

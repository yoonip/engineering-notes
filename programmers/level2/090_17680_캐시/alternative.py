from collections import deque

def solution(cacheSize, cities):
    cache = deque(maxlen=cacheSize)
    time = 0
    for city in cities:
        city = city.lower()
        if city in cache:
            cache.remove(city)
            time += 1
        else:
            time += 5
        cache.append(city)
    return time

# 문제: 캐시
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17680
# 풀이: OrderedDict로 조회와 최근 사용 위치 갱신을 묶는다. 가장 오래 사용하지 않은 항목을 앞에서 제거해 LRU를 유지한다.
# 복잡도: 요청 N개·도시 글자수 합 L·최대 길이 W·용량 C: 평균 시간 O(L+N), 추가 공간 O(min(N,C)W).

from collections import OrderedDict


def solution(cacheSize, cities):
    if cacheSize == 0:
        return 5 * len(cities)
    cache = OrderedDict()
    time = 0
    for city in cities:
        city = city.lower()
        if city in cache:
            cache.move_to_end(city)
            time += 1
        else:
            time += 5
            if len(cache) == cacheSize:
                cache.popitem(last=False)
            cache[city] = None
    return time

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

# 전체 코드 줄별 설명
# from collections import deque  # collections의 deque를 import. 양끝 추가·삭제가 가능한 자료구조.
# 
# def solution(cacheSize, cities):  # def는 함수 정의. 캐시 용량·도시 요청 목록 입력.
#     cache = deque(maxlen=cacheSize)  # maxlen은 최대 길이. 가득 찬 상태에서 뒤에 추가하면 맨 앞 원소를 자동 제거. 0이면 저장하지 않음.
#     time = 0  # =는 대입. 총 실행시간 초기화.
#     for city in cities:  # for~in으로 도시 요청 순회.
#         city = city.lower()  # lower는 소문자 변환. 대소문자를 같은 도시로 취급.
#         if city in cache:  # in은 포함 여부. cache hit 검사.
#             cache.remove(city)  # remove는 같은 값 원소 삭제. 최근 사용 위치로 옮기기 위해 기존 항목 제거.
#             time += 1  # +=는 더해 저장. hit 비용 1 누적.
#         else:  # else는 cache miss인 경우.
#             time += 5  # miss 비용 5 누적.
#         cache.append(city)  # append로 가장 최근 사용 도시를 뒤에 배치. 앞에는 가장 오래 쓰지 않은 도시가 남음.
#     return time  # return으로 총 실행시간 반환.

# 풀이 요약
# 캐시를 오래 사용하지 않은 순서로 유지합니다. hit는 기존 항목을 지운 뒤 맨 뒤로, miss는 추가하며 용량 초과 시 맨 앞을 제거합니다.
# 예: 용량 2에서 NewYork와 newyork는 같은 도시라 마지막 요청은 hit. 도시 N개·용량 C일 때 시간 O(NC), 공간 O(C); C<=30.

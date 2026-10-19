from heapq import heappush, heappop

def solution(n, k, enemy):
    shielded = []
    for index, count in enumerate(enemy):
        heappush(shielded, count)
        if len(shielded) > k:
            n -= heappop(shielded)
        if n < 0:
            return index
    return len(enemy)

# 전체 코드 줄별 설명
# from heapq import heappush, heappop  # heapq는 최소 힙 모듈. heappush는 추가, heappop은 최솟값을 꺼내 삭제하는 함수.
# 
# def solution(n, k, enemy):  # def는 함수 정의, () 안은 병사 수·무적권 수·라운드별 적 수 입력.
#     shielded = []  # []는 리스트. 가장 큰 k개 공격을 보관하는 최소 힙으로 사용.
#     for index, count in enumerate(enemy):  # enumerate는 (인덱스,값)을 제공. for로 순서대로 순회.
#         heappush(shielded, count)  # 현재 공격을 무적권 후보 힙에 추가.
#         if len(shielded) > k:  # len은 원소 수, >는 큼. 후보가 무적권 개수를 넘었는지 검사.
#             n -= heappop(shielded)  # -=는 빼서 저장. 가장 작은 공격은 병사로 막고 큰 공격들만 힙에 유지.
#         if n < 0:  # <는 작음. 병사로 현재까지의 공격을 감당할 수 없는지 검사.
#             return index  # 0부터인 인덱스가 현재 라운드 이전까지 성공한 라운드 수.
#     return len(enemy)  # return으로 모든 라운드 수 반환.

# 풀이 요약
# 진행한 공격 중 큰 k개에 무적권을 배정하고 나머지를 병사로 막습니다. 최소 힙에서 가장 작은 공격을 병사 비용으로 옮깁니다.
# 예: 병사 7·무적권 3이면 예제에서 5라운드 성공. 라운드 N개일 때 시간 O(N log(min(k,N)+1)), 공간 O(min(k,N)).

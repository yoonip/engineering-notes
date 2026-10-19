from collections import Counter

def solution(k, tangerine):
    counts = sorted(Counter(tangerine).values(), reverse=True)
    for kinds, count in enumerate(counts, 1):
        k -= count
        if k <= 0:
            return kinds

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 각 크기가 몇 번 나오는지 세는 자료구조.
# 
# def solution(k, tangerine):  # def는 함수 정의. ()의 k는 고를 개수, tangerine은 크기 목록.
#     counts = sorted(Counter(tangerine).values(), reverse=True)  # values()는 개수들, sorted는 새 정렬 리스트. reverse=True로 내림차순 정렬.
#     for kinds, count in enumerate(counts, 1):  # enumerate(목록,1)은 1부터 번호 부여. 종류 수·해당 개수를 언패킹.
#         k -= count  # -=는 빼서 저장. 가장 많은 크기부터 필요한 귤 수를 줄임.
#         if k <= 0:  # if는 조건 분기, <=는 이하. 필요한 귤을 다 골랐는지 검사.
#             return kinds  # return으로 지금까지 선택한 종류 수 반환. 마지막 종류는 필요한 만큼만 사용.

# 풀이 요약
# 크기별 개수를 내림차순으로 정렬해 많은 종류부터 고르면 같은 종류 수로 가장 많은 귤을 담을 수 있습니다.
# 예: k=6이면 개수 2,2,2인 세 종류 선택. 귤 N개·크기 U종류일 때 시간 O(N+U log U), 공간 O(U).

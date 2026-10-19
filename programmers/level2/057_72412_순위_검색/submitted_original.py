from collections import defaultdict
from itertools import product
from bisect import bisect_left

def solution(info, query):
    table = defaultdict(list)
    for record in info:
        parts = record.split()
        score = int(parts.pop())
        for key in product(*[(value, '-') for value in parts]):
            table[key].append(score)
    for scores in table.values():
        scores.sort()
    answer = []
    for request in query:
        parts = request.replace(' and ', ' ').split()
        minimum = int(parts.pop())
        scores = table.get(tuple(parts), [])
        answer.append(len(scores) - bisect_left(scores, minimum))
    return answer

# 전체 코드 줄별 설명
# from collections import defaultdict  # collections의 defaultdict를 import. 없는 키에 기본값을 자동 생성하는 딕셔너리.
# from itertools import product  # itertools의 product는 각 자리 선택의 모든 조합 생성.
# from bisect import bisect_left  # bisect의 bisect_left는 정렬 목록에서 값 이상이 처음 나오는 위치를 이진 탐색.
# 
# def solution(info, query):  # def는 함수 정의. info는 지원자 정보, query는 검색 조건 목록.
#     table = defaultdict(list)  # 없는 키에는 list()로 빈 점수 리스트 생성.
#     for record in info:  # for~in으로 지원자 순회.
#         parts = record.split()  # split()으로 공백 기준 단어 목록 생성.
#         score = int(parts.pop())  # pop은 마지막 단어를 꺼내 삭제, int는 점수를 정수로 변환.
#         for key in product(*[(value, '-') for value in parts]):  # 리스트 내포로 실제 값·와일드카드 선택 구성. *는 인수 펼치기, product로 16가지 키 생성.
#             table[key].append(score)  # [키]의 점수 리스트에 append로 점수 추가. 키는 불변 튜플.
#     for scores in table.values():  # values()는 딕셔너리 값 목록 제공.
#         scores.sort()  # sort()는 점수 리스트 제자리 오름차순 정렬.
#     answer = []  # []는 결과 리스트.
#     for request in query:  # 문의를 원래 순서대로 처리.
#         parts = request.replace(' and ', ' ').split()  # replace는 문자열 치환. and를 제거하고 조건·점수 분리.
#         minimum = int(parts.pop())  # 마지막 단어를 최소 점수 정수로 변환.
#         scores = table.get(tuple(parts), [])  # tuple은 불변 묶음 변환. get(키,기본값)은 조건이 없으면 빈 리스트 반환.
#         answer.append(len(scores) - bisect_left(scores, minimum))  # len은 개수. 최소 점수 이상인 첫 위치 뒤의 원소 수를 결과에 추가.
#     return answer  # return으로 조건별 인원 수 목록 반환.

# 풀이 요약
# 지원자마다 '-' 포함 16개 조건 조합에 점수를 저장합니다. 각 목록을 정렬하면 문의는 이진 탐색 한 번으로 처리됩니다.
# 예: 모든 조건 '-'에 최소 150점이면 예제에서 4명. 지원자 N·문의 Q개일 때 시간 O(16N log N+Q log N), 공간 O(16N+Q).

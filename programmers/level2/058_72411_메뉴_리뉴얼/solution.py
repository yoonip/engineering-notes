from collections import Counter
from itertools import combinations

def solution(orders, course):
    orders = [sorted(order) for order in orders]
    answer = []
    for size in course:
        counts = Counter()
        for order in orders:
            counts.update(combinations(order, size))
        highest = max(counts.values(), default=0)
        if highest >= 2:
            answer.extend(''.join(menu) for menu, count in counts.items() if count == highest)
    return sorted(answer)

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 메뉴 조합별 등장 횟수 저장.
# from itertools import combinations  # itertools의 combinations는 지정한 개수의 중복 없는 조합 생성.
# 
# def solution(orders, course):  # def는 함수 정의. 주문 목록·코스별 메뉴 수 입력.
#     orders = [sorted(order) for order in orders]  # 리스트 내포와 sorted로 각 주문 문자를 알파벳순 정렬. 같은 조합의 표현 통일.
#     answer = []  # []는 빈 결과 리스트.
#     for size in course:  # for~in으로 만들 코스 길이 순회.
#         counts = Counter()  # 조합 개수를 세는 빈 Counter 생성.
#         for order in orders:  # 각 손님의 주문 순회.
#             counts.update(combinations(order, size))  # update는 각 조합의 횟수를 1씩 추가. 짧은 주문에서는 조합이 생성되지 않음.
#         highest = max(counts.values(), default=0)  # values는 개수들, max는 최댓값. 비어 있으면 default=0 사용.
#         if highest >= 2:  # >=는 이상. 최소 두 손님에게 주문된 코스인지 검사.
#             answer.extend(''.join(menu) for menu, count in counts.items() if count == highest)  # items는 키·값 제공, ==는 같음. join으로 문자열을 만들고 extend로 공동 최다 조합 모두 추가.
#     return sorted(answer)  # 전체 메뉴 구성을 사전순 정렬해 return으로 반환.

# 풀이 요약
# 코스 길이마다 각 주문의 메뉴 조합 횟수를 세고, 두 번 이상 주문된 공동 최다 조합을 모두 선택합니다.
# 예: 첫 예제는 AC·CDE·ACDE·BCFG를 사전순 반환. 생성 조합 수 T·결과 수 A일 때 시간 O(T+A log A), 공간 O(T).

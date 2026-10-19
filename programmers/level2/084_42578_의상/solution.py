# 문제: 의상
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42578
# 풀이: 종류별 의상 수를 Counter로 센다. 각 종류의 미착용 선택을 더해 곱한 뒤 아무것도 입지 않는 한 경우를 뺀다.
# 복잡도: 의상 N개·종류 U개: 평균 시간 O(N), 추가 공간 O(U). 큰 정수 곱셈 비용은 별도다.

from collections import Counter

def solution(clothes):
    counts = Counter(kind for name, kind in clothes)
    answer = 1
    for count in counts.values():
        answer *= count + 1
    return answer - 1

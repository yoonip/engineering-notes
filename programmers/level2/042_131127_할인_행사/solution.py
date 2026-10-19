# 문제: 할인 행사
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/131127
# 풀이: 열흘 구간의 상품 수를 Counter로 세어 희망 수량과 비교한다. 구간 길이가 10으로 고정되어 전체 날짜 수에 비례해 처리한다.
# 복잡도: 할인 D일·희망 상품 U종류: 시간 O(U+10D), 추가 공간 O(U+10). 열흘은 고정 길이다.

from collections import Counter

def solution(want, number, discount):
    needed = dict(zip(want, number))
    answer = 0
    for start in range(len(discount) - 9):
        current = Counter(discount[start:start + 10])
        if current == needed:
            answer += 1
    return answer

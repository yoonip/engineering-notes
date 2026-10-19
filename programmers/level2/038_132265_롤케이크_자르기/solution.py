# 문제: 롤케이크 자르기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/132265
# 풀이: 왼쪽 종류는 set, 오른쪽 남은 수는 Counter로 관리한다. 경계를 한 칸 옮길 때 필요한 두 상태만 갱신한다.
# 복잡도: 토핑 N개·종류 U개: 평균 시간 O(N), 추가 공간 O(U).

from collections import Counter

def solution(topping):
    right = Counter(topping)
    left = set()
    answer = 0
    for value in topping:
        left.add(value)
        right[value] -= 1
        if right[value] == 0:
            del right[value]
        if len(left) == len(right):
            answer += 1
    return answer

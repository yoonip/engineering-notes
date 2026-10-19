# 문제: 예상 대진표
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12985
# 풀이: 각 라운드의 새 번호를 올림 나눗셈으로 구한다. 두 참가자의 번호가 같아지는 첫 라운드가 만나는 시점이다.
# 복잡도: 참가자 N명: 시간 O(log N), 추가 공간 O(1).

def solution(n, a, b):
    rounds = 0
    while a != b:
        a = (a + 1) // 2
        b = (b + 1) // 2
        rounds += 1
    return rounds

# 문제: 점프와 순간 이동
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12980
# 풀이: 거꾸로 보면 짝수는 무료로 절반 이동하고 홀수는 비용 1로 한 칸 줄인다. 이진수의 1 개수만 누적하면 된다.
# 복잡도: 거리 N: 제한 범위 정수 연산 기준 시간 O(log N), 추가 공간 O(1).

def solution(n):
    answer = 0
    while n:
        answer += n % 2
        n //= 2
    return answer

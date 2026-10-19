# 짝수와 홀수
# 분류: 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12937
# 선택 이유: 2로 나눈 나머지로 홀짝을 구분한다. 음수에도 같은 규칙을 적용한다.
# 비용: 시간 O(1), 추가 공간 O(1).

def solution(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

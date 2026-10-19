# 평균 구하기
# 분류: 합계 / 평균
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12944
# 선택 이유: 한 번 구한 합을 원소 수로 나눈다.
# 비용: 원소 N개: 시간 O(N), 추가 공간 O(1).

def solution(arr):
    return sum(arr) / len(arr)

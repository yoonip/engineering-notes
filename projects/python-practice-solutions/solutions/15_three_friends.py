# 삼총사
# 분류: 완전탐색 / 조합
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/131705
# 선택 이유: 서로 다른 세 인덱스를 증가 순서로 고르면 순서만 다른 조합을 중복해서 세지 않는다.
# 비용: 원소 N개: 시간 O(N³), 추가 공간 O(1). 작은 조합을 직접 확인하는 풀이다.

def solution(number):
    n = len(number)
    answer = 0

    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if number[i] + number[j] + number[k] == 0:
                    answer += 1

    return answer

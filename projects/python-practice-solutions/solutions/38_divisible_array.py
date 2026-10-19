# 나누어 떨어지는 숫자 배열
# 분류: 조건 필터 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12910
# 선택 이유: 나누어떨어지는 원소만 모아 정렬하고, 결과가 비면 [-1]을 돌려준다.
# 비용: 입력 N개, 선택 K개: 시간 O(N+K log K), 추가 공간 O(K).

def solution(arr, divisor):
    answer = []
    for num in arr:
        if num % divisor == 0:
            answer.append(num)
    if not answer:
        return [-1]
    return sorted(answer)

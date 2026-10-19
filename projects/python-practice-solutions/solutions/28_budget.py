# 예산
# 분류: 그리디 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12982
# 선택 이유: 작은 요청부터 지원하면 같은 예산으로 더 많은 부서를 지원할 수 있다.
# 비용: 요청 N개: 시간 O(N log N), 추가 공간 O(N). sorted는 원본을 바꾸지 않는다.

def solution(d, budget):
    answer = 0

    for cost in sorted(d):
        if cost > budget:
            break

        budget -= cost
        answer += 1

    return answer

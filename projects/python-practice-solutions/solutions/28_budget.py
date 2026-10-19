# 예산
# 분류: 그리디 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12982
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(d, budget):
    answer = 0

    for cost in sorted(d):
        if cost > budget:
            break

        budget -= cost
        answer += 1

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(d, budget):  # def로 함수를 정의합니다. 신청 금액 리스트와 전체 예산을 매개변수로 받습니다.
#     answer = 0  # =는 대입입니다. 지원한 부서 수를 0으로 시작합니다.
#
#     for cost in sorted(d):  # sorted()는 오름차순으로 정렬한 새 리스트를 반환합니다. 작은 금액부터 cost에 넣으며 반복합니다.
#         if cost > budget:  # >는 크다는 비교입니다. 신청 금액이 남은 예산보다 큰지 확인합니다.
#             break  # 가장 가까운 반복문을 종료합니다. 이후 금액도 더 크거나 같으므로 추가 지원이 불가능합니다.
#
#         budget -= cost  # budget = budget - cost와 같습니다. 지원 금액만큼 남은 예산을 줄입니다.
#         answer += 1  # answer = answer + 1과 같습니다. 지원한 부서 수를 늘립니다.
#
#     return answer  # 반복문이 끝나면 부서 수를 반환하고 함수를 종료합니다.
#

# 명예의 전당 (1)
# 분류: 최소 힙
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/138477
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

import heapq


def solution(k, score):
    hall = []
    answer = []

    for point in score:
        heapq.heappush(hall, point)

        if len(hall) > k:
            heapq.heappop(hall)

        answer.append(hall[0])

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# import heapq  # import는 모듈을 가져옵니다. heapq는 최소 힙을 다루는 Python 기본 모듈입니다.
#
#
# def solution(k, score):  # def로 함수를 정의합니다. k는 유지할 점수 수, score는 날짜 순서의 점수 리스트입니다.
#     hall = []  # []는 빈 리스트입니다. 이 리스트를 최소 힙으로 사용합니다.
#     answer = []  # 매일 발표한 점수를 차례로 저장할 리스트입니다.
#
#     for point in score:  # for로 score의 점수를 하나씩 꺼내 point에 넣습니다.
#         heapq.heappush(hall, point)  # 모듈.함수 형식입니다. 리스트를 힙으로 유지하면서 점수를 추가합니다.
#
#         if len(hall) > k:  # len은 원소 수, >는 크다는 비교입니다. k개를 넘었는지 확인합니다.
#             heapq.heappop(hall)  # 힙에서 가장 작은 값 하나를 꺼내 제거합니다. 남은 점수는 상위 k개입니다.
#
#         answer.append(hall[0])  # [0]은 첫 원소입니다. 최소 힙의 첫 값은 최솟값이며 append로 결과 뒤에 추가합니다.
#
#     return answer  # 모든 날짜를 처리한 뒤 결과 리스트를 반환하고 함수를 종료합니다.
#

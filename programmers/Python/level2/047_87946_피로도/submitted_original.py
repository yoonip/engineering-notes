from itertools import permutations

def solution(k, dungeons):
    answer = 0
    for order in permutations(dungeons):
        remaining, count = k, 0
        for required, cost in order:
            if remaining < required:
                break
            remaining -= cost
            count += 1
        answer = max(answer, count)
    return answer

# 전체 코드 줄별 설명
# from itertools import permutations  # itertools의 permutations를 import. 모든 방문 순서인 순열을 만드는 함수.
# 
# def solution(k, dungeons):  # def는 함수 정의. k는 초기 피로도, dungeons는 필요·소모 피로도 목록.
#     answer = 0  # =는 대입. 최대 방문 수 초기화.
#     for order in permutations(dungeons):  # for~in으로 모든 던전 방문 순서 검사.
#         remaining, count = k, 0  # 각 순서를 초기 피로도·방문 수 0부터 시작.
#         for required, cost in order:  # 던전의 두 값을 최소 필요량·소모량으로 언패킹.
#             if remaining < required:  # if는 분기, <는 작음. 입장할 수 없는 경우 검사.
#                 break  # break는 가장 가까운 반복문 종료. 이 순서의 가능한 방문 접두부만 평가.
#             remaining -= cost  # -=는 빼서 저장. 탐험 비용 차감.
#             count += 1  # +=는 더해 저장. 방문 수 증가.
#         answer = max(answer, count)  # max는 최댓값. 모든 순서 중 최대 방문 수 갱신.
#     return answer  # return으로 최대 던전 방문 수 반환.

# 풀이 요약
# 던전이 최대 8개이므로 모든 방문 순서를 검사합니다. 입장 조건을 만족하는 동안 피로도를 차감해 방문 수를 셉니다.
# 예: 80에서 80/20→30/10→50/40 순으로 세 곳 방문 가능. 던전 N개일 때 시간 O(N!*N), 순열 작업 공간 O(N).

def solution(scores):
    target = tuple(scores[0])
    target_sum = sum(target)
    rank = 1
    best_second = -1
    for first, second in sorted(scores, key=lambda row: (-row[0], row[1])):
        if second < best_second:
            if (first, second) == target:
                return -1
            continue
        best_second = second
        if first + second > target_sum:
            rank += 1
    return rank

# 전체 코드 줄별 설명
# def solution(scores):  # def는 함수 정의. scores는 직원별 두 점수 목록이며 첫 행이 완호.
#     target = tuple(scores[0])  # [0]은 첫 직원. tuple은 수정 불가능한 두 점수 묶음으로 변환.
#     target_sum = sum(target)  # sum은 합계. 완호의 점수 합 저장.
#     rank = 1  # 자신보다 높은 유효 직원 수에 1을 더해 순위를 계산.
#     best_second = -1  # 앞서 처리한 직원들의 동료 평가 최고 점수. 가능한 최솟값 0보다 작은 값으로 시작.
#     for first, second in sorted(scores, key=lambda row: (-row[0], row[1])):  # sorted는 새 정렬 목록, key는 기준, lambda는 짧은 함수. 첫 점수 내림차순·같으면 둘째 점수 오름차순.
#         if second < best_second:  # if는 조건문, <는 미만. 앞에 두 점수가 모두 더 높은 직원이 존재.
#             if (first, second) == target:  # ()는 튜플, ==는 같음. 완호도 제외 대상인지 확인.
#                 return -1  # return은 함수 종료. 인센티브를 못 받는 완호의 답은 -1.
#             continue  # continue는 제외 직원을 건너뛰고 다음 반복으로 진행.
#         best_second = second  # 이 직원은 이전 최고 점수 이상이므로 최고값 갱신.
#         if first + second > target_sum:  # 점수 합이 완호보다 엄격히 큰 유효 직원인지 검사.
#             rank += 1  # +=는 더해 저장. 동점은 더하지 않아 공동 순위를 정확히 처리.
#     return rank  # 완호의 최종 순위 반환.

# 풀이 요약
# 첫 점수를 내림차순, 같은 첫 점수에서는 둘째 점수를 오름차순으로 정렬합니다. 이 순서면 앞에서 본 둘째 점수보다 낮은 직원만 두 점수 모두 낮은 제외 대상입니다.
# 완호가 제외되면 -1, 아니면 유효 직원 중 점수 합이 완호보다 큰 사람 수+1을 반환합니다. 시간 O(N log N), 공간 O(N).
# 예: [[2,2],[1,4],[3,2],[3,2],[2,1]]에서 [2,1]만 제외되고, 완호보다 합이 큰 유효 직원 세 명이 있어 4등입니다.

# scores는 직원별 두 점수 목록이며 첫 행이 완호.
def solution(scores):
    # tuple은 수정 불가능한 두 점수 묶음으로 변환.
    target = tuple(scores[0])
    # 완호의 점수 합 저장.
    target_sum = sum(target)
    # 자신보다 높은 유효 직원 수에 1을 더해 순위를 계산.
    rank = 1
    # 가능한 최솟값 0보다 작은 값으로 시작.
    best_second = -1
    # 첫 점수 내림차순·같으면 둘째 점수 오름차순.
    for first, second in sorted(scores, key=lambda row: (-row[0], row[1])):
        # 앞에 두 점수가 모두 더 높은 직원이 존재.
        if second < best_second:
            # 완호도 제외 대상인지 확인.
            if (first, second) == target:
                # 인센티브를 못 받는 완호의 답은 -1.
                return -1
            # continue는 제외 직원을 건너뛰고 다음 반복으로 진행.
            continue
        # 이 직원은 이전 최고 점수 이상이므로 최고값 갱신.
        best_second = second
        # 점수 합이 완호보다 엄격히 큰 유효 직원인지 검사.
        if first + second > target_sum:
            # 동점은 더하지 않아 공동 순위를 정확히 처리.
            rank += 1
    # 완호의 최종 순위 반환.
    return rank

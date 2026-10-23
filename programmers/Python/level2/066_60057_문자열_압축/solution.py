def solution(s):
    # 압축하지 않은 길이로 최솟값 초기화.
    answer = len(s)
    for size in range(1, len(s) // 2 + 1):
        # 끝은 미포함.
        previous = s[:size]
        count, length = 1, 0
        # range(시작,끝,간격)으로 다음 조각 시작점 순회.
        for start in range(size, len(s), size):
            current = s[start:start + size]
            # 이전 조각과 연속 반복인지 검사.
            if current == previous:
                count += 1
            else:
                length += len(previous) + (len(str(count)) if count > 1 else 0)
                # 새 조각으로 기준을 바꾸고 반복 수 1로 초기화.
                previous, count = current, 1
        length += len(previous) + (len(str(count)) if count > 1 else 0)
        # 단위 길이별 결과 비교.
        answer = min(answer, length)
    return answer

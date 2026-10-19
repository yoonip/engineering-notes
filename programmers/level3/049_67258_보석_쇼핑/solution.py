# gems는 진열 순서대로 저장된 보석 목록.
def solution(gems):
    # 필요한 전체 보석 종류 수.
    kinds = len(set(gems))
    # 현재 연속 구간 안에서 보석별 개수 저장.
    counts = {}
    # 오른쪽과 함께 움직이는 투 포인터 방식.
    left = 0
    # 처음에는 전체 구간을 답으로 둠.
    best_left, best_right = 0, len(gems) - 1
    # 오른쪽 끝을 한 칸씩 늘림.
    for right, gem in enumerate(gems):
        # 새로 포함한 보석 수 증가.
        counts[gem] = counts.get(gem, 0) + 1
        # 모든 종류가 들어 있는 동안 왼쪽을 줄임.
        while len(counts) == kinds:
            # 더 짧은 구간일 때만 갱신해 동점이면 이른 시작점 유지.
            if right - left < best_right - best_left:
                # 최적 구간 갱신.
                best_left, best_right = left, right
            # []로 구간에서 빠질 보석 조회.
            old = gems[left]
            # 왼쪽 보석 하나 제거.
            counts[old] -= 1
            # 이 종류가 현재 구간에서 완전히 사라졌는지 확인.
            if counts[old] == 0:
                # len(counts)가 실제 포함 종류 수를 나타내게 함.
                del counts[old]
            # 왼쪽 끝을 한 칸 이동.
            left += 1
    # 0부터 세는 인덱스를 1부터 세는 진열대 번호로 변환.
    return [best_left + 1, best_right + 1]

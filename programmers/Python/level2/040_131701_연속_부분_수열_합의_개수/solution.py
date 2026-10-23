def solution(elements):
    n = len(elements)
    # 두 번 이어 붙이면 원형 경계를 넘는 구간도 그대로 읽을 수 있다.
    doubled = elements * 2
    sums = set()
    for start in range(n):
        total = 0
        # 시작마다 길이 1부터 전체 길이까지의 합을 모은다.
        for end in range(start, start + n):
            total += doubled[end]
            sums.add(total)
    return len(sums)

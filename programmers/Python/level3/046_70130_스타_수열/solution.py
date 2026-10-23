# a는 원래 수열.
def solution(a):
    # 원소 값이 0~n-1이므로 값 자체를 배열 인덱스로 사용 가능.
    n = len(a)
    # 각 값을 공통 원소로 쓸 때 만든 쌍 수.
    pairs = [0] * n
    # 서로 다른 후보의 탐색 상태는 독립적.
    used_until = [-1] * n
    # 인접한 두 칸을 왼쪽부터 확인.
    for i in range(n - 1):
        # 두 값을 언패킹 대입.
        first, second = a[i], a[i + 1]
        # 같은 숫자끼리는 유효한 쌍이 아님.
        if first == second:
            # 이번 인접 쌍을 건너뜀.
            continue
        # 공통값=first인 후보에서 두 칸 모두 아직 사용하지 않았는지 검사.
        if used_until[first] < i:
            # 유효한 쌍 한 개 추가.
            pairs[first] += 1
            # 두 칸을 사용했으므로 마지막 사용 위치 갱신.
            used_until[first] = i + 1
        # 공통값=second인 별도의 후보에도 같은 판단 적용.
        if used_until[second] < i:
            # 이 공통값의 쌍 수 증가.
            pairs[second] += 1
            # 해당 후보의 마지막 사용 위치 갱신.
            used_until[second] = i + 1
    # 쌍마다 원소가 두 개이므로 최장 길이는 최대 쌍 수의 두 배.
    return 2 * max(pairs)

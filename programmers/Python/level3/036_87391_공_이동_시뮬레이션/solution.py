# 격자 크기·마지막 목표 행열·이동 명령 목록 입력.
def solution(n, m, x, y, queries):
    # 가능한 열 구간과 행 구간을 목표 한 점으로 초기화.
    bounds = [[y, y], [x, x]]
    # 각 축의 격자 길이.
    lengths = [m, n]
    # 마지막 이동부터 시작점 후보 구간을 거꾸로 복원.
    for command, distance in reversed(queries):
        # 명령 0·1은 열 축 0, 2·3은 행 축 1.
        axis = command // 2
        # 현재 가능한 최소·최대 좌표를 언패킹.
        low, high = bounds[axis]
        # 해당 축의 크기.
        length = lengths[axis]
        # 원래 감소 방향 이동의 역산은 좌표 증가.
        if command % 2 == 0:
            # 0 경계를 포함하면 벽에 막혀 모였던 시작점도 모두 포함해야 함.
            if low != 0:
                # 경계가 아닌 아래 끝은 이동량만큼 증가.
                low += distance
            # 위 끝은 증가하되 격자 마지막 좌표까지만 허용.
            high = min(length - 1, high + distance)
        else:
            # 마지막 경계를 포함하지 않으면 위 끝도 이동량만큼 감소.
            if high != length - 1:
                # -=는 빼서 저장.
                high -= distance
            # 아래 끝은 감소하되 0 이상으로 제한.
            low = max(0, low - distance)
        # 가능한 구간이 빈 상태인지 검사.
        if low > high:
            # return으로 도착 가능한 시작점이 없음을 반환.
            return 0
        # 이번 명령 이전의 후보 구간으로 갱신.
        bounds[axis] = [low, high]
    # 포함 구간 길이들의 곱이 가능한 시작점 수.
    return (bounds[0][1] - bounds[0][0] + 1) * (bounds[1][1] - bounds[1][0] + 1)

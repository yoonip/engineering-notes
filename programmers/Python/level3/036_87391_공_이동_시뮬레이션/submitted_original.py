def solution(n, m, x, y, queries):
    bounds = [[y, y], [x, x]]
    lengths = [m, n]
    for command, distance in reversed(queries):
        axis = command // 2
        low, high = bounds[axis]
        length = lengths[axis]
        if command % 2 == 0:
            if low != 0:
                low += distance
            high = min(length - 1, high + distance)
        else:
            if high != length - 1:
                high -= distance
            low = max(0, low - distance)
        if low > high:
            return 0
        bounds[axis] = [low, high]
    return (bounds[0][1] - bounds[0][0] + 1) * (bounds[1][1] - bounds[1][0] + 1)

# 전체 코드 줄별 설명
# def solution(n, m, x, y, queries):  # def는 함수 정의. 격자 크기·마지막 목표 행열·이동 명령 목록 입력.
#     bounds = [[y, y], [x, x]]  # [] 중첩 리스트. 가능한 열 구간과 행 구간을 목표 한 점으로 초기화.
#     lengths = [m, n]  # 첫 축은 열, 둘째 축은 행. 각 축의 격자 길이.
#     for command, distance in reversed(queries):  # reversed는 역순 순회. 마지막 이동부터 시작점 후보 구간을 거꾸로 복원.
#         axis = command // 2  # //는 정수 나눗셈. 명령 0·1은 열 축 0, 2·3은 행 축 1.
#         low, high = bounds[axis]  # 현재 가능한 최소·최대 좌표를 언패킹.
#         length = lengths[axis]  # 해당 축의 크기.
#         if command % 2 == 0:  # %는 나머지, ==는 같음. 원래 감소 방향 이동의 역산은 좌표 증가.
#             if low != 0:  # if는 조건문, !=는 다름. 0 경계를 포함하면 벽에 막혀 모였던 시작점도 모두 포함해야 함.
#                 low += distance  # +=는 더해 저장. 경계가 아닌 아래 끝은 이동량만큼 증가.
#             high = min(length - 1, high + distance)  # min은 작은 값. 위 끝은 증가하되 격자 마지막 좌표까지만 허용.
#         else:  # 원래 증가 방향 이동을 역산하는 경우.
#             if high != length - 1:  # 마지막 경계를 포함하지 않으면 위 끝도 이동량만큼 감소.
#                 high -= distance  # -=는 빼서 저장.
#             low = max(0, low - distance)  # max는 큰 값. 아래 끝은 감소하되 0 이상으로 제한.
#         if low > high:  # 가능한 구간이 빈 상태인지 검사.
#             return 0  # return으로 도착 가능한 시작점이 없음을 반환.
#         bounds[axis] = [low, high]  # 이번 명령 이전의 후보 구간으로 갱신.
#     return (bounds[0][1] - bounds[0][0] + 1) * (bounds[1][1] - bounds[1][0] + 1)  # 행·열 변화는 독립. 포함 구간 길이들의 곱이 가능한 시작점 수.

# 풀이 요약
# 10억×10억 격자를 직접 돌리지 않고 목표 한 점에서 명령을 역순으로 적용해 가능한 시작 구간을 확장·이동합니다.
# 벽에 막혀 같은 좌표에 모일 수 있으므로 후보 구간이 0 또는 마지막 경계를 포함할 때 해당 끝을 그대로 둡니다. 빈 구간이면 0입니다. 시간 O(Q), 추가 공간 O(1).
# 예: 마지막 열이 0이고 직전에 왼쪽으로 3칸 이동했다면 이전 열은 0~3 모두 가능하므로 역산 구간이 넓어집니다.
# 
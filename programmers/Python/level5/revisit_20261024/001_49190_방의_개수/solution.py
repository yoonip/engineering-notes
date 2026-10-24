def solution(arrows):
    base = 400001
    moves = (1, base + 1, base, base - 1, -1, -base - 1, -base, -base + 1)
    visited = {0: 0}
    position = 0
    rooms = 0
    for direction in arrows:
        step = moves[direction]
        forward = 1 << direction
        backward = 1 << ((direction + 4) & 7)
        for _ in range(2):
            following = position + step
            if not visited[position] & forward:
                old = visited.get(following)
                if old is None:
                    old = 0
                else:
                    rooms += 1
                visited[position] |= forward
                visited[following] = old | backward
            position = following
    return rooms

# 전체 코드 줄별 설명
# def solution(arrows):  # 방향 배열을 받아 닫힌 방 개수를 계산하는 함수
#     base = 400001  # 좌표를 정수 하나로 묶을 간격; 두 배 격자의 y 차이보다 크게 잡기
#     moves = (1, base + 1, base, base - 1, -1, -base - 1, -base, -base + 1)  # 위부터 시계 방향으로 x*base+y의 변화량을 튜플에 저장
#     visited = {0: 0}  # 딕셔너리 키는 좌표, 값은 이미 그은 여덟 방향의 비트
#     position = 0  # 원점의 좌표 키로 시작
#     rooms = 0  # 새로 닫힌 방 수
#     for direction in arrows:  # 이동 방향을 입력 순서대로 처리
#         step = moves[direction]  # 해당 방향으로 한 칸 움직일 때의 키 변화
#         forward = 1 << direction  # 현재 점에서 나가는 간선을 표시할 비트
#         backward = 1 << ((direction + 4) & 7)  # 도착점에서 반대로 돌아오는 방향 비트
#         for _ in range(2):  # 한 이동을 두 번으로 나눠 대각선의 중간 교차점도 방문
#             following = position + step  # 다음 점의 정수 좌표 키
#             if not visited[position] & forward:  # 처음 그리는 간선일 때만 방 증가 여부 확인
#                 old = visited.get(following)  # 처음 보는 점이면 None, 방문한 점이면 방향 비트 반환
#                 if old is None:  # 새 점으로 뻗는 간선은 방을 만들지 않음
#                     old = 0  # 새 점의 방향 표시를 빈 상태로 시작
#                 else:  # 새 간선으로 기존 점에 닿는 경우
#                     rooms += 1  # 닫힌 영역 하나가 추가됨
#                 visited[position] |= forward  # 현재 점의 나가는 간선을 기록
#                 visited[following] = old | backward  # 도착점에도 같은 무방향 간선의 반대 방향을 기록
#             position = following  # 다음 이동의 출발점 갱신
#     return rooms  # 완성된 방 수 반환

# 풀이 요약
# 새 간선으로 이미 방문한 점에 도착할 때만 방이 하나 늘어남. 같은 선분을 다시 지나갈 때는 방향 비트가 이미 있어 건너뛰기.
# 모든 이동을 두 번으로 나눠 대각선끼리 만나는 중간점도 꼭짓점으로 처리.
# 최대 20만 칸 이동하므로 y 좌표 차이는 40만 이하. x*400001+y로 좌표를 충돌 없이 묶어 튜플·간선 집합 대신 점별 방향 딕셔너리 하나 사용.
# 시간과 공간 모두 O(N).

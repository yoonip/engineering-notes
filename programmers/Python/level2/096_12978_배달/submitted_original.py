def solution(N, road, K):
    distance = [[float('inf')] * N for _ in range(N)]
    for village in range(N):
        distance[village][village] = 0
    for a, b, time in road:
        distance[a - 1][b - 1] = min(distance[a - 1][b - 1], time)
        distance[b - 1][a - 1] = distance[a - 1][b - 1]
    for via in range(N):
        for start in range(N):
            for end in range(N):
                distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end])
    return sum(time <= K for time in distance[0])

# 전체 코드 줄별 설명
# def solution(N, road, K):  # def는 함수 정의. 마을 수·도로 정보·배달 시간 제한 입력.
#     distance = [[float('inf')] * N for _ in range(N)]  # 리스트 내포로 독립된 행 생성. float('inf')는 무한대, 아직 경로 없음 표시.
#     for village in range(N):  # range(N)은 0~N-1. 마을 인덱스 순회.
#         distance[village][village] = 0  # [][]는 두 인덱스 접근. 자기 마을까지의 시간은 0.
#     for a, b, time in road:  # for~in으로 도로의 두 마을·소요 시간을 언패킹.
#         distance[a - 1][b - 1] = min(distance[a - 1][b - 1], time)  # min은 최솟값. 1부터인 번호를 -1로 바꾸고 여러 도로 중 최소 시간 저장.
#         distance[b - 1][a - 1] = distance[a - 1][b - 1]  # 양방향 도로이므로 반대 방향도 같은 최소 시간으로 설정.
#     for via in range(N):  # 중간에 거쳐 갈 수 있는 마을을 하나씩 허용.
#         for start in range(N):  # 출발 마을 순회.
#             for end in range(N):  # 도착 마을 순회.
#                 distance[start][end] = min(distance[start][end], distance[start][via] + distance[via][end])  # 직접 경로와 via 경유 두 구간의 합 중 짧은 시간 선택.
#     return sum(time <= K for time in distance[0])  # <=는 이하. 생성식의 참은 1로 더해지므로 sum으로 1번 마을에서 제한 내 도달하는 마을 수 반환.

# 풀이 요약
# 마을을 하나씩 경유지로 허용하는 플로이드–워셜로 최단 거리를 갱신합니다. 1번 마을의 거리 중 K 이하를 셉니다.
# 예: 첫 예제는 1·2·4·5번 마을까지 가능해 4개. N<=50이므로 시간 O(N³+도로 수), 공간 O(N²).

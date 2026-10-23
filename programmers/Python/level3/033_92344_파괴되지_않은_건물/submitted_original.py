def solution(board, skill):
    n, m = len(board), len(board[0])
    difference = [[0] * (m + 1) for _ in range(n + 1)]
    for kind, r1, c1, r2, c2, degree in skill:
        change = -degree if kind == 1 else degree
        difference[r1][c1] += change
        difference[r1][c2 + 1] -= change
        difference[r2 + 1][c1] -= change
        difference[r2 + 1][c2 + 1] += change
    for r in range(n):
        for c in range(1, m):
            difference[r][c] += difference[r][c - 1]
    for r in range(1, n):
        for c in range(m):
            difference[r][c] += difference[r - 1][c]
    return sum(board[r][c] + difference[r][c] > 0 for r in range(n) for c in range(m))

# 전체 코드 줄별 설명
# def solution(board, skill):  # def는 함수 정의. board는 초기 내구도 격자, skill은 직사각형 공격·회복 목록.
#     n, m = len(board), len(board[0])  # len은 길이. 행·열 수를 언패킹.
#     difference = [[0] * (m + 1) for _ in range(n + 1)]  # [] 리스트 내포로 2차원 차분 배열 생성. 범위 끝 다음 칸을 표시하려고 한 행·열 더 확보.
#     for kind, r1, c1, r2, c2, degree in skill:  # for~in으로 스킬 종류·두 끝 좌표·변화량을 언패킹.
#         change = -degree if kind == 1 else degree  # a if 조건 else b는 조건식. 공격은 음수, 회복은 양수.
#         difference[r1][c1] += change  # +=는 더해 저장. 직사각형의 시작 꼭짓점에 변화 시작 표시.
#         difference[r1][c2 + 1] -= change  # -=는 빼서 저장. 오른쪽 경계 다음에서 가로 방향 변화 취소.
#         difference[r2 + 1][c1] -= change  # 아래 경계 다음에서 세로 방향 변화 취소.
#         difference[r2 + 1][c2 + 1] += change  # 가로·세로 취소가 겹친 오른쪽 아래 바깥점은 한 번 다시 더함.
#     for r in range(n):  # range는 끝 제외. 실제 격자의 모든 행 순회.
#         for c in range(1, m):  # 첫 열을 제외한 열들을 왼쪽부터 순회.
#             difference[r][c] += difference[r][c - 1]  # 가로 누적합으로 각 행의 구간 변화 복원.
#     for r in range(1, n):  # 첫 행을 제외한 행들을 위에서부터 순회.
#         for c in range(m):  # 모든 실제 열 순회.
#             difference[r][c] += difference[r - 1][c]  # 세로 누적합으로 직사각형 변화량 전체 복원.
#     return sum(board[r][c] + difference[r][c] > 0 for r in range(n) for c in range(m))  # sum은 합계. >0 비교의 참·거짓이 1·0으로 계산되어 최종 생존 건물 수 반환.

# 풀이 요약
# 직사각형을 매번 모두 바꾸는 대신, 변화 시작·취소를 네 꼭짓점에 기록하는 2차원 차분을 사용합니다.
# 가로·세로 누적합을 각각 한 번 적용하면 각 칸의 총 변화량이 복원됩니다. 중간에 파괴돼도 변화는 계속 누적하며 마지막 내구도>0만 셉니다. 스킬 수 K에 대해 시간 O(K+NM), 공간 O(NM).
# 예: 공격 4와 회복 2가 겹친 칸의 총 변화량은 -2입니다. 초기 내구도 5이면 최종 3이므로 생존합니다.
# 
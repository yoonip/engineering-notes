def solution(beginning, target):
    n, m = len(beginning), len(beginning[0])
    difference = [[beginning[r][c] ^ target[r][c] for c in range(m)] for r in range(n)]
    columns = difference[0][:]
    rows = [difference[r][0] ^ columns[0] for r in range(n)]
    for r in range(n):
        for c in range(m):
            if rows[r] ^ columns[c] != difference[r][c]:
                return -1
    flips = sum(rows) + sum(columns)
    return min(flips, n + m - flips)

# 전체 코드 줄별 설명
# def solution(beginning, target):  # def는 함수 정의. beginning과 target은 시작·목표 동전 격자.
#     n, m = len(beginning), len(beginning[0])  # len은 길이. 행 수와 열 수를 언패킹.
#     difference = [[beginning[r][c] ^ target[r][c] for c in range(m)] for r in range(n)]  # 중첩 리스트 내포. ^는 XOR이므로 두 상태가 다르면 1, 같으면 0.
#     columns = difference[0][:]  # [0]은 첫 행, [:]는 복사. 첫 행을 뒤집지 않는다고 정하면 열별 뒤집기 여부는 이 값으로 확정.
#     rows = [difference[r][0] ^ columns[0] for r in range(n)]  # 첫 열의 차이를 열 뒤집기로 설명하고 남는 차이가 각 행의 뒤집기 여부.
#     for r in range(n):  # range는 0부터 n-1. 모든 행 검사.
#         for c in range(m):  # 모든 열 검사.
#             if rows[r] ^ columns[c] != difference[r][c]:  # if는 조건문, !=는 다름. 행·열 뒤집기의 XOR이 필요한 변화와 일치하는지 검사.
#                 return -1  # return으로 불가능을 알리고 종료. 첫 행을 반대로 정해도 이 모순은 사라지지 않음.
#     flips = sum(rows) + sum(columns)  # sum은 합계. 0·1 선택값의 합이 실제 뒤집기 횟수.
#     return min(flips, n + m - flips)  # min은 작은 값. 모든 행·열의 선택을 동시에 반대로 하면 같은 결과이므로 두 경우 중 최소 반환.

# 풀이 요약
# 각 칸의 필요한 변화는 행 뒤집기 XOR 열 뒤집기입니다. 첫 행을 안 뒤집는다고 고정하면 나머지 모든 선택이 결정됩니다.
# 모든 칸이 일치하는지 확인한 뒤, 그 선택과 모든 행·열 선택을 반대로 한 경우 두 개만 비교하면 됩니다. 같은 줄을 두 번 뒤집는 것은 불필요합니다. 시간·공간 O(NM).
# 예: 첫 행 고정 해법이 행 2개·열 3개를 뒤집는다면 총 5번입니다. 선택을 전부 뒤집은 해법의 비용은 N+M-5입니다.
# 
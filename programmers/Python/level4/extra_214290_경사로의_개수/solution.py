def solution(grid, d, k):
    mod = 1_000_000_007  # _는 숫자 자릿수 구분으로 값에 영향 없음. 정답을 나눌 수.
    n, m = len(grid), len(grid[0])
    size = n * m  # 모든 칸을 0부터 size-1까지의 번호로 표현.
    edges = {}  # {}는 빈 딕셔너리. 경사별 (출발, 도착) 간선 목록 저장.
    for r in range(n):  # range(n)은 0부터 n-1까지. 각 행 순회.
        for c in range(m):  # 모든 열 순회.
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # ()는 튜플. 상하좌우 네 방향의 좌표 변화량 순회.
                nr, nc = r + dr, c + dc  # 이동한 이웃 칸의 좌표 계산.
                if 0 <= nr < n and 0 <= nc < m:  # 연속 비교와 and로 이웃이 격자 내부인지 검사.
                    slope = grid[nr][nc] - grid[r][c]  # 도착 높이에서 출발 높이를 빼어 경사 계산.
                    edges.setdefault(slope, []).append((r * m + c, nr * m + nc))  # setdefault는 키가 없으면 빈 리스트 생성. 해당 경사의 간선 추가.
    matrix = [[0] * size for _ in range(size)]  # 리스트 내포로 서로 독립적인 행 생성. 시작·도착별 경로 수 행렬.
    for start in range(size):  # 모든 출발 칸을 하나씩 선택.
        ways = [0] * size  # 현재 각 칸에 도달하는 경로 수 초기화.
        ways[start] = 1  # 아무 이동도 하지 않은 출발 상태는 한 가지.
        for slope in d:  # 경사 수열의 각 값을 차례대로 처리.
            next_ways = [0] * size  # 한 번 이동한 후의 경로 수를 새 리스트에 저장.
            for a, b in edges.get(slope, []):  # get은 해당 키의 값 또는 기본값 반환. 요구 경사와 같은 간선만 사용.
                next_ways[b] = (next_ways[b] + ways[a]) % mod  # 출발 a의 경로 수를 도착 b에 더하고 나머지를 저장.
            ways = next_ways  # 이번 이동 결과를 다음 이동의 입력으로 교체.
        matrix[start] = ways  # 경사 수열을 한 번 완료한 출발·도착별 경로 수 저장.
    def multiply(a, b):  # 두 행렬의 곱을 계산하는 내부 함수 정의.
        result = []  # 결과 행을 담을 빈 리스트.
        for row in a:  # 왼쪽 행렬의 각 행 순회.
            out = [0] * size  # 이번 결과 행 초기화.
            for middle, value in enumerate(row):  # enumerate는 (인덱스, 값) 제공. 중간 칸과 그 경로 수를 얻음.
                if value:  # 경로 수가 0인 항은 계산을 생략.
                    for end, count in enumerate(b[middle]):  # 중간 칸에서 각 도착 칸으로 가는 경로 수 순회.
                        out[end] += value * count  # 이어지는 경로의 가짓수는 곱셈, 서로 다른 중간 칸은 덧셈으로 합침.
            result.append([value % mod for value in out])  # 리스트 내포로 각 원소의 나머지를 구해 결과 행 추가.
        return result  # 곱한 행렬 반환.
    answer = [[1] * size]  # 모든 칸에서 출발할 수 있으므로 각 출발 칸의 초기 경로 수는 1.
    while k:  # while은 조건이 참인 동안 반복. 지수의 비트를 하나씩 처리.
        if k & 1:  # &는 비트 AND. k가 홀수이면 현재 거듭제곱을 답에 반영.
            answer = multiply(answer, matrix)  # 선택된 반복 횟수만큼의 경로 전이를 적용.
        k //= 2  # //=는 정수 나눗셈 후 저장. 지수를 절반으로 줄임.
        if k:  # 이후 계산이 남아 있을 때만 제곱 수행.
            matrix = multiply(matrix, matrix)  # 같은 전이를 두 번 이어 반복 횟수를 두 배로 늘림.
    return sum(answer[0]) % mod  # sum은 합계. 모든 도착 칸의 경로 수를 더하여 반환.

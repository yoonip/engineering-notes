import sys # 보드 크기 입력
n = int(sys.stdin.buffer.read()) # 한 변의 길이를 정수로 변환
columns, down, up = [False] * n, [False] * (2 * n - 1), [False] * (2 * n - 1) # 열과 두 대각선의 사용 표시
def search(row): # 이번 행의 퀸 위치를 고르는 재귀 함수
    if row == n: # 모든 행에 퀸을 놓은 경우
        return 1 # 완성 배치 한 개 반환
    count = 0 # 현재 접두 배치에서 완성되는 개수
    for col in range(n): # 이번 행의 열을 왼쪽부터 확인
        d, u = row - col + n - 1, row + col # 두 대각선의 식별자 계산
        if columns[col] or down[d] or up[u]: # 기존 퀸에게 공격받는 후보인지 검사
            continue # 불가능한 후보의 하위 탐색 생략
        columns[col] = down[d] = up[u] = True # 이번 선택이 차지한 방향 표시
        count += search(row + 1) # 다음 행의 모든 완성 개수 누적
        columns[col] = down[d] = up[u] = False # 다음 열을 탐색하기 전 선택 복구
    return count # 이 접두 배치의 완성 개수 반환
print(search(0)) # 첫 행부터 탐색한 전체 N퀸 배치 수 출력

import sys # 격자와 명령 토큰 읽기
tokens = sys.stdin.read().split() # 공백 단위 입력 분리
h, w = map(int, tokens[:2]) # 격자 크기 변환
grid = tokens[2:2 + h] # 격자 행 문자열 목록
row, col, direction, count = map(int, tokens[2 + h:6 + h]) # 시작 상태와 명령 수 읽기
commands = ''.join(tokens[6 + h:]) # 붙어 있거나 공백으로 나뉜 명령을 하나로 모으기
steps = [(-1, 0), (0, 1), (1, 0), (0, -1)] # 북·동·남·서 좌표 변화
for command in commands[:count]: # 약속한 수의 명령을 순서대로 처리
    if command == 'R': # 오른쪽 회전 분기
        direction = (direction + 1) % 4 # 방향 번호를 0~3 안에서 회전
    else: # F 명령의 이동 후보 계산
        dr, dc = steps[direction] # 현재 방향의 이동량 해체
        nr, nc = row + dr, col + dc # 다음 좌표를 임시 계산
        if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] != '#': # 경계와 벽 검사
            row, col = nr, nc # 허용된 위치로만 이동
print(row, col, direction) # 최종 위치와 방향 출력

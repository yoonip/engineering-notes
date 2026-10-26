import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수 목록으로 변환
n, m = data[:2] # 초기 노드 수와 삽입 수
values = data[2:2 + n] + [0] * m # 새 노드 자리까지 값 배열 확보
next_node = list(range(1, n)) + [-1] + [-1] * m # 초기 순서와 끝 표시를 연결 배열로 저장
for index in range(m): # 삽입 명령을 순서대로 처리
    after, item = data[2 + n + 2 * index:4 + n + 2 * index] # 앞 노드와 삽입 값 읽기
    node = n + index # 새 노드의 고정 번호
    values[node] = item # 새 값 저장
    next_node[node] = next_node[after] # 기존 뒷부분을 새 노드에 먼저 연결
    next_node[after] = node # 앞 노드의 다음 위치를 새 노드로 변경
result, node = [], 0 # 출력 목록과 머리 노드 준비
while node != -1: # 끝 표시까지 다음 연결을 따라 이동
    result.append(values[node]) # 현재 노드의 값을 결과에 추가
    node = next_node[node] # 다음 노드로 이동
print(*result) # 연결 순서의 값 출력

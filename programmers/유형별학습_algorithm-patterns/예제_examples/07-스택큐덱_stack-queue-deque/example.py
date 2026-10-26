import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, values = data[0], data[1:] # 원소 수와 배열 분리
answer, stack = [-1] * n, [] # 답이 없는 표시와 미해결 인덱스 스택
for index, value in enumerate(values): # 현재 값과 위치를 왼쪽부터 확인
    while stack and values[stack[-1]] < value: # 현재 값이 스택 끝 후보보다 큰지 검사
        answer[stack.pop()] = index # 가장 가까운 오른쪽 큰 값의 위치 확정
    stack.append(index) # 현재 원소는 미해결 후보로 남기기
print(*answer) # 각 원소의 다음 큰 값 인덱스 출력

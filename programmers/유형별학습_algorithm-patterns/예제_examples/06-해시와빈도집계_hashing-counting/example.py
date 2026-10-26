import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 공백 입력을 정수로 변환
n, q = data[:2] # 값 수와 질의 수
counts = {} # 키별 빈도를 저장할 해시 딕셔너리
for key in data[2:2 + n]: # 입력 값 한 번씩 순회
    counts[key] = counts.get(key, 0) + 1 # 없는 키의 기본 빈도 0에서 증가
queries = data[2 + n:2 + n + q] # 조회할 키 목록 분리
print(*(counts.get(key, 0) for key in queries)) # 없는 키는 0으로 답하고 원래 질의 순서 유지

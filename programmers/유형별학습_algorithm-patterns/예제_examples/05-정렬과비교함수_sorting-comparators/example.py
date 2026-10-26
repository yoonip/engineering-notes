import sys # 정수 입력 토큰 읽기
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수 목록으로 변환
n = data[0] # 기록 수
records = [tuple(data[1 + 3 * i:4 + 3 * i]) for i in range(n)] # 식별자·점수·벌점 묶기
records.sort(key=lambda item: (-item[1], item[2], item[0])) # 점수 역방향과 나머지 정방향을 하나의 키로 지정
print(*(item[0] for item in records)) # 정렬된 식별자 출력

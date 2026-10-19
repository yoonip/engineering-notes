# 자체 창작 연습 01 · 숫자 기록의 합 
# 핵심 상태: total은 지금까지 읽은 숫자의 합, x는 이번에 읽은 숫자, n은 숫자 개수다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
data = list(map(int, sys.stdin.buffer.read().split()))
# data[0]은 숫자 개수 N이다. 실제 숫자는 그 뒤에서 시작한다.
# Python list의 첫 위치는 0이며 N을 실제 합산 값에 포함하면 안 된다.
# Python int는 큰 정수를 표현하므로 합이 커져도 C의 %lld 같은 형식은 필요 없다.
n = data[0]
total = 0
# data[1:n+1]은 1번 위치부터 n번 위치까지의 새 리스트다.
# 슬라이스 오른쪽 끝은 포함하지 않으므로 n+1을 사용한다.
# x가 각 값을 한 번씩 가져오고 total에 더한다. 입력 파싱과 슬라이스는 메모리를 쓴다.
for x in data[1:n + 1]:
    total += x  # 이번 값까지 포함한 누적합으로 갱신한다.
print(total)

# 복잡도: 시간 O(N). C/C++는 입력을 즉시 더해 추가 공간 O(1); Python 예제는 전체 입력 파싱으로 O(N).
# 마지막 경계 확인:
# - C에서 long long 입력은 %lld, 출력도 %lld.
# - 입력 N을 합에 포함하지 않는다.
# - 출력에 설명 문장을 붙이지 않는다.

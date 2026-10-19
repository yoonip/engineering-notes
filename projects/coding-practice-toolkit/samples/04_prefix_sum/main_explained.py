# 자체 창작 연습 04 · 구간 기록 조회 
# 핵심 상태: prefix[i]는 첫 원소부터 i번째 원소까지의 합. 질문 L,R은 1 기반 위치다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
# read는 EOF까지 전체 입력을 읽는다. split은 공백·줄바꿈으로 토큰을 나눈다.
# map(int,...)가 정수 변환을 하고 iter/next로 순서대로 토큰을 소비한다.
# 유효 입력에서 필요한 토큰이 정확히 있다는 가정이다. 토큰이 부족하면 StopIteration이 난다.
it = iter(map(int, sys.stdin.buffer.read().split()))
n, q = next(it), next(it)
# 0번 기준칸과 1~n번 누적합 칸을 만든다.
# Python 숫자 목록도 위치가 0부터라 n+1칸이 필요하다.
# 음수 입력이라도 prefix[i-1]+현재값이라는 정의대로 계산하면 된다.
prefix = [0] * (n + 1)
for i in range(1, n + 1):
    prefix[i] = prefix[i - 1] + next(it)
# 많은 출력은 문자열 목록 out에 모은 뒤 줄바꿈으로 연결해 한 번 출력한다.
# str로 숫자를 문자열로 바꿔야 join을 사용할 수 있다.
# out과 입력 토큰까지 저장하므로 이 Python 예제의 전체 메모리는 O(N+Q)다.
out = []
for _ in range(q):
    l, r = next(it), next(it)
    out.append(str(prefix[r] - prefix[l - 1]))  # L 앞까지의 합만 제거한다.
print('\n'.join(out))

# 복잡도: 시간 O(N+Q), 누적합 공간 O(N). Python은 입력·출력 목록까지 포함해 O(N+Q).
# 마지막 경계 확인:
# - prefix[R]-prefix[L]이 아니라 prefix[R]-prefix[L-1].
# - prefix 배열은 N+1칸이 필요하다.
# - 음수가 있어도 누적합 방식은 정확하다.

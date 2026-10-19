# 자체 창작 연습 07 · 기준 이상 첫 위치 
# 핵심 상태: 아직 분류하지 않은 원소 구간은 [lo,hi).
# lo 왼쪽은 X보다 작고 hi부터는 X 이상이다.
# lower_bound의 경계 위치 후보에는 hi도 포함된다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
it = iter(map(int, sys.stdin.buffer.read().split()))
n, q = next(it), next(it)
# next(it)로 헤더 이후 정렬 배열 n개를 순서대로 소비한다.
# list comprehension은 반복 결과들을 새 리스트에 모으는 표현이다.
# 배열을 만든 뒤 남은 토큰은 Q개의 기준값이다. 입력 소비 순서가 중요하다.
a = [next(it) for _ in range(n)]
out = []
for _ in range(q):
    x = next(it)
    # Python에서도 아직 분류하지 않은 원소 구간을 [lo,hi)로 둔다.
    # mid 계산의 //는 정수 나눗셈이다. 이 문제의 인덱스는 음수가 아니어서 C와 같은 값을 준다.
    # >=일 때 hi=mid, 작을 때 lo=mid+1로 줄이면 반복이 끝나며 첫 위치를 얻는다.
    lo, hi = 0, n
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] >= x:
            hi = mid  # X 이상인 첫 위치는 mid보다 오른쪽일 필요가 없다.
        else:
            lo = mid + 1
    # 숫자 lo를 문자열로 바꿔 출력 목록에 추가한다.
    # 마지막에 줄바꿈으로 연결한다. join은 문자열 원소 목록을 받는다.
    # lo=n일 수 있다. 찾은 위치의 원소를 읽으려면 별도의 범위 검사가 필요하다.
    out.append(str(lo))
print('\n'.join(out))

# 복잡도: 시간 O(N+Q log N), 배열 공간 O(N). Python 전체 파싱·출력 포함 O(N+Q).
# 마지막 경계 확인:
# - 정렬되지 않은 배열에 바로 적용하지 않는다.
# - 인덱스는 0부터 시작한다.
# - hi=N이므로 a[hi]를 직접 읽지 않는다.
# - 중복값에서 찾자마자 종료하면 첫 위치가 아닐 수 있다.

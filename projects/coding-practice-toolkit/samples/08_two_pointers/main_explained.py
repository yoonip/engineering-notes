# 자체 창작 연습 08 · 목표 합의 연속 구간 
# 핵심 상태: [left,right]가 현재 연속 구간, window가 그 합, answer가 찾은 구간 개수다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
data = list(map(int, sys.stdin.buffer.read().split()))
n, k = data[0], data[1]
# 헤더가 N,K 두 개라 실제 배열은 2번 위치부터 시작한다.
# n개의 값을 포함하려면 오른쪽 끝은 n+2다. 그 끝 위치는 슬라이스에 포함되지 않는다.
# 배열을 보관해야 나중에 왼쪽 끝 값을 window에서 뺄 수 있다.
a = data[2:n + 2]
left = 0
window = answer = 0
# right는 0~n-1로 이동하고 매 단계 a[right]를 더한다.
# window>k이면 while에서 a[left]를 빼고 left를 앞으로 옮긴다.
# Python int는 큰 합을 담을 수 있지만 양수 조건에 따른 알고리즘의 성립 여부는 따로 확인해야 한다.
for right in range(n):
    window += a[right]
    while left <= right and window > k:
        window -= a[left]
        left += 1  # 뺀 원소 다음 위치가 새 왼쪽 끝이다.
    # 조건이 참이면 answer를 1 증가시킨다. 현재 구간은 연속이며 비어 있지 않다.
    # k≥1이므로 합 0인 빈 구간을 잘못 세는 일이 없다.
    # 연속 구간은 부분집합과 다르다. 배열 중간 값을 임의로 건너뛰지 않는다.
    if window == k:
        answer += 1
print(answer)

# 복잡도: 시간 O(N), 저장 배열 공간 O(N). 이중 반복문이 있어도 각 원소를 한 번 넣고 한 번 뺀다.
# 마지막 경계 확인:
# - 양수 조건을 확인한다.
# - K와 window는 C/C++ long long.
# - window>K일 때 한 번만 빼지 말고 while로 충분히 줄인다.
# - 부분배열은 연속이고, 부분집합과 다르다.

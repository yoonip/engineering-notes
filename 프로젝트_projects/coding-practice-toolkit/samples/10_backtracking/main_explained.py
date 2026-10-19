# 자체 창작 연습 10 · 목표 합의 부분집합 
# 핵심 상태: dfs(i,total,used)는 i번째부터 결정할 차례. total은 선택 합, used는 하나 이상 선택 여부다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
data = list(map(int, sys.stdin.buffer.read().split()))
n, target = data[0], data[1]
a = data[2:n + 2]
answer = 0
# 함수의 세 인자가 현재 위치·누적합·하나 이상 선택했는지를 나타낸다.
# 정수와 bool 값은 호출마다 전달하며 목록 a는 함수 밖에서 읽는다.
# 함수 안에서 answer에 +=로 대입하므로 global answer로 바깥 카운터를 사용한다고 명시한다.
def dfs(i, total, used):
    global answer  # 함수 밖의 전체 답 카운터를 갱신한다.
    # 모든 위치를 결정했으면 비어 있지 않음과 목표 합을 검사하고 return한다.
    # target=0에서 아무것도 고르지 않은 선택도 합은 0이지만 정답에 포함하면 안 된다.
    # 재귀 종료 조건을 빼면 인덱스 범위를 벗어나거나 재귀가 끝나지 않는다.
    if i == n:
        if used and total == target:
            answer += 1
        return
    # 현재 원소를 포함한 선택을 먼저 탐색한 뒤 포함하지 않은 선택을 탐색한다.
    # 사용한 상태를 새로운 인자로 넘기므로 부모 호출의 상태는 그대로 남는다.
    # 이 예제의 최대 재귀 깊이는 20이라 재귀 한도를 변경하지 않는다. 큰 N에서는 다른 방법을 검토한다.
    dfs(i + 1, total + a[i], True)
    dfs(i + 1, total, used)
dfs(0, 0, False)
print(answer)

# 복잡도: 시간 O(2^N), 재귀 깊이 및 배열 공간 O(N). 재귀 깊이가 20이므로 이 예제는 Python 재귀 한도 변경이 필요 없다.
# 마지막 경계 확인:
# - T=0에서 빈 집합을 세지 않는다.
# - 같은 값을 가진 서로 다른 위치를 임의로 합치지 않는다.
# - 연속 구간 개수와 부분집합 개수를 구분한다.
# - 합은 C/C++ long long으로 받는다.

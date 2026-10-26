# 그래프 모델링과 BFS

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 위치보다 먼저 정의할 상태

그래프는 정점과 이동 가능한 관계를 표현합니다. 정점은 도시일 수도 있지만, 보드의 배치나 현재 문자열일 수도 있습니다. 문제에 그래프라는 말이 없어도 한 번의 행동으로 다른 상태로 바뀐다면 그래프로 생각할 수 있습니다.

상태 두 개를 합치려면 앞으로 허용되는 행동과 비용이 같아야 합니다. 열쇠가 있는 칸과 없는 칸은 좌표가 같아도 다른 상태입니다. 방문 배열을 좌표에만 두면 나중에 문을 열 수 있는 경로를 지워 버립니다.

그래프를 만들기 전에 다음을 적습니다.

1. 상태를 구별하는 최소 정보입니다.
2. 한 행동이 만드는 다음 상태입니다.
3. 행동의 비용과 목표 조건입니다.
4. 방향, 중복 간선, 자기 간선의 허용 여부입니다.

## 가까운 순서가 중요한 이유

BFS는 시작점에서 간선 수가 적은 상태부터 확인합니다. 모든 이동 비용이 같을 때 최초 발견 거리가 최단 거리입니다. 큐에는 거리가 작은 층부터 들어가므로, 거리 d인 정점에서 처음 발견한 이웃의 거리는 d+1입니다. 더 짧은 경로가 있었다면 이전 층에서 먼저 발견했어야 한다는 모순으로 정당화합니다. [Princeton의 BFS 설명](https://algs4.cs.princeton.edu/41graph/index.php)은 이 층별 탐색과 큐의 관계를 설명합니다.

도달 가능성만 필요하면 DFS도 가능합니다. 최단 행동 횟수를 함께 구하려면 BFS의 순서가 추가 정보를 제공합니다. 비용이 서로 다르면 같은 보장을 사용할 수 없습니다.

## 직접 구성한 예제와 추적

무방향 간선을 A-B, A-C, B-D, C-D, D-E로 둡니다.

| 꺼낸 정점 | 새로 발견한 정점 | 남은 큐 | 확정한 거리 |
| --- | --- | --- | --- |
| A | B, C | B, C | B=1, C=1 |
| B | D | C, D | D=2 |
| C | 없음 | D | 이미 발견한 D를 중복 삽입하지 않습니다. |
| D | E | E | E=3 |

다음 코드는 인접 리스트와 시작 정점 번호를 받는 학습용 예제입니다.

~~~python
from collections import deque  # deque에서 왼쪽 원소를 상수 시간에 꺼내기
def bfs(adj, start):  # 인접 리스트에서 시작점까지의 최단 간선 수 계산
    dist = [-1] * len(adj)  # -1을 아직 발견하지 않은 상태로 사용
    dist[start] = 0  # 시작점의 이동 횟수는 0
    queue = deque([start])  # 시작점 하나가 든 FIFO 큐 생성
    while queue:  # 발견했지만 이웃을 확인하지 않은 정점이 남은 동안 반복
        u = queue.popleft()  # 가장 먼저 들어온 정점 꺼내기
        for v in adj[u]:  # u에서 한 번에 갈 수 있는 모든 정점 확인
            if dist[v] == -1:  # 아직 발견하지 않은 정점만 처리
                dist[v] = dist[u] + 1  # 큐에 넣기 전에 거리를 기록해 중복 발견 방지
                queue.append(v)  # 다음 층에서 이웃을 확인하도록 큐 뒤에 추가
    return dist  # 도달하지 못한 정점의 거리는 -1로 유지
~~~

## 변형을 고르는 기준

| 조건 | 상태와 시작점 구성 | 확인할 사항 |
| --- | --- | --- |
| 가장 가까운 여러 출발점 | 모든 출발점을 거리 0으로 함께 삽입합니다. | 출발점마다 BFS를 반복할 필요가 없습니다. |
| 벽을 한 번 제거 | (행, 열, 사용 횟수)로 방문을 구별합니다. | 자원 사용 여부를 잃지 않습니다. |
| 주기적으로 바뀌는 장애물 | (위치, 시간 mod 주기)를 저장합니다. | 같은 나머지에서 미래 규칙이 반복되어야 합니다. |
| 여러 말의 동시 이동 | 모든 말의 위치를 하나의 상태로 묶습니다. | 충돌과 교차 금지 조건을 전이에 반영합니다. |
| 출발점과 목적지가 고정 | 양방향 BFS를 검토합니다. | 역방향 전이와 층별 종료 조건을 증명합니다. |

격자 전체를 간선 객체로 만들 필요는 없습니다. 상하좌우 이웃을 필요할 때 계산하는 방식도 같은 그래프를 탐색합니다. 최단 경로 복원은 처음 발견한 부모를 저장하고 목표에서 역추적합니다. 최단 경로 수를 세면 같은 거리로 도착하는 경우를 별도 합산하며, 재삽입 여부와 경우의 수 갱신을 구분합니다.

## 비용과 구현

인접 리스트의 정점 수 V, 간선 수 E에 대해 시간은 O(V+E), 거리·큐의 추가 공간은 O(V)입니다. 무방향 간선은 보통 두 번 저장하지만 점근식은 같습니다. 행렬의 모든 열을 확인하면 O(V²)입니다. 상태를 자원 K개로 확장했다면 원래 격자 크기가 아니라 확장된 V와 E로 계산합니다.

C에서는 충분한 배열과 head/tail 인덱스로 큐를 만들 수 있습니다. C++에서는 queue 또는 deque를 사용합니다. Python에서는 list.pop(0)이 뒤 원소를 이동시키므로 deque.popleft를 사용합니다. 동적으로 변하는 입력이라면 큐에 전체 경로를 복제하기보다 부모 인덱스를 저장합니다.

## 실전과 실제 시스템

의존 관계의 전파 범위, 같은 비용의 통신 홉 수, 퍼즐의 최소 조작 횟수를 계산하는 데 연결됩니다. 실제 이동 시간이 다르면 홉 수 최소화가 시간 최소화와 일치하지 않습니다. 상태에 시간·배터리를 넣으면 표현은 쉬워지지만 상태 수가 곱으로 늘어나므로 모델을 먼저 줄여야 합니다.

## 반례와 복습

A에서 B로 비용 100, A-C-B로 각각 비용 1인 그래프에서 BFS는 B를 먼저 찾을 수 있습니다. 이것은 최소 간선 수이고 최소 비용은 2입니다. 가중치가 0과 1이면 0-1 BFS, 일반 비음수이면 Dijkstra를 검토합니다.

복습: 방문 표시를 꺼낼 때만 하면 어떤 문제가 생기는지 생각합니다. 답은 여러 부모가 같은 정점을 중복 삽입해 큐와 작업량이 불필요하게 커질 수 있다는 점입니다. 모든 칸을 방문한 것은 모든 가능한 경로를 열거한 것과도 다릅니다.

[DFS](20-DFS와연결요소_graph-dfs.md) · [확장 상태 최단 경로](21-최단경로와확장상태_shortest-path.md)

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

작은 무방향 그래프에서 BFS로 출발점으로부터의 최소 간선 수를 구합니다. 인접 행렬을 사용하므로 예제의 시간은 O(V²+E)입니다.

이 예제에서 직접 구현하는 기법은 BFS · 발견 시 방문 처리 · 인접 행렬입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

첫 줄은 V E S입니다. 1≤V≤8, 0≤E≤28, 0≤S<V이며 이후 E줄에 서로 다른 무방향 간선 u v가 주어집니다. 자기 간선은 없습니다.

```text
6 5 0
0 1
0 2
1 3
2 3
3 4
```

정점 번호순 최소 거리를 한 줄에 출력합니다. 도달할 수 없으면 -1입니다.

```text
0 1 1 2 3 -1
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | queue=[0], distance=[0,-1,-1,-1,-1,-1] | 출발점만 거리 0으로 발견합니다. |
| 2 | 0 처리: queue=[0,1,2], head=1 | 두 이웃을 거리 1로 넣습니다. |
| 3 | 1 처리: distance[3]=2 | 큐에 넣을 때 표시하여 2에서 중복 삽입하지 않습니다. |
| 4 | distance=[0,1,1,2,3,-1] | 4의 거리는 3이고 고립 정점 5는 미도달 상태입니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/19-그래프모델링과BFS_graph-bfs/example.c>)

```c
#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 작은 그래프의 BFS 거리 계산
    int n = read_int(), m = read_int(), start = read_int();  // 정점 수·간선 수·출발점
    int adj[8][8] = {0}, distance[8], queue[8];  // 연결 여부·거리·FIFO 저장 공간
    for (int i = 0; i < m; ++i) {  // 무방향 간선 입력
        int a = read_int(), b = read_int();  // 간선의 양끝
        adj[a][b] = adj[b][a] = 1;  // 양방향 이동 표시
    }  // 그래프 입력 끝
    for (int i = 0; i < n; ++i) distance[i] = -1;  // 미발견 정점의 거리
    int head = 0, tail = 0;  // 큐의 읽을 위치와 다음 저장 위치
    queue[tail++] = start; distance[start] = 0;  // 넣는 순간 출발점 발견
    while (head < tail) {  // 먼저 발견한 정점부터 처리
        int u = queue[head++];  // FIFO 순서의 다음 정점
        for (int v = 0; v < n; ++v) {  // 현재 행의 이웃 후보 순회
            if (adj[u][v] && distance[v] == -1) {  // 연결된 미발견 이웃만 선택
                distance[v] = distance[u] + 1;  // 한 간선 더 이동한 거리
                queue[tail++] = v;  // 다음 층 후보를 큐 뒤에 추가
            }  // 새 이웃의 발견 처리 끝
        }  // 현재 정점 이웃 확인 끝
    }  // 도달 가능한 정점 탐색 끝
    for (int i = 0; i < n; ++i) {  // 정점 번호순 출력
        if (i) write_text(" ");  // 숫자 사이의 공백
        write_number(distance[i]);  // 미도달 -1도 그대로 출력
    }  // 거리 배열 출력 끝
    write_text("\n");  // 결과 줄 마침
    return 0;  // 정상 종료
}  // BFS 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/19-그래프모델링과BFS_graph-bfs/example.cpp>)

```cpp
#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    cout << value;  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 작은 그래프의 BFS 거리 계산
    int n = read_int(), m = read_int(), start = read_int();  // 정점 수·간선 수·출발점
    int adj[8][8] = {}, distance[8], queue[8];  // 연결 여부·거리·FIFO 저장 공간
    for (int i = 0; i < m; ++i) {  // 무방향 간선 입력
        int a = read_int(), b = read_int();  // 간선의 양끝
        adj[a][b] = adj[b][a] = 1;  // 양방향 이동 표시
    }  // 그래프 입력 끝
    for (int i = 0; i < n; ++i) distance[i] = -1;  // 미발견 정점의 거리
    int head = 0, tail = 0;  // 큐의 읽을 위치와 다음 저장 위치
    queue[tail++] = start; distance[start] = 0;  // 넣는 순간 출발점 발견
    while (head < tail) {  // 먼저 발견한 정점부터 처리
        int u = queue[head++];  // FIFO 순서의 다음 정점
        for (int v = 0; v < n; ++v) {  // 현재 행의 이웃 후보 순회
            if (adj[u][v] && distance[v] == -1) {  // 연결된 미발견 이웃만 선택
                distance[v] = distance[u] + 1;  // 한 간선 더 이동한 거리
                queue[tail++] = v;  // 다음 층 후보를 큐 뒤에 추가
            }  // 새 이웃의 발견 처리 끝
        }  // 현재 정점 이웃 확인 끝
    }  // 도달 가능한 정점 탐색 끝
    for (int i = 0; i < n; ++i) {  // 정점 번호순 출력
        if (i) write_text(" ");  // 숫자 사이의 공백
        write_number(distance[i]);  // 미도달 -1도 그대로 출력
    }  // 거리 배열 출력 끝
    write_text("\n");  // 결과 줄 마침
    return 0;  // 정상 종료
}  // BFS 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/19-그래프모델링과BFS_graph-bfs/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m, start = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 그래프 크기와 출발점
    adj = [[0] * n for _ in range(n)]  # 각 행이 독립인 인접 행렬
    for _ in range(m):  # 무방향 간선 입력
        a, b = int(next(tokens)), int(next(tokens))  # 간선 양끝
        adj[a][b] = adj[b][a] = 1  # 양방향 이동 표시
    distance = [-1] * n  # 아직 발견하지 않은 거리
    queue = [start]  # head로 읽을 FIFO 목록
    distance[start] = 0  # 출발점을 넣는 순간 발견 처리
    head = 0  # 다음에 읽을 큐 위치
    while head < len(queue):  # 발견 순서대로 처리
        u = queue[head]  # 이번 정점
        head += 1  # 읽는 위치 전진
        for v in range(n):  # 현재 행의 모든 이웃 후보
            if adj[u][v] and distance[v] == -1:  # 연결된 미발견 정점만 선택
                distance[v] = distance[u] + 1  # 한 간선 더 이동한 최단 거리
                queue.append(v)  # 다음 층 후보를 뒤에 추가
    print(*distance)  # 번호순 거리 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 입력과 출력 | scanf와 fputs를 감싼 함수를 사용합니다. | cin과 cout을 감싼 함수를 사용합니다. | 입력을 split으로 나누고 print로 출력합니다. |
| 작업 배열 | 입력 형식에 명시한 작은 상한의 고정 배열을 사용합니다. | 절차 비교를 위해 C와 같은 고정 배열을 사용합니다. 가변 길이 배열이나 bits 헤더는 사용하지 않습니다. | 입력 크기에 맞춘 리스트를 생성합니다. |
| 정수와 상태 | 예제의 값 범위가 int 안에 들어가도록 상한을 제한합니다. | 같은 정수 범위와 상태 전이를 사용합니다. | int는 가변 정밀도이지만 이 예제는 작은 정수만 사용합니다. |

### 예제의 비용과 실행 파일

- 시간: O(V²+E)
- 보조 공간: O(V²)

인접 행렬 초기화와 정점별 V개 이웃 후보 확인이 필요합니다. 큐와 거리는 O(V)입니다.

[예제 입력](<예제_examples/19-그래프모델링과BFS_graph-bfs/input.txt>) · [예상 출력](<예제_examples/19-그래프모델링과BFS_graph-bfs/output.txt>) · [예제 실행 방법](<예제_examples/19-그래프모델링과BFS_graph-bfs/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 2 | 1844 게임 맵 최단거리 | — | [C++](<../C++/level2/extra_1844_게임_맵_최단거리/README.md>) | [Python](<../Python/level2/extra_1844_게임_맵_최단거리/README.md>) |
| 2 | 159993 미로 탈출 | [C](<../C/level2/022_159993_미로_탈출/README.md>) | [C++](<../C++/level2/022_159993_미로_탈출/README.md>) | [Python](<../Python/level2/022_159993_미로_탈출/README.md>) |
| 0 | 181921 배열 만들기 2 | [C](<../C/level0/extra_181921_배열_만들기_2/README.md>) | [C++](<../C++/level0/extra_181921_배열_만들기_2/README.md>) | [Python](<../Python/level0/extra_181921_배열_만들기_2/README.md>) |
| 2 | 388353 지게차와 크레인 | [C](<../C/level2/007_388353_지게차와_크레인/README.md>) | [C++](<../C++/level2/007_388353_지게차와_크레인/README.md>) | [Python](<../Python/level2/007_388353_지게차와_크레인/README.md>) |
| 3 | 468375 발전소 회로 복구 | [C](<../C/level3/005_468375_발전소_회로_복구/README.md>) | [C++](<../C++/level3/005_468375_발전소_회로_복구/README.md>) | [Python](<../Python/level3/005_468375_발전소_회로_복구/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/bfs.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

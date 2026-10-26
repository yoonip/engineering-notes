# 최단 경로와 확장 상태

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 최소화하는 비용부터 확인

최단 경로의 길이는 거리뿐 아니라 시간, 가격, 위험도의 합일 수 있습니다. 먼저 경로 비용의 결합 규칙을 적습니다. 합을 최소화하는 문제와 경로 중 최대 간선의 크기를 최소화하는 문제는 전이가 다릅니다. 후자는 후보 비용을 max(현재 비용, 간선 비용)으로 만드는 최소 병목 경로입니다.

완화는 현재 알려진 거리보다 더 좋은 경로를 발견하면 값을 갱신하는 연산입니다. 정점 v에 대한 후보가 dist[u]+w(u,v)일 때 더 작으면 부모와 거리도 바꿉니다.

## 조건에 따른 알고리즘 선택

| 입력 조건 | 방법 | 대표 시간·추가 공간 |
| --- | --- | --- |
| 모든 이동 비용 동일 | BFS | O(V+E), O(V) |
| 비용이 0 또는 1 | 0-1 BFS | O(V+E), O(V+E) 이내 큐 구현 |
| 모든 비용 비음수 | 이진 힙 Dijkstra | 중복 삽입 구현 O((V+E)log(V+E)), 거리 O(V), 힙 O(E) |
| 음수 허용 | Bellman–Ford | O(VE), O(V) |
| DAG | 위상 순서 완화 | O(V+E), O(V) |
| 작은 그래프의 모든 쌍 | Floyd–Warshall | O(V³), O(V²) |

단순 그래프에서는 힙 Dijkstra를 보통 O((V+E)log V)로 적습니다. 중복 간선이 매우 많으면 힙 크기까지 세어 더 일반적인 식을 사용합니다. 음수 간선에서 확정 규칙을 버린 재삽입 변형은 같은 성능 보장을 갖지 않습니다. [Princeton의 알고리즘 선택 표](https://www.cs.princeton.edu/courses/archive/spring24/cos226/lectures/44ShortestPaths.pdf)를 확인할 수 있습니다.

## 직접 구성한 Dijkstra 추적

방향 간선 S→A=5, S→B=1, B→A=1, A→T=2, B→T=8을 둡니다. 처음 후보는 A=5, B=1입니다. B를 꺼내 A=2, T=9로 바꿉니다. A=2를 꺼내 T=4로 바꿉니다. 나중에 남아 있는 A=5 후보는 현재 거리와 달라 버립니다.

~~~python
from heapq import heappop, heappush  # 최소 거리 후보를 먼저 꺼낼 힙 연산
def dijkstra(adj, start):  # 비음수 가중치 인접 리스트의 최단 거리 계산
    dist = [float('inf')] * len(adj)  # 아직 경로가 없는 상태를 무한대로 표시
    dist[start] = 0  # 출발점의 누적 비용 초기화
    heap = [(0, start)]  # 거리와 정점 번호를 쌍으로 저장
    while heap:  # 처리할 후보가 남아 있으면 반복
        cost, u = heappop(heap)  # 비용이 가장 작은 후보 꺼내기
        if cost != dist[u]:  # 이후 더 짧은 경로로 갱신된 낡은 후보라면
            continue  # 낡은 후보의 간선을 다시 순회하지 않기
        for v, weight in adj[u]:  # u에서 나가는 모든 간선 확인
            candidate = cost + weight  # u를 거친 후보 거리 계산
            if candidate < dist[v]:  # 기존 경로보다 짧은 경우에만 갱신
                dist[v] = candidate  # v까지의 최선 비용 저장
                heappush(heap, (candidate, v))  # 갱신한 후보를 우선순위 큐에 추가
    return dist  # 도달 불가능한 정점은 무한대로 유지
~~~

## 왜 확정할 수 있는지

비음수 간선에서는 아직 처리하지 않은 경로를 더 연장해도 비용이 줄어들지 않습니다. 최소 거리 후보 u보다 더 싼 경로가 나중에 나타나려면 그 경로에서 먼저 확정되지 않은 첫 정점도 u보다 싸야 하므로 최소 후보를 꺼냈다는 사실과 충돌합니다. 이 논리 때문에 음수 간선이 없어야 합니다.

0-1 BFS는 비용 0인 갱신을 덱 앞, 1인 갱신을 뒤에 둡니다. 단순히 최초 발견 시 영구 방문 처리하는 일반 BFS를 그대로 쓰지 않고 더 짧은 거리의 완화를 허용합니다.

Bellman–Ford는 간선 수가 최대 k개인 최단 경로를 k번의 완화 단계로 포괄한다는 관점입니다. V-1회 뒤에도 갱신되는 정점은 출발점에서 도달 가능한 음수 사이클의 영향을 받을 수 있습니다. 목표의 답이 무한히 작아지는지는 그 사이클에서 목표로 갈 수 있는지도 확인합니다. Floyd–Warshall은 중간 정점 k를 허용할지에 따라 dist[i][j]를 갱신하며 k 반복문을 바깥에 둡니다.

## 조건이 있는 이동을 상태로 바꾸기

쿠폰 한 장으로 간선 하나를 무료 통과한다면 정점을 (위치, 쿠폰 사용 여부)로 만듭니다. 일반 이동은 같은 층에 비용 w의 간선, 쿠폰 사용은 미사용 층에서 사용 층으로 비용 0의 간선입니다. 위치만 방문 처리하면 쿠폰을 아껴 온 경로가 사라집니다.

시간표가 있으면 대기 시간을 전이에 넣습니다. 시간에 따라 이동 비용이 바뀌는 모든 문제에 일반 Dijkstra를 바로 적용할 수는 없습니다. 늦게 출발한 사람이 먼저 도착할 수 없는 FIFO 조건 같은 모델의 가정을 확인해야 합니다.

음수 간선이 있지만 음수 사이클은 없는 희소 그래프의 모든 쌍에는 Johnson 재가중치를 검토합니다. Bellman–Ford로 구한 potential h로 w'=w+h[u]-h[v]를 만들면 경로 사이의 비용 차이가 보존되고 간선을 비음수로 만들 수 있습니다. 모든 간선에 같은 상수를 더하는 방법은 간선 수가 다른 경로의 비교를 바꾸므로 대안이 아닙니다.

## 실전·실무와 반례

고정된 비음수 통행 비용의 경로, 단계별 서비스 호출 비용, 이동 제약이 있는 퍼즐에 연결됩니다. 교통 혼잡·용량·여러 차량의 상호 영향까지 포함하면 단일 최단 경로보다 큰 모델이 필요합니다.

C/C++에서는 INF에 가중치를 더하다 정수 범위를 넘지 않도록 도달 여부를 먼저 확인합니다. Python 큰 정수도 연산 비용이 있으므로 입력 크기와 값의 비트 수를 함께 봅니다. 모든 경로를 힙에 저장하지 않고 정점별 최선 거리와 부모만 관리합니다.

복습: 목적지가 힙에 처음 들어갔을 때 종료해도 되는지 확인합니다. 답은 아닙니다. 유효한 최소 후보로 꺼내지는 순간에 종료할 수 있습니다. 위 예제의 T=9는 삽입 뒤 4로 바뀝니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

비음수 방향 그래프에서 미확정 정점 중 최소 거리를 직접 골라 Dijkstra를 수행합니다. 힙과 0-1 BFS는 구현하지 않습니다.

이 예제에서 직접 구현하는 기법은 비음수 Dijkstra · 거리 완화 · 최소 정점 스캔 · 평행 간선 최솟값입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

V E S 뒤에 E줄의 u v w가 주어집니다. 1≤V≤8, 0≤E≤64, 0≤S,u,v<V, 0≤w≤1000000입니다. 평행 간선은 최솟값만 남깁니다.

```text
4 5 0
0 1 5
0 2 1
2 1 1
1 3 2
2 3 8
```

정점 번호순 최단 거리를 출력합니다. 도달하지 못한 정점은 -1입니다.

```text
0 2 1 4
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | distance=[0,INF,INF,INF] | 출발점만 도달한 상태로 시작합니다. |
| 2 | 0 확정 후 distance=[0,5,1,INF] | 직접 연결된 두 후보를 완화합니다. |
| 3 | 2 확정 후 distance=[0,2,1,9] | 2를 거치면 1번까지의 비용이 5에서 2로 줄어듭니다. |
| 4 | 1 확정 후 distance=[0,2,1,4] | 1번을 거친 목표 비용 4가 최종 최단 거리입니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/21-최단경로와확장상태_shortest-path/example.c>)

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


int main(void) {  // 정점 최소 스캔 방식의 Dijkstra
    int n = read_int(), m = read_int(), start = read_int();  // 그래프 크기와 출발점
    int weight[8][8], distance[8], used[8] = {0};  // 최소 간선·거리·확정 여부
    const int inf = 1000000000;  // 최대 단순 경로 비용보다 큰 미도달 값
    for (int i = 0; i < n; ++i) {  // 모든 정점과 간선 후보 초기화
        distance[i] = inf;  // 출발점을 제외한 미도달 상태
        for (int j = 0; j < n; ++j) weight[i][j] = inf;  // 아직 없는 방향 간선
    }  // 초기화 끝
    for (int i = 0; i < m; ++i) {  // 비음수 방향 간선 입력
        int a = read_int(), b = read_int(), cost = read_int();  // 간선의 출발·도착·비용
        if (cost < weight[a][b]) weight[a][b] = cost;  // 평행 간선의 최소 비용 유지
    }  // 간선 입력 끝
    distance[start] = 0;  // 출발 비용은 0
    for (int step = 0; step < n; ++step) {  // 최대 n개 정점을 확정
        int u = -1;  // 이번에 고를 미확정 정점
        for (int v = 0; v < n; ++v) {  // 현재 거리가 가장 작은 후보 찾기
            if (!used[v] && (u == -1 || distance[v] < distance[u])) u = v;  // 최소 거리 후보 갱신
        }  // 최소 후보 선택 끝
        if (u == -1 || distance[u] == inf) break;  // 남은 정점이 전부 미도달이면 종료
        used[u] = 1;  // 비음수 조건으로 현재 최단 거리 확정
        for (int v = 0; v < n; ++v) {  // u를 지나가는 방향 간선 완화
            if (weight[u][v] != inf && distance[u] + weight[u][v] < distance[v]) {  // 실제 간선의 더 짧은 경로
                distance[v] = distance[u] + weight[u][v];  // 새 최단 거리 저장
            }  // 현재 간선 완화 끝
        }  // u의 이웃 갱신 끝
    }  // 모든 도달 거리 계산 끝
    for (int i = 0; i < n; ++i) {  // 번호순 결과 출력
        if (i) write_text(" ");  // 숫자 사이 공백
        write_number(distance[i] == inf ? -1 : distance[i]);  // 미도달만 -1로 변환
    }  // 결과 배열 출력 끝
    write_text("\n"); return 0;  // 줄바꿈 후 정상 종료
}  // Dijkstra 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/21-최단경로와확장상태_shortest-path/example.cpp>)

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


int main(void) {  // 정점 최소 스캔 방식의 Dijkstra
    int n = read_int(), m = read_int(), start = read_int();  // 그래프 크기와 출발점
    int weight[8][8], distance[8], used[8] = {};  // 최소 간선·거리·확정 여부
    const int inf = 1000000000;  // 최대 단순 경로 비용보다 큰 미도달 값
    for (int i = 0; i < n; ++i) {  // 모든 정점과 간선 후보 초기화
        distance[i] = inf;  // 출발점을 제외한 미도달 상태
        for (int j = 0; j < n; ++j) weight[i][j] = inf;  // 아직 없는 방향 간선
    }  // 초기화 끝
    for (int i = 0; i < m; ++i) {  // 비음수 방향 간선 입력
        int a = read_int(), b = read_int(), cost = read_int();  // 간선의 출발·도착·비용
        if (cost < weight[a][b]) weight[a][b] = cost;  // 평행 간선의 최소 비용 유지
    }  // 간선 입력 끝
    distance[start] = 0;  // 출발 비용은 0
    for (int step = 0; step < n; ++step) {  // 최대 n개 정점을 확정
        int u = -1;  // 이번에 고를 미확정 정점
        for (int v = 0; v < n; ++v) {  // 현재 거리가 가장 작은 후보 찾기
            if (!used[v] && (u == -1 || distance[v] < distance[u])) u = v;  // 최소 거리 후보 갱신
        }  // 최소 후보 선택 끝
        if (u == -1 || distance[u] == inf) break;  // 남은 정점이 전부 미도달이면 종료
        used[u] = 1;  // 비음수 조건으로 현재 최단 거리 확정
        for (int v = 0; v < n; ++v) {  // u를 지나가는 방향 간선 완화
            if (weight[u][v] != inf && distance[u] + weight[u][v] < distance[v]) {  // 실제 간선의 더 짧은 경로
                distance[v] = distance[u] + weight[u][v];  // 새 최단 거리 저장
            }  // 현재 간선 완화 끝
        }  // u의 이웃 갱신 끝
    }  // 모든 도달 거리 계산 끝
    for (int i = 0; i < n; ++i) {  // 번호순 결과 출력
        if (i) write_text(" ");  // 숫자 사이 공백
        write_number(distance[i] == inf ? -1 : distance[i]);  // 미도달만 -1로 변환
    }  // 결과 배열 출력 끝
    write_text("\n"); return 0;  // 줄바꿈 후 정상 종료
}  // Dijkstra 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/21-최단경로와확장상태_shortest-path/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m, start = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 그래프 크기와 출발점
    inf = 10 ** 9  # 가능한 최단 거리보다 큰 표시값
    weight = [[inf] * n for _ in range(n)]  # 방향 간선의 최소 비용 행렬
    for _ in range(m):  # 비음수 간선 입력
        a, b, cost = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 출발·도착·비용
        weight[a][b] = min(weight[a][b], cost)  # 평행 간선 중 최솟값만 저장
    distance = [inf] * n  # 미도달 거리 초기화
    used = [False] * n  # 확정 여부
    distance[start] = 0  # 출발 비용 0
    for _ in range(n):  # 정점을 하나씩 확정
        u = -1  # 다음 최소 후보
        for v in range(n):  # 미확정 정점의 현재 거리 비교
            if not used[v] and (u == -1 or distance[v] < distance[u]):  # 더 작은 후보 확인
                u = v  # 이번 확정 후보 갱신
        if u == -1 or distance[u] == inf:  # 남은 정점이 미도달이면
            break  # 불필요한 확정 생략
        used[u] = True  # 비음수 간선 조건으로 거리 확정
        for v in range(n):  # 현재 정점에서 나가는 간선 확인
            if weight[u][v] != inf:  # 실제 간선만 사용
                distance[v] = min(distance[v], distance[u] + weight[u][v])  # 더 짧은 경로 완화
    print(*(-1 if value == inf else value for value in distance))  # 미도달을 구분해 출력

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

최소 후보 선택과 이웃 완화를 각각 V번 스캔합니다. 힙을 쓰지 않는 인접 행렬 구현입니다.

[예제 입력](<예제_examples/21-최단경로와확장상태_shortest-path/input.txt>) · [예상 출력](<예제_examples/21-최단경로와확장상태_shortest-path/output.txt>) · [예제 실행 방법](<예제_examples/21-최단경로와확장상태_shortest-path/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 2 | 12978 배달 | — | [C++](<../C++/level2/096_12978_배달/README.md>) | [Python](<../Python/level2/096_12978_배달/README.md>) |
| 3 | 72413 합승 택시 요금 | — | [C++](<../C++/level3/045_72413_합승_택시_요금/README.md>) | [Python](<../Python/level3/045_72413_합승_택시_요금/README.md>) |
| 4 | 81304 미로 탈출 | [C](<../C/level4/extra_81304_미로_탈출/README.md>) | [C++](<../C++/level4/extra_81304_미로_탈출/README.md>) | [Python](<../Python/level4/extra_81304_미로_탈출/README.md>) |
| 3 | 468376 최고 속도 | [C](<../C/level3/004_468376_최고_속도/README.md>) | [C++](<../C++/level3/004_468376_최고_속도/README.md>) | [Python](<../Python/level3/004_468376_최고_속도/README.md>) |
| 5 | 214293 중요한 도로 | [C](<../C/level5/005_214293_중요한_도로/README.md>) | [C++](<../C++/level5/005_214293_중요한_도로/README.md>) | [Python](<../Python/level5/revisit_20261024/005_214293_중요한_도로/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/shortest-path.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

# 위상 정렬과 DAG의 동적 계획법

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 계산 순서를 문제의 일부로 보기

유향 비순환 그래프(DAG)는 방향을 따라 돌아오는 사이클이 없는 그래프입니다. 위상 순서는 모든 간선 u→v에서 u가 v보다 앞서는 순서입니다. 정렬 키가 숫자나 문자열이 아니라 선행 조건이라는 점에서 일반 정렬과 다릅니다.

어떤 값을 계산하려면 다른 값이 먼저 필요할 때 위상 순서를 사용합니다. 위상 순서를 얻은 뒤 그 순서로 DP를 하면 아직 계산하지 않은 상태를 잘못 읽는 문제를 피합니다. [CMU DFS 강의 3절](https://www.cs.cmu.edu/~15451-f18/lectures/lec19-DFS-strong-components.pdf)은 DAG와 DFS 종료 순서의 관계를 증명합니다.

## Kahn 알고리즘의 절차

1. 각 정점으로 들어오는 간선 수인 진입 차수를 셉니다.
2. 진입 차수가 0인 정점을 큐에 넣습니다.
3. 하나를 꺼내 결과에 붙이고 그 정점에서 나가는 간선을 제거합니다.
4. 제거 후 진입 차수가 0이 된 이웃을 큐에 넣습니다.
5. 결과 길이가 V보다 작으면 사이클 때문에 끝내지 못한 정점이 있습니다.

큐의 정점에는 미처리 선행 조건이 없다는 불변식을 유지합니다. DAG에 정점이 남아 있다면 반드시 진입 차수 0인 정점이 있습니다. 없다고 가정해 선행 정점을 계속 따라가면 유한한 그래프에서 반복이 생겨 사이클이 되기 때문입니다.

## 직접 구성한 예제

A와 B가 끝나야 C를 시작하고, C가 끝나야 D를 시작한다고 둡니다. 간선은 A→C, B→C, C→D입니다.

| 단계 | 진입 차수 0 후보 | 처리 후 변화 |
| --- | --- | --- |
| 시작 | A, B | C의 진입 차수는 2입니다. |
| A 처리 | B | C가 1로 줄어 아직 준비되지 않습니다. |
| B 처리 | C | C가 0이 되어 준비됩니다. |
| C 처리 | D | D가 0이 되어 준비됩니다. |

A,B,C,D와 B,A,C,D는 모두 정답 순서입니다. 최소 번호를 우선하는 조건이 있으면 큐 대신 최소 힙을 사용합니다. 이 경우 시간은 O((V+E)log V) 이내이며 단순 FIFO는 O(V+E)입니다.

## 위상 순서에서 계산하는 값

작업 시간이 A=2, B=5, C=3, D=1이면 완료 시각은 finish[C]=max(2,5)+3=8, finish[D]=9입니다. 독립된 선행 작업을 동시에 진행할 수 있다는 가정이 있으므로 합이 아닌 최댓값을 사용합니다. 작업자가 한 명뿐이면 이 계산은 실제 일정의 충분조건이 아닙니다.

~~~text
각 작업의 finish를 자기 작업 시간으로 초기화  # 선행 조건 없는 작업의 완료 시각 준비
위상 순서대로 u를 처리  # 모든 선행 결과가 반영된 뒤 작업 확인
    각 간선 u→v에 대해  # u 완료가 v의 시작을 제한하는 관계 확인
        finish[v] = max(finish[v], finish[u] + duration[v])  # 가장 늦게 끝나는 선행 조건 반영
~~~

경로 수는 ways[v]+=ways[u], 최단 경로는 min, 최장 경로는 max로 바뀝니다. DAG에서는 경로가 순환하지 않으므로 음수 간선이 있어도 위상 순서 최단 경로를 O(V+E)에 계산할 수 있습니다. 불가능한 상태의 초기값과 빈 경로를 셀지 여부는 별도로 정합니다.

## 사이클 판정에서 놓치기 쉬운 부분

시작점 하나에서만 탐색하면 다른 연결 부분의 사이클을 놓칠 수 있습니다. 전체 그래프의 순서가 필요하면 모든 정점을 처리합니다. 중복 간선을 저장했다면 진입 차수도 중복 횟수만큼 세고 제거합니다. 진입 차수만 중복을 없애면 음수가 되는 오류가 생깁니다.

큐가 빈 상태에 남은 정점이 모두 사이클 위에 있는 것은 아닙니다. 사이클의 뒤에 의존하는 정점도 처리되지 못합니다. 어느 정점이 실제 사이클 구성원인지 필요하면 SCC로 분석합니다.

## 실무 연결

빌드 대상, 데이터 처리 파이프라인, 스프레드시트 셀의 의존 관계를 분석하는 모형에 사용합니다. 실제 시스템에서는 순서뿐 아니라 변경된 부분의 재계산, 실패 전파, 자원 제한과 동시성도 필요합니다. 정적인 DAG와 실행 중 바뀌는 의존 관계를 구분합니다.

C/C++은 진입 차수를 충분한 정수 범위로 저장합니다. Python에서는 선행 조건 목록을 매번 전체 검색하지 않고 인접 리스트로 후속 작업만 갱신합니다. 순서가 하나인지 확인하려면 각 단계의 선택 가능 후보가 하나뿐인지 봅니다. 사이클 유무와 순서 유일성은 다른 질문입니다.

## 복습과 연결

복습: DFS의 종료 순서를 뒤집으면 항상 위상 순서인지 확인합니다. 답은 사이클이 없는 방향 그래프에서만 가능합니다. 사이클이 있는 그래프에서도 종료 순서 배열은 만들어지지만 위상 순서는 아닙니다.

[DP 상태와 전이](16-동적계획법의상태와전이_dynamic-programming.md) · [SCC와 2-SAT](24-강한연결요소단절점2SAT_scc-lowlink-2sat.md)

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

독립 작업을 병렬로 진행할 수 있다고 가정하고 Kahn 위상 정렬 중 선행 작업의 최대 완료 시각을 전달합니다. 인력 수 제한은 모델에 없습니다.

이 예제에서 직접 구현하는 기법은 Kahn 위상 정렬 · DAG 완료 시각 DP · 사이클 존재 판정입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

V E, 이어서 V개 작업 시간, E개의 선행 간선 u v입니다. 1≤V≤8, 0≤E≤28, 시간은 0~100이며 정점 번호는 0부터입니다. 중복 간선은 한 번만 저장합니다.

```text
4 3
2 5 3 1
0 2
1 2
2 3
```

사이클이 없으면 정점 번호순 최소 완료 시각을 출력하고, 사이클이 있으면 CYCLE을 출력합니다.

```text
2 5 8 9
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | degree=[0,0,2,1], finish=[2,5,3,1] | 각 작업 자체 시간으로 초기화합니다. |
| 2 | 0 완료 후 finish[2]=5, degree[2]=1 | 첫 선행 작업만 끝나 아직 2를 시작하지 않습니다. |
| 3 | 1 완료 후 finish[2]=8, degree[2]=0 | 더 늦은 1번 완료 시각 5를 반영합니다. |
| 4 | 3까지 처리 후 finish[3]=9, processed=4 | 후속 작업까지 처리하여 전체 DAG의 완료 시각을 얻습니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/23-위상정렬과DAG_topological-dag/example.c>)

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


int main(void) {  // Kahn 순서와 완료 시각 DP
    int n = read_int(), m = read_int();  // 작업 수와 선행 관계 수
    int duration[8], finish[8], degree[8] = {0}, adj[8][8] = {0}, queue[8];  // 시간·진입 차수·연결·큐
    for (int i = 0; i < n; ++i) { duration[i] = read_int(); finish[i] = duration[i]; }  // 선행 작업 없는 기본 완료 시각
    for (int i = 0; i < m; ++i) {  // 선행 관계 입력
        int u = read_int(), v = read_int();  // u 완료 후 v 시작
        if (!adj[u][v]) { adj[u][v] = 1; ++degree[v]; }  // 중복을 한 번만 진입 차수에 반영
    }  // 선행 관계 입력 끝
    int head = 0, tail = 0, processed = 0;  // 큐 위치와 처리한 작업 수
    for (int u = 0; u < n; ++u) if (!degree[u]) queue[tail++] = u;  // 바로 시작할 수 있는 작업 등록
    while (head < tail) {  // 준비된 작업을 차례로 완료 처리
        int u = queue[head++]; ++processed;  // 선행 조건이 모두 끝난 작업
        for (int v = 0; v < n; ++v) {  // 이 작업을 기다리는 후속 작업
            if (!adj[u][v]) continue;  // 실제 선행 관계만 처리
            if (finish[u] + duration[v] > finish[v]) finish[v] = finish[u] + duration[v];  // 가장 늦은 선행 완료 시각 반영
            if (--degree[v] == 0) queue[tail++] = v;  // 모든 선행 작업이 끝나면 큐에 추가
        }  // 후속 작업 갱신 끝
    }  // 가능한 작업 처리 끝
    if (processed != n) { write_text("CYCLE\n"); return 0; }  // 남은 작업은 순환 의존의 영향
    for (int i = 0; i < n; ++i) {  // 작업 번호순 완료 시각 출력
        if (i) write_text(" ");  // 출력 숫자 사이 공백
        write_number(finish[i]);  // 현재 작업의 최소 완료 시각
    }  // 완료 시각 배열 출력 끝
    write_text("\n"); return 0;  // 결과 줄을 마치고 종료
}  // 위상 DP 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/23-위상정렬과DAG_topological-dag/example.cpp>)

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


int main(void) {  // Kahn 순서와 완료 시각 DP
    int n = read_int(), m = read_int();  // 작업 수와 선행 관계 수
    int duration[8], finish[8], degree[8] = {}, adj[8][8] = {}, queue[8];  // 시간·진입 차수·연결·큐
    for (int i = 0; i < n; ++i) { duration[i] = read_int(); finish[i] = duration[i]; }  // 선행 작업 없는 기본 완료 시각
    for (int i = 0; i < m; ++i) {  // 선행 관계 입력
        int u = read_int(), v = read_int();  // u 완료 후 v 시작
        if (!adj[u][v]) { adj[u][v] = 1; ++degree[v]; }  // 중복을 한 번만 진입 차수에 반영
    }  // 선행 관계 입력 끝
    int head = 0, tail = 0, processed = 0;  // 큐 위치와 처리한 작업 수
    for (int u = 0; u < n; ++u) if (!degree[u]) queue[tail++] = u;  // 바로 시작할 수 있는 작업 등록
    while (head < tail) {  // 준비된 작업을 차례로 완료 처리
        int u = queue[head++]; ++processed;  // 선행 조건이 모두 끝난 작업
        for (int v = 0; v < n; ++v) {  // 이 작업을 기다리는 후속 작업
            if (!adj[u][v]) continue;  // 실제 선행 관계만 처리
            if (finish[u] + duration[v] > finish[v]) finish[v] = finish[u] + duration[v];  // 가장 늦은 선행 완료 시각 반영
            if (--degree[v] == 0) queue[tail++] = v;  // 모든 선행 작업이 끝나면 큐에 추가
        }  // 후속 작업 갱신 끝
    }  // 가능한 작업 처리 끝
    if (processed != n) { write_text("CYCLE\n"); return 0; }  // 남은 작업은 순환 의존의 영향
    for (int i = 0; i < n; ++i) {  // 작업 번호순 완료 시각 출력
        if (i) write_text(" ");  // 출력 숫자 사이 공백
        write_number(finish[i]);  // 현재 작업의 최소 완료 시각
    }  // 완료 시각 배열 출력 끝
    write_text("\n"); return 0;  // 결과 줄을 마치고 종료
}  // 위상 DP 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/23-위상정렬과DAG_topological-dag/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m = int(next(tokens)), int(next(tokens))  # 작업 수와 선행 관계 수
    duration = [int(next(tokens)) for _ in range(n)]  # 각 작업의 소요 시간
    finish = duration[:]  # 선행 조건이 없을 때의 완료 시각
    degree = [0] * n  # 아직 남은 선행 관계 수
    adj = [[0] * n for _ in range(n)]  # 선행 관계의 인접 행렬
    for _ in range(m):  # 선행 간선 입력
        u, v = int(next(tokens)), int(next(tokens))  # u가 v보다 먼저 끝나야 함
        if not adj[u][v]:  # 중복 관계는 한 번만 저장
            adj[u][v] = 1  # 방향 간선 표시
            degree[v] += 1  # 남은 선행 조건 추가
    queue = [u for u in range(n) if degree[u] == 0]  # 바로 처리 가능한 작업
    head = processed = 0  # 큐 위치와 처리 수
    while head < len(queue):  # 준비 작업이 남은 동안 반복
        u = queue[head]  # 다음 완료 작업
        head += 1  # 읽는 위치 이동
        processed += 1  # 사이클 판정용 처리 수
        for v in range(n):  # 후속 작업 후보 확인
            if not adj[u][v]:  # 관계없는 작업
                continue  # 갱신 생략
            finish[v] = max(finish[v], finish[u] + duration[v])  # 가장 늦은 선행 완료 시각
            degree[v] -= 1  # 끝난 선행 작업 하나 제거
            if degree[v] == 0:  # 남은 선행 조건이 없으면
                queue.append(v)  # 이후 처리할 작업에 추가
    if processed != n:  # 전체 작업을 처리하지 못한 경우
        print("CYCLE")  # 순환 의존 표시
    else:  # 모든 작업이 위상 순서로 처리된 경우
        print(*finish)  # 정점별 최소 완료 시각

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

인접 행렬의 각 행을 한 번 확인합니다. 완료 시각은 선행 작업의 최댓값으로 갱신합니다.

[예제 입력](<예제_examples/23-위상정렬과DAG_topological-dag/input.txt>) · [예상 출력](<예제_examples/23-위상정렬과DAG_topological-dag/output.txt>) · [예제 실행 방법](<예제_examples/23-위상정렬과DAG_topological-dag/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 4 | 67260 동굴 탐험 | — | [C++](<../C++/level4/extra_67260_동굴_탐험/README.md>) | [Python](<../Python/level4/extra_67260_동굴_탐험/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/topological.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

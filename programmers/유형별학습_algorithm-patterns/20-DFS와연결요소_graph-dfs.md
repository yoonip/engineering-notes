# DFS와 연결 요소, 사이클과 오일러 경로

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 깊게 들어갔다 돌아오는 순서

DFS는 아직 방문하지 않은 이웃을 따라 더 진행한 뒤 돌아옵니다. 재귀 호출이 관리하는 것은 현재 탐색 경로와 돌아갈 지점입니다. 깊게 들어간다는 동작보다 진입 시점과 종료 시점이 구별된다는 사실이 중요합니다. 자식의 결과가 끝난 뒤 부모의 값을 계산하는 트리 DP와, 의존 관계의 종료 순서를 구하는 데 사용합니다.

정점 방문은 도달 가능성을 중복 계산하지 않는 방법입니다. 반면 모든 경로를 찾는 백트래킹은 현재 경로에서만 방문을 제한하고 돌아올 때 복구할 수 있습니다. 둘 다 재귀라고 해서 방문 배열의 의미가 같지는 않습니다.

## 직접 구성한 연결 요소 예제

무방향 그래프의 간선이 0-1, 1-2, 3-4이고 정점 5가 고립되어 있다고 둡니다. 0에서 DFS를 하면 0,1,2만 발견합니다. 바깥 반복문에서 아직 방문하지 않은 3과 5를 새 출발점으로 잡아 총 세 요소를 얻습니다.

~~~python
def components(adj):  # 무방향 그래프의 연결 요소에 번호 부여
    label = [-1] * len(adj)  # 아직 요소가 정해지지 않은 정점은 -1
    count = 0  # 지금까지 시작한 요소 수
    for start in range(len(adj)):  # 고립 정점까지 모든 정점을 출발 후보로 확인
        if label[start] != -1:  # 이전 탐색에 포함된 정점이면 건너뛰기
            continue  # 같은 요소를 다시 시작하지 않기
        stack = [start]  # 현재 요소의 탐색 스택 생성
        label[start] = count  # 넣는 시점에 요소 번호 기록
        while stack:  # 이 요소의 미처리 정점이 남으면 반복
            u = stack.pop()  # 마지막에 발견한 정점부터 이웃 확인
            for v in adj[u]:  # u에 연결된 이웃을 순회
                if label[v] == -1:  # 아직 어떤 요소에도 들어가지 않았다면
                    label[v] = count  # 현재 요소에 포함
                    stack.append(v)  # 이후 이웃을 확인할 대상으로 추가
        count += 1  # 한 요소의 탐색을 끝내고 다음 번호 준비
    return label, count  # 각 정점의 소속과 전체 요소 수 반환
~~~

이 코드는 연결 요소 판정에 충분합니다. 재귀 DFS의 정확한 종료 순서를 재현하는 코드는 아닙니다. 종료 순서가 필요하면 (정점, 다음에 볼 이웃 인덱스) 프레임이나 진입·퇴장 표식을 저장합니다.

## 사이클을 판단하는 정보

방향 그래프에서는 미방문·현재 경로에 있음·종료의 세 상태를 구별합니다. 현재 경로의 조상으로 돌아가는 간선은 사이클을 만듭니다. 종료된 정점으로 향하는 간선이 있다고 사이클인 것은 아닙니다. 0→1, 0→2, 2→1은 사이클이 없는 반례입니다.

무방향 그래프에서는 방금 넘어온 간선의 반대 방향을 그대로 사이클로 세지 않습니다. 평행 간선이 있으면 부모 정점 번호만 비교해서 두 간선을 모두 건너뛰지 말고 부모 간선 ID를 구별합니다. DFS 진입·퇴장과 간선 분류는 [CMU DFS 강의의 2~3절](https://www.cs.cmu.edu/~15451-f18/lectures/lec19-DFS-strong-components.pdf)에서 근거를 확인할 수 있습니다.

## 이분 그래프와 색칠

이웃끼리 다른 두 색을 배정합니다. 이미 같은 색인 두 정점을 잇는 간선이 나오면 이분 그래프가 아닙니다. 삼각형은 세 간선 뒤 시작 색과 충돌합니다. 무방향 그래프에 홀수 길이 사이클이 없다는 조건과 같습니다. 이 성질은 두 집단의 매칭 문제로 넘어갈 때 필요합니다. [Princeton Bipartite API](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/Bipartite.html)는 판정과 O(V+E) 비용을 명시합니다.

## 간선을 모두 쓰는 오일러 경로

오일러 경로는 모든 간선을 한 번씩 쓰고, 해밀턴 경로는 모든 정점을 한 번씩 씁니다. 방문의 대상이 다르므로 같은 탐색으로 바꾸면 안 됩니다. Hierholzer 방식은 더 나갈 간선이 없는 정점을 결과에 넣고 결과를 뒤집습니다. 소모한 간선을 다시 사용하지 않으며, 닫힌 부분 경로를 이어 붙인다는 원리입니다.

무방향 그래프는 간선이 있는 정점들이 연결되어 있고 홀수 차수 정점이 0개 또는 2개일 때 오일러 회로 또는 열린 경로가 가능합니다. 방향 그래프의 열린 경로는 시작점의 out-in=1, 끝점의 in-out=1, 나머지는 같아야 합니다. 간선이 있는 정점의 연결 조건과 실제 사용 간선 수까지 확인합니다.

직접 구성한 A-B, B-C, C-A, A-D에서는 A와 D만 홀수 차수이므로 A에서 시작해 A-B-C-A-D로 모든 간선을 사용합니다. 사전순 조건이 붙으면 간선 선택 순서와 역순 결과의 관계까지 따로 증명합니다.

## 비용과 안전한 구현

인접 리스트 DFS는 O(V+E) 시간과 O(V) 방문·스택 공간을 사용합니다. 깊이 V의 사슬은 재귀 깊이도 V입니다. Python 재귀 제한만 크게 올려도 메모리와 호출 비용은 사라지지 않습니다. C와 C++도 호출 스택 한계가 있으므로 입력이 긴 사슬이면 명시적 스택을 검토합니다.

Hierholzer는 간선 삭제를 상수 시간에 할 수 있으면 O(V+E)이며, 매번 배열 중간을 삭제하면 비용이 커집니다. 간선마다 ID를 부여하거나 인접 목록의 뒤에서 꺼내는 식으로 관리합니다.

## 실제 쓰임과 복습

연결 요소는 분리된 네트워크와 영상의 붙어 있는 영역을 식별하는 데 연결됩니다. DFS 종료 순서는 의존 관계 분석에 사용합니다. 실제 장애 원인을 찾는 일은 연결 판정만으로 끝나지 않으며 방향·권한·시간에 따라 간선이 달라질 수 있습니다.

복습: 방향 그래프에서 DFS 한 번으로 도달한 정점들은 항상 하나의 강한 연결 요소인지 확인합니다. 답은 아닙니다. 0→1에서는 0에서 1로 갈 수 있지만 되돌아갈 수 없습니다. [강한 연결 요소](24-강한연결요소단절점2SAT_scc-lowlink-2sat.md)로 구분합니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

무방향 그래프의 연결 요소를 명시적 스택으로 찾습니다. 재귀 DFS의 종료 순서나 lowlink를 구현하는 예제는 아닙니다.

이 예제에서 직접 구현하는 기법은 반복 DFS · 무방향 연결 요소 · 발견 시 소속 표시입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

V E 뒤에 E개의 무방향 간선 u v가 주어집니다. 1≤V≤8, 0≤E≤28이며 정점은 0부터이고 자기 간선·평행 간선은 없습니다.

```text
6 3
0 1
1 2
3 4
```

첫 줄에 연결 요소 수, 둘째 줄에 정점 번호순 요소 번호를 출력합니다. 요소 번호는 가장 작은 미방문 정점부터 0,1,...을 부여합니다.

```text
3
0 0 0 1 1 2
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | label=[-1,-1,-1,-1,-1,-1] | 아직 어느 요소에도 배정하지 않습니다. |
| 2 | start=0, 발견={0,1,2}, count=1 | 0에서 도달하는 정점에 요소 번호 0을 붙입니다. |
| 3 | start=3, 발견={3,4}, count=2 | 다음 미방문 정점에서 새 요소를 시작합니다. |
| 4 | start=5, label=[0,0,0,1,1,2], count=3 | 고립 정점도 하나의 연결 요소로 셉니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/20-DFS와연결요소_graph-dfs/example.c>)

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


int main(void) {  // DFS로 연결 요소 번호 계산
    int n = read_int(), m = read_int();  // 그래프의 정점 수와 간선 수
    int adj[8][8] = {0}, label[8], stack[8];  // 인접 행렬·소속·탐색 스택
    for (int i = 0; i < m; ++i) {  // 간선 입력
        int a = read_int(), b = read_int();  // 간선 양끝
        adj[a][b] = adj[b][a] = 1;  // 두 방향의 연결 저장
    }  // 간선 입력 끝
    for (int i = 0; i < n; ++i) label[i] = -1;  // 아직 소속이 없는 정점 표시
    int count = 0;  // 지금까지 발견한 연결 요소 수
    for (int start = 0; start < n; ++start) {  // 고립 정점까지 새 출발 후보 확인
        if (label[start] != -1) continue;  // 이미 끝낸 요소는 다시 탐색하지 않기
        int top = 0; stack[top++] = start; label[start] = count;  // 새 요소의 시작점 등록
        while (top) {  // 현재 요소의 미처리 정점이 남으면 반복
            int u = stack[--top];  // 마지막에 넣은 정점부터 확인
            for (int v = 0; v < n; ++v) {  // 연결된 이웃 후보 확인
                if (adj[u][v] && label[v] == -1) {  // 새로 발견한 이웃만 스택에 넣기
                    label[v] = count; stack[top++] = v;  // 중복 삽입 전에 소속 확정
                }  // 새 이웃 등록 끝
            }  // 현재 정점의 이웃 확인 끝
        }  // 한 연결 요소 탐색 끝
        ++count;  // 다음 요소에 사용할 번호
    }  // 모든 연결 요소 탐색 끝
    write_number(count); write_text("\n");  // 요소 수 출력
    for (int i = 0; i < n; ++i) {  // 번호순 소속 출력
        if (i) write_text(" ");  // 소속 번호 사이 공백
        write_number(label[i]);  // 현재 정점의 요소 번호
    }  // 소속 배열 출력 끝
    write_text("\n"); return 0;  // 결과 줄을 끝내고 종료
}  // 연결 요소 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/20-DFS와연결요소_graph-dfs/example.cpp>)

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


int main(void) {  // DFS로 연결 요소 번호 계산
    int n = read_int(), m = read_int();  // 그래프의 정점 수와 간선 수
    int adj[8][8] = {}, label[8], stack[8];  // 인접 행렬·소속·탐색 스택
    for (int i = 0; i < m; ++i) {  // 간선 입력
        int a = read_int(), b = read_int();  // 간선 양끝
        adj[a][b] = adj[b][a] = 1;  // 두 방향의 연결 저장
    }  // 간선 입력 끝
    for (int i = 0; i < n; ++i) label[i] = -1;  // 아직 소속이 없는 정점 표시
    int count = 0;  // 지금까지 발견한 연결 요소 수
    for (int start = 0; start < n; ++start) {  // 고립 정점까지 새 출발 후보 확인
        if (label[start] != -1) continue;  // 이미 끝낸 요소는 다시 탐색하지 않기
        int top = 0; stack[top++] = start; label[start] = count;  // 새 요소의 시작점 등록
        while (top) {  // 현재 요소의 미처리 정점이 남으면 반복
            int u = stack[--top];  // 마지막에 넣은 정점부터 확인
            for (int v = 0; v < n; ++v) {  // 연결된 이웃 후보 확인
                if (adj[u][v] && label[v] == -1) {  // 새로 발견한 이웃만 스택에 넣기
                    label[v] = count; stack[top++] = v;  // 중복 삽입 전에 소속 확정
                }  // 새 이웃 등록 끝
            }  // 현재 정점의 이웃 확인 끝
        }  // 한 연결 요소 탐색 끝
        ++count;  // 다음 요소에 사용할 번호
    }  // 모든 연결 요소 탐색 끝
    write_number(count); write_text("\n");  // 요소 수 출력
    for (int i = 0; i < n; ++i) {  // 번호순 소속 출력
        if (i) write_text(" ");  // 소속 번호 사이 공백
        write_number(label[i]);  // 현재 정점의 요소 번호
    }  // 소속 배열 출력 끝
    write_text("\n"); return 0;  // 결과 줄을 끝내고 종료
}  // 연결 요소 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/20-DFS와연결요소_graph-dfs/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m = int(next(tokens)), int(next(tokens))  # 정점 수와 간선 수
    adj = [[0] * n for _ in range(n)]  # 독립적인 행들로 연결 표 생성
    for _ in range(m):  # 무방향 간선 입력
        a, b = int(next(tokens)), int(next(tokens))  # 간선의 양끝
        adj[a][b] = adj[b][a] = 1  # 양방향 연결
    label = [-1] * n  # 미방문 정점 표시
    count = 0  # 새 연결 요소 번호
    for start in range(n):  # 고립 정점도 출발 후보에 포함
        if label[start] != -1:  # 이전 요소에 들어간 정점
            continue  # 중복 탐색 생략
        stack = [start]  # 이번 요소의 DFS 스택
        label[start] = count  # 넣는 순간 현재 소속 기록
        while stack:  # 이 요소의 후보가 남은 동안 반복
            u = stack.pop()  # LIFO 순서로 정점 꺼내기
            for v in range(n):  # 연결된 이웃 후보 확인
                if adj[u][v] and label[v] == -1:  # 새 이웃만 등록
                    label[v] = count  # 스택 중복 삽입 방지
                    stack.append(v)  # 다음 DFS 후보 추가
        count += 1  # 한 요소를 끝내고 번호 증가
    print(count)  # 연결 요소 수
    print(*label)  # 정점별 소속

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

예제는 인접 행렬을 사용하므로 각 정점에서 V개 이웃 후보를 확인합니다. 스택에는 각 정점이 한 번 들어갑니다.

[예제 입력](<예제_examples/20-DFS와연결요소_graph-dfs/input.txt>) · [예상 출력](<예제_examples/20-DFS와연결요소_graph-dfs/output.txt>) · [예제 실행 방법](<예제_examples/20-DFS와연결요소_graph-dfs/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 3 | 43162 네트워크 | — | [C++](<../C++/level3/061_43162_네트워크/README.md>) | [Python](<../Python/level3/061_43162_네트워크/README.md>) |
| 2 | 86971 전력망을 둘로 나누기 | [C](<../C/level2/050_86971_전력망을_둘로_나누기/README.md>) | [C++](<../C++/level2/050_86971_전력망을_둘로_나누기/README.md>) | [Python](<../Python/level2/050_86971_전력망을_둘로_나누기/README.md>) |
| 3 | 43164 여행경로 | — | [C++](<../C++/level3/059_43164_여행경로/README.md>) | [Python](<../Python/level3/059_43164_여행경로/README.md>) |
| 2 | 468373 바이러스 파이프 | [C](<../C/level2/003_468373_바이러스_파이프/README.md>) | [C++](<../C++/level2/003_468373_바이러스_파이프/README.md>) | [Python](<../Python/level2/003_468373_바이러스_파이프/README.md>) |
| 3 | 468381 기차 선로 | [C](<../C/level3/001_468381_기차_선로/README.md>) | [C++](<../C++/level3/001_468381_기차_선로/README.md>) | [Python](<../Python/level3/001_468381_기차_선로/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/dfs.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

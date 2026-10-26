# 강한 연결 요소, 단절점·단절선과 2-SAT

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 연결이라는 말의 서로 다른 의미

무방향 연결 요소에서는 두 정점 사이를 오갈 수 있습니다. 방향 그래프에서는 한쪽 도달만으로 부족하며 서로 도달 가능한 정점들을 강한 연결 요소(SCC)로 묶습니다. SCC를 한 정점으로 압축하면 DAG가 됩니다. 압축 뒤에도 사이클이 있다면 그 요소들을 서로 오갈 수 있어 원래 하나의 SCC여야 하기 때문입니다.

단절선(bridge)은 무방향 그래프에서 삭제하면 연결 요소 수가 증가하는 간선입니다. 단절점(articulation point)은 삭제하면 나머지 그래프의 연결 요소 수가 증가하는 정점입니다. SCC, bridge, articulation point는 질문과 그래프 방향이 다릅니다.

## SCC를 구하는 두 방법

Kosaraju는 한 그래프의 DFS 종료 순서와 반대 방향 그래프의 탐색 순서를 결합합니다. 예를 들어 원래 그래프의 종료 순서 역순으로 역그래프를 탐색하면 SCC를 하나씩 분리할 수 있습니다. 어느 그래프를 먼저 썼는지에 따라 두 번째 방향과 순서를 함께 맞춰야 합니다.

Tarjan은 DFS 방문 번호와 lowlink, 아직 SCC로 확정되지 않은 정점의 스택을 사용합니다. low[u]가 방문 번호와 같아질 때 u를 뿌리로 하는 SCC를 스택에서 꺼냅니다. 이미 다른 SCC로 확정된 정점으로 향하는 간선은 같은 방식으로 lowlink에 반영하지 않습니다. 재귀 호출 스택과 SCC 스택도 구별합니다.

둘 다 인접 리스트에서 시간 O(V+E), 추가 공간 O(V)이며 Kosaraju는 역간선 저장 O(V+E)도 필요합니다. [Princeton의 strong connectivity 설명](https://algs4.cs.princeton.edu/42digraph/)과 [CMU 강의 4절 이후](https://www.cs.cmu.edu/~15451-f18/lectures/lec19-DFS-strong-components.pdf)에서 SCC 압축과 선형 탐색의 원리를 확인합니다.

## 직접 구성한 SCC 예제

A→B, B→A, B→C, C→D, D→C, D→E를 둡니다. SCC는 {A,B}, {C,D}, {E}입니다. 압축 그래프는 {A,B}→{C,D}→{E}입니다. A에서 E로 갈 수 있다는 사실이 A와 E를 같은 요소로 만들지는 않습니다.

이 압축 그래프에서 도달 가능한 보상의 최댓값, 시작점에서 갈 수 있는 요소의 수 같은 값을 DAG DP로 계산할 수 있습니다. 원래 그래프의 사이클을 무시하고 바로 위상 정렬하려는 시도와 차이가 있습니다.

## 무방향 그래프의 low 값과 단절선

DFS의 진입 번호 tin[u]를 기록합니다. low[u]는 u의 DFS 서브트리에서 트리 간선들을 따라간 뒤 최대 한 개의 역방향 간선으로 도달할 수 있는 가장 작은 진입 번호입니다.

트리 간선 u-v에서 low[v]>tin[u]이면 v 쪽에서 u나 그 조상으로 우회하는 길이 없으므로 그 간선은 단절선입니다. 비루트 u는 어떤 자식 v에서 low[v]≥tin[u]이면 단절점입니다. DFS 루트는 자식 수가 둘 이상인지 따로 봅니다.

직접 만든 삼각형 A-B-C-A에 C-D를 붙이면 C-D만 단절선입니다. 삼각형 내부에서는 다른 방향으로 우회하지만 D에서는 되돌아갈 대체 경로가 없습니다. 단절선과 2-간선 연결의 관계는 실제 이중화 모형의 기초입니다.

평행 간선 두 개가 A와 B를 잇는다면 한 개를 지워도 연결됩니다. 부모 정점과 같은 이웃을 전부 건너뛰는 구현은 두 간선을 모두 무시해 오답을 낼 수 있습니다. 부모 간선 ID 하나만 건너뜁니다. SCC용 lowlink 갱신 규칙을 무방향 단절선 코드에 섞지 않습니다.

## 2-SAT의 변수와 함의 그래프

2-SAT는 각 절이 최대 두 리터럴의 OR인 논리식의 만족 가능성을 구합니다. 리터럴은 변수 x 또는 그 부정 ¬x입니다. 절 (a∨b)는 ¬a→b와 ¬b→a로 바꿉니다. 둘 다 거짓인 경우만 금지한다는 뜻입니다.

변수 x와 ¬x가 같은 SCC면 두 방향의 함의가 함께 있어 어떤 값을 골라도 모순이 생깁니다. 모든 변수에서 둘의 SCC가 다르면 SCC의 위상 순서를 이용해 모순 없는 값을 배정할 수 있습니다. SCC 번호의 크기만 외워 사용하지 말고 번호가 생성된 순서가 위상 순서인지 역순서인지 확인합니다.

직접 만든 (x∨y)∧(¬x∨y)∧(x∨¬y)는 x=y=true로 만족합니다. 가운데 두 절은 x와 y가 같아야 한다는 조건이고, 첫 절은 둘 다 거짓인 경우를 배제합니다. 여기에 (¬x∨¬y)를 넣으면 둘 다 참인 경우도 배제되어 해가 없어집니다. 단항 절은 (x∨x)처럼 나타낼 수 있습니다.

일반 3-SAT를 똑같은 함의 간선으로 바꾸면 의미가 보존되지 않습니다. 임의의 논리 제약이 모두 2-SAT가 되는 것은 아닙니다. 배정의 양자택일 조건을 정확히 두 리터럴 절들로 표현할 수 있어야 합니다.

## 실전과 실제 쓰임

SCC는 순환 의존 영역을 하나의 단위로 묶는 분석에, 단절점과 단절선은 하나의 장애로 분리되는 지점을 찾는 모형에 연결됩니다. 2-SAT는 두 선택지 사이의 금지 조합을 만족시키는 배정에 사용합니다. 실제 네트워크의 신뢰성은 여러 동시 장애, 방향별 용량, 복구 시간에 따라 달라지므로 단절선 하나만으로 전체를 평가하지 않습니다.

C/C++/Python 모두 DFS 깊이가 길 수 있습니다. 반복형 Tarjan은 복귀 후 low 갱신 시점을 프레임으로 관리해야 합니다. 연결 요소 번호를 결과로 쓰는 프로그램에서는 재귀를 스택으로 바꾼 뒤 번호 순서에 의존한 코드도 함께 확인합니다.

## 복습과 추가 근거

복습: SCC를 압축했는데 사이클이 남았다면 무엇이 잘못되었는지 설명합니다. 답은 분해 또는 압축 간선 구성의 오류입니다. 순환하는 요소들이 실제로 서로 도달 가능하므로 하나의 SCC여야 합니다.

2-SAT의 선형 시간 판정의 원전은 Aspvall, Plass, Tarjan의 [A linear-time algorithm for testing the truth of certain quantified Boolean formulas](https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/2SAT.pdf)입니다. 이 문서의 작은 그래프와 논리식은 원문 예제가 아닌 자체 구성입니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

두 리터럴 절을 함의 그래프로 바꾸고 Kosaraju SCC로 만족 가능성을 판정합니다. 변수의 실제 값 배정, Tarjan, 단절점과 단절선은 이 예제의 구현 범위가 아닙니다.

이 예제에서 직접 구현하는 기법은 2-SAT 함의 그래프 · Kosaraju SCC · 재귀 종료 순서 · 변수와 부정의 모순 판정입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

변수 수 N과 절 수 M 뒤에 M개의 리터럴 쌍 a b가 주어집니다. 1≤N≤4, 0≤M≤8이며 리터럴은 ±1~±N입니다. a b는 (a OR b) 절입니다.

```text
2 3
1 2
-1 2
1 -2
```

만족 가능한 배정이 있으면 SAT, 없으면 UNSAT을 출력합니다.

```text
SAT
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 리터럴 정점: x=0, ¬x=1, y=2, ¬y=3 | 변수와 부정을 서로 다른 정점으로 만듭니다. |
| 2 | (x∨y): 1→2, 3→0 | 둘 다 거짓인 배정을 금지하는 두 함의를 추가합니다. |
| 3 | 첫 DFS 종료 순서=[2,0,3,1] | 자식 탐색이 끝난 뒤 정점을 기록합니다. |
| 4 | component=[1,0,1,0], 결과=SAT | 각 변수와 부정이 다른 SCC이므로 배정이 존재합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/24-강한연결요소단절점2SAT_scc-lowlink-2sat/example.c>)

```c
#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int vertices, adj[8][8], seen[8], order[8], order_size, component[8];  // 최대 8개 리터럴 정점의 SCC 상태
static int literal_node(int literal) {  // 부호 있는 리터럴을 정점 번호로 변환
    return 2 * (abs(literal) - 1) + (literal < 0);  // 양수는 짝수, 부정은 바로 다음 홀수
}  // 리터럴 변환 함수 끝
static void dfs_order(int u) {  // 원래 그래프의 종료 순서 기록
    seen[u] = 1;  // 재귀로 다시 방문하지 않게 표시
    for (int v = 0; v < vertices; ++v) if (adj[u][v] && !seen[v]) dfs_order(v);  // 미방문 후속 리터럴부터 처리
    order[order_size++] = u;  // 자식 탐색을 마친 뒤 종료 순서에 추가
}  // 종료 순서 DFS 끝
static void dfs_component(int u, int label) {  // 역그래프의 연결 탐색으로 SCC 배정
    component[u] = label;  // 현재 SCC 번호 기록
    for (int v = 0; v < vertices; ++v) if (adj[v][u] && component[v] == -1) dfs_component(v, label);  // 반대 간선으로 같은 SCC 확장
}  // 역그래프 DFS 끝
int main(void) {  // 2-SAT 만족 가능성 판정
    int variables = read_int(), clauses = read_int();  // 변수 수와 OR 절 수
    vertices = 2 * variables;  // 각 변수의 참·거짓 리터럴 정점
    for (int i = 0; i < clauses; ++i) {  // 두 리터럴 절 입력
        int a = literal_node(read_int()), b = literal_node(read_int());  // 두 리터럴의 정점 번호
        adj[a ^ 1][b] = 1; adj[b ^ 1][a] = 1;  // 부정 a에서 b, 부정 b에서 a로 함의 추가
    }  // 함의 그래프 구성 끝
    for (int u = 0; u < vertices; ++u) if (!seen[u]) dfs_order(u);  // 모든 정점의 DFS 종료 순서
    for (int u = 0; u < vertices; ++u) component[u] = -1;  // 아직 SCC가 없는 정점 표시
    int count = 0;  // 다음 SCC 번호
    for (int i = order_size - 1; i >= 0; --i) {  // 종료 순서 역순으로 두 번째 탐색
        int u = order[i];  // 이번 역그래프 출발 후보
        if (component[u] == -1) dfs_component(u, count++);  // 아직 소속이 없는 SCC를 하나 분리
    }  // SCC 분해 끝
    for (int x = 0; x < variables; ++x) {  // 각 변수와 그 부정의 소속 비교
        if (component[2 * x] == component[2 * x + 1]) { write_text("UNSAT\n"); return 0; }  // 같은 SCC면 양쪽 함의가 모순
    }  // 모든 변수의 모순 검사 끝
    write_text("SAT\n"); return 0;  // 모순 없는 배정의 존재 표시
}  // SCC 기반 2-SAT 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/24-강한연결요소단절점2SAT_scc-lowlink-2sat/example.cpp>)

```cpp
#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int vertices, adj[8][8], seen[8], order[8], order_size, component[8];  // 최대 8개 리터럴 정점의 SCC 상태
static int literal_node(int literal) {  // 부호 있는 리터럴을 정점 번호로 변환
    return 2 * (abs(literal) - 1) + (literal < 0);  // 양수는 짝수, 부정은 바로 다음 홀수
}  // 리터럴 변환 함수 끝
static void dfs_order(int u) {  // 원래 그래프의 종료 순서 기록
    seen[u] = 1;  // 재귀로 다시 방문하지 않게 표시
    for (int v = 0; v < vertices; ++v) if (adj[u][v] && !seen[v]) dfs_order(v);  // 미방문 후속 리터럴부터 처리
    order[order_size++] = u;  // 자식 탐색을 마친 뒤 종료 순서에 추가
}  // 종료 순서 DFS 끝
static void dfs_component(int u, int label) {  // 역그래프의 연결 탐색으로 SCC 배정
    component[u] = label;  // 현재 SCC 번호 기록
    for (int v = 0; v < vertices; ++v) if (adj[v][u] && component[v] == -1) dfs_component(v, label);  // 반대 간선으로 같은 SCC 확장
}  // 역그래프 DFS 끝
int main(void) {  // 2-SAT 만족 가능성 판정
    int variables = read_int(), clauses = read_int();  // 변수 수와 OR 절 수
    vertices = 2 * variables;  // 각 변수의 참·거짓 리터럴 정점
    for (int i = 0; i < clauses; ++i) {  // 두 리터럴 절 입력
        int a = literal_node(read_int()), b = literal_node(read_int());  // 두 리터럴의 정점 번호
        adj[a ^ 1][b] = 1; adj[b ^ 1][a] = 1;  // 부정 a에서 b, 부정 b에서 a로 함의 추가
    }  // 함의 그래프 구성 끝
    for (int u = 0; u < vertices; ++u) if (!seen[u]) dfs_order(u);  // 모든 정점의 DFS 종료 순서
    for (int u = 0; u < vertices; ++u) component[u] = -1;  // 아직 SCC가 없는 정점 표시
    int count = 0;  // 다음 SCC 번호
    for (int i = order_size - 1; i >= 0; --i) {  // 종료 순서 역순으로 두 번째 탐색
        int u = order[i];  // 이번 역그래프 출발 후보
        if (component[u] == -1) dfs_component(u, count++);  // 아직 소속이 없는 SCC를 하나 분리
    }  // SCC 분해 끝
    for (int x = 0; x < variables; ++x) {  // 각 변수와 그 부정의 소속 비교
        if (component[2 * x] == component[2 * x + 1]) { write_text("UNSAT\n"); return 0; }  // 같은 SCC면 양쪽 함의가 모순
    }  // 모든 변수의 모순 검사 끝
    write_text("SAT\n"); return 0;  // 모순 없는 배정의 존재 표시
}  // SCC 기반 2-SAT 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/24-강한연결요소단절점2SAT_scc-lowlink-2sat/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    variables, clauses = int(next(tokens)), int(next(tokens))  # 변수 수와 두 리터럴 절 수
    vertices = 2 * variables  # 참과 부정을 각각 정점으로 생성
    adj = [[0] * vertices for _ in range(vertices)]  # 함의 그래프의 인접 행렬
    def literal_node(literal):  # 부호 있는 정수를 리터럴 정점으로 변환
        return 2 * (abs(literal) - 1) + (literal < 0)  # 서로 부정인 리터럴 번호는 XOR 1 관계
    for _ in range(clauses):  # OR 절 입력
        a, b = literal_node(int(next(tokens))), literal_node(int(next(tokens)))  # 절을 이루는 두 정점
        adj[a ^ 1][b] = adj[b ^ 1][a] = 1  # 두 방향의 함의 추가
    seen = [False] * vertices  # 첫 DFS의 방문 여부
    order = []  # 첫 DFS의 종료 순서
    def dfs_order(u):  # 원래 그래프의 후위 순서 계산
        seen[u] = True  # 재귀 중복 방문 방지
        for v in range(vertices):  # 후속 함의 확인
            if adj[u][v] and not seen[v]:  # 미방문 이웃만 탐색
                dfs_order(v)  # 이웃 종료를 먼저 기록
        order.append(u)  # 모든 이웃 처리를 마친 정점
    for u in range(vertices):  # 고립 리터럴도 탐색에 포함
        if not seen[u]:  # 아직 시작하지 않은 DFS
            dfs_order(u)  # 종료 순서 확장
    component = [-1] * vertices  # 두 번째 DFS의 SCC 번호
    def dfs_component(u, label):  # 역그래프에서 SCC 한 개 분리
        component[u] = label  # 현재 소속 기록
        for v in range(vertices):  # u로 들어오던 간선을 역방향으로 사용
            if adj[v][u] and component[v] == -1:  # 아직 SCC가 없는 역방향 이웃
                dfs_component(v, label)  # 같은 SCC에 포함
    count = 0  # 다음 SCC 번호
    for u in reversed(order):  # 종료 순서가 늦은 정점부터 시작
        if component[u] == -1:  # 이전 SCC에 포함되지 않은 정점
            dfs_component(u, count)  # 새로운 SCC 탐색
            count += 1  # 다음 SCC 번호로 이동
    possible = all(component[2 * x] != component[2 * x + 1] for x in range(variables))  # 변수와 부정의 동시 함의 모순 검사
    print("SAT" if possible else "UNSAT")  # 만족 가능성만 출력

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

- 시간: O(N²+M)
- 보조 공간: O(N²)

리터럴은 2N개이며 두 DFS가 인접 행렬의 행을 순회합니다. 인접 리스트의 선형 SCC와 비용을 구별합니다.

[예제 입력](<예제_examples/24-강한연결요소단절점2SAT_scc-lowlink-2sat/input.txt>) · [예상 출력](<예제_examples/24-강한연결요소단절점2SAT_scc-lowlink-2sat/output.txt>) · [예제 실행 방법](<예제_examples/24-강한연결요소단절점2SAT_scc-lowlink-2sat/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 5 | 214294 빠른 이동 | [C](<../C/level5/009_214294_빠른_이동/README.md>) | [C++](<../C++/level5/009_214294_빠른_이동/README.md>) | [Python](<../Python/level5/revisit_20261024/008_214294_빠른_이동/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/scc.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

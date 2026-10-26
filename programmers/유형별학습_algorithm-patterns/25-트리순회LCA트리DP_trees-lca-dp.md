# 트리 순회와 LCA, 트리 DP와 경로 분해

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 사이클이 없다는 조건의 힘

트리는 연결된 무방향 비순환 그래프입니다. 두 정점 사이 단순 경로가 하나뿐이므로 부모를 정하면 서브트리들이 겹치지 않습니다. 이 구조 덕분에 자식의 답을 합쳐 부모의 답을 계산할 수 있습니다. 방향 그래프의 부모 배열처럼 보여도 원래 구조가 트리인지 먼저 확인합니다.

루트가 있는 트리의 전위 순회는 부모를 먼저, 후위 순회는 자식을 먼저 처리합니다. 깊이·거리 누적은 전위, 서브트리 크기·트리 DP는 후위가 자연스럽습니다. 재귀 없이 부모와 방문 순서를 만들고 그 순서를 뒤집어 후위 계산을 할 수도 있습니다.

## 직접 구성한 트리와 Euler 순서

간선을 0-1, 0-2, 1-3, 1-4로 둡니다. 루트 0에서 진입 순서를 0,1,3,4,2로 잡으면 정점 1의 서브트리는 연속 구간 [1,4)입니다. 진입할 때 번호를 부여하고 서브트리 탐색이 끝난 다음의 번호를 끝점으로 저장하면 됩니다.

서브트리 질의를 배열 구간 질의로 바꾸려는 것이 목적입니다. 정점을 매번 진입·퇴장할 때 모두 기록하는 Euler tour와, 각 정점에 진입 번호 하나만 붙이는 평탄화를 구별합니다. LCA를 RMQ로 푸는 Euler 기록은 다른 길이와 정보를 사용합니다.

## 최소 공통 조상 LCA

LCA(u,v)는 두 정점의 공통 조상 중 깊이가 가장 큰 정점입니다. 예제에서 LCA(3,4)=1, LCA(3,2)=0입니다. 부모를 한 칸씩 올리면 사슬 모양에서 질의당 O(V)가 됩니다.

이진 리프팅은 up[k][v]를 v의 2^k번째 조상으로 저장합니다. up[k+1][v]=up[k][up[k][v]]로 전처리합니다. 먼저 깊이를 맞추고 두 정점이 같아졌으면 그 정점을 반환합니다. 다르면 큰 k부터 두 조상이 다를 때만 함께 올립니다. 마지막으로 두 정점의 부모가 LCA입니다. 전처리 O(V log V), 질의 O(log V), 공간 O(V log V)입니다.

루트 거리 합을 D로 저장하면 가중 트리의 거리 합은 D[u]+D[v]-2D[LCA]입니다. 경로가 유일하므로 이 식의 합은 음수 간선에서도 경로 합으로 맞지만, 이를 최단 경로 문제 전체에 대한 허용 조건으로 확대하지 않습니다.

## 트리 DP의 상태와 증명

서로 인접한 정점을 동시에 고르지 않으면서 가중치 합을 최대로 한다고 둡니다. take[u]는 u를 고른 서브트리 최댓값, skip[u]는 고르지 않은 최댓값입니다.

~~~text
후위 순서로 각 정점 u를 처리  # 자식의 두 상태가 계산된 뒤 부모 계산
take[u] = weight[u]  # u를 고른 상태의 기본 보상
skip[u] = 0  # u를 고르지 않은 상태의 기본 보상
각 자식 v에 대해  # 서로 분리된 자식 서브트리를 하나씩 결합
    take[u] += skip[v]  # u를 골랐으므로 인접한 v는 고를 수 없음
    skip[u] += max(take[v], skip[v])  # u를 안 고르면 v의 선택 여부는 자유
정답은 max(take[root], skip[root])  # 루트의 두 경우를 비교
~~~

자식 서브트리들이 부모를 제외하면 연결되지 않고, u의 선택 여부만으로 자식과의 제약이 결정된다는 사실이 증명의 핵심입니다. 같은 상태 정의로 일반 그래프를 풀면 자식 사이의 간선이나 중복 정점을 놓칩니다.

## 루트 바꾸기와 트리 지름

모든 정점에서 다른 정점까지의 거리 합을 구하려고 매번 DFS를 하면 O(V²)입니다. 크기 sz[v]인 자식 v로 루트를 옮기면 그 서브트리의 거리는 1씩 줄고 나머지는 1씩 늘어 ans[v]=ans[u]+V-2sz[v]입니다. 가중치 w인 간선이면 변화량에 w를 곱합니다. 한 번의 후위, 한 번의 전위로 O(V)에 계산합니다.

비음수 가중 트리의 지름은 임의 정점에서 가장 먼 정점을 찾고, 거기서 다시 가장 먼 정점을 찾는 방식으로 구할 수 있습니다. 음수 간선과 빈 경로 허용 여부가 있으면 이 방법을 그대로 보장하지 않습니다. 경로 최대합 DP의 상태를 다시 정의합니다.

## 경로 질의의 확장

HLD(heavy-light decomposition)는 가장 큰 서브트리 자식으로 내려가는 간선을 무거운 간선으로 정합니다. 가벼운 간선을 내려갈 때 서브트리 크기가 적어도 절반으로 줄어 경로가 O(log V)개 연속 구간으로 나뉩니다. 세그먼트 트리와 결합하면 경로 합·최댓값 등을 보통 O(log² V)에 질의합니다. 방향에 민감한 연산은 구간의 역방향 결합도 관리합니다.

센트로이드 분해는 제거 후 어느 요소도 절반을 넘지 않는 정점을 기준으로 트리를 나눕니다. 원래 트리와 별도의 분해 트리 높이가 O(log V)입니다. 예를 들어 활성 정점까지의 최소 거리를 관리하면 각 센트로이드 조상에서 저장한 최소값과 현재 정점까지의 거리를 합쳐 후보를 비교합니다. 거리 전처리와 질의 비용은 어떤 LCA 구성을 쓰는지에 따라 추가됩니다.

두 방법 모두 단순 트리 순회보다 상태와 구현 부담이 큽니다. 서브트리만 묻는다면 Euler 평탄화로 충분한지 먼저 확인합니다. 정적 경로 합이면 LCA와 루트 누적합으로 해결할 수 있어 HLD가 필요하지 않습니다.

## 실제 쓰임과 언어별 주의

조직·파일 계층의 조상 질의, 트리 모양 통신망의 경로 합, 계층별 자원 배정의 축소 모형에 연결됩니다. 실제 파일 링크나 의존 관계가 여러 부모와 사이클을 만들면 트리 가정을 다시 확인합니다.

C와 C++은 정점·간선 수에 맞게 배열을 잡고 누적합은 넓은 정수로 저장합니다. Python은 깊은 재귀와 log V개 리스트의 정수 객체 비용을 고려합니다. 부모를 -1로 둔 뒤 배열[-1]을 조상처럼 읽지 않도록 루트의 조상 값을 일관되게 정의합니다.

## 복습과 근거

복습: 트리 DP에서 단순 방문 표시 대신 부모만 제외해도 되는 이유를 설명합니다. 답은 연결된 비순환 구조에서 부모 이외로 이미 방문한 정점에 돌아가는 간선이 없기 때문입니다. 평행 간선이 있는 임의 그래프에는 같은 설명을 적용할 수 없습니다.

LCA의 원전으로 [Harel과 Tarjan의 Fast algorithms for finding nearest common ancestors](https://doi.org/10.1137/0213024)를 연결합니다. 원전의 최적 알고리즘과 본문의 구현하기 쉬운 O(log V) 이진 리프팅을 동일한 방법으로 표시하지 않습니다. 트리 DP와 rerooting 연습은 [AtCoder Educational DP의 P와 V 문제](https://atcoder.jp/contests/dp/tasks)로 확장할 수 있습니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

0번을 루트로 삼아 DFS로 깊이·부모·서브트리 크기를 구하고 이진 리프팅으로 LCA를 답합니다. 같은 정점과 조상 관계 질의를 별도로 처리합니다.

이 예제에서 직접 구현하는 기법은 트리 DFS · 서브트리 크기 · 이진 리프팅 LCA · 조상·동일 정점 처리입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

N Q 뒤에 N-1개의 무방향 트리 간선과 Q개의 질의 u v가 주어집니다. 1≤N≤8, 0≤Q≤8이며 정점은 0부터입니다. 입력은 연결된 단순 트리입니다.

```text
5 4
0 1
0 2
1 3
1 4
3 4
3 2
1 3
2 2
```

첫 줄은 정점 번호순 서브트리 크기입니다. 이후 각 줄은 입력 질의의 LCA입니다.

```text
5 3 1 1 1
1
0
1
2
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | depth=[0,1,1,2,2], up[0]=[0,0,0,1,1] | 루트 0에서 부모와 깊이를 정합니다. |
| 2 | subtree=[5,3,1,1,1] | 자식 크기를 더하여 서브트리 크기를 완성합니다. |
| 3 | LCA(3,4): 두 정점의 부모=1 | 서로 다른 형제는 한 단계 위에서 만납니다. |
| 4 | LCA(1,3): 3을 1로 올린 직후 u=v=1 | 조상 관계이면 동일 정점 분기에서 바로 반환합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/25-트리순회LCA트리DP_trees-lca-dp/example.c>)

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


static int n, adj[8][8], depth[8], subtree[8], up[4][8];  // 작은 트리와 2의 거듭제곱 조상 표
static void prepare(int u, int parent) {  // 깊이·부모·서브트리 크기 계산
    up[0][u] = parent; subtree[u] = 1;  // 직계 부모와 자기 자신 한 개
    for (int v = 0; v < n; ++v) {  // 트리의 이웃 후보 확인
        if (!adj[u][v] || v == parent) continue;  // 없는 간선과 부모로 돌아가는 간선 제외
        depth[v] = depth[u] + 1;  // 자식 깊이는 한 단계 아래
        prepare(v, u);  // 자식 결과부터 계산
        subtree[u] += subtree[v];  // 완성한 자식 크기를 부모에 합산
    }  // 현재 서브트리 집계 끝
}  // 초기 DFS 끝
static int lca(int u, int v) {  // 두 정점의 최소 공통 조상
    if (depth[u] < depth[v]) { int swap = u; u = v; v = swap; }  // 더 깊은 정점을 u로 통일
    int difference = depth[u] - depth[v];  // 먼저 맞출 깊이 차이
    for (int k = 0; k < 4; ++k) if ((difference >> k) & 1) u = up[k][u];  // 차이의 비트만큼 조상 이동
    if (u == v) return u;  // 같은 정점이나 조상 관계면 여기서 바로 반환
    for (int k = 3; k >= 0; --k) {  // 큰 점프부터 LCA 바로 아래까지 함께 이동
        if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }  // 공통 조상보다 아래인 점프만 허용
    }  // 두 정점의 부모가 같아진 상태
    return up[0][u];  // 한 단계 위의 LCA
}  // LCA 질의 함수 끝
int main(void) {  // 서브트리와 조상 질의 실행
    n = read_int(); int queries = read_int();  // 정점 수와 질의 수
    for (int i = 1; i < n; ++i) {  // 트리 간선 n-1개 입력
        int a = read_int(), b = read_int();  // 간선 양끝
        adj[a][b] = adj[b][a] = 1;  // 무방향 연결
    }  // 트리 입력 끝
    prepare(0, 0);  // 루트의 부모를 자신으로 두어 범위 밖 조상 방지
    for (int k = 1; k < 4; ++k) {  // 2의 거듭제곱 조상 표 채우기
        for (int u = 0; u < n; ++u) up[k][u] = up[k - 1][up[k - 1][u]];  // 두 번의 절반 점프로 조상 계산
    }  // 이진 리프팅 표 완성
    for (int u = 0; u < n; ++u) {  // 서브트리 크기 출력
        if (u) write_text(" ");  // 숫자 사이 공백
        write_number(subtree[u]);  // 자기 자신을 포함한 정점 수
    }  // 크기 배열 출력 끝
    write_text("\n");  // 크기 배열의 줄바꿈
    for (int i = 0; i < queries; ++i) {  // 입력 순서대로 LCA 질의
        int u = read_int(), v = read_int();  // 이번 두 정점
        write_number(lca(u, v)); write_text("\n");  // LCA 하나를 한 줄에 출력
    }  // 모든 질의 출력 끝
    return 0;  // 정상 종료
}  // 트리 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/25-트리순회LCA트리DP_trees-lca-dp/example.cpp>)

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


static int n, adj[8][8], depth[8], subtree[8], up[4][8];  // 작은 트리와 2의 거듭제곱 조상 표
static void prepare(int u, int parent) {  // 깊이·부모·서브트리 크기 계산
    up[0][u] = parent; subtree[u] = 1;  // 직계 부모와 자기 자신 한 개
    for (int v = 0; v < n; ++v) {  // 트리의 이웃 후보 확인
        if (!adj[u][v] || v == parent) continue;  // 없는 간선과 부모로 돌아가는 간선 제외
        depth[v] = depth[u] + 1;  // 자식 깊이는 한 단계 아래
        prepare(v, u);  // 자식 결과부터 계산
        subtree[u] += subtree[v];  // 완성한 자식 크기를 부모에 합산
    }  // 현재 서브트리 집계 끝
}  // 초기 DFS 끝
static int lca(int u, int v) {  // 두 정점의 최소 공통 조상
    if (depth[u] < depth[v]) { int swap = u; u = v; v = swap; }  // 더 깊은 정점을 u로 통일
    int difference = depth[u] - depth[v];  // 먼저 맞출 깊이 차이
    for (int k = 0; k < 4; ++k) if ((difference >> k) & 1) u = up[k][u];  // 차이의 비트만큼 조상 이동
    if (u == v) return u;  // 같은 정점이나 조상 관계면 여기서 바로 반환
    for (int k = 3; k >= 0; --k) {  // 큰 점프부터 LCA 바로 아래까지 함께 이동
        if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }  // 공통 조상보다 아래인 점프만 허용
    }  // 두 정점의 부모가 같아진 상태
    return up[0][u];  // 한 단계 위의 LCA
}  // LCA 질의 함수 끝
int main(void) {  // 서브트리와 조상 질의 실행
    n = read_int(); int queries = read_int();  // 정점 수와 질의 수
    for (int i = 1; i < n; ++i) {  // 트리 간선 n-1개 입력
        int a = read_int(), b = read_int();  // 간선 양끝
        adj[a][b] = adj[b][a] = 1;  // 무방향 연결
    }  // 트리 입력 끝
    prepare(0, 0);  // 루트의 부모를 자신으로 두어 범위 밖 조상 방지
    for (int k = 1; k < 4; ++k) {  // 2의 거듭제곱 조상 표 채우기
        for (int u = 0; u < n; ++u) up[k][u] = up[k - 1][up[k - 1][u]];  // 두 번의 절반 점프로 조상 계산
    }  // 이진 리프팅 표 완성
    for (int u = 0; u < n; ++u) {  // 서브트리 크기 출력
        if (u) write_text(" ");  // 숫자 사이 공백
        write_number(subtree[u]);  // 자기 자신을 포함한 정점 수
    }  // 크기 배열 출력 끝
    write_text("\n");  // 크기 배열의 줄바꿈
    for (int i = 0; i < queries; ++i) {  // 입력 순서대로 LCA 질의
        int u = read_int(), v = read_int();  // 이번 두 정점
        write_number(lca(u, v)); write_text("\n");  // LCA 하나를 한 줄에 출력
    }  // 모든 질의 출력 끝
    return 0;  // 정상 종료
}  // 트리 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/25-트리순회LCA트리DP_trees-lca-dp/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, queries = int(next(tokens)), int(next(tokens))  # 트리 크기와 질의 수
    adj = [[0] * n for _ in range(n)]  # 작은 트리의 인접 행렬
    for _ in range(n - 1):  # 트리 간선 입력
        a, b = int(next(tokens)), int(next(tokens))  # 간선 양끝
        adj[a][b] = adj[b][a] = 1  # 양방향 연결
    depth = [0] * n  # 루트 기준 깊이
    subtree = [0] * n  # 자기 자신을 포함한 크기
    up = [[0] * n for _ in range(4)]  # 최대 8정점에 충분한 조상 표
    def prepare(u, parent):  # 부모·깊이와 후위 크기 계산
        up[0][u] = parent  # 직계 부모 저장
        subtree[u] = 1  # 자기 자신부터 집계
        for v in range(n):  # 이웃 후보 확인
            if not adj[u][v] or v == parent:  # 없는 간선과 부모 제외
                continue  # 자식만 아래로 탐색
            depth[v] = depth[u] + 1  # 자식 깊이 갱신
            prepare(v, u)  # 자식 결과 계산
            subtree[u] += subtree[v]  # 완성한 크기를 부모에 더하기
    prepare(0, 0)  # 루트의 조상을 자신으로 통일
    for k in range(1, 4):  # 두 번의 절반 점프로 표 확장
        for u in range(n):  # 모든 정점의 같은 크기 점프 계산
            up[k][u] = up[k - 1][up[k - 1][u]]  # 2의 k제곱 번째 조상
    def lca(u, v):  # 깊이 정렬 후 최소 공통 조상 찾기
        if depth[u] < depth[v]:  # 깊은 쪽을 앞에 두기
            u, v = v, u  # 두 정점 교환
        difference = depth[u] - depth[v]  # 먼저 줄일 깊이 차이
        for k in range(4):  # 차이의 켜진 비트만큼 이동
            if (difference >> k) & 1:  # 해당 크기의 점프가 필요하면
                u = up[k][u]  # 조상으로 이동
        if u == v:  # 조상 관계와 같은 정점 질의
            return u  # 부모로 더 올라가지 않기
        for k in range(3, -1, -1):  # 큰 점프부터 함께 이동
            if up[k][u] != up[k][v]:  # 아직 공통 조상 아래인 점프
                u, v = up[k][u], up[k][v]  # 두 정점을 같은 높이로 올리기
        return up[0][u]  # 바로 위의 공통 부모
    print(*subtree)  # 번호순 서브트리 크기
    for _ in range(queries):  # 입력 순서대로 질의
        u, v = int(next(tokens)), int(next(tokens))  # 두 질의 정점
        print(lca(u, v))  # 질의 결과 한 줄

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

- 시간: O(V²+V log V+Q log V)
- 보조 공간: O(V²+V log V)

예제의 초기 DFS는 인접 행렬을 확인합니다. 조상 표 전처리는 O(V log V), 각 질의는 O(log V)입니다.

[예제 입력](<예제_examples/25-트리순회LCA트리DP_trees-lca-dp/input.txt>) · [예상 출력](<예제_examples/25-트리순회LCA트리DP_trees-lca-dp/output.txt>) · [예제 실행 방법](<예제_examples/25-트리순회LCA트리DP_trees-lca-dp/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 2 | 468372 리프 노드 수 최대화 | [C](<../C/level2/004_468372_리프_노드_수_최대화/README.md>) | [C++](<../C++/level2/004_468372_리프_노드_수_최대화/README.md>) | [Python](<../Python/level2/004_468372_리프_노드_수_최대화/README.md>) |
| 3 | 388354 홀짝트리 | [C](<../C/level3/009_388354_홀짝트리/README.md>) | [C++](<../C++/level3/009_388354_홀짝트리/README.md>) | [Python](<../Python/level3/009_388354_홀짝트리/README.md>) |
| 4 | 150364 1,2,3 떨어트리기 | [C](<../C/level4/extra_150364_1,2,3_떨어트리기/README.md>) | [C++](<../C++/level4/extra_150364_1,2,3_떨어트리기/README.md>) | [Python](<../Python/level4/extra_150364_1,2,3_떨어트리기/README.md>) |
| 5 | 214291 집합과 쿼리 | [C](<../C/level5/008_214291_집합과_쿼리/README.md>) | [C++](<../C++/level5/008_214291_집합과_쿼리/README.md>) | [Python](<../Python/level5/revisit_20261024/007_214291_집합과_쿼리/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/tree.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

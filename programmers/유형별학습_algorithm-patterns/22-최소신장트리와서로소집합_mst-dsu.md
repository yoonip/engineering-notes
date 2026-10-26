# 최소 신장 트리와 서로소 집합

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 연결 전체의 비용과 한 경로의 비용

최소 신장 트리(MST)는 무방향 가중 그래프에서 모든 정점을 연결하는 간선 비용 합을 최소화합니다. 정점 V개를 연결한 트리의 간선은 V-1개입니다. 서로 연결되지 않은 그래프에는 전체 신장 트리가 없으며 연결 요소마다 최소 신장 숲을 구합니다.

최단 경로 트리는 출발점에서 각 정점까지의 거리를 최소화합니다. MST는 전체 설치 비용이 목적이므로 같은 트리가 아닐 수 있습니다. 음수 간선도 사용할 수 있으며, 음수 사이클 때문에 최단 경로가 무너지는 상황과 구별합니다.

## 서로소 집합의 역할

DSU는 원소가 어느 연결 집합에 속하는지 find로 확인하고 두 집합을 union으로 합칩니다. 경로 압축은 부모를 대표에 가깝게 바꿉니다. 크기 또는 rank가 작은 트리를 큰 트리에 붙이면 한쪽으로 길어지는 현상을 줄입니다.

두 최적화를 함께 사용하면 m번 연산의 총비용은 초기화 O(V)를 제외하고 상각 O(m α(V))입니다. α는 역 Ackermann 함수이며 실용적인 입력에서 매우 느리게 증가하지만, 모든 개별 find가 최악 O(1)이라는 뜻은 아닙니다. [Princeton UF API](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/UF.html)는 rank와 경로 절반 압축을 결합한 비용을 명시합니다. [크기 기준 합치기만 사용한 API](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/WeightedQuickUnionUF.html)와 구별합니다.

DSU 자체에는 두 정점 사이 경로, 최단 거리, 임의 삭제를 복구할 정보가 없습니다. 삭제 질의가 필요하면 역순 처리나 rollback 같은 별도 구성을 검토합니다.

## Kruskal의 절차와 직접 구성한 예제

간선 AB=1, BC=2, AC=3, CD=4, BD=5를 둡니다.

1. 간선을 비용 순으로 정렬합니다.
2. AB를 선택해 {A,B}를 만듭니다.
3. BC를 선택해 {A,B,C}를 만듭니다.
4. AC는 같은 집합을 다시 이으므로 버립니다.
5. CD를 선택해 모든 정점을 연결하고 비용 7을 얻습니다.

~~~text
각 정점을 별도 집합으로 초기화  # 대표 배열과 집합 크기를 준비
간선을 비용 오름차순으로 정렬  # 가장 싼 안전한 연결부터 검사
각 간선 (u, v, w)을 순회  # 연결 후보를 한 번씩 확인
    find(u)와 find(v)가 다르면  # 선택된 간선들 사이에 사이클을 만들지 않는 조건
        두 집합을 합침  # 이후 같은 연결 요소로 판정
        비용 합에 w를 더함  # 선택한 간선의 비용 기록
선택 간선이 V-1개인지 확인  # 전체 연결 여부를 결과와 함께 판정
~~~

## 왜 싼 간선을 골라도 되는지

현재 선택한 숲의 한 연결 요소와 나머지를 가르는 절단을 생각합니다. 그 절단을 건너는 최소 비용 간선 e는 현재 숲을 포함하는 어떤 MST에 안전하게 넣을 수 있습니다. 그 MST에 e가 없으면 e를 넣어 생긴 사이클에서 같은 절단을 건너는 f를 빼면 됩니다. w(e)≤w(f)이므로 비용이 늘지 않습니다.

동일 비용 간선이 여러 개면 MST가 유일하지 않을 수 있습니다. 특정 최소 간선이 모든 MST에 반드시 들어간다고 쓰지 않습니다. [Princeton MST의 cut property](https://algs4.cs.princeton.edu/43mst/index.php)에서 안전한 선택의 근거를 확인할 수 있습니다.

## Prim과 변형

Prim은 하나의 연결된 트리를 키우며 트리와 바깥을 잇는 최소 간선을 선택합니다. 간선 중심 Kruskal과 정점 집합 중심 Prim은 같은 절단 성질을 사용합니다. 희소 그래프에는 힙 Prim O(E log V) 또는 Kruskal O(E log E)를, 조밀한 인접 행렬에는 O(V²) Prim을 검토합니다. 그래프 저장 공간 O(V+E) 또는 O(V²)도 함께 셉니다.

추가 간선을 넣어 차선 신장 트리를 찾는 문제는 MST 경로에서 제거할 최대 간선을 질의하는 문제로 이어집니다. 같은 비용의 다른 MST와 엄격하게 더 비싼 차선 해를 구별합니다. 방향 그래프의 최소 연결은 일반 MST가 아닌 방향 신장 트리 문제이며 Kruskal을 그대로 적용할 수 없습니다.

## 실제 쓰임과 한계

링크 설치 비용만 합산하는 통신망·배관 후보를 연결하는 모형에 사용합니다. 실제 설계가 장애 하나에도 연결을 유지해야 한다면 트리는 취약하며 이중화 제약이 추가됩니다. 용량·지리 장애물·허브 비용이 있으면 그 비용을 간선에 정확히 모델링할 수 있는지부터 확인합니다.

C는 대표·크기를 배열로 관리합니다. C++도 간단한 DSU를 직접 구현할 수 있으며 정렬 비교에서 뺄셈으로 int 오버플로를 만들지 않습니다. Python은 정수 객체와 간선 튜플의 메모리를 확인하고 재귀 find가 깊어지지 않도록 합치기 규칙을 적용합니다.

## 반례와 복습

정점 A,B,C에서 AB=2, AC=2, BC=1이면 A 기준 최단 경로 트리는 AB와 AC로 비용 4입니다. MST는 BC와 AB 또는 AC로 비용 3입니다. 전체 비용과 출발점 거리를 혼동하면 목적 함수가 바뀝니다.

복습: 이미 같은 DSU 집합인 두 정점의 간선을 추가하면 왜 제외하는지 설명합니다. 답은 기존 경로와 새 간선이 사이클을 이루고, 연결에 불필요한 간선을 추가하기 때문입니다. 그 간선이 음수인 경우에도 신장 트리라는 조건은 사이클을 허용하지 않습니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

비용순 간선을 보면서 DSU 대표가 다른 두 요소만 합칩니다. 전체를 연결할 수 없는 경우도 따로 출력합니다.

이 예제에서 직접 구현하는 기법은 Kruskal · 경로 압축 DSU · 크기 기준 병합 · 연결 불가 판정입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

V E 뒤에 E개의 u v w가 주어집니다. 1≤V≤8, 0≤E≤32, 0≤u,v<V, -100≤w≤100입니다. 무방향 간선이며 평행 간선을 허용합니다.

```text
4 5
0 1 1
1 2 2
0 2 3
2 3 4
1 3 5
```

최소 신장 트리 비용을 출력합니다. 연결되지 않으면 DISCONNECTED를 출력합니다.

```text
7
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | parent=[0,1,2,3], selected=0 | 각 정점에서 독립 집합으로 시작합니다. |
| 2 | 간선(0,1,1): total=1, selected=1 | 다른 두 집합을 가장 싼 간선으로 합칩니다. |
| 3 | 간선(1,2,2) 선택 뒤 (0,2,3) 제외 | 0과 2가 같은 집합이므로 새 사이클을 만들지 않습니다. |
| 4 | 간선(2,3,4): selected=3, total=7 | V-1개 간선을 선택하여 전체 연결을 확인합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/22-최소신장트리와서로소집합_mst-dsu/example.c>)

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


typedef struct { int u, v, weight; } Edge;  // 양끝과 비용을 묶은 간선 자료형
static int parent[8], sizes[8];  // DSU 대표 연결과 집합 크기
static int find_root(int node) {  // 경로를 줄이며 현재 대표 찾기
    while (parent[node] != node) {  // 자기 자신이 대표가 될 때까지 이동
        parent[node] = parent[parent[node]];  // 한 단계 위 조상으로 경로 압축
        node = parent[node];  // 짧아진 부모 방향으로 이동
    }  // 대표 탐색 끝
    return node;  // 집합을 식별하는 대표
}  // find 함수 끝
static int compare_edges(const void *first, const void *second) {  // qsort용 비용 비교
    const Edge *a = (const Edge *)first, *b = (const Edge *)second;  // 전달받은 원소를 간선으로 해석
    return (a->weight > b->weight) - (a->weight < b->weight);  // 뺄셈 오버플로 없이 비교 부호 반환
}  // 간선 비교 함수 끝
int main(void) {  // Kruskal 최소 신장 트리 계산
    int n = read_int(), m = read_int();  // 정점 수와 간선 수
    Edge edges[32];  // 입력 상한만큼 간선 보관
    for (int i = 0; i < m; ++i) {  // 간선 목록 입력
        edges[i].u = read_int(); edges[i].v = read_int(); edges[i].weight = read_int();  // 양끝과 비용 저장
    }  // 간선 입력 끝
    qsort(edges, m, sizeof(Edge), compare_edges);  // 작은 비용부터 간선 검사
    for (int i = 0; i < n; ++i) { parent[i] = i; sizes[i] = 1; }  // 정점마다 독립 집합 생성
    int selected = 0, total = 0;  // 선택 간선 수와 누적 비용
    for (int i = 0; i < m; ++i) {  // 정렬한 간선을 한 번씩 확인
        int a = find_root(edges[i].u), b = find_root(edges[i].v);  // 두 끝의 현재 소속
        if (a == b) continue;  // 사이클을 만드는 간선 제외
        if (sizes[a] < sizes[b]) { int swap = a; a = b; b = swap; }  // 작은 집합을 큰 집합에 붙이기
        parent[b] = a; sizes[a] += sizes[b];  // 두 연결 요소 병합
        total += edges[i].weight; ++selected;  // 선택한 간선 비용과 개수 반영
    }  // 간선 선택 끝
    if (selected == n - 1) { write_number(total); write_text("\n"); }  // 전체 연결이면 MST 비용
    else write_text("DISCONNECTED\n");  // 전체 신장 트리가 없는 상태
    return 0;  // 정상 종료
}  // Kruskal 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/22-최소신장트리와서로소집합_mst-dsu/example.cpp>)

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


typedef struct { int u, v, weight; } Edge;  // 양끝과 비용을 묶은 간선 자료형
static int parent[8], sizes[8];  // DSU 대표 연결과 집합 크기
static int find_root(int node) {  // 경로를 줄이며 현재 대표 찾기
    while (parent[node] != node) {  // 자기 자신이 대표가 될 때까지 이동
        parent[node] = parent[parent[node]];  // 한 단계 위 조상으로 경로 압축
        node = parent[node];  // 짧아진 부모 방향으로 이동
    }  // 대표 탐색 끝
    return node;  // 집합을 식별하는 대표
}  // find 함수 끝
static int compare_edges(const void *first, const void *second) {  // qsort용 비용 비교
    const Edge *a = (const Edge *)first, *b = (const Edge *)second;  // 전달받은 원소를 간선으로 해석
    return (a->weight > b->weight) - (a->weight < b->weight);  // 뺄셈 오버플로 없이 비교 부호 반환
}  // 간선 비교 함수 끝
int main(void) {  // Kruskal 최소 신장 트리 계산
    int n = read_int(), m = read_int();  // 정점 수와 간선 수
    Edge edges[32];  // 입력 상한만큼 간선 보관
    for (int i = 0; i < m; ++i) {  // 간선 목록 입력
        edges[i].u = read_int(); edges[i].v = read_int(); edges[i].weight = read_int();  // 양끝과 비용 저장
    }  // 간선 입력 끝
    qsort(edges, m, sizeof(Edge), compare_edges);  // 작은 비용부터 간선 검사
    for (int i = 0; i < n; ++i) { parent[i] = i; sizes[i] = 1; }  // 정점마다 독립 집합 생성
    int selected = 0, total = 0;  // 선택 간선 수와 누적 비용
    for (int i = 0; i < m; ++i) {  // 정렬한 간선을 한 번씩 확인
        int a = find_root(edges[i].u), b = find_root(edges[i].v);  // 두 끝의 현재 소속
        if (a == b) continue;  // 사이클을 만드는 간선 제외
        if (sizes[a] < sizes[b]) { int swap = a; a = b; b = swap; }  // 작은 집합을 큰 집합에 붙이기
        parent[b] = a; sizes[a] += sizes[b];  // 두 연결 요소 병합
        total += edges[i].weight; ++selected;  // 선택한 간선 비용과 개수 반영
    }  // 간선 선택 끝
    if (selected == n - 1) { write_number(total); write_text("\n"); }  // 전체 연결이면 MST 비용
    else write_text("DISCONNECTED\n");  // 전체 신장 트리가 없는 상태
    return 0;  // 정상 종료
}  // Kruskal 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/22-최소신장트리와서로소집합_mst-dsu/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m = int(next(tokens)), int(next(tokens))  # 정점 수와 간선 수
    edges = []  # 비용순으로 볼 간선 목록
    for _ in range(m):  # 무방향 간선 입력
        a, b, weight = int(next(tokens)), int(next(tokens)), int(next(tokens))  # 양끝과 비용
        edges.append((weight, a, b))  # 비용을 첫 정렬 키로 저장
    edges.sort()  # 작은 비용부터 검사
    parent = list(range(n))  # 초기 대표는 각 정점 자신
    sizes = [1] * n  # 초기 집합 크기
    def find_root(node):  # 현재 DSU 대표 찾기
        while parent[node] != node:  # 대표까지 부모를 따라 이동
            parent[node] = parent[parent[node]]  # 경로를 한 단계씩 줄이기
            node = parent[node]  # 짧아진 부모로 이동
        return node  # 현재 대표 반환
    selected = total = 0  # 선택 간선 수와 비용 합
    for weight, u, v in edges:  # 비용순 간선 확인
        a, b = find_root(u), find_root(v)  # 두 정점의 소속 조회
        if a == b:  # 이미 연결된 두 정점
            continue  # 사이클 간선 제외
        if sizes[a] < sizes[b]:  # 크기 기준 합치기 준비
            a, b = b, a  # 큰 집합을 앞에 두기
        parent[b] = a  # 작은 집합을 큰 대표에 연결
        sizes[a] += sizes[b]  # 새 집합 크기 갱신
        selected += 1  # 연결에 쓴 간선 수
        total += weight  # 해당 간선 비용 합산
    print(total if selected == n - 1 else "DISCONNECTED")  # 전체 연결 여부에 맞는 결과

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

- 시간: O(E log E + V + E α(V))
- 보조 공간: O(V+E)

간선을 정렬하고 경로 압축·크기 기준 DSU 연산을 수행합니다.

[예제 입력](<예제_examples/22-최소신장트리와서로소집합_mst-dsu/input.txt>) · [예상 출력](<예제_examples/22-최소신장트리와서로소집합_mst-dsu/output.txt>) · [예제 실행 방법](<예제_examples/22-최소신장트리와서로소집합_mst-dsu/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 3 | 468376 최고 속도 | [C](<../C/level3/004_468376_최고_속도/README.md>) | [C++](<../C++/level3/004_468376_최고_속도/README.md>) | [Python](<../Python/level3/004_468376_최고_속도/README.md>) |
| 4 | 64063 호텔 방 배정 | — | [C++](<../C++/level4/extra_64063_호텔_방_배정/README.md>) | [Python](<../Python/level4/extra_64063_호텔_방_배정/README.md>) |
| 5 | 389632 문자열과 알파벳과 쿼리 | [C](<../C/level5/010_389632_문자열과_알파벳과_쿼리/README.md>) | [C++](<../C++/level5/010_389632_문자열과_알파벳과_쿼리/README.md>) | [Python](<../Python/level5/revisit_20261024/009_389632_문자열과_알파벳과_쿼리/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/mst-dsu.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

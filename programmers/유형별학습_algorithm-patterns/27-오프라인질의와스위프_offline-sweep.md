# 오프라인 질의와 스위프의 처리 순서

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 핵심 원리와 중요성

오프라인 알고리즘은 모든 질의를 미리 알고 처리 순서를 바꾸는 방법입니다.
답은 원래 질의 번호에 저장하므로 출력 순서는 유지할 수 있습니다.
온라인에서 여러 차원을 함께 관리해야 할 문제도, 정렬한 한 차원을 처리 순서로 대체하면 단순해집니다.
앞선 답으로 다음 질의가 만들어지거나 즉시 응답해야 한다면 같은 재정렬을 적용할 수 없습니다.

## 좌표 압축

좌표 압축은 등장하는 값을 정렬하고 같은 값에 같은 순위 번호를 붙이는 방법입니다.
직접 구성한 값 [100,−5,100,7]은 [2,0,2,1]로 바뀝니다.
순서는 보존하지만 100과 7 사이의 실제 거리 93은 번호 차이 1로 바뀝니다.
개수·순위 질의에는 번호를, 길이·넓이 계산에는 원래 좌표의 차이를 사용합니다.
폐구간 [l,r]을 정수 반열린 구간으로 바꾼다면 r+1도 필요한 경계에 포함합니다.
최댓값의 r+1이 자료형 범위를 넘는지도 확인합니다.

## 스위프: 한 방향으로만 진행

스위프는 좌표나 시간을 순서대로 지나며 활성 상태를 갱신합니다.
점 (x,y) 중 x≤X, y≤Y인 개수는 x순으로 점을 추가하고 y의 접두 개수를 질의합니다.
이렇게 x 조건을 처리 순서로 해결하고 y 조건만 Fenwick 트리에 남깁니다. [CP Initiative 범위 스위프 강의](https://github.com/cpinitiative/usaco-guide/blob/master/content/5_Plat/Range_Sweep.mdx)

## 직접 구성한 점 개수 예제

점은 A=(1,4), B=(2,1), C=(2,3)입니다.
질의는 Q0=(2,2), Q1=(1,5), Q2=(2,4)입니다.
질의를 X순으로 바꾸어 Q1, Q0, Q2 순서로 처리합니다.

| 질의 | x 조건으로 추가한 점 | y 조건의 답 | 원래 답 위치 |
| --- | --- | ---: | --- |
| Q1=(1,5) | A | 1 | answer[1]=1 |
| Q0=(2,2) | A,B,C | 1 | answer[0]=1 |
| Q2=(2,4) | A,B,C | 3 | answer[2]=3 |

출력은 원래 순서 [1,1,3]입니다.
x≤X이므로 같은 x의 점을 질의보다 먼저 추가해야 합니다.
조건이 x<X라면 동률 이벤트의 순서가 달라집니다.
n개 점과 q개 질의에서 정렬·압축·Fenwick 처리는 O((n+q)log(n+q)) 시간, O(n+q) 공간입니다.
정렬 순서상 트리에 들어 있는 점이 정확히 x 조건을 만족한다는 불변식이 정당성의 핵심입니다.

## Mo 알고리즘: 양끝을 조금씩 이동

Mo 알고리즘은 정적 배열 구간 질의를 왼쪽 블록과 오른쪽 끝으로 정렬합니다.
현재 [L,R)의 답을 원소 하나의 추가·제거로 고칠 수 있어야 합니다.
합처럼 더 쉬운 구조가 있는 문제보다, 서로 다른 값의 수처럼 빈도 상태가 필요한 문제에서 유용합니다.
직접 구성한 [1,2,1,3]에서 [0,3)의 빈도는 {1:2,2:1}이며 종류 수는 2입니다.
[1,4)로 이동할 때 1 하나를 빼도 빈도 1이 남아 종류 수는 2입니다.
이후 3을 넣으면 빈도가 0에서 1이 되어 종류 수는 3입니다.
추가 때 빈도 0→1, 제거 때 1→0인 경우에만 종류 수를 바꿉니다.
블록 크기 B에서 양끝 이동 수의 상한은 O(n²/B+qB)이며 질의 정렬은 O(q log q)입니다.
한 번 이동 비용이 O(1), B≈√n이면 O((n+q)√n+q log q) 시간이고 저장 공간은 O(n+q)입니다.
값 변경이 있는 문제는 시간축까지 포함한 다른 변형이며 이 분석을 그대로 쓰지 않습니다. [Laaksonen 교재 27장](https://cses.fi/book/book.pdf)

## 영속 자료구조: 이전 버전을 함께 보관

영속 세그먼트 트리는 갱신 경로의 노드만 복사하고 나머지는 공유합니다.
이전 루트가 가리키는 노드를 바꾸지 않아 여러 버전을 동시에 조회합니다.
정적 배열의 앞 i개 값 빈도를 root[i]로 만들면 [l,r)의 값 빈도는 root[r]−root[l]입니다.
k번째 값은 두 루트의 왼쪽 자식 개수 차이를 비교하며 내려가 구합니다.
압축 값 종류 σ에서 버전 하나의 점 갱신·질의는 O(log σ) 시간, 새 노드는 O(log σ)개입니다.
n개 접두 버전은 빈 루트 공유 구현에서 O(n log σ) 공간입니다.
일반적인 min 요약은 두 루트 값을 빼서 구간 min으로 바꿀 수 없으므로 이 빈도 예제와 구별합니다. [CP Initiative 영속 자료구조 설명](https://usaco.guide/adv/persistent)

## 롤백: 최근 변경을 되돌리기

롤백은 과거 버전을 모두 남기는 대신 변경 전 값을 스택에 기록했다가 역순으로 복구합니다.
분기 하나를 처리하고 같은 출발 상태로 돌아오는 재귀 탐색과 잘 맞습니다.
간선이 활성인 시간 구간을 시간 세그먼트 트리에 넣고 DFS 중 합치면 동적 연결성 질의에 사용할 수 있습니다.
롤백 DSU에서는 보통 경로 압축을 피하고 크기 기준 합치기로 find 깊이를 O(log n)으로 제한합니다.
성공한 합치기는 부모·크기 변경을 상수 개 기록하여 O(1)에 되돌립니다.
일반 경로 압축의 변경까지 기록하지 않고 루트 부모만 복구하면 이전 상태가 복원되지 않습니다.
여러 버전의 임의 접근이 필요한 영속성과 현재 경로의 역순 복구가 필요한 롤백을 구분합니다. [MIT 롤백 방법 강의](https://courses.csail.mit.edu/6.851/spring07/scribe/lec07.pdf)

## CDQ 분할 정복: 왼쪽이 오른쪽에 주는 기여

3차원 조건 a≤A,b≤B,c≤C인 점 개수는 한 번의 1차원 트리 스위프만으로 바로 끝나지 않습니다.
첫 좌표순 이벤트를 반으로 나누고, 왼쪽의 추가가 오른쪽 질의에 주는 기여를 합칩니다.
이 합치기에서는 b순으로 훑으면서 c를 Fenwick 트리로 관리해 한 차원을 더 줄입니다.
같은 반쪽 안의 기여는 재귀가 담당하며, 좌우로 처음 갈라진 단계에서 각 추가·질의 쌍이 정확히 한 번 집계됩니다.
합치기 뒤 Fenwick 변경을 취소해야 다른 재귀 구간에 값이 섞이지 않습니다.
표준적인 정적 지배 개수 구현은 N개 이벤트에서 O(N log²N) 시간, 배열·트리 O(N) 공간입니다.
동률은 포함 부등식에 맞춰 묶거나 정렬하며, DP 의존성이 있으면 왼쪽 계산→기여 반영→오른쪽 계산의 순서도 지킵니다.
이 설명은 다차원 지배 개수의 분할 정복 원리를 확장한 구성입니다. [대학 분할 정복 강의의 지배 개수 문제](https://www.cs.toronto.edu/~edl/notes/uwaterloo/CS341.pdf)

## 실전 연결과 실수

분석용 로그를 시간순으로 재정렬하는 작업과 연결되지만, 실시간 응답 시스템에는 지연 허용 조건이 필요합니다.
C·C++에서는 복사 노드 저장소와 이벤트 용량을 계산하고, Python에서는 노드별 객체 수가 메모리에 미치는 영향을 확인합니다.
좌표 압축의 거리 손실, 이벤트 동률, 원래 질의 번호 유실이 공통 실수입니다.
[구간 자료구조](26-구간질의와지연전파_range-queries.md)와 [좌표 기하](33-계산기하와좌표변환_computational-geometry.md)를 함께 복습합니다.

## 복습 질문과 답

- 질문: 스위프와 Mo의 차이는 무엇입니까? 답: 스위프는 한 정렬 축을 대개 앞으로만 진행하고, Mo는 현재 구간의 양끝을 왕복하며 상태를 유지합니다.
- 질문: 압축 번호의 차이를 사각형 너비로 써도 됩니까? 답: 순위 차이는 실제 거리를 보존하지 않으므로 원래 경계 좌표를 사용합니다.
- 질문: 영속 트리와 롤백을 같은 방식으로 조회합니까? 답: 영속 트리는 여러 루트를 보존하고, 롤백은 현재 상태를 변경 스택으로 되돌립니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

질의를 x순으로 바꾸고 압축한 y의 Fenwick 접두 개수로 답을 계산합니다.

이 예제에서 직접 구현하는 기법은 좌표 압축 · x 스위프 · Fenwick 개수 · 질의 번호 복원입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

n,q(0≤n,q≤30), 다음 n쌍의 점 x,y와 다음 q쌍의 질의 X,Y입니다. 좌표는 -1000..1000이며 각 질의는 x≤X,y≤Y인 입력 점 수를 묻습니다. 중복 점은 별개로 셉니다.

```text
3 3
1 4
2 1
2 3
2 2
1 5
2 4
```

원래 질의 순서대로 각 개수를 한 줄에 출력합니다.

```text
1
1
3
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 점 (1,4),(2,1),(2,3), y압축 [1,3,4] | 실제 거리 대신 순위가 필요한 개수 상태를 만듭니다. |
| 2 | 질의 (1,5) 먼저 처리, 점 (1,4)만 추가, 답1 | x≤1인 점이 정확히 들어 있습니다. |
| 3 | x=2의 두 점을 모두 추가한 뒤 (2,2)의 답1 | 같은 x의 점은 포함 조건이므로 질의보다 먼저 반영합니다. |
| 4 | (2,4)의 답3, 원래 순서 [1,1,3] | 질의 번호로 저장하여 출력 순서를 되돌립니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/27-오프라인질의와스위프_offline-sweep/example.c>)

```c
#include <stdio.h>  // 점과 질의 입출력
#include <stdlib.h>  // 압축과 이벤트 정렬

typedef struct { int x, y, id; } Event;  // 점이나 질의의 좌표와 원래 번호
int coordinates[30], bit[31], unique_count;  // 압축 좌표와 활성 점의 Fenwick 개수
int compare_int(const void *a, const void *b) {  // 좌표 순서 비교
    int x = *(const int *)a, y = *(const int *)b;  // 비교할 정수
    return (x > y) - (x < y);  // 뺄셈 오버플로 없는 대소 비교
}  // 정수 비교 끝
int compare_event(const void *a, const void *b) {  // x순과 동률 번호순 비교
    const Event *x = (const Event *)a, *y = (const Event *)b;  // 두 이벤트
    if (x->x != y->x) return (x->x > y->x) - (x->x < y->x);  // 작은 x 우선
    return (x->id > y->id) - (x->id < y->id);  // 같은 x의 결정적 순서
}  // 이벤트 비교 끝
int upper(int value) {  // value 이하인 압축 좌표 개수
    int left = 0, right = unique_count;  // 첫 초과 위치를 찾는 구간
    while (left < right) {  // 이분 탐색 구간 축소
        int middle = (left + right) / 2;  // 비교할 좌표 번호
        if (coordinates[middle] <= value) left = middle + 1; else right = middle;  // 포함 조건에 맞는 경계
    }  // 첫 초과 위치 확정
    return left;  // Fenwick 접두 끝 위치
}  // 좌표 경계 탐색 끝
void add(int index) {  // 압축된 1기반 y에 점 하나 추가
    for (; index <= unique_count; index += index & -index) ++bit[index];  // 상위 블록 개수 증가
}  // 활성 점 추가 끝
int prefix(int end) {  // 압축 접두 개수 조회
    int result = 0;  // 조건을 만족하는 점 수
    for (; end > 0; end -= end & -end) result += bit[end];  // 서로소 접두 블록 합산
    return result;  // y 조건까지 만족하는 개수
}  // Fenwick 조회 끝
int main(void) {  // 오프라인 점 개수 처리
    int n, q, answer[30], cursor = 0;  // 입력 수와 점 추가 위치
    Event points[30], queries[30];  // 정렬할 점과 질의
    scanf("%d %d", &n, &q);  // 두 목록의 길이
    for (int i = 0; i < n; ++i) {  // 입력 점 저장
        scanf("%d %d", &points[i].x, &points[i].y);  // 점 좌표
        points[i].id = i; coordinates[i] = points[i].y;  // 동률 순서와 압축 후보
    }  // 점 입력 끝
    for (int i = 0; i < q; ++i) { scanf("%d %d", &queries[i].x, &queries[i].y); queries[i].id = i; }  // 원래 질의 번호 보관
    qsort(coordinates, n, sizeof(int), compare_int);  // y 좌표 정렬
    for (int i = 0; i < n; ++i) if (i == 0 || coordinates[i] != coordinates[i - 1]) coordinates[unique_count++] = coordinates[i];  // 중복 좌표 제거
    qsort(points, n, sizeof(Event), compare_event);  // 추가할 점을 x순으로 정렬
    qsort(queries, q, sizeof(Event), compare_event);  // 질의도 x순으로 재배치
    for (int i = 0; i < q; ++i) {  // 작은 X부터 질의
        while (cursor < n && points[cursor].x <= queries[i].x) {  // 현재 X에 포함되는 점만 추가
            add(upper(points[cursor].y)); ++cursor;  // 같은 y는 같은 빈도 위치 사용
        }  // x 조건 반영 끝
        answer[queries[i].id] = prefix(upper(queries[i].y));  // y 조건과 원래 번호 반영
    }  // 오프라인 처리 끝
    for (int i = 0; i < q; ++i) printf("%d\n", answer[i]);  // 원래 순서로 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/27-오프라인질의와스위프_offline-sweep/example.cpp>)

```cpp
#include <iostream>  // C++ 스트림 입출력
#include <algorithm>  // 좌표와 이벤트의 표준 정렬

typedef struct { int x, y, id; } Event;  // 점이나 질의의 좌표와 원래 번호
int coordinates[30], bit[31], unique_count;  // 압축 좌표와 활성 점의 Fenwick 개수
int compare_int(const void *a, const void *b) {  // 좌표 순서 비교
    int x = *(const int *)a, y = *(const int *)b;  // 비교할 정수
    return (x > y) - (x < y);  // 뺄셈 오버플로 없는 대소 비교
}  // 정수 비교 끝
int compare_event(const void *a, const void *b) {  // x순과 동률 번호순 비교
    const Event *x = (const Event *)a, *y = (const Event *)b;  // 두 이벤트
    if (x->x != y->x) return (x->x > y->x) - (x->x < y->x);  // 작은 x 우선
    return (x->id > y->id) - (x->id < y->id);  // 같은 x의 결정적 순서
}  // 이벤트 비교 끝
int upper(int value) {  // value 이하인 압축 좌표 개수
    int left = 0, right = unique_count;  // 첫 초과 위치를 찾는 구간
    while (left < right) {  // 이분 탐색 구간 축소
        int middle = (left + right) / 2;  // 비교할 좌표 번호
        if (coordinates[middle] <= value) left = middle + 1; else right = middle;  // 포함 조건에 맞는 경계
    }  // 첫 초과 위치 확정
    return left;  // Fenwick 접두 끝 위치
}  // 좌표 경계 탐색 끝
void add(int index) {  // 압축된 1기반 y에 점 하나 추가
    for (; index <= unique_count; index += index & -index) ++bit[index];  // 상위 블록 개수 증가
}  // 활성 점 추가 끝
int prefix(int end) {  // 압축 접두 개수 조회
    int result = 0;  // 조건을 만족하는 점 수
    for (; end > 0; end -= end & -end) result += bit[end];  // 서로소 접두 블록 합산
    return result;  // y 조건까지 만족하는 개수
}  // Fenwick 조회 끝
int main() {  // 오프라인 점 개수 처리
    int n, q, answer[30], cursor = 0;  // 입력 수와 점 추가 위치
    Event points[30], queries[30];  // 정렬할 점과 질의
    std::cin >> n >> q;  // 두 목록의 길이
    for (int i = 0; i < n; ++i) {  // 입력 점 저장
        std::cin >> points[i].x >> points[i].y;  // 점 좌표
        points[i].id = i; coordinates[i] = points[i].y;  // 동률 순서와 압축 후보
    }  // 점 입력 끝
    for (int i = 0; i < q; ++i) { std::cin >> queries[i].x >> queries[i].y; queries[i].id = i; }  // 원래 질의 번호 보관
    std::sort(coordinates, coordinates + n);  // y 좌표 정렬
    for (int i = 0; i < n; ++i) if (i == 0 || coordinates[i] != coordinates[i - 1]) coordinates[unique_count++] = coordinates[i];  // 중복 좌표 제거
    std::sort(points, points + n, [](const Event &a, const Event &b) { return compare_event(&a, &b) < 0; });  // 추가할 점을 x순으로 정렬
    std::sort(queries, queries + q, [](const Event &a, const Event &b) { return compare_event(&a, &b) < 0; });  // 질의도 x순으로 재배치
    for (int i = 0; i < q; ++i) {  // 작은 X부터 질의
        while (cursor < n && points[cursor].x <= queries[i].x) {  // 현재 X에 포함되는 점만 추가
            add(upper(points[cursor].y)); ++cursor;  // 같은 y는 같은 빈도 위치 사용
        }  // x 조건 반영 끝
        answer[queries[i].id] = prefix(upper(queries[i].y));  // y 조건과 원래 번호 반영
    }  // 오프라인 처리 끝
    for (int i = 0; i < q; ++i) std::cout << answer[i] << "\n";  // 원래 순서로 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/27-오프라인질의와스위프_offline-sweep/example.py>)

```python
import sys  # 정수 입력 읽기
from bisect import bisect_right  # value 이하 좌표 개수 탐색
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
n, q = next(tokens), next(tokens)  # 점과 질의 수
points = [(next(tokens), next(tokens), i) for i in range(n)]  # 점 좌표와 동률 번호
queries = [(next(tokens), next(tokens), i) for i in range(q)]  # 원래 질의 번호
coordinates = sorted({y for x, y, i in points})  # y의 순서만 압축
points.sort(key=lambda event: (event[0], event[2]))  # 작은 x의 점부터 추가
queries.sort(key=lambda event: (event[0], event[2]))  # 질의도 같은 x순
bit = [0] * (len(coordinates) + 1)  # 활성 점의 빈도 트리
answer = [0] * q  # 원래 번호별 결과
cursor = 0  # 아직 추가하지 않은 점
def add(index):  # 1기반 압축 좌표 추가
    while index < len(bit):  # 해당 점의 상위 블록
        bit[index] += 1  # 점 한 개 추가
        index += index & -index  # 다음 상위 블록
def prefix(end):  # y 접두 개수
    result = 0  # 집계 결과
    while end:  # 접두사를 서로소 블록으로 분리
        result += bit[end]  # 블록 개수 추가
        end -= end & -end  # 마지막 블록 제거
    return result  # 조건에 맞는 점 개수
for x, y, identity in queries:  # 정렬한 질의 처리
    while cursor < n and points[cursor][0] <= x:  # 같은 x도 포함
        add(bisect_right(coordinates, points[cursor][1]))  # 점의 압축 순위에 추가
        cursor += 1  # 다음 점으로 이동
    answer[identity] = prefix(bisect_right(coordinates, y))  # y 이하 빈도와 원래 번호
for value in answer:  # 원래 질의 순서
    print(value)  # 한 답씩 출력
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 점·질의·좌표 각30개와 Fenwick31개의 고정 배열을 사용합니다. | 같은 상한의 고정 배열을 사용하며 입력 범위를 지킵니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: O((n+q)log(n+q))
- 보조 공간: O(n+q)

x순 정렬로 한 조건을 만족한 점만 추가하고 y의 압축 접두 합을 질의합니다.

[예제 입력](<예제_examples/27-오프라인질의와스위프_offline-sweep/input.txt>) · [예상 출력](<예제_examples/27-오프라인질의와스위프_offline-sweep/output.txt>) · [예제 실행 방법](<예제_examples/27-오프라인질의와스위프_offline-sweep/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 2 | 155651 호텔 대실 | [C](<../C/level2/023_155651_호텔_대실/README.md>) | [C++](<../C++/level2/023_155651_호텔_대실/README.md>) | [Python](<../Python/level2/023_155651_호텔_대실/README.md>) |
| 3 | 138475 억억단을 외우자 | [C](<../C/level3/023_138475_억억단을_외우자/README.md>) | [C++](<../C++/level3/023_138475_억억단을_외우자/README.md>) | [Python](<../Python/level3/023_138475_억억단을_외우자/README.md>) |
| 5 | 214295 미로 주행 테스트 | [C](<../C/level5/019_214295_미로_주행_테스트/README.md>) | [C++](<../C++/level5/019_214295_미로_주행_테스트/README.md>) | [Python 미완료](<../Python/level5/revisit_20261024/attempts/214295/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/offline-sweep.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

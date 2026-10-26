# 구간 질의 자료구조와 지연 전파

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 핵심 원리와 선택 기준

구간 질의는 배열의 일부를 매번 훑는 대신 작은 구간의 요약을 합쳐 답하는 방법입니다.
먼저 배열이 바뀌는지, 질의가 합·최솟값·순서 통계 중 무엇인지 구분합니다.
요약을 합치는 연산의 성질에 따라 가능한 자료구조와 복잡도가 달라집니다.
여기서는 길이 n, 반열린 구간 [l,r), 요약 한 번의 결합 비용 O(1)을 가정합니다.

| 구조 | 적합한 연산과 조건 | 구축 | 갱신 / 질의 | 공간 |
| --- | --- | --- | --- | --- |
| 누적합 | 정적 구간 합, 역연산으로 두 접두사 차이 계산 | O(n) | 점 변경 뒤 재구축 O(n) / O(1) | O(n) |
| Fenwick 트리 | 점 덧셈과 구간 합 | 선형 구축 O(n) | O(log n) / O(log n) | O(n) |
| 세그먼트 트리 | 결합법칙과 항등원이 있는 구간 요약 | O(n) | 점 갱신 O(log n) / O(log n) | O(n) |
| 지연 세그먼트 트리 | 요약에 작용하고 합성 가능한 구간 갱신 | O(n) | 구간 갱신 O(log n) / O(log n) | O(n) |
| 희소 테이블 | 정적 min·max·gcd 등 멱등 연산 | O(n log n) | 재구축 / O(1) | O(n log n) |
| 제곱근 분할 | 블록 요약과 양끝 직접 처리 | O(n) | 합 기준 점 갱신 O(1) / O(√n) | O(n) |

희소 테이블의 O(1) 질의는 두 겹치는 구간을 결합해도 값이 같은 연산을 가정합니다.
합은 겹친 부분을 두 번 더하므로 같은 방법으로 O(1)에 구하지 않습니다.
이 표는 모든 변형의 보편적인 상한이 아니라 명시한 연산에 대한 구현 기준입니다.

## Fenwick 트리

1부터 시작하는 내부 인덱스 i는 마지막 1비트 lowbit(i)=i&-i 길이의 구간 합을 보관합니다.
접두합은 i에서 lowbit(i)를 빼며 서로 겹치지 않는 블록을 더합니다.
점 덧셈은 i에 lowbit(i)를 더하며 그 점을 포함하는 상위 블록을 바꿉니다.
구간 [l,r)의 합은 prefix(r)-prefix(l)입니다.
점 대입은 기존 값을 별도로 저장하고 차이를 더하는 방식으로 바꿀 수 있습니다.
최솟값은 일반적으로 두 접두 최솟값의 차이로 복원하지 못합니다. [ACL Fenwick 공식 문서](https://atcoder.github.io/ac-library/production/document_en/fenwicktree.html)

## 세그먼트 트리와 결합법칙

세그먼트 트리는 구간을 둘로 나누고 부모에 왼쪽·오른쪽 요약의 결합을 저장합니다.
합의 항등원은 0, 최솟값의 항등원은 +∞입니다.
문자열 이어 붙이기처럼 순서를 바꾸면 값이 달라도 결합법칙만 성립하면 사용할 수 있습니다.
질의에서 오른쪽 조각을 역순으로 결합하는 실수를 피해야 합니다.
평균만 저장하면 두 구간의 길이를 잃으므로, (합,길이)를 저장해 결합합니다. [ACL 세그먼트 트리의 대수 조건](https://atcoder.github.io/ac-library/production/document_en/segtree.html)

## 지연 전파의 원리

구간 전체에 같은 갱신을 적용할 때 자손까지 즉시 방문하면 빠른 처리가 어렵습니다.
현재 노드의 요약에는 즉시 반영하되, 자손에게 보낼 갱신을 태그로 남깁니다.
자식의 일부를 읽거나 바꾸기 전에 태그를 내려보내는 동작을 push라고 합니다.
구간 합에 d를 더하는 갱신은 sum←sum+d×length이므로 길이 정보가 필요합니다.
갱신 f가 결합을 보존하고, 갱신의 합성을 같은 종류의 태그로 표현할 수 있어야 합니다. [ACL 지연 트리 조건과 합성 순서](https://atcoder.github.io/ac-library/production/document_en/lazysegtree.html)

## 직접 구성한 지연 갱신 추적

배열 [2,1,3,4]의 루트 요약은 (합 10, 길이 4)입니다.
전체에 3을 더하면 루트는 합 22, 지연 태그 +3이 됩니다.
자식에 저장한 합 3과 7은 아직 갱신하지 않아도, 루트 합 22는 이미 현재 배열의 합입니다.
[1,3)의 합을 읽으려면 일부 자손을 방문해야 하므로 +3을 두 자식에 전달합니다.
왼쪽 합은 3+3×2=9, 오른쪽 합은 7+3×2=13으로 바뀝니다.
필요한 리프까지 태그를 전달하면 값은 [5,4,6,7]이며 질의 답은 4+6=10입니다.
자식의 변경 뒤에는 부모 합을 자식 합으로 다시 결합합니다.

## 덧셈·곱셈·대입의 합성

원소 갱신을 f(x)=ax+b로 표현하면 대입 c는 (a,b)=(0,c)입니다.
오래된 f 뒤에 새 g(x)=cx+d를 적용하면 g(f(x))=(ca)x+(cb+d)입니다.
태그 합성의 인수 순서를 반대로 쓰면 다른 연산을 수행합니다.
직접 구성한 x=2에서 +3 뒤 ×2는 10이고, ×2 뒤 +3은 7입니다.
노드 합에 대한 작용은 sum←a×sum+b×length입니다.
범위 chmin과 구간 합은 합·길이만으로 처리할 수 없습니다.
예를 들어 [0,10]과 [5,5]는 합이 같지만 chmin(6) 뒤 합은 6과 10으로 다릅니다.
이런 경우에는 더 풍부한 요약과 별도 상환 분석이 필요한 변형을 검토합니다.

## 제곱근 분할과 균형 탐색 트리

제곱근 분할은 길이 B의 블록으로 나눠 완전히 들어가는 블록은 요약을 읽습니다.
양끝 직접 처리 O(B), 가운데 블록 수 O(n/B)이므로 합 질의는 O(B+n/B)입니다.
B≈√n은 두 비용을 균형 있게 하며, 갱신 종류에 따라 블록 재계산 비용은 달라집니다.
구현이 단순하고 특이한 블록 요약을 만들기 쉽지만 큰 상수와 질의 조합을 확인합니다.

키의 삽입·삭제와 predecessor·successor가 필요하면 균형 이진 탐색 트리가 적합합니다.
구간 합이나 k번째 원소까지 원하면 각 서브트리에 합·개수를 추가한 트리가 필요합니다.
단순 std::map·std::set의 두 반복자 사이 원소 수를 세는 작업이 자동으로 O(log n)은 아닙니다.
배열 인덱스가 고정인지, 키 집합 자체가 바뀌는지에 따라 구간 트리와 구별합니다.

## 정확성·구현·활용

각 노드의 저장 요약에 미전달된 조상 태그를 순서대로 가상 적용하면 현재 구간의 올바른 요약이 된다는 불변식을 유지합니다.
루트에는 미전달된 조상 태그가 없으므로 저장한 합이 항상 현재 전체 합입니다.
자식으로 내려가기 전에 push하면 도달한 노드의 요약에도 필요한 조상 갱신이 반영됩니다.
부분 갱신 뒤 pull로 올바른 자식 요약을 결합하여 부모 요약을 복구합니다.
빈 구간, 마지막 인덱스, 덧셈 뒤 대입·대입 뒤 덧셈을 작은 배열과 비교합니다.
C·C++에서는 합과 길이 곱의 자료형을 넓히고, Python에서는 재귀 호출·객체 수의 비용을 확인합니다.
실시간 측정값의 구간 집계에 활용할 수 있지만, 동시 수정과 영속 저장은 별도 설계 문제입니다.
[오프라인 질의](27-오프라인질의와스위프_offline-sweep.md)로 순서를 바꾸면 더 단순한 구조로 바꿀 수 있는지도 검토합니다.

## 복습 질문과 답

- 질문: Fenwick 트리로 구간 최솟값도 접두사 두 개의 차이로 구합니까? 답: 최솟값에는 합의 뺄셈 같은 역연산이 없어 일반적으로 불가능합니다.
- 질문: lazy 태그가 남아 있으면 노드 합도 오래된 값입니까? 답: 자기 노드 합에는 반영된 상태이며, 아직 자식에 전달하지 않은 갱신을 태그로 보관합니다.
- 질문: 희소 테이블은 왜 min 질의에서 두 구간이 겹쳐도 됩니까? 답: min(x,x)=x라서 같은 원소를 다시 포함해도 결과가 같기 때문입니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

같은 배열에 구간 덧셈을 적용하고 Fenwick과 지연 세그먼트 트리의 합을 나란히 비교합니다.

이 예제에서 직접 구현하는 기법은 Fenwick 점 덧셈·접두합 · 지연 세그먼트 트리 구간 덧셈·합 · 같은 연산의 결과 비교입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

n,q(1≤n≤16,0≤q≤30), 초기 정수 n개(-1000..1000), q개 연산입니다. 0 l r d는 [l,r)에 d(-100..100)를 더하고 1 l r은 합을 질의합니다. 0≤l≤r≤n입니다.

```text
4 4
2 1 3 4
1 0 4
0 0 4 3
1 0 4
1 1 3
```

합 질의마다 Fenwick합 지연트리합을 한 줄에 출력합니다.

```text
10 10
22 22
10 10
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 초기 [2,1,3,4], 두 합 10 | 같은 값으로 두 자료구조를 구축합니다. |
| 2 | [0,4)에 +3, Fenwick은 네 점 갱신 | 기본 Fenwick의 점 덧셈을 반복한 비교 기준입니다. |
| 3 | 지연 트리 루트 sum=22,lazy=3 | 전체 구간은 자손 방문을 미루고 루트 요약에 반영합니다. |
| 4 | [1,3) 질의는 4+6=10 | 지연 태그를 필요한 자손으로 내린 결과도 Fenwick과 같습니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/26-구간질의와지연전파_range-queries/example.c>)

```c
#include <stdio.h>  // 표준 입력과 출력 함수

int n, values[16], bit[17], tree[64], lazy[64];  // 두 구조가 공유하는 작은 입력 상한
void bit_add(int index, int delta) {  // Fenwick 한 점 덧셈
    for (++index; index <= n; index += index & -index) bit[index] += delta;  // 해당 점의 상위 블록 갱신
}  // Fenwick 점 갱신 끝
int prefix(int end) {  // [0,end)의 Fenwick 합
    int result = 0;  // 분리한 접두 블록의 합
    for (; end > 0; end -= end & -end) result += bit[end];  // 마지막 블록부터 제거하며 누적
    return result;  // 접두 합 반환
}  // Fenwick 질의 끝
void build(int node, int left, int right) {  // 지연 트리 초기 구축
    if (right - left == 1) { tree[node] = values[left]; return; }  // 한 원소 구간의 합
    int middle = (left + right) / 2;  // 자식 구간의 경계
    build(node * 2, left, middle);  // 왼쪽 합 구축
    build(node * 2 + 1, middle, right);  // 오른쪽 합 구축
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 자식 합을 부모에 반영
}  // 초기 구축 끝
void apply(int node, int length, int delta) {  // 한 구간 전체의 덧셈 반영
    tree[node] += length * delta;  // 원소 수만큼 구간 합 증가
    lazy[node] += delta;  // 자손에 보낼 미전달 덧셈 누적
}  // 노드 전체 갱신 끝
void push(int node, int left, int right) {  // 내려가기 전 조상 태그 전달
    if (lazy[node] == 0 || right - left == 1) return;  // 전달할 값이나 자식이 없으면 종료
    int middle = (left + right) / 2;  // 두 자식 길이의 기준
    apply(node * 2, middle - left, lazy[node]);  // 왼쪽 자식의 합과 태그 갱신
    apply(node * 2 + 1, right - middle, lazy[node]);  // 오른쪽 자식의 합과 태그 갱신
    lazy[node] = 0;  // 부모의 전달 의무 해제
}  // 태그 전달 끝
void range_add(int node, int left, int right, int first, int last, int delta) {  // [first,last) 덧셈
    if (last <= left || right <= first) return;  // 겹치지 않는 구간 제외
    if (first <= left && right <= last) { apply(node, right - left, delta); return; }  // 완전히 포함된 구간 처리
    push(node, left, right);  // 일부 자손 갱신 전 기존 태그 전달
    int middle = (left + right) / 2;  // 자식 구간 경계
    range_add(node * 2, left, middle, first, last, delta);  // 왼쪽 교차 부분 갱신
    range_add(node * 2 + 1, middle, right, first, last, delta);  // 오른쪽 교차 부분 갱신
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 변경 뒤 부모 합 복구
}  // 구간 덧셈 끝
int range_sum(int node, int left, int right, int first, int last) {  // [first,last)의 지연 트리 합
    if (last <= left || right <= first) return 0;  // 빈 교차의 합
    if (first <= left && right <= last) return tree[node];  // 포함 구간의 요약 사용
    push(node, left, right);  // 읽을 자손에 조상 갱신 반영
    int middle = (left + right) / 2;  // 두 교차 구간의 경계
    return range_sum(node * 2, left, middle, first, last) + range_sum(node * 2 + 1, middle, right, first, last);  // 서로소 부분 합 결합
}  // 구간 합 끝
int main(void) {  // 두 구현의 결과 비교 시작
    int q;  // 연산 수
    scanf("%d %d", &n, &q);  // 입력 크기
    for (int i = 0; i < n; ++i) { scanf("%d", &values[i]); bit_add(i, values[i]); }  // 초기 값과 Fenwick 구축
    build(1, 0, n);  // 같은 값으로 세그먼트 트리 구축
    for (int i = 0; i < q; ++i) {  // 연산을 입력 순서대로 처리
        int kind, left, right;  // 연산 종류와 반열린 구간
        scanf("%d %d %d", &kind, &left, &right);  // 공통 연산 정보
        if (kind == 0) {  // 구간 덧셈 연산
            int delta;  // 더할 값
            scanf("%d", &delta);  // 덧셈 크기
            for (int p = left; p < right; ++p) bit_add(p, delta);  // 기본 Fenwick은 각 점 갱신
            if (left < right) range_add(1, 0, n, left, right, delta);  // 지연 트리는 구간으로 갱신
        } else {  // 같은 구간의 두 합 비교
            int first = prefix(right) - prefix(left);  // Fenwick 접두 합의 차이
            int second = range_sum(1, 0, n, left, right);  // 지연 트리의 구간 합
            printf("%d %d\n", first, second);  // 일치해야 하는 두 결과
        }  // 연산 분기 끝
    }  // 전체 연산 끝
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/26-구간질의와지연전파_range-queries/example.cpp>)

```cpp
#include <iostream>  // C++ 스트림 입력과 출력

int n, values[16], bit[17], tree[64], lazy[64];  // 두 구조가 공유하는 작은 입력 상한
void bit_add(int index, int delta) {  // Fenwick 한 점 덧셈
    for (++index; index <= n; index += index & -index) bit[index] += delta;  // 해당 점의 상위 블록 갱신
}  // Fenwick 점 갱신 끝
int prefix(int end) {  // [0,end)의 Fenwick 합
    int result = 0;  // 분리한 접두 블록의 합
    for (; end > 0; end -= end & -end) result += bit[end];  // 마지막 블록부터 제거하며 누적
    return result;  // 접두 합 반환
}  // Fenwick 질의 끝
void build(int node, int left, int right) {  // 지연 트리 초기 구축
    if (right - left == 1) { tree[node] = values[left]; return; }  // 한 원소 구간의 합
    int middle = (left + right) / 2;  // 자식 구간의 경계
    build(node * 2, left, middle);  // 왼쪽 합 구축
    build(node * 2 + 1, middle, right);  // 오른쪽 합 구축
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 자식 합을 부모에 반영
}  // 초기 구축 끝
void apply(int node, int length, int delta) {  // 한 구간 전체의 덧셈 반영
    tree[node] += length * delta;  // 원소 수만큼 구간 합 증가
    lazy[node] += delta;  // 자손에 보낼 미전달 덧셈 누적
}  // 노드 전체 갱신 끝
void push(int node, int left, int right) {  // 내려가기 전 조상 태그 전달
    if (lazy[node] == 0 || right - left == 1) return;  // 전달할 값이나 자식이 없으면 종료
    int middle = (left + right) / 2;  // 두 자식 길이의 기준
    apply(node * 2, middle - left, lazy[node]);  // 왼쪽 자식의 합과 태그 갱신
    apply(node * 2 + 1, right - middle, lazy[node]);  // 오른쪽 자식의 합과 태그 갱신
    lazy[node] = 0;  // 부모의 전달 의무 해제
}  // 태그 전달 끝
void range_add(int node, int left, int right, int first, int last, int delta) {  // [first,last) 덧셈
    if (last <= left || right <= first) return;  // 겹치지 않는 구간 제외
    if (first <= left && right <= last) { apply(node, right - left, delta); return; }  // 완전히 포함된 구간 처리
    push(node, left, right);  // 일부 자손 갱신 전 기존 태그 전달
    int middle = (left + right) / 2;  // 자식 구간 경계
    range_add(node * 2, left, middle, first, last, delta);  // 왼쪽 교차 부분 갱신
    range_add(node * 2 + 1, middle, right, first, last, delta);  // 오른쪽 교차 부분 갱신
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 변경 뒤 부모 합 복구
}  // 구간 덧셈 끝
int range_sum(int node, int left, int right, int first, int last) {  // [first,last)의 지연 트리 합
    if (last <= left || right <= first) return 0;  // 빈 교차의 합
    if (first <= left && right <= last) return tree[node];  // 포함 구간의 요약 사용
    push(node, left, right);  // 읽을 자손에 조상 갱신 반영
    int middle = (left + right) / 2;  // 두 교차 구간의 경계
    return range_sum(node * 2, left, middle, first, last) + range_sum(node * 2 + 1, middle, right, first, last);  // 서로소 부분 합 결합
}  // 구간 합 끝
int main() {  // 두 구현의 결과 비교 시작
    int q;  // 연산 수
    std::cin >> n >> q;  // 입력 크기
    for (int i = 0; i < n; ++i) { std::cin >> values[i]; bit_add(i, values[i]); }  // 초기 값과 Fenwick 구축
    build(1, 0, n);  // 같은 값으로 세그먼트 트리 구축
    for (int i = 0; i < q; ++i) {  // 연산을 입력 순서대로 처리
        int kind, left, right;  // 연산 종류와 반열린 구간
        std::cin >> kind >> left >> right;  // 공통 연산 정보
        if (kind == 0) {  // 구간 덧셈 연산
            int delta;  // 더할 값
            std::cin >> delta;  // 덧셈 크기
            for (int p = left; p < right; ++p) bit_add(p, delta);  // 기본 Fenwick은 각 점 갱신
            if (left < right) range_add(1, 0, n, left, right, delta);  // 지연 트리는 구간으로 갱신
        } else {  // 같은 구간의 두 합 비교
            int first = prefix(right) - prefix(left);  // Fenwick 접두 합의 차이
            int second = range_sum(1, 0, n, left, right);  // 지연 트리의 구간 합
            std::cout << first << " " << second << "\n";  // 일치해야 하는 두 결과
        }  // 연산 분기 끝
    }  // 전체 연산 끝
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/26-구간질의와지연전파_range-queries/example.py>)

```python
import sys  # 전체 연산을 공백 단위로 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 정수 토큰 순회
n, q = next(tokens), next(tokens)  # 원소 수와 연산 수
values = [next(tokens) for _ in range(n)]  # 두 자료구조의 같은 초기 값
bit = [0] * (n + 1)  # Fenwick의 1기반 블록 합
tree = [0] * (4 * n)  # 세그먼트 구간 합
lazy = [0] * (4 * n)  # 자손으로 전달할 덧셈
def bit_add(index, delta):  # Fenwick 한 점 덧셈
    index += 1  # 내부 1기반 번호로 변환
    while index <= n:  # 해당 점이 들어가는 상위 블록 순회
        bit[index] += delta  # 블록 합 갱신
        index += index & -index  # 다음 상위 블록
def prefix(end):  # [0,end)의 접두 합
    result = 0  # 누적 블록 합
    while end:  # 겹치지 않는 블록을 뒤에서부터 합산
        result += bit[end]  # 현재 블록 추가
        end -= end & -end  # 처리한 블록 제거
    return result  # Fenwick 접두 결과
def build(node, left, right):  # 초기 구간 합 구축
    if right - left == 1:  # 리프 원소 확인
        tree[node] = values[left]  # 원소의 합 저장
        return  # 리프 구축 종료
    middle = (left + right) // 2  # 자식 경계
    build(node * 2, left, middle)  # 왼쪽 구축
    build(node * 2 + 1, middle, right)  # 오른쪽 구축
    tree[node] = tree[node * 2] + tree[node * 2 + 1]  # 부모 합 결합
def apply(node, length, delta):  # 전체 구간 갱신
    tree[node] += length * delta  # 자기 합에는 즉시 반영
    lazy[node] += delta  # 자손 전달은 미루기
def push(node, left, right):  # 자손 방문 전 태그 전달
    if not lazy[node] or right - left == 1:  # 전달 값이나 자식이 없는 상태
        return  # 전달 생략
    middle = (left + right) // 2  # 두 자식의 길이 계산
    apply(node * 2, middle - left, lazy[node])  # 왼쪽 반영
    apply(node * 2 + 1, right - middle, lazy[node])  # 오른쪽 반영
    lazy[node] = 0  # 부모 태그 해제
def range_add(node, left, right, first, last, delta):  # 반열린 구간 덧셈
    if last <= left or right <= first:  # 교차가 없는 구간
        return  # 갱신 제외
    if first <= left and right <= last:  # 완전히 포함된 구간
        apply(node, right - left, delta)  # 요약과 태그만 갱신
        return  # 자손 방문 생략
    push(node, left, right)  # 기존 조상 갱신 전달
    middle = (left + right) // 2  # 분할 경계
    range_add(node * 2, left, middle, first, last, delta)  # 왼쪽 갱신
    range_add(node * 2 + 1, middle, right, first, last, delta)  # 오른쪽 갱신
    tree[node] = tree[node * 2] + tree[node * 2 + 1]  # 부모 합 복구
def range_sum(node, left, right, first, last):  # 반열린 구간 합
    if last <= left or right <= first:  # 교차가 없는 구간
        return 0  # 합의 항등원
    if first <= left and right <= last:  # 완전히 포함된 요약
        return tree[node]  # 현재 구간 합 사용
    push(node, left, right)  # 읽을 자손에 갱신 전달
    middle = (left + right) // 2  # 분할 경계
    return range_sum(node * 2, left, middle, first, last) + range_sum(node * 2 + 1, middle, right, first, last)  # 부분 합 결합
for i, value in enumerate(values):  # 초기 Fenwick 원소 반영
    bit_add(i, value)  # 한 점씩 블록 합에 추가
build(1, 0, n)  # 초기 지연 트리 구축
for _ in range(q):  # 입력 순서의 연산 실행
    kind, left, right = next(tokens), next(tokens), next(tokens)  # 연산과 구간
    if kind == 0:  # 구간 덧셈
        delta = next(tokens)  # 더할 값
        for position in range(left, right):  # 비교용 Fenwick의 각 점 처리
            bit_add(position, delta)  # 기본 점 덧셈 반복
        if left < right:  # 빈 구간은 갱신 생략
            range_add(1, 0, n, left, right, delta)  # 지연 태그 구간 갱신
    else:  # 합 질의
        print(prefix(right) - prefix(left), range_sum(1, 0, n, left, right))  # 같은 결과 비교
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 원소16개, Fenwick17개, 세그먼트 요약·태그 각64개의 고정 배열입니다. | 같은 상한의 고정 배열을 사용하며 입력 범위를 지킵니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: 구축 O(n log n); 덧셈 O((r-l)log n)+O(log n); 합 질의 O(log n)
- 보조 공간: O(n)

비교용 Fenwick은 구간 안의 점을 각각 갱신하며, 지연 트리는 구간 태그 한 개로 처리합니다.

[예제 입력](<예제_examples/26-구간질의와지연전파_range-queries/input.txt>) · [예상 출력](<예제_examples/26-구간질의와지연전파_range-queries/output.txt>) · [예제 실행 방법](<예제_examples/26-구간질의와지연전파_range-queries/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 5 | 389632 문자열과 알파벳과 쿼리 | [C](<../C/level5/010_389632_문자열과_알파벳과_쿼리/README.md>) | [C++](<../C++/level5/010_389632_문자열과_알파벳과_쿼리/README.md>) | [Python](<../Python/level5/revisit_20261024/009_389632_문자열과_알파벳과_쿼리/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/range-query.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

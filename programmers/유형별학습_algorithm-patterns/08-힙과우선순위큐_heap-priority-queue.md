# 힙과 우선순위 큐

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 다음에 필요한 원소만 정하는 구조

우선순위 큐는 원소를 추가하면서 가장 높은 우선순위의 원소를 조회하거나 제거하는 인터페이스입니다.
힙은 이 인터페이스를 구현하는 방법 중 하나입니다.
최소 힙에서는 부모 값이 자식 값보다 크지 않으며, 그 결과 루트가 전체 최솟값입니다.
전체 배열이 정렬되어 있어야 하는 것은 아닙니다. [Python heapq, Heap Invariant](https://docs.python.org/3/library/heapq.html)

이 구분이 중요한 이유는 정렬 전체의 비용을 지불하지 않고 다음 원소만 계속 고를 수 있기 때문입니다.
다음 사건의 시각, 가장 작은 후보 거리, 현재 보관한 상위 K개 중 최솟값처럼 경계 원소가 반복해서 필요할 때 사용합니다.

## 인식 단서와 적용 한계

“추가할 때마다 다음 최솟값”, “가장 급한 작업부터”, “큰 값 K개만 유지”가 대표 단서입니다.
모든 원소가 미리 주어지고 한 번 순서대로 읽기만 한다면 일괄 정렬도 비교해야 합니다.
어떤 값이 있는지 찾기, 임의 원소 삭제, 순위 조회를 일반 힙이 모두 빠르게 지원하는 것은 아닙니다.
최솟값과 최댓값을 둘 다 자주 삭제해야 한다면 별도 구조와 동기화 방법이 필요할 수 있습니다.

원소의 우선순위를 힙 밖에서 바꾼다고 힙의 위치가 자동으로 갱신되는 것은 아닙니다.
갱신 연산을 설계하거나 새 항목을 넣고 오래된 항목을 꺼낼 때 거르는 방법을 사용합니다.

## 직접 구성한 예제: 가장 큰 값 세 개

입력이 `5,1,8,3,9`이고 지금까지 본 값 중 가장 큰 세 개만 유지한다고 가정합니다.
보관한 값의 최솟값을 바로 알기 위해 크기 3의 최소 힙을 사용합니다.
아래 표는 힙의 실제 내부 배열이 아니라 보관한 값들을 읽기 좋게 정렬해 표시한 것입니다.

| 새 값 | 처리 전 보관 값 | 판정 | 처리 후 보관 값 |
|---:|---|---|---|
| 5 | 빈 집합 | 아직 세 개 미만 | 5 |
| 1 | 5 | 아직 세 개 미만 | 1,5 |
| 8 | 1,5 | 아직 세 개 미만 | 1,5,8 |
| 3 | 1,5,8 | 3이 경계값 1보다 큼 | 3,5,8 |
| 9 | 3,5,8 | 9가 경계값 3보다 큼 | 5,8,9 |

새 값이 경계값 이하이면 이미 보관한 K개보다 유리할 수 없으므로 버립니다.
동점에서 어떤 항목을 남길지 중요하다면 값뿐 아니라 식별자와 동점 기준도 키에 포함합니다.

```python
from heapq import heappush, heapreplace  # 최소 힙 삽입과 루트 교체 연산 가져오기
heap, k = [], 3  # 보관할 최소 힙과 최대 보관 개수 초기화
for value in [5, 1, 8, 3, 9]:  # 입력을 한 번씩 순서대로 읽기
    if len(heap) < k:  # 아직 K개를 채우지 못했는지 검사
        heappush(heap, value)  # 힙 조건을 유지하며 새 값 추가
    elif value > heap[0]:  # 새 값이 현재 상위 K개의 최솟값보다 좋은지 검사
        heapreplace(heap, value)  # 가장 약한 보관값을 제거하고 새 값을 넣기
result = sorted(heap, reverse=True)  # 필요한 경우에만 보관한 K개를 최종 내림차순 정렬
```

이 예제는 K가 양수라는 조건입니다.
K=0을 허용한다면 빈 힙의 루트를 읽기 전에 별도로 처리해야 합니다.

## 정답성의 귀납

입력의 접두 구간을 처리한 뒤 힙은 그 구간의 큰 값 K개 또는 아직 K개 미만인 모든 값을 보관합니다.
K개 미만이면 새 값을 모두 넣으므로 의미가 유지됩니다.
K개를 채운 뒤 새 값이 루트 이하이면 그 값보다 크거나 같은 보관값이 이미 K개입니다.
새 값이 루트보다 크면 기존 상위 K개 중 가장 작은 값만 교체해야 새 상위 K개가 됩니다.
이 귀납은 힙이 정렬된 목록이라는 가정 없이 루트의 최솟값 성질만 사용합니다.

## 시간과 공간

이진 힙의 높이는 O(log N)이며 한 원소의 삽입·제거는 위아래 경로를 따라 복구할 수 있습니다.
배열 전체를 아래부터 힙으로 만드는 작업은 O(N)이며 N번 삽입하는 O(N log N) 방식과 구별합니다. [MIT 강의 8, Binary Heaps·Build Heap](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/40d4851e550507ca14dc778b9b2266cc_MIT6_006S20_lec8.pdf)
예제는 N개 입력에 O(N log K), 보관 공간 O(K)이며 마지막 정렬에 O(K log K)가 추가됩니다.
거리 후보를 계속 추가하는 방식에서는 힙 크기가 정점 수가 아니라 후보 수에 비례할 수 있습니다.

## 언어별 구현 차이

C에서는 배열 힙의 부모·자식 인덱스와 현재 길이·용량을 관리합니다.
0부터 번호를 매기면 자식은 `2*i+1`, `2*i+2`이며 배열 범위 안에 있는지 확인합니다.
C++의 기본 `priority_queue`는 큰 값이 먼저 나오므로 최소 힙이 필요한지 비교자를 확인합니다.
Python `heapq`의 기본 연산은 작은 값이 먼저 나오는 최소 힙입니다.
같은 우선순위 뒤에 비교 불가능한 객체가 놓인 튜플은 비교 오류가 날 수 있으므로 증가하는 번호 같은 동점 키를 둘 수 있습니다.

## 실전의 적용 조건

이산 사건 모형에서는 다음 발생 시각이 가장 빠른 사건을 꺼내고 새 사건을 넣는 설계가 자연스럽습니다.
실행 시간을 실제 시각과 동기화해야 하는 시스템이라면 알고리즘 순서 외에 시계와 동시성 규칙도 필요합니다.
상위 K개 집계에서는 전체 입력을 정렬·보관하지 않아도 되지만, 이미 버린 항목에 대한 임의 질의는 답할 수 없습니다.
이러한 우선순위 큐 활용은 MIT 강의에서도 사건 시뮬레이션과 스케줄링의 예로 소개됩니다. [MIT 강의 8, Priority Queue Interface](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/40d4851e550507ca14dc778b9b2266cc_MIT6_006S20_lec8.pdf)

## 실수와 반례

- 힙 배열 `[1,4,2]`는 최소 힙 조건을 만족하지만 정렬된 배열은 아닙니다.
- 새 값이 더 작은데도 무조건 `heapreplace`를 쓰면 상위 K개 불변식이 깨집니다.
- 오래된 후보를 제거하지 않는 거리 탐색은 불필요한 반복과 경우에 따라 잘못된 처리를 만들 수 있습니다.
- 우선순위만 같을 때도 처리 순서가 중요하면 그 순서를 명시하지 않은 구현은 요구를 만족하지 못할 수 있습니다.

## 연계 유형

[정렬](05-정렬과비교함수_sorting-comparators.md)은 전체 순서를 만드는 대안입니다.
[큐](07-스택큐덱_stack-queue-deque.md)는 우선순위 대신 도착 순서를 유지합니다.
[시뮬레이션](02-구현과시뮬레이션_implementation-simulation.md)은 다음 사건을 고르는 데 힙을 결합할 수 있습니다.

## 복습 질문과 답

질문 1. 큰 값 K개를 남기는데 왜 최소 힙을 사용합니까?

답. 현재 보관한 값 중 버릴 후보인 가장 작은 값을 빠르게 찾기 위해서입니다.

질문 2. 힙에서 두 번째 작은 값은 반드시 배열의 1번 위치입니까?

답. 아닙니다. 루트 외에는 전체 순위가 고정되지 않으며 양쪽 자식 중 하나일 수 있습니다.

## 근거와 예제 범위

힙 불변식과 API는 Python 문서, 높이·구축 비용과 활용 범위는 MIT 강의를 참고했습니다.
상위 세 값의 입력·추적·코드는 직접 구성한 예제입니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

입력된 값 중 큰 K개만 최소 힙에 남기고 마지막에 큰 값부터 출력합니다.

이 예제에서 직접 구현하는 기법은 최소 힙 · 상위 K개 유지 · 이진 힙 삽입과 삭제입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

N K(1≤K≤N≤20), N개 정수(−100~100)입니다. 같은 값도 서로 다른 원소로 셉니다.

```text
5 3
5 1 8 3 9
```

가장 큰 K개 값을 내림차순으로 한 줄에 출력합니다.

```text
9 8 5
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 입력5,1,8 처리 후 보관 값={1,5,8}, top=1 | 처음 세 값으로 크기3의 최소 힙을 채웁니다. |
| 2 | 새 값3: 1 제거 후 보관 값={3,5,8}, top=3 | 3보다 작은1은 이후의 상위3개에 필요하지 않습니다. |
| 3 | 새 값9: 3 제거 후 보관 값={5,8,9}, top=5 | 더 큰9를 넣고 가장 작은 보관 값을 버립니다. |
| 4 | 최솟값 삭제 순서=[5,8,9], 출력=[9,8,5] | 힙 삭제 결과를 뒤집어 내림차순을 얻습니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/08-힙과우선순위큐_heap-priority-queue/example.c>)

```c
#include <stdio.h> // 정수 입력과 선택한 값 출력
int heap[20], size = 0; // 작은 값이 맨 위인 힙과 현재 원소 수
void push(int value) { // 새 값을 힙에 넣는 함수
    int child = size++; // 새 값이 들어갈 마지막 위치 확보
    while (child > 0) { // 부모보다 작으면 위로 이동
        int parent = (child - 1) / 2; // 완전 이진 트리의 부모 인덱스
        if (heap[parent] <= value) break; // 부모가 더 작으면 힙 순서 확보
        heap[child] = heap[parent]; // 큰 부모를 한 칸 아래로 이동
        child = parent; // 다음 비교 위치를 부모로 변경
    } // 올라갈 경로 확인 끝
    heap[child] = value; // 정해진 위치에 새 값 저장
} // 삽입 함수 끝
int pop_min(void) { // 힙의 최솟값을 꺼내는 함수
    int result = heap[0], value = heap[--size], parent = 0; // 반환할 뿌리와 끝에서 가져올 값
    while (2 * parent + 1 < size) { // 왼쪽 자식이 있는 동안 아래로 이동
        int child = 2 * parent + 1; // 우선 왼쪽 자식 선택
        if (child + 1 < size && heap[child + 1] < heap[child]) ++child; // 두 자식 중 작은 쪽 선택
        if (value <= heap[child]) break; // 두 자식보다 작으면 이동 종료
        heap[parent] = heap[child]; // 작은 자식을 빈 부모 자리로 이동
        parent = child; // 빈자리를 자식 위치로 변경
    } // 내려갈 경로 확인 끝
    if (size > 0) heap[parent] = value; // 남은 힙이 있으면 끝 값을 빈자리에 저장
    return result; // 제거한 최솟값 반환
} // 삭제 함수 끝
int main(void) { // 실행 시작점
    int n, k, result[20]; // 입력 개수와 유지할 개수 및 정렬 출력 버퍼
    scanf("%d %d", &n, &k); // N과 K 읽기
    for (int i = 0; i < n; ++i) { // 값을 입력 순서대로 처리
        int value; scanf("%d", &value); // 이번 후보 값 읽기
        if (size < k) push(value); // K개가 차기 전에는 모두 보관
        else if (value > heap[0]) { // 현재 보관한 최솟값보다 큰 후보만 교체
            pop_min(); // 상위 K개에서 빠질 가장 작은 값 제거
            push(value); // 새 후보를 넣어 K개 유지
        } // 교체 판단 끝
    } // 전체 후보 확인 끝
    for (int i = 0; i < k; ++i) result[i] = pop_min(); // 남은 K개를 오름차순으로 꺼내기
    for (int i = k - 1; i >= 0; --i) printf("%s%d", i == k - 1 ? "" : " ", result[i]); // 역순으로 출력해 큰 값부터 나열
    printf("\n"); // 출력 줄 끝내기
    return 0; // 정상 종료
} // 상위 K개 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/08-힙과우선순위큐_heap-priority-queue/example.cpp>)

```cpp
#include <functional> // 작은 값 우선 비교자
#include <iostream> // 표준 입력과 출력
#include <queue> // 우선순위 큐
#include <vector> // 힙의 바탕 배열과 결과 저장
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n, k; cin >> n >> k; // 입력 개수와 유지할 개수 읽기
    priority_queue<int, vector<int>, greater<int>> heap; // 최솟값이 top인 힙
    for (int i = 0; i < n; ++i) { // 모든 후보를 입력 순서대로 처리
        int value; cin >> value; // 이번 후보 값 읽기
        if (static_cast<int>(heap.size()) < k) heap.push(value); // 빈자리가 있으면 후보 보관
        else if (value > heap.top()) { // 보관 중인 최솟값보다 클 때 교체
            heap.pop(); // 상위 K개에서 빠질 값 제거
            heap.push(value); // 새 값으로 K개 유지
        } // 교체 판단 끝
    } // 모든 후보 확인 끝
    vector<int> result; // 오름차순으로 꺼낸 값 저장
    while (!heap.empty()) { // 힙을 비울 때까지 반복
        result.push_back(heap.top()); // 현재 최솟값을 결과 끝에 저장
        heap.pop(); // 저장한 값을 힙에서 제거
    } // 오름차순 결과 완성
    for (int i = k - 1; i >= 0; --i) cout << (i == k - 1 ? "" : " ") << result[i]; // 역순으로 큰 값부터 출력
    cout << '\n'; // 출력 줄 끝내기
    return 0; // 정상 종료
} // 상위 K개 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/08-힙과우선순위큐_heap-priority-queue/example.py>)

```python
import heapq # 최솟값 힙 연산
import sys # 표준 입력 토큰 읽기
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, k = data[:2] # 입력 개수와 남길 개수 분리
heap = [] # 현재까지 큰 값 K개를 보관할 최소 힙
for value in data[2:]: # 후보 값을 입력 순서대로 처리
    if len(heap) < k: # 아직 K개를 채우지 못한 경우
        heapq.heappush(heap, value) # 후보를 힙에 추가
    elif value > heap[0]: # 가장 작은 보관 값보다 큰 후보인지 확인
        heapq.heappop(heap) # 상위 K개에서 빠질 최솟값 제거
        heapq.heappush(heap, value) # 새 후보를 넣어 크기 유지
result = [heapq.heappop(heap) for _ in range(k)] # 최솟값부터 꺼내 오름차순 배열 구성
print(*reversed(result)) # 역순으로 큰 값부터 출력
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 입력 | scanf로 공백으로 구분된 정수를 읽습니다. | cin으로 공백으로 구분된 정수를 읽습니다. | buffer.read().split()으로 입력 토큰을 한 번에 읽고 정수로 해석합니다. |
| 저장과 연산 | 크기20의 배열에서 부모·자식 인덱스를 계산해 직접 최소 힙을 유지합니다. | priority_queue에 greater&lt;int&gt;를 지정해 작은 값이 먼저 나오게 합니다. | heapq의 heappush와 heappop으로 같은 삽입·삭제 절차를 실행합니다. |
| 자료형과 범위 | 값과 인덱스 모두 작은 int 범위 안입니다. | 값과 인덱스 모두 작은 int 범위 안입니다. | int로 정수를 저장합니다. 허용 입력 범위는 C·C++ 예제와 같습니다. |

### 예제의 비용과 실행 파일

- 시간: O(N log(K+1)+K log(K+1))입니다.
- 보조 공간: 힙과 결과에 O(K)입니다. Python의 일괄 입력 목록에는 O(N)이 추가됩니다.

후보마다 힙 연산을 최대 한 쌍 수행하고 마지막 K개도 힙에서 꺼냅니다.

[예제 입력](<예제_examples/08-힙과우선순위큐_heap-priority-queue/input.txt>) · [예상 출력](<예제_examples/08-힙과우선순위큐_heap-priority-queue/output.txt>) · [예제 실행 방법](<예제_examples/08-힙과우선순위큐_heap-priority-queue/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 2 | 42626 더 맵게 | — | [C++](<../C++/level2/079_42626_더_맵게/README.md>) | [Python](<../Python/level2/079_42626_더_맵게/README.md>) |
| 3 | 42627 디스크 컨트롤러 | — | [C++](<../C++/level3/070_42627_디스크_컨트롤러/README.md>) | [Python](<../Python/level3/070_42627_디스크_컨트롤러/README.md>) |
| 3 | 42628 이중우선순위큐 | — | [C++](<../C++/level3/069_42628_이중우선순위큐/README.md>) | [Python](<../Python/level3/069_42628_이중우선순위큐/README.md>) |
| 2 | 142085 디펜스 게임 | [C](<../C/level2/033_142085_디펜스_게임/README.md>) | [C++](<../C++/level2/033_142085_디펜스_게임/README.md>) | [Python](<../Python/level2/033_142085_디펜스_게임/README.md>) |
| 3 | 468376 최고 속도 | [C](<../C/level3/004_468376_최고_속도/README.md>) | [C++](<../C++/level3/004_468376_최고_속도/README.md>) | [Python](<../Python/level3/004_468376_최고_속도/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/heap.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

# 완전 탐색과 중간에서 만나기

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 후보를 빠짐없이 표현하는 설계

완전 탐색은 가능한 후보를 모두 확인하여 정답을 찾는 방법입니다.
핵심은 반복문을 많이 쓰는 것이 아니라 모든 해를 표현하는 후보 체계와 올바른 검사입니다.
원소를 고를지 말지 결정하는 부분집합은 2^N개, 서로 다른 N개를 순서대로 놓는 순열은 N!개입니다.
조합과 순열을 혼동하면 필요한 후보를 빼거나 같은 후보를 여러 번 셀 수 있습니다.
Python도 두 생성 연산을 구별합니다. [Python itertools, Combinatoric Iterators](https://docs.python.org/3/library/itertools.html#itertools.combinations)

느리더라도 작은 입력에서 정확한 완전 탐색은 빠른 알고리즘의 독립 비교 기준으로 유용합니다.
다만 후보 생성기와 빠른 풀이가 같은 잘못된 가정을 공유하면 비교만으로 오류를 찾지 못할 수 있습니다.

## 중간에서 만나기의 단서

N이 대략 수십 개이고 각 선택의 결과를 합·차·개수 같은 작은 요약으로 결합할 수 있으면 반으로 나누기를 검토합니다.
왼쪽 절반의 모든 결과와 오른쪽 절반의 모든 결과를 만든 뒤 원하는 조합을 검색합니다.
이는 전체 후보를 근사적으로 줄이는 것이 아니라 결합 계산을 재사용하는 정확한 방법입니다.
MIT의 부분합 강의도 반씩 나눈 부분집합의 합을 정렬·검색해 결합하는 기법을 소개합니다. [MIT 6.1420 강의 2, §2.1 Subset Sum](https://people.csail.mit.edu/virgi/6.1420/lecture2.pdf)

두 절반의 내부 선택을 요약한 값만으로 결합 가능 여부를 알 수 있어야 합니다.
양쪽 사이의 복잡한 순서 제약을 요약에 담지 못하면 합 하나만 저장하는 분할은 정보가 부족합니다.

## 직접 구성한 예제: 합이 9인 부분집합 수

서로 다른 위치의 값 `[2,4,5,7]`에서 합이 9인 부분집합을 셉니다.
왼쪽은 `[2,4]`, 오른쪽은 `[5,7]`로 나눕니다.

| 왼쪽 선택 | 왼쪽 합 | 필요한 오른쪽 합 | 가능한 오른쪽 선택 |
|---|---:|---:|---|
| 빈 선택 | 0 | 9 | 없음 |
| 2 | 2 | 7 | 7 |
| 4 | 4 | 5 | 5 |
| 2,4 | 6 | 3 | 없음 |

왼쪽 합 목록은 `[0,2,4,6]`, 오른쪽 합 목록은 `[0,5,7,12]`입니다.
정답은 `{2,7}`, `{4,5}`의 두 가지입니다.
값이 같은 다른 위치를 별개 선택으로 센다면 같은 합이 여러 번 나오는 횟수도 보존해야 합니다.

## 부분합 생성과 결합 코드

다음 코드는 부분집합의 개수를 세며, 실제 선택 원소를 복원하지는 않습니다.

```python
from bisect import bisect_left, bisect_right  # 정렬된 합 목록에서 같은 값 구간의 양 끝 찾기
def subset_sums(values):  # 절반 배열의 모든 부분집합 합을 만드는 함수
    result = [0]  # 아무것도 고르지 않은 합 0부터 시작
    for value in values:  # 새 원소를 하나씩 선택 후보에 추가
        result += [subtotal + value for subtotal in result]  # 기존 선택마다 새 원소를 고른 경우를 별도 리스트로 만들어 추가
    return result  # 같은 합의 중복도 보존한 전체 부분합 반환
values, target = [2, 4, 5, 7], 9  # 직접 구성한 입력과 목표 합
middle = len(values) // 2  # 원소 수가 비슷한 두 절반의 경계
left = subset_sums(values[:middle])  # 왼쪽 절반의 모든 부분합 생성
right = sorted(subset_sums(values[middle:]))  # 오른쪽 부분합을 검색할 수 있게 정렬
answer = sum(bisect_right(right, target - subtotal) - bisect_left(right, target - subtotal) for subtotal in left)  # 필요한 오른쪽 합의 등장 횟수를 왼쪽 선택마다 더하기
```

새 결과를 만드는 리스트 내포는 기존 `result`를 다 읽은 다음 `+=`로 붙입니다.
같은 리스트를 늘리면서 그 리스트의 늘어나는 끝까지 순회하는 생성기로 바꾸면 다른 동작이 될 수 있습니다.

## 정답성: 해의 유일한 분해

전체 부분집합 S는 왼쪽에 속한 부분집합 L과 오른쪽에 속한 부분집합 R로 유일하게 나뉩니다.
반대로 L과 R을 하나씩 고르면 두 절반이 겹치지 않으므로 전체 부분집합 하나가 됩니다.
전체 합이 목표인 조건은 `sum(R)=target-sum(L)`과 동치입니다.
왼쪽의 모든 선택마다 정확히 이 값을 갖는 오른쪽 선택의 횟수를 더하므로 누락과 중복 계산이 없습니다.

빈 부분집합도 후보에 포함한 이유는 한쪽 절반에서 아무 원소도 선택하지 않은 해를 표현하기 위해서입니다.
목표가 0이고 빈 전체 선택을 금지한다면 마지막에 그 한 경우만 구별해 제외해야 합니다.

## 시간·공간과 규모

N=40에서 전체 부분집합은 2^40개이지만 절반은 각각 2^20개입니다.
이는 여전히 백만 단위의 목록이므로 저장 공간을 미리 계산해야 합니다.
8바이트 정수 백만 개라는 가정만으로 약 8MiB이며 Python 객체 목록의 실제 메모리는 그보다 클 수 있습니다.

위 코드의 반쪽 부분합 생성은 고정 크기 정수 연산을 가정할 때 O(2^(N/2))입니다.
정렬과 각 합의 이진 탐색을 포함한 전체 상한은 O(N·2^(N/2)), 공간은 O(2^(N/2))입니다.
해시 빈도를 사용하면 결합 단계의 기대 비용을 줄이는 대안도 있지만 최악 시간 보장과 메모리 특성이 다릅니다.
합의 크기가 작으면 지수적 열거 대신 합 범위를 상태로 쓰는 동적 계획법이 더 적절할 수 있습니다.

## 언어와 실전 조건

C·C++에서는 부분합의 정수 범위와 후보 개수에 맞는 할당 크기를 따로 계산합니다.
비트 마스크의 자료형 너비보다 큰 비트를 이동하는 표현도 피해야 합니다.
Python에서는 정수 객체·목록의 비용과 정렬용 공간을 함께 계산하며 거대한 선택 목록 전체를 저장하지 않도록 합니다.
작은 수의 옵션을 정확히 조합해야 하는 설계 비교에서는 중간 결과를 합·비용·사용 개수로 요약할 수 있는지 검토합니다.
옵션 간 충돌이 있다면 그 정보를 버리지 않는 요약이 필요하며 이 글의 단순 합 모형을 그대로 쓰면 안 됩니다.

## 실수와 반례

- 값 `[1,1]`의 부분합 1은 위치 기준으로 두 선택입니다. 집합으로 중복 제거하면 개수 답이 달라집니다.
- 합이 커졌으니 버린다는 가지치기는 음수가 있을 때 안전하지 않습니다.
- 전체 후보 쌍을 다시 곱으로 검사하면 반으로 나눈 뒤에도 2^N 비용이 됩니다.
- 선택 순서가 중요하지 않은 문제에서 모든 순열을 만들면 같은 조합을 여러 번 셉니다.

## 연계 유형

[이진 탐색](11-이진탐색과매개변수탐색_binary-parametric-search.md)과 [해시](06-해시와빈도집계_hashing-counting.md)는 두 절반의 결과를 결합하는 도구입니다.
[백트래킹](13-백트래킹과가지치기_backtracking-pruning.md)은 불가능한 후보의 하위 공간을 생략합니다.

## 복습 질문과 답

질문 1. 반으로 나누기만 하면 항상 빨라집니까?

답. 아닙니다. 두 절반의 결과를 전부 곱으로 검사하지 않고 정렬·검색 같은 방법으로 결합할 수 있어야 합니다.

질문 2. 같은 합을 중복 저장하는 이유는 무엇입니까?

답. 서로 다른 선택이 같은 합을 만들 수 있으며 개수 문제에서는 그 횟수도 정답의 일부이기 때문입니다.

## 근거와 예제 범위

MIT 자료는 부분합 meet-in-the-middle의 기본 분할·결합 원리, Python 문서는 후보 생성·경계 검색 API의 근거입니다.
작은 입력·코드·유일 분해 증명과 자원 계산은 직접 구성했으며 최신 최속 부분합 알고리즘을 주장하지 않습니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

원소를 두 절반으로 나누어 각 부분합을 만들고 보완 합의 개수를 더해 전체 부분집합 수를 구합니다.

이 예제에서 직접 구현하는 기법은 부분집합 열거 · 중간에서 만나기 · 보완 합 · 중복값의 이진 경계입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

N target(0≤N≤24,−100000≤target≤100000), N개 정수(−1000~1000)입니다. 같은 값도 위치가 다르면 다른 원소이며 빈 부분집합도 셉니다.

```text
4 9
2 4 5 7
```

합이 target인 부분집합의 개수를 정수 하나로 출력합니다.

```text
2
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 왼쪽[2,4]의 부분합=[0,2,4,6] | 각 원소를 넣거나 빼는 네 선택을 만듭니다. |
| 2 | 오른쪽[5,7]의 정렬 부분합=[0,5,7,12] | 필요한 합의 범위를 이진 탐색할 목록을 만듭니다. |
| 3 | 왼쪽 합2: need=7, 오른쪽 선택[7]이1개 | [2,7]이 목표 합9를 만드는 첫 부분집합입니다. |
| 4 | 왼쪽 합4: need=5가1개, 합0과6의 보완 값은0개, answer=2 | 두 번째 부분집합[4,5]를 더하고 전체 개수를2로 확정합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/12-완전탐색과중간에서만나기_exhaustive-meet-in-middle/example.c>)

```c
#include <stdio.h> // 정수 입력과 부분집합 개수 출력
#include <stdlib.h> // 오른쪽 부분합 정렬 함수
long long left_sums[4096], right_sums[4096]; // 절반당 최대 12개 원소의 모든 부분합
int compare(const void* a, const void* b) { // qsort가 사용할 오름차순 비교
    long long x = *(const long long*)a, y = *(const long long*)b; // 비교 대상의 실제 부분합 읽기
    return (x > y) - (x < y); // 뺄셈 넘침 없이 비교 부호 반환
} // 비교 함수 끝
int lower_bound_index(long long* sums, int count, long long target) { // target 이상인 첫 위치 검색
    int low = 0, high = count; // 정답 위치가 포함된 반열린 탐색 구간
    while (low < high) { // 경계가 하나로 좁혀질 때까지 반복
        int middle = low + (high - low) / 2; // 중앙 인덱스
        if (sums[middle] < target) low = middle + 1; // target보다 작은 부분을 제외
        else high = middle; // target 이상인 첫 위치를 왼쪽에서 탐색
    } // 경계 탐색 끝
    return low; // 첫 이상 위치 반환
} // lower bound 함수 끝
int upper_bound_index(long long* sums, int count, long long target) { // target보다 큰 첫 위치 검색
    int low = 0, high = count; // 가능한 삽입 위치 범위
    while (low < high) { // 첫 초과 위치를 찾을 때까지 반복
        int middle = low + (high - low) / 2; // 중앙 인덱스
        if (sums[middle] <= target) low = middle + 1; // target과 같은 부분까지 제외
        else high = middle; // 초과 값이 시작되는 왼쪽 경계 탐색
    } // 경계 탐색 끝
    return low; // 첫 초과 위치 반환
} // upper bound 함수 끝
int main(void) { // 실행 시작점
    int n, values[24], left_count = 1, right_count = 1; // 원소와 양쪽 부분합 개수
    long long target, answer = 0; // 목표 합과 찾은 부분집합 수
    scanf("%d %lld", &n, &target); // 원소 수와 목표 합 입력
    for (int i = 0; i < n; ++i) scanf("%d", &values[i]); // 각 위치의 원소 입력
    left_sums[0] = right_sums[0] = 0; // 두 절반 모두 빈 부분집합부터 시작
    for (int i = 0; i < n / 2; ++i) { // 왼쪽 절반의 모든 부분합 생성
        int old_count = left_count; // 새 원소를 넣기 전 부분합 수 고정
        for (int j = 0; j < old_count; ++j) left_sums[left_count++] = left_sums[j] + values[i]; // 기존 부분합마다 이번 원소를 넣은 경우 추가
    } // 왼쪽 부분합 생성 끝
    for (int i = n / 2; i < n; ++i) { // 오른쪽 절반의 모든 부분합 생성
        int old_count = right_count; // 확장 전 부분합 수 고정
        for (int j = 0; j < old_count; ++j) right_sums[right_count++] = right_sums[j] + values[i]; // 이번 원소를 넣는 선택 추가
    } // 오른쪽 부분합 생성 끝
    qsort(right_sums, right_count, sizeof(long long), compare); // 같은 보완 합이 연속하도록 정렬
    for (int i = 0; i < left_count; ++i) { // 각 왼쪽 선택에 맞는 오른쪽 선택 수 누적
        long long need = target - left_sums[i]; // 오른쪽에서 필요한 보완 합
        answer += upper_bound_index(right_sums, right_count, need) - lower_bound_index(right_sums, right_count, need); // 같은 합의 전체 개수를 두 경계 차이로 더하기
    } // 모든 양쪽 조합 계산 끝
    printf("%lld\n", answer); // 목표 합을 만드는 부분집합 수 출력
    return 0; // 정상 종료
} // 중간에서 만나기 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/12-완전탐색과중간에서만나기_exhaustive-meet-in-middle/example.cpp>)

```cpp
#include <algorithm> // 정렬과 두 삽입 경계 검색
#include <iostream> // 표준 입력과 출력
#include <vector> // 절반의 부분합 목록
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n; long long target; cin >> n >> target; // 원소 수와 목표 합 입력
    vector<int> values(n); // 각 위치의 값 저장
    for (int& value : values) cin >> value; // 원소 입력
    vector<long long> left_sums{0}, right_sums{0}; // 빈 부분집합의 합부터 시작
    for (int i = 0; i < n / 2; ++i) { // 왼쪽 절반의 선택 확장
        int old_count = static_cast<int>(left_sums.size()); // 확장 전 길이 고정
        for (int j = 0; j < old_count; ++j) left_sums.push_back(left_sums[j] + values[i]); // 원소를 넣는 새 부분집합 추가
    } // 왼쪽 부분합 생성 끝
    for (int i = n / 2; i < n; ++i) { // 오른쪽 절반의 선택 확장
        int old_count = static_cast<int>(right_sums.size()); // 이번 확장 전 길이 고정
        for (int j = 0; j < old_count; ++j) right_sums.push_back(right_sums[j] + values[i]); // 이번 원소를 넣은 부분합 추가
    } // 오른쪽 부분합 생성 끝
    sort(right_sums.begin(), right_sums.end()); // 보완 합의 개수를 셀 수 있게 정렬
    long long answer = 0; // 목표 합을 만드는 부분집합 수
    for (long long left : left_sums) { // 왼쪽의 모든 선택 확인
        long long need = target - left; // 오른쪽에서 필요한 합
        answer += upper_bound(right_sums.begin(), right_sums.end(), need) - lower_bound(right_sums.begin(), right_sums.end(), need); // 같은 보완 합의 개수 누적
    } // 양쪽 절반 결합 끝
    cout << answer << '\n'; // 부분집합 개수 출력
    return 0; // 정상 종료
} // 중간에서 만나기 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/12-완전탐색과중간에서만나기_exhaustive-meet-in-middle/example.py>)

```python
from bisect import bisect_left, bisect_right # 같은 보완 합의 양쪽 경계 검색
import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, target = data[:2] # 원소 수와 목표 합
values = data[2:] # 위치별 원소 값
left_sums, right_sums = [0], [0] # 양쪽 빈 부분집합의 합
for value in values[:n // 2]: # 왼쪽 절반의 원소를 하나씩 반영
    left_sums += [total + value for total in left_sums] # 확장 전 각 선택에 이번 원소를 넣는 경우 추가
for value in values[n // 2:]: # 오른쪽 절반의 원소를 하나씩 반영
    right_sums += [total + value for total in right_sums] # 이번 원소를 넣는 오른쪽 선택 추가
right_sums.sort() # 같은 부분합을 연속 위치로 모으기
answer = 0 # 목표 합을 만드는 부분집합 수
for left in left_sums: # 왼쪽 선택마다 보완 합 검색
    need = target - left # 오른쪽에서 필요한 합
    answer += bisect_right(right_sums, need) - bisect_left(right_sums, need) # 같은 값의 전체 개수 누적
print(answer) # 목표 합의 부분집합 수 출력
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 입력 | scanf로 공백으로 구분된 정수를 읽습니다. | cin으로 공백으로 구분된 정수를 읽습니다. | buffer.read().split()으로 입력 토큰을 한 번에 읽고 정수로 해석합니다. |
| 저장과 연산 | 최대4096칸의 두 long long 배열과 직접 구현한 lower·upper bound를 사용합니다. | vector의 확장 전 길이를 고정해 push_back하고 표준 경계 검색을 사용합니다. | 리스트 내포를 먼저 평가해 기존 선택의 확장본을 더하고 bisect로 중복 개수를 셉니다. |
| 자료형과 범위 | 합과 부분집합 개수는 long long입니다. N≤24이므로 전체 부분집합 수는2^24 이하입니다. | 합과 부분집합 개수는 long long입니다. N≤24이므로 전체 부분집합 수는2^24 이하입니다. | int로 정수를 저장합니다. 허용 입력 범위는 C·C++ 예제와 같습니다. |

### 예제의 비용과 실행 파일

- 시간: 정렬이 O(M log M)인 구현에서는 O(N·2^ceil(N/2))입니다. C qsort의 최악 시간은 표준이 보장하지 않습니다.
- 보조 공간: 양쪽 부분합에 O(2^ceil(N/2))입니다.

각 절반의 부분집합을 만들고 오른쪽을 정렬한 뒤 왼쪽마다 두 경계를 검색합니다.

[예제 입력](<예제_examples/12-완전탐색과중간에서만나기_exhaustive-meet-in-middle/input.txt>) · [예상 출력](<예제_examples/12-완전탐색과중간에서만나기_exhaustive-meet-in-middle/output.txt>) · [예제 실행 방법](<예제_examples/12-완전탐색과중간에서만나기_exhaustive-meet-in-middle/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 0 | 181921 배열 만들기 2 | [C](<../C/level0/extra_181921_배열_만들기_2/README.md>) | [C++](<../C++/level0/extra_181921_배열_만들기_2/README.md>) | [Python](<../Python/level0/extra_181921_배열_만들기_2/README.md>) |
| 1 | 468371 노란불 신호등 | [C](<../C/level1/extra_468371_노란불_신호등/README.md>) | [C++](<../C++/level1/extra_468371_노란불_신호등/README.md>) | [Python](<../Python/level1/extra_468371_노란불_신호등/README.md>) |
| 2 | 468377 힌트 스테이지 | [C](<../C/level2/002_468377_힌트_스테이지/README.md>) | [C++](<../C++/level2/002_468377_힌트_스테이지/README.md>) | [Python](<../Python/level2/002_468377_힌트_스테이지/README.md>) |
| 3 | 451808 숫자 야구 | [C](<../C/level3/007_451808_숫자_야구/README.md>) | [C++](<../C++/level3/007_451808_숫자_야구/README.md>) | [Python](<../Python/level3/007_451808_숫자_야구/README.md>) |
| 4 | 389630 격자 뒤집기 미로 | [C](<../C/level4/extra_389630_격자_뒤집기_미로/README.md>) | [C++](<../C++/level4/extra_389630_격자_뒤집기_미로/README.md>) | [Python](<../Python/level4/extra_389630_격자_뒤집기_미로/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/bruteforce.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

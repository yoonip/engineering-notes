# 행렬 거듭제곱과 선형 점화

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 핵심 원리와 중요성

같은 상태 전이를 매우 많이 반복해야 할 때 한 번의 전이를 행렬로 나타냅니다.
행렬 곱셈은 결합법칙이 있으므로 전이를 두 배씩 합쳐 지수를 이진수로 처리할 수 있습니다.
단계 수 N이 커도 상태 차원 d가 작으면 N번 반복하는 대신 O(log N)번의 행렬 곱으로 줄입니다.
곱셈의 순서는 일반적으로 바꿀 수 없으므로 결합법칙과 교환법칙을 혼동하지 않습니다.
피보나치 행렬과 이진 거듭제곱의 관계는 [Williams 대학 원저자 해설](https://web.williams.edu/Mathematics/sjmiller/public_html/math/papers/ComputingFibonacciRevised.pdf)에서 확인합니다.

## 알아보는 단서와 불가 조건

- 앞의 고정된 k개 항으로 다음 항을 만드는 상수 계수 선형 점화를 찾습니다.
- 작은 상태의 경로 수·확률 분포를 동일한 전이로 반복하는지 확인합니다.
- N이 매우 크고, 직접 반복 O(N)이 제한을 넘는 경우를 검토합니다.
- 다음 항이 이전 항들의 곱이나 조건부 비선형 함수이면 같은 작은 선형 행렬로 바로 바꿀 수 없습니다.

시간에 따라 전이가 바뀐다면 A^N이 아니라 A_(N-1)…A_1 A_0의 순서 있는 곱입니다.
전이가 주기적으로 반복되면 한 주기의 곱을 만들고 남은 구간을 분리할 수 있습니다.
상태 차원이 너무 크거나 희소성이 제곱 중 사라지면 행렬 곱의 비용이 더 커질 수 있습니다.

## 상태 벡터와 행렬의 방향

피보나치 F0=0,F1=1,F_(n+1)=F_n+F_(n-1)을 사용합니다.
열벡터 v_n=[F_(n+1),F_n]^T라 정하면 v_(n+1)=A v_n입니다.
A=[[1,1],[1,0]]이며, 첫 행은 두 값을 더하고 둘째 행은 앞 값을 그대로 옮깁니다.
v_0=[1,0]^T이므로 v_n=A^n v_0입니다.
행벡터를 쓰는 구현은 오른쪽에 행렬을 곱하므로 표의 방향을 통일합니다.

## 직접 구성한 지수 추적

F5를 구하면 N=5=4+1입니다.

| 행렬 | 값 | 의미 |
| --- | --- | --- |
| A | [[1,1],[1,0]] | 한 단계 |
| A² | [[2,1],[1,1]] | 두 단계 |
| A⁴ | [[5,3],[3,2]] | 네 단계 |
| A⁵=A⁴A | [[8,5],[5,3]] | 다섯 단계 |

A⁵[1,0]^T=[8,5]^T이므로 F5=5입니다.
F5를 찾는다고 A를 5번 곱할 필요 없이 두 번의 제곱과 선택한 지수의 곱으로 구성합니다.
단계 0에서는 단위행렬 I를 사용하므로 초기 벡터가 그대로 남습니다.

## 짧은 구현

```python
def matrix_power(matrix, exponent, modulus):  # 정사각 행렬과 음이 아닌 지수
    size = len(matrix)  # 상태의 차원
    answer = [[int(i == j) for j in range(size)] for i in range(size)]  # 단위행렬
    def multiply(left, right):  # 왼쪽 뒤에 오른쪽 인수를 곱한 행렬 계산
        return [[sum(left[i][k] * right[k][j] for k in range(size)) % modulus for j in range(size)] for i in range(size)]  # 행·열 내적 후 나머지
    base = [[value % modulus for value in row] for row in matrix]  # 입력과 분리한 현재 거듭제곱
    while exponent:  # 아직 처리하지 않은 이진수 자리 확인
        if exponent & 1:  # 해당 자리의 거듭제곱이 필요하면 선택
            answer = multiply(answer, base)  # 현재 결과에 선택한 인수 누적
        base = multiply(base, base)  # 다음 자리의 두 배 거듭제곱
        exponent >>= 1  # 처리한 자리 제거
    return [[value % modulus for value in row] for row in answer]  # 지수 0과 modulus=1도 정규화
```

이 코드는 개념을 보이는 짧은 구현이며, 큰 입력에는 중간 합의 크기와 반복문 비용을 따로 확인합니다.
modulus는 양의 정수이며 빈 행렬·직사각 행렬은 이 예제의 입력 범위에 포함하지 않습니다.

## 왜 맞는지와 복잡도

처리 중 answer × base^exponent가 원래 거듭제곱과 같다는 불변식을 유지합니다.
지수가 홀수이면 base 한 개를 answer로 옮기고, 남은 짝수 지수는 base²의 절반 지수로 바꿉니다.
결합법칙으로 이 변형이 같은 값을 보존하며 exponent=0일 때 answer가 답입니다.
일반적인 세 겹 반복문 곱셈은 O(d³) 산술 연산입니다.
따라서 거듭제곱은 O(d³ log N) 시간, 반복형의 행렬 저장은 O(d²) 공간입니다.
정확한 정수 피보나치처럼 답의 비트 수가 커지는 경우에는 산술 연산을 O(1)로 보지 않습니다.
모듈러가 고정된 경우에도 C·C++에서 곱과 여러 항의 합이 자료형 범위를 넘는지 확인합니다.

## 선형 점화의 확장

a_n=c1 a_(n-1)+…+ck a_(n-k)이면 최근 k개 항을 상태로 놓습니다.
첫 행에는 c1…ck를, 그 아래에는 이전 항을 한 칸씩 옮기는 1을 배치합니다.
a_(n+1)=2a_n+3 같은 상수항은 상태에 항상 1인 성분을 추가해 선형 전이로 바꿉니다.
누적합 S_(n+1)=S_n+a_(n+1)도 S 성분을 추가하면 함께 구합니다.
점화 차수 k가 크면 특성 다항식으로 x^N을 줄이는 방법이 행렬보다 유리할 수 있습니다.
직접 다항식 곱·나머지를 쓰는 대표 구성은 O(k² log N) 연산, O(k) 저장을 목표로 합니다.
이때 초기 k개 항과 동일한 상수 계수 점화라는 조건이 필요합니다.

## 경로 수·확률과 실전 연결

인접 행렬의 (i,j)가 i→j의 간선 수이면 A^N의 (i,j)는 정확히 N개 간선을 쓰는 보행 수입니다.
정점을 반복 방문할 수 있으므로 단순 경로 개수를 세는 결과로 해석하지 않습니다.
확률 전이 행렬은 행·열 합의 방향을 정하고 초기 분포와 같은 약속으로 곱합니다.
마르코프 모델은 현재 상태에 미래 분포가 충분히 결정된다는 가정이며, 숨은 과거 의존성이 있으면 상태를 늘립니다.
이산 선형 시스템의 반복 전이와 연결되지만, 부동소수점 제곱에서는 오차와 수치 안정성도 검토합니다.
[선형 점화와 생성함수](31-조합론과생성함수_combinatorics-generating-functions.md), [함수 반복 점프](38-함수그래프와반복점프_functional-graph-lifting.md)는 같은 “전이 합성” 관점을 공유합니다.

## 복습 질문과 답

- 질문: a_(n+1)=a_n²도 두 항짜리 선형 행렬로 옮길 수 있습니까? 답: 상태 성분에 대한 선형 결합이 아니므로 같은 방식으로 바로 옮길 수 없습니다.
- 질문: 인접 행렬 거듭제곱은 최단 경로 길이입니까? 답: 보통의 덧셈·곱셈에서는 정해진 간선 수의 보행 수이며, 다른 목적은 연산 정의도 바꿔야 합니다.
- 질문: 시간 복잡도 O(log N)이라고만 써도 됩니까? 답: 상태 차원과 행렬 곱 비용이 있어 일반적인 구현은 O(d³ log N)입니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

같은 선형 전이의 거듭제곱을 합성하여 큰 단계의 피보나치 나머지를 구합니다.

이 예제에서 직접 구현하는 기법은 선형 점화의 행렬 표현 · 단위행렬 · 이진 거듭제곱입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

N,m 두 정수이며 0≤N≤1000000000,1≤m≤1000000입니다. F0=0,F1=1입니다.

```text
5 1000
```

F_N mod m을 한 줄에 출력합니다.

```text
5
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | A=[[1,1],[1,0]],v0=[1,0] | 한 단계의 두 항 이동을 행렬로 정의합니다. |
| 2 | A²=[[2,1],[1,1]] | 같은 전이를 두 번 합성합니다. |
| 3 | A⁴=[[5,3],[3,2]],5=4+1 | 필요한 지수의 행렬만 골라 곱합니다. |
| 4 | A⁵=[[8,5],[5,3]],F5=5 | 열벡터의 두 번째 성분을 읽는 것과 같은 answer[1][0]을 출력합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/32-행렬거듭제곱과선형점화_matrix-recurrence/example.c>)

```c
#include <stdio.h>  // 표준 입력과 출력 함수

typedef struct { long long cell[2][2]; } Matrix;  // 두 항의 선형 전이 저장
long long modulus;  // 모든 행렬 연산의 같은 모듈러
Matrix multiply(Matrix left, Matrix right) {  // 입력과 분리한 행렬 곱
    Matrix result = {{{0, 0}, {0, 0}}};  // 새 결과는 영행렬
    for (int i = 0; i < 2; ++i) {  // 결과의 행
        for (int j = 0; j < 2; ++j) {  // 결과의 열
            for (int k = 0; k < 2; ++k) result.cell[i][j] = (result.cell[i][j] + left.cell[i][k] * right.cell[k][j]) % modulus;  // 행과 열의 내적
        }  // 한 행의 열 계산 끝
    }  // 행렬 곱 계산 끝
    return result;  // 독립적인 결과 행렬
}  // 곱셈 함수 끝
int main(void) {  // 피보나치 전이의 거듭제곱
    long long exponent;  // 계산할 단계 수
    scanf("%lld %lld", &exponent, &modulus);  // 지수와 모듈러 입력
    Matrix answer = {{{1, 0}, {0, 1}}};  // 0단계의 단위행렬
    Matrix base = {{{1, 1}, {1, 0}}};  // 한 단계 피보나치 전이
    while (exponent > 0) {  // 필요한 거듭제곱을 비트별로 선택
        if (exponent & 1LL) answer = multiply(answer, base);  // 현재 자리의 전이 누적
        base = multiply(base, base);  // 두 배 이동 길이로 제곱
        exponent >>= 1;  // 처리한 지수 비트 제거
    }  // 모든 단계 합성 끝
    printf("%lld\n", answer.cell[1][0] % modulus);  // F_N의 나머지
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/32-행렬거듭제곱과선형점화_matrix-recurrence/example.cpp>)

```cpp
#include <iostream>  // C++ 스트림 입력과 출력

typedef struct { long long cell[2][2]; } Matrix;  // 두 항의 선형 전이 저장
long long modulus;  // 모든 행렬 연산의 같은 모듈러
Matrix multiply(Matrix left, Matrix right) {  // 입력과 분리한 행렬 곱
    Matrix result = {{{0, 0}, {0, 0}}};  // 새 결과는 영행렬
    for (int i = 0; i < 2; ++i) {  // 결과의 행
        for (int j = 0; j < 2; ++j) {  // 결과의 열
            for (int k = 0; k < 2; ++k) result.cell[i][j] = (result.cell[i][j] + left.cell[i][k] * right.cell[k][j]) % modulus;  // 행과 열의 내적
        }  // 한 행의 열 계산 끝
    }  // 행렬 곱 계산 끝
    return result;  // 독립적인 결과 행렬
}  // 곱셈 함수 끝
int main() {  // 피보나치 전이의 거듭제곱
    long long exponent;  // 계산할 단계 수
    std::cin >> exponent >> modulus;  // 지수와 모듈러 입력
    Matrix answer = {{{1, 0}, {0, 1}}};  // 0단계의 단위행렬
    Matrix base = {{{1, 1}, {1, 0}}};  // 한 단계 피보나치 전이
    while (exponent > 0) {  // 필요한 거듭제곱을 비트별로 선택
        if (exponent & 1LL) answer = multiply(answer, base);  // 현재 자리의 전이 누적
        base = multiply(base, base);  // 두 배 이동 길이로 제곱
        exponent >>= 1;  // 처리한 지수 비트 제거
    }  // 모든 단계 합성 끝
    std::cout << answer.cell[1][0] % modulus << "\n";  // F_N의 나머지
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/32-행렬거듭제곱과선형점화_matrix-recurrence/example.py>)

```python
import sys  # 단계와 모듈러 읽기
exponent, modulus = map(int, sys.stdin.read().split())  # 피보나치 조건
def multiply(left, right):  # 2×2 행렬 내적
    result = [[0, 0], [0, 0]]  # 입력과 별개인 영행렬
    for i in range(2):  # 결과 행
        for j in range(2):  # 결과 열
            for k in range(2):  # 내적의 공통 좌표
                result[i][j] = (result[i][j] + left[i][k] * right[k][j]) % modulus  # 나머지를 유지한 곱 누적
    return result  # 새 행렬 반환
answer = [[1, 0], [0, 1]]  # 0단계 단위 전이
base = [[1, 1], [1, 0]]  # 한 단계의 점화
while exponent:  # 이진수 자리 처리
    if exponent & 1:  # 필요한 길이의 전이 선택
        answer = multiply(answer, base)  # 현재 결과에 합성
    base = multiply(base, base)  # 다음 자리의 제곱
    exponent >>= 1  # 처리한 자리 제거
print(answer[1][0] % modulus)  # 초기 벡터에서 F_N인 성분
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 2×2 long long 행렬 세 개와 지수 변수만 사용합니다. | 같은 2×2 구조체를 값으로 반환하여 행렬 입력을 덮어쓰지 않습니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: O(log(N+1)) 행렬 곱; 일반 차원 d에서는 O(d³log(N+1))
- 보조 공간: O(1); 일반 차원 d에서는 O(d²)

2×2 크기가 고정되어 한 제곱의 산술 연산 수가 일정합니다.

[예제 입력](<예제_examples/32-행렬거듭제곱과선형점화_matrix-recurrence/input.txt>) · [예상 출력](<예제_examples/32-행렬거듭제곱과선형점화_matrix-recurrence/output.txt>) · [예제 실행 방법](<예제_examples/32-행렬거듭제곱과선형점화_matrix-recurrence/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 2 | 12949 행렬의 곱셈 | — | [C++](<../C++/level2/extra_12949_행렬의_곱셈/README.md>) | [Python](<../Python/level2/extra_12949_행렬의_곱셈/README.md>) |
| 4 | 214290 경사로의 개수 | [C](<../C/level4/extra_214290_경사로의_개수/README.md>) | [C++](<../C++/level4/extra_214290_경사로의_개수/README.md>) | [Python](<../Python/level4/extra_214290_경사로의_개수/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/matrix.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

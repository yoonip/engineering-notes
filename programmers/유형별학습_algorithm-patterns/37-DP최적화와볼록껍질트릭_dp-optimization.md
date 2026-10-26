# DP 전이 최적화와 볼록 껍질 트릭

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 최적화 전에 필요한 정보

DP 최적화는 상태 수를 그대로 두고 상태마다 비교하는 전이 후보를 줄이는 방법입니다.
먼저 맞는 기본 전이와 느린 구현을 만들고, 최적 분할점이나 비용식의 구조를 증명합니다.
작은 입력에서 관찰한 분할점 순서가 큰 입력에서도 유지된다고 추측하는 것만으로는 부족합니다.
Monge 성질, 분할 정복 최적화, Knuth 최적화, CHT는 관련이 있지만 적용 조건이 같지 않습니다.

| 도구 | 확인할 핵심 조건 | 대표 효과 |
| --- | --- | --- |
| Monge 비용 | 교차한 네 비용의 부등식 | 일관된 동률 선택에서 최적 후보의 단조성 도출 |
| 분할 정복 DP | 한 층의 최적 분할점이 상태 순서대로 단조 | 한 층 O(n²)→O(n log n) |
| Knuth | 구간 점화와 양쪽 최적점 경계 | 전체 O(n³)→O(n²) |
| CHT | 전이를 직선의 값 비교로 분리 | 직선 질의 구조로 후보 탐색 대체 |

아래 계산 예제는 모두 직접 구성한 예제입니다.

## Monge 성질과 최적점 단조성

전이를 D_t[i]=min(j<i){D_(t-1)[j]+C(j,i)}로 정합니다.
j1<j2<i1<i2에서 C(j1,i1)+C(j2,i2)≤C(j1,i2)+C(j2,i1)이 성립하는 비용을 생각합니다.
두 열에 더한 이전 층의 값은 양쪽에서 상쇄되므로 후보 비교 행렬에도 이 부등식이 유지됩니다.
이 성질은 앞 상태의 큰 최적 후보가 뒤 상태의 작은 최적 후보와 역전될 수 없다는 단조성의 근거입니다.
동률에서는 항상 가장 작은 후보처럼 같은 규칙을 사용해야 합니다.
유효 후보 범위와 부등식의 방향도 현재 최소화 점화에 맞춰 확인합니다. [원저자 Knuth–Yao·총단조성 논문](https://www.cse.ust.hk/~golin/pubs/QI_SODA06_final.pdf)

예를 들어 음이 아닌 수열의 누적합 S에서 C(j,i)=(S_i−S_j)²를 생각합니다.
네 비용의 왼쪽−오른쪽은 −2(S_j2−S_j1)(S_i2−S_i1)≤0입니다.
비음수 수열이라는 조건은 두 누적합 차이의 부호를 보장합니다.
[1,1,−1]의 누적합 [0,1,2,1]에서는 j1=0,j2=1,i1=2,i2=3일 때 왼쪽 4, 오른쪽 2로 성질이 깨집니다.
모든 비용이 제곱이라 음이 아니어도 Monge라는 결론은 성립하지 않습니다.

## 분할 정복 최적화의 절차

한 층의 중간 상태 mid를 정하고 허용된 후보 [optL,optR]를 모두 비교합니다.
최적 후보 k를 찾으면 왼쪽 상태의 후보는 [optL,k], 오른쪽은 [k,optR]로 제한합니다.
이 축소가 안전한 이유는 이미 증명한 최적점의 비감소 순서입니다.
각 깊이에서 후보 확인량이 O(n)이고 깊이가 O(log n)이므로 한 층 O(n log n)입니다.
K개 층이면 O(Kn log n) 시간, 이전·현재 층과 누적합은 O(n) 공간입니다.
이는 C(j,i)를 O(1)에 계산할 수 있을 때이며, 비용 계산이 더 느리면 함께 곱합니다. [CP Initiative 분할 정복 DP 설명](https://usaco.guide/plat/DC-DP)

직접 구성한 [1,2,3,4]를 두 연속 구간으로 나누고 구간 합 제곱의 합을 최소화합니다.

| 접두 길이 i | 분할 j별 비용 | 최적 분할 |
| ---: | --- | ---: |
| 2 | j=1:1²+2²=5 | 1 |
| 3 | j=1:1²+5²=26, j=2:3²+3²=18 | 2 |
| 4 | j=1:1²+9²=82, j=2:3²+7²=58, j=3:6²+4²=52 | 3 |

이 예제의 순서는 단조성을 보여 주지만 일반적인 증명은 위 비용 부등식에서 얻습니다.
같은 층의 미계산 값이 필요한 점화에는 이전 층이 모두 정해졌다는 절차를 그대로 적용하지 않습니다.

## Knuth 최적화: 구간의 양쪽 경계

D[l][r]=C(l,r)+min(l≤k<r){D[l][k]+D[k+1][r]} 형태를 생각합니다.
구간 비용이 포함에 대해 단조이고 사각 부등식을 만족하면 대표적인 충분 조건을 얻습니다.
a≤b≤c≤d에서 C(b,c)≤C(a,d), C(a,c)+C(b,d)≤C(a,d)+C(b,c)를 확인합니다.
일관된 동률 규칙으로 opt[l][r−1]≤opt[l][r]≤opt[l+1][r]가 성립합니다.
이때 k를 두 경계 사이의 유효 분할점만 확인하도록 줄여 전체 O(n²) 시간, O(n²) 공간을 얻습니다.
단순히 한 축에서 opt가 증가한다는 사실만으로 이 양쪽 경계를 가정하지 않습니다. [Yao의 사각 부등식 원논문](https://doi.org/10.1145/800141.804691)

음이 아닌 파일 크기의 구간 합은 위 충분 조건을 만족합니다.
[2,3,4]에서 D[0][1]=5,opt=0이고 D[1][2]=7,opt=1입니다.
전체 비용은 k=0에서 7+9=16, k=1에서 5+9=14라 opt[0][2]=1입니다.
구간 길이를 늘리며 계산하고, 두 경계와 [l,r−1]의 교집합만 확인합니다.
초기 대각선의 opt와 동률 규칙을 명시하지 않으면 경계 오류가 생깁니다.

## 볼록 껍질 트릭: 전이를 직선으로 분리

D[i]=min(j<i){D[j]+(x_i−x_j)²+C}를 전개합니다.
D[i]=x_i²+C+min(j<i){(−2x_j)x_i+(D[j]+x_j²)}입니다.
이전 상태 j는 기울기 −2x_j, 절편 D[j]+x_j²인 직선 한 개가 됩니다.
현재 x_i에서 가장 낮은 직선 값을 질의한 뒤 현재 상태의 새 직선을 넣습니다.
모든 i가 공통으로 더하는 x_i²+C는 직선 간 비교에서 제외해도 됩니다. [스위스 정보올림피아드 CHT 강의](https://soi.ch/wiki/dp-optimization/)

C=1,x=[0,1,3,4],D[0]=0으로 직접 계산합니다.
x=1에서 기존 직선 0을 읽어 D[1]=1+1=2를 얻고 직선 −2x+3을 추가합니다.
x=3에서 직선 값 min(0,−3)=−3이므로 D[2]=9+1−3=7입니다.
이제 직선 −6x+16을 넣고 x=4에서 min(0,−5,−8)=−8을 읽어 D[3]=9를 얻습니다.
직접 비교에서도 D[2]+(4−3)²+1=9로 같습니다.

## CHT의 구현 조건과 복잡도

기울기와 질의 x가 모두 적절한 단조 순서이면 덱에서 쓸모없는 직선을 제거해 총 O(n) 처리가 가능합니다.
기울기는 단조지만 질의 순서가 임의이면 껍질에서 이분 탐색하는 O(log n) 질의를 검토합니다.
둘 다 임의이면 동적 직선 컨테이너나 Li Chao 트리처럼 다른 구조가 필요합니다.
유한 정수 x 범위 크기 U의 Li Chao 트리는 직선 한 개 삽입·점 질의를 각각 O(log U)에 처리할 수 있습니다.
고정 범위 전체 배열 또는 동적 노드·좌표 압축 중 어떤 저장 모델을 쓰는지에 따라 공간을 계산합니다.
같은 기울기의 직선은 최소화에서 절편이 큰 쪽을 버리며 0으로 나누는 교점을 만들지 않습니다.
교점의 부동소수점 비교 대신 교차 곱을 쓰더라도 중간 곱이 넘치지 않는 자료형 범위를 확인합니다.
일반적인 비선형 곡선을 아무 조건 없이 직선 CHT에 넣지 않습니다.

## 실전 연결과 확인 방법

구간 분할 비용과 순차 의사결정의 큰 DP에서 반복 후보 비교를 줄이는 데 활용합니다.
업무 비용식에 음수 할인·시간별 제약이 추가되면 기존 단조성 증명이 유지되는지 다시 확인합니다.
느린 전수 DP와 무작위 작은 입력을 비교하고, 최적 후보가 역전하는 입력을 별도로 찾습니다.
검증 사례는 증명의 대체가 아니며 조건을 위반한 예제에서 최적화가 실패하는지도 확인합니다.
Python은 큰 교차 곱을 정확히 계산하지만 연산 비용이 커지고, C·C++은 고정 폭 오버플로를 먼저 점검합니다.
[DP 상태 설계](16-동적계획법의상태와전이_dynamic-programming.md), [구간 DP](17-배낭수열구간확률DP_dp-variants.md), [기하의 외적](33-계산기하와좌표변환_computational-geometry.md)과 연결합니다.

## 복습 질문과 답

- 질문: 비용이 양수면 Monge 성질이 성립합니까? 답: 네 비용의 부등식이 별도로 필요하며 음이 아닌 제곱 비용도 누적합의 순서 조건이 깨지면 실패할 수 있습니다.
- 질문: 분할 정복 최적화와 Knuth의 전이 형태가 같습니까? 답: 전자는 층별 후보 단조성을, 후자는 구간 점화의 양쪽 최적점 경계를 사용합니다.
- 질문: CHT 덱에서 질의마다 앞 직선을 지워도 됩니까? 답: 이후 질의 x의 순서가 그 제거를 정당화할 때에만 가능하며 임의 순서 질의는 다른 처리가 필요합니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

증가하는 좌표의 제곱 비용 DP를 직선의 최소값으로 바꾸고 덱에서 불필요한 후보를 제거합니다.

이 예제에서 직접 구현하는 기법은 제곱 전이의 직선 분리 · 기울기 감소와 질의 증가 · 덱 CHT · 교차 곱으로 불필요한 직선 제거입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

n,C(0≤n≤30,0≤C≤1000), 다음 엄격히 증가하는 양의 좌표 x1..xn(1..1000)입니다. x0=0,D0=0,Di=min(j<i){Dj+(xi−xj)^2+C}입니다.

```text
3 1
1 3 4
```

D_n을 한 줄에 출력합니다.

```text
9
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | x=[0,1,3,4],C=1,직선0은 y=0 | 초기 상태를 직선 후보로 넣습니다. |
| 2 | x=1에서 D1=2,새 직선 y=−2x+3 | 현재 질의 후 계산한 상태를 다음 후보로 추가합니다. |
| 3 | x=3에서 직선값−3을 택해 D2=7 | 작은 x에서만 유리했던 앞 직선을 제거할 수 있습니다. |
| 4 | x=4에서 y=−6x+16의 값−8, D3=17−8=9 | 단조 질의로 앞 후보를 줄이며 실제 최적 전이를 계산합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/37-DP최적화와볼록껍질트릭_dp-optimization/example.c>)

```c
#include <stdio.h>  // 표준 입력과 출력 함수

long long slope[31], intercept[31];  // 이전 DP 상태를 나타내는 직선
long long evaluate(int line, long long x) {  // 현재 x에서 직선 값
    return slope[line] * x + intercept[line];  // 기울기와 절편의 선형식
}  // 직선 평가 끝
int redundant(int first, int middle, int last) {  // 가운데 직선이 아래 껍질에 불필요한지 확인
    return (intercept[middle] - intercept[first]) * (slope[middle] - slope[last]) >= (intercept[last] - intercept[middle]) * (slope[first] - slope[middle]);  // 감소 기울기의 교점 순서를 정수 곱으로 비교
}  // 후보 제거 판정 끝
int main(void) {  // 단조 CHT로 DP 계산
    int n, queue[31], head = 0, tail = 1;  // 앞과 뒤에서 줄일 후보 덱
    long long cost, x[31] = {0}, dp[31] = {0};  // x0과 D0은0
    scanf("%d %lld", &n, &cost);  // 상태 수와 매 전이의 상수 비용
    for (int i = 1; i <= n; ++i) scanf("%lld", &x[i]);  // 엄격 증가 좌표
    queue[0] = 0;  // 초기 직선 y=0
    for (int i = 1; i <= n; ++i) {  // 질의 x도 증가하는 순서
        while (tail - head >= 2 && evaluate(queue[head], x[i]) >= evaluate(queue[head + 1], x[i])) ++head;  // 앞으로도 불리한 앞 직선 제거
        dp[i] = x[i] * x[i] + cost + evaluate(queue[head], x[i]);  // 직선 최솟값과 공통 항 결합
        slope[i] = -2 * x[i];  // 새로운 상태의 감소 기울기
        intercept[i] = dp[i] + x[i] * x[i];  // 새로운 상태의 절편
        while (tail - head >= 2 && redundant(queue[tail - 2], queue[tail - 1], i)) --tail;  // 앞으로도 선택되지 않는 가운데 후보 제거
        queue[tail++] = i;  // 새 직선을 덱 뒤에 삽입
    }  // 모든 상태 계산 끝
    printf("%lld\n", dp[n]);  // 마지막 최적 비용
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/37-DP최적화와볼록껍질트릭_dp-optimization/example.cpp>)

```cpp
#include <iostream>  // C++ 스트림 입력과 출력

long long slope[31], intercept[31];  // 이전 DP 상태를 나타내는 직선
long long evaluate(int line, long long x) {  // 현재 x에서 직선 값
    return slope[line] * x + intercept[line];  // 기울기와 절편의 선형식
}  // 직선 평가 끝
int redundant(int first, int middle, int last) {  // 가운데 직선이 아래 껍질에 불필요한지 확인
    return (intercept[middle] - intercept[first]) * (slope[middle] - slope[last]) >= (intercept[last] - intercept[middle]) * (slope[first] - slope[middle]);  // 감소 기울기의 교점 순서를 정수 곱으로 비교
}  // 후보 제거 판정 끝
int main() {  // 단조 CHT로 DP 계산
    int n, queue[31], head = 0, tail = 1;  // 앞과 뒤에서 줄일 후보 덱
    long long cost, x[31] = {0}, dp[31] = {0};  // x0과 D0은0
    std::cin >> n >> cost;  // 상태 수와 매 전이의 상수 비용
    for (int i = 1; i <= n; ++i) std::cin >> x[i];  // 엄격 증가 좌표
    queue[0] = 0;  // 초기 직선 y=0
    for (int i = 1; i <= n; ++i) {  // 질의 x도 증가하는 순서
        while (tail - head >= 2 && evaluate(queue[head], x[i]) >= evaluate(queue[head + 1], x[i])) ++head;  // 앞으로도 불리한 앞 직선 제거
        dp[i] = x[i] * x[i] + cost + evaluate(queue[head], x[i]);  // 직선 최솟값과 공통 항 결합
        slope[i] = -2 * x[i];  // 새로운 상태의 감소 기울기
        intercept[i] = dp[i] + x[i] * x[i];  // 새로운 상태의 절편
        while (tail - head >= 2 && redundant(queue[tail - 2], queue[tail - 1], i)) --tail;  // 앞으로도 선택되지 않는 가운데 후보 제거
        queue[tail++] = i;  // 새 직선을 덱 뒤에 삽입
    }  // 모든 상태 계산 끝
    std::cout << dp[n] << "\n";  // 마지막 최적 비용
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/37-DP최적화와볼록껍질트릭_dp-optimization/example.py>)

```python
import sys  # 상태와 좌표 입력 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
n, cost = next(tokens), next(tokens)  # 전이 수와 상수 비용
x = [0] + [next(tokens) for _ in range(n)]  # 증가 좌표와 초기 x0
dp = [0] * (n + 1)  # 상태별 최적 비용
slope, intercept = [0] * (n + 1), [0] * (n + 1)  # 직선 계수
queue = [0] * (n + 1)  # 후보 덱의 배열 저장
head, tail = 0, 1  # 초기 직선0만 포함
def evaluate(line, coordinate):  # 한 직선의 현재 값
    return slope[line] * coordinate + intercept[line]  # 선형식 계산
def redundant(first, middle, last):  # 가운데 후보의 불필요성
    return (intercept[middle] - intercept[first]) * (slope[middle] - slope[last]) >= (intercept[last] - intercept[middle]) * (slope[first] - slope[middle])  # 감소 기울기의 교점 순서 비교
for i in range(1, n + 1):  # 증가하는 질의 좌표
    while tail - head >= 2 and evaluate(queue[head], x[i]) >= evaluate(queue[head + 1], x[i]):  # 뒤 직선이 더 낮은 경우
        head += 1  # 앞으로 불리한 앞 후보 제거
    dp[i] = x[i] * x[i] + cost + evaluate(queue[head], x[i])  # 직선 질의로 DP 전이
    slope[i] = -2 * x[i]  # 감소하는 새 기울기
    intercept[i] = dp[i] + x[i] * x[i]  # 새 상태의 절편
    while tail - head >= 2 and redundant(queue[tail - 2], queue[tail - 1], i):  # 아래 껍질에 필요 없는 후보
        tail -= 1  # 덱 뒤쪽에서 제거
    queue[tail] = i  # 새 직선 저장
    tail += 1  # 후보 범위 확장
print(dp[n])  # 마지막 상태의 최적값
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 좌표·DP·기울기·절편·후보 덱 각31칸을 사용하며 중간 곱은 long long입니다. | 같은 고정 배열 덱을 사용하며 기울기·교차 곱을 정수로 비교합니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: O(n) 상환
- 보조 공간: O(n)

기울기와 질의 좌표의 단조성으로 각 직선이 후보 덱에 한 번 들어가고 최대 한 번 제거됩니다.

[예제 입력](<예제_examples/37-DP최적화와볼록껍질트릭_dp-optimization/input.txt>) · [예상 출력](<예제_examples/37-DP최적화와볼록껍질트릭_dp-optimization/output.txt>) · [예제 실행 방법](<예제_examples/37-DP최적화와볼록껍질트릭_dp-optimization/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

현재 대표 보관 풀이에서 이 유형으로 직접 분류한 문제는 없습니다. 위의 자체 예제와 참고 자료로 원리를 익힐 수 있으며, 다른 알고리즘으로 푼 문제를 이 유형의 채점 사례로 표시하지 않습니다.

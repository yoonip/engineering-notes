# 수학적 규칙, 불변량과 구성적 풀이

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 계산을 줄이는 관점

입력을 직접 따라가면 많은 단계가 필요하지만, 결과를 결정하는 성질만 보면 짧게 풀리는 문제가 있습니다. 합, 나머지, 홀짝, 순서, 연결 요소 수처럼 연산 전후에 보존되거나 한 방향으로 바뀌는 값을 찾습니다. 수학 유형이라는 이름은 증명 없이 규칙을 추측해도 된다는 뜻이 아닙니다.

불변량은 허용된 연산을 해도 변하지 않는 값입니다. 단조량은 한 방향으로만 바뀌며, 잠재 함수는 진행이나 총작업량을 수치로 나타내는 도구입니다. 상태를 모두 나열하는 대신 가능한 결과를 제한하거나 종료를 보이는 데 사용합니다.

## 직접 구성한 홀짝 예제

정수 배열에서 두 원소에 각각 1을 더하는 연산만 가능하다고 둡니다. 전체 합은 매번 2씩 증가하므로 합의 홀짝은 보존됩니다. 시작 합이 짝수이고 목표 합이 홀수라면 도달할 수 없습니다.

이것은 필요조건입니다. 같은 홀짝이라고 항상 도달 가능한 것은 아닙니다. 예를 들어 원소를 줄일 수 없다는 제약도 남아 있습니다. 불변량 하나를 찾았다고 충분조건까지 얻었다고 결론내리지 않습니다.

격자의 상하좌우 이동에서는 행+열의 홀짝이 매번 바뀝니다. 정확히 k번 이동해 목표에 도착하려면 Manhattan 거리 d≤k와 k-d가 짝수라는 조건이 필요합니다. 남은 두 걸음을 왕복으로 쓸 수 있는 환경인지도 확인해야 충분조건을 말할 수 있습니다. 고립 정점이나 시간 제한 문이 있는 격자에서는 달라집니다.

## 구성적 풀이의 절차

최솟값 하나를 계산하는 대신 조건을 만족하는 실제 배열·순서·경로를 출력하는 문제가 있습니다. 이때는 다음 순서를 사용합니다.

1. 불가능한 입력의 필요조건을 먼저 찾습니다.
2. 답을 만드는 구체적인 규칙을 정의합니다.
3. 규칙이 모든 출력 조건을 지킨다는 것을 증명합니다.
4. 필요조건을 통과한 모든 입력에 대해 규칙이 끝까지 진행되는지 확인합니다.
5. 출력 크기와 구성 시간도 계산합니다.

자체 예제로 1부터 n까지를 인접 두 수의 차이가 항상 1이 되도록 배열하면 오름차순 구성이 바로 답입니다. 순환 배열로 마지막과 처음에도 차이 1을 요구하면 n>2에서 같은 구성이 실패합니다. 출력 조건 하나가 필요충분조건을 바꿉니다.

## 관찰을 증명으로 바꾸기

| 발견한 현상 | 확인할 논리 | 흔한 오류 |
| --- | --- | --- |
| 일정 주기로 답이 반복 | 같은 상태가 재등장해 이후 전이도 같음을 보입니다. | 앞부분 몇 값만 보고 주기를 추측합니다. |
| 작은 값부터 배치 가능 | 그 배치가 남은 선택의 가능성을 깨지 않음을 보입니다. | 정렬 자체를 증명으로 대신합니다. |
| 한 번 바꿀 때 값 감소 | 비음수 정수가 엄격히 감소하거나, 하한이 있는 값이 고정된 ε>0 이상씩 감소함을 보입니다. | 실수 값의 무한 감소도 유한 종료라고 생각합니다. |
| 대칭인 경우의 수 같음 | 대응이 일대일인지, 고정점이 있는지 확인합니다. | 가운데 원소까지 무조건 2로 나눕니다. |

반복문 검증에서는 초기 성립·한 단계 보존·종료 시 결론의 세 부분을 구별합니다. 반복 종료 자체는 감소하는 비음수 정수 같은 별도 근거가 필요할 수 있습니다. [Furia 등의 불변식 분석 논문](https://arxiv.org/abs/1211.4470)은 다양한 알고리즘에서 불변식이 어떤 역할을 하는지 분류합니다. 본문의 홀짝·격자 예시는 직접 구성했습니다.

## 자주 결합하는 수학 도구

등차·등비수열 합은 반복을 식으로 바꿉니다. 바닥 함수가 있는 합은 나눗셈의 몫이 같은 구간을 묶을 수 있습니다. 예를 들어 floor(n/i)=q인 구간의 끝은 floor(n/q)여서 서로 다른 몫의 수가 O(√n)입니다. 이것은 모든 정수론 문제의 자동 해법이 아니라 해당 합이 몫별로 같은 형태일 때의 묶음입니다.

좌표를 바꾸거나 원소를 정규화해도 필요한 답이 유지되는지 확인합니다. 최대공약수로 약분하면 비율이 같다는 정보를 보존할 수 있지만, 원래 길이의 제한이나 개수 가중치는 별도로 남겨야 합니다. 계산 결과가 부동소수점 근사에 민감하면 정수 교차 곱 비교를 검토하며 오버플로 범위까지 확인합니다.

## 실제 쓰임과 복습

프로토콜의 상태 전이, 회계 원장의 합 보존, 재고 이동 전후 총량, 자원 배분의 가능성 검사가 불변량 관점과 연결됩니다. 단순 합이 맞아도 개별 거래가 맞는 것은 아니므로 여러 독립 조건을 함께 확인합니다. 체크섬이나 해시의 충돌 가능성을 완전한 동일성 증명과 구분하는 것도 같은 태도입니다.

시간 복잡도는 발견한 규칙에 달려 있습니다. O(n) 반복을 수식으로 바꿔 O(1)개의 산술 연산으로 줄여도 큰 정수 연산과 출력 크기의 비용이 사라지는 것은 아닙니다.

복습: 작은 입력 100개에서 성립한 규칙과 불변량의 증명 중 무엇이 다른지 설명합니다. 답은 표본의 일치와 모든 허용 전이에 대한 보존 논리가 다르다는 점입니다. 표본은 반례를 찾는 데 도움을 주고, 증명은 전 범위의 결론을 지탱합니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

서로 다른 두 원소를 각각 1 올리는 연산으로 목표 배열을 만듭니다. 차이의 비음수성·합의 홀짝·최대 차이 조건을 검사하고 가장 큰 두 부족량을 줄이며 실제 연산을 출력합니다.

이 예제에서 직접 구현하는 기법은 합의 홀짝 불변량 · 비음수성 · 구성적 풀이 · 감소하는 정수 부족량입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

N, 초기 배열 A, 목표 배열 B가 차례로 주어집니다. 2≤N≤6이고 각 원소는 0~6입니다. 한 연산은 서로 다른 두 인덱스의 값을 각각 1 올립니다.

```text
3
0 0 0
2 1 1
```

불가능하면 IMPOSSIBLE입니다. 가능하면 POSSIBLE K 뒤에 K줄의 0기반 인덱스 쌍을 출력합니다. 최댓값 동률은 작은 인덱스부터 고릅니다.

```text
POSSIBLE 2
0 1
0 2
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | deficit=[2,1,1], total=4, largest=2 | 증가량이 모두 비음수이고 합이 짝수인지 확인합니다. |
| 2 | 2*largest=4≤total=4 | 가장 큰 부족량도 다른 위치의 부족량과 모두 짝지을 수 있습니다. |
| 3 | 연산(0,1) 후 deficit=[1,0,1] | 큰 두 부족량을 줄여 짝짓기 가능 조건을 보존합니다. |
| 4 | 연산(0,2) 후 deficit=[0,0,0] | 초기 배열에서 두 번 증가하면 목표 배열에 도달합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/39-수학적규칙과구성적풀이_invariants-constructive/example.c>)

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


int main(void) {  // 불변량 검사 후 실제 증가 연산 구성
    int n = read_int(), initial[6], deficit[6];  // 배열 길이·초기값·남은 부족량
    for (int i = 0; i < n; ++i) initial[i] = read_int();  // 초기 배열 입력
    int total = 0, largest = 0, possible = 1;  // 부족량 합·최댓값·가능 여부
    for (int i = 0; i < n; ++i) {  // 목표와의 차이 계산
        deficit[i] = read_int() - initial[i];  // 이 위치에서 더해야 할 양
        if (deficit[i] < 0) possible = 0;  // 감소 연산이 없으므로 음수 차이는 불가능
        total += deficit[i];  // 한 연산이 2 줄일 총부족량
        if (deficit[i] > largest) largest = deficit[i];  // 한 위치의 최대 부족량
    }  // 부족량 집계 끝
    if (!possible || total % 2 || 2 * largest > total) { write_text("IMPOSSIBLE\n"); return 0; }  // 다른 위치와 짝지을 수 있는 조건 검사
    int steps = total / 2;  // 모든 연산은 합을 정확히 2 올림
    write_text("POSSIBLE "); write_number(steps); write_text("\n");  // 구성할 연산 수 먼저 출력
    for (int step = 0; step < steps; ++step) {  // 부족량이 모두 0이 될 때까지 구성
        int first = -1, second = -1;  // 가장 큰 두 부족량의 위치
        for (int i = 0; i < n; ++i) {  // 작은 인덱스부터 동률 처리
            if (first == -1 || deficit[i] > deficit[first]) { second = first; first = i; }  // 새 최댓값을 첫 후보로
            else if (second == -1 || deficit[i] > deficit[second]) second = i;  // 나머지 중 두 번째 후보
        }  // 서로 다른 두 위치 선택 끝
        --deficit[first]; --deficit[second];  // 선택한 두 위치의 목표 부족량을 1씩 줄이기
        write_number(first); write_text(" "); write_number(second); write_text("\n");  // 실제 증가 연산 출력
    }  // 목표까지의 구성 끝
    return 0;  // 정상 종료
}  // 불변량·구성 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/39-수학적규칙과구성적풀이_invariants-constructive/example.cpp>)

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


int main(void) {  // 불변량 검사 후 실제 증가 연산 구성
    int n = read_int(), initial[6], deficit[6];  // 배열 길이·초기값·남은 부족량
    for (int i = 0; i < n; ++i) initial[i] = read_int();  // 초기 배열 입력
    int total = 0, largest = 0, possible = 1;  // 부족량 합·최댓값·가능 여부
    for (int i = 0; i < n; ++i) {  // 목표와의 차이 계산
        deficit[i] = read_int() - initial[i];  // 이 위치에서 더해야 할 양
        if (deficit[i] < 0) possible = 0;  // 감소 연산이 없으므로 음수 차이는 불가능
        total += deficit[i];  // 한 연산이 2 줄일 총부족량
        if (deficit[i] > largest) largest = deficit[i];  // 한 위치의 최대 부족량
    }  // 부족량 집계 끝
    if (!possible || total % 2 || 2 * largest > total) { write_text("IMPOSSIBLE\n"); return 0; }  // 다른 위치와 짝지을 수 있는 조건 검사
    int steps = total / 2;  // 모든 연산은 합을 정확히 2 올림
    write_text("POSSIBLE "); write_number(steps); write_text("\n");  // 구성할 연산 수 먼저 출력
    for (int step = 0; step < steps; ++step) {  // 부족량이 모두 0이 될 때까지 구성
        int first = -1, second = -1;  // 가장 큰 두 부족량의 위치
        for (int i = 0; i < n; ++i) {  // 작은 인덱스부터 동률 처리
            if (first == -1 || deficit[i] > deficit[first]) { second = first; first = i; }  // 새 최댓값을 첫 후보로
            else if (second == -1 || deficit[i] > deficit[second]) second = i;  // 나머지 중 두 번째 후보
        }  // 서로 다른 두 위치 선택 끝
        --deficit[first]; --deficit[second];  // 선택한 두 위치의 목표 부족량을 1씩 줄이기
        write_number(first); write_text(" "); write_number(second); write_text("\n");  // 실제 증가 연산 출력
    }  // 목표까지의 구성 끝
    return 0;  // 정상 종료
}  // 불변량·구성 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/39-수학적규칙과구성적풀이_invariants-constructive/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n = int(next(tokens))  # 배열 길이
    initial = [int(next(tokens)) for _ in range(n)]  # 초기 배열
    target = [int(next(tokens)) for _ in range(n)]  # 목표 배열
    deficit = [b - a for a, b in zip(initial, target)]  # 위치별 필요한 증가량
    total = sum(deficit)  # 한 연산마다 2 줄일 전체 부족량
    if min(deficit) < 0 or total % 2 or 2 * max(deficit) > total:  # 감소 불가·홀짝·짝짓기 조건 검사
        print("IMPOSSIBLE")  # 목표에 도달할 수 없는 경우
        return  # 구성을 시작하지 않고 종료
    steps = total // 2  # 필요한 증가 연산 수
    print("POSSIBLE", steps)  # 연산 수를 포함한 결과 머리
    for _ in range(steps):  # 가장 큰 두 부족량을 반복해서 줄이기
        first = second = -1  # 서로 다른 두 후보 위치
        for i in range(n):  # 작은 인덱스부터 동률 처리
            if first == -1 or deficit[i] > deficit[first]:  # 더 큰 부족량 발견
                second, first = first, i  # 기존 첫 후보를 두 번째로 이동
            elif second == -1 or deficit[i] > deficit[second]:  # 두 번째로 큰 부족량 확인
                second = i  # 두 번째 위치 갱신
        deficit[first] -= 1  # 첫 위치를 실제로 1 올린 효과
        deficit[second] -= 1  # 둘째 위치를 실제로 1 올린 효과
        print(first, second)  # 선택한 연산 출력

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

- 시간: O(N+NS)
- 보조 공간: O(N)

S는 초기 부족량 합이며 S/2번 연산마다 N개 후보를 확인합니다. 모든 부족량이 비음수이고 최대값이 나머지 합 이하이면 큰 두 값을 줄인 뒤에도 이 조건이 유지됩니다.

[예제 입력](<예제_examples/39-수학적규칙과구성적풀이_invariants-constructive/input.txt>) · [예상 출력](<예제_examples/39-수학적규칙과구성적풀이_invariants-constructive/output.txt>) · [예제 실행 방법](<예제_examples/39-수학적규칙과구성적풀이_invariants-constructive/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 0 | 120922 종이 자르기 | [C](<../C/level0/extra_120922_종이_자르기/README.md>) | [C++](<../C++/level0/extra_120922_종이_자르기/README.md>) | [Python](<../Python/level0/extra_120922_종이_자르기/README.md>) |
| 1 | 134240 푸드 파이트 대회 | [C](<../C/level1/extra_134240_푸드_파이트_대회/README.md>) | [C++](<../C++/level1/extra_134240_푸드_파이트_대회/README.md>) | [Python](<../Python/level1/extra_134240_푸드_파이트_대회/README.md>) |
| 2 | 258711 도넛과 막대 그래프 | [C](<../C/level2/011_258711_도넛과_막대_그래프/README.md>) | [C++](<../C++/level2/011_258711_도넛과_막대_그래프/README.md>) | [Python](<../Python/level2/011_258711_도넛과_막대_그래프/README.md>) |
| 3 | 388354 홀짝트리 | [C](<../C/level3/009_388354_홀짝트리/README.md>) | [C++](<../C++/level3/009_388354_홀짝트리/README.md>) | [Python](<../Python/level3/009_388354_홀짝트리/README.md>) |
| 4 | 389630 격자 뒤집기 미로 | [C](<../C/level4/extra_389630_격자_뒤집기_미로/README.md>) | [C++](<../C++/level4/extra_389630_격자_뒤집기_미로/README.md>) | [Python](<../Python/level4/extra_389630_격자_뒤집기_미로/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/invariants.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

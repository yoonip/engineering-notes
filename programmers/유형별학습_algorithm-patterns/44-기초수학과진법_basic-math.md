# 기초 수학과 진법, 정수 경계 계산

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 식으로 표현하는 기초

배열·문자열을 다루기 전에 합, 비율, 자리값, 몫과 나머지를 정확히 표현하는 문제가 있습니다. 계산식이 짧아도 무엇을 세고 어떤 순서로 계산하는지가 중요합니다. 이 유형은 소수·약수·합동식 중심의 정수론과 구별해 기초 산술을 다룹니다.

총량에서 부분을 빼거나, 같은 크기 묶음으로 나누거나, 반복되는 증가량을 수열로 표현합니다. 먼저 단위와 범위를 맞추면 복잡한 조건문을 줄일 수 있습니다. 시간은 시·분을 정수 분 또는 초로 통일한 뒤 계산하고 마지막에 표시 형식으로 되돌릴 수 있습니다.

## 몫과 나머지, 올림과 내림

양의 정수 n개를 한 묶음에 k개씩 담으면 완전한 묶음은 n//k, 남는 개수는 n%k입니다. 모두 담을 묶음 수는 n//k+(n%k!=0)입니다. 흔한 (n+k-1)//k도 같은 값이지만 C/C++에서는 덧셈이 범위를 넘는지 확인합니다.

직접 구성한 17개를 5개씩 담는 예제에서는 3묶음과 2개가 남으므로 모두 담으려면 4묶음입니다. 총부피를 나누는 것만으로 입체 물건이 공간에 들어간다고 결론내릴 수는 없습니다. 방향별로 들어가는 개수를 계산해야 하는 문제와 구별합니다.

음수에도 같은 공식을 쓰려면 나눗셈의 정의를 맞춰야 합니다. Python //는 내림이고 C/C++ 정수 나눗셈은 0 방향입니다. 예를 들어 -3/2의 정수 몫이 달라져 음수 좌표의 구간 개수 계산이 틀릴 수 있습니다. [언어별 구현 비교](40-C와CPP와Python구현비교_language-implementation.md)와 함께 확인합니다.

## 자리값과 진법 변환

밑 b의 정수에서 n%b는 가장 낮은 자리이고 n//b는 그 자리를 제거한 앞부분입니다. 이 과정을 반복하면 낮은 자리부터 얻습니다. 반대로 높은 자리부터 읽는다면 value=value*b+digit으로 누적합니다.

자체 예제로 13을 2진수로 바꾸면 나머지가 1,0,1,1 순서로 나와 뒤집은 1101이 됩니다. 1101을 다시 읽으면 1→3→6→13으로 누적합니다. 정수 0도 표현상 한 자리 0이므로 while n만으로 처리하면 빈 결과가 되는 경계를 따로 봅니다.

고정 개수 자리씩 나눌 수도 있습니다. 123456을 오른쪽 두 자리씩 나누면 밑 100에서 56,34,12를 얻습니다. 숫자 문자열이 매우 길면 전체를 정수로 바꿀 필요 없이 자리별 누적이나 나머지만 유지합니다.

~~~python
def remainder_of_digits(text, modulus):  # 십진 숫자열의 값을 만들지 않고 나머지 계산
    result = 0  # 아직 읽은 자리가 없을 때의 나머지
    for ch in text:  # 높은 자리부터 문자 하나씩 읽기
        digit = ord(ch) - ord('0')  # 숫자 문자를 0~9 정수로 변환
        result = (result * 10 + digit) % modulus  # 다음 자리를 붙인 값의 나머지만 유지
    return result  # 전체 정수를 modulus로 나눈 나머지 반환
~~~

입력이 0~9 문자이고 modulus가 양수라는 전제입니다. 읽은 접두사의 실제 값과 result가 같은 나머지를 가진다는 불변식을 초기화와 한 자리 확장으로 증명합니다. 자릿수 D에 대해 작은 고정 범위 정수 연산 모형에서 O(D) 시간과 O(1) 보조 공간입니다.

## 수열·비율과 정확한 계산

연속 정수 a부터 b까지의 개수는 b-a+1이고 합은 (a+b)(b-a+1)/2입니다. 양끝을 짝지으면 각 쌍의 합이 같다는 이유로 유도합니다. 빈 구간이나 a>b를 허용하는지 먼저 정합니다. 등비수열 합의 식은 공비가 1인 경우를 따로 처리합니다.

할인 후 금액을 버림 처리하는 문제에서는 정수 곱셈 후 나눗셈으로 표현할 수 있습니다. 나누고 곱하는 순서를 바꾸면 중간의 버림 때문에 값이 달라집니다. 자체 예제로 199의 90%를 정수로 버리면 179이지만, 199//100*90은 90입니다.

두 분수 a/b와 c/d는 분모가 양수이면 ad와 cb를 비교해 순서를 구할 수 있습니다. 부호가 섞이면 부등호 방향과 분모 0을 먼저 처리합니다. C/C++에서는 교차 곱의 범위도 계산해야 합니다. 실수 제곱근의 반올림에 의존한 정수 판정 대신 정수 제곱근을 쓰는 방법은 [Python math.isqrt 공식 문서](https://docs.python.org/3/library/math.html#math.isqrt)에서 확인할 수 있습니다.

## 중요성과 실제 연결

페이지 수·버퍼 블록 수·패킷 분할 수·시간 표시 변환과 비용 계산의 기본 모형에 연결됩니다. 실제 금전 계산은 통화 단위와 반올림 규칙을 명시해야 하며 코딩 문제의 버림 규칙을 모든 업무 규칙으로 확대하지 않습니다. 화면상 십진수와 내부 이진 부동소수점 표현의 차이도 확인합니다.

짧은 식은 반복문을 줄이지만 식 자체가 성립하는 범위가 핵심입니다. 아주 큰 정수에서는 곱셈·나눗셈 비용이 자릿수에 따라 달라지므로 O(1)개의 연산과 O(1) 실행 시간을 혼동하지 않습니다.

## 복습

복습: 소수점 이하를 버려야 하는 비율 계산에서 곱셈을 나눗셈 앞으로 옮기는 이유를 설명합니다. 답은 중간 단계에서 필요한 정밀도를 버리지 않기 위해서입니다. 다만 먼저 곱한 값이 자료형 범위를 넘으면 넓은 정수나 다른 안전한 식이 필요합니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

밑 2~16의 숫자 문자열을 전체 정수로 바꾸지 않고 자리값의 나머지만 누적합니다. 큰 정수 전체 변환이나 소수 판정은 구현하지 않습니다.

이 예제에서 직접 구현하는 기법은 진법의 자리값 · Horner 형태 누적 · 모듈러 불변량 · 문자 자릿값 변환입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

밑 B, 양의 나누는 수 M, 숫자 문자열이 차례로 주어집니다. 2≤B≤16, 1≤M≤1000, 길이는 1~32입니다. 0~9와 대문자 A~F만 사용하며 각 자릿값은 B보다 작습니다.

```text
16 7 1A
```

해당 B진수 정수를 M으로 나눈 나머지를 한 줄에 출력합니다.

```text
5
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | base=16, modulus=7, remainder=0 | 빈 접두사의 나머지를 0으로 둡니다. |
| 2 | 문자 1: digit=1, remainder=(0*16+1)%7=1 | 첫 자릿값을 붙인 나머지입니다. |
| 3 | 문자 A: digit=10, remainder=(1*16+10)%7=5 | 16진수의 A를 10으로 해석합니다. |
| 4 | 1A₁₆=26, 26%7=5 | 직접 작은 정수로 계산한 결과와 누적 결과가 같습니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/44-기초수학과진법_basic-math/example.c>)

```c
#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    scanf("%32s", text);  // 종료 문자까지 들어갈 33칸 버퍼 사용
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int digit_value(char ch) {  // 숫자 문자 한 개를 자릿값으로 해석
    if (ch >= '0' && ch <= '9') return ch - '0';  // 십진 숫자의 자릿값
    return ch - 'A' + 10;  // 대문자 A~F를 10~15로 변환
}  // 자릿값 변환 함수 끝
int main(void) {  // 자리값의 나머지 누적
    int base = read_int(), modulus = read_int();  // 진법의 밑과 양의 나누는 수
    char text[33]; read_word(text);  // 최대 32자리와 종료 문자
    int remainder = 0;  // 빈 접두사의 나머지
    for (int i = 0; text[i] != '\0'; ++i) {  // 높은 자리부터 차례로 읽기
        int digit = digit_value(text[i]);  // 현재 숫자의 자릿값
        remainder = (remainder * base + digit) % modulus;  // 다음 자리를 붙인 값의 나머지만 유지
    }  // 모든 자릿값 누적 끝
    write_number(remainder); write_text("\n");  // 전체 수의 나머지 출력
    return 0;  // 정상 종료
}  // 진법·나머지 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/44-기초수학과진법_basic-math/example.cpp>)

```cpp
#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    cin.width(33);  // 종료 문자를 포함한 버퍼 크기로 읽기 제한
    cin >> text;  // 공백 전까지의 토큰 읽기
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    cout << value;  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int digit_value(char ch) {  // 숫자 문자 한 개를 자릿값으로 해석
    if (ch >= '0' && ch <= '9') return ch - '0';  // 십진 숫자의 자릿값
    return ch - 'A' + 10;  // 대문자 A~F를 10~15로 변환
}  // 자릿값 변환 함수 끝
int main(void) {  // 자리값의 나머지 누적
    int base = read_int(), modulus = read_int();  // 진법의 밑과 양의 나누는 수
    char text[33]; read_word(text);  // 최대 32자리와 종료 문자
    int remainder = 0;  // 빈 접두사의 나머지
    for (int i = 0; text[i] != '\0'; ++i) {  // 높은 자리부터 차례로 읽기
        int digit = digit_value(text[i]);  // 현재 숫자의 자릿값
        remainder = (remainder * base + digit) % modulus;  // 다음 자리를 붙인 값의 나머지만 유지
    }  // 모든 자릿값 누적 끝
    write_number(remainder); write_text("\n");  // 전체 수의 나머지 출력
    return 0;  // 정상 종료
}  // 진법·나머지 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/44-기초수학과진법_basic-math/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    base, modulus = int(next(tokens)), int(next(tokens))  # 진법과 양의 나누는 수
    text = next(tokens)  # 전체 정수로 바꾸지 않을 숫자 문자열
    remainder = 0  # 빈 접두사의 나머지
    for ch in text:  # 높은 자리부터 순서대로 읽기
        digit = ord(ch) - ord("0") if "0" <= ch <= "9" else ord(ch) - ord("A") + 10  # 숫자·대문자를 자릿값으로 변환
        remainder = (remainder * base + digit) % modulus  # 이전 접두사에 한 자리 붙인 나머지
    print(remainder)  # 전체 진법 숫자의 나머지

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

- 시간: O(D)
- 보조 공간: 입력 포함 O(D), 누적 상태 O(1)

D개 자리를 한 번씩 읽으며 중간값은 최대 999×16+15이므로 명시한 범위에서 작은 정수 연산입니다.

[예제 입력](<예제_examples/44-기초수학과진법_basic-math/input.txt>) · [예상 출력](<예제_examples/44-기초수학과진법_basic-math/output.txt>) · [예제 실행 방법](<예제_examples/44-기초수학과진법_basic-math/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 0 | 340206 [PCCE 기출문제] 2번 / 각도 합치기 | — | [C++](<../C++/level0/extra_340206_[PCCE_기출문제]_2번___각도_합치기/README.md>) | [Python](<../Python/level0/extra_340206_[PCCE_기출문제]_2번___각도_합치기/README.md>) |
| 1 | 155652 둘만의 암호 | [C](<../C/level1/extra_155652_둘만의_암호/README.md>) | [C++](<../C++/level1/extra_155652_둘만의_암호/README.md>) | [Python](<../Python/level1/extra_155652_둘만의_암호/README.md>) |
| 2 | 181187 두 원 사이의 정수 쌍 | [C](<../C/level2/015_181187_두_원_사이의_정수_쌍/README.md>) | [C++](<../C++/level2/015_181187_두_원_사이의_정수_쌍/README.md>) | [Python](<../Python/level2/015_181187_두_원_사이의_정수_쌍/README.md>) |
| 3 | 389481 봉인된 주문 | [C](<../C/level3/008_389481_봉인된_주문/README.md>) | [C++](<../C++/level3/008_389481_봉인된_주문/README.md>) | [Python](<../Python/level3/008_389481_봉인된_주문/README.md>) |
| 5 | 76504 RPG와 쿼리 | [C](<../C/level5/014_76504_RPG와_쿼리/README.md>) | [C++](<../C++/level5/014_76504_RPG와_쿼리/README.md>) | [Python](<../Python/level5/revisit_20261024/012_76504_RPG와_쿼리/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/basic-math.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

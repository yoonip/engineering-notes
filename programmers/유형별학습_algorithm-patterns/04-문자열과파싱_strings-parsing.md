# 문자열과 파싱

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 문자 나열과 구조 있는 입력

문자열 처리는 문자를 읽고 바꾸는 작업이고, 파싱은 그 나열을 규칙에 맞는 구조로 해석하는 작업입니다.
`12+3*4`에서 문자를 나누는 일과 곱셈을 먼저 묶는 일은 다른 단계입니다.
일반적으로 문자 입력, 토큰, 구조, 의미 검사 순서로 나누면 오류 위치를 찾기 쉽습니다.
토큰은 정수, 이름, 구분자처럼 문법에서 하나로 취급하는 단위입니다.

이 구분이 중요한 이유는 단순한 분리 함수로 해결할 수 있는 형식과 그렇지 않은 형식을 가르기 때문입니다.
예를 들어 쉼표가 따옴표 안에도 나올 수 있으면 쉼표마다 무조건 나누는 방식은 형식을 보존하지 않습니다.

## 인식 단서와 적용 조건

“공백으로 구분된 정수”는 보통 분리 후 정수 변환으로 충분합니다.
중첩 괄호, 이스케이프, 따옴표, 연산자 우선순위가 있으면 현재 해석 상태를 저장해야 합니다.
특정 문자열 패턴이 반복되는지를 찾는 문제와 입력 전체가 문법에 맞는지를 검사하는 문제도 구별합니다.
정규식의 부분 검색이 성공했다고 입력 전체가 유효한 것은 아닙니다.
Python은 전체 일치를 검사하는 `fullmatch`를 별도 연산으로 제공합니다. [Python re, fullmatch](https://docs.python.org/3/library/re.html#re.fullmatch)

JSON처럼 이미 표준 문법이 있는 입력은 전용 파서를 사용할 수 있는지 먼저 확인합니다.
Python `json.loads`는 JSON 텍스트를 객체로 해석하고 잘못된 문법에 대해 해석 오류를 보고합니다. [Python json, Decoding·Exceptions](https://docs.python.org/3/library/json.html)

## 직접 구성한 예제: 구분자 안의 구분자

입력 `name="Kim, Min",age=17`을 키·값 목록으로 읽는다고 가정합니다.
이 예제에서는 큰따옴표로 감싼 값 안의 쉼표를 필드 경계로 보지 않으며 이스케이프는 지원하지 않습니다.
필요한 상태는 현재 위치, 따옴표 안 여부, 현재 필드 시작 위치입니다.

| 읽은 문자 또는 구간 | 따옴표 안 여부 | 처리 |
|---|---|---|
| name= | 거짓 | 현재 필드에 포함 |
| 첫 큰따옴표 | 참으로 전환 | 인용 값 시작 |
| Kim, Min | 참 | 쉼표도 값의 일부 |
| 닫는 큰따옴표 | 거짓으로 전환 | 인용 값 종료 |
| 다음 쉼표 | 거짓 | 첫 필드 확정 |
| age=17 | 거짓 | 마지막 필드 확정 |

일반 CSV나 다른 데이터 형식까지 처리하려면 이 예제의 규칙을 임의로 확대하지 말고 해당 형식의 문법을 확인해야 합니다.

## 단순한 구분 파서의 코드

다음 코드는 위에서 정한 제한된 문법의 필드 분리만 수행합니다.

```python
def fields(text):  # 함수 정의로 제한된 형식의 필드 분리 연산 묶기
    result, start, quoted = [], 0, False  # 결과·현재 필드 시작·인용 상태 초기화
    for index, character in enumerate(text):  # 위치와 문자를 함께 순회
        if character == '"':  # 큰따옴표를 만났는지 비교
            quoted = not quoted  # 인용 영역의 시작과 끝을 토글
        elif character == "," and not quoted:  # 인용 영역 밖의 쉼표만 경계로 판정
            result.append(text[start:index])  # 슬라이스로 완성된 필드를 결과에 저장
            start = index + 1  # 다음 필드의 첫 위치로 이동
    if quoted:  # 입력 끝에서도 인용 상태가 남았는지 검사
        raise ValueError("닫히지 않은 따옴표")  # 예외로 잘못된 제한 문법 입력 보고
    result.append(text[start:])  # 마지막 쉼표 뒤의 필드도 빠짐없이 추가
    return result  # 분리한 필드 목록 반환
```

빈 필드, 키 중복, `=` 존재 여부와 값의 자료형 검사는 이 함수 다음 단계의 책임입니다.
문법 단계와 의미 검사를 섞지 않으면 어떤 오류를 어디서 거부할지 명확해집니다.

## 정당성의 불변식

각 문자를 읽기 전 `quoted`는 앞선 접두 구간에서 아직 닫히지 않은 인용의 존재 여부입니다.
구분자로 확정한 쉼표는 모두 이 상태가 거짓일 때의 쉼표입니다.
따라서 인용 값 내부를 잘못 나누지 않고, 인용 밖의 모든 쉼표는 정확히 한 번 경계가 됩니다.
마지막 접미 구간을 따로 추가해야 끝 구분자가 없는 정상 입력도 보존합니다.

## 비용과 문자열 단위

문자 수를 L이라 하면 상태 스캔은 O(L)입니다.
각 필드를 한 번씩 복사하며 복사되는 문자 길이의 총합도 O(L)이므로 전체 시간·출력 공간은 O(L)입니다.
반복 중 매번 전체 문자열을 새로 이어 붙이면 복사 누적으로 O(L²)이 될 수 있습니다.
인덱스를 저장해 마지막에 필요한 구간만 만들거나 조각을 모아 합치는 방식과 비교합니다.

C의 일반적인 `char` 문자열은 바이트열과 끝 표시를 직접 관리합니다.
C++ `string`도 문자 인코딩을 해석하는 규칙까지 자동으로 제공하는 것은 아닙니다.
Python `str`는 Unicode 문자 코드 기반 시퀀스이며 바이트열 `bytes`와 구별합니다. [Python Text Sequence Type](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
사용자가 눈으로 한 글자로 보는 단위와 코드 단위가 항상 같은지도 별도로 확인해야 합니다.

## 실전의 적용 조건

로그 수집에서는 필드 구분뿐 아니라 인코딩, 잘린 입력, 잘못된 숫자, 시간 형식을 정의해야 합니다.
설정 파일에서는 키를 인식한 다음 허용 범위와 필수 키를 검사하는 단계가 필요합니다.
중첩 수식을 해석할 때는 괄호 깊이와 연산자 우선순위를 유지하는 스택이나 문법 기반 파서가 적절합니다.
이 예시는 처리 단계의 구분이며 특정 로그 제품의 내부 파서를 설명하지 않습니다.

## 실수와 반례

- 빈 문자열을 분리한 결과와 필드가 없는 입력의 의미는 문법에 따라 다릅니다.
- 음수 앞의 `-`와 뺄셈 연산자 `-`는 문맥에 따라 다른 토큰일 수 있습니다.
- 문자열을 모두 소문자로 바꾸면 대소문자가 의미 있는 식별자를 잘못 합칠 수 있습니다.
- 정규식이나 사용자 입력을 `eval` 같은 코드 실행 수단에 그대로 전달하는 것은 파싱과 다른 작업입니다.

## 연계 유형

[스택](07-스택큐덱_stack-queue-deque.md)은 괄호와 중첩 구조를 처리하는 데 연결됩니다.
[해시](06-해시와빈도집계_hashing-counting.md)는 해석한 이름을 값과 연결하고, [시뮬레이션](02-구현과시뮬레이션_implementation-simulation.md)은 명령 실행을 담당합니다.

## 복습 질문과 답

질문 1. 쉼표로 나누기만 하면 안 되는 입력은 무엇입니까?

답. 인용 값이나 이스케이프 규칙 안에서 쉼표가 데이터로 쓰이는 입력입니다.

질문 2. 정규식 부분 검색과 전체 문법 검사의 차이는 무엇입니까?

답. 부분 검색은 일부 구간만 맞아도 성공할 수 있지만 전체 검사는 입력 끝까지 규칙을 만족해야 합니다.

## 근거와 예제 범위

Python 공식 문서는 문자열·정규식·JSON API의 의미를 확인하는 근거입니다.
필드 문법, 상태 추적, 파서와 비용 분석은 직접 구성했으며 일반 CSV 파서의 완전한 구현이 아닙니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

한 줄을 문자 위치로 순회하며 공백·부호·숫자·구분자를 해석해 정수의 개수와 합을 구합니다.

이 예제에서 직접 구현하는 기법은 문자열 스캔 · 토큰 파싱 · 부호와 자리값입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

길이 1~100인 ASCII 한 줄입니다. 콤마로 구분한 정수 1~10개이며 각 값은 −1000~1000입니다. 부호 +/−와 숫자 앞뒤의 ASCII 공백을 허용하고 마지막 콤마와 잘못된 토큰은 없습니다.

```text
12,-3,7
```

정수 개수와 정수 합을 한 줄에 출력합니다.

```text
3 16
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | position=0,count=0,total=0 | 첫 정수의 시작에서 스캔을 시작합니다. |
| 2 | 12 해석 뒤 position=2,count=1,total=12 | 십진수 자리값을 누적하고 콤마를 만납니다. |
| 3 | −3 해석 뒤 position=5,count=2,total=9 | 음수 부호를 현재 정수에만 적용합니다. |
| 4 | 7 해석 뒤 position=7,count=3,total=16 | 끝 표시를 만나 결과를 확정합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/04-문자열과파싱_strings-parsing/example.c>)

```c
#include <stdio.h> // 한 줄 입력과 결과 출력
int main(void) { // 실행 시작점
    char text[102]; // 최대 100문자와 줄바꿈·끝 표시 공간
    fgets(text, sizeof(text), stdin); // 콤마가 포함된 입력 줄 읽기
    int position = 0, count = 0; long long total = 0; // 스캔 위치·정수 수·합 초기화
    while (1) { // 정수 토큰 하나씩 해석
        while (text[position] == ' ') ++position; // 토큰 앞의 ASCII 공백 건너뛰기
        int sign = 1, number = 0; // 기본 양수 부호와 현재 정수 초기화
        if (text[position] == '+' || text[position] == '-') { // 선택적 부호 검사
            if (text[position] == '-') sign = -1; // 음수 부호 반영
            ++position; // 부호 다음 숫자로 이동
        } // 부호 처리 끝
        while ('0' <= text[position] && text[position] <= '9') { // 연속된 십진수 숫자 읽기
            number = number * 10 + text[position] - '0'; ++position; // 자리값을 누적하고 다음 문자로 이동
        } // 정수 한 개 해석 끝
        total += sign * number; ++count; // 정수의 합과 개수 갱신
        while (text[position] == ' ') ++position; // 정수 뒤 공백 건너뛰기
        if (text[position] != ',') break; // 콤마가 없으면 마지막 토큰 처리 완료
        ++position; // 구분자 다음 토큰으로 이동
    } // 전체 줄 파싱 끝
    printf("%d %lld\n", count, total); // 읽은 정수 수와 합 출력
    return 0; // 정상 종료
} // 제한된 콤마 문법 파싱 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/04-문자열과파싱_strings-parsing/example.cpp>)

```cpp
#include <iostream> // 표준 입출력
#include <string> // 줄 전체 문자열 저장
using namespace std; // 표준 이름 접두사 생략
int main() { // 실행 시작점
    string text; getline(cin, text); // 공백을 포함한 한 줄 읽기
    text.push_back('\0'); // 마지막 숫자 뒤 검사에 쓸 끝 표시 추가
    int position = 0, count = 0; long long total = 0; // 위치·개수·합 초기화
    while (true) { // 정수 토큰을 하나씩 처리
        while (text[position] == ' ') ++position; // 앞 공백 건너뛰기
        int sign = 1, number = 0; // 부호와 현재 값 준비
        if (text[position] == '+' || text[position] == '-') { // 선택적 부호 확인
            if (text[position] == '-') sign = -1; // 음수 부호 저장
            ++position; // 숫자가 시작되는 위치로 이동
        } // 부호 처리 끝
        while ('0' <= text[position] && text[position] <= '9') { // 연속된 숫자 순회
            number = number * 10 + text[position] - '0'; ++position; // 자리값을 누적하며 위치 전진
        } // 한 정수의 숫자 읽기 끝
        total += sign * number; ++count; // 합과 토큰 개수 갱신
        while (text[position] == ' ') ++position; // 뒤 공백 건너뛰기
        if (text[position] != ',') break; // 구분자가 없으면 줄 해석 종료
        ++position; // 다음 정수로 이동
    } // 모든 토큰 처리 끝
    cout << count << ' ' << total << '\n'; // 개수와 합 출력
    return 0; // 정상 종료
} // 제한된 콤마 문법 파싱 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/04-문자열과파싱_strings-parsing/example.py>)

```python
import sys # 한 줄 문자열 입력
text = sys.stdin.readline().rstrip('\n') + '\0' # 줄바꿈을 제거하고 검사할 끝 표시 추가
position = count = total = 0 # 스캔 위치·정수 개수·합 초기화
while True: # 토큰이 끝날 때까지 정수 하나씩 해석
    while text[position] == ' ': # 토큰 앞 공백 검사
        position += 1 # 공백 다음 위치로 이동
    sign, number = 1, 0 # 기본 양수 부호와 현재 정수 초기화
    if text[position] in '+-': # 선택적 부호 검사
        sign = -1 if text[position] == '-' else 1 # 문자에 맞는 부호 저장
        position += 1 # 부호 뒤 숫자로 이동
    while '0' <= text[position] <= '9': # 연속된 십진수 숫자 읽기
        number = number * 10 + ord(text[position]) - ord('0') # 기존 자리값에 새 숫자 추가
        position += 1 # 다음 문자로 이동
    total += sign * number # 해석한 정수를 전체 합에 반영
    count += 1 # 읽은 정수 개수 증가
    while text[position] == ' ': # 토큰 뒤 공백 검사
        position += 1 # 다음 구분자 위치로 이동
    if text[position] != ',': # 구분자가 없으면 마지막 정수인지 확인
        break # 전체 줄 해석 종료
    position += 1 # 콤마 뒤 다음 정수로 이동
print(count, total) # 정수 개수와 합 출력
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 입력 | fgets로 공백과 부호를 포함한 한 줄을 읽습니다. | getline으로 한 줄을 읽고 검사할 끝 표시를 추가합니다. | readline으로 한 줄을 읽고 줄바꿈을 제거한 뒤 끝 표시를 추가합니다. |
| 저장과 연산 | fgets로 읽은 char 배열에서 끝 표시를 검사합니다. | getline의 string 끝에 검사할 끝 표시를 붙입니다. | 한 줄 문자열과 ord로 숫자의 자리값을 계산합니다. |
| 자료형과 범위 | int 범위 안의 값만 사용하며 합은 long long으로 누적합니다. | int 범위 안의 값만 사용하며 합은 long long으로 누적합니다. | int로 정수를 저장합니다. 허용 입력 범위는 C·C++ 예제와 같습니다. |

### 예제의 비용과 실행 파일

- 시간: 줄 길이 L에 대해 O(L)입니다.
- 보조 공간: 입력 줄 보관에 O(L), 파싱 상태는 O(1)입니다.

위치가 뒤로 가지 않고 각 문자를 상수 번 검사합니다.

[예제 입력](<예제_examples/04-문자열과파싱_strings-parsing/input.txt>) · [예상 출력](<예제_examples/04-문자열과파싱_strings-parsing/output.txt>) · [예제 실행 방법](<예제_examples/04-문자열과파싱_strings-parsing/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 0 | 340207 [PCCE 기출문제] 1번 / 문자 출력 | — | [C++](<../C++/level0/extra_340207_[PCCE_기출문제]_1번___문자_출력/README.md>) | [Python](<../Python/level0/extra_340207_[PCCE_기출문제]_1번___문자_출력/README.md>) |
| 1 | 468370 중요한 단어를 스포 방지 | [C](<../C/level1/extra_468370_중요한_단어를_스포_방지/README.md>) | [C++](<../C++/level1/extra_468370_중요한_단어를_스포_방지/README.md>) | [Python](<../Python/level1/extra_468370_중요한_단어를_스포_방지/README.md>) |
| 2 | 92335 k진수에서 소수 개수 구하기 | [C](<../C/level2/046_92335_k진수에서_소수_개수_구하기/README.md>) | [C++](<../C++/level2/046_92335_k진수에서_소수_개수_구하기/README.md>) | [Python](<../Python/level2/046_92335_k진수에서_소수_개수_구하기/README.md>) |
| 3 | 389481 봉인된 주문 | [C](<../C/level3/008_389481_봉인된_주문/README.md>) | [C++](<../C++/level3/008_389481_봉인된_주문/README.md>) | [Python](<../Python/level3/008_389481_봉인된_주문/README.md>) |
| 4 | 60060 가사 검색 | — | [C++](<../C++/level4/extra_60060_가사_검색/README.md>) | [Python](<../Python/level4/extra_60060_가사_검색/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/strings.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

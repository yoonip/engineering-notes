# C·C++·Python의 자료 표현과 구현 비용

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 알고리즘이 같아도 바뀌는 부분

세 언어를 비교할 때 문법을 한 줄씩 바꾸는 것보다 정수 범위, 소유권, 컨테이너 연산, 재귀와 복사 비용을 먼저 비교합니다. 문제의 상태·불변식·전이는 같게 두고 그 상태를 저장하는 방식을 바꿉니다. 서로 다른 언어의 정답 기록은 각 언어의 기존 채점 문서에서 확인하며, 이 학습 자료를 썼다고 새로 채점한 것으로 표시하지 않습니다.

| 작업 | C | C++ | Python |
| --- | --- | --- | --- |
| 가변 길이 배열 | capacity와 길이, realloc 실패 처리를 직접 관리합니다. | vector의 크기·용량과 참조 무효화를 확인합니다. | list가 원소 참조를 저장하며 슬라이싱은 새 리스트를 만듭니다. |
| FIFO 큐 | 배열+head/tail 또는 원형 버퍼를 만듭니다. | queue/deque를 사용합니다. | collections.deque를 사용합니다. |
| 빈도 집계 | 값 범위가 작으면 배열, 크면 해시 테이블 등을 구성합니다. | unordered_map/map의 목적과 최악 비용을 구별합니다. | dict/Counter를 사용하며 키의 hash 가능성을 확인합니다. |
| 최소 힙 | sift-up/down과 크기를 관리합니다. | priority_queue의 기본은 최대 힙이므로 비교자를 확인합니다. | heapq의 기본은 최소 힙입니다. |
| 문자열 조립 | 종료 문자와 버퍼 길이를 함께 관리합니다. | string의 추가와 재할당 비용을 봅니다. | 조각을 모아 join하면 반복적인 전체 복사를 줄일 수 있습니다. |

## 정수 범위와 나눗셈

C/C++의 signed 정수 연산이 표현 범위를 벗어나면 정의되지 않은 동작이 될 수 있습니다. 곱셈 결과를 long long에 넣더라도 두 int를 먼저 곱하면 이미 넘칠 수 있으므로 피연산자부터 넓힙니다. unsigned의 모듈러 연산도 음수가 필요한 수식에는 자동 대안이 아닙니다. [C++ 공개 초안의 산술식 규칙](https://eel.is/c++draft/expr.pre)을 근거로 구분합니다.

Python int는 필요한 만큼 커지지만 산술 연산을 무조건 O(1)로 취급할 수는 없습니다. 수천 비트 이상의 정수, 비트셋·다항식 패킹을 사용하면 정수 길이가 실제 비용입니다.

음수 나눗셈에서 Python의 //는 음의 무한대 방향이고 C/C++의 정수 나눗셈은 0 방향입니다. 자체 예제로 -3을 2로 나누면 Python //는 -2, C/C++의 정수 몫은 -1입니다. 나머지의 부호도 함께 달라집니다. 정수 좌표 구간의 개수를 세는 수식을 옮길 때 floor_div와 ceil_div의 정의를 먼저 맞춥니다.

## 상태 공유와 복사

Python에서 행 하나를 여러 번 참조하는 2차원 리스트를 만들면 한 칸의 수정이 여러 행에 보일 수 있습니다. 각 행을 별도로 생성해야 독립 배열이 됩니다. 가변 기본 인자도 함수 호출 사이에 상태를 공유할 수 있습니다.

C는 반환할 배열을 지역 자동 배열에 두지 않습니다. 함수가 끝난 뒤에도 유효한 저장 공간과 반환 길이가 필요합니다. C++에서는 vector 확장 뒤 원소 포인터·반복자가 무효가 될 수 있습니다. 백트래킹에서 공유 상태를 썼다면 되돌림 순서, 복사 상태를 썼다면 전체 복사량을 계산합니다.

## 정렬과 비교

비교 함수가 일관된 순서를 만들어야 합니다. a<b, b<c인데 c<a인 비교는 정렬의 가정을 깨뜨립니다. 부동소수점 오차 허용치를 무조건 비교 함수에 넣는 방법도 추이성을 깨뜨릴 수 있습니다. C qsort의 비교값을 a-b로 반환하는 방식은 큰 정수에서 넘칠 수 있으므로 대소 관계로 부호를 결정합니다.

Python의 key는 정렬 키를 먼저 계산하는 방식이고 C++ comparator는 비교할 때 호출될 수 있습니다. 문자열을 a+b와 b+a로 비교하면 임시 문자열 생성 비용까지 봅니다. 정렬 뒤 같은 값의 기존 순서가 필요한지 안정성 조건도 명확히 합니다.

## 비용이 바뀌는 대표 함정

| 구현 | 실제로 추가되는 일 | 바꿀 기준 |
| --- | --- | --- |
| Python list.pop(0) 반복 | 남은 원소들의 이동입니다. | 양끝 큐 연산은 deque로 바꿉니다. |
| 재귀마다 문자열·배열 전체 복사 | 호출 수에 상태 크기를 곱한 작업입니다. | 인덱스·공유 버퍼·되돌림을 검토합니다. |
| 매 단계 전체 정렬 | 필요한 극값 하나보다 많은 정보를 계산합니다. | 동적 극값이면 힙을 검토합니다. |
| 큰 인접 행렬 | 실제 간선이 적어도 V² 칸입니다. | 희소 그래프는 인접 리스트를 검토합니다. |
| 반복문 속 선형 탐색 | 겉보기 반복 횟수보다 차수가 커집니다. | 빈도 배열·집합·정렬 후 탐색을 검토합니다. |

[Python deque 공식 설명](https://docs.python.org/3/library/collections.html#collections.deque)은 양끝 연산과 list 앞부분 삽입·삭제의 차이를 명시합니다. 이는 언어 이름의 차이보다 필요한 연산을 맞추는 것이 중요하다는 예입니다.

## 코딩 테스트와 실제 프로그램

플랫폼의 함수 시그니처, 입력 길이와 결과 메모리 규약을 지킵니다. 같은 함수가 여러 번 호출될 수 있으므로 C의 전역 카운터나 Python 캐시가 이전 입력을 섞지 않게 합니다. 큰 테스트 하나만 맞아도 메모리 누수·범위 밖 접근·누적 상태 오류가 사라졌다고 볼 수 없습니다.

실제 서비스에서는 알고리즘 외에 잘못된 입력, 실패 복구, 데이터 소유권, 동시 접근, 직렬화 비용과 관측 가능성도 설계합니다. 코딩 테스트의 정해진 입력 가정과 신뢰할 수 없는 외부 입력을 구별합니다. 성능을 위해 자료형을 줄일 때는 값의 최대 범위를 계산한 근거를 남깁니다.

## 복습

복습: C++의 int 곱셈을 계산한 뒤 long long으로 변환하는 것과 곱셈 전에 변환하는 것이 왜 다른지 설명합니다. 답은 표현식의 피연산자 자료형이 중간 계산의 자료형을 결정하기 때문입니다. 결과 변수의 넓은 범위가 이미 발생한 오버플로를 복구하지 않습니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

양의 나누는 수에 대해 세 언어 모두 a=bq+r, 0≤r<b를 만족하는 내림 몫과 나머지를 출력합니다. C·C++의 0 방향 나눗셈에 필요한 보정을 직접 구현합니다.

이 예제에서 직접 구현하는 기법은 0 방향 나눗셈 · floor 몫 보정 · 몫과 나머지 등식입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

정수 a b 두 개입니다. -1000≤a≤1000, 1≤b≤1000입니다. b=0과 최소 정수/-1의 범위 오류는 입력에 없습니다.

```text
-3 2
```

내림 몫 q와 0≤r<b인 나머지 r을 공백으로 출력합니다.

```text
-2 1
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | a=-3, b=2 | 나누는 수는 양수라는 조건을 사용합니다. |
| 2 | C/C++의 초기 q=-1, r=-1 | 정수 나눗셈이 0 방향이므로 보정이 필요합니다. |
| 3 | 보정 후 q=-2, r=1 | 몫을 줄인 만큼 나머지에 b를 더합니다. |
| 4 | -3=2*(-2)+1, 0≤1&lt;2 | 등식과 나머지 범위를 함께 확인한 뒤 출력합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/40-C와CPP와Python구현비교_language-implementation/example.c>)

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


int main(void) {  // 양의 분모에 대한 floor 나눗셈 비교
    int a = read_int(), b = read_int();  // 나눌 정수와 양의 나누는 수
    int quotient = a / b, remainder = a % b;  // C·C++의 0 방향 몫과 그 나머지
    if (remainder < 0) {  // 음수 나머지이면 아직 내림 규칙과 다름
        --quotient;  // 몫을 한 단계 더 낮추기
        remainder += b;  // 같은 등식을 유지하며 나머지를 비음수로 조정
    }  // 내림 몫 보정 끝
    write_number(quotient); write_text(" "); write_number(remainder); write_text("\n");  // 두 값을 같은 형식으로 출력
    return 0;  // 정상 종료
}  // 음수 나눗셈 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/40-C와CPP와Python구현비교_language-implementation/example.cpp>)

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


int main(void) {  // 양의 분모에 대한 floor 나눗셈 비교
    int a = read_int(), b = read_int();  // 나눌 정수와 양의 나누는 수
    int quotient = a / b, remainder = a % b;  // C·C++의 0 방향 몫과 그 나머지
    if (remainder < 0) {  // 음수 나머지이면 아직 내림 규칙과 다름
        --quotient;  // 몫을 한 단계 더 낮추기
        remainder += b;  // 같은 등식을 유지하며 나머지를 비음수로 조정
    }  // 내림 몫 보정 끝
    write_number(quotient); write_text(" "); write_number(remainder); write_text("\n");  // 두 값을 같은 형식으로 출력
    return 0;  // 정상 종료
}  // 음수 나눗셈 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/40-C와CPP와Python구현비교_language-implementation/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    a, b = int(next(tokens)), int(next(tokens))  # 정수와 양의 분모
    quotient, remainder = divmod(a, b)  # Python의 내림 몫과 비음수 나머지
    print(quotient, remainder)  # 세 언어가 같은 q와 r을 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 기본 정수 몫 | a/b는 0 방향 몫입니다. | a/b는 0 방향 몫입니다. | a//b와 divmod의 몫은 음의 무한대 방향입니다. |
| 음수 나머지 | a%b가 음수이면 몫을 1 줄이고 b를 더합니다. | 같은 보정을 적용해 Python과 규칙을 맞춥니다. | b가 양수이면 divmod가 이미 비음수 나머지를 반환합니다. |
| 허용 범위 | 분모 0과 표현 범위를 넘는 나눗셈을 입력에서 제외합니다. | 같은 작은 int 범위를 사용합니다. | 큰 정수를 처리할 수 있지만 이 예제는 입력 범위를 동일하게 제한합니다. |

### 예제의 비용과 실행 파일

- 시간: O(1)
- 보조 공간: O(1)

명시한 작은 정수 범위에서 나눗셈·나머지와 한 번의 보정만 수행합니다.

[예제 입력](<예제_examples/40-C와CPP와Python구현비교_language-implementation/input.txt>) · [예상 출력](<예제_examples/40-C와CPP와Python구현비교_language-implementation/output.txt>) · [예제 실행 방법](<예제_examples/40-C와CPP와Python구현비교_language-implementation/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

[유형별 연습문제](<연습문제_problem-index.md>)에서 문제를 고르고 상태·정당성·구현 비용을 함께 비교할 수 있습니다.

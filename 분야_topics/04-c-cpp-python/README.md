# C·C++·Python

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

C는 데이터 표현과 메모리 접근을 직접 다룹니다. MCU 펌웨어, 운영체제, 드라이버, 통신 라이브러리에서 많이 쓰입니다. C++는 여기에 클래스·템플릿·표준 라이브러리 등을 더해 복잡한 프로그램을 구성합니다. Python은 제어 흐름을 간결하게 표현하고 분석 도구를 연결하는 데 강점이 있습니다.

## C: 데이터와 메모리

배열은 같은 형식의 원소가 연속으로 놓인 자료구조이고, 포인터는 객체나 함수의 주소를 다룹니다. 함수 인자로 전달된 포인터에는 배열 길이가 자동으로 포함되지 않습니다. 구조체는 관련 데이터를 묶고, 비트 연산은 레지스터 필드나 통신 패킷을 다루는 데 사용합니다.

```c
#include <stddef.h>  // #include는 size_t 등의 선언이 있는 표준 헤더를 포함합니다.
#include <stdio.h>  // printf 선언을 포함합니다.

double mean(const double *values, size_t count) {  // double 결과를 반환하며 포인터와 원소 수를 받습니다.
    double sum = 0.0;  // 합계를 실수 0으로 초기화합니다.
    for (size_t i = 0; i < count; ++i) {  // i를 0부터 count 직전까지 1씩 증가시킵니다.
        sum += values[i];  // []로 i번째 원소를 읽고 +=로 합계에 더합니다.
    }  // for 블록의 끝입니다.
    return sum / (double)count;  // count를 double로 변환한 뒤 나눈 값을 반환합니다.
}  // mean 함수의 끝입니다.

int main(void) {  // 인수 없는 프로그램 진입 함수를 정의합니다.
    const double voltage[] = {3.1, 3.2, 3.3};  // 변경하지 않을 실수 배열을 {}의 값으로 초기화합니다.
    const size_t count = sizeof voltage / sizeof voltage[0];  // 배열 전체 byte 수를 원소 하나의 크기로 나눕니다.
    printf("%.3f V\n", mean(voltage, count));  // 평균을 소수 셋째 자리까지 출력하고 줄을 바꿉니다.
    return 0;  // 정상 종료를 나타내는 정수를 반환합니다.
}  // main 함수의 끝입니다.
```

이 예의 `mean`은 `count > 0`이고 그 길이만큼 읽을 수 있는 배열을 입력으로 받습니다. `const`는 이 포인터를 통해 원소를 바꾸지 않는다는 뜻입니다. Linux에서 GCC가 설치되어 있다면 `gcc -std=c17 -Wall -Wextra -Wpedantic mean.c -o mean`으로 빌드하고 `./mean`으로 실행합니다. 위 배열의 평균은 3.200 V입니다.

`sizeof voltage / sizeof voltage[0]`는 여기처럼 실제 배열이 보이는 위치에서 사용합니다. 함수 안의 포인터 `values`에 같은 식을 쓰면 포인터 크기를 나누게 되어 길이를 얻지 못합니다. [WG14 N1570(C11 초안), §6.5.3.4 예 2·주 103](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)

`malloc`으로 확보한 메모리는 수명 관리가 필요합니다. 범위를 벗어난 접근, 해제 후 사용, 초기화하지 않은 값, 부호 있는 정수의 오버플로는 대표적인 오류 원인입니다. `volatile`은 장치 레지스터 접근 등에 쓰이지만 스레드 동기화나 원자성을 보장하지 않습니다.

## C++: 자원 수명과 추상화

RAII는 자원 해제를 소유 객체의 소멸에 연결하는 방식입니다. 자동 저장 기간의 지역 객체는 정상적으로 범위를 벗어날 때 소멸하지만, `std::exit()`는 그 지역 객체의 소멸자를 호출하지 않습니다. `abort()`나 전원 상실까지 정리를 보장하는 방식으로 해석하지 않습니다. [C++ 작업 초안의 선언문 §2](https://eel.is/c++draft/stmt.dcl), [프로그램 종료 규칙](https://eel.is/c++draft/support.start.term)

`std::vector`는 크기가 변하는 연속 배열이고, `std::unique_ptr`는 단일 소유권을 표현합니다. 템플릿은 자료형에 걸쳐 알고리즘을 재사용하게 합니다.

```cpp
#include <iostream>  // 표준 출력 스트림 std::cout의 선언을 포함합니다.
#include <numeric>  // std::accumulate의 선언을 포함합니다.
#include <vector>  // 연속 동적 배열 std::vector의 선언을 포함합니다.

int main() {  // 프로그램 진입 함수를 정의합니다.
    const std::vector<double> voltage{3.1, 3.2, 3.3};  // double 원소를 가진 vector를 {}로 초기화합니다.
    const double sum = std::accumulate(voltage.begin(), voltage.end(), 0.0);  // [begin,end)의 원소를 double 합계에 더합니다.
    std::cout << sum / voltage.size() << '\n';  // <<로 비어 있지 않은 vector의 평균과 개행을 출력합니다.
}  // main의 끝에서는 0을 반환한 것처럼 정상 종료합니다.
```

`accumulate`의 세 번째 인수는 초기값이면서 누산 타입을 정합니다. 여기의 `0.0`을 `0`으로 바꾸면 누산기가 `int`가 되어 덧셈마다 실수 부분을 잃을 수 있습니다. 반환 뒤 `double` 변수에 담아도 이미 버린 소수부는 돌아오지 않습니다. [C++ 작업 초안, accumulate §2](https://eel.is/c++draft/accumulate)

## Python과 다른 언어의 연결

Python에서는 `sum(values) / len(values)`로 같은 계산을 표현할 수 있습니다. 대량의 수치 계산은 NumPy·PyTorch처럼 내부가 C/C++·GPU 코드로 구현된 라이브러리에 맡기는 경우가 많습니다. ctypes·CFFI·pybind11은 언어 경계를 연결합니다.

Rust는 소유권과 차용을 이용한 메모리 안전성, Go는 서비스와 동시성, Java·C#은 관리형 런타임과 애플리케이션 생태계, JavaScript·TypeScript는 웹, Julia는 수치 계산에 자주 쓰입니다. Tcl·SKILL은 EDA 자동화에 쓰이고, Assembly는 명령어와 호출 규약을 직접 확인하는 데 쓰입니다.

## 길이·소유권·공유 상태를 실제 코드로 비교합니다

[C 이진 프레임](../../설계와검증사례_engineering-cases/이진프레임의길이와바이트순서_c-frame-bounds.md)에서 헤더의 count가 2,147,483,648일 때 계산한 길이를 uint32_t로 좁히면 4가 됩니다. 4바이트만 받은 입력이 잘못 승인되는 경로와, 실제 공간으로 개수 상한을 확인해 거절하는 경로를 실행합니다. 포인터에는 배열 길이가 자동으로 들어 있지 않으므로 호출자와 파서의 계약이 모두 필요합니다.

[C++ 뷰·소유 복사](../../설계와검증사례_engineering-cases/수신버퍼의소유권과뷰수명_cpp-view-ownership.md)는 원본 버퍼가 READY에서 ERROR로 덮어써질 때 뷰와 복사본의 결과가 달라지는 것을 보여 줍니다. 두 주소가 모두 유효해도 필요한 값의 보관 시점이 다를 수 있습니다. data()로 포인터만 전달해 필드 길이를 잃는 문제도 따로 비교합니다.

[C11 SPSC 링버퍼](../../설계와검증사례_engineering-cases/링버퍼의공개순서와공유카운터_ring-publication.md)는 일반 정수 used를 두 문맥이 갱신할 때의 유실과, 각 문맥이 head·tail을 소유하고 release·acquire로 공개하는 규칙을 나눕니다. 호스트 빌드·사건 모델·순차 검사를 실제 ISR·보드 시험으로 확대하지 않습니다. [실행 코드와 명령](../../예제_examples/실무검증_practical-validation/native_firmware/README.md)에서 직접 대조하실 수 있습니다.

## 관련 기술

C, C++, Python, Rust, Go, Java, C#, JavaScript/TypeScript, Julia, R, Tcl, Lua, Assembly

## 참고 자료

- [GCC language standards](https://gcc.gnu.org/onlinedocs/gcc/Standards.html)
- [Python Tutorial](https://docs.python.org/3/tutorial/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [비트에서 수까지: 정수, 부동소수점, 고정소수점](해설_notes/비트에서수까지_numbers-and-quantization.md)

## English

C gives direct control over data representation and memory access. It is widely used in MCU firmware, operating systems, drivers, and communication libraries. C++ adds tools such as classes, templates, and the standard library for structuring larger programs. Python offers concise control flow and convenient connections to analysis libraries.

### C: data and memory

An array stores elements of one type contiguously. A pointer refers to an object or function, but a pointer passed to a function does not automatically carry an array's length. Structures group related values, and bit operations are useful for register fields and communication packets.

The C example above computes the mean of three voltage measurements. Its `mean` function expects `count > 0` and an array with at least that many readable elements. `const` prevents modification through that pointer. With GCC on Linux, `gcc -std=c17 -Wall -Wextra -Wpedantic mean.c -o mean` builds it and `./mean` runs it. The mean of the example array is 3.200 V.

The `sizeof` ratio determines the element count where the actual array is in scope. Applying it to the function's pointer parameter measures the pointer, not the original array. [WG14 N1570, §6.5.3.4, example 2 and footnote 103](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)

Memory allocated with `malloc` needs explicit lifetime management. Out-of-bounds access, use after free, uninitialized values, and signed integer overflow are common sources of errors. `volatile` is useful for accesses such as device registers, but does not provide thread synchronization or atomicity.

### C++: resource lifetime and abstraction

RAII ties resource release to destruction of its owner. Automatic local objects are destroyed on ordinary scope exit, but `std::exit()` does not destroy them; `abort()` and power loss do not promise this cleanup. [C++ declaration statements](https://eel.is/c++draft/stmt.dcl), [termination rules](https://eel.is/c++draft/support.start.term)

`std::vector` provides a resizable contiguous array, `std::unique_ptr` expresses exclusive ownership, and templates allow algorithms across types. In the existing C++ mean example, `accumulate` uses the initial value's type for its accumulator: `0.0` keeps a `double` sum, whereas `0` can truncate fractional parts during integer accumulation. Converting the final result to `double` cannot recover them. [C++ accumulate §2](https://eel.is/c++draft/accumulate)

### Connecting Python and other languages

Python expresses the same calculation as `sum(values) / len(values)`. Large numerical workloads often run through libraries such as NumPy and PyTorch, whose implementations include C, C++, and GPU code. ctypes, CFFI, and pybind11 connect these language boundaries.

Rust uses ownership and borrowing for memory safety; Go is common in services and concurrent programs. Java and C# have managed runtimes and broad application ecosystems, JavaScript and TypeScript are central to web development, and Julia targets numerical computing. Tcl and SKILL appear in EDA automation, while Assembly exposes instructions and calling conventions directly.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Integer, floating-point and fixed-point representation](해설_notes/비트에서수까지_numbers-and-quantization.md#english)


## 심화 해설 | Advanced article

- [C의 고정 크기 ring buffer: 경계와 소유권부터](해설_notes/고정크기링버퍼_bounded-ring-buffer.md) · [English](해설_notes/고정크기링버퍼_bounded-ring-buffer.md#english)

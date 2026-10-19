# C, C++ & Python

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

C는 자료의 표현과 메모리 접근을 직접 다루기 좋은 언어다. MCU 펌웨어, 운영체제, 드라이버, 통신 라이브러리에서 많이 쓰인다. C++는 여기에 클래스·템플릿·표준 라이브러리 등을 더해 복잡한 프로그램을 구성한다. Python은 제어 흐름을 간결하게 표현하고 분석 도구를 연결하는 데 강점이 있다.

## C: 데이터와 메모리

배열은 같은 형식의 원소가 연속으로 놓인 자료구조이고, 포인터는 객체나 함수의 주소를 다룬다. 함수 인자로 전달된 포인터에는 배열 길이가 자동으로 포함되지 않는다. 구조체는 관련 데이터를 묶고, 비트 연산은 레지스터 필드나 통신 패킷을 다루는 데 사용한다.

```c
#include <stddef.h>
#include <stdio.h>

double mean(const double *values, size_t count) {
    double sum = 0.0;
    for (size_t i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum / (double)count;
}

int main(void) {
    const double voltage[] = {3.1, 3.2, 3.3};
    const size_t count = sizeof voltage / sizeof voltage[0];
    printf("%.3f V\n", mean(voltage, count));
    return 0;
}
```

이 예의 `mean`은 `count > 0`이고 그 길이만큼 읽을 수 있는 배열을 입력으로 받는다. `const`는 이 포인터를 통해 원소를 바꾸지 않는다는 뜻이다. Linux에서 GCC가 설치되어 있다면 `gcc -std=c17 -Wall -Wextra -Wpedantic mean.c -o mean`으로 빌드하고 `./mean`으로 실행한다. 위 배열의 평균은 3.200 V다.

`malloc`으로 확보한 메모리는 수명 관리가 필요하다. 범위를 벗어난 접근, 해제 후 사용, 초기화하지 않은 값, 부호 있는 정수의 오버플로는 대표적인 오류 원인이다. `volatile`은 장치 레지스터 접근 등에 쓰이지만 스레드 동기화나 원자성을 보장하지 않는다.

## C++: 자원 수명과 추상화

RAII는 객체 수명과 자원 수명을 묶는 방식이다. 파일과 메모리를 소유하는 객체가 범위를 벗어나면 정리 작업이 이루어진다. `std::vector`는 크기가 변하는 연속 배열이고, `std::unique_ptr`는 단일 소유권을 표현한다. 템플릿은 자료형에 걸쳐 알고리즘을 재사용하게 한다.

```cpp
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<double> voltage{3.1, 3.2, 3.3};
    const double sum = std::accumulate(voltage.begin(), voltage.end(), 0.0);
    std::cout << sum / voltage.size() << '\n';
}
```

## Python과 다른 언어의 연결

Python에서는 `sum(values) / len(values)`로 같은 계산을 표현할 수 있다. 대량의 수치 계산은 NumPy·PyTorch처럼 내부가 C/C++·GPU 코드로 구현된 라이브러리에 맡기는 경우가 많다. ctypes·CFFI·pybind11은 언어 경계를 연결한다.

Rust는 소유권과 차용을 이용한 메모리 안전성, Go는 서비스와 동시성, Java·C#은 관리형 런타임과 애플리케이션 생태계, JavaScript·TypeScript는 웹, Julia는 수치 계산에 자주 쓰인다. Tcl·SKILL은 EDA 자동화에서 만나기 쉽고, Assembly는 명령어와 호출 규약을 직접 확인하는 데 쓰인다.

## 관련 기술

C, C++, Python, Rust, Go, Java, C#, JavaScript/TypeScript, Julia, R, Tcl, Lua, Assembly

## 참고 자료

- [GCC language standards](https://gcc.gnu.org/onlinedocs/gcc/Standards.html)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

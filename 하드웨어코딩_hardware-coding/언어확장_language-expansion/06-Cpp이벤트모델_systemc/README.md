# SystemC FIFO의 대기와 도착 시간 | SystemC FIFO timing

C++의 두 프로세스가 용량 한 개의 FIFO로 정수 네 개를 주고받는 예제입니다. 실제 SystemC 3.0.2 커널에서 실행하여 데이터 순서와 요청·수락·도착 시각을 검사합니다. 소비가 늦으면 생산자가 기다리는 역압(backpressure)이 생깁니다. 이때 역압은 별도의 `ready` 핀이 아니라 `sc_fifo::write()`의 블로킹으로 표현합니다.

[소스](example.cpp) · [CMake 설정](CMakeLists.txt) · [판본·해시·실행 결과](example.json) · [언어와 검증 도구](../../언어와검증도구_languages-and-verification.md)

## 무엇을 모델링하는지

[SystemC 공식 소개](https://systemc.org/overview/systemc/)는 C++ 클래스 라이브러리를 이용한 시스템 수준 모델링과 하드웨어·소프트웨어 상호작용을 설명합니다. 이 예제에서는 프로세스가 언제 기다리고 다시 실행되는지를 다룹니다. 생성한 RTL이나 물리 회로를 검사하는 실습은 아닙니다.

생산자는 1ns에 첫 쓰기를 시도하고, 쓰기가 수락되면 1ns 뒤 다음 데이터를 준비합니다. 소비자는 느린 설정에서 5ns에 첫 읽기를 시작하고 이후 4ns마다 읽습니다. 다음 요청 시각은 외부에서 고정된 도착 시각이 아니라, 이전 쓰기의 완료 시각에 따라 늦춰집니다.

`SC_THREAD`는 SystemC 커널에 등록한 시뮬레이션 프로세스입니다. 운영체제의 두 스레드가 벽시계 시간으로 달린다는 의미가 아닙니다. `wait()`는 현재 프로세스를 잠시 중단하고 커널이 다음 시간 또는 이벤트에서 재개하도록 합니다. 소스는 1ns 시간 해상도를 지정하여 `sc_time_stamp().value()`를 나노초 정수로 기록합니다.

## 느린 소비자의 시간 흐름

| 값 | 쓰기 요청 | 쓰기 수락 | 소비자 도착 | 생산자 대기 |
| --- | ---: | ---: | ---: | ---: |
| 11 | 1ns | 1ns | 5ns | 0ns |
| 22 | 2ns | 5ns | 9ns | 3ns |
| 33 | 6ns | 9ns | 13ns | 3ns |
| 44 | 10ns | 13ns | 17ns | 3ns |

1. 1ns에 값 11을 넣으면 FIFO가 가득 찹니다. 소비자가 아직 읽지 않았으므로 2ns의 값 22 쓰기는 대기합니다.
2. 5ns에 소비자가 11을 꺼내면 채널 갱신과 0시간 이벤트 통지 뒤 생산자가 재개됩니다. 같은 5ns라도 뒤의 델타 사이클에서 22의 쓰기가 끝날 수 있습니다. 표는 델타 번호를 기록하지 않습니다.
3. 생산자는 수락 뒤 1ns를 기다리므로 33은 3ns가 아니라 6ns에 요청합니다. 소비자의 다음 읽기는 9ns이며, 이때 33의 쓰기가 수락됩니다.
4. 같은 과정으로 44는 13ns에 수락되고 17ns에 읽힙니다. 마지막 읽기 뒤 두 프로세스가 종료되며 예약된 미래 이벤트가 없으므로 `sc_start()`가 돌아옵니다.

FIFO의 블로킹과 델타 이벤트는 [3.0.2 sc_fifo.h의 read·write·update](https://github.com/accellera-official/systemc/blob/3.0.2/src/sysc/communication/sc_fifo.h)에서 확인할 수 있습니다. 이 채널을 단순한 C++ `std::queue` 반복 계산으로 대체하지 않고 실제 엔진에 연결합니다.

## 실행 결과와 검사 범위

2026년 10월 26일 Windows x64에서 SystemC 3.0.2를 정적 라이브러리로 빌드하고 실행했습니다. 예제와 라이브러리는 같은 Zig 0.16.0의 C++ 프런트엔드(Clang 21.1.0)와 C++17을 사용했습니다. CMake 4.4.4와 Ninja 1.13.2를 사용했으며, 예제는 `-Wall -Wextra -Werror`로 경고 없이 컴파일했습니다. 명령·실제 출력·반환 코드·게시 소스와 컴파일 복사본의 SHA-256은 [example.json](example.json)에 있습니다.

| 설정 | 검사한 조건 | 실제 결과 |
| --- | --- | --- |
| `slow` | 네 값의 순서, 요청·수락·도착 시각, 마지막 이벤트 17ns | `PASS`, 종료 코드 0 |
| `fast` | 즉시 읽기를 시작하고 1ns 간격으로 소비하여 네 전송의 대기가 0ns인지 확인 | `PASS`, 종료 코드 0 |
| `bad-expectation` | 정상 모델은 그대로 두고 마지막 도착 기대값만 18ns로 변경 | `FAIL`, 종료 코드 1로 잘못된 기대값 검출 |

음성 대조는 결함 회로를 검출했다는 뜻이 아닙니다. 정상 출력에 잘못된 기대값을 주었을 때 검사기가 실패를 반환하는지 확인합니다. 두 정상 설정은 서로 다른 프로세스로 실행하므로 커널 초기화 상태를 공유하지 않습니다.

느린 설정의 실제 출력은 다음과 같습니다.

```text
SystemC 3.0.2-Accellera
mode=slow fifo_capacity=1
value request_ns accept_ns arrival_ns blocked_ns
11 1 1 5 0
22 2 5 9 3
33 6 9 13 3
44 10 13 17 3
PASS
```

빠른 설정에서는 네 행의 요청·수락·도착 시각이 각각 1·2·3·4ns이고 모든 `blocked_ns`가 0입니다. 기대 시각은 실행 결과에서 복사해 검사식으로 만드는 대신, 위 시간 규칙을 손으로 전개한 고정 배열로 적었습니다.

## 실행 방법

[공식 3.0.2 설치 안내](https://github.com/accellera-official/systemc/blob/3.0.2/INSTALL.md)의 CMake 경로로 라이브러리를 먼저 설치합니다. C++ 표준과 컴파일러 ABI가 라이브러리와 응용 프로그램에서 맞아야 합니다. 아래 예제의 CMake 하한은 3.16입니다.

```bash
cmake -S /path/to/systemc-3.0.2 -B /path/to/systemc-build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=17 -DBUILD_SHARED_LIBS=OFF -DENABLE_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=/path/to/systemc-install
cmake --build /path/to/systemc-build --config Release
cmake --install /path/to/systemc-build --config Release
cmake -S . -B /path/to/fifo-build -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/path/to/systemc-install
cmake --build /path/to/fifo-build --config Release
/path/to/fifo-build/fifo_demo slow
/path/to/fifo-build/fifo_demo fast
/path/to/fifo-build/fifo_demo bad-expectation
```

마지막 명령은 의도적으로 종료 코드 1을 반환합니다. Windows에서는 생성한 `.exe`를 사용하며, 여러 구성의 빌드 도구는 `Release` 하위 폴더에 실행 파일을 둘 수 있습니다. 기본 라이브러리는 시작 배너를 표준 오류에 출력할 수 있지만 이 기록은 `DISABLE_COPYRIGHT_MESSAGE=ON`으로 빌드하여 배너를 끈 조건입니다.

이 환경의 Zig는 외부 라이브러리 `sc_ver.cpp`의 `__DATE__`·`__TIME__`를 기본 오류로 처리했습니다. 원본 SystemC 코드를 수정하지 않고 해당 라이브러리 빌드에만 `-Wno-error=date-time`를 추가하여 두 경고를 기록했습니다. 직접 작성한 예제의 `-Werror`는 유지했습니다. 비ASCII 작업 경로 문제를 피하려고 해시가 같은 소스 복사본을 ASCII 임시 경로에서 빌드했으며, 해당 경로와 설정은 실행 기록에 남겼습니다. 이 Windows 조합의 로컬 성공을 모든 컴파일러 조합의 공식 지원으로 확대하지 않습니다.

## 전체 코드와 줄별 복습 메모

각 비어 있지 않은 코드 줄의 오른쪽 주석에 문법과 그 줄의 목적을 적었습니다. SystemC 3.0.2를 대상으로 하므로, 이 판본에서 더 이상 필요하지 않은 구형 `SC_HAS_PROCESS` 매크로는 사용하지 않습니다.

```cpp
#include <systemc> // 이벤트·시뮬레이션 시간·FIFO를 제공하는 실제 SystemC 라이브러리
#include <array> // 전송 네 개의 값과 시각을 고정 길이 배열에 보관
#include <cstdint> // 나노초 시각을 부호 없는 64비트 정수로 저장
#include <iostream> // 검사 결과를 표 형태로 출력
#include <string> // 실행 모드 이름 비교

class FifoDemo : public sc_core::sc_module { // 두 프로세스와 FIFO를 하나의 시뮬레이션 모듈로 구성
public: // sc_main에서 결과를 읽을 수 있도록 기록 공개
    sc_core::sc_fifo<int> fifo; // 용량 한 개의 블로킹 채널
    const std::array<int, 4> values{11, 22, 33, 44}; // 생산 순서가 보존되어야 할 독립 입력
    std::array<int, 4> received{}; // 소비자가 실제로 읽은 값
    std::array<std::uint64_t, 4> requested_ns{}; // write를 호출하기 직전 시각
    std::array<std::uint64_t, 4> accepted_ns{}; // write가 끝나 생산자가 재개된 시각
    std::array<std::uint64_t, 4> arrived_ns{}; // read가 끝나 소비자가 값을 얻은 시각
    const sc_core::sc_time start_delay; // 소비자가 첫 읽기를 시작하기까지의 지연
    const sc_core::sc_time interval; // 소비자의 연속 읽기 사이 간격
    FifoDemo(sc_core::sc_module_name name, bool fast) // 모듈 이름과 소비 속도로 실험 조건 선택
        : sc_core::sc_module(name), fifo("fifo", 1), // 기본 모듈 초기화와 용량 한 개의 FIFO 생성
          start_delay(fast ? 0 : 5, sc_core::SC_NS), // 빠른 소비자는 즉시, 느린 소비자는 5ns 뒤 시작
          interval(fast ? 1 : 4, sc_core::SC_NS) { // 소비 간격을 1ns 또는 4ns로 설정
        SC_THREAD(produce); // wait로 중단·재개되는 생산 프로세스 등록
        SC_THREAD(consume); // 독립적으로 기다리는 소비 프로세스 등록
    } // 생성자 끝, 실제 프로세스는 sc_start에서 실행
    void produce() { // 1ns마다 다음 전송을 시도하는 생산자
        sc_core::wait(1, sc_core::SC_NS); // 첫 데이터 준비 시간을 1ns로 고정
        for (std::size_t i = 0; i < values.size(); ++i) { // 입력 네 개를 원래 순서로 전송
            requested_ns[i] = sc_core::sc_time_stamp().value(); // 1ns 해상도에서 요청 시각 기록
            fifo.write(values[i]); // 가득 차 있으면 공간이 생길 때까지 이 프로세스만 대기
            accepted_ns[i] = sc_core::sc_time_stamp().value(); // 블로킹 호출이 돌아온 실제 수락 시각 기록
            if (i + 1 < values.size()) { // 마지막 전송 뒤에는 불필요한 타이머를 남기지 않음
                sc_core::wait(1, sc_core::SC_NS); // 수락 뒤 1ns를 지나 다음 데이터 준비
            } // 다음 전송 준비 조건 끝
        } // 생산 순회 끝
    } // 생산 프로세스 종료
    void consume() { // 일정 간격으로 FIFO를 읽는 소비자
        sc_core::wait(start_delay); // 초기 지연 또는 0시간 델타 대기로 시작
        for (std::size_t i = 0; i < received.size(); ++i) { // 네 번 읽어 순서와 누락을 검사할 기록 생성
            received[i] = fifo.read(); // 비어 있으면 데이터 쓰기 이벤트까지 대기
            arrived_ns[i] = sc_core::sc_time_stamp().value(); // 값을 실제로 얻은 시각 기록
            if (i + 1 < received.size()) { // 마지막 읽기 뒤에는 새 타이머가 필요하지 않음
                sc_core::wait(interval); // 처리 시간이 지난 뒤 다음 항목 요구
            } // 다음 읽기 준비 조건 끝
        } // 소비 순회 끝
    } // 소비 프로세스 종료
}; // FIFO 모듈 정의 끝

int sc_main(int argc, char* argv[]) { // SystemC 라이브러리가 호출하는 시뮬레이션 진입점
    const std::string mode = argc == 1 ? "slow" : argv[1]; // 인수가 없으면 역압이 생기는 기본 실험
    if (argc > 2 || (mode != "slow" && mode != "fast" && mode != "bad-expectation")) { // 허용하지 않은 실행 조건 차단
        std::cerr << "usage: fifo_demo [slow|fast|bad-expectation]\n"; // 올바른 모드 안내
        return 2; // 사용법 오류와 검사 실패를 구분
    } // 인수 검사 끝
    const bool fast = mode == "fast"; // 빠른 소비 실험 여부
    sc_core::sc_set_time_resolution(1, sc_core::SC_NS); // value()의 한 tick을 1ns로 고정
    FifoDemo demo("demo", fast); // 생산자·소비자·채널을 실제 SystemC 커널에 등록
    sc_core::sc_start(); // 실행할 프로세스나 미래 이벤트가 없을 때까지 실제 엔진 실행
    const std::array<std::uint64_t, 4> expected_requested = fast // 독립 손계산으로 정한 요청 시각
        ? std::array<std::uint64_t, 4>{1, 2, 3, 4} : std::array<std::uint64_t, 4>{1, 2, 6, 10}; // 이전 수락 후 1ns 규칙 반영
    const std::array<std::uint64_t, 4> expected_accepted = fast // 독립 손계산으로 정한 수락 시각
        ? std::array<std::uint64_t, 4>{1, 2, 3, 4} : std::array<std::uint64_t, 4>{1, 5, 9, 13}; // 느린 소비에서는 빈칸이 생길 때까지 대기
    std::array<std::uint64_t, 4> expected_arrived = fast // 독립 손계산으로 정한 도착 시각
        ? std::array<std::uint64_t, 4>{1, 2, 3, 4} : std::array<std::uint64_t, 4>{5, 9, 13, 17}; // 소비 시작과 읽기 간격 반영
    if (mode == "bad-expectation") { // 검사기가 잘못된 기대값을 잡는지 확인하는 음성 대조
        ++expected_arrived.back(); // 마지막 도착 기대값만 17ns에서 18ns로 틀리게 변경
    } // 음성 대조 설정 끝
    const bool passed = demo.received == demo.values // 네 값의 개수·내용·순서를 함께 비교
        && demo.requested_ns == expected_requested // write 요청의 실제 시간 비교
        && demo.accepted_ns == expected_accepted // 역압으로 지연된 수락 시간 비교
        && demo.arrived_ns == expected_arrived // read 완료 시간 비교
        && sc_core::sc_time_stamp().value() == (fast ? 4U : 17U); // 마지막 이벤트 이후 불필요한 대기가 없는지 확인
    std::cout << "SystemC " << sc_core::sc_release() << '\n'; // 링크한 실제 라이브러리의 릴리스 문자열 출력
    std::cout << "mode=" << mode << " fifo_capacity=1\n"; // 실험 조건 표시
    std::cout << "value request_ns accept_ns arrival_ns blocked_ns\n"; // 네 종류 시각과 대기 시간 열 이름
    for (std::size_t i = 0; i < demo.values.size(); ++i) { // 네 전송의 실제 기록 출력
        std::cout << demo.received[i] << ' ' << demo.requested_ns[i] << ' ' // 읽은 값과 요청 시각 출력
                  << demo.accepted_ns[i] << ' ' << demo.arrived_ns[i] << ' ' // 수락 시각과 도착 시각 출력
                  << demo.accepted_ns[i] - demo.requested_ns[i] << '\n'; // 생산자가 막힌 시뮬레이션 시간 계산
    } // 전송 기록 출력 끝
    std::cout << (passed ? "PASS" : "FAIL") << '\n'; // 실행 완료와 기대값 일치를 구분하는 최종 판정
    return passed ? 0 : 1; // 검사 실패를 프로세스 종료 코드에 반영
} // 시뮬레이션 진입점 끝
```

## 어디에 쓰는지와 한계

버퍼 크기·생산 간격·소비 간격이 처리 지연에 주는 영향을 미리 살펴보는 작은 시스템 모델에 사용할 수 있습니다. 실제 SoC의 여러 블록을 나누고 상호작용을 평가하는 맥락과 연결되지만, 이 예제는 TLM 소켓·버스 프로토콜·프로세서 모델까지 구현하지 않습니다. 큐에 저장되는 값은 호스트 C++의 `int`이며 특정 비트 폭의 하드웨어 데이터 경로를 검증하지 않습니다.

시뮬레이션의 1ns는 모델이 정한 시간 단위입니다. 컴퓨터에서 프로그램이 실행되는 데 걸린 벽시계 시간이나 물리 회로의 전파 지연 측정값이 아닙니다. 클록 핀, 동기 리셋, `valid/ready` 에지 동작, 합성, 배치·배선, 정적 타이밍, 보드·실리콘은 검사하지 않았습니다. 확인한 범위는 네 원소와 두 소비 속도에서 값·순서·시간 규칙이 일치한다는 로컬 결과입니다.

전송 수를 N으로 늘린 같은 구조에서는 기록 배열이 O(N) 공간을 사용하고 FIFO 저장 용량은 O(1)입니다. 이 두 프로세스가 만드는 이벤트 수는 N에 비례하며, 예제처럼 동시에 예약하는 이벤트 수가 제한된 조건에서 처리량도 N에 비례합니다. 일반적인 SystemC 모델 전체의 성능 보장은 아닙니다.

## 출처와 코드 이용 조건

- [Accellera SystemC 배포표](https://accellera.org/downloads/standards/systemc)의 Current Releases에서 3.0.2와 TLM 포함 범위를 확인합니다.
- [3.0.2 INSTALL.md](https://github.com/accellera-official/systemc/blob/3.0.2/INSTALL.md)의 System Requirements·CMake 설치와 [SystemC 소개](https://systemc.org/overview/systemc/)를 실행 환경·용도 설명의 근거로 사용합니다.
- [3.0.2 sc_fifo.h](https://github.com/accellera-official/systemc/blob/3.0.2/src/sysc/communication/sc_fifo.h)의 블로킹 호출·이벤트 통지 동작을 확인합니다.
- 외부 SystemC 라이브러리는 [Apache-2.0 LICENSE](https://github.com/accellera-official/systemc/blob/3.0.2/LICENSE)와 [NOTICE](https://github.com/accellera-official/systemc/blob/3.0.2/NOTICE)를 따릅니다. 라이브러리 소스·바이너리를 이 폴더에 복사하지 않았으며, 의존성을 재배포하는 경우 해당 고지를 유지해야 합니다.

회로 전송 조건, 기대 시각, C++ 예제와 설명은 직접 작성했습니다. 외부 예제나 문제 본문을 복사한 풀이가 아니며 온라인 채점 통과 기록도 아닙니다.

## CMakeLists.txt의 전체 코드

```cmake
cmake_minimum_required(VERSION 3.16) # 예제에서 사용하는 CMake 기능의 하한
project(systemc_fifo_demo LANGUAGES CXX) # C++로 실행하는 SystemC 예제
find_package(SystemCLanguage CONFIG REQUIRED) # 별도 설치한 SystemC 패키지 검색
add_executable(fifo_demo example.cpp) # 실제 시뮬레이션 실행 파일 생성
target_link_libraries(fifo_demo PRIVATE SystemC::systemc) # 이벤트 커널과 채널 구현 연결
target_compile_features(fifo_demo PRIVATE cxx_std_17) # SystemC 3 계열과 맞춘 C++17
```

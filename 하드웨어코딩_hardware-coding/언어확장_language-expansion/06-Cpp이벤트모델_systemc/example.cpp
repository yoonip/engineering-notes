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

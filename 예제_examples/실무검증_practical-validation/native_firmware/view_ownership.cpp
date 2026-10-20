// 잘못된 계약은 정의된 접근으로 대조하며 무효 포인터를 역참조하지 않습니다.
#include <array>        // array: 크기가 고정된 소유 컨테이너입니다.
#include <cassert>      // assert: 검사 조건을 실행 중 확인합니다.
#include <iostream>     // cout: 표준 출력 스트림입니다.
#include <optional>     // optional: 값이 없을 수 있음을 나타냅니다.
#include <string>       // string: 문자 저장 공간을 소유합니다.
#include <string_view>  // string_view: 소유하지 않는 문자 범위입니다.
#include <vector>       // vector: 연속 원소를 소유하는 가변 배열입니다.
#ifdef NDEBUG
#error "This executable requires active assertions; compile with -UNDEBUG."
#endif

struct Handle { std::size_t index; unsigned generation; };

class Samples {
    std::vector<int> values{37};
    unsigned generation = 0;
public:
    Handle borrow(std::size_t i) const { return {i, generation}; }
    std::optional<int> read(Handle h) const {
        if (h.generation != generation || h.index >= values.size()) return std::nullopt;
        return values[h.index];
    }
    void grow() {
        values.reserve(values.capacity() + 1); // 기존 용량보다 크게 요구해 재할당합니다.
        ++generation; // 이 클래스가 발행한 이전 핸들을 명시적으로 만료시킵니다.
    }
};

int main() {
    std::array<char, 6> receive{'R', 'E', 'A', 'D', 'Y', '\0'};
    std::string_view borrowed(receive.data(), 5);
    std::string owned(borrowed); // 복사해 수신 버퍼와 수명을 분리합니다.
    const std::array<char, 5> next{'E', 'R', 'R', 'O', 'R'};
    for (std::size_t i = 0; i < next.size(); ++i) receive[i] = next[i];
    assert(borrowed == "ERROR" && owned == "READY");
    std::cout << "borrowed=" << borrowed << " owned=" << owned << '\n';

    const char packet[] = "PASS,FAULT";
    const std::string_view status(packet, 4);
    const std::string lost_bound(status.data()); // 포인터 생성자는 첫 NUL까지 읽습니다.
    const std::string kept_bound(status); // 뷰 생성자는 길이 4를 유지합니다.
    assert(lost_bound == "PASS,FAULT" && kept_bound == "PASS");
    std::cout << "lost_bound=" << lost_bound << " kept_bound=" << kept_bound << '\n';

    Samples samples;
    Handle before = samples.borrow(0);
    assert(samples.read(before).value() == 37);
    samples.grow();
    assert(!samples.read(before).has_value());
    const Handle rebound = samples.borrow(0);
    assert(samples.read(rebound).value() == 37);
    std::cout << "stale_handle=rejected rebound=" << samples.read(rebound).value() << '\n';
    std::cout << "ownership contract checks passed\n";
}

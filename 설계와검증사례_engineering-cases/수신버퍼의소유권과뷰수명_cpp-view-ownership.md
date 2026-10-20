# 수신 버퍼의 소유권과 뷰 수명 / Receive-buffer ownership and view lifetime in C++

수신 데이터를 복사하지 않고 다루면 할당과 복사 비용을 줄일 수 있습니다. 그 대신 누가 메모리를 소유하고 언제 다시 쓰는지 계약이 필요합니다. 이 글은 `std::string_view`와 `std::vector`를 사용해 내용 변경, 범위 정보 손실, 재할당 후 핸들 만료를 구분합니다. 직접 만든 교육 예제로 논리 오류를 재현하며, 이미 수명이 끝난 포인터를 읽고 그 결과를 정답처럼 해석하지 않습니다.

[C++17 실행 코드](../예제_examples/실무검증_practical-validation/native_firmware/view_ownership.cpp), [실행 방법](../예제_examples/실무검증_practical-validation/native_firmware/README.md), [실행 기록](검증기록_evidence/C펌웨어경계검사_20261021.md)을 연결했습니다.

## 1. 메모리 주소가 유효해도 과거 데이터는 아닙니다

자체 예제의 수신 버퍼는 길이가 6인 `std::array<char, 6>`입니다. 처음 다섯 글자에는 `READY`가 들어 있고 마지막에는 문자 값 0인 NUL이 들어 있습니다. `std::array`는 이 저장 공간을 소유합니다. `std::string_view`는 문자 범위의 위치와 길이를 제공하지만 원본 문자열의 독립적인 복사본을 만들지 않습니다.

```cpp
std::string_view borrowed(receive.data(), 5); // 범위 [시작 주소, 시작 주소+5)를 빌립니다.
std::string owned(borrowed); // 같은 다섯 글자를 새 문자열 저장 공간에 복사합니다.
for (std::size_t i = 0; i < next.size(); ++i) receive[i] = next[i];
// for는 반복문, []는 원소 접근, ++i는 인덱스를 하나 증가시키는 연산입니다.
```

그다음 버퍼를 같은 길이의 `ERROR`로 덮어씁니다. 배열은 여전히 살아 있고 크기도 변하지 않았으므로 이 접근은 정의된 동작입니다. 하지만 두 변수의 의미는 갈라집니다.

| 보관 방식 | 다음 프레임으로 버퍼를 덮어쓴 뒤 | 유지하는 계약 |
| --- | --- | --- |
| `string_view` | `ERROR`를 읽습니다. | 현재 버퍼의 같은 범위를 봅니다. |
| `string` 복사 | `READY`를 읽습니다. | 보관 시점의 다섯 글자를 유지합니다. |

로그 큐에 과거 상태를 남기려는 코드가 뷰만 저장했다면 이것은 논리 오류입니다. 반대로 즉시 파싱하는 함수가 반환 전에 처리를 끝내고 원본이 그동안 유지된다면 뷰 사용이 적합할 수 있습니다. 복사 자체가 늘 옳거나 뷰 자체가 위험한 것이 아니라, 필요한 시간 범위와 실제 소유권이 맞아야 합니다.

실제 비동기 로거에서는 메시지 값의 복사, 공유 소유권으로 유지하는 불변 버퍼, 풀에서 빌린 버퍼의 반환 시점 같은 선택지가 있습니다. 큐에 넣는 순간 처리까지 끝났다고 생각하면 원본 버퍼 재사용과 소비자 실행이 충돌할 수 있습니다. 이번 예제는 스레드 없이 덮어쓰기 순서를 명시해 이 계약 오류만 분리했습니다.

## 2. `data()`는 길이를 함께 넘겨 주지 않습니다

두 번째 입력은 NUL로 끝나는 전체 배열 `PASS,FAULT`입니다. 첫 네 글자만 상태 필드로 보는 뷰를 만듭니다. 버퍼는 정상이며 모든 문자를 읽을 수 있지만, 어느 생성자를 사용하는지에 따라 결과가 다릅니다.

```cpp
const std::string_view status(packet, 4); // const는 이 뷰 변수를 바꾸지 않는다는 뜻입니다.
const std::string lost_bound(status.data()); // char 포인터 생성자는 첫 NUL까지 읽습니다.
const std::string kept_bound(status); // 뷰를 받는 생성자는 뷰의 길이 4를 유지합니다.
```

`lost_bound`는 `PASS,FAULT`, `kept_bound`는 `PASS`가 됩니다. `status.data()`가 잘못된 주소이기 때문이 아닙니다. 원래 뷰의 길이 정보가 함수 호출 경계를 넘지 못했기 때문입니다. 이 예제에서 `PASS,FAULT` 전체를 읽는 일은 할당 범위 안이며 정의되지 않은 동작도 아닙니다. 다만 상태 필드를 읽는다는 요구와 결과가 다릅니다.

로그나 C API에 `view.data()`를 전달할 때도 같은 점을 확인해야 합니다. 상대 API가 NUL 종료 문자열을 받는지, 포인터와 길이를 함께 받는지 구분합니다. 원본에 NUL이 없다면 첫 번째 생성자 사용은 범위 밖 읽기로 이어질 수도 있으나, 여기서는 그 위험한 입력을 실행하지 않았습니다. 길이가 필요한 API에는 시작 주소와 바이트 수를 함께 넘기거나 `std::string(view)`로 독립적인 NUL 종료 문자열을 만듭니다.

## 3. `vector`의 재할당은 별도의 문제입니다

`std::vector<int>`는 정수를 연속된 공간에 저장하는 가변 배열입니다. `size()`는 실제 원소 수이고 `capacity()`는 재할당 없이 담을 수 있는 원소 수입니다. 원래 용량보다 큰 값을 `reserve()`에 주어 재할당이 발생하면 기존 원소의 참조·포인터·반복자는 무효가 됩니다. 이 규칙은 [C++17 공개 초안 N4659의 26.3.11.3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf)에서 확인했습니다.

무효 포인터를 역참조해서 같은 숫자가 나왔다고 유효성을 판단할 수는 없습니다. 해제된 공간이 한동안 같은 내용을 가질 수도 있고, 최적화가 예상과 다르게 동작할 수도 있습니다. 이 사례는 ASan을 실행했다고 주장하지 않으며, 무효 포인터의 실제 읽기도 하지 않습니다. 대신 `index + generation` 핸들로 재할당 이후 접근을 명시적으로 거부하는 작은 클래스를 실행합니다.

```cpp
Handle borrow(std::size_t i) const { return {i, generation}; }
// { }는 두 멤버를 초기화하며 현재 세대 번호와 원소 위치를 묶습니다.
std::optional<int> read(Handle h) const {
    if (h.generation != generation || h.index >= values.size()) return std::nullopt;
    // ||는 하나라도 참이면 참이며, 만료되거나 범위를 벗어난 핸들을 거부합니다.
    return values[h.index]; // optional<int>에 정수 값을 담아 반환합니다.
}
void grow() {
    values.reserve(values.capacity() + 1); // 현재 용량을 초과하므로 재할당을 요구합니다.
    ++generation; // 이 클래스가 발행한 예전 핸들을 모두 만료시킵니다.
}
```

`std::optional<int>`는 정수 값이 있거나 없는 상태를 나타냅니다. `std::nullopt`는 값이 없다는 표식입니다. 따라서 오류를 숫자 `-1` 같은 정상 데이터와 섞지 않고 호출자가 `has_value()`로 확인할 수 있습니다. 벡터와 세대 번호는 클래스의 비공개 멤버로 두어 외부에서 세대 갱신을 빼먹고 `reserve()`만 호출하는 일을 막았습니다.

이 구현의 핸들은 원소의 영구 식별자가 아닙니다. 원소 삭제·정렬이 허용되는 시스템에서는 인덱스가 가리키는 대상을 별도로 추적해야 합니다. 세대 번호도 unsigned 정수이므로 무한히 증가하지 않습니다. 매우 오래 보관되는 핸들에는 번호 순환 정책이나 더 넓은 식별자, 소유 객체의 수명 규약이 필요합니다. 이번 코드는 한 번의 재할당을 이해하기 위한 제한된 계약입니다.

## 4. 재현 결과와 판정

2026-10-21 Windows x86-64에서 Zig 0.17.0의 C++ 드라이버, C++17, `-O2 -UNDEBUG -Wall -Wextra -Werror`로 빌드했습니다. 실행 출력은 다음과 같습니다.

```text
borrowed=ERROR owned=READY
lost_bound=PASS,FAULT kept_bound=PASS
stale_handle=rejected rebound=37
ownership contract checks passed
```

첫 줄은 수신 버퍼 재사용 뒤에도 과거 값을 보관하려면 소유 복사가 필요하다는 직접 대조입니다. 두 번째 줄은 포인터만 넘겨 필드 범위를 잃는 오류입니다. 세 번째 줄은 재할당 전 핸들을 거부하고 재발급한 핸들에서 기존 원소 값 37을 읽었음을 나타냅니다. 원소 수는 늘리지 않았으며, `reserve`가 크기까지 늘렸다고 해석하면 안 됩니다.

```powershell
python run_cases.py --zig C:/tools/zig/zig.exe --output C:/temp/ownership-review-new
```

명령은 [코드 폴더](../예제_examples/실무검증_practical-validation/native_firmware/README.md)에서 실행합니다. 러너는 새 폴더만 허용하고 소스 해시·컴파일 인수·종료 코드·출력을 남깁니다. 각 실행 파일은 `NDEBUG`가 정의된 채라면 빌드를 거부하므로 조건 검사를 없앤 최적화 빌드를 성공 결과로 남기지 않습니다.

## 5. 문제를 좁혀 가는 방법

주소가 유효한지, 원본 내용이 바뀌었는지, 원본 수명이 끝났는지, 길이 전달을 잃었는지를 서로 다른 질문으로 나눕니다. 버퍼 ID와 세대, 원소 수, 큐 삽입·소비 시점, 복사 여부를 함께 기록하면 어떤 계약이 어긋났는지 확인하기 쉽습니다. 원본 메모리가 해제됐다고 의심하면 재현 프로그램을 별도 프로세스에서 AddressSanitizer 등으로 검사하는 방법이 있지만, 이번 실행 결과에는 그 검사를 포함하지 않습니다.

할당 금지 구간에서는 무조건 `string`을 쓰기 어려울 수 있습니다. 최대 길이가 정해진 메시지는 고정 크기 소유 버퍼로 복사할 수 있고, 큰 프레임은 풀의 버퍼 반환을 소비자 완료 이후로 미룰 수도 있습니다. 선택할 때에는 평균 복사 비용만 아니라 최대 지연, 큐에 쌓일 수 있는 수, 할당 실패 처리와 버퍼 회수 경로를 함께 봅니다. 이번 코드는 성능 벤치마크나 실시간 보장을 제공하지 않습니다.

## 확인 문제

1. `const string_view`를 사용하면 원본 버퍼를 다른 코드가 수정하지 못합니까?
2. `reserve(100)` 뒤 원소 수가 100이 됩니까?
3. 뷰로부터 `string`을 만들 때 `string(view.data())`와 `string(view)`는 언제 다른 결과를 냅니까?

답: 1. 그렇지 않습니다. 뷰를 통해 문자를 수정하지 않는 것과 원본이 불변인 것은 다릅니다. 2. 아닙니다. 용량과 크기는 다르며 `reserve`는 원소 수를 늘리지 않습니다. 3. 뷰가 NUL 앞의 일부만 가리키거나 중간에 NUL을 포함하는 등, 뷰 길이와 NUL로 정한 길이가 다를 때입니다.

## English

The executable separates three contracts without dereferencing an invalid pointer. Reusing a live receive array changes a borrowed view from READY to ERROR while an owning copy retains READY. Passing only `data()` loses a four-character field boundary and yields PASS,FAULT. A small generation-checked wrapper rejects a handle after forced vector reallocation and permits a newly acquired handle to read 37. This is a deterministic host demonstration, not an ASan run, concurrency test, or allocation-latency benchmark.

## 출처와 읽은 범위

- [WG21 N4659, 2017-03-21](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf): 24.3.2.2의 문자열 생성자, 24.4의 뷰, 26.3.11.3의 `vector` 재할당을 확인했습니다. 공개 초안이며 실행 표준을 C++17로 지정했습니다.
- [현재 C++ 작업 초안의 vector.capacity](https://eel.is/c++draft/vector.capacity), [string.view.template](https://eel.is/c++draft/string.view.template): 용량·무효화 규칙을 대조했습니다. 최신 초안 전체를 C++17 기능으로 취급하지 않았습니다.
- 상태 문자열, 세대 핸들, 입력과 출력은 직접 구성한 교육 예제입니다.

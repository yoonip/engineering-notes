# C/C++와 펌웨어 경계 검사 / C, C++ and firmware contract checks

직접 만든 교육용 오류와 수정 경로를 같은 입력에서 대조하는 호스트 실행 예제입니다. 기존 제품의 버그, 장치 실측, MCU 인터럽트 시험으로 소개하지 않습니다.

| 코드 | 재현하는 문제 | 함께 읽을 해설 |
| --- | --- | --- |
| [frame_bounds.c](frame_bounds.c) | 32비트 길이 축약, 잘린 프레임, 남는 바이트, 바이트 순서 | [이진 프레임의 길이와 바이트 순서](../../../설계와검증사례_engineering-cases/이진프레임의길이와바이트순서_c-frame-bounds.md) |
| [view_ownership.cpp](view_ownership.cpp) | 수신 버퍼 재사용, 문자열 범위 손실, 재할당 후 핸들 만료 | [수신 버퍼의 소유권과 뷰 수명](../../../설계와검증사례_engineering-cases/수신버퍼의소유권과뷰수명_cpp-view-ownership.md) |
| [ring_publish_model.c](ring_publish_model.c) | 조기 공개의 오래된 값 읽기, 공유 카운터 갱신 유실 | [링 버퍼의 공개 순서와 공유 카운터](../../../설계와검증사례_engineering-cases/링버퍼의공개순서와공유카운터_ring-publication.md) |

## 실행 환경과 명령

Python 3.10 이상과 C11·C++17 컴파일러가 필요합니다. Python은 빌드·실행 기록만 관리하며 알고리즘은 C/C++ 실행 파일에서 수행합니다. Python 외부 패키지는 필요하지 않습니다. 2026-10-21 기록에서는 Python 3.12.14와 Zig 0.17.0의 C/C++ 드라이버를 Windows x86-64에서 사용했습니다.

이 폴더에서 실행합니다. GCC를 사용하려면 `gcc`와 `g++`가 PATH에 있어야 합니다.

```powershell
python run_cases.py --output C:/temp/native-contract-run-new
```

Zig의 드라이버를 지정하는 명령입니다. 경로는 설치 위치에 맞게 바꿉니다.

```powershell
python run_cases.py --zig C:/tools/zig/zig.exe --output C:/temp/native-zig-run-new
```

다른 이름의 GCC 실행 파일은 `--cc`와 `--cxx`로 지정할 수 있습니다. 출력 폴더가 이미 있으면 덮어쓰지 않고 중단합니다. 각 실행 파일은 `-O2 -UNDEBUG -Wall -Wextra -Werror`로 빌드하며, C/C++ 표준은 각각 C11·C++17입니다. `assert`를 제거하는 `NDEBUG`가 남아 있으면 소스의 `#error`가 빌드를 거부합니다.

출력 폴더에는 실제 빌드한 소스 복사본, 실행 파일, 빌드·실행 로그, `results.json`이 생깁니다. JSON은 환경·실행 인수·종료 코드·표준 출력·오류 출력·C/C++ 소스 SHA-256을 담습니다. 컴파일 실패나 실행 실패는 러너의 종료 코드 1로 전달합니다. 성공이면 종료 코드 0입니다.

## 해석할 때 구분할 것

- 프레임 예제의 잘못된 경로는 길이 승인만 재현합니다. 승인된 잘못된 크기로 메모리를 읽지 않습니다.
- C++ 예제는 정의된 버퍼 수정과 범위 손실을 대조합니다. 무효 포인터의 역참조나 ASan 검사는 수행하지 않습니다.
- 링 버퍼의 여섯 사건 순서는 한 스레드가 열거하는 모델입니다. C11 SPSC 구현의 full/empty·FIFO·wrap 검사는 순차 실행이며, 실제 동시 실행·ISR·DMA·캐시 시험은 아닙니다.
- 교육용 잘못된 경로의 관측값이 예상대로 나오는지를 검사하므로, 프로그램의 성공은 그 잘못된 구현을 사용해도 된다는 뜻이 아닙니다.

[날짜별 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/C펌웨어경계검사_20261021.md)에서 관측값과 한계를 확인할 수 있습니다.

## English

These fixtures contrast deliberately faulty and corrected contracts using native C/C++ execution. The Python runner records compiler invocations, source hashes, exit codes, and output in a new directory. No invalid-pointer dereference, physical instrument access, MCU interrupt execution, or concurrent stress test is claimed.

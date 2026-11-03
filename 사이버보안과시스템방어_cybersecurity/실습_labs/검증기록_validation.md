# 실습 검사 기록 | Lab validation record

[분야 목차](../README.md) · [실습 코드](README.md) · [출처와 판본](../출처_sources.md)

## Python 단위 검사

2026-11-04에 Python 3.13.14에서 다음 명령을 실행했습니다.

```text
python -B -m unittest discover -s 사이버보안과시스템방어_cybersecurity\실습_labs -p test_security.py -v
Ran 38 tests in 0.016s
OK
```

검사는 SQL 입력 경계, 객체 권한, AI 도구 호출의 허용 목록과 인수 형식, 합성 로그인 시간창, HTML 텍스트 인코딩, SHA-256 기준값, HMAC 태그·시각·재전송 검사를 포함합니다. HMAC 표준 벡터는 RFC 4231 §4.2의 공개 예시와 대조합니다. 각 테스트는 로컬의 고정된 입력을 사용하며 외부 서비스나 계정에 접속하지 않습니다.

## C 프레임 경계 검사

`frame_bounds.c`와 `test_frame_bounds.c`는 C11로 빌드했습니다. `assert`가 비활성화되는 빌드를 막기 위해 테스트 소스는 `NDEBUG`가 설정된 경우 컴파일 오류를 냅니다. 실행 파일은 Zig의 C 호환 프런트엔드로 아래 옵션을 사용해 만들었습니다.

```text
zig cc -std=c11 -UNDEBUG -Wall -Wextra -Werror -O1 -g test_frame_bounds.c -o frame_bounds_test.exe
```

실행 출력은 다음과 같습니다.

```text
C boundaries: 7 cases + 65536 length headers passed
```

일곱 가지 명시적 사례에는 정상 프레임, 빈 자료, 잘린 헤더·본문, 허용 상한, 상한 초과가 포함됩니다. 추가로 16비트 길이 필드의 모든 값 0~65535를 검사했습니다. 이 테스트는 해당 함수의 로컬 경계 처리만 확인하며, 네트워크 스택이나 운영체제 전체의 안전성을 증명하지 않습니다.

## 실행한 소스의 SHA-256

아래 해시는 검증에 사용한 Python·C 소스의 SHA-256입니다. 테스트를 다시 실행하기 전 파일이 바뀌었는지 대조할 수 있습니다.

| 파일 | SHA-256 |
| --- | --- |
| `access_control.py` | `273f48b00141c2da2e097731a9f0b2ed97d7f63ec4c8d3a3d4e261c27a7afdae` |
| `agent_boundary.py` | `af49ca9664fb5de44223c7b677b08c731e594f297a827264c291a997a8b180b7` |
| `artifact_digest.py` | `34d037ad73f2d403154db6c09f1b6630f28a4e71c493c5943a6458c4299ec345` |
| `login_detection.py` | `e542a2bf139d7f0e008e7e9725504506998e748962e9d942630f1c662eaff422` |
| `output_encoding.py` | `bc0ee4620d2463ede9306b046046c11db8b03256bd8a2c848f5aba08f630b118` |
| `sql_boundary.py` | `2ac8a04d94cb058200d1508dfcbbc4c6bfa63ea435f53d48358fbb5aff0f2b8d` |
| `test_security.py` | `aebcac3ba140e8dedecc2470f9152ddcc551161f07e627ebef98bd5aca747102` |
| `webhook_auth.py` | `4b52982836584f8dc7b5bf27aa1cb15d32bec9c51146087d88b42bc4cd7021c8` |
| `frame_bounds.c` | `f8aca146c4604f534f2ff59b8ed463790101ad60f277569b401a642af5dc0696` |
| `test_frame_bounds.c` | `d05b8c25d6f6bbc3a6331399101b21122452e8eb4268e28e6176accb70c39ed0` |

## 검증 범위

결과는 이 저장소에 포함된 교육용 함수와 테스트 입력에 한정됩니다. 정적 분석기·동적 분석기·fuzzer·침투 시험 결과가 아니며, 기업 제품이나 상용 보안 통제의 인증 결과도 아닙니다. C 프레임 예제는 `memcpy`를 사용하므로 입력·출력 메모리 구간이 겹치지 않는다는 호출 전제가 있습니다. 겹칠 수 있는 인터페이스라면 범위를 검증한 뒤 `memmove` 사용 여부를 설계해야 합니다. 함수 호출 전에 필요한 신원 확인, 키 보관, 동시 요청 간 재전송 상태 공유, 실제 HTTP 프레임 파싱, 파일 digest 기준값의 신뢰성은 별도의 시스템 설계와 시험이 필요합니다.

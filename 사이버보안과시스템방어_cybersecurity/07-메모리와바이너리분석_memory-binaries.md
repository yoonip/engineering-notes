# 메모리와 바이너리 분석 | Memory safety and binary analysis

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## C의 포인터는 용량을 자동으로 알려 주지 않습니다

배열 밖 접근, 해제 후 사용, 이중 해제, 정수 overflow·underflow는 입력 처리의 의미를 바꿀 수 있습니다. ‘수신한 길이’와 ‘실제 버퍼 길이’, ‘복사할 자료 길이’와 ‘목적지 용량’을 따로 봐야 합니다. 헤더가 2바이트인데 먼저 `len - 2`를 계산하면 부호 없는 크기형에서 매우 큰 값으로 돌아갈 수 있습니다. [SEI CERT C ARR30-C](https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts)

실습은 헤더를 읽기 전에 `len >= 2`를 확인하고, 헤더 길이가 실제 자료 길이와 같으며 목적지 용량 이하인 경우만 복사합니다. 입력과 출력 메모리는 유효하고 서로 겹치지 않는다는 호출 계약이 있습니다. C 함수에 전달한 포인터가 실제로 그 길이만큼 유효한지는 이 함수가 독립적으로 알아낼 수 없습니다. 겹치는 구간에는 `memcpy`의 계약도 성립하지 않습니다.

## 작은 정상 예제와 모든 길이 헤더를 대조합니다

입력 `[0, 3, 10, 20, 30]`은 길이3·본문3바이트입니다. 목적지 용량3은 성공하고 용량2는 실패해야 합니다. 검증 코드는 헤더의 0~65535 전체 값을 넣되 실제 본문을 3바이트로 고정합니다. 따라서 헤더가 3인 경우에만 성공해야 한다는 독립 기대값을 사용할 수 있습니다. 거부된 입력이 목적지를 바꾸지 않는지도 봅니다.

이 검사는 가능한 모든 포인터·메모리 레이아웃·동시 실행에 대한 증명이 아닙니다. 검사한 배열의 길이 경계와 출력 조건에 대한 실행 근거입니다. 이 기록과 컴파일러 진단을 함께 읽습니다.

## 컴파일러 방어와 분석 도구

| 방법 | 얻는 근거 | 남는 범위 |
| --- | --- | --- |
| 경고·정적 분석 | 소스의 의심스러운 경로를 찾습니다. | 모델링과 설정에 따라 누락·오탐이 있습니다. |
| ASan | 실행한 경로의 범위 오류·해제 후 사용 등을 탐지합니다. | 실행하지 않은 경로는 별도입니다. |
| UBSan | 일부 정의되지 않은 동작을 실행 중 찾습니다. | 모든 논리 오류를 찾지는 않습니다. |
| coverage-guided fuzzing | 새 코드 경로로 이어지는 입력을 탐색합니다. | 테스트 harness와 oracle이 있어야 합니다. |
| 메모리 안전 언어 | 여러 종류의 메모리 오류를 설계 단계에서 줄입니다. | unsafe·FFI·논리·권한 오류는 별도로 다룹니다. |

[Clang ASan](https://clang.llvm.org/docs/AddressSanitizer.html)과 [LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html)는 각각 런타임 검사와 입력 탐색의 공식 사용법을 제공합니다. 이 저장소의 현재 결과에서 sanitizer 실행 여부는 별도 검증 기록에 표시합니다.

## 역공학이 필요한 경우

소스가 없는 자신 소유의 firmware나 허용된 분석 대상에서는 파일 형식·아키텍처·함수·상수·호출 관계를 확인합니다. 디스어셈블리는 기계어를 명령으로, 디컴파일은 더 높은 수준의 추정 표현으로 보여 줍니다. 디컴파일 결과가 원래의 C 소스와 같다는 뜻은 아닙니다. [Ghidra 공식 저장소](https://github.com/NationalSecurityAgency/ghidra)를 도구 출처로 연결합니다. 이 글은 Ghidra를 실행해 특정 제품의 취약점을 찾은 결과는 아닙니다.

## 코드와 줄별 설명

공식 API·설계 원칙을 참고해 직접 작성한 교육 예제입니다. 기업의 내부 코드나 원문 발췌가 아닙니다. [실행 파일](실습_labs/frame_bounds.c) · [검사 방법과 결과](실습_labs/검증기록_validation.md)

```c
/* 직접 작성한 교육 예제: [길이 2바이트][자료] 프레임을 경계 검사 후 복사합니다. */
#include <stddef.h> /* size_t는 메모리 크기를 나타내는 부호 없는 정수형입니다. */
#include <stdint.h> /* uint8_t는 정확히 8비트인 부호 없는 정수형입니다. */
#include <string.h> /* memcpy는 정해진 바이트 수를 복사합니다. */

int copy_frame(const uint8_t *src, size_t len, uint8_t *dst, size_t cap, size_t *written) { /* 포인터와 각각의 실제 용량을 인수로 받습니다. */
    if (written == NULL) return 0; /* 출력 길이를 쓸 주소가 없으면 실패합니다. */
    *written = 0; /* *는 포인터가 가리키는 값이며 실패 시의 출력 길이를 초기화합니다. */
    if (src == NULL || dst == NULL || len < 2) return 0; /* ||는 논리 OR이며 헤더를 읽기 전에 포인터와 길이를 검사합니다. */
    size_t count = ((size_t)src[0] << 8) | src[1]; /* 형 변환·비트 이동·OR로 big-endian 길이를 계산합니다. */
    if (count != len - 2 || count > cap) return 0; /* 먼저 확인한 len에서 2를 빼므로 underflow를 피하고 실제 자료·목적지 길이를 대조합니다. */
    if (count != 0) memcpy(dst, src + 2, count); /* 포인터 덧셈으로 헤더 뒤를 가리키며 용량 검사를 통과한 바이트만 복사합니다. */
    *written = count; /* 성공한 복사 길이를 호출자에게 기록합니다. */
    return 1; /* int의 1을 성공 값으로 반환합니다. */
} /* 함수 본문을 닫습니다. */
```

## 원문에서 이어 읽기

- [SEI CERT C ARR30-C](https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts): 배열·포인터 범위의 규칙과 예제입니다.
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html): 검출 오류·빌드 방법·제약 절입니다.
- [LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html): coverage-guided fuzzing 소개·사용법·입력 목표 함수입니다.
- [NSA Ghidra](https://github.com/NationalSecurityAgency/ghidra): 공식 README·빌드·역공학 도구 소개입니다.

## English

The C example validates header length and destination capacity before copying. Tests exercise fixed valid buffers; pointer validity and non-overlap remain caller obligations.

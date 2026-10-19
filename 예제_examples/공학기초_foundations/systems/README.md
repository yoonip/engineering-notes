# 시스템 기초 실행 모델 / Executable systems foundations

## 한국어

하드웨어와 소프트웨어가 만나는 경계에서 수치 표현, 시작 코드, DMA, 통신 프레임, 메모리 보호와 인증 규칙을 작은 모델로 확인합니다. 모든 구현은 Python 표준 라이브러리만 사용합니다. 코드 주석은 한국어로 작성했습니다.

저장소 최상위에서 실행합니다.

```bash
python -m unittest discover -s 예제_examples/공학기초_foundations/systems -p "test_*.py" -v
```

| 글 | 구현 | 확인하는 성질 |
| --- | --- | --- |
| [수치 표현과 양자화](../../../분야_topics/04-c-cpp-python/해설_notes/비트에서수까지_numbers-and-quantization.md) | `signed_word`, `quantize`, `fixed_multiply`, `binary32_value` | 비트 해석, 반올림, 포화, 오차 한계, binary32 간격 |
| [컴파일에서 리셋과 main까지](../../../분야_topics/39-컴파일러언어런타임_compilers-languages/해설_notes/C코드가실행되기까지_reset-to-main-and-toolchain.md) | `initialize_ram` | 복사·0 초기화·미변경 영역과 범위 검사 |
| [MMIO·인터럽트·DMA](../../../분야_topics/17-펌웨어-RTOS_firmware-rtos/해설_notes/CPU와장치가같은데이터를다룰때_mmio-interrupt-dma.md) | `DmaBuffer` | 버퍼 소유권, clean/invalidate의 데이터 효과 |
| [UART·프레이밍·CRC](../../../분야_topics/20-인터페이스통신_interfaces-communications/해설_notes/바이트가메시지가되려면_framing-uart-crc.md) | `crc16_x25`, `encode_frame`, `FrameParser` | CRC 기준값, chunk 경계, escape, 저장 상한과 복구 |
| [프로세스·메모리·동시성](../../../분야_topics/07-컴퓨터공학기초_cs-foundations/해설_notes/같은주소다른메모리_processes-memory-concurrency.md) | `translate`, `Page`, interleaving 테스트 | offset 보존, alias, 권한, 잃어버린 갱신 |
| [보안과 신뢰성의 경계](../../../분야_topics/38-보안암호하드웨어신뢰_security-cryptography/해설_notes/오류를찾는것과공격을막는것_security-and-reliability-boundaries.md) | `verify_tag` | 공식 HMAC 벡터, 변조 거부, 재전송 검증의 한계 |

검증에서는 구현과 같은 식을 그대로 반복하는 대신 별도 기준을 사용했습니다. signed 해석은 `int.from_bytes`, CRC는 `binascii.crc_hqx`와 비트 반전, 고정소수점 곱은 인접 정수까지의 거리, HMAC은 RFC4231 case 6과 비교합니다. 동시성은 두 실행 흐름의 가능한 읽기·쓰기 순서를 전부 열거합니다.

2026-10-19에 CPython 3.12.14에서 19개 테스트가 통과했습니다. [기계 판독 결과와 범위](VALIDATION.json)에 실행 조건을 기록했습니다. 이 모델은 실제 MCU 캐시 명령, MMU, OS 스케줄러나 UART 전기 특성을 재현하지 않습니다. 특정 보드의 부팅·DMA 타이밍·보안 인증 결과로 해석하지 않습니다.

## English

These small models examine the hardware/software boundary through number representation, startup, DMA, framing, memory protection, and authentication. They use only the Python standard library. Code comments are in Korean.

Run the command above from the repository root. The six linked articles cover numerical interpretation and quantization, startup memory initialization, DMA ownership and cache effects, bounded framing and CRC, translation and concurrency, and authentication boundaries.

Verification uses separate references rather than merely repeating implementation expressions: `int.from_bytes` for signed words, `binascii.crc_hqx` plus reflection for CRC, nearest-integer distance for fixed-point multiplication, and RFC4231 case 6 for HMAC. The concurrency test exhaustively enumerates two execution flows' read/write interleavings.

All 19 tests passed on CPython 3.12.14 on 2026-10-19. [Machine-readable results and scope](VALIDATION.json) record the environment. These models do not reproduce actual MCU cache instructions, an MMU, an OS scheduler, or UART electrical behavior. They are not board-boot results, real DMA timing measurements, or security certification.

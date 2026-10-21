# 예외 상태로 Cortex-M 고장 원인을 좁히는 방법 / Tracing Cortex-M faults from exception state

`HardFault_Handler`에서 멈췄다는 사실만으로 원인을 알 수는 없습니다. 배열 밖 쓰기가 반환 주소를 덮었거나 외부 메모리 설정이 틀렸을 수 있습니다. 이 글은 Cortex-M7의 상태 레지스터·예외 스택과 GDB로 원인 후보를 나눕니다. 공식 문서와 자체 주소·비트 계산을 확인한 자료이며 실보드 장애 보고서는 아닙니다.

확인일은 2026-10-21입니다. 부품 번호·코어 revision·메모리 지도·SDK·debugger 버전을 고정합니다. 구성이 다른 Cortex-M0·M23 등에 같은 레지스터 목록을 그대로 적용하지 않습니다.

## C/C++ 오류와 하드웨어 예외의 차이

가상 배치에서 `uint32_t buf[16]`이 `0x20001000`에 시작하면 크기는 64바이트, 마지막 원소는 `0x2000103C`입니다. `buf[16]` 쓰기는 `0x20001040`으로 배열 밖입니다. 그래도 접근 가능한 RAM이면 즉시 예외 없이 옆 객체를 손상시키고, 나중에 함수 포인터를 사용할 때 멈출 수 있습니다.

C/C++ 객체 수명·배열 경계는 하드웨어 접근 권한·버스 응답과 다릅니다. 하드웨어가 모든 객체 경계를 알아서 검사하지는 않습니다. 따라서 HardFault 부재는 메모리 안전성의 증명이 아니며, HardFault 하나만으로 포인터 버그를 확정할 수도 없습니다.

| 관측 | 나누어 볼 원인 후보 | 다음 분리 확인 |
| --- | --- | --- |
| 같은 load에서 반복 중단됩니다 | 잘못된 포인터, 미초기화 외부 메모리, 접근 권한 | 명령의 주소 계산과 linker·MPU·장치 지도를 대조합니다 |
| 정상 함수의 복귀 뒤 엉뚱한 코드로 갑니다 | 반환 주소·함수 포인터 손상, 스택 부족 | 저장된 LR·스택 경계와 그 값을 바꾼 writer를 찾습니다 |
| 최적화를 바꾸면 증상이 달라집니다 | 미정의 동작, 배치·타이밍 변화, 경쟁 | 실행 ELF를 보존하고 소스·역어셈블리를 함께 비교합니다 |
| debugger를 멈추면 재부팅합니다 | watchdog 진행, 다른 reset 원인 | 부팅 직후 reset 원인과 debug freeze 설정을 보존합니다 |

## 첫 중단에서 보존할 상태

리셋 전에 ELF·map·빌드 hash와 HFSR·CFSR·주소 레지스터, 진입 당시 LR·MSP·PSP·스택 범위를 보존합니다. HFSR는 HardFault의 배경, CFSR는 MemManage·BusFault·UsageFault의 원인 비트를 보여줍니다. HFSR의 `FORCED`는 다른 fault가 우선순위나 비활성 handler 등으로 HardFault에 올라왔다는 신호이며 원인 이름 자체는 아닙니다.

BFAR·MMFAR는 각각 버스·메모리 보호 오류의 주소입니다. `BFARVALID`·`MMARVALID`와 함께 해석합니다. [Arm M7 안내서](https://documentation-service.arm.com/static/61efd6602dd99944d051417b?token=) §4.3.14는 주소 저장 후 유효 비트를 확인하도록 설명합니다. 높은 우선순위 예외가 값을 바꿀 가능성도 고려합니다.

```c
uint32_t saved_bfar = SCB->BFAR;  // CMSIS의 SCB 정의로 주소 값을 먼저 읽습니다.
uint32_t saved_cfsr = SCB->CFSR;  // 원시 상태 비트를 보존합니다.
bool address_valid =
    (saved_cfsr & SCB_CFSR_BFARVALID_Msk) != 0U;  // 마스크와 AND해 유효 비트를 확인합니다.
```

이 읽기 조각은 표준 정수·bool header와 장치용 CMSIS를 전제로 하며 완성된 handler나 원자적 snapshot은 아닙니다. `printf`·동적 할당·mutex 로그는 손상 상태에서 다시 막힐 수 있습니다. 기록 RAM의 접근·reset 후 보존도 설계합니다. CFSR의 여러 비트는 1을 쓰면 지워지므로 무심코 상태를 지우지 않습니다.

## 저장된 PC와 현재 PC를 구별합니다

정상 예외 진입에서는 중단 문맥의 R0·R1·R2·R3·R12·LR·PC·xPSR를 저장합니다. 현재 handler의 PC는 이 저장 PC와 다릅니다. 진입 시 LR는 복귀 방식 코드인 `EXC_RETURN`이고, 스택 안의 LR는 중단 문맥의 LR입니다.

M7의 `EXC_RETURN=0xFFFFFFFD`는 기본 프레임·PSP를 쓰는 Thread mode 복귀이고, `0xFFFFFFF9`는 기본 프레임·MSP입니다. Handler mode는 MSP로 실행하므로 PSP task의 원래 문맥을 현재 MSP에서 찾으면 틀릴 수 있습니다. C 함수 prologue도 SP·LR를 바꾸므로 첫 명령이나 진입 코드에서 원래 값을 보존합니다.

자체 계산으로 프레임 시작 `0x20001000`에서 PC를 담은 일곱 번째 word의 위치는 `시작 + 6×4 = 0x20001018`입니다. 거기에 든 값이 저장 PC이며 슬롯 주소 자체가 실행 주소는 아닙니다. [Arm §2.3.7 그림 2-2·표 2-15](https://documentation-service.arm.com/static/61efd6602dd99944d051417b?token=)의 M7 배치에서는 부동소수점 확장 공간이 있어도 기본 레지스터는 낮은 주소 쪽입니다. 기본 PC 위치를 18word 뒤로 옮기지 않습니다.

기본 프레임은 32바이트, 부동소수점 확장 공간이 있으면 104바이트이며 정렬용 word 여부도 봅니다. `EXC_RETURN` bit 4와 FPU·lazy stacking 상태를 확인합니다. `STKERR`·`MSTKERR`는 저장 자체의 실패를 뜻할 수 있으므로 그럴듯한 PC도 신뢰하지 않습니다.

가상 스택 `[0x20001000, 0x20001080)`에서 `sp=0x20001070`의 기본 프레임 끝은 `0x20001090`으로 범위 밖입니다. 덧셈 overflow를 피하려면 sp 경계를 먼저 확인한 뒤 `필요바이트 <= 상한 - sp`로 비교할 수 있습니다.

## 상태 비트에서 원인 명령까지

가상 snapshot `HFSR=0x40000000`, `CFSR=0x00008200`에는 HFSR bit 30 FORCED, CFSR bit 15 BFARVALID와 bit 9 PRECISERR가 켜져 있습니다. `BFAR=0x60001004`의 의미는 장치 지도·외부 메모리 초기화·MPU와 대조해야 정해집니다. 모든 STM32에서 잘못된 주소라는 뜻은 아닙니다. 비트 위치는 [CMSIS 6.3.0 core_cm7.h](https://github.com/ARM-software/CMSIS_6/blob/v6.3.0/CMSIS/Core/Include/core_cm7.h#L688-L752)와 대조했습니다.

PRECISERR는 유효한 저장 PC로 명령을 찾고 레지스터·offset에서 접근 주소를 재계산합니다. IMPRECISERR는 비동기 오류여서 저장 PC가 원인 명령을 가리키지 않을 수 있고, 이 비트 자체는 BFAR에 원인 주소를 기록하지 않습니다. 이전 store·버퍼·버스 설정을 나눠 구간별로 조사합니다. 다른 코어의 쓰기 버퍼 처방을 M7에 복사하지 않습니다.

## GDB·SWD로 writer와 시점을 분리합니다

SWD는 프로브와 코어의 디버그 연결이며 GDB는 기호·메모리·명령과 중단 조건을 다룹니다. 연결 성공과 원인 규명은 다릅니다. 다음 주소·심볼은 가상 예시이며 실제 세션 출력이 아닙니다.

```gdb
file firmware.elf
info registers
set $frame = 0x20001000
x/8wx $frame
disassemble /r parse_frame
watch -location guard_word
```

`x/8wx`는 범위를 확인한 4바이트 word 8개를 16진수로 읽습니다. `disassemble /r`는 기계어·명령을, `watch -location`은 특정 위치의 값 변화를 봅니다. [GDB Watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html)처럼 hardware 설정 여부와 자원 한계를 확인합니다. 소프트웨어 대체는 비용·관측 시점을 바꾸며, 코어 watchpoint로 DMA 등 모든 writer를 봤다고 간주하지 않습니다.

guard가 손상됐다면 객체 생성 시점부터 watchpoint를 걸어 최초 writer를 찾습니다. guard 하나가 모든 범위 초과를 검출하지는 않습니다. 인라인·재배치·사라진 지역 변수 때문에 소스와 명령이 일대일 대응하지 않을 수도 있습니다. [GDB Optimized Code](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Optimized-Code.html)에 따라 원래 ELF·debug 정보를 보존합니다. 낮은 최적화에서 증상이 사라져도 수정됐다는 증거는 아닙니다.

## watchdog과 최종 기록

코어를 정지해도 watchdog이나 주변장치가 계속 움직일 수 있습니다. STM32F7 HAL에는 [IWDG·WWDG debug freeze 매크로](https://github.com/STMicroelectronics/stm32f7xx-hal-driver/blob/master/Inc/stm32f7xx_hal.h#L78-L117)가 있지만, 해당 장치·설정에서의 지원을 확인해야 합니다. 개발용 freeze 조건에서 로그를 읽은 것과 debugger 없이 watchdog이 복구 동작을 한 것은 다른 시험입니다. reset 원인 플래그도 부팅 코드가 지우기 전에 보존해야 합니다.

기록에는 입력·반복 조건, firmware hash·옵션·ELF, 첫 원시 상태·유효 비트, 원래 SP·경계·문맥, 확인한 writer를 넣습니다. 같은 입력에서 전후 주소 계산과 반복 여부를 비교합니다. 이 글은 가상 계산만 실행했고 SWD·fault·watchdog 절차는 문서로 확인했습니다.

## 작업 정지와 리셋 원인을 함께 남기는 예

watchdog reset 표시는 “어떤 task가 왜 멈췄는지”까지 알려 주지는 않습니다. fault handler에서 돌아오지 못했을 수도 있고, 예외 없이 무한 대기했을 수도 있습니다. 따라서 reset 원시 플래그와 마지막으로 완료한 업무 checkpoint를 별개로 남깁니다. 임의의 주기 feed를 건강 상태의 증거로 사용하지 않습니다.

[워치독 호스트 모형](../../예제_examples/실무검증_practical-validation/watchdog_reset/README.md)에서 control과 acquire는 252에 한 번씩 진행을 보고하고 acquire만 멈춥니다. 주기 feed 경로는 254·258·262·266·270에 계속 feed합니다. task별 새 sequence와 마지막 보고 나이를 요구하면 254 뒤의 feed를 거부합니다. 같은 보고를 다음 epoch의 진행으로 재사용하지 않는 차이입니다.

이 실행은 8비트 tick과 자체 허용 구간 `[4, 12)`를 사용합니다. 250에서 경과 12의 저장 tick은 6이므로 `now >= deadline`만으로 판단하면 now=254에서도 만료라고 오판합니다. 비교하는 실제 차이가 128 미만이라는 계약 아래 `(now-before)%256`을 사용했습니다. 이는 실제 WWDG downcounter나 밀리초 계산이 아닙니다. 모형의 reset_at=266도 deadline에 배치한 poll의 관측이며 poll 사이 비동기 reset 타이머를 실행한 결과는 아닙니다.

원인 보존의 짧은 코드는 새 예제 폴더의 Python API로 실행했습니다. 아래 1·4는 모형 비트이며 실제 RCC 비트 위치가 아닙니다.

```python
from models import ResetLatch  # from/import는 예제의 상태 저장 클래스를 가져옵니다.
latch = ResetLatch()  # ()는 객체를 만들며 원인 표시는 0으로 시작합니다.
latch.latch("power")  # 메서드 호출로 전원 관련 모형 원인을 남깁니다.
latch.latch("watchdog")  # 다른 원인을 OR로 함께 보존합니다.
saved = latch.capture()  # 읽은 snapshot을 반환한 뒤 표시를 지웁니다.
print(saved["raw"], saved["causes"])  # []로 사전 값을 읽어 5와 두 원인을 출력합니다.
print(latch.capture()["raw"])  # 다시 읽은 0은 이미 보존한 증거를 대신하지 않습니다.
```

실제 출력은 `5 ['watchdog', 'power']`, 다음 줄은 `0`이었습니다. 순서를 바꿔 먼저 clear하는 오류는 raw=0·빈 원인 목록을 남겼습니다. 여러 sticky 비트만으로 사건의 시간 순서를 알아낸 것은 아닙니다. bootloader·초기화 코드가 먼저 소거하지 않는지도 확인해야 합니다. ST RM0368 Rev 6 §6.3.18과 [F4 HAL v1.8.3의 reset flag 조회·소거 매크로](https://github.com/STMicroelectronics/stm32f4xx-hal-driver/blob/v1.8.3/Inc/stm32f4xx_hal_rcc.h)를 대조했습니다.

[사례 본문](../../설계와검증사례_engineering-cases/작업진행을확인하는워치독과리셋기록_watchdog-health-reset.md)은 연속 watchdog 부팅 세 번째에 recovery를 선택하는 자체 정책도 설명합니다. 이력은 부팅 간 보존된다는 모형 가정이며 실제 retained RAM·flash 기록·CRC·전원 상실 검증을 수행하지 않았습니다. [실행 기록](../../설계와검증사례_engineering-cases/검증기록_evidence/워치독진행상태와리셋검사_20261021.md)에서 기본/최적화 실행과 오류 주입을 구분합니다.

## 확인 문제

1. `buf[16]` 쓰기가 배열 밖인데도 HardFault가 즉시 생기지 않을 수 있는 이유는 무엇인가요?
2. 현재 handler의 MSP만 읽으면 PSP를 쓰던 task의 오류 문맥을 놓칠 수 있는 이유는 무엇인가요?
3. CFSR에 IMPRECISERR만 있고 BFARVALID가 0이면 저장 PC와 BFAR를 어떻게 다루어야 하나요?

<details>
<summary>해설</summary>

1. C/C++ 객체 경계와 하드웨어 접근 권한 경계는 다릅니다. 배열 밖 주소도 접근 가능한 RAM이면 옆 데이터를 손상시킨 뒤 나중에 문제가 드러날 수 있습니다.
2. 예외 진입 전 task는 PSP를 사용했어도 handler는 MSP로 실행됩니다. 진입 시 EXC_RETURN으로 원래 스택을 구분하고 prologue·프레임 형식·범위도 확인해야 합니다.
3. IMPRECISERR는 저장 PC가 원인 명령을 가리킨다고 보장하지 않습니다. 유효 비트가 없는 BFAR를 이번 원인 주소로 확정하지 않고 이전 쓰기와 버스 상태를 후보로 조사합니다.

</details>

## 문서와 확인 범위

- Arm DUI 0646B, ID082615, Cortex-M7 r1p1용, Issue B: §2.3.7·그림 2-2·표 2-15, §2.4, §4.3.10~14를 읽었습니다. 그림의 스택 방향도 PDF 39쪽에서 확인했습니다. 코어의 예외·레지스터 정의이며 MCU 전체의 주소·주변장치 명세를 대신하지 않습니다.
- CMSIS 6.3.0 `core_cm7.h`의 CFSR·HFSR 마스크를 확인했습니다. GDB 온라인 매뉴얼은 2026-10-21 열람한 Watchpoints·Optimized Code 절이며, 본문 명령을 실제 대상에서 실행한 기록은 아닙니다.
- ST HAL의 debug freeze 정의는 위 링크의 열람본을 확인했습니다.

## English

Fault analysis separates language-level memory errors, hardware access faults and the later point where corruption is discovered. Preserve the exact ELF, raw status, valid address flags, entry EXC_RETURN and the correct stack before decoding a saved PC. Watchpoints and lower-optimization builds help isolate causes but change observability. Address and bit examples were checked locally; no board fault, SWD session or watchdog experiment was performed.

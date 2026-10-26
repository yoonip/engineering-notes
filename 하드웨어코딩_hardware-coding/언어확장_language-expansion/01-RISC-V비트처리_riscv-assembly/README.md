# RV32I의 비트필드 갱신·바이트 검사합과 C 독립 검사

[하드웨어 코딩 목차](../../README.md) · [실제 명령·해시·집계](example.json)

이 예제는 직접 작성한 RV32I 어셈블리 함수 두 개를 C에서 호출하고 결과를 독립 기준과 비교합니다. 레지스터 값의 일부 비트를 교체하는 update_field와 일반 RAM의 바이트를 더하는 byte_sum입니다. 호스트 PC의 C 프로그램만 실행한 결과가 아니라 RISC-V ELF를 만들어 QEMU의 rv32i CPU에서 실제 명령으로 실행한 결과입니다. 물리 RISC-V 보드에서 측정한 결과는 아닙니다.

## ISA·ABI·플랫폼의 구분

ISA는 명령의 의미이며 ABI는 함수 인자·반환값·보존 레지스터·스택 사용의 약속입니다. 이 ELF는 `-march=rv32i -mabi=ilp32`로 만들었으며 readelf에서 ELF32, little endian, `Tag_RISCV_arch="rv32i2p1"`, 스택 정렬16바이트를 확인했습니다. M·C·벡터 확장은 사용하지 않습니다. 의사 명령 ret·la·call은 어셈블러가 기본 명령으로 풀며 실제 역어셈블 결과도 기록했습니다. 명령의 의미는 [RV32I Version2.1의 정수 연산·load/store 절](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html)을 근거로 합니다.

| 함수 경계의 역할 | 이 예제의 사용 |
| --- | --- |
| a0~a3 | update_field의 원래값·새값·시작 비트·폭입니다. |
| a0·a1 | byte_sum의 주소·길이입니다. |
| a0 | 두 함수의32비트 반환값입니다. |
| t0~t2 | 함수 안에서 자유롭게 바꾸는 임시 레지스터입니다. |
| s0~s11 | 호출자가 맡긴 값을 보존해야 하며 두 본체는 사용하지 않습니다. |
| ra | 복귀 주소이며 다른 함수를 부르지 않는 두 leaf 함수는 그대로 유지합니다. |
| sp | 호출 경계에서16바이트 정렬을 유지합니다. |

[RISC-V psABI의1.1절과2.1절](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/)이 이 정수 호출 규약과 스택 약속의 근거입니다. 두 계산 함수는 다른 함수를 호출하지 않아 별도의 저장 프레임이 필요 없습니다. 반대로 abi_probe는 다른 함수를 호출하므로 ra와 원래 s레지스터를64바이트 프레임에 보존합니다. 검사 뒤 복구해야 C 호출자의 상태도 유지됩니다.

시작 코드는 sp와 gp를 설정하고4바이트 정렬 BSS를 지운 뒤 main으로 들어갑니다. 코드·초기 자료는 QEMU ELF 로더가 같은 RAM에 적재하며 다른 ROM의 초기 자료를 복사하는 CRT는 필요하지 않습니다. 코드·자료의 ELF 적재 권한은 분리합니다. 운영체제·SBI·인터럽트 서비스·예외 처리기를 갖춘 범용 런타임은 아닙니다.

## 비트필드 갱신의 계약

함수는 아래 C 서명으로 호출합니다. 여기서 갱신하는 것은 레지스터 안의 값이며 주소를 받아 메모리를 직접 바꾸는 함수가 아닙니다.

```c
uint32_t update_field(uint32_t original, uint32_t value, uint32_t shift, uint32_t width); // 원래값의 지정 비트만 교체한 새값 반환
```

유효 입력은0≤shift≤31,0≤width≤32−shift입니다. 필드 밖의 비트는 보존하고 value의 낮은 width개 비트만 넣습니다. 폭0은 원래값을 그대로 반환하며 폭32는 shift=0일 때 전체값을 교체합니다. 이 범위를 벗어나는 인자는 검사하지 않습니다.

width<32이면 낮은 마스크는 `(1<<width)-1`입니다. 이를 shift만큼 옮겨 지울 비트를 찾고, 원래값의 해당 위치를0으로 만든 다음 잘라낸 새 비트를 OR합니다. [RV32I의 레지스터 시프트는 이동량의 낮은5비트만 사용](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html#_integer_register_register_instructions)하므로32만큼 이동한다고32개의0이 생기는 것은 아닙니다. 폭32를 별도로 처리하는 이유입니다.

| 단계 | 값 | 목적 |
| --- | --- | --- |
| 인자 | original=F0F00F0F, value=000001AB, shift=8, width=8 |8번부터8비트만 교체합니다. |
| 낮은 마스크 |000000FF | 새값의 AB만 남깁니다. |
| 필드 마스크 |0000FF00 | 원래값에서 지울 위치입니다. |
| 필드 제거 | F0F0000F | 필드 밖 비트를 보존합니다. |
| 새 필드 |0000AB00 | 선택한 값을 올바른 위치로 옮깁니다. |
| 반환 a0 | F0F0AB0F | 지운 자리만 새값으로 채웁니다. |

C 기준은 이 마스크식을 반복하지 않습니다. 결과의32개 비트를 하나씩 확인하여 필드 안쪽만 새 비트로 덮어씁니다. 모든 유효 시작·폭 조합560개에 원래값6종과 새값6종을 교차하여20,160개를 비교하고 직접 예제 한 개를 더 검사합니다. 빈 필드·전체32비트·최상위 비트·새값의 넘치는 비트도 포함합니다.

## 바이트 검사합의 계약과 반복 불변식

```c
uint32_t byte_sum(const uint8_t *bytes, uint32_t length); // 읽을 수 있는 일반 RAM 바이트의32비트 합 반환
```

길이만큼 읽을 수 있고 주소가 순환하지 않는 일반 RAM 범위가 전제입니다. 길이0이면 아무 메모리도 읽지 않으므로 이 경우의 NULL 주소도 허용합니다. 함수는 RAM을 쓰지 않습니다. 반환값은32비트 모듈러 합이며 로컬 검사는 길이0~64에서 수행합니다. 큰 버퍼에서의32비트 넘침 경로를 따로 실행한 시험은 아닙니다.

반복 시작 시 a0는 이미 읽은 바이트의 합, t0는 다음 바이트 주소, a1은 남은 길이입니다. lbu는 한 바이트를0~255로 넓힙니다. 한 번 더하고 주소를1 늘리고 남은 길이를1 줄이면 같은 약속이 유지됩니다. 남은 길이가0이면 전체합을 반환합니다. byte_sum의 시간은 O(length), 추가 저장은 O(1)입니다. update_field는 입력 폭과 관계없이 상수 개 명령으로 처리합니다.

| 읽은 바이트 | unsigned 값 | 누적합 |
| --- | --- | --- |
|00 |0 |0 |
|7F |127 |127 |
|80 |128 |255 |
| FF |255 |510=000001FE |

C 기준은 같은 RAM을 역방향으로 합산합니다. 덧셈 순서가 달라도 부호 없는 모듈러 합은 같습니다. 오프셋0~3과 길이0~64를 교차한260개, 위 직접 예제, NULL·길이0 한 개로 총262개를 확인합니다.128·255가 들어 있으므로 잘못된 부호 확장을 구분할 수 있습니다.

## 메모리 정렬과 MMIO의 경계

바이트 load는 주소가 어디든1바이트 자연 정렬을 만족합니다. 그래서 byte_sum은 bytes+1·+2·+3도 lbu로 읽습니다. 이를 정렬되지 않은 주소의 lw도 항상 안전하다는 뜻으로 해석하지 않습니다. [RV32I load/store 절](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html)은 접근 크기에 맞춘 정렬과 비정렬 접근의 실행 환경 의존성을 구분합니다. 시작 코드·ABI 검사·C 스택의 워드 접근은4바이트 정렬이며 sp는 그보다 강한16바이트 정렬을 지킵니다.

| 주소·영역 | 이 예제의 역할 |
| --- | --- |
|80000000부터128KiB | ELF 코드·자료·스택에 예약한 RAM입니다. QEMU에 제공한 전체 RAM32MiB보다 작습니다. |
|10000000의 UART | 검사 로그를 출력하는 MMIO입니다. 두 계산 함수의 입력 버퍼가 아닙니다. |
|00100000의 finisher | QEMU 실행을 정상 또는 실패 코드로 끝내는 가상 장치입니다. |

주소는 RISC-V ISA 공통 규칙이 아니라 [QEMU virt 가상 플랫폼](https://www.qemu.org/docs/master/system/riscv/virt.html)의 계약입니다. 메모리 배치는 [QEMU v10.1.0의 공개 virt_memmap](https://github.com/qemu/qemu/blob/v10.1.0/hw/riscv/virt.c#L77-L99)과 대조했으며 실제 실행 도구는 아래에 기록한11.1.0 빌드입니다. 참조한 소스 판본과 실행한 도구 판본을 같다고 쓰지 않습니다. UART 출력과 [test finisher 종료](https://github.com/qemu/qemu/blob/v10.1.0/hw/misc/sifive_test.c#L32-L49)는 실제 로컬 실행에서 확인합니다. 다른 보드에 이 주소를 그대로 쓰면 안 됩니다.

C 드라이버의 volatile 포인터는 장치 접근이 컴파일러에 의해 사라지지 않도록 표현합니다. volatile만으로 원자적 read-modify-write나 모든 장치 순서를 보장하지는 않습니다. 종료 전 FENCE는 접근 순서를 지정하며 주변 장치의 개별 동작·완료 계약을 대체하지 않습니다. UART 로그·finisher 외의 두 계산 함수는 MMIO에 접근하지 않습니다.

update_field를 이용해 장치 레지스터를 바꾸려면 읽기 부작용·write-one-to-clear·예약 비트·인터럽트와의 경쟁을 별도로 판단해야 합니다. 이 산술 함수가 안전한 MMIO 갱신 절차를 자동으로 제공하지는 않습니다. byte_sum에 읽을 때 상태가 바뀌는 장치 주소를 전달하는 사용법도 전제하지 않습니다.

## ABI 검사와 오류 대조

abi_probe는 s0~s11에 서로 다른 표식을 넣고 두 계산 함수를 부른 뒤 모든 표식과 sp의16바이트 정렬을 확인합니다. 이어 원래 호출자의 s레지스터·ra·sp를 복구합니다. 이 한 시나리오는 반환값 검사와 별개인 ABI 관측이며 모든 ABI 동작을 증명하는 것은 아닙니다.

음성 대조에서는 빌드 복사본의 lbu 한 명령만 lb로 바꿉니다. 원본 functions.S는 바꾸지 않습니다.80·FF가 각각−128·−1로 읽혀0+127−128−1=−2가 되고, 실제 UART에서 expected=000001FE,actual=FFFFFFFE를 출력한 뒤 QEMU가 종료1을 반환합니다. 이 오류 검출은 잘못된 어셈블리가 실제 실행 경로에 들어갔는지도 확인하는 대조입니다. 결함 회로·함수가 정상 기능 시험을 통과한 결과로 집계하지 않습니다.

## 실제 실행 결과

2026-10-26에 xPack GNU RISC-V GCC15.2.0과 QEMU11.1.0을 실행했습니다. 정상 ELF의 실제 로그는 다음과 같습니다. 집계는 나눗셈 라이브러리를 추가하지 않도록8자리16진수로 출력하며 JSON에는 정수로 변환한 값도 저장합니다.

```text
TRACE field result=f0f0ab0f
TRACE byte sum=000001fe
PASS RV32I field_checks=00004ec1 checksum_checks=00000106 abi_checks=00000001 total_checks=00004fc8
```

| 설정 | 컴파일 종료 | QEMU 종료 | 관측 결과 |
| --- | --- | --- | --- |
| 정상 |0 |0 | 비트필드20,161·검사합262·ABI1, 총20,424개 비교가 통과했습니다. |
| lbu→lb 결함 복사본 |0 |1 | unsigned byte demo에서510과−2의 차이를 검출했습니다. |

컴파일의 stderr는 비어 있습니다. QEMU는 satp 모드를 지정하지 않아 bare로 기본 설정한다는 경고를 출력했습니다. 이 예제는 페이지 테이블을 사용하지 않는 물리 주소의 bare-metal 실행이며 경고 원문도 기록했습니다. 경고가 없었다고 바꾸어 적지 않습니다. QEMU의 명령 블록 로그·ELF 역어셈블·실행 파일 해시를 남기지만 이 로그를 사이클 수나 모든 명령의 retire 기록으로 부르지는 않습니다.

## 파일과 재실행

| 파일 | 역할 |
| --- | --- |
| [functions.S](functions.S) | 직접 작성한 RV32I 계산 함수 두 개입니다. |
| [driver.c](driver.c) | 독립 C 기준·검사 입력·UART·종료 처리입니다. |
| [abi_probe.S](abi_probe.S) | 보존 레지스터·스택 정렬 관측입니다. |
| [startup.S](startup.S) | sp·gp·BSS를 설정하고 C에 진입합니다. |
| [linker.ld](linker.ld) | 가상 플랫폼의 RAM 배치와 권한을 정합니다. |
| [run.py](run.py) | 새 빌드 폴더에서 컴파일·ELF 확인·CPU 실행을 기록합니다. |

다음 PowerShell 명령은 저장소 루트에서 시작합니다. --out은 아직 없는 폴더여야 하며 기존 결과를 덮어쓰지 않습니다. 다른 환경에서는 --gcc와 --qemu를 해당 도구 경로로 바꿉니다. Python3 표준 라이브러리만 사용하며 RISC-V 도구와 QEMU는 별도 실행 파일입니다.

```powershell
$source = Resolve-Path '하드웨어코딩_hardware-coding/언어확장_language-expansion/01-RISC-V비트처리_riscv-assembly'
$gcc = 'C:/Users/test2/Documents/ChatGPT/stm32/post-silicon-virtual-lab/tools/riscv-gcc/xpack-riscv-none-elf-gcc-15.2.0-1/bin/riscv-none-elf-gcc.exe'
$qemu = 'C:/Users/test2/Documents/ChatGPT/stm32/post-silicon-virtual-lab/tools/qemu/qemu-system-riscv32.exe'
$build = Join-Path ([IO.Path]::GetTempPath()) ('rv32i-example-' + [Guid]::NewGuid().ToString('N'))
python (Join-Path $source 'run.py') --gcc $gcc --qemu $qemu --out $build
$negative = Join-Path ([IO.Path]::GetTempPath()) ('rv32i-negative-' + [Guid]::NewGuid().ToString('N'))
python (Join-Path $source 'run.py') --gcc $gcc --qemu $qemu --out $negative --negative-byte-sign
```

실제 컴파일 인자는 `-march=rv32i -mabi=ilp32 -mcmodel=medany -mno-relax -msmall-data-limit=0 -nostdlib`를 포함합니다. 실행은 `qemu-system-riscv32 -machine virt -cpu rv32i -m 32M -bios none -kernel program.elf`를 사용합니다. 전체 인자와 반환 코드·stdout·stderr는 example.json과 새 빌드의 report.json에 저장합니다. 호스트용 C 실행으로 어셈블리 검사를 대체하는 분기는 없습니다.

## 사용처와 한계

비트필드 갱신은 이미 읽은 상태 워드의 일부 값을 조합하거나 패킷의 수치 필드를 구성할 때 원리를 적용할 수 있습니다. 바이트 합은 작은 자료의 무결성 확인·실험용 체크 값에 쓸 수 있지만 단순 합은 바이트 순서 교환과 여러 상쇄 오류를 구별하지 못합니다. CRC나 암호학적 해시와 같은 오류·공격 검출 강도를 제공하지 않습니다.

이 코드는 CPU 명령으로 실행되는 펌웨어이며 HDL처럼 회로 구조를 합성한 결과가 아닙니다. QEMU는 실제 보드의 파이프라인·캐시·버스 지연·전력이나 외부 UART 속도를 측정하지 않습니다. 처리 시간·소비전력·실시간 마감의 보장을 얻으려면 대상 하드웨어에서 별도 측정과 타이밍 분석을 해야 합니다. 기존 RV32I RTL CPU·Python 명령 모델은 수정하거나 복제하지 않았습니다.

## 줄별 문법과 목적

어셈블리의 # 주석, C·링커·러너의 줄 주석에 해당 문법과 사용하는 값을 함께 설명합니다. 계산 함수 외의 시작·검사·실행 코드도 재현에 필요한 전체 소스입니다.

### functions.S

```asm
.section .text # 실행할 함수 코드를 text 영역에 배치
.balign 4 # RV32I 명령 시작을4바이트에 맞추기
.globl update_field # C에서 호출할 함수 이름 공개
.type update_field, @function # ELF 심볼을 함수로 표시
update_field: # a0=원래값,a1=새비트,a2=시작,a3=폭
    beq a3, zero, .Lfield_return # 폭0이면 원래값을 그대로 반환
    addi t0, zero, 32 # 전체 레지스터 폭 비교 상수
    beq a3, t0, .Lfield_full # 폭32의 특별 경로로 shift32 문제 피하기
    addi t0, zero, 1 # 낮은 비트 마스크를 만들 시작값
    sll t0, t0, a3 # 1을 필드 폭만큼 이동
    addi t0, t0, -1 # 낮은 width개 비트가1인 마스크
    sll t1, t0, a2 # 실제 필드 위치로 마스크 이동
    xori t2, t1, -1 # 필드 밖은1이고 안쪽은0인 보존 마스크
    and a0, a0, t2 # 원래값의 필드 부분만 지우기
    and a1, a1, t0 # 새비트에서 필드 폭을 넘는 부분 제거
    sll a1, a1, a2 # 새 필드값을 시작 위치로 이동
    or a0, a0, a1 # 보존한 비트와 새 필드를 결합
.Lfield_return: # a0가 반환값인 공통 경로
    ret # ra로 돌아가는 jalr 의사 명령
.Lfield_full: # 유효 계약상 폭32이면 시작 위치는0
    addi a0, a1, 0 # 전체32비트를 새값으로 교체
    ret # 호출자에게 새값 반환
.size update_field, .-update_field # 함수의 코드 길이 기록

.balign 4 # 두 번째 함수도4바이트 경계에 배치
.globl byte_sum # C에서 호출할 검사합 함수 공개
.type byte_sum, @function # ELF 함수 심볼 표시
byte_sum: # a0=일반RAM 바이트 주소,a1=길이
    addi t0, a0, 0 # 읽기 포인터를 임시 레지스터에 보관
    addi a0, zero, 0 # 반환 레지스터를 합0으로 초기화
    beq a1, zero, .Lsum_return # 길이0이면 주소를 읽지 않고 반환
.Lsum_loop: # 아직 읽지 않은 바이트가 있는 반복
    lbu t1, 0(t0) # 현재 바이트를 부호 없이0~255로 읽기
    add a0, a0, t1 # 32비트 모듈러 합 누적
    addi t0, t0, 1 # 다음 바이트 주소로 전진
    addi a1, a1, -1 # 남은 바이트 수 하나 감소
    bne a1, zero, .Lsum_loop # 남은 바이트가 있으면 계속 읽기
.Lsum_return: # a0에 최종 검사합 보관
    ret # 합을 유지한 채 호출자 복귀
.size byte_sum, .-byte_sum # 검사합 함수 길이 기록
.section .note.GNU-stack,"",@progbits # 실행 가능한 스택을 요청하지 않는 표시
```

### abi_probe.S

```asm
.section .text # ABI 검사 전용 코드 영역
.balign 4 # 함수 시작의4바이트 정렬
.globl abi_probe # C에서 부를 보존 레지스터 검사
.type abi_probe, @function # 함수 심볼 표시
abi_probe: # 호출 뒤 s레지스터 보존과 스택 정렬 확인
    addi sp, sp, -64 #16바이트 정렬을 유지하며 저장 프레임 확보
    sw ra, 0(sp) # 두 함수 호출 전 원래 복귀 주소 보관
    sw s0, 4(sp) # 호출자의 s0 원래값을 스택에 보존
    sw s1, 8(sp) # 호출자의 s1 원래값을 스택에 보존
    sw s2, 12(sp) # 호출자의 s2 원래값을 스택에 보존
    sw s3, 16(sp) # 호출자의 s3 원래값을 스택에 보존
    sw s4, 20(sp) # 호출자의 s4 원래값을 스택에 보존
    sw s5, 24(sp) # 호출자의 s5 원래값을 스택에 보존
    sw s6, 28(sp) # 호출자의 s6 원래값을 스택에 보존
    sw s7, 32(sp) # 호출자의 s7 원래값을 스택에 보존
    sw s8, 36(sp) # 호출자의 s8 원래값을 스택에 보존
    sw s9, 40(sp) # 호출자의 s9 원래값을 스택에 보존
    sw s10, 44(sp) # 호출자의 s10 원래값을 스택에 보존
    sw s11, 48(sp) # 호출자의 s11 원래값을 스택에 보존
    addi s0, zero, 1 # s0에 보존 여부를 확인할 고유값 설정
    addi s1, zero, 2 # s1에 보존 여부를 확인할 고유값 설정
    addi s2, zero, 3 # s2에 보존 여부를 확인할 고유값 설정
    addi s3, zero, 4 # s3에 보존 여부를 확인할 고유값 설정
    addi s4, zero, 5 # s4에 보존 여부를 확인할 고유값 설정
    addi s5, zero, 6 # s5에 보존 여부를 확인할 고유값 설정
    addi s6, zero, 7 # s6에 보존 여부를 확인할 고유값 설정
    addi s7, zero, 8 # s7에 보존 여부를 확인할 고유값 설정
    addi s8, zero, 9 # s8에 보존 여부를 확인할 고유값 설정
    addi s9, zero, 10 # s9에 보존 여부를 확인할 고유값 설정
    addi s10, zero, 11 # s10에 보존 여부를 확인할 고유값 설정
    addi s11, zero, 12 # s11에 보존 여부를 확인할 고유값 설정
    addi a0, zero, 123 # 비트필드 검사의 원래값
    addi a1, zero, 45 # 새 필드 값
    addi a2, zero, 4 # 필드 시작 위치
    addi a3, zero, 5 # 필드 폭
    call update_field # 첫 어셈블리 함수 호출
    addi a0, zero, 0 # 길이0 검사에서는 주소를 읽지 않음
    addi a1, zero, 0 # 빈 검사합 요청
    call byte_sum # 두 번째 어셈블리 함수 호출
    andi t0, sp, 15 # 현재 스택의16바이트 정렬 확인
    bne t0, zero, .Labi_fail # 정렬 위반이면 실패
    addi t0, zero, 1 # s0의 보존 기대값
    bne s0, t0, .Labi_fail # 호출 전 s0 값이 바뀌면 실패
    addi t0, zero, 2 # s1의 보존 기대값
    bne s1, t0, .Labi_fail # 호출 전 s1 값이 바뀌면 실패
    addi t0, zero, 3 # s2의 보존 기대값
    bne s2, t0, .Labi_fail # 호출 전 s2 값이 바뀌면 실패
    addi t0, zero, 4 # s3의 보존 기대값
    bne s3, t0, .Labi_fail # 호출 전 s3 값이 바뀌면 실패
    addi t0, zero, 5 # s4의 보존 기대값
    bne s4, t0, .Labi_fail # 호출 전 s4 값이 바뀌면 실패
    addi t0, zero, 6 # s5의 보존 기대값
    bne s5, t0, .Labi_fail # 호출 전 s5 값이 바뀌면 실패
    addi t0, zero, 7 # s6의 보존 기대값
    bne s6, t0, .Labi_fail # 호출 전 s6 값이 바뀌면 실패
    addi t0, zero, 8 # s7의 보존 기대값
    bne s7, t0, .Labi_fail # 호출 전 s7 값이 바뀌면 실패
    addi t0, zero, 9 # s8의 보존 기대값
    bne s8, t0, .Labi_fail # 호출 전 s8 값이 바뀌면 실패
    addi t0, zero, 10 # s9의 보존 기대값
    bne s9, t0, .Labi_fail # 호출 전 s9 값이 바뀌면 실패
    addi t0, zero, 11 # s10의 보존 기대값
    bne s10, t0, .Labi_fail # 호출 전 s10 값이 바뀌면 실패
    addi t0, zero, 12 # s11의 보존 기대값
    bne s11, t0, .Labi_fail # 호출 전 s11 값이 바뀌면 실패
    addi a0, zero, 0 # 모든 보존 검사가 맞으면 성공0
    j .Labi_restore # 호출자 상태를 복구하는 공통 경로
.Labi_fail: # 보존 또는 정렬 불일치
    addi a0, zero, 1 # 검사 실패1 반환
.Labi_restore: # 검사 결과와 무관하게 원래 저장 상태 복원
    lw s0, 4(sp) # 호출자의 s0 원래값 복원
    lw s1, 8(sp) # 호출자의 s1 원래값 복원
    lw s2, 12(sp) # 호출자의 s2 원래값 복원
    lw s3, 16(sp) # 호출자의 s3 원래값 복원
    lw s4, 20(sp) # 호출자의 s4 원래값 복원
    lw s5, 24(sp) # 호출자의 s5 원래값 복원
    lw s6, 28(sp) # 호출자의 s6 원래값 복원
    lw s7, 32(sp) # 호출자의 s7 원래값 복원
    lw s8, 36(sp) # 호출자의 s8 원래값 복원
    lw s9, 40(sp) # 호출자의 s9 원래값 복원
    lw s10, 44(sp) # 호출자의 s10 원래값 복원
    lw s11, 48(sp) # 호출자의 s11 원래값 복원
    lw ra, 0(sp) # 원래 복귀 주소 복원
    addi sp, sp, 64 # 저장 프레임 반환
    ret # C 검사 드라이버로 복귀
.size abi_probe, .-abi_probe # ABI 검사 코드 길이 기록
.section .note.GNU-stack,"",@progbits # 실행 스택을 요구하지 않는 표시
```

### startup.S

```asm
.section .text.start,"ax",@progbits # ELF 시작 코드를 먼저 배치
.balign 4 # 첫 RV32I 명령의4바이트 정렬
.globl _start # 링커가 찾을 진입점 공개
.type _start, @function # 진입점을 함수 심볼로 표시
_start: # QEMU의 부트 ROM에서 넘어올 시작 위치
    la sp, __stack_top # 16바이트로 정렬한 스택 최상단 설정
    .option push # 현재 어셈블러 옵션 보관
    .option norelax # gp 자체 초기화가 완화로 생략되지 않게 설정
    la gp, __global_pointer$ # ABI의 전역 포인터 기준값 설정
    .option pop # 이전 어셈블러 옵션 복원
    la t0, __bss_start # 0으로 지울 영역의 시작
    la t1, __bss_end # 0으로 지울 영역의 끝
.Lzero_bss: # 4바이트씩 BSS 초기화
    bgeu t0, t1, .Lcall_main # 빈 영역이나 끝에 도달하면 초기화 종료
    sw zero, 0(t0) # 정렬된 RAM 한 워드를0으로 저장
    addi t0, t0, 4 # 다음 워드 주소로 이동
    j .Lzero_bss # 남은 BSS 초기화 반복
.Lcall_main: # C 실행 환경의 최소 저장 영역 초기화 완료
    call main # C 검사 드라이버 진입
.Lhalt: # main이 예기치 않게 반환한 경우
    j .Lhalt # 실행을 다른 데이터 영역으로 흘려보내지 않기
.size _start, .-_start # 진입 코드의 길이 기록
.section .note.GNU-stack,"",@progbits # 실행 스택을 요구하지 않는 표시
```

### driver.c

```c
#include <stdint.h> // 정확한32비트·8비트 정수 자료형
extern uint32_t update_field(uint32_t original, uint32_t value, uint32_t shift, uint32_t width); // a0~a3 인자로 호출할 어셈블리 함수
extern uint32_t byte_sum(const uint8_t *bytes, uint32_t length); // RAM 바이트 검사합 함수
extern uint32_t abi_probe(void); // s레지스터와 스택 정렬의 별도 검사
_Static_assert(sizeof(uint32_t) == 4, "u32 width"); // 32비트 기준의 C 검사 전제
_Static_assert(sizeof(void *) == 4, "RV32 pointer"); // 실제32비트 타깃으로 빌드되는지 확인
static uint32_t field_checks, checksum_checks, abi_checks; // 실제 함수 결과 비교 수
static volatile uint8_t *const uart = (volatile uint8_t *)0x10000000u; // QEMU virt의 로그 출력 MMIO
static volatile uint32_t *const finisher = (volatile uint32_t *)0x00100000u; // QEMU 전용 종료 장치의 정렬된 워드 주소
static void put_char(char value) { // UART를 통한 한 문자 출력
    while ((uart[5] & 0x20u) == 0) { } // 송신 레지스터가 빌 때까지 MMIO 상태 확인
    uart[0] = (uint8_t)value; // 한 문자를 장치 레지스터에 기록
} // 문자 출력 끝
static void put_text(const char *text) { // 0으로 끝나는 로그 문자열 출력
    while (*text) put_char(*text++); // 문자열 끝까지 한 글자씩 전송
} // 문자열 출력 끝
static void put_hex(uint32_t value) { // 라이브러리 나눗셈 없이8자리16진수 출력
    const char *digits = "0123456789abcdef"; // 각4비트의 출력 문자 표
    for (int shift = 28; shift >= 0; shift -= 4) put_char(digits[(value >> shift) & 15u]); // 높은4비트부터 차례로 출력
} // 32비트 수 출력 끝
static _Noreturn void finish(uint32_t status) { // QEMU 종료와 실패 코드 전달
    while ((uart[5] & 0x40u) == 0) { } // 남은 로그의 송신 완료 확인
    __asm__ volatile ("fence iorw, iorw" ::: "memory"); // 컴파일러와 ISA 수준에서 앞선 I/O 순서 구분
    *finisher = status ? (status << 16) | 0x3333u : 0x5555u; // 이 가상 장치의 실패 또는 정상 종료 값
    for (;;) { __asm__ volatile ("j ."); } // 장치가 없을 때 무관한 주소로 실행하지 않기
} // 플랫폼 전용 종료 함수 끝
static void require_equal(uint32_t actual, uint32_t expected, const char *name) { // 어셈블리 결과와 독립 기준 비교
    if (actual != expected) { // 첫 잘못된 결과 분리
        put_text("FAIL RV32I "); put_text(name); put_text(" expected="); put_hex(expected); // 기준값 기록
        put_text(" actual="); put_hex(actual); put_text("\n"); // 실제 결과 기록
        finish(1); // 실패 코드로 실제 CPU 실행 종료
    } // 결과 불일치 처리 끝
} // 공통 비교 함수 끝
static uint32_t reference_field(uint32_t original, uint32_t value, uint32_t shift, uint32_t width) { // 마스크식 대신 비트별 덮어쓰기 기준
    uint32_t result = original; // 필드 밖의 비트는 원래값에서 시작
    for (uint32_t bit = 0; bit < 32; ++bit) { // 모든 결과 비트 독립 확인
        if (bit >= shift && bit - shift < width) { // 해당 위치가 유효 필드 안인지 검사
            uint32_t mask = 1u << bit; // 0~31 사이의 한 비트 마스크
            if ((value >> (bit - shift)) & 1u) result |= mask; // 새 비트가1이면 해당 위치 설정
            else result &= ~mask; // 새 비트가0이면 해당 위치 해제
        } // 필드 안의 선택 갱신 끝
    } // 32개 비트 기준 완성
    return result; // 독립적인 새 레지스터값 반환
} // 비트필드 기준 함수 끝
static uint32_t reference_sum(const uint8_t *bytes, uint32_t length) { // 역방향으로 합산하는 독립 바이트 기준
    uint32_t result = 0; // 빈 배열의 합0
    while (length > 0) result += bytes[--length]; // 어셈블리와 반대 순서로 같은 RAM 바이트 합산
    return result; // 32비트 모듈러 합 반환
} // 검사합 기준 함수 끝
int main(void) { // QEMU의 RISC-V CPU에서 실행할 C 검사 드라이버
    static const uint32_t patterns[6] = {0u, 0xffffffffu, 0x80000000u, 0x55555555u, 0xaaaaaaaau, 0x12345678u}; // 0·전체1·최상위 비트·교대·혼합 패턴
    static const uint8_t demo[4] = {0x00u, 0x7fu, 0x80u, 0xffu}; // 부호 확장 오류도 구분할 네 바이트
    uint8_t bytes[68]; // 오프셋0~3에서 최대64바이트를 읽을 RAM 버퍼
    uint32_t field_demo = update_field(0xf0f00f0fu, 0x1abu, 8, 8); // 넘치는 새 비트도 잘라 넣는 실제 어셈블리 호출
    require_equal(field_demo, 0xf0f0ab0fu, "field demo"); ++field_checks; // 직접 계산한 결과와 대조
    put_text("TRACE field result="); put_hex(field_demo); put_text("\n"); // 실제 호출 결과를 로그로 확인
    for (uint32_t shift = 0; shift < 32; ++shift) { // 필드 시작의 모든 유효 위치
        for (uint32_t width = 0; width <= 32 - shift; ++width) { // 빈 필드와 전체32비트를 포함한 폭
            for (uint32_t old = 0; old < 6; ++old) { // 원래값의 여섯 패턴
                for (uint32_t value = 0; value < 6; ++value) { // 새값의 여섯 패턴
                    uint32_t actual = update_field(patterns[old], patterns[value], shift, width); // 외부 어셈블리 함수 실행
                    require_equal(actual, reference_field(patterns[old], patterns[value], shift, width), "field cross product"); // 비트별 C 기준과 비교
                    ++field_checks; // 실제 비트필드 비교 수 누적
                } // 새값 패턴 끝
            } // 원래값 패턴 끝
        } // 시작 위치에 맞는 폭 끝
    } // 전체560개 시작·폭 조합 끝
    uint32_t sum_demo = byte_sum(demo, 4); // 0·127·128·255의 실제 어셈블리 검사합
    require_equal(sum_demo, 510u, "unsigned byte demo"); ++checksum_checks; // lbu의 부호 없는 결과 확인
    put_text("TRACE byte sum="); put_hex(sum_demo); put_text("\n"); // 실제 합510을16진수로 출력
    require_equal(byte_sum((const uint8_t *)0, 0), 0, "empty null pointer"); ++checksum_checks; // 길이0이면 주소를 읽지 않는 경계
    for (uint32_t index = 0; index < 68; ++index) bytes[index] = (uint8_t)(index * 37u + 11u); // 재현 가능한 RAM 자료 초기화
    for (uint32_t offset = 0; offset < 4; ++offset) { // 워드 경계와 어긋나는 바이트 주소도 사용
        for (uint32_t length = 0; length <= 64; ++length) { // 빈 길이부터 버퍼 안의 최대 길이
            require_equal(byte_sum(bytes + offset, length), reference_sum(bytes + offset, length), "byte ranges"); // 순방향 ASM과 역방향 C의 합 비교
            ++checksum_checks; // 실제 검사합 비교 수 누적
        } // 길이 경계 검사 끝
    } // 네 시작 오프셋 검사 끝
    require_equal(abi_probe(), 0, "callee saved registers and aligned stack"); ++abi_checks; // 12개 s레지스터와 호출 뒤 스택 정렬 확인
    put_text("PASS RV32I field_checks="); put_hex(field_checks); // 실제 비트필드 검사 수
    put_text(" checksum_checks="); put_hex(checksum_checks); // 실제 바이트 합 검사 수
    put_text(" abi_checks="); put_hex(abi_checks); // 별도 ABI 검사 시나리오 수
    put_text(" total_checks="); put_hex(field_checks + checksum_checks + abi_checks); put_text("\n"); // 전체 결과 집계
    finish(0); // 성공 로그 뒤 QEMU를 정상 종료
} // 독립 검사 드라이버 끝
```

### linker.ld

```ld
ENTRY(_start) /* ELF 진입점은 직접 작성한 시작 코드 */
MEMORY { /* 예제에서 사용할 메모리 영역 */
    RAM (rwx) : ORIGIN = 0x80000000, LENGTH = 128K /* QEMU virt DRAM의 첫128KiB만 사용 */
} /* 영역 정의 끝 */
PHDRS { /* ELF 적재 구간의 권한 분리 */
    text PT_LOAD FLAGS(5); /* 읽기·실행 코드 구간 */
    data PT_LOAD FLAGS(6); /* 읽기·쓰기 자료 구간 */
} /* 적재 권한 정의 끝 */
SECTIONS { /* 코드·자료·스택 심볼의 배치 */
    .text : { *(.text.start) *(.text .text.*) *(.rodata .rodata.*) } > RAM :text /* 시작 코드와 함수·읽기 전용 자료 배치 */
    . = ALIGN(16); /* 다음 자료 경계 정렬 */
    .data : { *(.data .data.*) *(.sdata .sdata.*) } > RAM :data /* 초기값 있는 자료를 같은 RAM에 직접 적재 */
    __global_pointer$ = ADDR(.data) + 0x800; /* gp 초기화에 쓸 전역 포인터 기준 */
    .bss (NOLOAD) : { /* 파일에0을 저장하지 않는 초기화 영역 */
        . = ALIGN(4); __bss_start = .; /* 워드 저장이 가능한 시작 주소 */
        *(.bss .bss.*) *(.sbss .sbss.*) *(COMMON) /* 초기값 없는 자료 수집 */
        . = ALIGN(4); __bss_end = .; /* 4바이트 단위 초기화의 끝 */
    } > RAM :data /* BSS를 쓰기 가능한 RAM에 배치 */
    __stack_top = ORIGIN(RAM) + LENGTH(RAM); /* 16바이트 정렬 RAM 상단에서 스택 시작 */
    ASSERT(__bss_end + 4096 < __stack_top, "RAM overlaps stack") /* 최소4KiB의 스택 여유 확인 */
} /* 메모리 배치 끝 */
```

### run.py

```python
import argparse  # 도구 경로와 새 결과 폴더의 명령행 해석
import hashlib  # 실행 원본과 작업 복사본의 SHA-256 기록
import json  # 실제 명령·출력·결과를 기계 판독 형식으로 저장
import os  # 자식 프로세스 환경 설정
from pathlib import Path  # 소스와 빌드 경로 처리
import re  # ELF 속성과 실제 출력 집계 추출
import shutil  # 원본 소스를 새 빌드 폴더로 복사
import subprocess  # RISC-V 컴파일러와 CPU 에뮬레이터 실행

def main():  # 컴파일·실행·증거 저장의 시작점
    parser = argparse.ArgumentParser()  # 예제 전용 실행 옵션
    parser.add_argument('--gcc', required=True, type=Path)  # RV32I를 지원하는 GNU 컴파일러
    parser.add_argument('--qemu', required=True, type=Path)  # qemu-system-riscv32 실행 파일
    parser.add_argument('--out', required=True, type=Path)  # 기존 결과를 덮지 않을 새 빌드 경로
    parser.add_argument('--negative-byte-sign', action='store_true')  # 복사본에서만 lbu를 lb로 바꾸는 음성 대조
    args = parser.parse_args()  # 실제 전달한 옵션 읽기
    source = Path(__file__).resolve().parent  # 저장소의 이 예제 위치
    work = args.out.resolve()  # 결과를 저장할 절대 경로
    work.mkdir(parents=True, exist_ok=False)  # 이미 있는 결과 폴더는 거절
    gcc, qemu = args.gcc.resolve(), args.qemu.resolve()  # 두 실제 도구의 절대 경로
    names = ['functions.S', 'abi_probe.S', 'startup.S', 'driver.c', 'linker.ld']  # ELF를 만드는 실제 입력 파일
    for name in names:  # 원본 대신 작업 폴더에서 컴파일
        shutil.copyfile(source / name, work / name)  # 소스 바이트를 그대로 복사
    source_hashes = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in names + ['run.py']}  # 검사한 원본 식별
    if args.negative_byte_sign:  # 정상 원본은 건드리지 않는 결함 주입
        text = (work / 'functions.S').read_text(encoding='utf-8')  # 작업 복사본의 함수 코드
        if text.count('lbu t1, 0(t0)') != 1:  # 정확한 한 명령에만 결함 적용
            raise ValueError('byte load mutation target count')  # 모호한 위치를 임의로 변경하지 않기
        (work / 'functions.S').write_text(text.replace('lbu t1, 0(t0)', 'lb t1, 0(t0)'), encoding='utf-8', newline='\n')  # 부호 확장 결함을 작업 복사본에만 저장
    report = {'commands': [], 'source_sha256': source_hashes, 'negative_byte_sign': args.negative_byte_sign}  # 실행 보고서의 기본 구조
    environment = dict(os.environ)  # 현재 실행 환경을 자식에게 전달
    environment.update(TEMP='.', TMP='.', TMPDIR='.')  # 임시 산출물도 지정한 빌드 폴더 안에 생성
    def command(label, argv):  # 실제 도구 명령 하나와 결과 기록
        completed = subprocess.run([str(value) for value in argv], cwd=work, env=environment, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)  # 셸 해석 없이30초 이내 실행
        item = {'name': label, 'command': [str(value) for value in argv], 'cwd': str(work), 'returncode': completed.returncode, 'stdout': completed.stdout, 'stderr': completed.stderr}  # 도구의 원래 종료·출력 보존
        report['commands'].append(item)  # 전체 실행 순서에 추가
        (work / (label + '.json')).write_text(json.dumps(item, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')  # 개별 결과도 저장
        return item  # 다음 검증 단계에서 결과 사용
    command('gcc_version', [gcc, '--version'])  # 설치된 컴파일러 판본 확인
    command('qemu_version', [qemu, '--version'])  # 설치된 CPU 에뮬레이터 판본 확인
    flags = ['-march=rv32i', '-mabi=ilp32', '-mcmodel=medany', '-mno-relax', '-msmall-data-limit=0', '-O2', '-g', '-std=c11', '-ffreestanding', '-fno-builtin', '-fno-pic', '-fno-pie', '-fno-stack-protector', '-Wall', '-Wextra', '-Werror', '-nostdlib', '-Wl,--no-relax', '-Tlinker.ld']  # 기본 정수 ISA와32비트 ABI로 제한
    built = command('compile', [gcc, *flags, 'startup.S', 'functions.S', 'abi_probe.S', 'driver.c', '-o', 'program.elf'])  # 실제 RISC-V ELF 생성
    if built['returncode'] != 0:  # 컴파일 실패를 CPU 기능 결과와 구분
        raise RuntimeError('compile failed; see compile.json')  # 원래 도구 로그를 근거로 중단
    readelf = gcc.with_name(gcc.name.replace('gcc', 'readelf'))  # 같은 도구 모음의 ELF 검사기
    attributes = command('elf_attributes', [readelf, '-h', '-A', 'program.elf'])  # ELF32·RISC-V·명령 확장 속성 확인
    if attributes['returncode'] or not re.search(r'Class:\s+ELF32', attributes['stdout']) or 'rv32i2p1' not in attributes['stdout']:  # 호스트 ELF나 다른 ISA 결과를 거절
        raise RuntimeError('unexpected ELF class or ISA')  # 실제 빌드 타깃의 증거가 없으면 실행 성공으로 쓰지 않기
    objdump = gcc.with_name(gcc.name.replace('gcc', 'objdump'))  # 실제 기계어를 읽을 역어셈블러
    disassembly = command('disassembly', [objdump, '-d', '-M', 'no-aliases', 'program.elf'])  # 의사 명령이 풀린 실제 ELF 코드 기록
    if disassembly['returncode'] != 0:  # 기계어 관측 실패 구분
        raise RuntimeError('objdump failed')  # 없는 역어셈블 결과를 만들지 않기
    (work / 'disassembly.txt').write_text(disassembly['stdout'], encoding='utf-8')  # 전체 명령 목록을 빌드 자료에 보관
    executed = command('qemu_cpu', [qemu, '-machine', 'virt', '-cpu', 'rv32i', '-m', '32M', '-bios', 'none', '-kernel', 'program.elf', '-display', 'none', '-serial', 'stdio', '-monitor', 'none', '-no-reboot', '-d', 'in_asm', '-D', 'qemu-instructions.log'])  # RV32I 가상 CPU에서 ELF를 실제 명령으로 실행
    marker = 'FAIL RV32I unsigned byte demo' if args.negative_byte_sign else 'PASS RV32I '  # 정상과 의도적 부호 오류의 기대 결과 분리
    expected_code = 1 if args.negative_byte_sign else 0  # finisher가 내보낼 실제 프로세스 종료 코드
    if executed['returncode'] != expected_code or marker not in executed['stdout']:  # 종료0만으로 기능 통과를 판단하지 않기
        raise RuntimeError('CPU result mismatch; see qemu_cpu.json')  # 실제 UART·종료 결과와 기대가 다른 경우
    report['result'] = 'EXPECTED_FUNCTIONAL_FAILURE' if args.negative_byte_sign else 'PASS'  # 음성 대조 실패를 정상 회로 성공과 구분
    report['checks'] = {key: int(value, 16) for key, value in re.findall(r'(field_checks|checksum_checks|abi_checks|total_checks)=([0-9a-f]{8})', executed['stdout'])}  # 실제 출력의16진수 집계를 정수로 변환
    report['built_source_sha256'] = {name: hashlib.sha256((work / name).read_bytes()).hexdigest() for name in names}  # 결함 복사본과 정상 원본의 해시 구분
    report['elf_sha256'] = hashlib.sha256((work / 'program.elf').read_bytes()).hexdigest()  # 실행한 실제 기계어 식별
    report['qemu_instruction_log_sha256'] = hashlib.sha256((work / 'qemu-instructions.log').read_bytes()).hexdigest()  # CPU 명령 블록 로그 식별
    report['environment_overrides'] = {'TEMP': '.', 'TMP': '.', 'TMPDIR': '.'}  # 빌드 위치 재현에 필요한 환경
    (work / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')  # 최종 실제 실행 기록 저장
    print(executed['stdout'], end='')  # RISC-V 펌웨어가 출력한 원래 결과 전달
    print('REPORT', work / 'report.json')  # 빌드 자료 위치 안내
    return 0  # 기대한 정상 또는 음성 대조가 확인된 러너의 성공

if __name__ == '__main__':  # 스크립트로 실행할 때만 도구 호출
    raise SystemExit(main())  # 러너 자체 종료 코드 전달
```

## 근거와 판본

- [RISC-V RV32I 2.1(2026-01-20): 정수 연산·load/store·FENCE](https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html)
- [RISC-V psABI 1.1 integer registers and 2.1 integer calling convention](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/)
- [QEMU virt generic virtual platform](https://www.qemu.org/docs/master/system/riscv/virt.html)
- [QEMU v10.1.0 virt memory map reference](https://github.com/qemu/qemu/blob/v10.1.0/hw/riscv/virt.c#L77-L99)
- [QEMU v10.1.0 test finisher reference](https://github.com/qemu/qemu/blob/v10.1.0/hw/misc/sifive_test.c#L32-L49)

공식 문서 열람 기준일은2026-10-26입니다. ISA·호출 규약·가상 플랫폼 설명을 근거로 사용하며 함수·C 비교기·검사 입력·부호 오류 대조는 직접 구성했습니다. psABI 웹 문서 전체는 열람 시점의2.0-rc0 초안이며 이 예제가 사용하는 ILP32 정수 ABI는 해당 문서에서 Ratified로 구분되어 있습니다.

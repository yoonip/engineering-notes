# 명령어가 보는 메모리: ISA, byte 순서와 load/store

[Arm과 RISC-V](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 같은 계산을 다른 회로가 실행할 수 있는 이유

ISA(instruction set architecture)는 프로그램이 관찰할 수 있는 명령어·레지스터·동작의 약속이다. Pipeline 단계 수, cache 크기, 실행 유닛 수 같은 microarchitecture와는 구분한다. ABI는 함수 호출, 레지스터 사용, 데이터 배치 등 소프트웨어 간의 약속이다. ISA 이름이 같아도 지원 extension, privilege, 실행 환경과 ABI를 확인해야 같은 binary의 실행 가능성을 판단할 수 있다. 아래 구체적인 명령어 의미는 RISC-V RV32I를 기준으로 한다. Arm 프로세서의 세부 동작을 이 예제에 그대로 대입하지 않는다. [RISC-V 공식 ISA, 소개와 RV32I](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf)

RV32I는 load/store 구조다. 정수 산술은 register에서 수행하고 메모리와의 데이터 이동은 load/store로 한다. “CPU가 메모리를 전혀 사용하지 않는다”는 뜻은 아니다. 명령어 fetch나 실제 cache·bus 동작은 별도의 층위다.

### 주소는 byte를 가리킨다

Byte-addressed memory에서 주소 a와 a+1은 인접 byte다. 32-bit word가 4 byte라면 인접 word의 시작 주소 차이는 4다. 예를 들어 `lw x5, 12(x6)`은 x6의 byte 주소에 부호 있는 offset 12를 더한 위치에서 word를 읽는다. 배열 index를 자동으로 4배 하는 명령이 아니다. 일반적으로 effective address는 $EA=x[rs1]+sext(imm)$에서 계산하며 주소 폭·접근 권한은 ISA와 실행 환경의 규칙을 따른다. [Berkeley CS61C data transfer](https://notes.cs61c.org/content/rv-data-transfer/rv-load-store/)

숫자 $w=\sum_{k=0}^{B-1}b_k2^{8k}$에서 $b_k$는 0…255인 byte다. Little-endian은 $M[a+k]=b_k$, big-endian은 $M[a+k]=b_{B-1-k}$로 배치한다.

| 값 0x12345678 | 주소 a | a+1 | a+2 | a+3 |
|---|---|---|---|---|
| Little-endian | 78 | 56 | 34 | 12 |
| Big-endian | 12 | 34 | 56 | 78 |

Endianness는 여러 byte가 숫자를 이루는 순서다. Byte 내부의 bit 번호나 통신선의 bit 전송 순서를 자동으로 정하지 않는다. RISC-V는 byte-address invariance를 정의하며, 실제 메모리의 endian 설정은 EEI(execution environment interface)가 정한다. 모든 RISC-V가 한 가지 설정만 허용한다고 적어서는 안 된다. [공식 ISA §2.6](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf)

### 폭과 부호를 구분하기

같은 byte 0x80도 unsigned 8-bit로는 128, signed two's-complement로는 −128이다. k-bit pattern u를 정수로 해석하면

$$signed(u)=\begin{cases}u,&u<2^{k-1}\\u-2^k,&u\ge2^{k-1}.\end{cases}$$

RV32I의 `LB`는 8-bit를 읽어 32-bit로 sign-extend하고 `LBU`는 zero-extend한다. `LH/LHU`도 같은 구분을 16-bit에 적용한다. `SB/SH/SW`는 register의 낮은 8/16/32 bit를 저장한다. 따라서 signed와 unsigned load의 결과 차이는 memory가 바뀌어서가 아니라 읽은 bit의 확장 방식 때문이다.

### 정렬과 장치 접근은 추가 조건이다

폭 B의 자연 정렬은 $EA\bmod B=0$이다. RV32I의 자연 정렬 접근은 address-misaligned 예외를 만들지 않지만, 범위·권한 등 다른 이유의 fault까지 없어진다는 뜻은 아니다. 비정렬 접근의 지원·trap·성능과 atomicity는 EEI에 달린다. “항상 성공” 또는 “항상 CPU가 멈춘다”로 일반화하지 않는다. [RISC-V §2.6](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf), [CS61C 정렬 설명](https://notes.cs61c.org/content/rv-data-transfer/rv-load-store/)

MMIO register는 읽기 부작용이나 허용 접근 폭이 있을 수 있다. RAM용 byte 조합을 장치 register에 그대로 적용하면 읽기 횟수 자체가 달라질 수 있다. Endianness와 memory ordering도 다른 문제다. 바이트 순서를 맞췄다고 여러 core·DMA의 관찰 순서가 보장되지는 않는다.

### 구현과 검증

`ByteMemory`는 유한한 bytearray에 자연 정렬된 1·2·4·8-byte 접근을 제공한다. Store는 낮은 bit만 보관하고 load는 byte를 shift/OR로 조립한 뒤 선택적으로 signed 해석을 한다. 이 모델은 RAM의 byte 배치를 보여 주며 RV32/RV64 CPU, trap handler, cache, MMIO를 실행하지 않는다.

검산에서는 직접 작성한 shift/OR 구현을 Python의 `int.to_bytes`·`int.from_bytes`와 비교한다. 두 endian과 네 폭에서 무작위 값, 0x12345678의 명시적 byte 표, 0x80의 부호, 경계·비정렬 거부를 확인한다. 실제 ISA 검증은 compiler/ABI와 target을 고정하고 assembly·disassembly, simulator 또는 보드의 register/memory trace를 명세와 비교하는 단계가 더 필요하다. 기능 trace가 맞더라도 성능이나 memory ordering 전체를 검증한 것은 아니다.

## English

### One architecture, multiple implementations

An ISA defines software-visible instructions, registers and behavior. Microarchitecture includes choices such as pipeline depth, cache size and execution resources. An ABI defines software conventions including calls, register use and data layout. Shared ISA branding alone does not establish binary compatibility: extensions, privilege, execution environment and ABI also matter. Concrete instructions below use RISC-V RV32I; Arm-specific behavior must be checked separately. [Official RISC-V ISA](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf)

RV32I is a load/store architecture: integer arithmetic operates on registers and loads/stores move data to and from memory. This does not mean the processor avoids memory for instruction fetch or that caches and buses perform no other activity.

### Addresses identify bytes

In byte-addressed memory, a and a+1 identify adjacent bytes. Consecutive 32-bit words begin four bytes apart. `lw x5, 12(x6)` adds a signed byte offset of 12 to the base address; it does not automatically scale an array index by four. The general form is $EA=x[rs1]+sext(imm)$, subject to address-width and access rules. [Berkeley CS61C](https://notes.cs61c.org/content/rv-data-transfer/rv-load-store/)

Write a B-byte value as $w=\sum b_k2^{8k}$, with each $b_k$ in 0…255. Little-endian places $b_k$ at address a+k; big-endian places $b_{B-1-k}$ there. Thus 0x12345678 occupies ascending byte addresses as 78/56/34/12 or 12/34/56/78 respectively. This says nothing automatically about bit numbering inside a byte or serial bit-transmission order.

RISC-V specifies byte-address invariance, while the EEI selects the memory endian configuration. Do not assume every RISC-V environment permits only one setting. [ISA §2.6](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf)

### Width and signed interpretation

The byte pattern 0x80 represents unsigned 128 or signed two's-complement −128. For a k-bit pattern u, signed interpretation is u below $2^{k-1}$ and $u-2^k$ otherwise. RV32I `LB` sign-extends an 8-bit load to 32 bits, while `LBU` zero-extends it. `LH/LHU` apply the distinction to 16 bits; `SB/SH/SW` store the register's low 8/16/32 bits. Different extended values do not imply different stored bytes.

### Alignment and device access add constraints

Natural alignment for B-byte access means $EA\bmod B=0$. Naturally aligned RV32I accesses do not raise address-misaligned exceptions, but may still fault for other reasons such as permissions or invalid regions. Support, traps, speed and atomicity of misaligned access depend on the EEI. Neither universal success nor universal failure is correct. [RISC-V §2.6](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf), [CS61C alignment](https://notes.cs61c.org/content/rv-data-transfer/rv-load-store/)

MMIO can restrict widths and attach side effects to reads. Replacing one register access with several byte accesses may change behavior. Endianness is also distinct from memory ordering: correct byte order does not establish observation order across cores or DMA.

### Implementation and verification

`ByteMemory` models finite RAM with naturally aligned 1/2/4/8-byte accesses. Stores retain low bits; loads reconstruct values by shifts/ORs and optionally interpret them as signed. It is not a CPU, trap handler, cache or MMIO simulator.

Tests compare that implementation against independent `int.to_bytes`/`int.from_bytes` encodings across both byte orders and all four widths, checking random values, the explicit 0x12345678 layout, signed 0x80, bounds and misalignment rejection. Actual ISA validation additionally fixes target/compiler/ABI and compares assembly, disassembly and simulator or board traces against the specification. Correct functional traces do not by themselves validate performance or complete memory-ordering behavior.

## 출처 대조 / Source cross-check

RISC-V 공식 20260120 문서의 RV32I §2.6과 Berkeley의 독립 교육 설명을 대조했다. / The official 20260120 ISA's RV32I §2.6 was cross-checked against Berkeley's independent teaching explanation. 확인 / checked: 2026-10-19.

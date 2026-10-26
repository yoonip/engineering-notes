# 칩과 메모리의 공개 검사 코드 | Public test code for chips and memory

[직무 목차](../README.md) · [삼성 DS](../02-삼성DS의직무와요구역량_samsung-ds-role-map.md) · [SK하이닉스](../03-SK하이닉스의직무와요구역량_sk-hynix-role-map.md) · [칩 설계·평가](../06-칩설계와평가분석_chip-design-characterization.md) · [메모리 제품·테스트](../08-메모리제품과테스트개발_memory-product-test-engineering.md)

같은 ‘메모리 오류’라도 RTL 계산, CPU가 접근하는 DRAM, SSD의 파일 읽기·쓰기는 검사 대상이 다릅니다. 이 글은 공개 검증 도구의 실제 코드를 읽고, 어떤 입력과 결과를 비교하는지부터 설명합니다. 사례의 원인 분리 표는 학습용으로 구성했으며, 삼성전자·SK하이닉스의 내부 시험 기록이나 사내 도구 목록은 아닙니다.

## 1. 코드의 종류와 사용하는 위치

| 사례 | 직무에서 연결할 작업 | 가져온 코드의 성격 | 실행·관측 위치 |
| --- | --- | --- | --- |
| RTL 덧셈기 검증 | 회로설계·설계 검증에서 입력과 기대값을 대조합니다. | cocotb 프로젝트가 제공하는 공식 입문 시험 예제입니다. | 개발 PC의 Python이 시뮬레이터 안의 RTL 신호를 제어합니다. |
| 보드의 DRAM 읽기·쓰기 검사 | 초기 구동·제품 평가·Solution HW/SW에서 메모리 경로를 조사합니다. | 실제 U-Boot 부트로더의 `mtest` 명령 구현입니다. | 대상 보드의 CPU가 C 코드를 실행하고 콘솔로 주소·읽은 값·기대값을 기록합니다. |
| SSD 데이터 검증 | Product Engineering·Test·Solution SW/HW·품질에서 데이터 경로와 부하 조건을 검사합니다. | 실제 I/O 시험 도구 fio의 공식 job 예제입니다. | 호스트가 파일·블록 계층에 I/O를 보내고 반환 상태·내용·지연을 관찰합니다. |

공식 예제는 도구 사용법을 보여 주는 코드이고, 실제 구현은 배포되는 도구의 기능을 수행하는 코드입니다. 둘을 구분하여 표시했습니다. 아래 발췌는 출처의 실행문을 임의로 다시 만든 코드가 아닙니다. 생략한 범위·추가한 설명 주석·필요한 실행 환경을 각 사례에 적었습니다.

## 2. 회로설계·검증: RTL의 덧셈 결과가 기대값과 다릅니다

### 먼저 이해할 개념

RTL, register-transfer level은 레지스터와 신호 사이의 동작을 표현하는 하드웨어 기술 수준입니다. testbench는 설계에 입력을 주고 결과를 확인하는 시험 환경입니다. DUT, device under test는 시험 대상이며, 여기서는 실물 칩이 아니라 시뮬레이터가 실행하는 덧셈기입니다.

cocotb 예제의 기본 입력 A·B는 각각 4비트이고 출력 X는 5비트입니다. 4비트 부호 없는 수의 범위는 0–15이며, 최댓값끼리 더하면 30이므로 결과에는 5비트가 필요합니다. 출력 폭이 4비트로 잘못 줄어들면 최상위 자리올림이 잘릴 수 있습니다. 구조는 [원본 `adder.sv` 6–14행](https://github.com/cocotb/cocotb/blob/5de5ec5149f768f9624a400edd508935e9669d51/examples/adder/hdl/adder.sv#L6-L14)에 있습니다.

### 검사 환경과 관측량

| 항목 | 구체적으로 확인할 내용 |
| --- | --- |
| 장비·환경 | 개발 PC, cocotb와 지원 HDL 시뮬레이터입니다. 논리 기능을 보는 단계이므로 오실로스코프나 실물 ATE의 측정 결과로 해석하지 않습니다. |
| 입력 | A·B의 값, 비트 폭, 부호 규칙과 입력을 바꾼 시점입니다. |
| 비교 기준 | Python 기준 모델 `adder_model(A, B)`가 계산한 합입니다. 원본 모델은 정수 두 개의 합을 반환합니다. |
| 관측량 | X의 값, 입력·출력의 시뮬레이션 시각, 실패 입력과 assertion 위치입니다. |
| 남길 결과 | 코드 판본, 시뮬레이터 판본·설정, random seed, 실패 로그와 필요한 파형입니다. 같은 실패를 다시 만들 수 있어야 합니다. |

### 원본 Python 시험 코드

출처는 cocotb `v2.0.0`, commit `5de5ec5149f768f9624a400edd508935e9669d51`의 [`examples/adder/tests/test_adder.py` 34–49행](https://github.com/cocotb/cocotb/blob/5de5ec5149f768f9624a400edd508935e9669d51/examples/adder/tests/test_adder.py#L34-L49)입니다. 파일은 public domain·`CC0-1.0`으로 표시되어 있습니다. 빈 줄을 줄이고 한국어 설명 주석만 추가했습니다. 실행문·함수명·반복 횟수·입력 범위는 그대로입니다. [CC0 이용 조건](licenses/CC0-1.0.txt)을 함께 제공합니다.

```python
@cocotb.test()  # @는 decorator이며 이 비동기 함수를 cocotb 시험으로 등록합니다.
async def adder_randomised_test(dut):  # async def는 기다릴 수 있는 함수를 정의하며 dut는 설계에 접근하는 객체입니다.
    """Test for adding 2 random numbers multiple times"""  # 문자열로 원래 함수의 설명을 남깁니다.
    for _ in range(10):  # range(10)으로 열 번 반복하며 _는 사용하지 않는 반복 변수입니다.
        A = random.randint(0, 15)  # randint는 양 끝을 포함한 정수 중 하나를 뽑아 A에 대입합니다.
        B = random.randint(0, 15)  # B도 같은 범위에서 정하므로 두 입력의 조합이 바뀝니다.
        dut.A.value = A  # 점(.)으로 설계 신호의 속성에 접근하여 입력값을 예약합니다.
        dut.B.value = B  # 두 번째 입력 신호에도 Python 정수를 지정합니다.
        await Timer(2, unit="ns")  # await로 시뮬레이션 시간 2 ns가 지날 때까지 이 시험을 기다리게 합니다.
        assert dut.X.value == adder_model(A, B), (  # assert는 비교가 거짓이면 실패시키며 함수 호출은 기대 합을 계산합니다.
            f"Randomised test failed with: {dut.A.value} + {dut.B.value} = {dut.X.value}"  # f 문자열의 {}에 실패 당시 값을 넣습니다.
        )  # 여러 줄에 적은 실패 메시지 표현을 닫습니다.
```

위 발췌만으로 실행되는 독립 프로그램은 아닙니다. 원본 앞부분은 `random`·`cocotb`·`Timer`를 import하고, 시뮬레이터가 실행 중일 때 `adder_model`을 가져옵니다. `import`는 다른 모듈이 제공하는 이름을 현재 코드에서 사용할 수 있게 하는 문법입니다. 원본의 runner는 HDL 파일과 시험 모듈을 연결합니다. [원본 기준 모델 5–7행](https://github.com/cocotb/cocotb/blob/5de5ec5149f768f9624a400edd508935e9669d51/examples/adder/model/adder_model.py#L5-L7), [runner 52–85행](https://github.com/cocotb/cocotb/blob/5de5ec5149f768f9624a400edd508935e9669d51/examples/adder/tests/test_adder.py#L52-L85)을 함께 읽으시면 됩니다.

Python은 이 사례에서 칩에 올라가는 펌웨어가 아니라 입력 생성·기대값 계산·자동 비교를 맡습니다. `Timer`의 2 ns는 이 예제의 시뮬레이션 대기이며 실물 칩의 전파 지연을 측정한 수치가 아닙니다. 신호 대입과 시험의 성공·실패 규칙은 [cocotb 2.0.0의 Assigning values·Passing and failing tests](https://docs.cocotb.org/en/v2.0.0/writing_testbenches.html#assigning-values-to-signals)에서 확인할 수 있습니다.

### 결과를 해석하고 원인을 좁힙니다

아래 값은 실행 로그를 재현한 것이 아니라 비트 폭을 설명하는 가정입니다. 입력이 A=15, B=15라면 수학적 기대값은 30입니다. X가 14라면 `30 mod 16 = 14`와 일치하므로 4비트 절단을 의심할 수 있습니다. 하지만 이 값 하나만으로 소스의 어떤 줄이 틀렸는지 확정하지는 않습니다.

| 관측한 상황 | 우선 비교할 원인 | 원인을 나눌 확인 | 조치와 재검사 |
| --- | --- | --- | --- |
| 큰 합에서만 상위 비트가 사라집니다. | 출력·중간 신호의 폭, 연결부의 절단입니다. | 작은 합과 자리올림이 필요한 합을 나누고 포트·중간 신호의 폭을 파형과 소스로 대조합니다. | 사양에 맞게 폭을 수정하고 경계 입력과 회귀 시험을 다시 수행합니다. |
| 음수를 넣은 확장 시험만 다릅니다. | signed/unsigned 해석 또는 모델의 범위가 다를 수 있습니다. | 이 원본은 부호 없는 입력 예제라는 조건을 먼저 확인합니다. 부호 있는 제품은 별도 사양·모델이 필요합니다. | 모델과 RTL의 부호·비트 폭을 같은 계약으로 맞춥니다. |
| X에 미정 값이 남거나 시점에 따라 결과가 달라집니다. | 미구동 신호, 초기화·리셋 또는 잘못 고른 관찰 시점입니다. | 첫 구동 시점과 신호 변화, traceback의 오류 종류를 함께 확인합니다. | 구동·초기화·관찰 시점을 사양에 맞추고 같은 입력으로 재검사합니다. |
| 열 번은 통과했지만 경계 입력에서 실패합니다. | 무작위 입력이 필요한 경계를 아직 방문하지 않았습니다. | 기록한 seed와 실제 방문한 A·B 조합을 확인합니다. | 원본 예제를 그대로 통과한 결과와 경계·상태 검증의 범위를 구분합니다. |

4비트 입력 두 개의 조합은 `16 × 16 = 256`개입니다. 원본의 무작위 열 번이 그 조합을 전부 덮는 것은 아닙니다. 실무 검증에서는 제품 사양의 산술 폭·상태·프로토콜·리셋 조건을 추가로 계획합니다. 위 표는 그러한 원인 분리의 예이며 이 글에서 RTL 시뮬레이션을 실행한 결과는 아닙니다.

## 3. 제품 평가·Solution HW/SW: DRAM에서 읽은 값이 다릅니다

### 메모리 칩과 CPU 사이의 경로부터 봅니다

CPU가 주소에 값을 기록했다고 DRAM 셀만 단독으로 검사한 것은 아닙니다. CPU·캐시·메모리 제어기·PHY·보드 배선·전원·DRAM이 읽기·쓰기 경로를 구성합니다. PHY는 디지털 제어 정보와 실제 핀의 신호·타이밍 사이를 연결하는 물리 인터페이스입니다. 같은 비트 오류도 경로의 여러 위치에서 생길 수 있습니다.

U-Boot는 제품의 초기 부팅을 담당하는 공개 부트로더입니다. 여기서는 실제 구현인 `mtest`의 일부를 읽습니다. [공식 명령 설명](https://docs.u-boot.org/en/v2025.01/usage/cmd/mtest.html)은 메모리에 값을 쓰고 다시 읽어 차이를 검사하며, 설정에 따라 기본 시험과 대체 패턴 시험을 선택한다고 설명합니다.

### 검사 환경과 관측량

| 항목 | 구체적으로 확인할 내용 |
| --- | --- |
| 대상·실행 위치 | 평가 보드의 CPU와 DRAM 경로이며 C 코드는 대상 보드의 U-Boot에서 실행됩니다. |
| 기본 수집 수단 | 직렬 콘솔·디버거로 보드 ID, 빌드·초기화 설정, 주소 범위, 오류 주소·기대값·읽은 값과 반복 번호를 기록합니다. |
| 전기 측정 장비 | 증상이 전원·타이밍과 연관되면 전원 공급기·전압계·적절한 프로브와 오실로스코프로 실제 인가 조건을 확인합니다. 고속 DDR 파형은 해당 인터페이스·속도에 맞는 계측 구성이 필요합니다. |
| 시험 조건 | 데이터율, 온도, 전원, 메모리 초기화·training 설정과 캐시·매핑 조건입니다. |
| 비교 대상 | 동일 주소에서 프로그램이 기록한 패턴과 읽어 온 값입니다. ATE가 셀별 결함을 선별하는 양산 시험과 검사 범위를 구분합니다. |

`mtest`는 지정한 범위를 덮어쓰는 명령입니다. 따라서 실제 보드에서는 메모리 맵에서 U-Boot 자체·스택·실행 코드·예약 영역과 겹치지 않는 시험 구간을 먼저 정해야 합니다. 여기서는 주소를 정한 실행 명령을 제시하거나 사용자 장비를 조작하지 않습니다.

### 실제 U-Boot C 구현

출처는 U-Boot `v2025.01`, commit `6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72`의 [`cmd/mem.c`, `mem_test_quick()` 1034–1056행](https://github.com/u-boot/u-boot/blob/6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72/cmd/mem.c#L1034-L1056)입니다. 원문 저작권 표시는 `(C) Copyright 2000, Wolfgang Denk, DENX Software Engineering, wd@denx.de.`입니다. 원문 SPDX `GPL-2.0+`에 따라 이 C 발췌와 추가 설명 주석은 `GPL-2.0-or-later`로 제공합니다. [GPLv2 전문](licenses/GPL-2.0.txt)과 위 원본을 함께 확인하실 수 있습니다.

한국어 주석을 추가하고 빈 줄만 줄였습니다. `for`·대입·비교·출력·반환의 실행문은 원문 그대로입니다. 변수 선언·범위 계산·패턴 변경은 같은 함수 앞부분에 있어 아래 발췌만으로 컴파일되는 프로그램은 아닙니다.

```c
for (addr = buf, val = pattern; addr < end; addr++) { // for의 초기화·조건·증가로 시험 범위의 각 워드를 순회합니다.
    schedule();                                    // U-Boot의 주기 작업 처리 기회를 주는 호출이며 메모리 값을 비교하는 줄은 아닙니다.
    *addr = val;                                   // *는 포인터가 가리키는 메모리이며 기대 패턴을 해당 위치에 씁니다.
    val += incr;                                   // +=는 누적 대입이며 다음 주소에서 사용할 값을 증가량만큼 바꿉니다.
}                                                  // 기록 루프의 블록을 닫습니다.
puts("Reading...");                                // 문자열을 출력하여 읽기 단계가 시작됨을 알립니다.
for (addr = buf, val = pattern; addr < end; addr++) { // 같은 시작 주소·초기 패턴으로 읽기 루프를 시작합니다.
    schedule();                                    // 긴 검사 중에도 U-Boot의 주기 작업을 처리할 기회를 줍니다.
    readback = *addr;                               // 메모리에서 읽은 값을 readback 변수에 대입합니다.
    if (readback != val) {                          // if는 != 비교가 참일 때만 오류 처리 블록을 실행합니다.
        ulong offset = addr - buf;                 // 두 포인터의 차이로 시작점에서 떨어진 워드 수를 구합니다.
        printf("\nMem error @ 0x%0*lX: found %0*lX, expected %0*lX\n", // printf의 형식 문자열로 오류 위치·값을 표시합니다.
               plen, start_addr + offset * sizeof(vu_long), // sizeof로 워드 수를 바이트 주소 오프셋으로 바꿉니다.
               plen, readback, plen, val);         // %*의 폭과 실제 읽은 값·기대값을 순서대로 전달합니다.
        errs++;                                    // ++는 오류 개수를 하나 늘립니다.
        if (ctrlc())                               // 함수가 중단 요청을 반환하면 다음 return을 실행합니다.
            return -1;                             // 이 함수의 중단 표시를 호출자에게 돌려줍니다.
    }                                              // 값 불일치 처리 블록을 닫습니다.
    val += incr;                                   // 다음 주소에서 비교할 기대값도 기록 때와 같은 규칙으로 바꿉니다.
}                                                  // 읽기·비교 루프를 닫습니다.
```

`ulong`은 이 프로젝트의 unsigned long 계열 타입이고 `vu_long`은 volatile unsigned long 계열 타입입니다. 실제 워드 크기는 빌드 대상에 따라 다릅니다. 포인터 `addr`를 한 번 증가시키면 한 바이트가 아니라 가리키는 타입 한 개 크기만큼 이동합니다. `volatile`은 접근을 보존하는 데 관련되지만 CPU 캐시를 자동으로 끄거나 모든 접근 순서를 보장하는 장치가 아닙니다. 캐시·매핑 조건은 [DMA·캐시의 경계](../../현장계측과검증_measurement-validation/펌웨어와디버깅_firmware-debugging/DMA버퍼와캐시의경계_cortex-m7-cache-dma.md), 타입 정의는 [U-Boot의 `include/linux/types.h`](https://github.com/u-boot/u-boot/blob/6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72/include/linux/types.h)에서 이어집니다.

C가 필요한 이유는 대상 보드의 주소·자료형·포인터 접근과 부트 환경을 직접 다루기 때문입니다. Python 호스트는 콘솔과 조건을 기록·비교하는 별도 자동화에 쓸 수 있지만, 그 수집기를 이 C 원본에 있는 코드처럼 제시하지는 않습니다.

### 읽은 값의 차이를 불량 원인과 연결합니다

32비트 워드라고 가정하여 기대값이 `0x01234567`, 읽은 값이 `0x01234563`이라면 두 값의 XOR은 `0x00000004`입니다. 이는 비트 2가 다르다는 뜻입니다. 이 계산은 설명용 예이며 실물 DRAM의 특정 비트 불량을 관측한 기록은 아닙니다.

| 관측한 상황 | 가능한 원인 | 비교할 근거·장비 | 조치 뒤 확인할 항목 |
| --- | --- | --- | --- |
| 여러 주소에서 같은 데이터 비트가 반복해서 다릅니다. | DQ 경로, 배선·접속, 특정 lane 설정 또는 칩 내부 문제가 후보입니다. | 오류 비트별 분포와 주소·시료·보드 교체 결과를 나누고, 해당 신호·전원·초기화 설정을 대조합니다. | 보드·부품·설정 중 무엇을 바꾸었는지 남기고 기존 실패 패턴과 다른 패턴을 다시 확인합니다. |
| 특정 주소 간격으로 오류가 생깁니다. | 주소 디코딩·매핑, 경계 설정이나 특정 영역 문제가 후보입니다. | 오류 주소의 규칙, 메모리 맵, 실제 용량·칩 선택 설정을 대조합니다. | 잘못된 범위를 수정했다면 원래 오류와 범위·경계 접근을 함께 재검사합니다. |
| 데이터율을 낮추면 통과합니다. | 타이밍 여유·training·SI/PI가 후보입니다. | 같은 패턴·주소에서 데이터율·온도·전원을 한 조건씩 바꾸고 필요한 파형을 측정합니다. | 낮은 속도의 통과만으로 정격 속도 문제를 해결한 것으로 처리하지 않습니다. |
| CPU 검사와 DMA·운영 중 결과가 다릅니다. | 캐시·일관성·버퍼 소유권 또는 경로별 접근이 후보입니다. | 두 시험의 캐시 상태·매핑·기준 주소·완료 동기화를 확인합니다. | 각 경로의 계약을 맞추고 같은 데이터로 교차 확인합니다. |

이 판본의 `do_mem_mtest()`는 누적 오류 `count`를 출력하지만 마지막 반복의 `errs`로 반환값을 만듭니다. [원본 1106–1138행](https://github.com/u-boot/u-boot/blob/6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72/cmd/mem.c#L1106-L1138)을 읽으면 두 값을 구분할 수 있습니다. 자동 판정은 종료 상태만 떼어 쓰지 않고 누적 오류 수·완주 여부·중단 기록을 함께 확인해야 합니다. 또한 빠른 패턴 검사 통과는 메모리의 모든 고장 기구·사용 조건·장기 신뢰성이 통과했다는 뜻이 아닙니다.

## 4. Product Engineering·Test·품질: SSD는 완료됐지만 내용이 맞지 않습니다

### 성능과 데이터의 정확성을 나눕니다

SSD 시험에서 IOPS는 초당 처리한 I/O 수이고, latency는 정한 요청부터 완료 지점까지의 시간입니다. 데이터 검증은 그 요청에서 기대한 내용을 다시 얻는지 확인합니다. 많은 I/O가 빨리 끝났더라도 내용이 다르면 성능 수치만으로 정상 판정할 수 없습니다.

fio는 Linux I/O 계층·스케줄러와 여러 부하를 시험하기 위해 만들어진 공개 도구입니다. [프로젝트 README의 목적·공식 미러 설명](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/README.rst#L1-L39)을 확인했습니다. 여기서는 `fio-3.39`의 공식 파일을 읽으며, 이를 특정 회사의 제품 인증 절차로 부르지는 않습니다.

### 공식 job 파일에서 가져온 설정

출처는 commit `a6e474c9e896e4ba1eb40066a03402afb040710a`의 [`examples/basic-verify.fio` 3–9행](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/examples/basic-verify.fio#L3-L9)입니다. C나 Python 소스가 아니라 fio가 읽는 설정 문법입니다. 프로젝트는 [COPYING의 GPLv2](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/COPYING)를 제공합니다. 아래 발췌와 설명 주석도 GPLv2로 제공하며 [라이선스 전문](licenses/GPL-2.0.txt)을 연결했습니다.

설정값을 바꾸지 않고 각 행 바로 위에 설명 주석을 추가했습니다. 원본 마지막의 장치 경로 `filename` 행은 이 발췌에 포함하지 않았습니다. 이는 바로 실행할 완성 job이 아니며, 파일 시험을 할 때에는 새 시험 디렉터리·파일과 크기를 따로 정합니다. 원본 주석에도 장치 대신 파일을 사용하는 방법이 설명되어 있습니다.

```ini
# []는 job 구역의 이름을 지정합니다.
[write-and-verify]
# rw는 I/O 종류이며 randwrite는 무작위 위치 쓰기입니다.
rw=randwrite
# bs는 한 I/O의 크기이며 이 예제의 4k는 4 KiB입니다.
bs=4k
# direct=1은 지원 환경에서 비버퍼 I/O를 요청합니다.
direct=1
# ioengine은 I/O 실행 방식이며 여기서는 Linux libaio를 사용합니다.
ioengine=libaio
# iodepth는 진행 중인 I/O의 목표 수이며 실제 달성 분포를 확인해야 합니다.
iodepth=16
# verify는 기록 내용의 검증 방식을 정하며 여기서는 CRC32C입니다.
verify=crc32c
```

CRC는 데이터에서 계산한 검사값입니다. 이 예제는 검증용 헤더와 데이터를 기록한 뒤 읽은 내용과 검사값·위치 정보를 대조합니다. CRC는 NAND 내부의 ECC와 같은 계층이 아니며, 오류를 검출한 사실만으로 NAND 셀·컨트롤러·펌웨어·호스트 중 원인을 정할 수 없습니다.

`direct=1`은 모든 하드웨어 캐시가 꺼진다는 뜻이 아닙니다. `iodepth=16`도 언제나 실제 큐에 16개가 들어 있었다는 측정 결과가 아닙니다. 정의와 적용 조건은 고정 판본의 [HOWTO `direct` 1133–1137행](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/HOWTO.rst#L1133-L1137), [`iodepth` 3246–3255행](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/HOWTO.rst#L3246-L3255), [`verify` 3821행 이후](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/HOWTO.rst#L3821-L3833)에 있습니다.

### 장비와 기록을 결과 해석에 연결합니다

| 업무 | 장비·소프트웨어와 입력 | 측정·확인할 항목 |
| --- | --- | --- |
| 데이터 무결성 시험 | 시험 호스트·대상 SSD·fio와 새로운 시험 파일입니다. | 요청 오류, 검증 오류·offset, 첫 실패 시각, 시험 파일·모델·펌웨어·OS·드라이버 판본입니다. |
| 부하 성능 비교 | 같은 SSD·인터페이스·파일시스템·I/O 크기·읽기/쓰기 비율·큐 깊이를 사용합니다. | 처리량·IOPS·지연 분포와 실제 달성한 큐 깊이, CPU 사용량입니다. |
| 전원·열과 연계한 원인 분석 | 전원 공급기·오실로스코프·온도 측정과 장치 로그를 함께 사용합니다. | 전압 변화·온도·리셋·시간초과와 실패 I/O의 시간 관계입니다. |
| 반복 시험·품질 보고 | 원시 결과·설정·장치 이력과 실패 데이터를 보관합니다. | 초기 상태·시험 순서·재시험·교체한 구성요소와 최초 실패를 연결합니다. |

| 관측한 상황 | 원인 후보 | 원인을 나누는 방법 | 조치와 재검사 |
| --- | --- | --- | --- |
| 검증 실패가 특정 offset에서 반복됩니다. | 매핑·기록 데이터·파일 경계 또는 저장 경로의 오류입니다. | 기대/실제 블록, 헤더·offset, 원본 파일 범위와 동시 쓰기 여부를 비교합니다. | 수정한 계층과 기존 실패 offset을 기록하고 다른 경계·부하도 확인합니다. |
| I/O 오류 없이 CRC가 다릅니다. | 내용이 달라졌지만 명령 완료 경로가 오류로 보고하지 못한 상황입니다. | 호스트 메모리·파일시스템·드라이버·SSD의 경계를 나누고 비교 가능한 장치·호스트를 교체합니다. | 발견 위치와 원인을 구분하여 기록하고 원인 조치 전후 같은 데이터 검증을 반복합니다. |
| 검증은 통과하지만 드문 지연이 큽니다. | GC·열 관리·큐잉·다른 부하 등이 후보입니다. | 평균만 보지 않고 지연 분포와 온도·장치 상태·동시 작업을 같은 시간축에 맞춥니다. | 정상 상태와 일시 상태를 나누고 같은 부하·초기 조건으로 재평가합니다. |
| 전원 중단 이후 내용만 다릅니다. | 쓰기 완료·flush·영속성 계약이나 복구 경로가 후보입니다. | 중단 전 명령·완료·flush 순서와 재기동 후 내용·장치 로그를 비교합니다. | 일반 fio 검증 통과와 전원 차단 내성을 별도 시험 항목으로 기록합니다. |

실패 블록 분석에는 fio의 `verify_dump`가 원래 블록과 읽은 블록을 파일로 남기는 기능을 제공합니다. 기본값은 꺼짐이며 위 공식 job에 이 옵션을 추가하지는 않았습니다. [원본 HOWTO 3946–3956행](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/HOWTO.rst#L3946-L3956)에 `verify_fatal`과 함께 설명되어 있습니다. 보존된 실패 데이터를 비교하는 일과 원인을 확정하는 일은 구분해야 합니다.

이 글에서는 fio를 실행하거나 SSD를 측정하지 않았습니다. 파일 대상 검증, 실제 SSD의 성능·전원 차단 시험, NAND 셀 수준의 생산 시험은 서로 다른 결과로 기록합니다. 상세한 영속성 계약은 기존 [NVMe 쓰기 완료와 영속성](../../설계와검증사례_engineering-cases/NVMe의쓰기완료와영속성_nvme-write-persistence.md)에서 이어집니다.

## 5. 원인 분석 보고서에 남길 내용

어떤 도구를 사용했는지보다 실패를 다시 찾아갈 수 있는 기록이 중요합니다.

1. 제품·보드·파일·RTL 등 시험 대상과 사양을 적습니다.
2. 원본 코드의 판본과 실제 사용한 설정·변경점을 적습니다.
3. 입력·조건·기대값·실제값·단위·시각을 저장합니다.
4. DUT의 기능 실패, 시험 환경 오류, 미완료를 나눕니다.
5. 원인 후보를 둘 이상 세우고 어느 대조가 후보를 나누는지 적습니다.
6. 변경 후에는 최초 실패 조건과 새로 영향을 받는 범위를 함께 확인합니다.

공통 판정과 누적·재시험 기록은 [검사 결과의 판정과 기록](../11-검사결과의판정과기록_test-decisions-evidence.md)에서 읽으실 수 있습니다.

## 출처와 확인 범위

확인일은 2026-10-26입니다. 원본 코드·관련 공식 설명과 라이선스를 읽고 발췌의 실행문을 대조했습니다. 표의 불량 상황·진단 순서는 원인을 설명하기 위한 자체 학습 사례입니다. RTL 시뮬레이션, U-Boot 보드 시험, SSD 시험을 실행한 것으로 표시하지 않습니다.

| 출처 | 확인한 범위 |
| --- | --- |
| [cocotb v2.0.0 공식 adder 예제](https://github.com/cocotb/cocotb/tree/5de5ec5149f768f9624a400edd508935e9669d51/examples/adder) | Python 시험·기준 모델·SystemVerilog 포트·runner와 파일별 CC0 표시입니다. |
| [cocotb 2.0.0 시험 작성 문서](https://docs.cocotb.org/en/v2.0.0/writing_testbenches.html) | 설계 신호 접근·값 대입·시험 성공/실패와 비동기 대기입니다. |
| [U-Boot v2025.01 `cmd/mem.c`](https://github.com/u-boot/u-boot/blob/6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72/cmd/mem.c) · [명령 문서](https://docs.u-boot.org/en/v2025.01/usage/cmd/mtest.html) | `mem_test_quick()`·호출자·오류 누적/반환·기본/대체 검사와 GPL-2.0+ 표시입니다. |
| [fio-3.39 공식 예제](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/examples/basic-verify.fio) · [HOWTO](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/HOWTO.rst) · [COPYING](https://github.com/axboe/fio/blob/a6e474c9e896e4ba1eb40066a03402afb040710a/COPYING) | 쓰기·읽기 검증 예제, I/O 깊이·direct·CRC·dump의 조건과 GPLv2입니다. |

## English

Three cases connect a CC0 cocotb adder example, the GPL-2.0-or-later U-Boot memory-test implementation, and a GPLv2 fio verification job to RTL verification, board memory evaluation and storage testing. Pinned upstream versions and excerpt ranges identify the source of executable statements. Korean comments explain syntax and purpose. Failure scenarios and diagnostic comparisons are educational constructions; no RTL simulation, board memory test or SSD measurement was performed for this article.

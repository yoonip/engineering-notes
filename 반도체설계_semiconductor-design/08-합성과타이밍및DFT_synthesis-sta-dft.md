# 합성·타이밍 제약·DFT의 연결 / Synthesis, static timing and design for test

합성은 RTL의 상태와 연산을 논리 셀의 연결로 바꾸는 과정입니다. STA는 그 연결이 주어진 클록·입출력 조건에서 시간을 지키는지 분석합니다. DFT는 만들어진 칩의 결함을 검사할 수 있도록 회로와 접근 경로를 설계하는 일입니다. 세 작업은 파일과 제약을 주고받지만 같은 성공 기준을 사용하지 않습니다. 공개 자료 확인일은 2026-10-26이며, 아래 수치는 실제 라이브러리의 측정값이 아닌 자체 예입니다.

## 1. 문법을 읽는 단계와 셀에 대응시키는 단계

합성기는 먼저 파일을 읽고 top module, 파라미터, 조건부 컴파일과 계층을 확정합니다. 이를 elaboration이라고 합니다. 이어 연산·선택·상태 요소를 정리하고, 목표 라이브러리의 게이트·플립플롭 등으로 대응시키는 technology mapping을 수행합니다. `a+b`라는 한 줄도 비트 폭·부호·상수·타이밍 목표에 따라 다른 회로가 됩니다.

매핑된 넷리스트는 ‘셀 인스턴스의 어떤 핀이 어느 신호에 연결됩니다’라는 구조를 담습니다. 셀 수가 같아도 드라이브 강도·입력 부하·배선과 전압 조건이 다르면 지연은 달라집니다. RTL 코드 줄 수로 면적이나 최고 주파수를 계산하지 않습니다.

| 입력 | 합성·검증에서 확인할 내용 |
|---|---|
| RTL과 파일 목록 | top·파라미터·매크로 정의·비트 폭·메모리 모델을 맞춥니다. |
| Liberty 라이브러리 | 사용할 셀과 해당 PVT 조건, 기능·타이밍·전력 정보를 확인합니다. |
| SDC | 클록·외부 입출력 시간·부하·예외 경로의 의도를 확인합니다. |
| 전원 의도·테스트 요구 | 전원 영역과 isolation·retention, scan·메모리 시험 요구를 연결합니다. |
| 물리 정보 | 사용할 흐름에 따라 셀 크기·핀·배선 추정 조건을 제공합니다. |

[Yosys의 셀 라이브러리 매핑 설명](https://yosyshq.readthedocs.io/projects/yosys/en/v0.49/using_yosys/synthesis/cell_libs.html)은 대상 라이브러리와 매핑을 읽는 출발점입니다. 합성 후에는 미해결 셀·예상하지 않은 래치·비트 잘림·부호 확장·사라진 출력과 경고를 확인합니다. 가능하면 RTL과 매핑 결과의 등가성을 정해진 리셋·미정값·메모리 가정 아래에서 비교합니다. 등가성 성공도 실제 배선의 타이밍이나 제조 결함을 검사한 결과는 아닙니다.

## 2. SDC는 분석할 시간 관계를 정합니다

SDC는 Tcl을 바탕으로 클록과 시간 제약을 표현하는 형식입니다. 아래 한 줄은 [ORFS 공식 튜토리얼의 `create_clock` 예](https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/FlowTutorial.html#timing-constraints)에서 문법을 가져와 포트명·클록명·주기를 자체 예로 바꾼 것입니다. 명령 전체의 실행 흐름이나 실제 설계 제약 세트는 아닙니다.

```tcl
create_clock -name core_clk -period 10.0 [get_ports {clk}] ;# clk 포트를 찾아 core_clk의 주기를 현재 시간 단위로 10.0으로 정합니다.
```

숫자 10.0을 무조건 10 ns로 읽지 않습니다. 선택한 도구와 라이브러리의 시간 단위를 확인해야 합니다. 이 예에서는 설명을 위해 1단위를 1 ns로 가정하므로 100 MHz에 해당합니다. 클록 한 줄만으로 외부 입력이 언제 도착하고 출력이 언제까지 필요한지까지 정해지지는 않습니다.

| 제약 | 필요한 질문 |
|---|---|
| 주 클록·generated clock | 실제 클록원, 분주·배수·위상 관계가 무엇인지 확인합니다. |
| 입력 지연·출력 지연 | 외부 장치와 보드에 할당한 최대·최소 시간 예산을 확인합니다. |
| 입력 slew·출력 부하 | 신호 변화 속도와 구동해야 할 정전용량의 모델을 확인합니다. |
| uncertainty·latency | 지터·모델링 여유와 클록 경로 지연의 적용 범위를 확인합니다. |
| 경로 예외 | 기능상 검사하지 않을 관계나 여러 주기가 허용되는 관계의 근거를 확인합니다. |

제약의 포트·핀 검색 결과가 비어 있으면 의도한 경로에 적용되지 않을 수 있습니다. 미제약 endpoint, 클록이 없는 레지스터, 잘못 정의한 generated clock을 먼저 찾습니다. 보고서의 양수 slack만 보고 분석 범위가 충분하다고 판단하지 않습니다.

## 3. Setup과 hold는 최대·최소 지연을 각각 봅니다

플립플롭의 clock-to-Q는 클록 사건 뒤 출력이 바뀌기까지의 지연입니다. 조합 경로를 지나 다음 플립플롭에 도착한 데이터는 capture 에지 전에 setup 시간만큼, 그 뒤에는 hold 시간만큼 안정되어야 합니다. [MIT 6.004의 단일 클록 타이밍 설명](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/)은 최대 전파 지연과 최소 오염 지연을 이 두 조건에 연결합니다.

자체 단순 모형에서 launch 클록 도착을 0, capture 클록의 같은 주기 도착을 s라고 정합니다. s가 양수면 capture 클록이 더 늦습니다. 다음 capture 에지는 T+s입니다. 추가 여유 u를 보수적으로 더하면 다음과 같습니다.

```math
\text{setup slack}=T+s-(t_{cq,max}+t_{comb,max}+t_{setup}+u_{setup})
```

```math
\text{hold slack}=t_{cq,min}+t_{comb,min}-(s+t_{hold}+u_{hold})
```

실제 STA는 상승·하강, 서로 다른 클록·에지, 셀의 조건부 타이밍 아크, 변동 모델 등도 다룹니다. 위 식은 부호와 최대·최소의 차이를 익히는 한 경로 예입니다.

| 자체 가정 | 값 |
|---|---:|
| T / s | 2.00 ns / 0.05 ns |
| 최대 clock-to-Q / 조합 지연 | 0.15 ns / 1.60 ns |
| setup / setup 여유 | 0.10 ns / 0.05 ns |
| 최소 clock-to-Q / 조합 지연 | 0.05 ns / 0.03 ns |
| hold / hold 여유 | 0.08 ns / 0.02 ns |

Setup slack은 `2.00+0.05−(0.15+1.60+0.10+0.05)=0.15 ns`입니다. Hold slack은 `0.05+0.03−(0.05+0.08+0.02)=−0.07 ns`입니다. 같은 경로에서 setup은 만족하고 hold는 위반할 수 있습니다. 주기를 길게 하는 방법은 이 모형의 hold 식에 들어가지 않습니다. 최소 경로 지연·클록 관계·셀·배선을 바꾸는 검토가 필요합니다. 더 자세한 경로 해석은 [setup·hold와 정적 타이밍](../전자컴퓨터공학_ece/15-FPGA-ASIC설계_fpga-asic/해설_notes/너무늦어도너무빨라도문제다_setup-hold-static-timing.md)에서 읽으실 수 있습니다.

## 4. 예외 경로와 CDC는 회로 동작의 근거가 필요합니다

False path는 특정 시간 관계를 STA 검사에서 제외하는 지정입니다. 실제 배선을 제거하거나 신호가 안전하게 전달되도록 바꾸지 않습니다. ‘음수 slack을 없애기 위해’ 넓은 경로를 제외하면 실제 실패를 가릴 수 있습니다.

Multicycle path는 기능상 여러 클록 주기 뒤의 capture를 허용하는 관계입니다. 예를 들어 송신값을 두 주기 유지하고 수신 enable도 그 관계를 지킨다는 근거가 있어야 합니다. Setup의 기준 에지를 옮기면 hold 검사 에지의 관계도 달라질 수 있습니다. 흔히 쓰이는 설정 쌍을 복사하기 전에 시작·끝 클록과 실제 보고서의 에지 쌍을 확인합니다. [OpenSTA 명령 문서의 `set_false_path`·`set_multicycle_path`](https://opensta.readthedocs.io/en/latest/Commands/)는 대상과 setup·hold, start·end 옵션을 구분합니다.

CDC는 서로 다른 클록 영역 사이의 전달입니다. 비동기 신호를 일반적인 단일 클록 setup 식으로만 처리할 수 없습니다. 단일 비트 동기화기, handshake, 비동기 FIFO 등 전달 대상에 맞는 구조와 메타안정성 가정을 검토합니다. 버스 각 비트에 동기화기를 붙이는 것만으로 한 단어의 일관성이 보장되지는 않습니다. CDC 도구 검사·회로 구조·프로토콜 검증과 STA 예외를 함께 맞춥니다. 리셋 영역을 넘는 관계인 RDC도 별도로 봅니다.

## 5. PVT·MMMC·전원 의도

PVT는 공정 변화(process), 전원 전압(voltage), 온도(temperature)의 조건입니다. MMMC는 여러 동작 모드와 여러 분석 코너를 함께 관리하는 방식입니다. 기능 모드·scan 모드, 주파수·전원 상태, 셀 라이브러리와 배선 RC 조건을 조합합니다. 가장 느린 셀 코너 하나만 확인하면 최소 지연과 hold, 다른 전원 모드의 문제를 놓칠 수 있습니다. 온도에 따른 지연의 방향도 모든 공정에서 같다고 고정하지 않습니다.

[OpenLane의 Timing Corners 문서](https://openlane2.readthedocs.io/en/latest/usage/timing_corners.html)는 셀과 상호연결의 코너를 나누어 설명합니다. 실제 프로젝트에서는 PDK·라이브러리 제공자가 허용한 분석 조합과 변동·여유 적용 방법을 확인합니다. 존재하는 파일 이름을 임의로 조합한 것과 승인된 분석 조건은 다릅니다.

UPF는 전원 영역·공급·전원 스위치·isolation·level shifter·retention 등의 전원 의도를 전달하는 형식입니다. Isolation은 꺼진 영역의 출력이 동작 중인 영역에 미정값을 퍼뜨리지 않도록 정한 상태로 만드는 기능입니다. Retention은 필요한 상태를 전원 상태 전환 사이에 보존하는 기능입니다. 실제 셀·핀·제어 순서와 연결해야 하며 UPF 파일이 물리 전원 배선을 대신하지 않습니다. [Accellera의 UPF 교육 개요](https://www.accellera.org/resources/videos/upf-tutorial-2013)는 이 전원 구조와 상태의 개념을 구분합니다. 이 글에서 영상 전체를 재생한 것은 아닙니다. [OpenROAD UPF utility](https://openroad.readthedocs.io/en/latest/main/src/upf/README.html)의 power domain·power switch·isolation 설명을 읽되, 나열된 명령의 존재만으로 모든 IEEE UPF 기능과 상용 흐름의 동등성을 주장하지 않습니다.

## 6. DFT와 메모리 자체 시험

| 방법 | 검사 접근을 만드는 방법 | 구분할 한계 |
|---|---|---|
| Scan | 플립플롭을 시험용 이동 경로로 연결해 상태를 넣고 읽습니다. | 정상 동작의 모든 기능 검증을 대체하지 않습니다. |
| ATPG | 정한 결함 모델에서 결함을 드러낼 시험 패턴을 만듭니다. | 결함 모델별 coverage와 검출하지 못한 항목이 남습니다. |
| MBIST | 칩 안의 제어기가 메모리 주소·쓰기·읽기 순서를 실행합니다. | 메모리 종류·포트·고장 모델·속도와 시험 알고리즘을 맞춰야 합니다. |
| Repair·ECC | 예비 자원 치환이나 오류 정정으로 지정한 오류에 대응합니다. | 오류를 찾는 시험, 결함 수리, 운용 중 정정은 같은 기능이 아닙니다. |

자체 예로 32개 플립플롭을 한 scan chain에 넣으면 한 패턴의 상태 이동에 32번의 shift가 필요합니다. 두 개의 16비트 chain을 병렬로 쓰면 16번으로 줄일 수 있지만 핀·제어·압축·배선과 시험 전력 조건이 바뀝니다. Capture·제어·추가 패턴 시간을 제외한 단순 비교입니다.

MBIST에서는 SRAM의 읽기 지연, write mask, 포트 충돌, 테스트 클록과 전원 상태가 중요합니다. 메모리 기능 모델로 연결을 검사한 결과와 실제 배열의 결함 검출·수리 검증은 구별합니다. [Siemens Tessent MemoryBIST의 공식 설명](https://resources.sw.siemens.com/cs-CZ/fact-sheet-tessent-memorybist-fact-sheet/)은 내장 메모리의 시험·진단·수리 역할을 제시합니다. 개별 메모리 IP의 지원 여부나 알고리즘·명령은 해당 판본 문서가 필요합니다.

흐름은 ‘시험 요구 정의 → DFT 규칙 확인 → scan·MBIST 삽입과 연결 → 기능·테스트 모드 검증 → 배치 후 chain·배선 조정 → 테스트 모드 STA·전력 검토 → 패턴·결함 coverage 확인’으로 읽습니다. 일부 단계는 선택한 도구 흐름에서 결합되거나 반복됩니다. [OpenROAD DFT 설명](https://openroad.readthedocs.io/en/latest/main/src/dft/README.html)은 scan 치환·chain 구성을 다루며, [Synopsys TestMAX DFT 공개 설명](https://www.synopsys.com/implementation-and-signoff/test-automation/testmax-dft.html)은 scan·test point·압축 등을 다룹니다. 서로 다른 도구의 지원 범위를 같은 기능표로 합치지 않습니다.

## 7. 보고서가 이상할 때의 확인 순서

| 관측 | 먼저 비교할 항목 |
|---|---|
| 셀 수가 갑자기 줄었습니다. | 출력 연결·상수화·리셋 가정·미해결 black box를 확인합니다. |
| 경로가 보고서에서 사라졌습니다. | 클록·입출력 제약과 false path의 대상 범위를 확인합니다. |
| Setup 수정 뒤 hold가 나빠졌습니다. | 최소 지연과 clock skew, 바뀐 버퍼·셀을 확인합니다. |
| 기능 모드는 통과하고 scan 모드는 실패합니다. | test enable·test clock·chain 순서·시험 전원 조건을 확인합니다. |
| MBIST가 시간 초과됩니다. | 메모리 지연·포트 연결·시험 시작/완료 handshake와 클록을 확인합니다. |

다음 단계에는 매핑 넷리스트, 정확히 사용한 라이브러리·SDC·전원 의도, 메모리 물리·기능 뷰, DFT 연결 정보와 모드별 보고서를 함께 전달합니다. [배치·배선](09-배치배선과전력설계_physical-implementation.md)에서 배선과 실제 클록 경로가 생기면 STA 결과를 다시 계산합니다.

[RTL·검증·아날로그 모델](07-Verilog와SystemVerilog의연결_rtl-verification-ams.md) · [물리 검증](10-DRC와LVS및PEX_physical-verification.md) · [반도체 설계 목차](README.md)

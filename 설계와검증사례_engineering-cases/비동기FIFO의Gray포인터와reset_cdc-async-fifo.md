# 비동기 FIFO의 Gray 포인터와 reset | Gray pointers and reset in an asynchronous FIFO

## 같은 큐를 서로 다른 클록에서 읽고 씁니다

센서가 자료를 만들고 처리기가 소비하는 속도가 다르면 FIFO가 두 동작 사이를 연결합니다. CDC는 clock domain crossing, 즉 서로 다른 클록의 경계를 건너는 전달입니다. 단일 클록 FIFO의 점유량 레지스터를 두 클록의 `always` 블록에서 함께 갱신하면 어느 edge가 그 상태를 소유하는지 불명확해집니다. 비동기 FIFO는 쓰기·읽기 포인터를 각자의 도메인에서 관리하고, 상대 포인터의 전달본으로 쓰기와 읽기를 제한합니다.

이 사례에서는 [SV DUT·testbench와 Python 실행기](../예제_examples/실무검증_practical-validation/cdc_async_fifo/README.md)를 실제 Icarus Verilog로 컴파일하고 실행했습니다. 깊이는 4, 자료는 32비트, write/read 주기는 10/14ns입니다. 같은 시각의 상승 edge도 포함하지만 모든 주파수·위상 조합을 탐색한 시험은 아닙니다. 저장소에서 직접 만든 교육용 회로이며 FPGA·실제 칩·장비를 측정한 결과는 아닙니다.

## 주소보다 포인터가 한 비트 더 필요한 이유

네 칸의 주소는 2비트로 표현합니다. 그러나 쓰기와 읽기의 주소가 모두 `00`일 때 비어 있는지, 한 바퀴 돌아 꽉 찼는지는 주소만으로 구별할 수 없습니다. 포인터를 3비트로 만들고 0~7을 순환시키며, 하위 두 비트만 메모리 주소로 사용합니다. 추가 비트는 같은 주소의 서로 다른 바퀴를 구별합니다.

다른 도메인에 넘기는 값은 binary 포인터를 Gray 코드로 바꾼 값입니다. Gray 코드는 인접한 카운트 사이에서 한 비트만 바뀌도록 만든 표현입니다. 예를 들어 binary `011→100`은 세 비트가 바뀌지만, Gray `010→110`은 한 비트만 바뀝니다. `Gray = binary ^ (binary >> 1)`로 계산합니다. `^`는 비트별 배타적 논리합, `>>`는 오른쪽 비트 이동입니다.

이 회로는 binary 포인터로 주소를 만들고 Gray 포인터를 등록한 뒤, 상대 클록의 레지스터 두 단을 거쳐 전달합니다. 목적 도메인이 느리면 중간 카운트를 건너뛸 수 있습니다. 모든 카운트를 하나씩 보아야 하는 이벤트 수신기와는 다릅니다. 이 구조와 full/empty 판정은 [Cummings의 원 논문 §4~6, Rev 1.2](https://github.com/zhangzek/Clock-Domain-Crossing-Design/blob/master/doc%26paper/CummingsSNUG2002SJ_FIFO1.pdf)에 있는 방식을 참고했습니다.

## full 비교에서 한 비트만 반전하면 덮어씁니다

읽기 포인터가 binary 0, Gray `000`일 때 네 번 쓴 포인터는 binary 4, Gray `110`입니다. full은 동기화된 read Gray의 상위 두 비트를 반전한 `110`과 다음 write Gray를 비교해야 합니다. binary 포인터의 wrap 비트 하나를 뒤집는 규칙을 Gray 표현에 그대로 옮기면 `100`을 기다리게 됩니다. Gray `100`은 binary 7이므로 네 칸에 일곱 건을 넣으려 합니다.

```verilog
wire [2:0] bad_target = {~rq2[2], rq2[1:0]}; // 잘못된 비교: ~는 한 비트 반전이며 아래 두 비트는 그대로입니다.
wire [2:0] full_target = {~rq2[2:1], rq2[0]}; // 올바른 비교: [2:1] 두 비트를 반전하고 {}로 이어 붙입니다.
wire [2:0] wn = wbin + {2'b00, wfire};       // 3비트 다음 포인터이며 수락한 쓰기에만 1을 더합니다.
wire [2:0] wg = (wn >> 1) ^ wn;             // 다음 binary 값을 Gray로 변환합니다.
```

입력은 45/55/65/75ns에 1003/1004/1005/1006을 수락하도록 구성했습니다. 정상은 85ns의 다섯 번째 요청을 거절합니다. 변이는 85ns에 점유량 4인 큐에 다시 쓰고, 처음 값 1003이 있던 주소를 1007로 덮습니다. 147ns의 첫 읽기에서 기대값 1003과 실제 1007이 다릅니다. 이 오류는 의도적으로 삽입했으며 새로 발견한 상용 칩 결함이 아닙니다.

## flag가 늦게 내려가도 오류는 아닙니다

write는 상대 read Gray의 동기화본으로 full을, read는 상대 write Gray의 동기화본으로 empty를 판단합니다. 상대 도메인이 진행해도 전달에 시간이 걸리므로 실제 빈자리나 자료가 있어도 잠시 대기할 수 있습니다. [AMD UG1353의 XPM_FIFO_ASYNC 설명](https://docs.amd.com/r/2025.2-English/ug1353-versal-architecture-ai-libraries/XPM_FIFO_ASYNC)도 상대 연산에 따른 flag 지연이 설정과 모드에 따라 다름을 설명합니다. 아래 수치는 자체 DUT에서 관측한 값이며 해당 IP의 지연 표를 재현한 값이 아닙니다.

| read 상승 edge | 동기화 1단 | 2단 | edge 직전 empty |
| --- | --- | --- | --- |
| 63ns | 0 | 0 | 1 |
| 77ns | 3 | 0 | 1 |
| 91ns | 6 | 3 | 1 |
| 105ns | 6 | 6 | 0 |

표는 NBA, 즉 nonblocking assignment의 지연 갱신 전 값입니다. 예를 들어 77ns의 `sync2 <= sync1`은 그 edge 직전 1단의 3을 받아 edge 뒤 2단을 바꿉니다. 등록된 empty는 다음 edge에서 그 전달본을 사용합니다. 첫 쓰기 45ns 이후에도 read 쪽 empty가 즉시 내려가지 않는 것이 정상입니다.

따라서 기준 모델은 `empty == (전역 큐 길이 == 0)`을 모든 순간 강제하지 않습니다. 실제 수락한 쓰기를 `deque` 뒤에 넣고 수락한 읽기를 앞에서 꺼내 순서를 비교합니다. `deque`는 양 끝 삽입·제거가 가능한 Python 표준 자료구조입니다. 같은 시각의 read와 write는 기존 자료의 read를 먼저 비교하며 새 write의 즉시 bypass는 허용하지 않습니다. 큐가 빈데 읽거나 길이 4인 큐에 쓰는 것은 별도로 실패시킵니다. 포인터 수식과 메모리 배열을 기준 모델에 복제하지 않습니다.

```python
queue.append(row["data"])       # []는 사전의 키 조회이며 append는 수락 자료를 큐 뒤에 넣습니다.
wanted = queue.popleft()         # 가장 오래된 자료를 앞에서 꺼내 읽기 기대값으로 삼습니다.
if row["data"] != wanted:       # if는 조건 분기, !=는 서로 다름을 검사하는 비교입니다.
    fail(row, "data_order")     # fail 함수를 호출해 관측 시각과 오류 이유를 저장합니다.
```

동시에 수락 gate, 수락에 따른 포인터 전진, Gray 인접 변화, 도메인별 2단 전달의 이전/현재 관계도 검사합니다. 초기 네 값과 첫 읽기 시각은 코드에 별도 리터럴로 남겼습니다. 아무 거래도 수락하지 않는 잘못된 회로가 빈 큐만 유지하며 통과하지 못하도록 활동·wrap·대기 조건도 확인합니다.

## 한쪽의 reset 요청도 양쪽 자료를 함께 비웁니다

정상 계약은 common reset 또는 write reset 요청 중 하나라도 들어오면 양쪽 포인터·동기화기·flags를 함께 초기화하는 방식입니다. 한쪽만 reset하고 반대쪽의 이전 바퀴·세대 자료를 계속 읽는 복구는 지원하지 않습니다. 메모리 비트는 그대로 두어도 포인터와 empty가 이전 값을 유효 자료로 읽지 못하게 합니다.

reset은 1~22ns, 1002~1032ns의 common 요청과 1502~1532ns의 write 요청으로 시험했습니다. assert/deassert를 클록 상승 edge에 맞추지 않았습니다. 두 도메인 모두 비동기로 assert하고 각자의 두 레지스터를 통해 release합니다. 22ns에 요청을 내리면 write는 25/35ns, read는 35/49ns의 두 edge에서 release를 진행합니다. release 신호는 각각 두 번째 edge 뒤에 내려가고, core는 45/63ns부터 연산합니다. 이 관측 전·후 구분을 reset 비교기에도 반영했습니다.

1002ns reset은 대기 자료 1095~1098 네 건을, 1502ns 요청은 1144·1147 두 건을 취소합니다. 정상에서는 총 쓰기 64 = 읽기 58 + reset 취소 6이 됩니다. read 도메인에 write reset을 전달하지 않는 변이는 1505ns에 reset 요청 중 읽기를 수락하고 이전 자료를 새 세대 큐와 섞습니다. empty를 무시하는 별도 변이에서는 217ns부터 gate 위반을 검출하고, 847ns에는 실제 거래 큐가 빈 상태의 읽기도 검출합니다.

## 실행 결과와 검증 경계

[실행 명령과 결과 형식](../예제_examples/실무검증_practical-validation/cdc_async_fifo/README.md)을 따르면 실제 compile→sim→trace 비교가 순서대로 실행됩니다. 네 설정의 컴파일·실행은 모두 정상 종료했으며, 기능 판정은 설정에 따라 다릅니다.

| 설정 | 비교 결과 | 불일치 수 | 첫 대표 오류 |
| --- | --- | --- | --- |
| 정상 | PASS | 0 | 377행에서 자료·reset·포인터 계약이 일치합니다. |
| full 상위 한 비트만 반전 | FUNCTIONAL_FAIL | 160 | 85ns에 깊이 4를 넘는 쓰기입니다. |
| empty 읽기 허용 | FUNCTIONAL_FAIL | 66 | 217ns에 empty gate를 위반합니다. |
| 한쪽만 reset | FUNCTIONAL_FAIL | 27 | 1505ns에 read reset 누락과 읽기 수락입니다. |

불일치 수는 이번 입력과 검사 규칙에서 나온 오류 기록 수입니다. 하나의 원인에서 여러 후속 오류가 생기므로 오류 발생률이나 실리콘 고장률로 바꿀 수 없습니다. 정상에서는 양쪽 포인터가 각각 7번 wrap했고, full/empty 때문에 쓰기 58건·읽기 52건을 차단했습니다. 입력 해시와 네 trace 해시는 소스를 바꾸지 않은 두 실행에서 같았습니다.

trace 누락·중복·열 오류, 알 수 없는 control/pointer는 기능 결과를 판정할 자료가 없으므로 `INFRA_ERROR`입니다. 수락된 읽기 자료의 X/Z는 기능상 유효 자료를 만들지 못했으므로 `FUNCTIONAL_FAIL`입니다. 별도 8개 오류 trace 대조와 도구 누락·출력 폴더 재사용 거절도 확인했습니다. [실행별 기록과 SHA256](검증기록_evidence/비동기FIFO비교검증_20261021.md)에서 범위를 확인할 수 있습니다.

2단 동기화기를 디지털 RTL에서 실행했다는 사실로 metastability의 발생 확률이나 MTBF, 평균 고장 간격을 구할 수는 없습니다. Gray 코드도 배선 지연이 제약 없이 달라도 된다는 뜻은 아닙니다. [Altera F-Tile 공식 문서의 Gray pointer 경로 설명](https://docs.altera.com/r/docs/720985/23.3/f-tile-low-latency-ethernet-10g-mac-ip-user-guide/dual-clock-fifo?contentId=VIE5jksRM0BqEJvK0yUsew)은 skew와 net delay를 별도로 다룹니다. 실제 구현에는 대상 소자의 메모리 추론, 배치·배선 제약, CDC 정적 분석과 reset 경로 확인이 추가로 필요합니다. 이 예제는 그 절차를 실행한 결과가 아닙니다.

## 확인 문제

1. 깊이 4인데 왜 포인터는 3비트인가요? 주소 2비트만으로는 같은 위치의 빈 상태와 한 바퀴 뒤의 full을 구별하지 못하기 때문입니다. 하위 2비트는 주소, 추가 비트는 바퀴 구분에 사용합니다.
2. 큐에 자료가 있는데 read empty가 1이면 실패인가요? 원격 포인터의 동기화와 flag 등록이 끝나기 전의 보수적 대기는 허용합니다. 실제 빈 큐에서 자료를 꺼내는 수락은 허용하지 않습니다.
3. 한 도메인만 reset해도 포인터가 모두 0이면 충분한가요? 반대 도메인의 포인터·동기화기·대기 자료가 이전 세대에 남을 수 있습니다. 이 사례는 요청을 양쪽 flush로 확장하며 독립적인 한쪽 복구는 지원하지 않습니다.

## English

The actual Icarus run compares a depth-four asynchronous FIFO against an independent Python transaction queue. Binary pointers address memory; registered three-bit Gray pointers cross through two destination-clock stages. The full comparison inverts the top two synchronized Gray bits. Inverting only the top bit permits an overwrite at 85ns, and the first read at 147ns returns 1007 instead of 1003.

Flags are local and conservative. The checker allows delayed deassertion rather than requiring equality with instantaneous global occupancy. It checks accepted transfers, ordering, capacity, pointer movement and synchronizer stage relationships. Read-before-write processing at coincident edges matches the testbench's pre-NBA observation and excludes immediate bypass.

Any reset request flushes both domains. Assertion is asynchronous; each domain releases through two local edges and resumes core operations on the next edge. The correct run accepts 64 writes, consumes 58 and cancels six queued values. Three controlled faults produce 160, 66 and 27 mismatch records. All four compiler and simulator processes exit successfully, so process success alone does not establish functional success.

The tests use fixed 10/14ns clocks and do not establish metastability behavior, MTBF, physical timing closure, CDC signoff or measured hardware reliability. The sources describe the design rationale; input values and reported results come from this repository's educational DUT.

## 출처

- Clifford E. Cummings, Simulation and Synthesis Techniques for Asynchronous FIFO Design, SNUG San Jose 2002, Rev 1.2, June 2005, §2.2·4·5·6·12.2. 저자의 기존 배포 주소가 현재 redirect되어 [원 논문 보관본](https://github.com/zhangzek/Clock-Domain-Crossing-Design/blob/master/doc%26paper/CummingsSNUG2002SJ_FIFO1.pdf)을 내려받아 해당 구간을 읽었습니다.
- [AMD UG1353 2025.2, XPM_CDC_GRAY](https://docs.amd.com/r/2025.2-English/ug1353-versal-architecture-ai-libraries/XPM_CDC_GRAY): Gray 표현·목적 클록 동기화의 전제입니다. 개별 카운트의 lossless 전달 조건을 FIFO의 모든 중간 포인터 관측 조건으로 적용하지 않습니다.
- [AMD UG1353 2025.2, XPM_FIFO_ASYNC](https://docs.amd.com/r/2025.2-English/ug1353-versal-architecture-ai-libraries/XPM_FIFO_ASYNC): 수락 gate·상대 도메인 연산과 flag 지연을 대조했습니다. 자체 DUT는 이 vendor IP를 인스턴스화하지 않습니다.
- [Altera F-Tile Low Latency Ethernet 10G MAC IP User Guide 23.3, §3.6.1.1.3](https://docs.altera.com/r/docs/720985/23.3/f-tile-low-latency-ethernet-10g-mac-ip-user-guide/dual-clock-fifo?contentId=VIE5jksRM0BqEJvK0yUsew): Gray pointer 경로의 skew·net delay 제약입니다. 특정 IP의 수치 제약과 자체 예제의 클록 조건을 구분했습니다. 출처 확인일은 2026-10-21입니다.

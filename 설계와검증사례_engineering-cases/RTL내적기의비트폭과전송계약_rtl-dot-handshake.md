# RTL 내적기의 비트 폭과 전송 계약 / RTL dot products, widths and handshakes

정수 계산식이 맞아도 RTL의 부호·저장 폭·전송 시점이 다르면 다른 회로가 됩니다. 이 사례는 SystemVerilog 내적기를 실제로 컴파일하고 시뮬레이션한 뒤, Python의 독립 기준 모델과 각 상승 에지의 관측을 비교합니다. 정상 RTL과 다섯 결함 설정을 같은 입력으로 실행합니다.

코드는 [DUT](../예제_examples/실무검증_practical-validation/rtl_reference/dot4.sv), [테스트벤치](../예제_examples/실무검증_practical-validation/rtl_reference/tb_dot4.sv), [기준 모델·비교 러너](../예제_examples/실무검증_practical-validation/rtl_reference/run_compare.py)에 있습니다. DUT는 시험 대상 회로입니다. 아래 수치는 2026-10-21 Icarus Verilog·VVP 실행에서 얻었으며 FPGA 보드·실리콘 측정이 아닙니다.

## 비교할 계약을 먼저 고정합니다

입력은 부호 있는 8비트 정수 네 개씩의 두 벡터입니다. 같은 위치끼리 곱한 네 항을 더하고 signed 32비트 결과와 16비트 tag를 출력합니다. tag는 같은 거래의 결과를 연결하는 ID입니다. 양자화·포화·bias는 없습니다.

한 번에 한 거래만 처리합니다. reset이 아니고 `in_valid && in_ready`인 상승 에지 n에서만 입력을 수락합니다. 출력은 n+2 에지부터 전송할 수 있고, `out_valid && out_ready`인 에지에서 소비합니다. 준비되지 않은 출력은 valid·tag·값을 유지합니다. 출력 소비와 새 입력 수락을 같은 에지에 하는 처리량 최적화는 이 설계에 넣지 않았습니다.

reset은 상태를 상승 에지에서 비우며, rst=1 동안 ready·valid를 0으로 마스킹합니다. 소비하지 않은 이전 거래는 취소합니다. 이는 이 예제의 자체 계약입니다. Arm의 [AXI-Stream §2.2](https://documentation-service.arm.com/static/64819f1516f0f201aa6b963c)는 valid·ready의 동시 수락과 대기 중 정보 유지 원리를 설명하지만, 이 모듈을 전체 AXI-Stream 규격에 적합한 IP로 검증한 것은 아닙니다.

## Python의 큰 정수와 RTL의 비트 폭을 분리합니다

첫 손계산 입력은 다음과 같습니다.

```text
x = [20, -3, 5, 6], w = [7, -2, 3, 4]
20×7 + (-3)×(-2) + 5×3 + 6×4 = 185
```

-3의 8비트 표현은 unsigned로 읽으면 253입니다. 결함 설정 1은 피연산자를 unsigned로 곱하고 0을 붙여 확장합니다. 첫 결과는 `140 + 253×254 + 15 + 24 = 64,441`입니다. 같은 비트가 들어왔어도 숫자로 읽는 방법이 달라진 것입니다.

정상 경로는 8비트 signed 변수 두 개의 곱을 16비트 signed product에 넣고, 부호 비트를 복제하여 32비트로 확장한 다음 더합니다. 연결 표현 자체의 signed 여부에 기대기보다 확장할 비트를 명시했습니다.

```verilog
reg signed [7:0] sx, sw; // signed는 최상위 비트를 부호로 해석하는 선언입니다.
reg signed [15:0] product; // 8비트 두 값의 곱을 담습니다.
reg signed [31:0] accumulator; // 네 곱의 합을 넓게 유지합니다.
product = sx * sw; // *는 곱셈이며 이 변수에 16비트 곱을 저장합니다.
accumulator = accumulator + {{16{product[15]}}, product}; // {}로 부호 비트를 반복·연결합니다.
```

네 항의 양의 극값은 `4×(-128)×(-128)=65,536`입니다. 16비트 signed 최대값 32,767뿐 아니라 17비트 최대값 65,535도 넘으므로 이 원시 합에는 최소 18비트가 필요합니다. 여기서는 32비트를 택했습니다. 결함 설정 2는 합을 16비트로 잘라 65,536을 0으로, -65,024를 512로 만듭니다.

[AMD UG901의 변환 함수 설명](https://docs.amd.com/r/2023.1-English/ug901-vivado-synthesis/Using-Conversion-Functions)에서 `$signed`·`$unsigned`의 결과 폭은 입력 폭과 같다고 확인했습니다. 잘라 버린 16비트에 `$signed`만 붙여 원래 합을 되살릴 수는 없습니다. 정상 경로는 좁히기 전에 필요한 폭을 보존합니다.

## 값을 비교하기 전에 어떤 거래인지 확인합니다

첫 tag 1은 에지 3에서 수락됩니다. 다음 tag 2는 에지 4부터 valid를 유지하지만 회로가 바쁘므로 곧바로 수락되지 않습니다. 실제 정상 trace의 일부는 다음과 같습니다. 표의 신호는 해당 상승 에지의 순차논리 갱신 전 값입니다.

| 에지 | 입력 valid/ready | 출력 valid/ready | 출력 tag·값 | 의미 |
|---|---|---|---|---|
| 3 | 1/1 | 0/1 | 의미 없음 | tag 1을 수락합니다. |
| 4 | 1/0 | 0/0 | 의미 없음 | tag 2를 입력 쪽에서 유지합니다. |
| 5 | 1/0 | 1/0 | 1 · 185 | 결과는 준비됐지만 소비되지 않습니다. |
| 6 | 1/0 | 1/0 | 1 · 185 | 같은 결과를 유지합니다. |
| 7 | 1/0 | 1/1 | 1 · 185 | tag 1의 출력이 소비됩니다. |
| 8 | 1/1 | 0/1 | 의미 없음 | tag 2를 수락합니다. |
| 10 | 0/0 | 1/1 | 2 · 65,536 | tag 2의 출력이 소비됩니다. |

결함 설정 3은 HOLD 상태에서 `in_valid`만 보고 새 값을 결과 레지스터에 씁니다. ready가 0이므로 tag 2를 아직 받지 않았는데도 에지 6의 출력이 tag 2·65,536으로 바뀝니다. 숫자 자체는 올바른 내적일 수 있지만 tag 1의 대기 중 결과를 잃었습니다. 수정 경로는 입력을 수락한 에지에서만 내부 pending 값과 tag를 저장하고, HOLD에서는 새 입력을 읽지 않습니다.

출력 valid가 여러 에지에서 1이라고 같은 결과를 여러 번 소비한 것으로 세지도 않습니다. 다만 소비되지 않은 동안 값이 바뀌는지 확인하기 위해 비교는 매 valid 에지에서 수행합니다. 출력 거래 수는 valid·ready가 함께인 에지에서만 셉니다.

## 관측 시점을 섞으면 한 사이클 오류를 놓칩니다

테스트벤치는 하강 에지에서 입력을 구동하고 다음 상승 에지의 active 영역에서 CSV를 기록합니다. DUT의 레지스터는 nonblocking 대입 `<=`로 그 에지 뒤에 갱신됩니다. 따라서 CSV는 전송을 결정한 에지의 이전 상태를 읽습니다. HDL 코드에 `#1`을 더해 갱신 뒤를 읽는 방식으로 바꾸려면 기대 모델의 시점도 바꿔야 합니다.

정상 회로는 입력 수락 n 다음의 n+1 에지 뒤에 출력 레지스터와 HOLD 상태를 갱신합니다. 다음 전송 에지 n+2에서 그 결과를 읽을 수 있습니다. 결함 설정 4는 수락 에지에서 곧바로 HOLD로 바꾸어 n+1부터 전송될 수 있게 합니다. 실제 첫 차이는 에지 4의 `out_valid`: 기대 0, 실제 1입니다. 값과 tag만 순서대로 대조하면 이 latency 계약 위반을 놓칠 수 있습니다.

## reset 뒤의 이전 결과는 취소된 거래입니다

tag 4를 에지 16에서 받고, 출력이 대기하는 에지 18에 reset을 넣습니다. 정상 회로는 에지 19에 `in_ready=1`, `out_valid=0`입니다. 결함 설정 5는 HOLD 상태를 reset에서 남겨 에지 19에도 `out_valid=1`을 보입니다. 과거 계산값이 맞더라도 취소된 거래가 다시 나타나는 실패입니다.

정상 입력에는 37건의 수락이 있으며 reset으로 4건을 취소하고 33건을 출력 소비했습니다. `37=33+4`라는 대응을 유지합니다. reset 정책을 모르고 입력·출력 개수만 같아야 한다고 검사하면 이 설계의 정상 동작을 실패로 오판합니다. 반대로 reset을 이유로 임의의 누락을 없애지 않도록 취소한 tag를 따로 기록합니다.

## 기준 모델은 RTL 상태기를 복사하지 않습니다

Python은 수락한 거래 하나의 정수 내적, tag, 가장 이른 출력 전송 에지 `n+2`만 보관합니다. RTL의 IDLE·BUSY·HOLD 레지스터 전이를 다시 구현하지 않습니다. 기대 ready도 실제 DUT의 ready에 따라 바꾸지 않고 단일 거래 계약에서 계산하므로, DUT가 잘못된 ready를 내더라도 기대 거래까지 함께 바뀌지 않습니다.

고정 입력·극값·대기·reset을 먼저 배치하고, seed 20261021의 signed int8 벡터 32개를 추가하여 총 288에지를 구동합니다. 기준 모델은 입력 생산자도 ready 전까지 valid·값·tag를 유지했는지 확인합니다. 전체 trace의 행 수와 순서를 먼저 맞춘 뒤 각 에지의 기대 신호를 비교합니다. 짧은 trace를 `zip()`으로 잘라 통과시키지 않습니다.

이 parser는 모든 CSV 필드가 정수인 trace만 지원합니다. X/Z, 열 초과·부족, 행 누락, 결과 파일 없음은 수치 비교를 진행하지 않는 `INFRA_ERROR`입니다. 유효 출력의 X/Z를 특정 기능 FAIL로 분류하는 별도 규칙은 구현하지 않았습니다. 정상 RTL이 X/Z 없이 정수 trace를 낸다는 조건까지 포함한 비교이며, 임의의 HDL에 그대로 적용할 수 있는 4-state checker는 아닙니다.

## 실제 실행 결과

2026-10-21 Windows AMD64·CPython 3.12.14·Icarus Verilog/VVP 12.0 devel로 최종 소스를 두 번 실행했습니다. 각 실행에서 6개 설정의 compile·simulation 종료 코드는 모두 0이었고 아래 결과가 같았습니다.

| 설정 | 신호·에지 불일치 항목 | 판정 | 첫 차이 |
|---|---:|---|---|
| 정상 | 0 | PASS | 없습니다. |
| unsigned 곱 | 95 | FAIL | 에지 5, 185 → 64,441 |
| 16비트 축소 | 2 | FAIL | 에지 10, 65,536 → 0 |
| ready 무시 | 4 | FAIL | 에지 6, tag 1 → 2 |
| 한 에지 빠른 valid | 223 | FAIL | 에지 4, valid 0 → 1 |
| reset 미취소 | 8 | FAIL | 에지 19, ready 1 → 0·valid 0 → 1 |

불일치 수는 같은 잘못된 값의 여러 에지 관측을 포함합니다. 95개 독립 결함이나 결함 검출 확률 95%를 뜻하지 않습니다. 전체 러너의 PASS는 정상은 통과하고 의도한 다섯 결함은 검출됐다는 뜻입니다. 시뮬레이터가 종료 0이었다는 사실만으로 DUT를 통과시키지 않았습니다.

## 재현과 남기는 자료

[실행 안내](../예제_examples/실무검증_practical-validation/rtl_reference/README.md)에 따라 저장소 루트에서 실행합니다. Python 외에 실제 Icarus·VVP가 필요합니다.

```shell
python -B 예제_examples/실무검증_practical-validation/rtl_reference/run_compare.py --out /new/path/rtl-run
```

러너는 새 결과 폴더와 새 build 폴더, 설정별 TEMP/TMP를 사용하고 compile을 순차 실행합니다. 이번 build 경로는 ASCII였으며 상대 파일명으로 소스를 넘겼습니다. 과거의 다른 RTL에서 간헐 컴파일 실패가 있었지만, 이번 성공만으로 과거 원인을 확정하거나 해결했다고 쓰지 않습니다. 최소 회로는 한글 작업 경로와 ASCII 경로에서 모두 성공했습니다. 이전 실패 기록은 그대로 남깁니다.

도구가 없거나 compile·simulation이 실패하면 `INFRA_ERROR`와 종료 2로 차단합니다. 도구 없는 조건을 실제로 대조했고 false PASS가 없었습니다. [검증 기록](검증기록_evidence/RTL내적기비교검증_20261021.md)은 버전·명령·로그·입력과 소스 hash·CSV·불일치를 연결합니다. 합성·equivalence·STA·CDC·layout·실물 주파수·전력은 이번에 실행하지 않았습니다. 테스트벤치의 10ns 주기는 구현 가능한 최대 클록의 측정값이 아닙니다.

## 확인 문제

1. 16비트로 잘라진 65,536에 `$signed`를 적용하면 원래 합이 돌아옵니까?
2. 출력 valid=1·ready=0인 두 에지에 같은 값이 보이면 두 건이 소비됐습니까?
3. 입력 37건·출력 33건이어도 이 예제에서 정상일 수 있습니까?

<details>
<summary>답과 이유</summary>

1. 아닙니다. 값의 상위 비트가 이미 사라졌습니다. 필요한 폭을 좁히기 전에 유지해야 합니다.
2. 아닙니다. 아직 소비되지 않은 같은 출력입니다. 대신 대기 중 tag·값의 유지 여부를 검사합니다.
3. 그렇습니다. 이 실행은 reset으로 4건을 취소했습니다. 취소한 ID까지 대응하여 확인합니다.

</details>

## English summary

Actual SystemVerilog is compiled and executed with Icarus/VVP, then compared with an independent Python transaction oracle over 288 sampled edges. The corrected design has no mismatches; unsigned arithmetic, narrowing, ready bypass, early valid and reset-flush mutations are detected. The contract allows one outstanding transaction and output transfer from acceptance edge plus two. This is functional RTL simulation, not synthesis, formal equivalence, STA or hardware measurement. Non-integer/X/Z traces are blocked as unsupported comparison input.

## 원자료와 읽은 범위

- [Icarus command-line flags](https://steveicarus.github.io/iverilog/usage/command_line_flags.html), [VVP flags](https://steveicarus.github.io/iverilog/usage/vvp_flags.html): `-g2012`, expression width, top·parameter 지정, compile과 runtime의 구분을 2026-10-21에 읽었습니다. 현행 웹 문서와 설치된 12.0 devel을 구분합니다.
- Arm IHI 0051B, ID040921(2021), [§2.2](https://documentation-service.arm.com/static/64819f1516f0f201aa6b963c): handshake와 대기 중 정보 유지 부분입니다. 전체 규격 적합성 검사는 하지 않았습니다.
- AMD UG901 2023.1, 2023-06-09, [Using Conversion Functions](https://docs.amd.com/r/2023.1-English/ug901-vivado-synthesis/Using-Conversion-Functions): signed/unsigned 변환의 폭·부호 설명입니다. Vivado를 실행한 결과가 아닙니다.

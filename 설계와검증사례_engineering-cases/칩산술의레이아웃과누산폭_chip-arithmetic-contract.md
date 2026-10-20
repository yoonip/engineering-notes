# 칩 산술의 레이아웃과 누산 폭 / Layout and accumulation contracts in a chip model

NPU 검증에서 값이 다르면 곱셈 회로만 의심하기 쉽습니다. 같은 바이트를 어느 좌표로 읽었는지, 장치가 최신 입력을 보았는지, 결과를 몇 비트에 저장했는지도 확인해야 합니다. 이 사례는 기존 `practical-silicon-lab`의 의도적인 오류 주입 모형을 재사용하여 세 원인을 분리합니다. 새로 발견한 실칩 결함이나 실제 캐시 고장의 보고가 아닙니다. 2026-10-21에 Python 소프트웨어 모형으로 실행했습니다.

## 먼저 비교할 계약을 고정합니다

계약은 입력과 출력이 따라야 할 약속입니다. 여기서는 입력 3×3, 가중치 2×2, 부호 있는 8비트 정수, 행 우선 저장, 이동 간격 1, 테두리 덧붙임 없음으로 정합니다. 연산은 가중치를 뒤집지 않는 cross-correlation입니다. 출력은 2×2이며 네 곱을 더한 원시 정수 합을 보존합니다. 누산과 출력의 계약은 signed int32입니다. 양자화 scale·zero-point·bias·활성화 함수는 포함하지 않습니다.

int8은 -128~127을 표현합니다. 입력이 int8이라고 곱의 합도 int8에 들어가는 것은 아닙니다. 이 4항 계산의 최대 절댓값은 `4×128×128=65,536` 이하라서 int32 범위에는 들어갑니다. 채널 수와 커널 크기가 커지면 항 수를 다시 계산해야 합니다. Python의 정수는 자동으로 폭을 늘리므로, Python이 맞았다는 사실만으로 C나 RTL의 비트 폭이 맞았다고 판단하지 않습니다.

실제 라이브러리의 계약도 따로 읽습니다. [Arm CMSIS-NN v4.1.0의 convolution API](https://arm-software.github.io/CMSIS-NN/v4.1.0/group__NNConv.html)는 입력·필터·출력의 차원 순서와 자료형을 명시합니다. 이 글의 단일 채널 HW 배열은 해당 라이브러리의 전체 NHWC 인터페이스와 같지 않습니다. CMSIS-NN의 최종 int8 출력에는 양자화 단계가 있으므로 원시 합 185와 바로 비교해서는 안 됩니다.

## 작은 입력으로 정답을 따로 계산합니다

다음은 직접 구성한 입력입니다. 기준값을 DUT 함수에서 복사하면 같은 주소 오류가 양쪽에 들어갈 수 있으므로 네 값을 손으로 계산해 실행기의 고정 기대값으로 넣었습니다.

```text
입력                    가중치
 20  -3   4               7  -2
  5   6  -7               3   4
  8   9  10

기대 출력
185  -39
 83  123
```

왼쪽 위는 `20×7 + (-3)×(-2) + 5×3 + 6×4 = 185`입니다. 오른쪽 위는 `(-3)×7 + 4×(-2) + 6×3 + (-7)×4 = -39`입니다. 부호가 섞이고 행·열이 대칭이 아닌 입력을 골라 단순 주소 교환이 결과에 드러나게 했습니다. 모든 원소가 1인 입력은 전치해도 같아서 layout 오류를 놓칩니다. 실행기는 그 맹점도 별도 비교로 남깁니다.

[기존 scalar 기준 구현](../프로젝트_projects/practical-silicon-lab/validation/npu.py)은 이차원 좌표로 합을 구하고, DUT 모형은 일차원 버퍼의 인덱스를 계산합니다. 새 [재현 실행기](../예제_examples/실무검증_practical-validation/chip/run_chip_cases.py)의 `arithmetic()`은 두 구현을 고정 기대값과 비교합니다. 서로 다른 구현 경로와 손계산은 오류 공유 가능성을 줄이지만, 모든 크기와 양자화 모형을 검증한 증거는 아닙니다.

## 주소·입력 가시성·폭을 한 번에 하나씩 바꿉니다

행 우선 배열에서 폭이 3이면 `(row, column)`의 주소는 `row*3+column`입니다. 기존 모형의 layout fault는 이를 `column*3+row`로 바꿉니다. 정상 주소식으로 돌아가는 것이 이 모형에서의 해결입니다. 실제 코드에서는 stride의 단위가 원소인지 바이트인지도 고정하고, 비정사각형·여러 채널 입력으로 같은 가정을 다시 시험해야 합니다.

```python
index = (y + ky) * 3 + (x + kx)  # 정상: 행 번호×행 폭+열 번호입니다.
index = (x + kx) * 3 + (y + ky)  # 오류 대조: 행과 열을 바꿉니다.
```

stale fault는 장치 쪽 복사 버퍼의 가운데 값만 6에서 5로 바꿉니다. 원본 입력 파일의 SHA-256은 그대로입니다. 출력 차이는 순서대로 -4, -3, +2, -7이며 가운데 원소에 곱해지는 가중치와 대응합니다. 따라서 host 파일의 hash가 같다는 조건과 장치가 같은 값을 읽었다는 조건을 분리할 수 있습니다. 이 무늬가 실제 DMA 캐시 문제의 원인을 유일하게 증명하지는 않습니다. 물리 장치에서는 주소·버퍼 세대·소유권·캐시 유지보수·완료 시점의 별도 증거가 필요합니다.

overflow fault는 마지막 합을 수학적으로 int8 wrap 처리합니다. `((185+128)%256)-128=-71`이므로 첫 출력만 바뀝니다. C의 signed overflow를 실제로 실행한 것이 아니라 정해진 변환식을 Python으로 모델링했습니다. 수정한 경로는 int32 합을 그대로 돌려주며, 좁히기가 필요하면 별도의 출력 계약을 먼저 정합니다.

| 실행한 모형 | 실제 출력 | DUT 판정 |
|---|---|---|
| none | `[[185,-39],[83,123]]` | PASS |
| layout | `[[145,73],[-49,43]]` | FAIL |
| stale | `[[181,-42],[85,116]]` | FAIL |
| overflow | `[[-71,-39],[83,123]]` | FAIL |

실패 세 건은 실행기가 의도한 오류를 검출한 결과입니다. 오류를 없애려고 기대값을 잘못된 출력에 맞추지 않습니다. 원래의 주소식·동일 입력·충분한 누산 폭으로 돌아온 `none` 경로가 원래 기대값과 일치하는지 확인합니다.

## Wrap과 포화는 서로 다른 답을 만듭니다

Wrap은 표현 범위를 벗어난 값을 모듈러 연산으로 돌아오게 합니다. Saturation, 즉 포화는 범위의 끝값에 고정합니다. 128은 wrap8에서 -128, saturate8에서 127입니다. -129는 각각 127과 -128입니다. 따라서 ‘int8로 변환한다’만으로는 시험의 기대값이 완성되지 않습니다.

```python
wrapped = (value + 128) % 256 - 128  # %는 나머지이며, 부호 있는 8비트 순환을 정합니다.
clipped = max(-128, min(127, value))  # min·max로 표현 구간의 양 끝에 제한합니다.
```

실행기는 `[127,128,-128,-129,65536]`에 대해 int32 보존, wrap8, saturate8을 따로 비교합니다. -128 입력끼리의 4항 합 65,536과 -128·127의 4항 합 -65,024도 정상 경로로 확인합니다. 범위를 벗어난 입력 128, 실수 1.0, 참·거짓 값, 행 길이가 다른 배열은 계산 전에 거부합니다. Python에서 `bool`은 `int`의 하위 형식이므로 `type(value) is int`로 이 예제의 순수 정수 계약을 검사합니다.

실제 C/C++ 구현에서는 곱셈 전에 피연산자 형식을 확인하고 충분한 폭의 누산기에 더합니다. unsigned 혼합, narrowing, SIMD의 포화 여부도 시험 항목입니다. 여기서는 C 컴파일이나 명령어별 동작을 실행하지 않았으므로 Python 결과를 특정 컴파일러·NPU의 bit-exact 인증으로 쓰지 않습니다.

## 실행과 기록

저장소 루트에서 다음 명령을 실행합니다. `--out`에는 아직 없는 폴더를 지정합니다. 장비 드라이버나 외부 패키지는 필요하지 않습니다.

```shell
python -B 예제_examples/실무검증_practical-validation/chip/run_chip_cases.py --out /new/path/chip-run
```

`arithmetic/input.json`에 계약과 입력, `arithmetic/report.json`에 정상·오류 출력과 좌표별 차이가 저장됩니다. `summary.json`에는 환경, 입력 hash, 기존 모듈의 실행 전후 hash와 44개 비교·거부 확인이 기록됩니다. 44개는 이 실행기 전체의 소프트웨어 확인 개수이며 칩 44개나 44종 고장 coverage가 아닙니다. 전체 실행이 PASS여도 표의 잘못된 DUT는 FAIL로 유지됩니다.

2026-10-21의 관측은 Python 3.12.14, Windows AMD64에서 44개 확인 PASS, 예상 밖 오류 0건입니다. 기존 offline 테스트 19개도 따로 통과했습니다. 실행 폴더 재사용은 종료 코드 2로 거부하고 이전 파일의 hash가 유지되는지 확인했습니다. 환경과 보존 범위는 [실행 기록](검증기록_evidence/칩모델과시험자료검증_20261021.md)에 적었습니다.

## 확인 문제

1. 입력이 int8이면 출력 185는 반드시 오류입니까?
2. host 입력 hash가 같고 stale 모형이 실패하면 실제 캐시 고장까지 증명합니까?
3. 전치 fault가 모든 원소 1인 입력에서 통과하면 정상 구현입니까?

<details>
<summary>답과 이유</summary>

1. 아닙니다. 여기서는 int32 원시 합 출력이 계약입니다. 최종 int8 출력이면 scale·반올림·포화 등 다른 계약이 필요합니다.
2. 아닙니다. 이 모형은 장치 복사본이 다를 수 있다는 반례입니다. 실제 캐시·DMA의 원인 분리는 별도 관측이 필요합니다.
3. 아닙니다. 입력이 대칭이라 오류를 드러내지 못했습니다. 비대칭 입력과 다른 크기·채널의 시험이 필요합니다.

</details>

## English summary

The replay imports an existing educational DUT model unchanged and checks it against a fixed scalar oracle. It distinguishes row-major indexing, stale device-side input and explicit mathematical int8 wrapping. Wide accumulation and narrowing are different contracts. The run is an offline software experiment, with no measured chip, RTL execution or CMSIS-NN execution.

## 원자료와 읽은 범위

2026-10-21에 [CMSIS-NN v4.1.0 API](https://arm-software.github.io/CMSIS-NN/v4.1.0/group__NNConv.html)의 `arm_convolve_s8` 차원·자료형 설명과 [같은 태그의 원문](https://github.com/ARM-software/CMSIS-NN/blob/v4.1.0/Source/ConvolutionFunctions/arm_convolve_s8.c)의 입력 주소식, 누산·재양자화·활성화 제한 부분을 읽었습니다. 해당 코드를 복제하거나 실행하지 않았습니다. 본문의 입력·손계산·오류 대조는 이 저장소의 교육용 예제이며 Arm의 측정 결과가 아닙니다.

[함께 읽기: DMA 버퍼와 캐시](../현장계측과검증_measurement-validation/펌웨어와디버깅_firmware-debugging/DMA버퍼와캐시의경계_cortex-m7-cache-dma.md)

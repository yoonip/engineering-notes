# Tiny Transformer RTL

작은 decoder-only Transformer의 학습 가중치를 Q8.8로 변환하고, SystemVerilog에서 token을 순차 생성하는 프로젝트다. NumPy로 학습·역전파·Adam을 구현했으며, RTL에서 embedding, LayerNorm, causal self-attention, FFN, vocabulary projection을 계산한다.

질문 종류와 강수 범주를 입력으로 받아 네 가지 짧은 답변을 생성한다. 문장 입력을 분류하는 규칙과 외부 예보 조회는 PowerShell에서 처리하고, 신경망 추론은 RTL에서 수행한다.

| 항목 | 구성 |
| --- | --- |
| Decoder block / attention head | 1 / 1 |
| Model dimension / FFN dimension | 8 / 16 |
| Vocabulary / context length | 13 / 8 |
| 가중치 | signed Q8.8, scale 256 |
| 학습 데이터 | 질문 2종 × 강수 범주 2종, 총 4개 sequence |
| 학습 설정 | seed 1234, Adam, 2,500 epoch |
| 생성 방식 | argmax, 생성 token을 context에 추가, EOS 종료 |

## 입력과 출력

| 질문 ID | 강수 범주 ID | 생성 문장 | 출력 token ID |
| --- | --- | --- | --- |
| 2: 비 | 4: 높음 | 비가 올 가능성이 높습니다. | 6 7 8 9 |
| 2: 비 | 5: 낮음 | 비가 올 가능성이 낮습니다. | 6 7 8 10 |
| 3: 맑음 | 4: 높음 | 맑을 가능성이 낮습니다. | 12 8 10 |
| 3: 맑음 | 5: 낮음 | 맑을 가능성이 높습니다. | 12 8 9 |

입력 prefix는 `[BOS, 질문 ID, 강수 범주 ID]`다. 맑음 질문의 답은 강수 범주를 반대로 대응시킨 예시다. 자연어 입력은 `비`, `강수`, `맑`, `rain`, `clear` 등의 키워드로 분류하며, 모델의 vocabulary는 위 네 문장을 표현하는 token으로 구성했다.

## RTL 구조

```text
token + position embedding
  → LayerNorm → Q/K/V projection
  → causal attention → output projection + residual
  → LayerNorm → FFN(ReLU) + residual
  → LayerNorm → vocabulary projection → argmax
  → 생성 token을 context에 추가 → EOS까지 반복
```

Softmax는 최대 점수를 뺀 뒤 exp lookup table과 정수 나눗셈으로 계산한다. LayerNorm에는 정수 제곱근을 사용한다. RTL에 가중치 ROM이 들어 있어 시뮬레이션에는 Python이나 외부 weight 파일이 필요 없다.

## 실행

Icarus Verilog와 `vvp`가 필요하다. OSS CAD Suite를 사용하는 경우 해당 배포판의 `environment.ps1` 또는 `environment.bat`로 환경을 먼저 연다.

Windows PowerShell에서 네 입력 조합을 인터넷 없이 검사한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1
```

컴파일러 경로를 직접 지정할 수도 있다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Iverilog "C:\iverilog\bin\iverilog.exe"
```

터미널에서 직접 실행하는 명령은 다음과 같다.

```sh
iverilog -g2012 -s tb_tiny_gpt -o tiny_gpt.vvp rtl/tiny_gpt.sv tb/tb_tiny_gpt.sv
vvp tiny_gpt.vvp

iverilog -g2012 -s tb_tiny_gpt -o query.vvp rtl/tiny_gpt.sv tb/tb_query.sv
vvp query.vvp +QUERY_ID=2 +FORECAST_ID=4
```

`tb_query.sv`의 `QUERY_ID`는 2 또는 3, `FORECAST_ID`는 4 또는 5를 사용한다. 두 testbench는 같은 top module 이름을 사용하므로 각각 컴파일한다.

## 예보 API 연결

`run.ps1`에 문장을 전달하면 Open-Meteo에서 도시 좌표와 일별 최대 강수확률을 조회한다. 기본 기준은 50%이며, 호스트가 이 값을 높음·낮음 token으로 바꿔 RTL에 전달한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run.ps1 -Prompt "오늘 비가 올까?" -City "서울"
```

API에서 받은 예보값을 조건으로 사용하는 경로다. 모델 학습 데이터에는 실제 기상 관측값이 들어 있지 않다. 예보 API 연결의 현재 검증 상태는 아래 표에 기록했다. API 변수와 이용 조건은 [Open-Meteo 예보 문서](https://open-meteo.com/en/docs)와 [지오코딩 문서](https://open-meteo.com/en/docs/geocoding-api)를 따른다.

## 학습 코드

`train_numpy.py`는 forward, cross-entropy, 역전파, Adam 갱신과 정수 참조 추론을 포함한다. 학습 후 `rtl/tiny_gpt.sv`와 `weights/trained_weights_q8.json`을 생성한다. 재학습에는 Python 3와 NumPy가 필요하다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\train.ps1
```

## 파일

| 경로 | 내용 |
| --- | --- |
| `rtl/tiny_gpt.sv` | 가중치 ROM을 포함한 추론 RTL |
| `rtl/tiny_gpt_template.sv` | weight exporter가 사용하는 RTL template |
| `tb/tb_tiny_gpt.sv` | 네 입력 조합, token sequence, causal mask, EOS 검사 |
| `tb/tb_query.sv` | plusargs로 선택한 한 입력 조합 검사 |
| `train_numpy.py` | NumPy 학습·정수 참조 추론·weight exporter |
| `run.ps1` / `run_demo.bat` | 시뮬레이션 실행기 |
| `train.ps1` | 학습 실행기 |
| `weights/trained_weights_q8.json` | RTL ROM과 같은 정수 가중치 |

## 검증 기록

2026-10-19에 저장된 최신 소스로 검증했다. 새 학습이나 외부 API 호출은 이 검사에 포함하지 않았다.

| 검사 | 결과 |
| --- | --- |
| Icarus: 기본 testbench의 네 조건 | PASS |
| Icarus: 단일 질의 testbench의 네 조건 | PASS |
| 출력 token, causal mask, softmax 합 허용오차, EOS | PASS |
| 저장된 Q8.8 가중치의 Python 참조 생성 | 네 조건 일치 |
| RTL ROM과 JSON 가중치 | 모든 정수 일치 |
| PowerShell 실행기 | 오프라인 검사 통과 |
| 실시간 예보 조회 | 이전 실행에서 HTTPS 오류 발생, 이번 검사에서 실행하지 않음 |
| FPGA 합성·배치배선·자원·타이밍 | 검증 범위에 포함하지 않음 |

## English

A small decoder-only Transformer exports trained weights to Q8.8 and generates tokens sequentially in SystemVerilog. The NumPy trainer implements the forward pass, backpropagation and Adam. RTL computes embeddings, LayerNorm, causal self-attention, FFN and vocabulary projection. PowerShell handles question classification and optional weather queries; neural inference runs in RTL.

### Model and inputs

The model has one decoder block/head, model width 8, FFN width 16, vocabulary 13 and context length 8. Weights are signed Q8.8 with scale 256. Training uses four sequences, seed 1234, Adam and 2,500 epochs. Generation uses argmax, appends each token to the context and stops at EOS.

| Question/category | Response meaning | Output token IDs |
| --- | --- | --- |
| Rain (2), high precipitation (4) | Rain is likely | 6 7 8 9 |
| Rain (2), low precipitation (5) | Rain is unlikely | 6 7 8 10 |
| Clear (3), high precipitation (4) | Clear skies are unlikely | 12 8 10 |
| Clear (3), low precipitation (5) | Clear skies are likely | 12 8 9 |

The prefix is `[BOS, question ID, precipitation-category ID]`. Clear-sky answers invert the precipitation category. Host keyword rules recognize Korean rain/clear terms plus `rain`/`clear`; the vocabulary encodes these four short Korean sentences.

### RTL and execution

The flow is token/position embedding → LayerNorm/QKV → causal attention/output projection/residual → LayerNorm/ReLU FFN/residual → final LayerNorm/vocabulary projection/argmax → context append until EOS. Softmax subtracts the maximum score, uses an exponential LUT and integer division. LayerNorm uses an integer square root. Weight ROMs are embedded, so simulation needs neither Python nor an external weight file.

Use Icarus Verilog and `vvp`. OSS CAD Suite users can initialize its `environment.ps1` or `environment.bat`. The listed PowerShell runner checks all four cases offline; `-Iverilog` supplies an explicit compiler path. The direct terminal commands compile each testbench separately because both use the same top-module name. Query IDs are 2/3 and forecast IDs are 4/5.

Supplying `-Prompt` and `-City` makes the host query Open-Meteo for coordinates and the daily maximum precipitation probability. The default 50% threshold becomes a high/low input token. The model has no measured-weather training data. See the [forecast](https://open-meteo.com/en/docs) and [geocoding](https://open-meteo.com/en/docs/geocoding-api) documentation for API fields/terms.

### Training and files

`train_numpy.py` includes forward/cross-entropy/backpropagation/Adam and integer reference inference. `train.ps1` runs training with Python 3/NumPy and exports `rtl/tiny_gpt.sv` plus `weights/trained_weights_q8.json`. `rtl/tiny_gpt_template.sv` is the exporter template. `tb/tb_tiny_gpt.sv` checks four cases, token sequences, masks and EOS; `tb/tb_query.sv` selects one case using plusargs. `run.ps1`/`run_demo.bat` launch simulation. The JSON weights match the RTL ROM values.

### Verification

On October 19, 2026, both Icarus testbenches passed all four conditions. Output tokens, causal masking, integer softmax-sum tolerance and EOS passed; the saved-weight Python reference matched all four cases, all RTL/JSON integers matched and the PowerShell runner passed offline. Training was not repeated. Live forecast queries had an HTTPS error in an earlier run and were not called during this check. FPGA synthesis, placement/routing, utilization and timing are outside the recorded verification.

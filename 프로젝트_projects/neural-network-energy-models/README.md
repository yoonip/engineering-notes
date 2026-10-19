# Neural Network Energy Models

Transformer의 파라미터 수, 연산량, weight read와 KV cache 접근량을 계산하는 분석 코드입니다. Batch와 context 길이에 따라 메모리·연산 에너지의 비중이 어떻게 달라지는지 비교합니다. 지정한 계수를 사용하는 수치 모델이며 전력계나 GPU에서 측정한 값은 사용하지 않습니다.

## 계산 범위

| 항목 | 모델 |
| --- | --- |
| 파라미터 수 | embedding·attention·FFN의 GPT 계열 근사식 |
| 전체 prefix 연산량 | context 길이를 포함한 dense forward |
| 한 token decode | KV를 재사용하며 새 Q/K/V와 출력 LM head 계산 |
| Weight 접근 | batch step마다 한 번 읽는 가정 |
| KV 접근 | 기존 항목 읽기와 새 K/V 항목 쓰기 |
| 정규화 비교 | ResNet18·Llama-7B의 공개된 반올림 성분으로 100개 조건 계산 |

Activation·norm·softmax·누설·IO 에너지는 decode 모델의 합계에서 제외합니다. `max_positions`는 position embedding 용량, `context`는 현재 사용 길이로 구분합니다. Llama의 GQA 등 개별 checkpoint의 구조를 복원하는 코드와는 계산 범위가 다릅니다.

## 실행

```sh
python -m pip install -r requirements.txt
python -m unittest -v
python model_demo.py --out results
```

`model_demo.py`는 입력 Excel 없이 실행하며, batch 1·4·8·16에서 두 크기의 모델을 비교하고 정규화 조건 100개를 CSV로 저장합니다.

| 파일 | 내용 |
| --- | --- |
| `energy_analysis.py` | 수식 평가기, 파라미터·FLOPs·decode 에너지 모델, 정규화 계산 |
| `test_energy_analysis.py` | 손계산, batch 재사용, KV 경계, 잘못된 차원·수식 검사 |
| `model_demo.py` | Excel 없이 실행하는 수치 비교 |

`energy_analysis.py`에는 특정 Excel 양식의 수식·캐시값을 비교하는 선택적 경로도 있습니다. 해당 자료는 저장소에 포함하지 않았으며, 직접 지정한 `--energy-xlsx`와 `--memory-xlsx`를 읽기 전용으로 처리합니다. FormulaEvaluator는 산술·셀 참조·SUM 범위만 해석하고 순환 참조와 실행 코드를 거부합니다.

정규화 비교는 [Electronics 2025, 14(13), 2718](https://doi.org/10.3390/electronics14132718)의 Table 2 성분을 사용합니다. 반올림된 표 수치의 계산을 비교하는 것이므로 실측 전력의 재측정과는 구분합니다.

2026-10-19에 단위 검사 8개와 Excel 없는 실행 경로를 확인했습니다. 원본 Excel과 개인 경로, 기존 결과·이미지는 이 폴더에 포함하지 않았습니다.

## English

These analytical tools estimate Transformer parameter counts, operations, weight reads and KV-cache traffic. They compare the memory/compute energy balance across batch sizes and context lengths using explicit coefficients rather than power-meter or GPU measurements.

### Model scope

| Component | Assumption |
| --- | --- |
| Parameters | GPT-style embedding, attention and FFN approximation |
| Full-prefix computation | Dense forward pass at the selected context length |
| Single-token decode | Reuse KV while computing new Q/K/V and the output LM head |
| Weight traffic | One weight read per batch step |
| KV traffic | Read existing entries and write new K/V entries |
| Normalized comparison | One hundred conditions using published rounded ResNet18/Llama-7B components |

Activation, normalization, softmax, leakage and I/O energy are excluded from decode totals. `max_positions` controls positional-embedding capacity; `context` is the currently used length. The approximation does not reconstruct checkpoint-specific structures such as Llama GQA.

### Execution and files

The commands above install dependencies, run tests and launch `model_demo.py`. This demo needs no Excel input: it compares two model sizes at batches 1, 4, 8 and 16 and writes 100 normalized conditions to CSV.

`energy_analysis.py` contains formula evaluation, parameter/FLOP/decode-energy models and normalization. `test_energy_analysis.py` checks hand calculations, batch reuse, KV boundaries and invalid dimensions/formulas. `model_demo.py` provides the spreadsheet-free path.

An optional read-only path accepts `--energy-xlsx` and `--memory-xlsx` to compare formula/cached values in a specific workbook layout. Those workbooks are not bundled. FormulaEvaluator accepts arithmetic, cell references and SUM ranges, rejecting cycles and executable code.

Normalized comparisons use rounded Table 2 components from [Electronics 2025, 14(13), 2718](https://doi.org/10.3390/electronics14132718); recalculation of rounded table values is distinct from measuring power again. The October 19, 2026 check covered eight unit tests and the spreadsheet-free path. Original workbooks, personal paths and earlier result images are not included.

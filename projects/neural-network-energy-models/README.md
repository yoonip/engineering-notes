# Neural Network Energy Models

Transformer의 파라미터 수, 연산량, weight read와 KV cache 접근량을 계산하는 분석 코드다. Batch와 context 길이에 따라 메모리·연산 에너지의 비중이 어떻게 달라지는지 비교한다. 지정한 계수를 사용하는 수치 모델이며 전력계나 GPU에서 측정한 값은 사용하지 않는다.

## 계산 범위

| 항목 | 모델 |
| --- | --- |
| 파라미터 수 | embedding·attention·FFN의 GPT 계열 근사식 |
| 전체 prefix 연산량 | context 길이를 포함한 dense forward |
| 한 token decode | KV를 재사용하며 새 Q/K/V와 출력 LM head 계산 |
| Weight 접근 | batch step마다 한 번 읽는 가정 |
| KV 접근 | 기존 항목 읽기와 새 K/V 항목 쓰기 |
| 정규화 비교 | ResNet18·Llama-7B의 공개된 반올림 성분으로 100개 조건 계산 |

Activation·norm·softmax·누설·IO 에너지는 decode 모델의 합계에서 제외한다. `max_positions`는 position embedding 용량, `context`는 현재 사용 길이로 구분한다. Llama의 GQA 등 개별 checkpoint의 구조를 복원하는 코드와는 계산 범위가 다르다.

## 실행

```sh
python -m pip install -r requirements.txt
python -m unittest -v
python model_demo.py --out results
```

`model_demo.py`는 입력 Excel 없이 실행하며, batch 1·4·8·16에서 두 크기의 모델을 비교하고 정규화 조건 100개를 CSV로 저장한다.

| 파일 | 내용 |
| --- | --- |
| `energy_analysis.py` | 수식 평가기, 파라미터·FLOPs·decode 에너지 모델, 정규화 계산 |
| `test_energy_analysis.py` | 손계산, batch 재사용, KV 경계, 잘못된 차원·수식 검사 |
| `model_demo.py` | Excel 없이 실행하는 수치 비교 |

`energy_analysis.py`에는 특정 Excel 양식의 수식·캐시값을 비교하는 선택적 경로도 있다. 해당 자료는 저장소에 포함하지 않았으며, 직접 지정한 `--energy-xlsx`와 `--memory-xlsx`를 읽기 전용으로 처리한다. FormulaEvaluator는 산술·셀 참조·SUM 범위만 해석하고 순환 참조와 실행 코드를 거부한다.

정규화 비교는 [Electronics 2025, 14(13), 2718](https://doi.org/10.3390/electronics14132718)의 Table 2 성분을 사용한다. 반올림된 표 수치의 계산을 비교하는 것이므로 실측 전력의 재측정과는 구분한다.

2026-10-19에 단위 검사 8개와 Excel 없는 실행 경로를 확인했다. 원본 Excel과 개인 경로, 기존 결과·이미지는 공개본에 포함하지 않았다.

## English

This code estimates Transformer parameter counts, FLOPs, weight reads and KV-cache traffic. It compares analytical energy components across batch sizes and context lengths using explicit coefficients. The decode model includes the output LM head and reports the omitted components.

The standalone demo runs without the original spreadsheets. Eight unit tests cover hand calculations, batch reuse, KV boundaries, dimensional validation and restricted formula evaluation. The normalized comparison uses rounded values from Table 2 of Electronics 2025, 14(13), 2718. These are analytical results rather than measured GPU or silicon power.

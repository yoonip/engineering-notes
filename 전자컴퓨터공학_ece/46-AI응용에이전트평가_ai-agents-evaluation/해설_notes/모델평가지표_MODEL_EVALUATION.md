# 모델 평가 지표 / Model evaluation metrics

## 품질

Accuracy는 전체 표본 중 정답 비율, precision은 양성 예측 중 실제 양성 비율, recall은 실제 양성 중 찾아낸 비율입니다. F1은 precision과 recall의 조화평균입니다. 생성 모델의 exact match·사람 평가·모델 기반 평가는 무엇을 정답으로 보고 어떻게 판정하는지가 다릅니다.

## 속도와 자원

Latency는 요청이 끝날 때까지 걸리는 시간, throughput은 단위 시간의 처리량입니다. 언어 모델에서는 첫 token까지 걸리는 시간과 이후 생성 속도를 나누어 봅니다. Peak memory는 어떤 메모리를 어느 범위에서 측정했는지에 따라 달라집니다. 가중치 저장 크기와 실제 실행 중 사용하는 메모리는 구분합니다.

## 비교 조건

Model revision·tokenizer·입력 집합·출력 길이·sampling·정밀도·장치·batch가 비교 조건에 해당합니다. 모델 변경과 실행 설정 변경의 영향을 나누어 보면 수치가 달라진 이유를 설명하기 쉽습니다.

## 같은 예측을 네 가지 지표로 계산하기

다음은 실제 모델을 실행한 결과가 아니라 지표를 비교하기 위해 직접 정한 1,000건의 예측입니다. 찾으려는 종류를 ‘양성’이라고 부르며, 실제 양성은 10건입니다.

| 실제·예측 | 양성으로 예측 | 음성으로 예측 |
| --- | ---: | ---: |
| 실제 양성 | TP=8 | FN=2 |
| 실제 음성 | FP=12 | TN=978 |

True는 맞게 분류했다는 뜻, false는 잘못 분류했다는 뜻입니다. Positive와 negative는 모델이 고른 쪽을 가리킵니다. 따라서 FP는 실제로 음성인데 양성으로 고른 경우, FN은 실제로 양성인데 놓친 경우입니다.

| 지표 | 이 표에서의 계산 | 판단할 내용 |
| --- | --- | --- |
| Accuracy | `(8+978)/1000=98.6%` | 전체 예측 중 맞게 분류한 비율 |
| Precision | `8/(8+12)=40%` | 양성으로 예측한 표본 중 실제 양성의 비율 |
| Recall | `8/(8+2)=80%` | 실제 양성 중 찾아낸 비율 |
| F1 | `2×8/(2×8+12+2)≈53.33%` | precision과 recall을 조화평균으로 함께 봅니다. |

모든 입력을 음성으로 고르는 기준 방법은 accuracy가 `990/1000=99%`지만 실제 양성 10건을 하나도 찾지 못합니다. 따라서 위 모델보다 accuracy가 높다는 사실만으로 대상 탐색에 더 유용하다고 결론 내릴 수는 없습니다. 이때 precision의 분모가 0이므로 수학적으로는 정의되지 않습니다. 평가 도구가 0 등으로 처리하는 규칙을 사용했다면 그 설정도 밝혀야 합니다. 정의는 [scikit-learn의 분류 지표 문서](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)에서 확인하실 수 있습니다.

분류 점수에 어느 선부터 양성이라고 표시할지 정하는 값이 threshold입니다. 이를 바꾸면 같은 모델에서도 FP·FN과 precision·recall이 달라질 수 있습니다. 평가 정답을 보고 유리한 threshold를 고른 뒤 별도의 검증인 것처럼 보고하지 않습니다.

## 생성 답변의 정답 기준

직접 만든 과제가 ‘본문에 나온 도시 이름을 JSON으로 출력합니다’이고 정답이 `{"city":"서울"}`이라고 하겠습니다. 의미만 맞는 `서울입니다.`와 구조까지 맞는 JSON은 같은 종류의 성공이 아닙니다. 다음 항목을 나누면 실패 원인을 찾기 쉽습니다.

| 관찰 | 판단할 부분 |
| --- | --- |
| 내용에 서울이 들어 있습니다. | 값 추출 여부를 확인합니다. |
| JSON parser가 읽을 수 있습니다. | 문법 형식을 확인합니다. |
| city 필드와 문자열 타입이 맞습니다. | 출력 계약을 확인합니다. |
| 본문에 없는 인구를 추가했습니다. | 근거 없는 정보 추가를 확인합니다. |

Exact match는 정한 전처리 뒤 답이 정확히 같은지 비교하는 기준입니다. 공백이나 대소문자를 정규화하는지에 따라 결과가 달라질 수 있습니다. 사람이 뜻을 판단하는 평가나 다른 모델이 점수를 매기는 평가에는 각자의 기준과 일관성 문제가 있으므로 모두 같은 ‘정확도’로 합치지 않습니다.

## 첫 토큰과 이후 토큰의 시간을 나누기

설명을 위해 요청 시각을 0초, 첫 출력 토큰을 0.2초, 마지막 다섯 번째 토큰을 1.4초로 정합니다. TTFT(time to first token)는 0.2초입니다. 첫 토큰 이후에는 네 간격이 있으므로 평균 간격은 `(1.4−0.2)/(5−1)=0.3초/토큰`입니다. 이를 역수로 쓰면 약 3.33토큰/초입니다.

전체 요청 시간으로 단순히 나눈 `5/1.4≈3.57토큰/초`와는 계산 범위가 다릅니다. 첫 토큰을 기다린 시간까지 포함한 비율인지, 이후 생성 간격인지 밝혀야 합니다. 출력이 한 토큰이면 이 방식의 간격 평균은 정의되지 않습니다. 지표의 정의와 집계 방식은 [NVIDIA의 LLM 벤치마크 지표 안내](https://docs.nvidia.com/nim/benchmarking/llm/metrics)처럼 사용한 도구의 문서를 함께 확인합니다.

여러 요청을 겹쳐 처리하는 서비스의 throughput도 개별 요청 latency의 단순 역수는 아닙니다. 예를 들어 요청 10개를 겹쳐 처리해 2초 동안 모두 마치면 관찰 구간 처리량은 5요청/초입니다. 각 요청이 얼마나 기다렸는지는 요청별 시작·종료 시각이 있어야 계산할 수 있습니다.

## 저장 크기와 실행 메모리

가중치 70억 개를 값당 16비트로 저장한다는 단순 가정에서는 `7×10⁹×16/8=14×10⁹ byte`, 즉 14GB입니다. 이진 단위로는 약 13.04GiB입니다. 그러나 이것은 가중치 원소의 저장량 계산입니다. 실제 실행에는 KV cache·activation·임시 버퍼가 필요하며, 양자화에서는 scale 같은 부가 자료도 생길 수 있습니다.

따라서 ‘파일이 14GB이므로 14GB 메모리에서 실행됩니다’라는 결론은 나오지 않습니다. [AI 추론 평가](../../../기술동향_technology/AI추론평가_2026-10.md)와 [캐시 예산](../../26-AI모델-API_open-model-lab/해설_notes/빔탐색과캐시예산_beam-cache-budget.md)을 함께 읽으시면 됩니다.

## 직접 확인하기

1. 양성 예측 20건 중 실제 양성이 15건이면 precision은 얼마입니까?
2. 실제 양성이 30건이고 그중 15건을 찾았다면 recall은 얼마입니까?
3. 모델 A와 B의 출력 길이가 다른데 완료시간만 비교하면 어떤 차이가 섞입니까?

<details>
<summary>답과 이유</summary>

1. `15/20=75%`입니다.
2. `15/30=50%`입니다. 첫 질문과 분모가 다릅니다.
3. 모델의 처리 속도와 생성한 일의 양이 섞입니다. 입력·출력 길이와 실제 완료한 작업의 품질을 함께 맞춰 비교해야 합니다.

</details>

## English

### Quality

Accuracy is the fraction of all samples predicted correctly. Precision is the fraction of positive predictions that are true positives, and recall is the fraction of actual positives found. F1 is the harmonic mean of precision and recall. For generative models, exact match, human evaluation, and model-based evaluation differ in what counts as a correct answer and how it is judged.

### Speed and resources

Latency is the time until a request finishes; throughput is the amount processed per unit of time. For language models, time to first token and subsequent generation speed can be measured separately. Peak memory depends on the memory type and measurement scope. Weight storage size is different from the memory used during execution.

### Comparison conditions

Model revision, tokenizer, inputs, output length, sampling, precision, device, and batch size define the comparison conditions. Separating model changes from execution-setting changes makes differences in the results easier to explain.

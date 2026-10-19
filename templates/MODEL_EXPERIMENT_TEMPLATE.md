# 모델 평가 지표

## 품질

Accuracy는 전체 표본 중 정답 비율, precision은 양성 예측 중 실제 양성 비율, recall은 실제 양성 중 찾아낸 비율이다. F1은 precision과 recall의 조화평균이다. 생성 모델의 exact match·사람 평가·모델 기반 평가는 무엇을 정답으로 보고 어떻게 판정하는지가 다르다.

## 속도와 자원

Latency는 요청이 끝날 때까지 걸리는 시간, throughput은 단위 시간의 처리량이다. 언어 모델에서는 첫 token까지 걸리는 시간과 이후 생성 속도를 나누어 본다. Peak memory는 어떤 메모리를 어느 범위에서 측정했는지에 따라 달라진다. 가중치 저장 크기와 실제 실행 중 사용하는 메모리는 구분한다.

## 비교 조건

Model revision·tokenizer·입력 집합·출력 길이·sampling·정밀도·장치·batch가 비교 조건에 해당한다. 모델 변경과 실행 설정 변경의 영향을 나누어 보면 수치가 달라진 이유를 설명하기 쉽다.

## English

### Quality

Accuracy is the fraction of all samples predicted correctly. Precision is the fraction of positive predictions that are true positives, and recall is the fraction of actual positives found. F1 is the harmonic mean of precision and recall. For generative models, exact match, human evaluation, and model-based evaluation differ in what counts as a correct answer and how it is judged.

### Speed and resources

Latency is the time until a request finishes; throughput is the amount processed per unit of time. For language models, time to first token and subsequent generation speed can be measured separately. Peak memory depends on the memory type and measurement scope. Weight storage size is different from the memory used during execution.

### Comparison conditions

Model revision, tokenizer, inputs, output length, sampling, precision, device, and batch size define the comparison conditions. Separating model changes from execution-setting changes makes differences in the results easier to explain.

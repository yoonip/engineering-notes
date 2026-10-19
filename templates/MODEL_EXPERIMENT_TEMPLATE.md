# 모델 평가 지표

## 품질

Accuracy는 전체 표본 중 정답 비율, precision은 양성 예측 중 실제 양성 비율, recall은 실제 양성 중 찾아낸 비율이다. F1은 precision과 recall의 조화평균이다. 생성 모델의 exact match·사람 평가·모델 기반 평가는 정답과 판정 방식이 다르다.

## 속도와 자원

Latency는 요청 완료까지의 시간, throughput은 단위 시간의 처리량이다. 언어 모델에서는 첫 token까지 시간과 이후 생성 속도를 나눌 수 있다. Peak memory는 측정한 메모리 종류와 범위에 따라 의미가 달라진다. 가중치 저장 크기와 실제 실행 중 메모리는 다르다.

## 비교 조건

Model revision·tokenizer·입력 집합·출력 길이·sampling·정밀도·장치·batch가 비교 조건을 구성한다. 모델 변경의 효과와 실행 설정의 효과를 구분해야 수치를 설명할 수 있다.

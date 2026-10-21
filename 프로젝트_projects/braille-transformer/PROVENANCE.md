# 코드와 자료의 출처

PyTorch의 `TransformerEncoder`·`TransformerDecoder`와 자동미분을 바탕으로 학습·평가·추론 코드를 구성했습니다. 이 공개 구현은 사전학습 T5 가중치를 불러오지 않고 문자 단위 Transformer를 처음부터 학습합니다. 구조는 [model.py](model.py), 기준 설정과 집계 지표는 [configs/reference_run.json](configs/reference_run.json)과 [results/reference_metrics.json](results/reference_metrics.json)에 있습니다.

자료는 국립국어원 [모두의 말뭉치](https://kli.korean.go.kr/m/main/requestMain.do)의 ‘묵자-점자 병렬 말뭉치 2025’입니다. 저장된 실험은 그중 신문 문장을 사용합니다. [prepare_data.py](prepare_data.py)는 로컬 원자료에서 분할·중복 그룹·해시를 기록한 manifest를 생성하며, 원자료별 manifest는 공개 패키지에 포함하지 않습니다. 공개된 분할 수와 정확도는 기준 설정·집계 지표에서 확인할 수 있습니다. 공식 배포 목록은 이 프로젝트의 분할·정확도를 검증하는 자료가 아닙니다. 원자료 이용 조건과 승인 절차는 국립국어원의 안내를 따릅니다.

모델·라이브러리·말뭉치의 출처와 이용 조건은 각 배포물을 따릅니다. 이 폴더에는 프로젝트 소스와 설정, 집계 지표가 있습니다. 원자료와 학습 가중치는 별도로 관리하며 외부 라이브러리는 의존성으로 설치합니다.

`SHA256SUMS.txt`는 현재 공개 파일의 바이트를 식별합니다. `validation.json`은 2026-10-19의 실행 기록이며, 문서 해시를 갱신한 것이 학습·추론을 다시 실행했다는 뜻은 아닙니다.

## English

The training, evaluation and inference code uses PyTorch's `TransformerEncoder` and `TransformerDecoder` with automatic differentiation. This public implementation trains a character-level Transformer from scratch; it does not load pretrained T5 weights. See [model.py](model.py), [the reference configuration](configs/reference_run.json) and [aggregate metrics](results/reference_metrics.json).

The data source is the National Institute of Korean Language's 2025 print–Braille parallel corpus, listed in [모두의 말뭉치](https://kli.korean.go.kr/m/main/requestMain.do). The recorded experiment uses newspaper sentences. [prepare_data.py](prepare_data.py) generates a manifest of local splits, duplicate groups and hashes; source-data manifests are not bundled. The public reference configuration and aggregate metrics record the split counts and accuracy. The official corpus listing does not establish these project-specific results. Corpus access and usage follow the institute's terms and authorization process.

Models, libraries and corpora retain their respective attribution and usage terms. This directory contains project source, configuration and aggregate metrics. Raw data and trained weights are managed separately; external libraries are installed as dependencies.

`SHA256SUMS.txt` identifies the current published bytes. `validation.json` retains the October 19, 2026 execution record; updating document hashes does not constitute another training or inference run.

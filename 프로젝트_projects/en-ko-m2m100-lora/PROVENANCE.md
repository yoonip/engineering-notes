# 코드와 자료의 출처

기본 모델은 Meta의 [facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M)이며, 고정 revision은 [configs/train.json](configs/train.json)에 기록했습니다. [train_extended.py](train_extended.py)는 PEFT의 LoRA를 q_proj·v_proj에 적용합니다. 모델 전체를 처음부터 학습한 프로젝트가 아니며, 기본 가중치와 추가 학습한 어댑터를 구분합니다.

추가 학습 자료는 Tatoeba의 영어·한국어 문장과 번역 연결 export입니다. [공식 배포 디렉터리](https://downloads.tatoeba.org/exports/)와 [prepare_tatoeba.py](prepare_tatoeba.py)의 입력 경로를 대조할 수 있습니다. [prepare_grouped_split.py](prepare_grouped_split.py)는 ID·정규화한 문장으로 그룹을 나누고 로컬 `split_manifest.json`을 생성합니다. 원자료와 분할별 manifest는 공개 패키지에 포함하지 않습니다. 동일 test의 기본 모델·LoRA 비교는 [results/reference_metrics.json](results/reference_metrics.json)에 있습니다. 현재 추가 학습의 분할 간 중복 검사와 기본 모델의 사전학습 자료 중복 여부는 별개이며, 후자는 확인되지 않았습니다.

모델·라이브러리·말뭉치의 출처와 이용 조건은 각 배포물을 따릅니다. 이 폴더에는 프로젝트 소스와 설정, 집계 지표가 있습니다. 원자료와 학습 가중치는 별도로 관리하며 외부 라이브러리는 의존성으로 설치합니다.

`SHA256SUMS.txt`는 현재 공개 파일의 바이트를 식별합니다. `validation.json`은 2026-10-19의 실행 기록이며, 문서 해시를 갱신한 것이 학습·추론을 다시 실행했다는 뜻은 아닙니다.

## English

The base is Meta's [facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M), with the fixed revision recorded in [configs/train.json](configs/train.json). [train_extended.py](train_extended.py) applies PEFT LoRA to q_proj and v_proj. The project fine-tunes adapters rather than training the entire base model from scratch.

Fine-tuning uses Tatoeba English/Korean sentences and translation-link exports. Compare the [official export directory](https://downloads.tatoeba.org/exports/) with the inputs in [prepare_tatoeba.py](prepare_tatoeba.py). [prepare_grouped_split.py](prepare_grouped_split.py) groups sentence IDs and normalized text and writes a local `split_manifest.json`. Raw data and split manifests are not bundled. [Reference metrics](results/reference_metrics.json) compare the base and adapter on the same test split. Checking overlap between the current fine-tuning splits does not establish that these sentences were absent from the base model's pretraining data; that overlap is unknown.

Models, libraries and corpora retain their respective attribution and usage terms. This directory contains project source, configuration and aggregate metrics. Raw data and trained weights are managed separately; external libraries are installed as dependencies.

`SHA256SUMS.txt` identifies the current published bytes. `validation.json` retains the October 19, 2026 execution record; updating document hashes does not constitute another training or inference run.

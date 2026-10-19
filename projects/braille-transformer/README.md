# 점자 → 한국어 Transformer

Unicode 6점 점자를 한국어로 복원하는 PyTorch 프로젝트다. Encoder 3층·decoder 3층의 Transformer를 처음부터 학습한다. 입력은 점자 문자, 출력은 NFD 한글 자모이며 생성 결과는 NFC로 합친다.

## 모델과 실험

| 항목 | 설정 또는 결과 |
| --- | --- |
| 구조 | d_model 256, head 8, FFN 1024, dropout 0.1 |
| 파라미터 | 5,672,691개, 입력 어휘 68·출력 어휘 243 |
| 자료 | 국립국어원 묵자-점자 병렬 말뭉치 2025, 신문 문장 |
| 분할 | train 66,824 / validation 8,352 / test 8,352 |
| 학습 | 16 epoch, batch 32, AdamW 0.0005, seed 20261006 |
| 모델 선택 | validation loss가 가장 낮은 epoch 16 |
| 평가 | 8,352쌍 전체, autoregressive greedy, beam 1 |
| CER | NFC 0.145706%, NFD 0.088645% |
| 문장 완전 일치 | 7,824 / 8,352 = 93.6782% |

공백·숫자·기호를 포함해 평가했고, CUDA FP16 autocast와 batch 32를 사용했다. 생성에는 정답 접두사를 제공하지 않았다. 동일 문서로 추정한 단위와 중복 입력·정답을 연결한 그룹을 분할에 사용했다. 평가 자료의 도메인은 신문 문장이며, 집계 결과는 `results/`에 있다.

## 실행

Python 3.12와 PyTorch를 사용한다. CPU·CUDA 설치 명령은 [PyTorch 설치 안내](https://pytorch.org/get-started/locally/)에서 환경에 맞게 선택한다. 기준 실행 환경은 `environment/`에 기록했다.

```powershell
python -m pip install -r requirements.txt -r requirements-notebook.txt
python -m unittest discover -s tests -v
python -m jupyterlab
```

말뭉치의 이용 승인을 받은 로컬 사본을 `data/raw/nikl`에 둔 뒤 학습·평가한다.

```powershell
python prepare_data.py --raw-dir data/raw/nikl --seed 20261006
python train.py --data-dir data/processed --run-dir checkpoints/reference --device cuda --epochs 16 --batch-size 32 --grad-accum 1 --seed 20261006
python evaluate.py --checkpoint checkpoints/reference --data-dir data/processed --data-manifest data_manifest.json --split test --device cuda --batch-size 32
python export_weights.py --checkpoint checkpoints/reference
python app.py --checkpoint checkpoints/reference
```

CPU 앱은 checkpoint의 `best.pt`, `config.json`, `vocab.json`을 함께 읽는다. 공개 저장소는 소스·재현 설정·집계 지표를 제공하며 말뭉치와 학습 가중치는 별도로 관리한다.

## 소스 구성

- `model.py`: 문자 사전, NFD/NFC, position encoding, pre-LN Transformer, causal/PAD mask, greedy 생성
- `train.py`: 길이 버킷, 유효 토큰 수 기반 gradient accumulation, AMP, AdamW, warmup·cosine, epoch 단위 재개
- `prepare_data.py`: 검수 점자 선택, 중복 그룹 구성, 분할과 내용 해시
- `inference.py`, `app.py`: 입력 검사, CPU/GPU 추론과 Tkinter 앱
- `evaluate.py`, `export_weights.py`: 생성 결과 평가와 가중치 추출
- `notebooks/01_workflow.ipynb`: 데이터 준비부터 학습·추론까지 연결한 노트북

2026-10-19의 공개본 검사에서는 합성 자료 테스트 6개와 CLI·노트북 기본 실행을 확인했다. 위 학습 지표는 저장된 최종 실험의 결과이며, 이번 소스 정리 과정에서 전체 모델을 다시 학습하지 않았다. 세부 기록은 `validation.json`, 작성 경위는 `PROVENANCE.md`에 있다.

## English

A character-level encoder–decoder Transformer for Unicode six-dot Braille to Korean. The model was trained from scratch for 16 epochs and evaluated on all 8,352 held-out newspaper sentences using autoregressive greedy decoding. The recorded NFC CER is 0.145706%, with 93.6782% exact sentence match. Source code, reproducible configuration, notebooks and aggregate metrics are included; the corpus and trained weights are managed separately.

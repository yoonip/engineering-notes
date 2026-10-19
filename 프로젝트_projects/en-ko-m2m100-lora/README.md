# M2M100 + LoRA 영한 번역

Meta의 `facebook/m2m100_418M`에 LoRA를 적용한 영한 번역 프로젝트입니다. 학습·평가 코드와 CPU·GPU 추론 앱을 포함합니다. 최신 버전은 중복 문장을 그룹으로 묶어 분할한 자료로 3 epoch 학습했습니다.

## 모델과 실험

| 항목 | 설정 또는 결과 |
| --- | --- |
| 기본 모델 revision | 55c2e61bbf05dfb8d7abccdc3fae6fc8512fd636 |
| LoRA | q_proj·v_proj, rank 8, alpha 16, dropout 0.05 |
| 파라미터 | 전체 485,085,184 / 학습 대상 1,179,648개 |
| 자료 | Tatoeba 영한 문장쌍 11,552개 |
| 그룹 분할 | train 9,242 / validation 1,155 / test 1,155 |
| 학습 | 3 epoch, batch 2, gradient accumulation 8, max_length 96 |
| 최적화 | AdamW 0.00005, 3% warmup + cosine, clip norm 1.0 |
| 모델 선택 | validation loss가 가장 낮은 epoch 3 |

| 동일 test 1,155쌍 | 기본 모델 | LoRA 학습 후 |
| --- | --- | --- |
| BLEU | 10.2877 | 12.8599 |
| chrF | 28.9328 | 31.2576 |

평가는 SacreBLEU 2.6.0, beam 4, 한국어 forced BOS, 생성 최대 128토큰, CUDA FP16, batch 8로 수행했습니다. 동일 문장 ID와 정규화한 원문·번역문을 연결한 그룹이 한 분할에만 들어가도록 했습니다. 수치는 이 Tatoeba 시험 조건의 결과이며, CPU FP32·INT8 추론은 별도 조건입니다. 집계 지표와 설정은 `results/`, `configs/`에 있습니다.

## 실행

Python 3.12와 PyTorch를 사용합니다. CPU·CUDA 설치 명령은 [PyTorch 설치 안내](https://pytorch.org/get-started/locally/)에서 선택합니다. 기준 실행 환경은 `environment/`에 기록했습니다.

```powershell
python -m pip install -r requirements.txt -r requirements-notebook.txt
python -m unittest discover -s tests -v
python -m jupyterlab
```

Tatoeba export의 로컬 사본은 다음 경로에 둡니다.

```text
data/raw/tatoeba/eng_sentences.tsv.bz2
data/raw/tatoeba/kor_sentences.tsv.bz2
data/raw/tatoeba/links.tar.bz2
```

```powershell
python prepare_tatoeba.py
python prepare_grouped_split.py
python fetch_model.py
python train_extended.py --config configs/train.json --run-dir checkpoints/reference
python evaluate_extended.py --run-dir checkpoints/reference --batch-size 8
python cpu_app.py --checkpoint checkpoints/reference/adapter --quantization none
python editable_app.py --checkpoint checkpoints/reference/adapter --device cpu
```

`fetch_model.py`는 고정 revision의 기본 모델을 내려받습니다. 학습은 기본 모델에서 새 LoRA를 시작하며 `--init-adapter`는 가중치만 가져와 optimizer와 scheduler를 새로 만듭니다. 앱은 로컬 기본 모델과 학습된 어댑터를 함께 사용합니다. 기본 모델의 cache·어댑터·원자료는 소스 저장소와 별도로 관리합니다.

## 소스 구성

- `train_extended.py`: 설정 파일을 읽는 학습 CLI, token-weighted loss와 gradient accumulation
- `prepare_tatoeba.py`, `prepare_grouped_split.py`: 원자료 처리와 그룹 분할
- `evaluate_extended.py`: 같은 test에서 기본 모델과 어댑터 비교
- `cpu_app.py`: CPU FP32와 선택적 Linear 동적 INT8 양자화, Tkinter 화면
- `editable_app.py`: GPU/CPU 선택 앱
- `fetch_model.py`: 기본 모델 다운로드
- `notebooks/01_workflow.ipynb`: 학습·평가·추론을 연결한 노트북

2026-10-19 검사에서는 작은 무작위 모델과 합성 자료 테스트 6개, CLI·노트북 기본 실행을 확인했습니다. 전체 번역 모델을 새로 학습하거나 다운로드하지 않았습니다. 세부 결과는 `validation.json`, 구성 안내는 `PROVENANCE.md`에 있습니다.

## English

This English-to-Korean translation project applies LoRA to Meta's `facebook/m2m100_418M`. It includes training/evaluation code and CPU/GPU inference apps. The reference run trained for three epochs after grouping connected duplicate sentences before splitting.

### Model and experiment

| Item | Configuration or result |
| --- | --- |
| Base-model revision | `55c2e61bbf05dfb8d7abccdc3fae6fc8512fd636` |
| LoRA | q_proj/v_proj, rank 8, alpha 16, dropout 0.05 |
| Parameters | 485,085,184 total; 1,179,648 trainable |
| Corpus | 11,552 Tatoeba English–Korean pairs |
| Grouped split | 9,242 training / 1,155 validation / 1,155 test |
| Training | Three epochs, batch 2, accumulation 8, max_length 96 |
| Optimization | AdamW 0.00005, 3% warmup/cosine, clip norm 1.0 |
| Checkpoint | Epoch 3, selected by the lowest validation loss |

| Same 1,155-pair test set | Base model | After LoRA |
| --- | --- | --- |
| BLEU | 10.2877 | 12.8599 |
| chrF | 28.9328 | 31.2576 |

Evaluation used SacreBLEU 2.6.0, beam 4, Korean forced BOS, a 128-token generation limit, CUDA FP16 and batch 8. Connected groups of sentence IDs and normalized source/target text remain within one split. These scores describe this Tatoeba test condition; CPU FP32/INT8 inference is a separate condition. Metrics and settings are in `results/` and `configs/`.

### Running the project

Use Python 3.12 and a suitable [PyTorch CPU/CUDA installation](https://pytorch.org/get-started/locally/). `environment/` records the reference runtime. Install dependencies and run the tests/JupyterLab using the commands above.

Place local Tatoeba exports at the three listed `data/raw/tatoeba/` paths, then run preparation, grouped splitting, base-model download, training and evaluation. `fetch_model.py` downloads the pinned revision. Training starts a new LoRA adapter from the base model; `--init-adapter` loads only adapter weights and creates a new optimizer/scheduler. The apps need both the local base model and trained adapter. Caches, adapters and raw data are managed outside the source set.

### Source and checks

- `train_extended.py`: configuration-driven CLI, token-weighted loss and gradient accumulation.
- `prepare_tatoeba.py` / `prepare_grouped_split.py`: corpus preparation and connected-group splitting.
- `evaluate_extended.py`: base/adapter comparison on the same test set.
- `cpu_app.py`: CPU FP32 or optional dynamic INT8 Linear quantization with Tkinter.
- `editable_app.py`: selectable CPU/GPU inference app.
- `fetch_model.py`: base-model download.
- `notebooks/01_workflow.ipynb`: training, evaluation and inference workflow.

The October 19, 2026 check ran six synthetic-data tests with a small random model, plus basic CLI/notebook execution. It did not retrain or download the full translation model. See `validation.json` and `PROVENANCE.md` for the recorded checks and package information.

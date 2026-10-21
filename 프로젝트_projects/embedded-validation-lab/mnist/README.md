# MNIST CNN

28×28 손글씨 영상을 두 개의 convolution block과 fully connected layer로 분류합니다. 학습 데이터 60,000장을 학습 55,000장·검증 5,000장으로 나누고, 별도의 시험 데이터 10,000장으로 최종 성능을 평가합니다. 검증 loss가 가장 낮은 checkpoint를 저장합니다.

`train_mnist.py`는 학습과 평가, `infer_mnist.py`는 저장한 checkpoint의 단일 영상 추론, `plot_results.py`는 loss·accuracy 곡선과 confusion matrix, 정답·오답 영상 시각화를 담당합니다. 코드와 의존성 목록을 제공하며 데이터와 가중치는 포함하지 않습니다.

## 실행

이 디렉터리에서 실행합니다.

```bash
python -m pip install -r requirements.txt
python train_mnist.py --epochs 5 --device cpu --data data
python infer_mnist.py --checkpoint results/best.pt --data data --index 0
python plot_results.py --data data
```

데이터는 torchvision을 통해 받으며 결과는 `results/`에 저장합니다. `train_mnist.py`의 `--device`로 학습 장치를 지정합니다.

## 저장된 실행 결과

기존 CPU 실행 기록은 seed 42, Adam, learning rate 0.001, batch size 128, 5 epoch 조건입니다. 최종 시험 결과는 10,000장 중 9,903장 정답, accuracy 99.03%, cross-entropy loss 0.0305511763입니다. 이 수치는 CPU 실행에서 얻었으며 GPU 학습 성능을 나타내지 않습니다.

[기존 실행의 원본 지표](reference_metrics.json)에 epoch별 기록과 confusion matrix를 함께 보관했습니다. 이번 문서 점검에서는 학습을 다시 실행하지 않았으며, 저장된 행렬의 전체 합 10,000과 대각선 합 9,903을 지표와 대조했습니다. 당시 작업 폴더의 `train_mnist.py`와 이 폴더의 소스는 SHA-256이 같습니다. 데이터·checkpoint는 이 저장소에 포함하지 않아 지표 파일만으로 단일 영상 추론을 다시 실행할 수는 없습니다.

| 보존 자료 | SHA-256 |
| --- | --- |
| `reference_metrics.json` | `6f09dbff42da2964c8c7e3c4049672bcc9db9238aa758b4f5b5a0085d96b1518` |
| `train_mnist.py` | `ed987c31f076c64b173db230c42b6e2d1cbe42b2649481d170b02ff019535f8d` |

## English

This CNN classifies 28×28 handwritten digits using two convolution blocks and a fully connected layer. The 60,000 training images are divided into 55,000 training and 5,000 validation images; 10,000 separate test images provide final evaluation. The lowest validation loss selects the checkpoint.

`train_mnist.py` handles training/evaluation, `infer_mnist.py` runs one image from a saved checkpoint, and `plot_results.py` plots loss, accuracy, a confusion matrix and correct/incorrect examples. Source and dependencies are included; data and weights are generated locally.

Run the commands above from this directory. Torchvision downloads MNIST and results go in `results/`. Select the training device with `train_mnist.py --device`.

The recorded CPU run used seed 42, Adam, learning rate 0.001, batch 128 and five epochs. It classified 9,903 of 10,000 test images correctly: 99.03% accuracy and cross-entropy loss 0.0305511763. These are CPU results, not GPU training measurements.

The [original metrics](reference_metrics.json) retain epoch history and the confusion matrix. This document review did not retrain the model. The matrix total and diagonal sum agree with 10,000 examples and 9,903 correct predictions, and the original training script matches the published source hash above. Data and checkpoint files are not included, so the metrics alone do not replay inference.

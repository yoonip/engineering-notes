# MNIST CNN

28×28 손글씨 영상을 두 개의 convolution block과 fully connected layer로 분류한다. 학습 데이터 60,000장을 학습 55,000장·검증 5,000장으로 나누고, 별도의 시험 데이터 10,000장으로 최종 성능을 평가한다. 검증 loss가 가장 낮은 checkpoint를 저장한다.

`train_mnist.py`는 학습과 평가, `infer_mnist.py`는 저장한 checkpoint의 단일 영상 추론, `plot_results.py`는 loss·accuracy 곡선과 confusion matrix, 정답·오답 영상 시각화를 담당한다. 코드와 의존성 목록을 제공하며 데이터와 가중치는 포함하지 않는다.

## 실행

이 디렉터리에서 실행한다.

```bash
python -m pip install -r requirements.txt
python train_mnist.py --epochs 5 --device cpu --data data
python infer_mnist.py --checkpoint results/best.pt --data data --index 0
python plot_results.py --data data
```

데이터는 torchvision을 통해 받으며 결과는 `results/`에 저장한다. `train_mnist.py`의 `--device`로 학습 장치를 지정한다.

## 저장된 실행 결과

기존 CPU 실행 기록은 seed 42, Adam, learning rate 0.001, batch size 128, 5 epoch 조건이다. 최종 시험 결과는 10,000장 중 9,903장 정답, accuracy 99.03%, cross-entropy loss 0.0305511763이다. 이 수치는 CPU 실행에서 얻었으며 GPU 학습 성능을 나타내지 않는다.

## English

This CNN classifies 28×28 handwritten digits using two convolution blocks and a fully connected layer. The 60,000 training images are divided into 55,000 training and 5,000 validation images; 10,000 separate test images provide final evaluation. The lowest validation loss selects the checkpoint.

`train_mnist.py` handles training/evaluation, `infer_mnist.py` runs one image from a saved checkpoint, and `plot_results.py` plots loss, accuracy, a confusion matrix and correct/incorrect examples. Source and dependencies are included; data and weights are generated locally.

Run the commands above from this directory. Torchvision downloads MNIST and results go in `results/`. Select the training device with `train_mnist.py --device`.

The recorded CPU run used seed 42, Adam, learning rate 0.001, batch 128 and five epochs. It classified 9,903 of 10,000 test images correctly: 99.03% accuracy and cross-entropy loss 0.0305511763. These are CPU results, not GPU training measurements.

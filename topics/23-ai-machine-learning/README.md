# AI · Machine Learning · Deep Learning

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

머신러닝은 데이터에서 입력과 출력의 관계를 찾거나 데이터 자체의 구조를 학습한다. 지도학습은 정답이 있는 데이터, 비지도학습은 분포와 구조, 강화학습은 행동에 따른 보상과 상태 변화를 다룬다. 딥러닝은 여러 층의 신경망으로 표현을 학습한다.

## 학습과 평가

모델은 입력에서 예측을 만들고 손실함수는 예측과 목표의 차이를 수치화한다. 자동미분은 연산 그래프를 따라 파라미터의 기울기를 계산하며 optimizer는 그 값을 이용해 파라미터를 갱신한다. 학습·검증·테스트 분리는 데이터 누출과 평가 편향을 줄이는 기본 구조다.

## 모델 구조

CNN은 공간적으로 공유하는 필터, RNN은 순차적인 상태 갱신, Transformer는 attention을 중심으로 구성된다. Attention은 입력 표현들 사이의 관계에 따라 정보를 결합한다. MoE는 여러 expert 중 일부를 선택해 계산한다. Diffusion 모델은 잡음을 넣고 제거하는 과정을 학습하는 생성 모델 계열이다.

PyTorch·TensorFlow·Keras·JAX는 텐서 연산과 모델 학습에 쓰인다. scikit-learn은 전통적인 머신러닝, XGBoost·LightGBM·CatBoost는 gradient boosting 생태계다. Hugging Face Transformers는 여러 모델의 학습·추론 인터페이스를 제공하고 Lightning·fastai는 학습 코드 구성을 돕는다. 데이터 품질과 평가 설계도 모델 크기만큼 결과에 영향을 준다.

## 자동미분 예제

`y=x²`이면 `dy/dx=2x`다. PyTorch에서 x=3인 지점의 미분은 다음처럼 표현한다.

```python
import torch

x = torch.tensor(3.0, requires_grad=True)
y = x.square()
y.backward()
print(x.grad.item())  # dy/dx = 6.0
```

TensorFlow에서는 GradientTape가 미분에 필요한 연산을 기록한다.

```python
import tensorflow as tf

x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x * x
gradient = tape.gradient(y, x)
print(gradient.numpy())  # dy/dx = 6.0
```

두 예제는 scalar의 국소 미분을 구한다. 신경망 학습에서는 많은 parameter에 대한 gradient를 계산해 optimizer에 전달한다.

## 관련 기술

PyTorch, TensorFlow/Keras, JAX, scikit-learn, XGBoost, LightGBM, CatBoost, Hugging Face, Lightning, fastai

## 참고 자료

- [PyTorch — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
- [TensorFlow Guide](https://www.tensorflow.org/guide)


## 개념·유도·모델·검증

[기초부터 읽기](../../docs/FOUNDATIONS.md)

- [미분에서 학습까지: 모델이 바뀌는 이유](notes/gradients-and-learning.md)

## English

Machine learning learns relationships between inputs and outputs or structure within data. Supervised learning uses labeled data, unsupervised learning studies distributions and structure, and reinforcement learning concerns actions, rewards, and changing state. Deep learning learns representations through multilayer neural networks.

### Training and evaluation

A model produces predictions, and a loss function measures their difference from the target. Automatic differentiation calculates parameter gradients through a computation graph, and an optimizer uses them to update the parameters. Separating training, validation, and test data helps prevent leakage and biased evaluation.

### Model structures

CNNs share filters across space, RNNs update a sequential state, and Transformers are built around attention. Attention combines information according to relationships between input representations. Mixture-of-experts models activate selected experts, while diffusion models learn generative processes based on adding and removing noise.

PyTorch, TensorFlow, Keras, and JAX provide tensor computation and model training. scikit-learn covers traditional machine learning; XGBoost, LightGBM, and CatBoost support gradient boosting. Hugging Face Transformers provides training and inference interfaces for many models. Lightning and fastai help organize training code. Data quality and evaluation design can influence results as much as model size.

### Automatic differentiation example

For `y=x²`, the derivative is `dy/dx=2x`. The PyTorch example above calculates a gradient of 6 at `x=3` using `requires_grad`, `backward()`, and `x.grad`. The TensorFlow example obtains the same result using `GradientTape`, which records the operations required for differentiation.

These examples compute a local derivative of a scalar function. Neural-network training calculates gradients for many parameters and passes them to an optimizer.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../docs/FOUNDATIONS.md#english)

- [Gradients, backpropagation and learning](notes/gradients-and-learning.md#english)

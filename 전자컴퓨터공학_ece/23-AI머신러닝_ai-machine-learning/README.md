# AI·머신러닝·딥러닝 | AI, Machine Learning & Deep Learning

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

머신러닝은 데이터에서 입력과 출력의 관계를 찾거나 데이터 자체의 구조를 학습합니다. 지도학습은 정답이 있는 데이터, 비지도학습은 분포와 구조, 강화학습은 행동에 따른 보상과 상태 변화를 다룹니다. 딥러닝은 여러 층의 신경망으로 표현을 학습합니다.

## 학습과 평가

모델은 입력에서 예측을 만들고 손실함수는 예측과 목표의 차이를 수치화합니다. 자동미분은 연산 그래프를 따라 파라미터의 기울기를 계산하며 optimizer는 그 값을 이용해 파라미터를 갱신합니다. 학습·검증·테스트 분리는 데이터 누출과 평가 편향을 줄이는 기본 구조입니다.

## 모델 구조

CNN은 공간적으로 공유하는 필터, RNN은 순차적인 상태 갱신, Transformer는 attention을 중심으로 구성됩니다. Attention은 입력 표현들 사이의 관계에 따라 정보를 결합합니다. MoE는 여러 expert 중 일부를 선택해 계산합니다. Diffusion 모델은 잡음을 넣고 제거하는 과정을 학습하는 생성 모델 계열입니다.

PyTorch·TensorFlow·Keras·JAX는 텐서 연산과 모델 학습에 쓰입니다. scikit-learn은 전통적인 머신러닝, XGBoost·LightGBM·CatBoost는 gradient boosting 생태계입니다. Hugging Face Transformers는 여러 모델의 학습·추론 인터페이스를 제공하고 Lightning·fastai는 학습 코드 구성을 돕습니다. 데이터 품질과 평가 설계도 모델 크기만큼 결과에 영향을 줍니다.

## 자동미분 예제

`y=x²`이면 `dy/dx=2x`입니다. PyTorch에서 x=3인 지점의 미분은 다음처럼 표현합니다.

```python
import torch  # import는 PyTorch 패키지를 불러옵니다.

x = torch.tensor(3.0, requires_grad=True)  # 미분 대상인 실수 scalar tensor를 만듭니다.
y = x.square()  # .square()는 원소의 제곱을 계산하며 미분 경로를 기록합니다.
y.backward()  # scalar y의 미분을 역으로 전파해 x.grad에 누적합니다.
print(x.grad.item())  # .item()으로 scalar 값을 꺼냅니다. 새 x의 기대 미분값은 6.0입니다.
```

TensorFlow에서는 GradientTape가 미분에 필요한 연산을 기록합니다.

```python
import tensorflow as tf  # as는 TensorFlow 패키지에 짧은 이름 tf를 붙입니다.

x = tf.Variable(3.0)  # 기본적으로 미분을 추적하는 실수 변수를 만듭니다.
with tf.GradientTape() as tape:  # with 블록 안에서 미분에 필요한 연산을 기록합니다.
    y = x * x  # *는 곱셈이며 y=x²를 계산합니다.
gradient = tape.gradient(y, x)  # 기록한 경로를 따라 dy/dx를 계산합니다.
print(gradient.numpy())  # NumPy 값으로 꺼냅니다. 이 예제의 기대 미분값은 6.0입니다.
```

두 예제는 scalar의 국소 미분을 구하며 파라미터를 갱신하지 않습니다. PyTorch의 `backward()`는 leaf tensor의 `.grad`에 미분을 누적하므로, 여러 학습 step에서 매번 새 gradient만 쓰려면 이전 gradient를 지워야 합니다. TensorFlow는 이 예제의 trainable `Variable`을 기본 추적하지만 일반 `Tensor`에는 `tape.watch()`가 필요할 수 있습니다. 기본 tape는 한 번의 `gradient()` 호출 뒤 자원을 해제합니다. [PyTorch 자동미분의 Computing Gradients·More on Computational Graphs](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), [TensorFlow의 추적 대상·tape 수명 설명](https://www.tensorflow.org/guide/autodiff)을 기준으로 한 코드 설명이며, 이 문서에서 두 프레임워크를 새로 실행한 결과는 아닙니다.

## 관련 기술

PyTorch, TensorFlow/Keras, JAX, scikit-learn, XGBoost, LightGBM, CatBoost, Hugging Face, Lightning, fastai

## 참고 자료

- [PyTorch — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
- [TensorFlow Guide](https://www.tensorflow.org/guide)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [미분에서 학습까지: 모델이 바뀌는 이유](해설_notes/미분에서학습까지_gradients-and-learning.md)

## English

Machine learning learns relationships between inputs and outputs or structure within data. Supervised learning uses labeled data, unsupervised learning studies distributions and structure, and reinforcement learning concerns actions, rewards, and changing state. Deep learning learns representations through multilayer neural networks.

### Training and evaluation

A model produces predictions, and a loss function measures their difference from the target. Automatic differentiation calculates parameter gradients through a computation graph, and an optimizer uses them to update the parameters. Separating training, validation, and test data helps prevent leakage and biased evaluation.

### Model structures

CNNs share filters across space, RNNs update a sequential state, and Transformers are built around attention. Attention combines information according to relationships between input representations. Mixture-of-experts models activate selected experts, while diffusion models learn generative processes based on adding and removing noise.

PyTorch, TensorFlow, Keras, and JAX provide tensor computation and model training. scikit-learn covers traditional machine learning; XGBoost, LightGBM, and CatBoost support gradient boosting. Hugging Face Transformers provides training and inference interfaces for many models. Lightning and fastai help organize training code. Data quality and evaluation design can influence results as much as model size.

### Automatic differentiation example

For `y=x²`, the derivative is `dy/dx=2x`. The PyTorch example above calculates a gradient of 6 at `x=3` using `requires_grad`, `backward()`, and `x.grad`. The TensorFlow example obtains the same result using `GradientTape`, which records the operations required for differentiation.

These examples compute a local scalar derivative without updating parameters. PyTorch `backward()` accumulates into a leaf tensor's `.grad`, so clear old gradients when each training step should use a fresh gradient. TensorFlow watches the trainable `Variable` used here by default; an ordinary `Tensor` may require `tape.watch()`. A default tape releases its resources after one `gradient()` call. These explanations follow [PyTorch's gradient and computation-graph sections](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) and [TensorFlow's watching and tape-lifetime sections](https://www.tensorflow.org/guide/autodiff); they do not report a new execution of either framework.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Gradients, backpropagation and learning](해설_notes/미분에서학습까지_gradients-and-learning.md#english)


## 심화 해설 | Advanced article

- [작은 MLP로 역전파를 끝까지 계산하기](해설_notes/다층신경망역전파_mlp-backprop.md) · [English](해설_notes/다층신경망역전파_mlp-backprop.md#english)

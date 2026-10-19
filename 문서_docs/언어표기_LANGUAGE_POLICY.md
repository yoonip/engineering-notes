# 기술 용어와 표기

## 언어·도구·모델

C·C++·Python은 프로그래밍 언어다. Linux는 커널, Ubuntu는 배포판, Bash는 셸, Git은 버전 관리 도구, GitHub는 저장소 호스팅·협업 서비스다. PyTorch·TensorFlow는 학습 framework이고 GPT·Llama 같은 이름은 모델 계열을 가리킨다.

## 학습과 실행

Training은 데이터로 parameter를 갱신하는 과정, inference는 정해진 parameter로 출력을 계산하는 과정이다. Fine-tuning은 기반 모델을 추가 데이터로 조정하고, distillation은 다른 모델의 동작을 학습 자료로 사용한다. 공개 코드와 공개 가중치는 배포 대상이 다르다.

## 단위와 축

대문자 B는 byte, 소문자 b는 bit다. Bandwidth는 단위 시간에 이동할 수 있는 데이터량, latency는 요청에서 완료까지의 시간이다. Accuracy·precision·recall은 분류 평가에서 다른 의미를 갖고, 계측에서 쓰는 정확도·정밀도와도 문맥이 다르다. 단위와 평가 정의가 수치의 의미를 정한다.

## English

### Languages, tools, and models

C, C++, and Python are programming languages. Linux is a kernel, Ubuntu is a distribution, Bash is a shell, Git manages version history, and GitHub hosts repositories and collaboration. PyTorch and TensorFlow are training frameworks; names such as GPT and Llama refer to model families.

### Training and execution

Training updates parameters using data; inference computes outputs with a fixed set of parameters. Fine-tuning adapts a base model with additional data, while distillation uses another model's behavior as training material. Source code and model weights are separate kinds of release.

### Units and evaluation

Uppercase B means byte, while lowercase b means bit. Bandwidth measures data transferred per unit of time; latency measures time from request to completion. Accuracy, precision, and recall describe different aspects of classification, and their use differs from accuracy and precision in measurement. A number only becomes meaningful once its units and evaluation method are clear.

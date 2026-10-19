# 기술 용어와 표기

## 언어·도구·모델

C·C++·Python은 프로그래밍 언어입니다. Linux는 커널, Ubuntu는 배포판, Bash는 셸, Git은 버전 관리 도구, GitHub는 저장소 호스팅·협업 서비스입니다. PyTorch·TensorFlow는 학습 framework이고 GPT·Llama 같은 이름은 모델 계열을 가리킵니다.

## 학습과 실행

Training은 데이터로 parameter를 갱신하는 과정, inference는 정해진 parameter로 출력을 계산하는 과정입니다. Fine-tuning은 기반 모델을 추가 데이터로 조정하고, distillation은 다른 모델의 동작을 학습 자료로 사용합니다. 공개 코드와 공개 가중치는 배포 대상이 다릅니다.

## 단위와 축

대문자 B는 byte, 소문자 b는 bit입니다. Bandwidth는 단위 시간에 이동할 수 있는 데이터량, latency는 요청에서 완료까지의 시간입니다. Accuracy·precision·recall은 분류 평가에서 다른 의미를 갖고, 계측에서 쓰는 정확도·정밀도와도 문맥이 다릅니다. 단위와 평가 정의가 수치의 의미를 정합니다.

## 한 작업에서 각 이름이 맡는 역할

‘Python으로 모델을 실행합니다’라는 말 안에도 서로 다른 대상이 있습니다. Python 코드를 읽는 실행기, 배열과 미분 계산을 제공하는 PyTorch, 모델 구조를 정한 코드, 학습된 가중치, 텍스트를 토큰으로 바꾸는 tokenizer, CPU·GPU 장치를 나누어 보시면 오류 위치를 찾기 쉽습니다.

| 대상 | 뜻 | 구분할 예 |
| --- | --- | --- |
| 언어 | 프로그램을 표현하는 문법과 의미의 체계입니다. | Python 문법으로 코드를 적습니다. |
| 실행기·runtime | 프로그램을 실행하고 필요한 동작을 지원합니다. | Python 실행기 버전이 필요한 문법을 지원하는지 확인합니다. |
| Library | 프로그램에서 불러 쓸 기능의 모음입니다. | 수학·배열·파일 처리 기능을 사용합니다. |
| Framework | 프로그램을 구성하고 실행하는 흐름도 제공하는 도구입니다. | PyTorch로 연산과 학습을 구성합니다. library와 경계가 언제나 엄격한 것은 아닙니다. |
| 모델 구조 | 입력에서 출력까지 어떤 계산을 할지 정합니다. | 층 수와 각 층의 연산을 정합니다. |
| 가중치 | 그 구조의 계산에 사용하는 학습된 값입니다. | 구조가 같아도 학습된 값이 다르면 출력이 달라집니다. |
| API | 프로그램 사이에 요청·응답을 주고받는 약속입니다. | 함수 호출 규약이나 HTTP 요청의 필드와 형식이 해당합니다. |
| 배포물·revision | 특정 시점에 제공된 코드·파일·설정입니다. | 같은 계열 이름이어도 revision이 바뀌면 비교 조건이 달라질 수 있습니다. |

Tokenizer가 다른 두 모델에 같은 문장을 넣으면 토큰 수가 달라질 수 있습니다. 따라서 ‘한 토큰은 한 단어’라고 고정하거나, 두 모델의 토큰/초 숫자만으로 같은 문장을 처리하는 속도를 단정하지 않습니다. 문자 수·단어 수·토큰 수와 실제 완료시간의 차이를 함께 봅니다.

## 숫자와 단위를 직접 바꾸기

전송량 80Mbit를 초당 100Mbit의 일정한 유효 전송률로 보낸다는 단순 가정에서는 `80/100=0.8초`가 걸립니다. 80Mbyte라면 8배인 640Mbit이므로 같은 가정에서 6.4초입니다. 여기서 M은 10⁶으로 정했습니다. 실제 통신에서는 헤더·재전송·대기 등이 추가될 수 있으므로 이 나눗셈을 네트워크 실측 latency로 표시하지 않습니다.

메모리에서는 1GB=10⁹byte, 1GiB=2³⁰byte를 구분합니다. 같은 바이트 수라도 단위를 바꾸면 표시 숫자가 달라집니다. [모델 평가 지표](../제품리뷰_reviews/모델평가지표_MODEL_EVALUATION.md)에서 70억 가중치의 저장량과 실행 메모리를 비교하실 수 있습니다.

## 논문 용어로 이어가기

Attention·normalization·regularization·gradient·embedding의 뜻과 뉘앙스는 [논문에서 자주 만나는 말](../논문해설_papers/논문을읽는용어_PAPER_TERMS.md)에 숫자 예와 함께 있습니다. 용어가 익숙하지 않으시면 먼저 그 글의 예를 계산한 뒤 해당 논문으로 돌아오시면 됩니다.

직접 확인해 보시려면 ‘GitHub는 언어입니까, 서비스입니까?’, ‘가중치를 고정한 채 입력 예시만 바꾸면 무엇이 바뀝니까?’, ‘8Mbyte는 몇 Mbit입니까?’에 답해보십시오. 각각 저장소 호스팅·협업 서비스, 입력 문맥, 64Mbit입니다. 같은 계층에 있지 않은 이름과 단위를 구분하는 연습입니다.

## English

### Languages, tools, and models

C, C++, and Python are programming languages. Linux is a kernel, Ubuntu is a distribution, Bash is a shell, Git manages version history, and GitHub hosts repositories and collaboration. PyTorch and TensorFlow are training frameworks; names such as GPT and Llama refer to model families.

### Training and execution

Training updates parameters using data; inference computes outputs with a fixed set of parameters. Fine-tuning adapts a base model with additional data, while distillation uses another model's behavior as training material. Source code and model weights are separate kinds of release.

### Units and evaluation

Uppercase B means byte, while lowercase b means bit. Bandwidth measures data transferred per unit of time; latency measures time from request to completion. Accuracy, precision, and recall describe different aspects of classification, and their use differs from accuracy and precision in measurement. A number only becomes meaningful once its units and evaluation method are clear.

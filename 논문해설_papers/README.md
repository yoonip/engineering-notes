# 논문 해설 | Paper studies

계산 이론·정보·전자소자·분산 시스템·신경망의 설계에 큰 영향을 준 논문 30편을 한국어로 읽습니다. 처음 등장하는 전문 용어의 뜻과 뉘앙스를 풀고, 작은 숫자나 직접 만든 사례로 방법을 따라갑니다. 원 논문이 제시한 근거와 이 저장소의 예제·계산은 본문에서 구분합니다.

## 처음 읽으실 때

[논문에서 자주 만나는 말](논문을읽는용어_PAPER_TERMS.md)부터 읽으시면 attention, normalization, regularization, gradient, embedding과 inference를 예제로 구분하실 수 있습니다. 수식의 기호를 모를 때에는 그 기호가 나타내는 값, 모양과 단위를 먼저 확인합니다.

| 관심 | 이어서 읽을 순서 | 따라갈 질문 |
| --- | --- | --- |
| AI가 처음입니다. | [역전파](딥러닝_deep-learning/backprop.md) → [ResNet](딥러닝_deep-learning/resnet.md) → [LayerNorm](딥러닝_deep-learning/layer-normalization.md) → [Transformer](Transformer의계산_ATTENTION.md) | 오차로 무엇을 바꾸고, 각 층은 어떤 계산을 합니까? |
| Transformer 이후가 궁금합니다. | [Transformer](Transformer의계산_ATTENTION.md) → [BERT](딥러닝_deep-learning/bert.md)·[GPT-3](언어와멀티모달_language-multimodal/gpt3.md) → [CLIP](언어와멀티모달_language-multimodal/clip.md)·[LoRA](언어와멀티모달_language-multimodal/lora.md) | 구조가 이어져도 학습 목표와 적응 방식은 어떻게 달라집니까? |
| 컴퓨터와 서비스의 원리를 읽고 싶습니다. | [계산·데이터·네트워크와 분산 시스템](컴퓨팅과시스템_computing-systems/README.md) | 어떤 일을 계산할 수 있으며 데이터와 실패를 어떻게 다룹니까? |
| 회로·통신·성능이 궁금합니다. | [정보·소자·신호·프로세서](정보와전자공학_information-electronics/README.md) | 정보량, 소자 크기, 계산량과 실행시간은 어떻게 연결됩니까? |

처음부터 논문의 모든 식을 외우실 필요는 없습니다. ‘어떤 문제를 해결하려 했습니까?’, ‘기존 방법에서 무엇을 바꾸었습니까?’, ‘그 변화가 왜 작동합니까?’를 자기 말로 설명한 뒤 예제를 계산합니다. 마지막에는 논문이 평가한 조건과 아직 알 수 없는 부분을 확인합니다. 각 해설 끝의 자기 점검을 답 상자를 닫고 풀어보시면 됩니다.

## 정보이론·전자공학·프로세서의 기초 7편

[논문별 해설과 원문](정보와전자공학_information-electronics/README.md)

Shannon의 정보이론, Bardeen·Brattain의 트랜지스터, Moore의 집적 전망, Cooley·Tukey의 FFT, Amdahl의 병렬화 한계, Dennard의 MOSFET 축소, Patterson·Ditzel의 RISC를 다룹니다. 물리 소자를 작게 만드는 일, 알고리즘의 연산 수를 줄이는 일, 시스템 전체의 시간을 줄이는 일을 같은 ‘성능 향상’으로 합치지 않습니다.

## 컴퓨팅·데이터·네트워크와 분산 시스템 8편

[논문별 해설과 원문](컴퓨팅과시스템_computing-systems/README.md)

Turing의 계산 모형, Codd의 관계 모형, Cerf·Kahn의 통신망 연결, Diffie·Hellman의 키 합의, Lamport의 논리 시계, GFS, MapReduce, Dynamo를 읽습니다. 각 글에는 직접 만든 전이표·관계 연산·메시지 흐름·버전 비교가 있어 주장과 작동 과정을 연결하실 수 있습니다.

## 신경망의 학습·표현·생성 11편

[논문별 해설과 원문](딥러닝_deep-learning/README.md)

역전파, LeNet, AlexNet, VAE, GAN, Bahdanau attention, BatchNorm, ResNet, LayerNorm, BERT, DDPM을 다룹니다. ‘학습’과 ‘생성’을 나누고, 정규화의 통계 축, 잔차의 의미, 표현과 확률분포의 차이를 작은 계산으로 확인합니다.

## Transformer와 문맥·이미지·언어의 연결 4편

[언어·멀티모달 논문을 읽는 순서](언어와멀티모달_language-multimodal/README.md)

| 논문 | 한국어 해설에서 직접 해볼 일 |
| --- | --- |
| [Attention Is All You Need](Transformer의계산_ATTENTION.md), 2017 | Q·K·V 두 토큰의 비율과 출력, 미래 마스크, 입력 길이와 비교 칸 수를 계산합니다. |
| [Language Models are Few-Shot Learners](언어와멀티모달_language-multimodal/gpt3.md), 2020 | 문맥에 예시를 주는 방식과 가중치 갱신을 구분하고 조건부 확률을 계산합니다. |
| [CLIP](언어와멀티모달_language-multimodal/clip.md), 2021 | 이미지·설명 두 쌍의 유사도와 양방향 비교를 확인합니다. |
| [LoRA](언어와멀티모달_language-multimodal/lora.md), 2021 공개·2022 발표 | 작은 행렬 두 개로 변화량을 표현하고 병합 계산·학습 변수 수를 대조합니다. |

## 논문을 선정한 기준

후속 연구에서 다시 사용한 개념, 공개 교육과정에서 다루는 내용, 실제 시스템 설계로 이어진 영향을 기준으로 읽을 논문을 골랐습니다. 예를 들어 [Stanford CS231n 2025 강의 일정](https://cs231n.stanford.edu/2025/schedule.html)은 역전파·AlexNet·ResNet·BatchNorm·attention을 연결하고, [MIT 분산 시스템의 논문 질문](https://pdos.csail.mit.edu/6.824/questions.html)은 GFS와 MapReduce 등의 설계 조건을 검토합니다. 개별 글에서는 해당 논문의 원문과 확인 가능한 후속 논문·명세를 연결합니다.

발표 시점과 사전 공개 시점이 다른 글은 두 연도를 함께 적었습니다. 인용 횟수는 집계 시점과 데이터베이스에 따라 달라지므로 여기의 배열을 인용 순위로 읽지는 않습니다. 이 30편은 정보·컴퓨팅·공학·AI의 여러 출발점을 함께 공부하기 위한 선정 범위입니다.

## 모델별 분석과 재현 사례

| 글 | 확인할 내용 |
| --- | --- |
| [Tiny Recursive Models](../AI모델실험_model-lab/samsung-trm/README.md) | 반복 구조, 실제 논문의 과제, 교육용 계산의 범위 |
| [DeepSeek-R1과 증류](../AI모델실험_model-lab/deepseek-r1-distill/README.md) | 원 모델의 학습과 증류 모델의 학습 목표 |
| [부분곱 제거의 주장과 재현 범위](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/부분곱실험의주장과근거_partial-product-reproduction-case.md) | 산술 오차·모델 정확도·회로 전력을 나누어 검토하는 사례 |

[논문·코드·특허 읽기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md) · [쌍체 비교와 재현 실험](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md) · [참여 연구 기록](../연구_research/README.md)

## English

Thirty selected papers span information theory, electronics, computing, distributed systems and deep learning. Korean studies explain terminology, mechanisms, worked examples, evidence and limitations, with self-check questions. Original claims and locally constructed calculations are identified separately. Publication and preprint dates are distinguished; the sequence is a reading selection rather than a citation ranking.

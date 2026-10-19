# 논문 해설 | Paper studies

계산 이론·정보·전자소자·컴퓨터 시스템·AI부터 뇌신경·생명공학·의약품·신소재·우주 탐사와 사회 데이터 연구까지 논문 138편을 한국어로 읽습니다. 기존 30편에 서로 다른 논문 108편의 해설을 더했습니다. 처음 등장하는 전문 용어의 뜻과 뉘앙스를 풀고, 작은 숫자나 직접 만든 사례로 방법을 따라갑니다. 원 논문이 제시한 근거와 이 저장소의 예제·계산은 본문에서 구분합니다.

## 분야별 목록

| 분야 | 논문 수 | 읽을 내용 |
|---|---:|---|
| [정보·전자공학·프로세서](정보와전자공학_information-electronics/README.md) | 7 | 정보량, 트랜지스터, FFT, 병렬화와 집적 |
| [컴퓨팅과 분산 시스템의 기초](컴퓨팅과시스템_computing-systems/README.md) | 8 | 계산 모형, 관계형 데이터, 통신망과 분산 저장 |
| [알고리즘·보안·운영체제와 시스템](알고리즘과컴퓨터시스템_algorithms-systems/README.md) | 30 | 탐색과 복잡도, 암호, 합의, 커널 검증, 최근 GPU·메모리 연구 |
| [신경망의 기초](딥러닝_deep-learning/README.md) | 11 | 역전파, 합성곱, 정규화, 잔차, 확률 생성 |
| [머신러닝과 생성 모델](머신러닝과생성모델_machine-learning/README.md) | 30 | SVM부터 강화학습·3D·단백질·효율적인 언어·멀티모달 모델 |
| [Transformer](Transformer의계산_ATTENTION.md)와 [언어·멀티모달](언어와멀티모달_language-multimodal/README.md) | 4 | attention, 문맥 학습, 이미지·문장 연결, 저비용 적응 |
| [뇌와 신경공학](뇌와신경공학_neuroengineering/README.md) | 25 | 뉴런, 기억·공간, 연결지도, 초파리 모형, BCI와 유전체 |
| [반도체와 소재](반도체와소재_semiconductors-materials/README.md) | 9 | FinFET, 원자층 재료, 메모리 물리, 재료 탐색·합성, 태양전지 |
| [우주 탐사와 정밀 관측](우주와관측_space-observation/README.md) | 6 | 상태 추정, 화성 비행, 소행성 충돌, 광통신, JWST와 LIGO |
| [의약품과 대사 연구](의약품과대사_metabolic-medicine/README.md) | 2 | STEP 1·SURMOUNT-1의 설계, 감량 효과, 결측·중단·이상사건 |
| [게임·생물·사회 데이터를 활용한 연구](뜻밖의연결_interdisciplinary/README.md) | 6 | WoW와 감염병, Foldit과 단백질, 점균과 연결망, 검색과 독감, 음악과 사회적 영향 |

각 분야 목록의 모든 논문은 별도의 본문으로 연결됩니다. 관련 모델 카드와 외부 자료는 논문 138편 수에 더하지 않았습니다. 같은 연구의 사전논문과 심사 후 논문도 두 편으로 중복 계산하지 않습니다.

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

## 뇌 회로·초파리와 신경 인터페이스

[뇌와 신경공학 25편](뇌와신경공학_neuroengineering/README.md)은 논리 뉴런·막전위에서 연결지도와 음성 BCI, AlphaGenome까지 이어집니다. 구조를 모두 그렸다는 말, 일부 회로 기능을 예측했다는 말, 몸의 움직임을 모사했다는 말의 차이를 각 논문의 검증 범위로 설명합니다. 뇌의 모든 기능이나 의식을 복제했다는 표현으로 합치지 않습니다.

## 재료·반도체에서 장치와 제조로

[반도체와 소재 9편](반도체와소재_semiconductors-materials/README.md)에서는 단일 소자의 성능, 웨이퍼 수율, 계산으로 찾은 결정, 로봇이 합성한 물질, 외부 인증 태양전지를 구별합니다. A-Lab은 2026년 정정된 본문과 수치를 함께 읽습니다.

## 약물 효과와 뜻밖의 연구 재료

[의약품과 대사 연구](의약품과대사_metabolic-medicine/README.md)는 위고비·마운자로와 연결되는 두 대표 임상 논문을 읽습니다. 평균 감량, 개인의 결과, 관찰한 참여자와 무작위 배정 전체, 치료 중단과 결측 처리의 차이를 자체 계산으로 확인합니다. 작용 원리·발견 경위와 현재 상품의 허가는 [의약품·생명공학 리뷰](../제품리뷰_reviews/의약품과생명공학_biomedical/README.md)에서 이어집니다.

[게임·생물·사회 데이터를 활용한 연구](뜻밖의연결_interdisciplinary/README.md)는 연구 재료를 새롭게 고른 사례 여섯 편입니다. WoW의 감염 사건에 대한 제안, Foldit 참가자의 구조 탐색, 점균의 적응 연결망은 무엇을 검증했는지 나누어 읽습니다. Google Flu의 가능성과 후속 실패 분석을 함께 다루며, 음악시장 실험에서는 사회적 영향과 예측 불가능성을 살펴봅니다. 착상의 흥미와 실제 유용성의 근거를 구별합니다.

## 우주 탐사·관측을 가능하게 하는 공학

[우주·관측 6편](우주와관측_space-observation/README.md)은 칼만 필터의 불확실성 계산과 자율 항법, 검출기·광학·통계를 연결합니다. 당시의 개발 계획과 이후 실제 임무 결과를 섞지 않고, 논문에서 확인한 시점과 조건을 적었습니다.

## 최근 연구를 읽는 경로

[머신러닝·생성 모델](머신러닝과생성모델_machine-learning/README.md)에서는 AlphaFold 3, Mamba-2, Titans, DeepSeek-V3.2, Qwen3·Qwen3.5-Omni를 읽습니다. [시스템](알고리즘과컴퓨터시스템_algorithms-systems/README.md)에서는 Harmonic, Rex, PageFlex, KPerfIR, Soar·Alto를 읽습니다. [신경공학](뇌와신경공학_neuroengineering/README.md)의 초파리·음성 합성·유전체 연구와 [최근 소재 연구](반도체와소재_semiconductors-materials/README.md)도 연결됩니다.

최근이라는 이유로 장래의 영향이나 모든 비교 우위를 확정하지 않습니다. 기술 보고서·사전논문·심사 논문·정정본의 상태를 나누고, 결과가 나온 입력·장비·과제와 한계를 먼저 확인합니다.

## 논문을 선정한 기준

후속 연구에서 다시 사용한 개념, 공개 교육과정에서 다루는 내용, 실제 시스템 설계로 이어진 영향을 기준으로 읽을 논문을 골랐습니다. 예를 들어 [Stanford CS231n 2025 강의 일정](https://cs231n.stanford.edu/2025/schedule.html)은 역전파·AlexNet·ResNet·BatchNorm·attention을 연결하고, [MIT 분산 시스템의 논문 질문](https://pdos.csail.mit.edu/6.824/questions.html)은 GFS와 MapReduce 등의 설계 조건을 검토합니다. 개별 글에서는 해당 논문의 원문과 확인 가능한 후속 논문·명세를 연결합니다.

발표 시점과 사전 공개 시점이 다른 글은 두 연도를 함께 적었습니다. 인용 횟수는 집계 시점과 데이터베이스에 따라 달라지므로 여기의 배열을 인용 순위로 읽지는 않습니다. 2026-10-20에 확인한 이 138편은 여러 분야의 출발점과 최근 연구를 연결하기 위한 선정 범위입니다. 세계의 중요 논문 전체를 빠짐없이 모았다는 목록은 아닙니다. 소속 기관의 명성도 결과의 정확성이나 미래 영향력을 보장하지는 않습니다.

## 모델별 분석과 재현 사례

| 글 | 확인할 내용 |
| --- | --- |
| [Tiny Recursive Models](../AI모델실험_model-lab/samsung-trm/README.md) | 반복 구조, 실제 논문의 과제, 교육용 계산의 범위 |
| [DeepSeek-R1과 증류](../AI모델실험_model-lab/deepseek-r1-distill/README.md) | 원 모델의 학습과 증류 모델의 학습 목표 |
| [부분곱 제거의 주장과 재현 범위](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/부분곱실험의주장과근거_partial-product-reproduction-case.md) | 산술 오차·모델 정확도·회로 전력을 나누어 검토하는 사례 |

[논문·코드·특허 읽기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md) · [쌍체 비교와 재현 실험](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md) · [참여 연구 기록](../연구_research/README.md)

## English

One hundred and thirty-eight distinct papers span information theory, electronics, computer systems, AI, neuroscience, metabolic medicine, materials, space engineering and interdisciplinary studies using games, organisms and social data. One hundred and eight studies were added to the earlier thirty; preprints and later publications of the same work are counted once. Korean studies explain terminology, mechanisms, worked examples, evidence and limitations, with self-check questions. Original claims and locally constructed calculations are identified separately. Publication and preprint dates are distinguished; the sequence is a reading selection rather than a citation ranking.

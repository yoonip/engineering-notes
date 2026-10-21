# AI 모델과 수치 실험 | AI models and numerical experiments

공식 모델의 구조·학습·입출력 설명과 직접 실행한 교육용 계산을 구분해서 정리합니다. 모델을 설명한 글은 `models`, 기존 CPU 코드와 결과는 `experiments`에 있습니다.

| 읽을 내용 | 위치와 범위 |
| --- | --- |
| 공개 모델의 구조와 학습 | [모델별 문서](models/README.md)에서 원개발자·기반 모델·선택한 배포물과 출처를 함께 읽으실 수 있습니다. |
| 상용 모델의 API | [Claude Sonnet 5.5](models/anthropic.md)와 [Nova Micro v1](models/amazon.md)에서 공개된 입출력 계약과 비공개 내부 구조를 구분합니다. |
| 재귀 추론 연구 | [Samsung SAIL Montréal TRM](models/samsung-trm/README.md)은 답·잠재 상태의 반복과 gradient 경계를 다룹니다. |
| 생성 풀이를 배우는 학생 모델 | [DeepSeek R1-Distill](models/deepseek-r1-distill/README.md)은 R1 원본과 Qwen 기반 학생의 차이를 다룹니다. |
| 배열 계산 도구 | [Apple MLX](models/apple.md)는 가중치 모델과 구분한 framework 문서입니다. |
| 실행 전 평가 설계 | [평가 입력과 판정 기준](experiments/평가입력과판정기준_evaluation-design.md)은 자체 질문·정답표이며 모델 실행 결과가 아닙니다. |
| 직접 실행한 계산 | [CPU 수치 실험](experiments/README.md)에 코드·기존 결과·검사 범위가 있습니다. |
| 기관·플랫폼·모델의 관계 | [개발자와 배포 경로](PROVIDERS.md)에서 회사·기반 모델·Hub·API·runtime을 구분합니다. |

## 설명과 실행 결과를 읽는 기준

모델별 문서는 2026-10-21에 각 글이 다루는 배포물의 공식 카드·설정·코드를 다시 확인했습니다. 해당 배포물이 현재 최신이라는 의미는 아닙니다. 공개 가중치·코드의 존재와 동일 학습을 재현하는 데 필요한 모든 자료의 공개 여부도 다릅니다.

실행 기록은 Python 표준 라이브러리를 이용한 메모리 산술, 스칼라 반복식, 작은 교사·학생 학습, 균등 양자화입니다. 공식 가중치 추론·유료 API 호출·GPU 속도 측정·공식 벤치마크 재현은 수행하지 않았습니다. 자체 질문과 정답표는 별도 평가 설계 문서에 있으며 실행 결과와 구분합니다.

공식 자료에서 확인되지 않은 상용 모델의 층 수·가중치 구조·학습 자료를 다른 모델이나 작은 실험으로 대신 설명하지 않습니다. 모델 ID·revision·tokenizer·대화 형식·자료형·입출력 예산은 실제 실행을 비교할 때 별도로 고정해야 합니다.

## 관련 학습 자료

- [모델의 구성과 실행 방식](../분야_topics/26-AI모델-API_open-model-lab/README.md)은 tokenizer·가중치·runtime의 역할을 설명합니다.
- [학습·미세조정·경량화](../분야_topics/45-AI학습최적화_ai-training-optimization/README.md)는 가중치와 구조를 바꾸는 과정을 설명합니다.
- [응용·RAG·에이전트·평가](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/README.md)는 모델을 프로그램에 연결하는 과정을 다룹니다.

## English

Model notes under `models` explain a specific release using official cards, configuration files, code or API documentation. They separate authors, base-model lineage, distribution platforms and runtimes. The existing offline numerical code and results remain under `experiments`. They do not reproduce released model training, weight inference, commercial APIs or official benchmarks. Private commercial architectures are left unspecified when the cited public documents do not establish them.

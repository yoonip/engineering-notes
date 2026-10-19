# AI 모델 분석과 실험 | AI model analysis and experiments

모델 구조와 배포 조건을 읽고, 직접 실행한 계산을 함께 정리합니다. [29개 기관의 모델·도구 분석](models/README.md)에서는 공급사마다 구체적 배포물을 선택했습니다. 각 분석에서는 원개발 기관, 기반 모델, 배포 서비스와 실행 도구의 관계를 구분합니다.

## 먼저 읽을 글

| 글 | 확인할 내용 |
|---|---|
| [삼성 TRM의 반복 구조](samsung-trm/README.md) | 상태 갱신·공유 파라미터·gradient·중단 판정과 코드의 대응 |
| [DeepSeek R1-Distill의 기반 구조](deepseek-r1-distill/README.md) | 원본 R1과 Qwen 기반 학생 모델, 가중치·KV 캐시 계산 |
| [모델·도구별 분석 29편](models/README.md) | OpenAI·Google·Microsoft·Meta·Anthropic·국내외 모델과 실행 도구 |
| [CPU 수치 실험과 결과](experiments/README.md) | 메모리 계산·반복식·교사/학생 학습·양자화의 실제 실행값 |
| [기관과 모델을 구분하는 방법](PROVIDERS.md) | 원저작자·기반 모델·배포 서비스·실행 도구의 관계 |

## 분석과 실험의 범위

공식 모델 카드·코드·설정 파일을 2026-10-19에 확인했습니다. 문서의 ‘재현 방법’은 각 배포물을 실행할 때 필요한 조건과 평가 방법입니다. 실제로 실행한 것은 Python 표준 라이브러리 기반의 네 가지 수치 실험입니다. 공식 모델 가중치를 내려받거나 유료 API를 호출하지 않았으므로 생성 품질·GPU 속도·공식 벤치마크 재현 결과를 주장하지 않습니다.

메모리 추정값, 자체 예제의 학습 결과, 공식 문서가 보고한 성능은 표와 본문에서 구분합니다. 실험 조건이 바뀌면 모델 이름만 같아도 같은 결과를 기대하기 어렵습니다. 모델 ID와 revision, tokenizer, chat template, 자료형, 입력과 출력 예산이 비교의 기본 단위입니다.

## 관련 학습 자료

- [모델의 구성과 실행 방식](../분야_topics/26-AI모델-API_open-model-lab/README.md)을 통해 tokenizer·가중치·runtime의 역할을 살펴보실 수 있습니다.
- [학습·미세조정·경량화](../분야_topics/45-AI학습최적화_ai-training-optimization/README.md)에서는 모델을 바꾸는 과정을 다룹니다.
- [응용·RAG·에이전트·평가](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/README.md)에서는 모델을 프로그램에 연결하는 과정을 다룹니다.

## English

This section pairs source-based model analyses with executed offline numerical experiments. The 29 institution notes distinguish model authors, base-model lineages, hosted APIs, and runtimes. Only the linked four CPU experiments were run locally; no released weights, paid APIs, GPU benchmarks, or official benchmark reproductions were executed.

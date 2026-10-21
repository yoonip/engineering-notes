# 기관·기반 모델·실행 도구의 관계 | Authors, models, and runtimes

회사 이름 하나로 모델의 구조·가중치 사용 조건·실행 환경을 모두 설명할 수는 없습니다. 다음 관계를 나누어 보시면 공개 모델과 서비스의 관계를 파악하기 쉽습니다.

| 구분 | 의미 | 실제 사례 |
|---|---|---|
| 개발·배포 기관 | 모델이나 코드를 연구·학습·배포한 기관입니다. | Samsung SAIL Montréal의 TRM, NCSOFT의 VARCO가 있습니다. |
| 기반 모델 | 추가 학습을 시작한 원래 모델입니다. | R1-Distill-Qwen-1.5B는 Qwen2.5-Math-1.5B에서 출발합니다. |
| 배포 서비스 | 모델을 API 등으로 제공하는 서비스입니다. | Amazon Bedrock에서 제공하는 모델과 그 모델의 원개발자는 다를 수 있습니다. |
| 플랫폼 | 여러 기관의 가중치·자료·실행물을 배포하는 공간입니다. | Hugging Face Hub는 타 기관 모델도 호스팅하며 SmolLM2의 개발 주체와 구별합니다. |
| 실행 도구 | 모델을 로딩하고 계산하는 프로그램입니다. | Transformers·vLLM·MLX는 모델 가중치 자체와 역할이 다릅니다. |

예를 들어 [NCSOFT Llama VARCO](models/ncsoft.md)는 NCSOFT가 조정한 배포물이면서 Meta의 Llama 3.1 계보를 사용합니다. [DeepSeek R1-Distill](models/deepseek-r1-distill/README.md)은 R1이 만든 데이터를 학습하지만 학생의 구조는 Qwen 또는 Llama 계열입니다. 이 관계는 회사가 다른 회사에 포함된다는 뜻이 아닙니다.

## 모델 분석으로 이동하기

[모델·실행 도구 목록](models/README.md)은 기관과 구체적인 배포물을 나란히 표시합니다. 삼성 TRM 문서에서는 삼성 연구 코드만 다루며, Microsoft·Google·Meta 등 다른 기관은 각각 독립 문서로 연결합니다.

| 분류 | 분석 대상 |
|---|---|
| 공개 언어·추론 모델 | [OpenAI](models/openai.md), [Google](models/google.md), [Microsoft](models/microsoft.md), [Meta](models/meta.md), [DeepSeek](models/deepseek-r1-distill/README.md), [Qwen](models/qwen.md), [Mistral](models/mistral.md), [IBM](models/ibm.md), [NVIDIA](models/nvidia.md), [Cohere](models/cohere.md), [xAI](models/xai.md), [Baidu](models/baidu.md), [Z.ai](models/zai.md), [Moonshot](models/moonshot.md), [Hugging Face](models/huggingface.md)입니다. |
| 국내 공개 언어 모델 | [LG AI Research](models/lg.md), [NAVER](models/naver.md), [Kakao](models/kakao.md), [Upstage](models/upstage.md), [SK Telecom](models/skt.md), [KT](models/kt.md), [NCSOFT](models/ncsoft.md)입니다. |
| 퍼즐 추론 연구 | [Samsung SAIL Montréal TRM](models/samsung-trm/README.md)입니다. |
| Hosted API | [Anthropic Claude](models/anthropic.md), [Amazon Nova](models/amazon.md)입니다. 공개 가중치를 함께 제공하는 다른 기관도 서비스 API를 운영할 수 있습니다. |
| 이미지·영상 생성 | [Stability AI](models/stability.md), [Black Forest Labs](models/bfl.md), [Tencent](models/tencent.md)입니다. |
| 실행 framework | [Apple MLX](models/apple.md)입니다. |

## 비교할 때 남기는 기록

‘모델이 좋다’는 판단에는 작업과 조건이 필요합니다. 문서 요약에는 사실 보존·누락·근거 없는 추가를, 코드에는 실행 결과와 테스트를, 도구 호출에는 선택·인자·결과 반영을 기록합니다. 같은 prompt라도 tokenizer와 template이 다르면 토큰 수와 입력 형식이 달라집니다.

공개 가중치라는 표현은 모든 사용 조건이 같다는 뜻이 아닙니다. 모델별 라이선스 이름은 개별 분석 문서에 공식 원문과 연결했습니다. 실제 사용에서는 선택한 배포물의 revision과 적용 조건을 함께 확인합니다.

## English

Authorship, base-model lineage, distribution service, and runtime are separate relationships. The model index gives every institution its own entry; a Qwen-based DeepSeek checkpoint does not place Qwen under DeepSeek as a company. Evaluation records should specify the task, release, tokenizer, template, runtime, and generation budget.

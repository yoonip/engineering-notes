# 모델별 구조·학습·실행 조건 | Model architecture, training and execution

각 문서는 실제 배포물의 개발자·기반 계보·구조·학습 설명·실행 조건을 다룹니다. 공식 자료 재확인일은 2026-10-21입니다. 대상 버전은 표의 모델 식별자로 구분하며, 이 목록은 성능 순위표가 아닙니다.

공개 가중치 모델, 비공개 상용 API, 퍼즐 추론 연구, 이미지·영상 생성 모델을 다룹니다. 배열 연산·학습·추론을 수행하는 [실행 프레임워크](../frameworks/README.md)는 별도로 정리했습니다. Hugging Face는 Hub 플랫폼을 운영하는 동시에 SmolLM2도 개발합니다. 모든 Hub 배포물이 Hugging Face의 자체 모델이라는 뜻은 아닙니다.

실제 로컬 실행은 [별도 CPU 수치 실험](../experiments/README.md)에 있습니다. 아래 모델의 가중치·유료 API·공식 학습은 실행하지 않았습니다. [자체 질문과 판정표](../experiments/평가입력과판정기준_evaluation-design.md)는 공식 모델 설명과 구분한 평가 설계입니다. [기관과 배포 경로의 구분](../PROVIDERS.md)을 함께 읽으시면 됩니다.

| 개발자·기관 | 분석 대상 | 구조·학습·실행의 구분 |
|---|---|---|
| OpenAI | [gpt-oss-20b](openai.md) | 전체·활성 파라미터, MXFP4, Harmony |
| Google DeepMind | [Gemma 3 1B](google.md) | Gemini 서비스와 공개 Gemma, 크기별 입력 범위 |
| Microsoft | [Phi-4-mini-instruct](microsoft.md) | 소형 모델의 합성 데이터와 실행 커널 |
| Meta | [Llama 3.2 1B Instruct](meta.md) | GQA, 한국어 평가, 라이선스 |
| Anthropic | [Claude Sonnet 5.5](anthropic.md) | API 계약과 출력 블록, 실행하지 않은 비교 |
| Samsung SAIL Montréal | [TRM](samsung-trm/README.md) | 답·잠재 상태 갱신과 반복 계산 |
| DeepSeek | [R1-Distill-Qwen-1.5B](deepseek-r1-distill/README.md) | 원본 R1과 기반 구조, KV 캐시 |
| Alibaba / Qwen | [Qwen3-0.6B](qwen.md) | thinking 설정과 KV 헤드 |
| Mistral AI | [Ministral 8B 2410](mistral.md) | interleaved attention과 실행 지원 범위 |
| IBM | [Granite 3.3 2B](ibm.md) | 근거 기반 응답과 추론 출력 형식 |
| NVIDIA | [Nemotron Nano 9B v2](nvidia.md) | Mamba2·Transformer 혼합 구조 |
| Amazon / AWS | [Nova Micro v1](amazon.md) | Bedrock 배포와 텍스트 입력 범위 |
| Cohere Labs | [Aya Expanse 8B](cohere.md) | 다국어 평가와 비상업 라이선스 |
| xAI | [Grok-1](xai.md) | 공개 MoE와 서비스 모델의 차이 |
| Baidu | [ERNIE 4.5 0.3B PT](baidu.md) | 작은 dense 모델과 Paddle·PT 포맷 |
| Tencent | [HunyuanVideo](tencent.md) | 해상도·프레임 수·GPU 메모리 |
| Z.ai | [GLM-4.5-Air](zai.md) | 총 106B·활성 12B, hybrid reasoning |
| Moonshot AI | [Kimi-K2-Instruct](moonshot.md) | 총 1T·활성 32B, 도구 호출 상태 |
| Stability AI | [SD 3.5 Medium](stability.md) | MMDiT-X·텍스트 인코더·VAE |
| Black Forest Labs | [FLUX.1-schnell](bfl.md) | 1~4 생성 step과 이미지 비교 조건 |
| Hugging Face | [SmolLM2 135M Instruct](huggingface.md) | 소형 모델 학습과 언어 범위 |
| LG AI Research | [EXAONE 4.0 1.2B](lg.md) | 크기별 구조, 추론 모드 |
| NAVER | [HyperCLOVAX SEED 1.5B](naver.md) | 한국어 문화 지식과 16k 문맥 |
| Kakao | [Kanana 1.5 2.1B](kakao.md) | 기본 32k와 YaRN 확장 |
| Upstage | [SOLAR 10.7B Instruct v1](upstage.md) | Depth Up-Scaling과 단일 대화 |
| SK Telecom | [A.X 4.0 Light](skt.md) | Qwen 기반 추가 학습과 Light의 한도 |
| KT | [Mi:dm 2.0 Mini](kt.md) | pruning·distillation과 한국어 응답 |
| NCSOFT | [Llama VARCO 8B](ncsoft.md) | Llama 기반 한국어 조정과 출처 조건 |

## English

Each note examines a specific release, its source-supported architecture, training description, inference conditions and limits of public disclosure. Execution frameworks have a separate index. Only the linked offline numerical experiments were executed locally; no listed model weights or paid APIs were run.

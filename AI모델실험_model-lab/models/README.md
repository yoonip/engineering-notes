# 모델과 실행 도구 분석 | Models and runtimes

기관마다 실제 배포물 하나를 골라 구조·입출력·사용 조건·재현 방법을 정리했습니다. 2026-10-19에 공식 자료를 확인했으며, 각 회사의 전체 제품이나 최신 모델을 대표하는 순위표는 아닙니다. 공개 모델의 파라미터 수와 서비스 API의 기능, 실행 도구의 역할을 구분했습니다.

각 문서의 ‘재현 방법’은 해당 모델을 실행할 때 확인할 절차입니다. 이 저장소에서 실행한 것은 [네 가지 CPU 수치 실험](../experiments/README.md)이며, 아래 배포물의 가중치 추론과 유료 API 호출은 수행하지 않았습니다.

| 기관 | 분석 대상 | 핵심 비교 |
|---|---|---|
| OpenAI | [gpt-oss-20b](openai.md) | 전체·활성 파라미터, MXFP4, Harmony |
| Google DeepMind | [Gemma 3 1B](google.md) | Gemini 서비스와 공개 Gemma, 크기별 입력 범위 |
| Microsoft | [Phi-4-mini-instruct](microsoft.md) | 소형 모델의 합성 데이터와 실행 커널 |
| Meta | [Llama 3.2 1B Instruct](meta.md) | GQA, 한국어 평가, 라이선스 |
| Anthropic | [Claude Sonnet 5.5](anthropic.md) | API 계약과 출력 블록, 실행하지 않은 비교 |
| Samsung SAIL Montréal | [TRM](../samsung-trm/README.md) | 답·잠재 상태 갱신과 반복 계산 |
| DeepSeek | [R1-Distill-Qwen-1.5B](../deepseek-r1-distill/README.md) | 원본 R1과 기반 구조, KV 캐시 |
| Alibaba / Qwen | [Qwen3-0.6B](qwen.md) | thinking 설정과 KV 헤드 |
| Mistral AI | [Ministral 8B 2410](mistral.md) | interleaved attention과 실행 지원 범위 |
| IBM | [Granite 3.3 2B](ibm.md) | 근거 기반 응답과 추론 출력 형식 |
| NVIDIA | [Nemotron Nano 9B v2](nvidia.md) | Mamba2·Transformer 혼합 구조 |
| Apple | [MLX](apple.md) | 모델과 배열 연산 도구, 지연 실행 |
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

Each note examines a concrete release, its architecture or API interface, distribution terms, reproduction route, and limitations. These are source-based analyses, not a leaderboard. Apple MLX is listed as a runtime, not a model. Only the linked offline numerical experiments were executed locally; no listed model weights or paid APIs were run.

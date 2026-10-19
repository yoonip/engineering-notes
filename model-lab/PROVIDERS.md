# AI 기업과 모델

언어·코드·이미지·음성·영상 모델과 실행 도구를 기업·생태계별로 정리했다. 공개 가중치 모델과 hosted API는 제공 방식과 수정 범위가 다르다.

## OpenAI

GPT 계열은 텍스트·이미지 등 입력을 처리하는 API 모델 생태계이고, gpt-oss는 내려받아 실행할 수 있는 공개 가중치 모델 계열이다. Hosted API 활용과 로컬 추론은 실행 환경과 수정 범위가 다르다. 도구 호출, 구조화된 출력, 추론 runtime의 차이를 함께 다룬다.

- [공식 자료 1](https://developers.openai.com/learn/gpt-oss)
- [공식 자료 2](https://developers.openai.com/api/docs/models)

## Google / DeepMind

Gemini는 Google의 생성형 AI 모델·API 생태계다. Gemma는 직접 실행하고 조정할 수 있는 공개 가중치 계열이며, 언어·시각 입력 등 지원 범위는 모델별로 다르다. 두 계열은 이름뿐 아니라 제공 방식과 실행 도구도 구분된다.

- [공식 자료 1](https://ai.google.dev/gemini-api/docs)
- [공식 자료 2](https://ai.google.dev/gemma)

## Microsoft

Phi는 비교적 작은 언어 모델을 중심으로 한 Microsoft의 모델 계열이다. PhiCookBook은 로컬 실행·미세조정·배포를 연결하는 공식 예제를 제공한다. 소형 모델의 추론 자원과 양자화·장치 배포를 살펴보는 사례다.

- [공식 자료](https://github.com/microsoft/PhiCookBook)

## Meta

Llama는 Meta의 공개 가중치 언어 모델 계열이다. 모델 버전별로 크기·입력 형식·라이선스가 다르다. Meta의 연구 저장소에는 언어 외에 비전·표현 학습 관련 프로젝트도 있으며, 모델 구조와 학습 방법을 코드와 함께 읽을 수 있다.

- [공식 자료 1](https://github.com/meta-llama/llama-models)
- [공식 자료 2](https://github.com/facebookresearch)

## Anthropic

Claude는 API 기반의 언어·멀티모달 모델 생태계다. 긴 문서 처리, 코드, 도구 사용을 애플리케이션과 연결할 수 있다. API의 메시지·도구 인터페이스를 사용하는 작업과 모델 가중치 자체를 수정하는 작업은 구분된다.

- [공식 자료](https://platform.claude.com/docs/en/intro)

## Samsung

Samsung SAIL Montréal의 Tiny Recursive Models는 작은 네트워크를 반복 적용해 답과 내부 표현을 갱신하는 추론 연구 코드다. 일반적인 대화형 LLM과 문제 구성·학습 방식이 다르다. 재귀 단계와 학습 구조가 핵심 분석 대상이며 [TRM 문서](samsung-trm/README.md)에 구조를 정리했다.

- [공식 자료](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)

## DeepSeek

DeepSeek는 언어·코드·추론 모델과 관련 코드를 공개하는 생태계다. R1은 추론 학습, V3는 대규모 언어 모델 구조, R1-Distill은 다른 기반 모델로 추론 능력을 전달한 사례와 연결된다. 원본 모델과 distill checkpoint는 구조와 자원 요구가 다르다.

- [공식 자료](https://github.com/deepseek-ai)

## Alibaba / Qwen

Qwen은 언어·코드·시각언어 등 여러 작업을 다루는 모델 계열이다. 모델별 tokenizer·대화 형식·입력 범위가 다르다. 공개 가중치 실행과 framework 통합, 다국어 처리, 모델 크기에 따른 자원 사용을 연결해 볼 수 있다.

- [공식 자료](https://github.com/QwenLM/Qwen3)

## Mistral AI

Mistral은 공개 가중치 모델과 hosted API를 함께 제공하는 생태계다. Dense·MoE 구조, 언어·코드·문서 처리 등 모델별 목적이 다르다. 같은 회사의 모델이라도 배포 방식과 사용 조건은 release별로 나뉜다.

- [공식 자료](https://docs.mistral.ai/)

## IBM

Granite는 IBM의 언어·코드·기업용 AI 활용과 관련된 모델 계열이다. 공개 model card와 코드에서 학습 목적·평가·사용 조건을 읽을 수 있다. 검색·문서 처리·작은 모델의 배포를 연결하는 사례가 된다.

- [공식 자료](https://github.com/ibm-granite/granite-language-models)

## NVIDIA

Nemotron은 언어·추론 모델, Cosmos는 물리 세계와 영상·시뮬레이션 응용에 관련된 모델 생태계다. GPU 추론 도구와 로봇·합성 데이터 흐름도 함께 연결된다. 모델 성능과 TensorRT 등 runtime 최적화의 영향을 나누어 분석할 수 있다.

- [공식 자료](https://huggingface.co/nvidia)

## Apple

MLX는 Apple silicon을 위한 배열 연산·머신러닝 framework이며 Core ML은 Apple 플랫폼의 모델 통합·실행 생태계다. 두 이름은 단일 언어 모델의 이름이 아니다. 공개 모델을 Apple 장치에 올릴 때 구조 변환과 메모리·실행 조건을 다루게 된다.

- [공식 자료](https://ml-explore.github.io/mlx/build/html/index.html)

## Amazon / AWS

Nova는 Amazon의 생성형 AI 모델 계열이며 AWS 서비스와 연결해 사용한다. 모델 API와 데이터·권한·응용 인프라를 함께 구성하는 흐름을 볼 수 있다. 서비스 사용료와 지연은 모델 추론뿐 아니라 호출·전송·작업량 조건과 연결된다.

- [공식 자료](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)

## Cohere

Command는 생성형 모델, Aya는 다국어 연구 모델, embedding·rerank는 검색 품질과 관련된 생태계다. 문서 검색에서는 생성 모델 외에 검색용 표현과 재정렬 모델도 결과를 크게 바꾼다. 공개 모델과 API의 제공 범위는 각각 다르다.

- [공식 자료](https://docs.cohere.com/)

## xAI

Grok은 xAI의 모델 계열이다. 공개된 Grok-1 저장소와 서비스 API에서 제공하는 모델을 동일한 배포물로 볼 수는 없다. 공개 release의 구조 분석과 API 응용은 서로 다른 실행 경로를 가진다.

- [공식 자료 1](https://github.com/xai-org/grok-1)
- [공식 자료 2](https://docs.x.ai/overview)

## Baidu

ERNIE는 Baidu의 언어·지식·멀티모달 모델 연구 생태계다. PaddlePaddle 도구와 연결되는 구현을 접할 수 있다. 중국어와 다국어 데이터, 모델 구조와 학습 framework의 결합을 살펴보는 사례다.

- [공식 자료](https://github.com/PaddlePaddle/ERNIE)

## Tencent

Hunyuan은 언어·이미지·영상·3D 등 여러 생성 모델 프로젝트를 포함한다. 작업마다 입력 데이터와 출력 표현, 추론 비용이 다르다. 텍스트 생성과 시각·공간 생성 모델의 실행 흐름을 구분해 읽을 수 있다.

- [공식 자료](https://github.com/Tencent-Hunyuan)

## Z.ai

GLM은 언어·추론·도구 활용 등과 관련된 모델 계열이다. 공개 저장소에서 모델 설명과 실행 예제를 제공한다. 대화 형식과 도구 인터페이스, 지원 runtime은 선택한 release의 문서와 연결된다.

- [공식 자료](https://github.com/zai-org/GLM-4.5)

## Moonshot AI

Kimi는 긴 문맥 처리와 추론·도구 활용에 관련된 모델 생태계다. Kimi-K2는 MoE 기반 공개 모델을 읽는 사례다. 전체 파라미터 수, token당 활성화되는 파라미터, 실제 가중치 저장량은 서로 다른 개념이다.

- [공식 자료](https://github.com/MoonshotAI/Kimi-K2)

## Stability AI

Stable Diffusion을 포함한 이미지·미디어 생성 모델 생태계다. 확산 과정, latent 표현, 텍스트 조건, sampler가 결과 생성에 관여한다. Prompt 변경과 fine-tuning·LoRA는 모델에 영향을 주는 단계가 다르다.

- [공식 자료](https://github.com/Stability-AI/generative-models)

## Black Forest Labs

FLUX는 텍스트 조건의 이미지 생성·편집과 연결되는 모델 계열이다. 언어 모델과 달리 이미지 표현, 생성 step, 해상도 조건이 메모리와 시간에 직접 영향을 준다. 코드와 모델 variant별 가중치 조건은 따로 구분된다.

- [공식 자료](https://github.com/black-forest-labs/flux)

## Hugging Face

Hugging Face는 모델·데이터셋 배포와 학습·추론 도구를 제공하는 플랫폼이다. Transformers·Datasets·Tokenizers·Safetensors 같은 도구와 SmolLM 계열 모델을 접할 수 있다. Hub에 있는 모델의 원저작자와 라이선스는 각 model card에 따른다.

- [공식 자료 1](https://huggingface.co/HuggingFaceTB)
- [공식 자료 2](https://huggingface.co/docs)

## LG AI Research

EXAONE은 LG AI Research의 언어·추론 모델 계열이다. 한국어·영어 문맥과 공개 checkpoint의 실행을 연결하는 국내 사례다. 공개 가중치의 사용 범위는 해당 release의 라이선스에 따라 달라진다.

- [공식 자료](https://github.com/LG-AI-EXAONE/EXAONE-4.0)

## NAVER

HyperCLOVA X는 NAVER의 한국어·다국어·멀티모달 AI 생태계다. 서비스형 활용과 공개된 모델 release가 나뉜다. 한국어 문체·전문 용어·문서 처리에서 입력과 평가 데이터의 영향을 살펴볼 수 있다.

- [공식 자료](https://huggingface.co/naver-hyperclovax)

## Kakao

Kanana는 Kakao의 언어 모델 생태계다. 공개 저장소에서 모델 구성·사용 예제·model card를 읽을 수 있다. 한국어 표현과 tokenizer, 대화 형식, 작은 모델의 활용 조건을 비교하는 사례다.

- [공식 자료](https://github.com/kakao/kanana)

## Upstage

Solar는 Upstage의 언어 모델 계열이다. 공개 checkpoint와 서비스 제공 방식은 모델별로 구분된다. 문서·한국어 응용과 언어 모델의 학습·추론 구성을 연결해 볼 수 있다.

- [공식 자료](https://huggingface.co/upstage)

## SK Telecom

A.X는 SK Telecom의 언어 모델 계열이다. 공개 model card에는 모델 목적과 실행·사용 조건이 담긴다. 한국어 응답과 다국어 처리, 추론 자원과 모델 배포의 관계를 다루는 국내 사례다.

- [공식 자료](https://huggingface.co/skt)

## KT

Midm은 KT의 한국어 중심 언어 모델 계열이다. 공개 배포물은 K-intelligence 계정에서 접할 수 있다. 한국어 데이터와 모델 크기, 학습·추론 환경을 함께 살펴볼 수 있다.

- [공식 자료](https://huggingface.co/K-intelligence)

## NCSoft

VARCO는 NCSOFT의 AI 모델 생태계다. 공개 모델은 언어·멀티모달 등 release별 목적을 갖는다. 모델 이름만으로 지원 입력과 언어·라이선스를 판단하지 않고 개별 model card의 범위를 기준으로 구분한다.

- [공식 자료](https://huggingface.co/NCSOFT)

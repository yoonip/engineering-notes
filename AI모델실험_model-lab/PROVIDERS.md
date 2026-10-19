# AI 기업과 모델

언어·코드·이미지·음성·영상 모델과 실행 도구를 기업·생태계별로 정리했다. 공개 가중치 모델과 hosted API의 제공 방식, 실행 환경과 수정 범위를 살펴본다.


Models and tools for language, code, images, speech, and video, organized by provider and ecosystem. The notes cover how open-weight models and hosted APIs are distributed, run, and modified.

## OpenAI

GPT 계열은 텍스트·이미지 등의 입력을 처리하는 API 모델이고, gpt-oss는 내려받아 실행할 수 있는 공개 가중치 모델 계열이다. Hosted API와 로컬 추론은 실행 환경과 수정 범위가 다르다. 도구 호출, 구조화된 출력과 추론 runtime도 함께 살펴본다.

The GPT family provides API models that process inputs such as text and images. gpt-oss is a family of downloadable open-weight models. Hosted APIs and local inference differ in execution environment and the changes they allow. Tool calling, structured outputs, and inference runtimes are also part of this comparison.

- [Official resources 1](https://developers.openai.com/learn/gpt-oss)
- [Official resources 2](https://developers.openai.com/api/docs/models)

## Google / DeepMind

Gemini는 Google의 생성형 AI 모델·API 생태계다. Gemma는 직접 실행하고 조정할 수 있는 공개 가중치 계열이며, 언어·시각 입력 등 지원 범위는 모델별로 다르다. 제공 방식과 실행 도구를 기준으로 두 계열을 살펴본다.

Gemini is Google's generative AI model and API ecosystem. Gemma provides open-weight models that can be run and adapted directly, with language and visual-input support varying by model. The two families are compared through their distribution methods and execution tools.

- [Official resources 1](https://ai.google.dev/gemini-api/docs)
- [Official resources 2](https://ai.google.dev/gemma)

## Microsoft

Phi는 비교적 작은 언어 모델을 중심으로 한 Microsoft의 모델 계열이다. 공식 PhiCookBook에는 로컬 실행·미세조정·배포 예제가 있다. 소형 모델이 사용하는 자원과 양자화, 장치 배포 과정을 살펴본다.

Phi is Microsoft's model family centered on relatively small language models. The official PhiCookBook provides examples of local execution, fine-tuning, and deployment. It supports examination of small-model resource use, quantization, and deployment to devices.

- [Official resources](https://github.com/microsoft/PhiCookBook)

## Meta

Llama는 Meta의 공개 가중치 언어 모델 계열이다. 버전별로 크기·입력 형식·라이선스가 다르다. Meta의 연구 저장소에는 비전과 표현 학습 프로젝트도 있으며, 모델 구조와 학습 방법을 소스에서 살펴볼 수 있다.

Llama is Meta's open-weight language-model family, with sizes, input formats, and licenses varying by version. Meta's research repositories also include vision and representation-learning projects whose code exposes model architectures and training methods.

- [Official resources 1](https://github.com/meta-llama/llama-models)
- [Official resources 2](https://github.com/facebookresearch)

## Anthropic

Claude는 API 기반의 언어·멀티모달 모델 생태계다. 긴 문서 처리와 코드, 도구 사용을 애플리케이션에 연결한다. API의 메시지·도구 인터페이스를 구성하는 작업과 모델 가중치를 수정하는 작업은 다르다.

Claude is an API-based language and multimodal model ecosystem. It connects long-document processing, coding, and tool use to applications. Configuring its message and tool interfaces is different from modifying model weights.

- [Official resources](https://platform.claude.com/docs/en/intro)

## Samsung

Samsung SAIL Montréal의 Tiny Recursive Models는 작은 네트워크를 반복 적용해 답과 내부 표현을 갱신하는 추론 연구 코드다. 재귀 단계와 학습 구조를 중심으로 읽는다. 일반적인 대화형 LLM과는 문제 구성·학습 방식이 다르며, [TRM 문서](samsung-trm/README.md)에 구조를 정리했다.

Tiny Recursive Models from Samsung SAIL Montréal is research code that repeatedly applies a small network to update answers and internal representations. Its recursive steps and training structure are the focus. Its problem formulation and training differ from conversational LLMs; the [TRM notes](samsung-trm/README.md) describe the architecture.

- [Official resources](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)

## DeepSeek

DeepSeek는 언어·코드·추론 모델과 관련 코드를 공개한다. R1은 추론 학습, V3는 대규모 언어 모델 구조, R1-Distill은 다른 기반 모델로 추론 능력을 전달하는 방법과 관련된다. 원본 모델과 distill checkpoint는 구조와 자원 요구가 다르다.

DeepSeek publishes language, code, and reasoning models together with related code. R1 concerns reasoning training, V3 large-language-model architecture, and R1-Distill the transfer of reasoning capabilities to other base models. Original models and distilled checkpoints differ in architecture and resource requirements.

- [Official resources](https://github.com/deepseek-ai)

## Alibaba / Qwen

Qwen은 언어·코드·시각언어 등 여러 작업을 다루는 모델 계열이다. Tokenizer·대화 형식·입력 범위는 모델별로 다르다. 공개 가중치 실행과 framework 통합, 다국어 처리, 모델 크기별 자원 사용을 살펴본다.

Qwen covers language, code, and vision-language tasks. Tokenizers, chat formats, and supported inputs vary by model. Relevant topics include open-weight inference, framework integration, multilingual processing, and resource use at different model sizes.

- [Official resources](https://github.com/QwenLM/Qwen3)

## Mistral AI

Mistral은 공개 가중치 모델과 hosted API를 제공한다. Dense·MoE 구조, 언어·코드·문서 처리 등 모델마다 구조와 목적이 다르다. 배포 방식과 사용 조건도 release별로 살펴본다.

Mistral provides open-weight models and hosted APIs. Models differ in architecture and purpose, including dense and MoE designs and language, code, and document tasks. Distribution methods and usage terms are examined per release.

- [Official resources](https://docs.mistral.ai/)

## IBM

Granite는 IBM의 언어·코드·기업용 AI 활용을 위한 모델 계열이다. 공개 model card와 코드에 학습 목적·평가·사용 조건이 담겨 있다. 검색과 문서 처리, 소형 모델 배포를 살펴본다.

Granite is IBM's model family for language, code, and enterprise AI applications. Published model cards and code describe training goals, evaluation, and usage terms. Retrieval, document processing, and small-model deployment are relevant areas of study.

- [Official resources](https://github.com/ibm-granite/granite-language-models)

## NVIDIA

Nemotron은 언어·추론 모델, Cosmos는 물리 세계와 영상·시뮬레이션 응용을 다룬다. GPU 추론 도구, 로봇과 합성 데이터 흐름도 함께 살펴본다. 모델 자체의 성능과 TensorRT 같은 runtime 최적화의 효과를 나눠 분석한다.

Nemotron covers language and reasoning models; Cosmos concerns the physical world and video/simulation applications. Related areas include GPU inference tools, robotics, and synthetic-data pipelines. Model performance is considered separately from optimization effects introduced by runtimes such as TensorRT.

- [Official resources](https://huggingface.co/nvidia)

## Apple

MLX는 Apple silicon을 위한 배열 연산·머신러닝 framework이고, Core ML은 Apple 플랫폼에 모델을 통합하고 실행하는 도구다. 공개 모델을 Apple 장치에서 실행할 때 모델 변환과 메모리 사용, 실행 조건을 살펴본다.

MLX is an array-computing and machine-learning framework for Apple silicon. Core ML integrates and runs models on Apple platforms. Running published models on Apple devices involves model conversion, memory use, and execution requirements.

- [Official resources](https://ml-explore.github.io/mlx/build/html/index.html)

## Amazon / AWS

Nova는 Amazon의 생성형 AI 모델 계열이며 AWS 서비스와 연결해 사용한다. 모델 API에 데이터·권한·응용 인프라를 연결하는 흐름을 살펴본다. 서비스 비용과 지연에는 모델 추론뿐 아니라 호출·전송·작업량도 영향을 준다.

Nova is Amazon's generative AI model family, used through AWS services. Its application flow connects model APIs with data, permissions, and supporting infrastructure. Service cost and latency depend on calls, transfers, and workload as well as model inference.

- [Official resources](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)

## Cohere

Command는 생성형 모델, Aya는 다국어 연구 모델 계열이다. Embedding·rerank 모델은 문서 검색의 표현과 순서를 다뤄 검색 품질에 영향을 준다. 공개 모델과 API의 제공 범위는 각각 살펴본다.

Command is a generative-model family, and Aya is a multilingual research-model family. Embedding and reranking models affect document-search quality through representations and result ordering. Published models and APIs have their own availability and scope.

- [Official resources](https://docs.cohere.com/)

## xAI

Grok은 xAI의 모델 계열이다. 공개된 Grok-1 저장소와 서비스 API의 모델은 별도의 배포물이다. 공개 release의 구조 분석과 API 응용은 실행 경로를 나눠 살펴본다.

Grok is xAI's model family. The published Grok-1 repository and models offered through the service API are separate distributions. Architecture analysis of a published release and API application development follow different execution paths.

- [Official resources 1](https://github.com/xai-org/grok-1)
- [Official resources 2](https://docs.x.ai/overview)

## Baidu

ERNIE는 Baidu의 언어·지식·멀티모달 모델 계열이다. PaddlePaddle과 연결된 구현에서 중국어·다국어 데이터와 모델 구조, 학습 framework의 관계를 살펴본다.

ERNIE is Baidu's language, knowledge, and multimodal model family. Implementations connected to PaddlePaddle provide a way to examine Chinese and multilingual data alongside model architectures and training frameworks.

- [Official resources](https://github.com/PaddlePaddle/ERNIE)

## Tencent

Hunyuan에는 언어·이미지·영상·3D 생성 모델 프로젝트가 있다. 작업마다 입력 데이터와 출력 표현, 추론 비용이 다르다. 텍스트 생성과 시각·공간 생성의 실행 흐름을 살펴본다.

Hunyuan includes language, image, video, and 3D generation projects. Input data, output representations, and inference costs differ by task. Text generation and visual/spatial generation have different execution flows.

- [Official resources](https://github.com/Tencent-Hunyuan)

## Z.ai

GLM은 언어·추론·도구 활용을 다루는 모델 계열이다. 공개 저장소에 모델 설명과 실행 예제가 있다. 대화 형식과 도구 인터페이스, 지원 runtime은 release별 문서에서 살펴본다.

GLM is a model family covering language, reasoning, and tool use. Its public repositories provide model descriptions and execution examples. Chat formats, tool interfaces, and supported runtimes are documented for each release.

- [Official resources](https://github.com/zai-org/GLM-4.5)

## Moonshot AI

Kimi는 긴 문맥 처리와 추론·도구 활용을 다루는 모델 계열이다. Kimi-K2는 MoE 기반 공개 모델이다. 전체 파라미터 수, token당 활성 파라미터 수와 실제 가중치 저장량을 구분해 구조와 자원 사용을 살펴본다.

Kimi covers long-context processing, reasoning, and tool use. Kimi-K2 is a published MoE model. Architecture and resource use are examined by distinguishing total parameter count, active parameters per token, and actual weight storage.

- [Official resources](https://github.com/MoonshotAI/Kimi-K2)

## Stability AI

Stable Diffusion 등 이미지·미디어 생성 모델을 제공한다. 확산 과정과 latent 표현, 텍스트 조건, sampler가 생성 결과에 영향을 준다. Prompt는 입력 조건을, fine-tuning·LoRA는 학습을 통해 모델의 동작을 바꾼다.

Stability AI provides image and media generation models including Stable Diffusion. Diffusion processes, latent representations, text conditioning, and samplers affect the generated output. Prompts change input conditions, while fine-tuning and LoRA adapt model behavior through training.

- [Official resources](https://github.com/Stability-AI/generative-models)

## Black Forest Labs

FLUX는 텍스트 조건의 이미지 생성·편집 모델 계열이다. 이미지 표현과 생성 step, 해상도에 따라 메모리 사용과 실행 시간이 달라진다. 코드와 각 모델 variant의 가중치 사용 조건도 나눠 살펴본다.

FLUX is a model family for text-conditioned image generation and editing. Image representations, generation steps, and resolution affect memory use and execution time. Code terms and weight-usage terms are examined separately for each model variant.

- [Official resources](https://github.com/black-forest-labs/flux)

## Hugging Face

Hugging Face는 모델·데이터셋 배포와 학습·추론 도구를 제공하는 플랫폼이다. Transformers·Datasets·Tokenizers·Safetensors와 SmolLM 계열 모델을 제공한다. Hub 모델의 원저작자와 라이선스는 각 model card에서 확인할 수 있다.

Hugging Face is a platform for distributing models and datasets and for training and inference tooling. It provides Transformers, Datasets, Tokenizers, Safetensors, and the SmolLM model family. Each Hub model's model card identifies its original creator and license.

- [Official resources 1](https://huggingface.co/HuggingFaceTB)
- [Official resources 2](https://huggingface.co/docs)

## LG AI Research

EXAONE은 LG AI Research의 언어·추론 모델 계열이다. 한국어·영어 문맥 처리와 공개 checkpoint의 실행을 살펴본다. 공개 가중치의 사용 범위는 release별 라이선스를 따른다.

EXAONE is LG AI Research's language and reasoning model family. Relevant topics include Korean and English context processing and running published checkpoints. Usage of published weights is governed by the license for each release.

- [Official resources](https://github.com/LG-AI-EXAONE/EXAONE-4.0)

## NAVER

HyperCLOVA X는 NAVER의 한국어·다국어·멀티모달 AI 생태계다. 서비스와 공개 모델 release를 각각 제공한다. 한국어 문체와 전문 용어, 문서 처리 결과가 입력과 평가 데이터에 따라 어떻게 달라지는지 살펴본다.

HyperCLOVA X is NAVER's Korean, multilingual, and multimodal AI ecosystem, offered through services and published model releases. Its study includes how inputs and evaluation data affect Korean style, technical terminology, and document-processing results.

- [Official resources](https://huggingface.co/naver-hyperclovax)

## Kakao

Kanana는 Kakao의 언어 모델 계열이다. 공개 저장소에서 모델 구성과 사용 예제, model card를 읽을 수 있다. 한국어 표현과 tokenizer, 대화 형식, 소형 모델의 실행 조건을 비교한다.

Kanana is Kakao's language-model family. Public repositories provide model configurations, usage examples, and model cards. Korean expression, tokenizers, chat formats, and small-model execution requirements are compared.

- [Official resources](https://github.com/kakao/kanana)

## Upstage

Solar는 Upstage의 언어 모델 계열이다. 공개 checkpoint와 서비스 제공 방식은 모델마다 다르다. 문서·한국어 응용과 모델의 학습·추론 구성을 살펴본다.

Solar is Upstage's language-model family. Published checkpoints and service offerings vary by model. Relevant topics include document and Korean-language applications and the organization of training and inference.

- [Official resources](https://huggingface.co/upstage)

## SK Telecom

A.X는 SK Telecom의 언어 모델 계열이다. 공개 model card에 모델의 목적과 실행·사용 조건이 담겨 있다. 한국어 응답과 다국어 처리, 추론 자원과 모델 배포의 관계를 살펴본다.

A.X is SK Telecom's language-model family. Published model cards describe intended purposes and execution and usage conditions. Its study connects Korean responses and multilingual processing with inference resources and model deployment.

- [Official resources](https://huggingface.co/skt)

## KT

Midm은 KT의 한국어 중심 언어 모델 계열이다. K-intelligence 계정에서 공개 배포물을 제공한다. 한국어 데이터와 모델 크기, 학습·추론 환경을 살펴본다.

Midm is KT's Korean-centered language-model family. Published distributions are available through the K-intelligence account. Relevant topics include Korean data, model size, and training and inference environments.

- [Official resources](https://huggingface.co/K-intelligence)

## NCSoft

VARCO는 NCSOFT의 AI 모델 계열이다. 언어·멀티모달 등 release마다 목적이 다르다. 지원 입력과 언어, 라이선스는 개별 model card의 범위를 기준으로 살펴본다.

VARCO is NCSOFT's AI model family, with language, multimodal, and other purposes varying by release. Supported inputs, languages, and licenses are examined through the scope described in each model card.

- [Official resources](https://huggingface.co/NCSOFT)

# AI 모델과 API | AI Providers, Public Models & APIs

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

AI 모델은 서비스 API 호출, 공개 가중치 추론, 코드 분석, 재학습·미세조정 등 여러 방식으로 활용할 수 있습니다. API는 인프라 운영 부담이 적고, 공개 가중치는 실행 환경과 수정 범위를 더 직접적으로 다룰 수 있습니다. 공개 코드·공개 가중치·데이터·라이선스는 각각 확인할 대상입니다.

## 모델을 구성하는 파일

신경망 구조는 연산과 연결을, 가중치는 학습된 수치를, tokenizer는 입력을 token으로 바꾸는 규칙을 담습니다. 추론에는 설정·가중치·tokenizer·runtime의 호환성이 함께 필요합니다. 모델 이름만 같아도 checkpoint·revision·quantization이 다르면 다른 결과가 나올 수 있습니다.

## 수정과 비교

Prompt·retrieval·decoder 설정은 추론 흐름을 바꾸고, 학습은 모델의 가중치를 갱신합니다. LoRA는 낮은 rank의 추가 파라미터를 학습하고, quantization은 수치 표현을 줄여 저장·계산 비용을 낮춥니다. 효과는 데이터와 실행 장치, 지원 kernel에 따라 달라집니다.

정확도·지연·처리량·메모리·API 비용은 별도의 지표입니다. 모델만 비교하더라도 입력, 출력 길이, sampling 조건, 하드웨어 조건이 결과에 영향을 줍니다. OpenAI·Google·Microsoft·Meta·Anthropic·Samsung·DeepSeek와 국내외 생태계의 특징은 [기업·모델 안내](../../AI모델과수치실험_ai-models/PROVIDERS.md)에 정리했습니다.

## 관련 기술

OpenAI, Google/DeepMind, Microsoft, Meta, Anthropic, Samsung, DeepSeek, Qwen, Mistral, IBM, NVIDIA, LG, NAVER, Kakao, Upstage, SKT

## 참고 자료

- [Hugging Face documentation](https://huggingface.co/docs)
- [OpenAI model documentation](https://developers.openai.com/api/docs/models)

## 기초 해설

- [모델 평가 지표: 정확도·정밀도·재현율·속도·메모리](../46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/모델평가지표_MODEL_EVALUATION.md)
- [모델 파일에서 다음 토큰까지: 가중치, 토큰화, sampling](해설_notes/모델파일에서다음토큰까지_weights-tokenizers-and-sampling.md)

## English

AI models can be used through service APIs, local inference with published weights, source-code analysis, and retraining or fine-tuning. APIs reduce infrastructure management, while published weights offer more direct control over execution and modification. Source code, weights, datasets, and licenses each have their own conditions.

### Model files

The architecture defines operations and connections, weights contain learned values, and the tokenizer maps input into tokens. Inference depends on compatible configuration, weights, tokenizer, and runtime. Checkpoint, revision, and quantization choices can change results even under the same model name.

### Modification and comparison

Changing prompts, retrieval, or decoding settings affects the inference pipeline. Training updates weights. LoRA trains additional low-rank parameters, and quantization reduces numerical precision to lower storage and computation costs. Their effects depend on data, devices, and supported kernels.

Accuracy, latency, throughput, memory use, and API cost measure different aspects of a system. Input, output length, sampling, and hardware must also be considered when comparing models. The [provider and model guide](../../AI모델과수치실험_ai-models/PROVIDERS.md) covers OpenAI, Google, Microsoft, Meta, Anthropic, Samsung, DeepSeek, and the wider ecosystem.

### Foundation article

- [Model evaluation metrics: quality, speed and memory](../46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/모델평가지표_MODEL_EVALUATION.md#english)
- [모델 파일에서 다음 토큰까지: 가중치, 토큰화, sampling](해설_notes/모델파일에서다음토큰까지_weights-tokenizers-and-sampling.md#english)


## 심화 해설 | Advanced article

- [Beam search의 목적함수와 KV cache의 메모리 예산](해설_notes/빔탐색과캐시예산_beam-cache-budget.md) · [English](해설_notes/빔탐색과캐시예산_beam-cache-budget.md#english)

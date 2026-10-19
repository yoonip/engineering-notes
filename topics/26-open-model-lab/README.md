# AI Models & APIs

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

AI를 직접 활용하는 방법은 서비스 API 호출, 공개 가중치 추론, 공개 코드 분석, 재학습·미세조정으로 나뉜다. API는 인프라 운영 부담이 적고, 공개 가중치는 실행 환경과 수정 범위를 더 직접적으로 다룰 수 있다. 공개 코드·공개 가중치·데이터·라이선스는 각각 확인할 대상이다.

## 모델을 구성하는 파일

신경망 구조는 연산과 연결을, 가중치는 학습된 수치를, tokenizer는 입력을 token으로 바꾸는 규칙을 담는다. 추론에는 설정·가중치·tokenizer·runtime의 호환성이 함께 필요하다. 모델 이름만 같아도 checkpoint·revision·quantization이 다르면 다른 결과가 나올 수 있다.

## 수정과 비교

Prompt·retrieval·decoder 설정을 바꾸는 것과 가중치를 학습하는 것은 다른 변경이다. LoRA는 낮은 rank의 추가 파라미터를 학습하고, quantization은 수치 표현을 줄여 저장·계산 비용을 낮춘다. 효과는 데이터와 실행 장치, 지원 kernel에 따라 달라진다.

정확도·지연·처리량·메모리·API 비용은 별도의 지표다. 모델만 비교하더라도 입력, 출력 길이, sampling 조건, 하드웨어 조건이 결과에 영향을 준다. OpenAI·Google·Microsoft·Meta·Anthropic·Samsung·DeepSeek와 국내외 생태계의 특징은 [기업·모델 안내](../../model-lab/PROVIDERS.md)에 정리했다.

## 관련 기술

OpenAI, Google/DeepMind, Microsoft, Meta, Anthropic, Samsung, DeepSeek, Qwen, Mistral, IBM, NVIDIA, LG, NAVER, Kakao, Upstage, SKT

## 참고 자료

- [Hugging Face documentation](https://huggingface.co/docs)
- [OpenAI model documentation](https://developers.openai.com/api/docs/models)

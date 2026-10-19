# Language · Speech · Multimodal AI

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

언어 모델은 token의 문맥적 관계를 학습한다. Token은 단어와 일대일로 대응하지 않을 수 있으며 tokenizer에 따라 같은 문장의 길이와 표현이 달라진다. Embedding은 입력을 벡터로 표현해 유사도·분류·검색 등에 사용한다.

## 언어와 음성

BERT는 문맥 표현 학습, T5는 text-to-text, GPT 계열은 주로 다음 token 예측 기반 생성 모델의 맥락에서 이해할 수 있다. ASR은 음성을 글로, TTS는 글을 음성으로 바꾼다. Whisper·wav2vec 계열은 음성 인식·표현 학습을 읽는 사례다. torchaudio는 음성 데이터 처리, SentencePiece는 tokenization 생태계다.

## 여러 입력을 함께 다루기

CLIP은 이미지와 텍스트 표현의 정렬, LLaVA 계열은 시각 정보와 언어 모델의 결합 사례다. Multimodal 시스템은 이미지·음성·영상·텍스트의 입력 처리와 시간·공간 정렬을 포함한다. 문장이 유창한 것과 입력 내용에 정확히 근거한 것은 별도의 평가 대상이다.

한국어·영어·제2외국어에서는 tokenizer 효율, 높임말과 문체, 문화적 맥락, 전문 용어, 번역 방향이 결과에 영향을 준다. 같은 의미의 질문도 언어마다 길이와 난도가 같지 않다.

## 관련 기술

BERT, T5, GPT, Whisper, wav2vec, CLIP, LLaVA, Transformers, torchaudio, SentencePiece

## 참고 자료

- [Hugging Face documentation](https://huggingface.co/docs)

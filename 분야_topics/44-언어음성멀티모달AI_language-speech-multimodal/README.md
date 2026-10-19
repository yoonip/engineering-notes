# 언어·음성·멀티모달 AI | Language, Speech & Multimodal AI

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

언어 모델은 token의 문맥적 관계를 학습한다. Token은 단어와 일대일로 대응하지 않을 수 있으며 tokenizer에 따라 같은 문장의 길이와 표현이 달라진다. Embedding은 입력을 벡터로 표현해 유사도·분류·검색 등에 사용한다.

## 언어와 음성

BERT는 문맥 표현을 학습하고, T5는 과제를 text-to-text 형식으로 다룬다. GPT 계열은 주로 다음 token을 예측하며 문장을 생성한다. ASR은 음성을 글로, TTS는 글을 음성으로 바꾼다. Whisper·wav2vec 계열은 음성 인식과 표현 학습의 사례다. torchaudio는 음성 데이터 처리, SentencePiece는 tokenization에 쓰인다.

## 여러 입력을 함께 다루기

CLIP은 이미지와 텍스트 표현의 정렬, LLaVA 계열은 시각 정보와 언어 모델의 결합 사례다. Multimodal 시스템은 이미지·음성·영상·텍스트의 입력 처리와 시간·공간 정렬을 포함한다. 문장의 유창함과 입력 내용에 대한 정확성은 따로 평가한다.

한국어·영어·제2외국어에서는 tokenizer 효율, 높임말과 문체, 문화적 맥락, 전문 용어, 번역 방향이 결과에 영향을 준다. 같은 의미의 질문도 언어마다 길이와 난도가 같지 않다.

## 관련 기술

BERT, T5, GPT, Whisper, wav2vec, CLIP, LLaVA, Transformers, torchaudio, SentencePiece

## 참고 자료

- [Hugging Face documentation](https://huggingface.co/docs)


## 개념·유도·모델·검증

[기초부터 읽기](../../문서_docs/공학기초_FOUNDATIONS.md)

- [Attention: 필요한 정보를 가중합으로 모으기](해설_notes/attention-from-equations.md)

## English

### Language, speech, and multimodal AI

Language models learn contextual relationships between tokens. A token does not necessarily correspond to a word, and tokenizer choices change the length and representation of the same sentence. Embeddings represent inputs as vectors for similarity, classification, retrieval, and related tasks.

### Language and speech

BERT learns contextual representations, T5 uses a text-to-text formulation, and GPT models are commonly associated with generation based on next-token prediction. ASR converts speech to text, while TTS converts text to speech. Whisper and wav2vec models provide examples of speech recognition and representation learning. torchaudio supports audio processing, and SentencePiece supports tokenization.

### Combining input modalities

CLIP aligns image and text representations. LLaVA models illustrate ways to combine visual information with language models. Multimodal systems process images, audio, video, and text, including their alignment in time and space. Fluency and accurate grounding in the input are separate evaluation targets.

For Korean, English, and other languages, tokenizer efficiency, register and honorifics, cultural context, terminology, and translation direction affect results. Questions with the same meaning do not necessarily have the same length or difficulty in every language.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../문서_docs/공학기초_FOUNDATIONS.md#english)

- [Attention from equations to implementation](해설_notes/attention-from-equations.md#english)


## 심화 해설 | Advanced article

- [Attention의 역전파와 causal KV cache 검증](해설_notes/어텐션역전파와캐시_attention-gradients.md) · [English](해설_notes/어텐션역전파와캐시_attention-gradients.md#english)

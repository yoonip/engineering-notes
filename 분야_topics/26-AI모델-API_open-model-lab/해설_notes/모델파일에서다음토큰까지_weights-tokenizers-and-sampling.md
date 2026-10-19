# 모델 파일에서 다음 토큰까지: 가중치, 토큰화, sampling

## 모델을 실행한다는 것

언어 모델은 문자열을 그대로 계산하지 않는다. Tokenizer가 문자열을 token ID의 열로 바꾸고, 모델이 그 ID와 문맥을 받아 다음 token의 점수인 logits를 계산한다. Decoder는 선택한 ID를 다시 문자열로 바꾼다. Token은 글자 하나나 단어 하나와 항상 같지 않다. 한글, 숫자, 공백, 특수기호의 분할 방식은 tokenizer마다 다르다. 정규화, 사전 분할, subword 모델, 후처리는 tokenizer pipeline의 서로 다른 단계다. [Hugging Face Tokenizers pipeline](https://huggingface.co/docs/tokenizers/main/en/pipeline)

가중치 $\theta$는 학습으로 정해진 수치이고, 모델 구조는 이 수치를 어떤 연산에 쓰는지 정의한다. 같은 숫자 배열이라도 구조·정밀도·tensor 이름이 맞지 않으면 실행할 수 없다. Token ID와 embedding 행의 대응도 학습 때와 같아야 한다. 따라서 재현 가능한 실행 단위는 가중치 파일 하나보다 넓다. 구조 설정, tokenizer, special token, chat template, 런타임 버전, 모델 revision이 함께 필요하다. 대화 형식의 문자열을 바꾸는 것도 실제 입력 ID를 바꾸는 일이다.

## Open weights와 API는 접근 방식이다

Open weights는 가중치를 내려받을 수 있다는 뜻으로 사용되지만, 사용·변경·재배포 조건이 모두 같다는 뜻은 아니다. API는 서버의 모델에 요청을 보내는 인터페이스다. 같은 모델 계열도 로컬 가중치와 API의 tokenizer·template·revision·기본 generation 설정이 다르면 출력이 달라질 수 있다. API 사용만으로 서버의 가중치를 받는 것은 아니다.

Model card에는 의도한 용도, 한계, 학습 정보, 평가와 license 정보를 기록할 수 있다. 공개 저장소의 코드 license와 모델 가중치 license가 다를 수도 있다. 실제 이용 조건은 해당 revision의 license 원문을 기준으로 읽어야 한다. 이 글은 특정 모델의 상업 이용 가능 여부를 판정하지 않는다. [Hugging Face model cards](https://huggingface.co/docs/hub/main/en/model-cards)

| 구성 요소 | 기록하는 이유 |
|---|---|
| 모델 ID와 revision | 같은 이름의 파일 변경을 구분 |
| tokenizer·chat template | 입력 ID와 대화 구분자를 재현 |
| dtype·양자화·runtime | 메모리와 수치 차이를 추적 |
| generation 설정·seed | 선택 규칙과 확률적 차이를 설명 |
| license 원문 위치 | 코드·가중치의 이용 조건을 구분 |

## Logits에서 확률로

어휘 크기가 $V$이고 logits가 $z_1,\ldots,z_V$라면 온도 $T>0$의 확률은

$$p_i=\frac{\exp(z_i/T)}{\sum_j\exp(z_j/T)}.
$$

Logit은 확률이 아니므로 음수여도 된다. 모든 logit에 같은 상수 $c$를 더하면 분자와 분모에 $e^{c/T}$가 곱해져 약분된다. 이 성질을 이용해 $m=\max_j z_j$를 뺀 뒤 `exp((z_i-m)/T)`를 계산하면 큰 양수의 지수 overflow를 피할 수 있다. 작은 $T$는 최고 점수에 더 집중시키고 큰 $T$는 유한한 logits의 분포를 더 평평하게 한다. 정확히 $T=0$을 이 식에 대입할 수는 없다. Greedy decoding은 별도로 최고 logit의 ID를 선택한다.

Top-k는 점수가 높은 $k$개만 남긴 뒤 그 안에서 다시 정규화한다. Top-p는 확률을 큰 순서로 누적해 임계 질량을 채우는 집합을 선택한다. 둘은 같은 연산이 아니다. Multinomial sampling은 만들어진 확률에 따라 ID를 뽑는다. 확률이 0.75인 token도 항상 선택되는 것은 아니다. [Transformers generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies)

## 작은 구현으로 선택 규칙 확인하기

[모델 코드](../../../예제_examples/확장기초_extended/ai_data/models.py)의 `token_probabilities`는 안정적인 softmax와 top-k를 구현한다. 같은 점수는 ID가 작은 쪽을 먼저 남기는 규칙을 사용한다. `sample_token`은 외부에서 받은 $u\in[0,1)$가 누적 확률의 어느 구간에 속하는지 찾는다. 작은 예제에서 선택 경계를 명확히 보기 위해 난수 생성과 선택을 분리했다.

```python
import math
from models import token_probabilities, sample_token

# 두 토큰의 확률은 각각 1/4과 3/4이다.
p = token_probabilities([0.0, math.log(3.0)])
print(p)
print(sample_token(p, 0.2))  # 0
print(sample_token(p, 0.7))  # 1
```

[검증](../../../예제_examples/확장기초_extended/ai_data/test_models.py)은 $z=(0,\ln3)$의 해석적 확률, 상수 이동 불변성, top-1 동점 처리, 온도 효과를 확인한다. 100개의 균등 간격 중점은 각 확률 구간에 25개와 75개 들어간다. 이는 난수 품질이나 모델의 언어 능력 평가가 아니라 선택 알고리즘 검증이다. Seed를 기록해도 다른 장치·kernel·runtime에서 bit 단위 재현성이 자동으로 보장되지는 않는다. 실제 모델 비교에는 고정된 입력과 설정, 입력 ID 확인, 출력 품질 평가가 별도로 필요하다.

## English

### What is executed

A language model computes over token IDs rather than raw strings. A tokenizer turns text into IDs; the model maps the context to next-token scores called logits; a decoder maps selected IDs back to text. Tokens are not necessarily characters or words. Korean text, numbers, spaces and punctuation can be segmented differently by different tokenizers. Normalization, pre-tokenization, subword modeling and post-processing are distinct pipeline stages. [Tokenizer pipeline](https://huggingface.co/docs/tokenizers/main/en/pipeline)

Weights $\theta$ are learned numerical values, while architecture defines their operations. Shapes, tensor names and numerical representation must match. Token IDs must retain their correspondence with embedding rows. Reproduction therefore needs architecture configuration, tokenizer, special tokens, chat template, runtime version and model revision, not just one weights file. Changing conversation formatting changes the actual input IDs.

### Access and usage terms

Open weights usually describes downloadable weights; it does not imply identical permission to use, modify or redistribute every model. An API exposes a hosted service rather than handing over its weights. Local and hosted variants can produce different outputs when their revisions, tokenization, templates or generation defaults differ. Model cards can document purpose, limitations, training, evaluation and licenses. Code and weights may carry different terms; the license text for the relevant revision is the reference. This article makes no commercial-use determination for a named model. [Model cards](https://huggingface.co/docs/hub/main/en/model-cards)

The table records the identity and revision, input formatting, dtype and runtime, selection settings and seed, and locations of applicable license texts. Each records a different source of reproducibility or usage constraints.

### From scores to selections

For finite logits and $T>0$, softmax is the equation above. Logits can be negative because they are scores, not probabilities. Adding a common constant cancels between numerator and denominator. Subtracting the maximum before exponentiation prevents overflow from large positive logits. Lower temperatures concentrate probability on the maximum; higher temperatures flatten the distribution. Substitution of $T=0$ is undefined; greedy decoding separately chooses a maximum-scoring ID.

Top-k retains $k$ high-scoring IDs and renormalizes their probabilities. Top-p selects a set by cumulative probability mass; it is a different operation. Multinomial sampling draws from the resulting distribution, so an ID with probability 0.75 is not chosen on every draw. [Generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies)

### Implementation and independent checks

The linked `token_probabilities` implements stable softmax and top-k, resolving score ties by smaller ID. `sample_token` locates an externally supplied uniform $u\in[0,1)$ in cumulative-probability intervals. Keeping randomness separate exposes exact selection boundaries.

Tests use logits $(0,\ln3)$, whose probabilities are exactly $1/4,3/4$, check common-shift invariance, top-1 ties and temperature effects. One hundred evenly spaced midpoints fall into the two intervals 25 and 75 times. This validates the selection algorithm, not a language model or a random-number generator. Recording a seed does not automatically guarantee bitwise agreement across devices, kernels or runtimes. Real-model comparisons also need fixed inputs and settings, inspection of token IDs and an explicit quality evaluation.

## Sources

- [Hugging Face Tokenizers, pipeline](https://huggingface.co/docs/tokenizers/main/en/pipeline): tokenizer stages and text transformations.
- [Hugging Face Hub, model cards](https://huggingface.co/docs/hub/main/en/model-cards): metadata, limitations and license locations.
- [Hugging Face Transformers, generation strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies): greedy and probabilistic token selection. Reference date: 2026-10-19.

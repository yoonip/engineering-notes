# Beam search의 목적함수와 KV cache의 메모리 예산

[실행 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 다음 한 글자와 전체 경로의 점수

확률이 가장 높은 다음 token만 고르는 greedy는 각 시점의 선택입니다. 전체 문장의 확률이 가장 높은 경로를 찾는 문제와 같지 않습니다. 첫 선택이 조금 불리해도 이후 선택의 조건부 확률이 높을 수 있습니다. Beam search는 매 단계 여러 prefix를 남겨 이 차이를 일부 탐색합니다. 유한한 beam으로 버린 prefix는 다시 돌아오지 않으므로 전역 최적해를 항상 찾는 알고리즘은 아닙니다. [Hugging Face generation strategies](https://huggingface.co/docs/transformers/en/generation_strategies)

표본 경로 $`y_{1:T}`$의 확률을 autoregressive 분해하면

```math
P(y_{1:T})=\prod_{t=1}^{T}P(y_t\mid y_{1:t-1}),\qquad
S(y_{1:T})=\sum_{t=1}^{T}\ln P(y_t\mid y_{1:t-1}).
```

Log는 양수 확률에서 단조 증가하므로 곱의 순위와 로그 합의 순위는 같습니다. 작은 확률을 길게 곱할 때 underflow를 줄이는 이점도 있습니다. 확률 0인 전이는 후보에서 제외합니다.

## 두 token의 작은 반례

첫 선택의 확률을 a=0.6, b=0.4라 하고 a 뒤에는 a와 b가 각각 0.5, b 뒤에는 a=0.01, b=0.99라고 하겠습니다. 길이 2에서 greedy는 a 다음 동점 규칙에 따라 a를 골라 확률 0.3을 얻습니다. b→b는 0.396으로 더 큽니다. Beam 폭 2이면 첫 단계의 두 후보를 모두 남겨 이 경로를 찾습니다.

`beam_search`는 단계마다 각 beam을 확장한 뒤 로그 점수가 큰 후보 B개를 heap으로 선택합니다. 점수가 같으면 token ID tuple의 사전 순서를 사용해 재현합니다. 상태 전이는 직전 token만 보는 작은 bigram 표입니다. 실제 언어 모델을 내려받거나 그 언어 능력을 평가하는 코드는 아닙니다. 최대 T, 어휘 V, 폭 B에서 후보 확장·선택은 단계당 대략 $`O(BV\log B)`$이며 저장한 sequence tuple의 길이와 복사 비용도 더해집니다.

## EOS와 길이 보정을 명시합니다

예제는 EOS를 선택한 경로를 더 확장하지 않고 기존 점수 그대로 후보에 남깁니다. 그 외 경로는 최대 길이까지 진행합니다. 길이 정규화나 반복 패널티는 쓰지 않습니다. 그러므로 종료 경로끼리는 길이 차이가 점수에 영향을 줄 수 있습니다. 각 log 확률이 0 이하이기 때문에 연장을 하면 원래 prefix 점수보다 커지지 않습니다. 이 자체가 일반적인 생성 품질의 정의는 아닙니다.

Length penalty를 넣으면 목적함수가 바뀝니다. 예를 들어 $`S/T^\alpha`$를 쓰는 것과 log 확률 합을 그대로 쓰는 것은 다른 순위입니다. Prefix 가지치기의 효과도 달라집니다. 라이브러리의 EOS·early stopping·length penalty 설정을 같게 두지 않으면 같은 “beam 폭 4”만으로 결과를 비교할 수 없습니다.

## KV cache는 탐색 결과를 저장하는 표와 다릅니다

Beam은 후보 sequence의 탐색 구조입니다. KV cache는 decoder attention의 과거 key·value를 재사용하는 수치 저장소입니다. 고정된 모델, causal attention, 일치하는 position과 mask에서는 과거 token이 미래 token 때문에 바뀌지 않아 재사용할 수 있습니다. [Hugging Face cache 설명](https://huggingface.co/docs/transformers/en/cache_explanation)

Batch B, 층 L, KV head 수 H, 길이 T, head 차원 d, 원소당 s byte라면 일반적인 dense cache의 값 저장량은

```math
D_{\mathrm{KV}}=2BLHTds.
```

앞의 2는 key와 value입니다. GQA/MQA에서는 query head 수가 아니라 실제 KV head 수를 넣습니다. 예제 B=1, L=32, H=8, T=4096, d=128, s=2이면 536,870,912 byte, 즉 512 MiB입니다. 이것은 가중치·activation·allocator 여유·임시 workspace를 제외한 값 배열의 계산량입니다. Python 객체 cache의 실제 메모리와도 같지 않습니다.

Beam마다 논리적 prefix가 갈라지면 cache의 소유 관계도 맞춰야 합니다. 단순 복제는 메모리를 늘리고, 공유 prefix 관리나 paged cache는 구현 조건을 바꿉니다. 모델의 가중치, prompt 앞부분, position 규칙이 바뀌었는데 과거 cache를 재사용하면 같은 계산이라는 전제가 무너집니다.

## 실행과 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" decode
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

길이 4의 CLI에서 greedy 경로는 aaaa, beam2는 bbbb입니다. 로그 점수는 각각 약 -2.59027, -0.94644입니다. 캐시 예산도 같은 JSON에 출력합니다. 테스트는 2-token 어휘의 길이 4 경로 16개를 모두 열거해 충분히 넓은 beam 결과와 직접 곱한 확률을 대조합니다. EOS를 더 확장하지 않는지와 작은 단위 계산도 확인합니다.

이 검증은 탐색의 목적함수와 byte 산술에 한정됩니다. 실제 모델에서는 tokenizer·revision·generation 설정을 고정하고, 정답·유용성·지연·cache 자원까지 별도로 측정합니다. 확률이 높은 문장이 사실이거나 유용하다는 뜻은 아닙니다.

## English

### Local selection versus sequence score

Greedy chooses the highest-probability next token at each step, which need not maximize a full sequence's probability. Beam search keeps several prefixes but permanently prunes others, so finite beam width does not guarantee a global optimum. [Generation strategies](https://huggingface.co/docs/transformers/en/generation_strategies)

Autoregressive probability factors into conditional probabilities. Their logarithms add, preserving rankings for positive probabilities and avoiding products that underflow. Zero-probability transitions are excluded.

The explicit two-token example starts with probabilities 0.6 and 0.4. After a, either next token has probability 0.5; after b, b has probability 0.99. Greedy obtains aa with probability 0.3, whereas bb has probability 0.396. Width two retains both initial prefixes and finds bb.

The code expands candidates and uses a heap to select the best B scores. Equal scores use lexicographic token-ID tuples. It is a bigram transition-table experiment, not a downloaded language model. Candidate selection is roughly $`O(BV\log B)`$ per step; sequence storage and copying add length-dependent costs.

### Termination changes the objective

An EOS-ended sequence is retained without further expansion. Other paths continue to a maximum length. No length normalization or repetition penalty is applied. Log probabilities are nonpositive, so extension cannot improve a prefix's raw score. Comparing different-length completions therefore requires acknowledging the chosen objective.

A length penalty such as $`S/T^\alpha`$ changes ranking and pruning behavior. Equal beam width alone does not establish comparable decoding unless EOS, stopping and scoring rules also match. Sequence probability is not itself factual correctness or usefulness.

### Cache storage is a different structure

Beams represent search candidates. A KV cache stores past attention keys and values. Causal inference with fixed weights, prompt, positions and mask allows past representations to be reused. [Cache explanation](https://huggingface.co/docs/transformers/en/cache_explanation)

Dense value storage is $`2BLHTds`$ bytes for batch B, layers L, actual KV heads H, context length T, head dimension d and element width s. Grouped/multi-query attention uses KV-head count rather than query-head count. The example gives 536,870,912 bytes, or 512 MiB. This excludes weights, activations, allocator overhead and workspace and is not Python-object memory usage.

Divergent beam prefixes require matching cache ownership. Duplication, shared prefixes and paged allocation have different costs. Changes to weights, earlier prompt content or position conventions invalidate the equivalence behind cache reuse.

### Executed checks

The commands above run four-token decoding. Greedy returns aaaa with score approximately -2.59027; beam two returns bbbb with -0.94644. Tests enumerate all 16 four-token sequences and compare a sufficiently wide beam against independently multiplied probabilities. EOS retention and a small cache-byte calculation are also checked.

These results establish the stated search and storage calculations. Actual model comparison additionally fixes tokenization, revision and generation settings and measures quality, latency and memory. A likely sequence need not be a true or useful one.

## 출처 / Sources

- [Hugging Face, Generation strategies](https://huggingface.co/docs/transformers/en/generation_strategies): greedy, beam and generation controls.
- [Hugging Face, How caching works](https://huggingface.co/docs/transformers/en/cache_explanation): causal KV reuse, per-layer storage and matching masks. 확인 / checked: 2026-10-19.

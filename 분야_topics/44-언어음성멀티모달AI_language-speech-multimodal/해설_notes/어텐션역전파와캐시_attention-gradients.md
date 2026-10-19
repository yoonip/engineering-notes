# Attention의 역전파와 causal KV cache 검증

[계산 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 가중합을 만드는 점수도 학습한다

Attention의 출력은 value의 가중합이다. 학습에서는 value만 바꾸는 것이 아니라 어떤 key를 더 볼지 정하는 query·key도 바뀐다. 출력이 조금 변할 때 손실이 얼마나 달라지는지 알면 이 세 경로로 기울기를 되돌릴 수 있다.

여기서는 query 한 개 $`q\in\mathbb R^d`$, key n개, value 폭 r을 다룬다. Dropout, 여러 head, projection weight와 layer norm은 포함하지 않는다. K와 V는 같은 위치 수를 가지지만 d와 r은 달라도 된다. Scaled dot-product의 정의는 원 논문과 PyTorch 연산 정의를 대조했다. [Attention Is All You Need `3.2](https://arxiv.org/pdf/1706.03762), [PyTorch SDPA](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.scaled_dot_product_attention.html)

```math
s_j=\frac{q^Tk_j}{\sqrt d},\qquad
p_j=\frac{e^{s_j}}{\sum_i e^{s_i}},\qquad
o=\sum_jp_jv_j.
```

Softmax는 최대 점수를 빼서 계산한다. Mask로 허용하지 않은 key의 p는 0이다. 적어도 하나의 key는 허용되어야 하며, 전부 막힌 행의 softmax를 정상 확률처럼 만들지 않는다.

## 출력에서 확률까지 역으로 이동한다

출력 쪽에서 도착한 gradient를 $`g=\partial L/\partial o\in\mathbb R^r`$라 하자. Value는 p만큼 출력에 기여하므로

```math
\frac{\partial L}{\partial v_j}=p_jg,\qquad
u_j=\frac{\partial L}{\partial p_j}=g^Tv_j.
```

다음은 softmax다. Jacobian 전체를 n×n 배열로 만들지 않고 곱의 형태로 정리할 수 있다.

```math
\frac{\partial p_i}{\partial s_j}=p_i(\delta_{ij}-p_j),\qquad
\bar u=\sum_ip_iu_i,\qquad
g_{s_j}=p_j(u_j-\bar u).
```

유도는 $`\sum_i u_ip_i(\delta_{ij}-p_j)`$에서 j항을 분리하면 된다. 평균보다 큰 u를 가진 위치의 점수에는 양의 방향 기여가 생긴다. 모든 score에 같은 상수를 더해도 확률이 안 바뀌므로 $`\sum_jg_{s_j}=0`$이라는 점검 관계도 얻는다.

Query와 key의 내적을 미분하면

```math
g_q=\frac1{\sqrt d}\sum_jg_{s_j}k_j,\qquad
g_{k_j}=\frac1{\sqrt d}g_{s_j}q.
```

Mask된 위치는 p=0이므로 이 모델에서 key·value 경로의 gradient도 0이다. Value 한 개만 허용되면 p=1, 출력은 그 value라 query와 key의 gradient는 0이 된다. 이런 극한은 숫자가 그럴듯한지보다 강한 검증 기준이다.

## 전체 Transformer로 연결할 때

실제 self-attention은 입력 X로부터 $`Q=XW_Q`$, $`K=XW_K`$, $`V=XW_V`$를 만든다. 위 미분에 affine map의 chain rule을 한 번 더 연결하면 projection weight와 X의 gradient가 나온다. 같은 X에서 세 갈래로 갈라졌으므로 X로 돌아오는 기여는 더해야 한다. 본 코드는 q,k,v 입력까지의 미분을 계산하며 Transformer 전체를 학습한 구현이라고 부르지 않는다.

한 query의 계산과 역전파는 대략 $`O(n(d+r))`$다. n×n Jacobian을 저장하지 않아 불필요한 제곱 메모리를 피한다. 모든 query를 한꺼번에 다루는 dense attention의 n×n score와는 계산 범위가 다르다. 실제 fused kernel은 메모리 저장과 재계산 방식을 더 바꿀 수 있다.

## Causal cache는 같은 순전파를 재사용해야 한다

Causal inference에서는 새 query가 이전 token들의 K,V를 재사용할 수 있다. 단, 모델과 앞 문맥, position 규칙이 고정되어 있어야 한다. Mask의 길이도 cache의 과거와 현재를 함께 포함해야 한다. [Hugging Face cache 설명](https://huggingface.co/docs/transformers/en/cache_explanation)

`KVCache`는 key·value를 tuple로 저장해 외부의 원래 list 수정이 저장 내용을 바꾸지 않도록 한다. 새 key·value를 추가하고 해당 prefix 전체에 대해 query 출력을 계산한다. 이는 단일 head의 이미 계산된 K,V를 받는 cache다. Tokenizer·embedding·projection을 수행하는 실제 decoder 모델은 아니다. 학습 중 오래된 weight로 계산한 cache를 그대로 쓰면 같은 함수의 gradient라는 전제가 맞지 않는다.

## 실행과 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" attention
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

CLI의 출력은 약 [0.2769451,0.6994068], query gradient는 [0.1229766,-0.0296572]다. 세 prefix의 cache 출력도 함께 보여 준다. Scalar 목적함수 $`L=g^To`$를 만들어 q의 모든 성분, key와 value의 모든 성분을 각각 중앙 차분으로 검사한다. 이 목적함수는 임의의 upstream gradient를 흘려보내는 검증 장치다.

추가 검사는 mask된 경로의 0 미분, 한 key의 극한, 모든 key가 막혔을 때의 거부, cache와 직접 prefix 계산의 일치다. 이 결과는 수치 계산 검증이며 실제 언어 모델의 loss·언어 능력·GPU 메모리 절감 측정은 아니다. 실서비스에서는 cache 수명, 사용자 간 소유권, prompt 변경과 batch 재정렬도 함께 검증한다.

## English

### Scores receive gradients too

Attention learns query and key representations as well as values. This example uses one d-dimensional query, n keys and r-dimensional values, without dropout, multiple heads, projection parameters or layer normalization. K and V share position count but need not share width. The equations match [the Transformer paper](https://arxiv.org/pdf/1706.03762) and [PyTorch SDPA](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.scaled_dot_product_attention.html).

Scores are scaled dot products, probabilities are stable softmax weights, and output is their weighted sum. Disallowed keys have probability zero. At least one key must remain; an all-masked row is rejected rather than treated as a normal probability distribution.

### Derive the vector backward pass

For upstream output derivative g, each value receives $`p_jg`$ and each probability receives $`u_j=g^Tv_j`$. Multiplying the softmax Jacobian by u gives $`g_{s_j}=p_j(u_j-\bar u)`$ with $`\bar u=\sum_ip_iu_i`$. This follows by separating the Kronecker-delta term in the sum. No n×n Jacobian needs to be allocated.

A common score shift leaves probabilities unchanged, yielding $`\sum_jg_{s_j}=0`$. The dot-product chain rule then gives $`g_q=\sum_jg_{s_j}k_j/\sqrt d`$ and $`g_{k_j}=g_{s_j}q/\sqrt d`$. Masked key/value gradients vanish. With only one permitted value, output equals it and query/key gradients are zero.

A Transformer additionally projects X into Q,K,V. Affine chain rules propagate these derivatives to projection weights and X; the three contributions to shared X add. The code stops at q,k,v and is not a full Transformer training implementation. One-query forward/backward work is $`O(n(d+r))`$, distinct from evaluating every query's dense n×n scores.

### Cache equivalence

With fixed weights, preceding context and positional conventions, causal inference can reuse past K,V. Masks must cover both cached and current positions. [Cache explanation](https://huggingface.co/docs/transformers/en/cache_explanation)

The cache stores tuples, appends already-computed single-head keys/values and computes output over the resulting prefix. It implements no tokenizer, embedding or decoder projections. Reusing values computed under old training weights would break the same-function premise needed for the gradient.

### Executed checks and scope

The commands produce output approximately [0.2769451,0.6994068] and query derivative [0.1229766,-0.0296572], plus three cached-prefix outputs. Tests form scalar $`L=g^To`$ and independently perturb every q, K and V component with centered differences.

Other checks cover zero derivatives of masked paths, the one-key limit, rejection of all-masked rows and cache agreement with a direct prefix calculation. These are arithmetic checks, not measured language-model loss, language quality or GPU-memory savings. Deployment also needs cache lifetime, user ownership, prompt-change and batch-reordering checks.

## 출처 / Sources

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/pdf/1706.03762): scaled dot-product attention and causal structure.
- [PyTorch 2.9 SDPA](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.scaled_dot_product_attention.html): scale, mask and weighted output semantics.
- [Hugging Face, How caching works](https://huggingface.co/docs/transformers/en/cache_explanation): inference reuse and position/mask alignment. 확인 / checked: 2026-10-19.

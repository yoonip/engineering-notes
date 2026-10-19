# Transformer의 attention 계산 | A worked attention calculation

대상은 Vaswani 등의 [Attention Is All You Need](https://arxiv.org/abs/1706.03762)입니다. 최초 제출은 2017년이며, 여기서는 [v7의 §3.2](https://arxiv.org/html/1706.03762v7#S3.SS2)를 기준으로 attention을 계산합니다. 논문의 번역 성능을 재현하는 실험과 아래의 수치 예제는 범위가 다릅니다.

## 논문에서 가져올 핵심

Transformer는 encoder–decoder 구조에서 attention과 위치별 feed-forward 계산을 사용합니다. Scaled dot-product attention은 query와 key의 내적을 $\sqrt{d_k}$로 나누고 softmax를 적용한 뒤, 그 비율로 value를 합칩니다. decoder의 미래 위치에는 마스크를 적용합니다. 이 설명의 근거는 원 논문 §3.1–3.2이며, 여기서는 해당 연산 하나를 분석합니다.

$$
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}(QK^T/\sqrt{d_k})V
$$

| 기호 | 역할 | 이 예제의 크기 |
| --- | --- | --- |
| Q | 현재 위치가 찾는 정보를 표현합니다. | 한 행, 두 성분 |
| K | 각 위치를 비교할 기준입니다. | 두 행, 두 성분 |
| V | 비율에 따라 섞을 실제 내용입니다. | 두 행, 두 성분 |
| softmax | 점수를 합이 1인 양의 비율로 바꿉니다. | 두 위치의 혼합 비율 |

## 두 토큰을 손으로 계산하기

직접 정한 입력은 `q=[1,0]`, `k1=[1,0]`, `k2=[0,1]`, `v1=[10,0]`, `v2=[0,20]`입니다. 내적은 `[1,0]`이며 $d_k=2$이므로 점수는 `[1/√2,0]`입니다.

첫 비율은 $p_1=e^{1/\sqrt2}/(e^{1/\sqrt2}+1)$이고 두 번째는 $1-p_1$입니다. 따라서 출력은 $p_1[10,0]+(1-p_1)[0,20]$입니다. 점수가 더 큰 첫 위치만 선택하는 것이 아니라 두 value를 서로 다른 비율로 섞습니다.

| 계산 | Python 3.12.14에서 실행한 값 |
| --- | --- |
| attention 비율 | `[0.6697615493, 0.3302384507]` |
| 가중합 출력 | `[6.6976154933, 6.6047690135]` |
| 첫 위치에서 미래 위치를 가린 비율 | `[1.0]` |
| 미래 위치를 가린 출력 | `[10.0, 0.0]` |

마스크가 있을 때에는 두 번째 key를 아무리 크게 바꾸어도 첫 위치의 출력이 바뀌지 않아야 합니다. 이 성질을 검사하면 단순히 표의 숫자를 맞추는 것보다 미래 정보 누출을 직접 확인할 수 있습니다.

## 계산이 알려 주는 것

내적 점수와 attention 비율, 출력 벡터는 서로 다른 값입니다. 비율이 0.67이라고 해서 정답 확률이 67%라는 뜻은 아닙니다. 이 비율은 현재 행에서 value를 섞는 데 쓰입니다. 최종 출력 확률은 뒤의 여러 계산을 거쳐 정해집니다.

여기서는 입력 행렬을 직접 정했으므로 Q·K·V의 학습, multi-head 연결, feed-forward, residual, layer normalization, 위치 표현을 구현하지 않았습니다. 이 작은 계산이 맞는다는 사실은 번역 품질이나 학습 성공을 보여 주지 않습니다. 다음 단계는 [attention 수식 해설](../분야_topics/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/attention-from-equations.md)과 [역전파·캐시 검증](../분야_topics/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/어텐션역전파와캐시_attention-gradients.md)입니다.

## 재실행

저장소 루트에서 `python 논문해설_papers/attention_calculation.py`를 실행합니다. 외부 패키지는 필요하지 않습니다. [실행 코드](attention_calculation.py)는 합 1, 비음수, 닫힌 형태와의 일치, 첫 위치 마스크, 미래 key 변경에 대한 불변성을 검사합니다. [원시 결과](attention_result.json)에는 반올림 전 값이 있습니다. 실행 확인일은 2026-10-19입니다.

## English

The worked example isolates scaled dot-product attention from Vaswani et al., §3.2. With two orthogonal keys and a two-component query, the weights are approximately 0.66976 and 0.33024. Their weighted value sum is `[6.69762, 6.60477]`. A causal mask leaves only the first value and makes the result invariant to future-key changes. The script checks these properties; it neither trains a Transformer nor reproduces translation scores.

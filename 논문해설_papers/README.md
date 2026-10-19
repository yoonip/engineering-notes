# 논문 해설 | Paper studies

논문의 주장을 수식과 구현, 실험 조건에 연결해 읽습니다. 저자의 연구 결과와 이 저장소에서 실행한 작은 계산은 구분하여 표시합니다. 참여 연구와 수상 이력은 [연구 기록](../연구_research/README.md)에 별도로 모았습니다.

| 읽을 글 | 분석할 질문 | 확인할 근거 |
| --- | --- | --- |
| [Attention Is All You Need](Transformer의계산_ATTENTION.md) | Q·K·V와 마스크가 어떤 계산을 만듭니까? | 원 논문 §3.2와 두 토큰 수치 계산 |
| [부분곱 제거의 주장과 재현 범위](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/부분곱실험의주장과근거_partial-product-reproduction-case.md) | 산술 오차·모델 정확도·회로 전력을 어떻게 구분합니까? | 구현·입력 조건·검증 기록과 연결한 분석 |
| [Tiny Recursive Models](../AI모델실험_model-lab/samsung-trm/README.md) | 작은 반복 모델이 어떤 과제를 푸는 구조입니까? | 논문·공식 코드·교육용 반복 계산 |
| [DeepSeek-R1과 증류](../AI모델실험_model-lab/deepseek-r1-distill/README.md) | 원 모델의 학습과 증류 모델은 어떻게 다릅니까? | 기술 보고서·모델 카드·학습 목표 비교 |

## 처음 읽을 때의 순서

초록에서 문제와 기여를 한 문장씩 적은 뒤, 결과 표에서 지표·비교 대상·데이터를 확인합니다. 다음으로 방법의 핵심 수식을 계산 가능한 작은 입력에 적용합니다. 마지막으로 실험 절에서 그 작은 계산만으로 확인할 수 없는 부분을 찾습니다. 정확도, 지연시간, 전력처럼 단위가 다른 결과를 한 가지 ‘성능’으로 합치지 않습니다.

논문의 그림을 그대로 베끼는 대신 입력·계산·출력의 관계를 직접 그리면 구현 경계가 보입니다. [논문·코드·특허 읽기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md)와 [쌍체 비교 실험](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md)에서는 비교 조건과 재현의 의미를 더 자세히 다룹니다.

## English

These studies connect claims to equations, implementations and experimental conditions. Paper-reported results are distinct from local calculations. The first worked study evaluates attention and masking on two tokens. Related studies examine partial-product approximation, Tiny Recursive Models and DeepSeek distillation. Personal publications and research participation have their own research index.

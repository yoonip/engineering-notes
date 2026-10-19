# Mistral Ministral 8B Instruct 2410

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `mistralai/Ministral-8B-Instruct-2410` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense Transformer · 36층 · GQA · interleaved sliding-window attention |
| 사용 조건의 표기 | Mistral Research License |

## 구조와 용도

긴 문맥을 처리하는 층과 sliding-window 층을 섞습니다. 공식 카드의 attention pattern은 128k·32k·32k·32k입니다. 이를 모든 층이 같은 길이의 KV 캐시를 보관하는 모델로 계산하면 실제 구조를 반영하지 못합니다.

## 재현 방법과 비교 항목

V3-Tekken tokenizer와 공식 mistral-common·mistral-inference 경로를 확인합니다. 모델 카드에는 runtime별 attention 지원 범위 차이가 기록되어 있으므로 설치한 버전에서 가능한 문맥을 다시 확인합니다. 같은 문서 검색 과제를 길이별로 나누어 평가합니다.

## 결과를 해석할 때

이 2410 배포물의 Research License를 Mistral의 다른 Apache 배포물과 혼동하면 안 됩니다. 128k 학습 한도가 모든 runtime의 128k 지원을 뜻하지 않습니다.

## 서로 다른 attention 범위를 읽는 법

sliding window는 각 층에서 최근의 일정 범위를 직접 참조하도록 제한하는 방식입니다. 이 모델은 128k 범위와 32k 범위를 섞으므로 한 층의 window만 보고 전체 모델이 오래된 정보를 무조건 버린다고 결론 내리면 안 됩니다. 다른 층을 통해 전달되는 정보와 직접 참조 범위는 다릅니다. 대화도 V3-Tekken의 차례 표식을 사용해 token ID로 만들며, 일반 문자열의 길이만으로 문맥을 계산하지 않습니다. [공식 구조 표와 입력 형식](https://huggingface.co/mistralai/Ministral-8B-Instruct-2410#ministral-8b-architecture)

직접 만든 캐시 비교에서는 층 네 개의 범위를 128·32·32·32로 놓고 다른 조건을 같게 두겠습니다. 모두 최대 범위에 도달했을 때 저장하는 토큰 위치 수의 합은 224이며, 전부 128인 경우의 512와 비교한 비율은 224/512=7/16입니다. 단위 k를 공통으로 생략한 산술입니다. 실제 runtime이 window 밖 캐시를 어떻게 저장하는지, 부가 메모리가 얼마인지는 측정하지 않았으므로 이 비율을 GPU 전체 메모리 절감률로 쓰지 않습니다.

## 직접 만든 긴 공지 독해 예

자체 문서의 앞에는 “배송 마감은 오후 3시입니다.”, 뒤에는 “이번 주 금요일에 한하여 배송 마감을 오후 2시로 바꿉니다.”를 놓겠습니다. 질문은 금요일과 토요일 마감 시각을 각각 묻습니다. 실제 생성 결과가 아닌 평가 입력의 설계입니다.

| 대상 | 유지해야 할 조건 |
| --- | --- |
| 금요일 | 한정된 변경이 적용되어 오후 2시입니다. |
| 토요일 | 다른 변경이 없다는 조건에서 일반 규칙인 오후 3시입니다. |
| 긴 간격 | 앞뒤 규칙이 실제 입력에 모두 남아 있어야 합니다. |
| 오류 해석 | 앞의 규칙만 쓰는 오류와 예외를 모든 요일로 넓히는 오류를 구분합니다. |

두 규칙 사이에 방해 문장을 더해도 질문의 정답은 바뀌지 않습니다. 다만 runtime이 입력 길이를 거절하거나 잘랐다면 같은 문서 독해 시험을 끝냈다고 볼 수 없습니다. 128k 학습 범위와 설치한 실행기의 지원 범위를 먼저 나누어야 긴 문맥의 정답률도 비교할 수 있습니다. 이 예와 캐시 산술은 실제 Ministral 추론 결과가 아닙니다.

[공식 모델 카드 또는 문서](https://huggingface.co/mistralai/Ministral-8B-Instruct-2410) · [공식 실행 코드 또는 참고 자료](https://github.com/mistralai/mistral-inference)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Interleaved attention changes cache behavior. The selected 2410 release has its own research license and runtime-dependent context support. This is a source-based release analysis; model inference was not run locally.

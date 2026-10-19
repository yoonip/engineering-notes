# NAVER HyperCLOVAX SEED Text 1.5B

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B` |
| 제공·입출력 | 공개 가중치 · 텍스트 → 텍스트 |
| 구조·설정 | Dense Transformer · 1.5B · 16k 문맥 |
| 사용 조건의 표기 | HyperCLOVAX SEED 라이선스 |

## 구조와 용도

한국어 언어·문화 지식에 초점을 둔 작은 텍스트 배포물입니다. HyperCLOVA X라는 서비스 계열의 멀티모달 기능을 이 체크포인트의 기능으로 옮기지 않습니다. 사실 지식과 자연스러운 한국어 문체는 별도 평가 항목입니다.

## 재현 방법과 비교 항목

모델 접근 조건과 공식 template을 확인합니다. 한국어 존댓말 변환·호칭 유지·수치 추출·모르는 질문 거절 과제를 준비합니다. 문맥이 길어질수록 입력의 근거 문장 위치를 바꾸어 정답 보존 여부를 기록합니다.

## 결과를 해석할 때

서비스 API와 이 공개 모델의 한도·라이선스는 서로 다를 수 있습니다. 한국 문화 벤치마크의 점수만으로 특정 분야 문서의 사실 정확도를 보장하지 않습니다.

[공식 모델 카드 또는 문서](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B) · [공식 실행 코드 또는 참고 자료](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

This 1.5B release is a text model with a 16k context, distinct from the full service ecosystem. Korean style and factual knowledge should be scored separately. This is a source-based release analysis; model inference was not run locally.

# Amazon Nova Micro v1

공식 자료 확인일: 2026-10-19입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `amazon.nova-micro-v1:0` |
| 제공·입출력 | Amazon Bedrock API · 텍스트 → 텍스트 |
| 구조·설정 | 서비스 배포 · 공개 가중치 구조를 가정하지 않습니다. |
| 사용 조건의 표기 | AWS 서비스 이용 조건 |

## 구조와 용도

Nova Micro는 공식 표에서 텍스트 전용 입력과 128k 문맥을 갖습니다. Nova Lite·Pro·Premier의 이미지·영상 입력을 Micro에도 적용하면 요청 설계가 잘못됩니다. API 모델을 선택하는 일과 모델 가중치를 직접 관리하는 일은 다릅니다.

## 재현 방법과 비교 항목

Bedrock에서 접근 가능한 region·모델 ID·IAM 권한을 확인하고 Converse 또는 Invoke API를 선택합니다. 동일한 정보 추출 입력과 출력 제한으로 비교하며 usage·재시도·중단 이유를 기록합니다. region을 넘는 inference profile을 쓰는지도 남깁니다.

## 결과를 해석할 때

서비스의 미세조정 기능이 가중치 다운로드를 뜻하지 않습니다. 실제 호출하지 않았으므로 접근 가능 여부·비용·지연은 이 문서에서 확정하지 않습니다.

[공식 모델 카드 또는 문서](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) · [공식 실행 코드 또는 참고 자료](https://docs.aws.amazon.com/nova/latest/userguide/using-converse-api.html)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Nova Micro is the text-only service variant examined here. Regional routing, permissions, retries, and usage belong in a reproducible API record. This is a source-based release analysis; model inference was not run locally.

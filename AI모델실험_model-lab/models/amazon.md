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

## 요청과 응답을 읽는 순서

Converse 요청은 `modelId`와 `messages`를 구분합니다. 대화는 메시지의 목록이고, 각 메시지의 `role`은 말한 주체, `content`는 내용 블록의 목록입니다. Micro의 자체 입력 예는 `{"role":"user","content":[{"text":"아래 공지의 날짜를 추출해 주세요."}]}`처럼 텍스트 블록으로 구성할 수 있습니다. Micro에는 PDF 문서 지원이 없으므로 PDF 파일을 직접 넣는 요청과, 파일에서 별도로 추출한 글자를 넣는 요청은 다릅니다. [Nova v1 기능 표](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)

응답에서는 본문만 읽지 않고 `output.message.content`의 텍스트, `stopReason`, `usage`를 함께 확인합니다. 예를 들어 `max_tokens` 중단은 답을 끝까지 완성했다는 표시가 아닙니다. 토큰 사용량은 문자 수와도 다릅니다. API 요청 성공과 업무 정답을 분리하면 권한 오류·출력 잘림·내용 오류가 같은 ‘실패’로 섞이지 않습니다. [Converse 응답 구조](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-response)

## 직접 만든 공지 추출 예

다음은 호출 결과가 아니라 평가에 사용할 자체 입력입니다. “행사는 11월 4일이며 접수는 10월 30일까지입니다. 장소는 추후 공지합니다. 행사일·접수마감·장소를 JSON으로 적고 없는 값은 null로 적어 주세요.”라고 묻습니다.

| 확인할 값 | 이 입력에서의 판정 기준 |
| --- | --- |
| 행사일 | 11월 4일을 골라야 합니다. |
| 접수마감 | 10월 30일과 행사일을 바꾸면 오답입니다. |
| 장소 | 실제 장소를 만들어 쓰면 오답입니다. |
| 형식 | JSON 파싱 성공과 각 필드의 정답을 따로 셉니다. |

세 필드 중 두 개만 맞으면 필드 정확도는 2/3이지만 문서 전체 정답은 아닙니다. 반대로 값이 모두 맞아도 JSON 뒤에 설명이 붙으면 엄격한 단일 JSON 계약은 어긴 것입니다. 이는 직접 정한 채점 규칙이며 모델의 측정 점수가 아닙니다. 같은 공지를 이미지로만 제공하여 실패했다면 Micro의 텍스트 입력 범위를 먼저 확인해야 하며, 그 결과를 텍스트 독해 능력의 오답률로 합산하지 않습니다.

[공식 모델 카드 또는 문서](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) · [공식 실행 코드 또는 참고 자료](https://docs.aws.amazon.com/nova/latest/userguide/using-converse-api.html)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Nova Micro is the text-only service variant examined here. Regional routing, permissions, retries, and usage belong in a reproducible API record. This is a source-based release analysis; model inference was not run locally.

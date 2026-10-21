# 텍스트 모델과 서비스 경로: Amazon Nova Micro v1 | Text model and Bedrock

공식 자료 재확인일: 2026-10-21입니다. 아래 내용은 특정 배포물의 자료 분석이며, 가중치 추론이나 유료 API 실험 결과는 아닙니다.

| 항목 | 내용 |
|---|---|
| 분석 대상 | `amazon.nova-micro-v1:0` |
| 제공·입출력 | Amazon Bedrock API · 텍스트 → 텍스트 |
| 구조·설정 | 서비스 배포 · 공개 가중치 구조를 가정하지 않습니다. |
| 사용 조건의 표기 | AWS 서비스 이용 조건 |

## 구조와 용도

Nova는 모델 계열이고 Bedrock은 모델을 호출하는 서비스입니다. Converse는 요청·응답 API 형식입니다. 세 이름은 같은 층위가 아닙니다. 이 글에서 확인한 Micro v1 문서에는 층 수·가중치·전체 학습 절차가 공개 추론 코드로 제공되지 않으므로 다른 공개 Transformer의 세부 구조를 대입하지 않습니다.

[공식 Nova v1 기능 표](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)는 Micro의 텍스트 입력, 문맥, 문서 직접 입력 미지원과 API 경로를 구분합니다. 미세조정 제공 여부와 원 가중치 다운로드 여부도 다릅니다. 여기서는 Nova 2의 새 기능을 Micro v1의 기능으로 옮기지 않으며 서비스의 홍보 문구로 성능 순위를 정하지 않습니다.

Nova Micro는 공식 표에서 텍스트 전용 입력과 128k 문맥을 갖습니다. Nova Lite·Pro·Premier의 이미지·영상 입력을 Micro에도 적용하면 요청 설계가 잘못됩니다. API 모델을 선택하는 일과 모델 가중치를 직접 관리하는 일은 다릅니다.

## 실행에 필요한 조건과 비교 항목

Bedrock에서 접근 가능한 region·모델 ID·IAM 권한을 확인하고 Converse 또는 Invoke API를 선택합니다. 동일한 정보 추출 입력과 출력 제한으로 비교하며 usage·재시도·중단 이유를 기록합니다. region을 넘는 inference profile을 쓰는지도 남깁니다.

## 공개 범위와 한계

서비스의 미세조정 기능이 가중치 다운로드를 뜻하지 않습니다. 실제 호출하지 않았으므로 접근 가능 여부·비용·지연은 이 문서에서 확정하지 않습니다.

## 요청과 응답을 읽는 순서

Converse 요청은 `modelId`와 `messages`를 구분합니다. 대화는 메시지의 목록이고, 각 메시지의 `role`은 말한 주체, `content`는 내용 블록의 목록입니다. Micro의 자체 입력 예는 `{"role":"user","content":[{"text":"아래 공지의 날짜를 추출해 주세요."}]}`처럼 텍스트 블록으로 구성할 수 있습니다. Micro에는 PDF 문서 지원이 없으므로 PDF 파일을 직접 넣는 요청과, 파일에서 별도로 추출한 글자를 넣는 요청은 다릅니다. [Nova v1 기능 표](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html)

응답에서는 본문만 읽지 않고 `output.message.content`의 텍스트, `stopReason`, `usage`를 함께 확인합니다. 예를 들어 `max_tokens` 중단은 답을 끝까지 완성했다는 표시가 아닙니다. 토큰 사용량은 문자 수와도 다릅니다. API 요청 성공과 업무 정답을 분리하면 권한 오류·출력 잘림·내용 오류가 같은 ‘실패’로 섞이지 않습니다. [Converse 응답 구조](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-response)

평가 입력과 판정 예는 [별도 문서](../experiments/평가입력과판정기준_evaluation-design.md#amazon)에서 보실 수 있습니다. 실제 모델 응답을 얻은 기록은 아닙니다.

[공식 모델 카드 또는 문서](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) · [공식 실행 코드 또는 참고 자료](https://docs.aws.amazon.com/nova/latest/userguide/using-converse-api.html)

[모델 목록](README.md) · [직접 실행한 CPU 수치 실험](../experiments/README.md)

## English

Nova Micro is the text-only service variant examined here. Regional routing, permissions, retries, and usage belong in a reproducible API record. This is a source-based release analysis; model inference was not run locally.

# 클라우드와 분산 시스템 | Cloud, Distributed Systems & Operations

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

분산 시스템은 네트워크로 연결된 여러 실행 주체가 함께 서비스를 제공하는 구조입니다. 네트워크 지연, 부분적인 장애, 독립적인 실행 순서 때문에 단일 프로그램과 다른 문제가 생깁니다.

## 실패와 일관성

요청을 보낸 뒤 응답이 없으면 서버가 실패했는지, 처리 후 응답만 사라졌는지 구분하기 어렵습니다. Retry는 복구에 도움이 되지만 중복 실행을 만들 수 있습니다. Idempotency는 같은 요청을 반복해도 의도한 효과가 중복되지 않는 성질입니다. 복제 데이터의 일관성과 가용성은 장애 조건을 포함해 해석합니다.

## 배포와 운영

AWS·Azure·Google Cloud는 compute·storage·network·managed service를 제공합니다. Docker는 컨테이너 실행 환경, Kubernetes는 여러 컨테이너의 배치·상태 관리, Terraform은 인프라 구성을 코드로 다루는 도구입니다. 컨테이너 수를 늘리는 것만으로 공유 데이터와 병목 문제가 해결되지는 않습니다.

Log는 사건, metric은 수치 시계열, trace는 요청이 여러 서비스를 거치는 경로를 보여줍니다. Prometheus·Grafana·OpenTelemetry는 서비스 상태를 관측하는 데 쓰입니다. Latency·error rate·비용을 함께 보면 성능과 운영 방식의 영향을 파악할 수 있습니다.

## 관련 기술

AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Prometheus, Grafana, OpenTelemetry

## 참고 자료

- [Kubernetes concepts](https://kubernetes.io/docs/concepts/)

## 기초 해설

- [복제본의 교집합: quorum과 일관성의 조건](해설_notes/복제본의교집합_quorums-failures-and-consistency.md)

## 응답 유실과 늦은 효과의 순서

재시도 정책은 ‘응답을 받았는가’와 ‘이전 요청이 다시 영향을 줄 수 있는가’를 나누어 판단해야 합니다. 서버가 이미 처리했지만 응답만 사라졌다면 새 ID로 재시도하는 요청은 같은 작업을 두 번 만들 수 있습니다. 같은 ID의 결과를 보관하는 방식은 그 중복을 다루지만, 결과 저장과 실제 부작용을 따로 갱신하면 둘 사이에서 장애가 날 수 있습니다. 멱등성 키가 존재한다는 사실만으로 원자적인 중복 제거가 완성되지는 않습니다.

멱등성은 순서 보장과도 다릅니다. 값 대입 `set(A)`를 두 번 연속 수행하면 A이지만, `set(A) → set(B) → set(A)`는 마지막 값이 A입니다. 첫 A를 옛 시도로 보고 callback만 버려도 마지막 효과는 그대로입니다. 저장장치 모델에서는 R1의 A가 timeout된 뒤 retry B가 AAAA를 쓰고, R2가 BBBB를 쓴 다음 옛 A가 적용되면 최종 AAAA가 됩니다. 응용 완료는 R1·R2 각각 한 번이므로 완료 개수와 최종 값을 함께 확인해야 합니다.

| 구별할 조건 | 확인해야 할 내용 |
| --- | --- |
| 응답이 없습니다. | 미실행·실행 후 응답 유실 중 어느 쪽인지 아직 모릅니다. |
| 같은 ID로 재시도합니다. | ID 범위·보관 기간·중복 결과·부작용과 결과 저장의 원자성을 확인합니다. |
| 옛 callback을 무시합니다. | 호스트 통지를 걸러도 옛 장치·서버의 부작용이 멈췄다는 증거는 아닙니다. |
| 새 값을 쓰려고 합니다. | 미해결 옛 작업이 새 값을 다시 덮을 수 있는지 확인합니다. |

교육용 [늦은 쓰기와 retry 사례](../../설계와검증사례_engineering-cases/시간초과뒤늦은쓰기와재시도_block-io-timeout-retry.md)는 미해결 쓰기를 막고, 옛 작업이 더 이상 영향을 줄 수 없다는 명시적 모델 입력 뒤에만 재시도를 허용합니다. 이것을 분산 서비스의 실제 취소 구현이나 일반적인 exactly-once 보장으로 바꾸어 설명하지 않습니다. 네트워크에서는 취소·중복 제거·트랜잭션·순서 번호의 구체적인 계약이 각각 필요합니다.

## English

### Cloud and distributed systems

A distributed system provides a service through multiple participants connected by a network. Network delay, partial failures, and independent execution orders introduce problems that do not occur in a single process in the same way.

### Failures and consistency

When a request receives no response, it can be difficult to distinguish a server failure from a successful operation whose response was lost. Retrying can help recovery but can also repeat an operation. Idempotency allows repeated requests without duplicating the intended effect. Data consistency and availability need to be considered together with the failure conditions.

### Deployment and operations

AWS, Azure, and Google Cloud provide compute, storage, networking, and managed services. Docker runs containers, Kubernetes schedules and manages containerized workloads, and Terraform describes infrastructure as code. Adding containers alone does not resolve shared-data issues or bottlenecks.

Logs record events, metrics record numerical time series, and traces follow a request across services. Prometheus, Grafana, and OpenTelemetry support observability. Latency, error rate, and cost together show the effects of performance and operational decisions.

### Foundation article

- [복제본의 교집합: quorum과 일관성의 조건](해설_notes/복제본의교집합_quorums-failures-and-consistency.md#english)


### Lost replies and late effects

Retry policy must distinguish a missing reply from evidence that an older attempt can no longer have effects. An idempotency key needs a defined scope, retention period, and atomic relationship between the recorded result and the side effect. A stored key alone does not supply those conditions.

Idempotency also differs from ordering. Repeating `set(A)` yields A, but `set(A), set(B), set(A)` still ends in A. The [late-write example](../../설계와검증사례_engineering-cases/시간초과뒤늦은쓰기와재시도_block-io-timeout-retry.md#english) executes this counterexample: filtering an old callback preserves one completion per request while the old effect overwrites the newer value. Its explicit stop-evidence input is an educational contract, not a distributed cancellation or exactly-once implementation.

## 심화 해설 | Advanced article

- [Lamport clock: 시각을 맞추지 않고 인과 순서를 기록하기](해설_notes/논리시계와인과관계_lamport-clocks.md) · [English](해설_notes/논리시계와인과관계_lamport-clocks.md#english)

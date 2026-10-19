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


## 심화 해설 | Advanced article

- [Lamport clock: 시각을 맞추지 않고 인과 순서를 기록하기](해설_notes/논리시계와인과관계_lamport-clocks.md) · [English](해설_notes/논리시계와인과관계_lamport-clocks.md#english)

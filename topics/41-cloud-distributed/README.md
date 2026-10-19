# Cloud & Distributed Systems

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

분산 시스템은 네트워크로 연결된 여러 실행 주체가 함께 서비스를 제공하는 시스템이다. 네트워크 지연, 부분적인 장애, 독립적인 실행 순서 때문에 단일 프로그램과 다른 문제가 생긴다.

## 실패와 일관성

요청을 보낸 뒤 응답이 없으면 서버가 실패했는지, 처리 후 응답만 사라졌는지 구분하기 어렵다. Retry는 복구에 도움이 되지만 중복 실행을 만들 수 있다. Idempotency는 같은 요청을 반복해도 의도한 효과가 중복되지 않게 설계하는 성질이다. 복제 데이터의 일관성과 가용성은 장애 조건을 포함해 해석한다.

## 배포와 운영

AWS·Azure·Google Cloud는 compute·storage·network·managed service를 제공한다. Docker는 컨테이너 실행 환경, Kubernetes는 여러 컨테이너의 배치·상태 관리, Terraform은 인프라 구성을 코드로 다루는 도구다. 컨테이너 수를 늘리는 것만으로 공유 데이터와 병목 문제가 해결되지는 않는다.

Log는 사건, metric은 수치 시계열, trace는 요청이 여러 서비스를 거치는 경로를 보여준다. Prometheus·Grafana·OpenTelemetry는 관측 도구 생태계다. Latency·error rate·비용을 함께 보면 성능과 운영 선택의 영향을 읽을 수 있다.

## 관련 기술

AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Prometheus, Grafana, OpenTelemetry

## 참고 자료

- [Kubernetes concepts](https://kubernetes.io/docs/concepts/)

# Kubernetes 네트워크 정책 | Kubernetes Network Policy

자료 확인일: 2026-11-04

Kubernetes NetworkPolicy는 Pod 사이와 Pod의 외부 통신을 IP·포트 수준에서 제한하는 API입니다. YAML 객체를 만들었다고 통신이 자동으로 제한되는 것은 아닙니다. 실제 정책 적용은 NetworkPolicy를 지원하는 네트워크 플러그인(CNI)이 맡습니다. 플러그인이 지원하지 않으면 정책 객체가 있어도 아무 효과가 없을 수 있습니다. [Kubernetes 공식 문서](https://kubernetes.io/docs/concepts/services-networking/network-policies/)의 1.37 문서를 기준으로 동작을 설명합니다.

이 장은 Kubernetes 기본 NetworkPolicy의 적용 범위와 정책 작성·검증 흐름을 다룹니다. 특정 CNI나 클라우드 사업자의 실서비스 설정은 아니며, 코드 조각도 실행하지 않은 교육 예시입니다.

## 네트워크 정책이 적용되는 범위

Kubernetes Namespace는 객체를 구분하고 권한·이름·정책 범위를 구성하는 단위입니다. Namespace가 나뉘었다는 사실만으로 그 안의 Pod 통신이 차단되지는 않습니다. 기본적으로 어떤 NetworkPolicy도 적용되지 않은 Pod는 ingress와 egress 통신이 모두 허용됩니다.

NetworkPolicy는 `podSelector`로 정책 대상 Pod를 고르고, `policyTypes`의 방향별로 그 Pod를 격리합니다. ingress 규칙은 다른 곳에서 대상 Pod로 들어오는 연결을, egress 규칙은 대상 Pod가 바깥으로 시작하는 연결을 다룹니다. 선택된 방향에서는 적용 가능한 정책들이 허용하는 연결의 합집합이 허용됩니다. 정책 순서로 뒤의 정책이 앞의 허용을 취소하는 구조가 아닙니다.

Pod A에서 Pod B로 연결하려면 A의 egress 정책과 B의 ingress 정책이 모두 허용해야 합니다. 한쪽이라도 허용하지 않으면 연결할 수 없습니다. 응답 패킷은 허용된 연결의 일부로 처리되지만, 별도의 업무 흐름을 새로 시작하는 연결은 따로 검토해야 합니다. [Kubernetes 문서의 정책 결합·기본 정책 설명](https://kubernetes.io/docs/concepts/services-networking/network-policies/#networkpolicy-resource)에서 이 동작과 기본 허용 상태를 확인할 수 있습니다.

## 웹에서 API를 거쳐 DB로 가는 흐름

예를 들어 `frontend` Namespace의 웹 Pod가 `app` Namespace의 API Pod에 요청하고 API Pod가 `data` Namespace의 데이터베이스에 접속한다고 하겠습니다.

```text
frontend/web ── TCP 8443 ──▶ app/api ── TCP 5432 ──▶ data/postgres
     DNS 질의 ───────────────▶ cluster DNS ◀────────────── DNS 질의
```

다음 정책은 API Pod의 ingress와 egress를 모두 격리하고, 웹 Pod에서 오는 TCP 8443 요청, PostgreSQL로 향하는 TCP 5432 요청, 클러스터 DNS 질의만 허용하는 예시입니다. Namespace 및 Pod label, DNS Pod label, 포트는 설명용이므로 실제 클러스터에 맞춰 확인해야 합니다.

```yaml
apiVersion: networking.k8s.io/v1 # Kubernetes의 NetworkPolicy API 버전을 지정합니다.
kind: NetworkPolicy # 생성할 객체가 네트워크 정책임을 나타냅니다.
metadata: # 객체의 이름과 소속 Namespace를 기록합니다.
  name: api-traffic-boundary # 정책 이름으로 대상과 목적을 식별합니다.
  namespace: app # 정책 객체를 app Namespace 안에 둡니다.
spec: # 실제 선택 대상과 허용 흐름을 정의합니다.
  podSelector: # 아래 규칙을 적용할 Pod를 고릅니다.
    matchLabels: # Pod에 붙은 label을 조건으로 사용합니다.
      app: api # app=api인 Pod에만 이 정책을 적용합니다.
  policyTypes: # 이 정책이 격리할 통신 방향을 지정합니다.
    - Ingress # 선택한 API Pod로 들어오는 연결을 제한합니다.
    - Egress # 선택한 API Pod가 밖으로 시작하는 연결을 제한합니다.
  ingress: # API Pod에 들어올 수 있는 연결을 적습니다.
    - from: # 허용할 출발 Pod와 Namespace 조건입니다.
        - namespaceSelector: # 출발 Pod가 속한 Namespace를 선택합니다.
            matchLabels: # Namespace label을 조건으로 지정합니다.
              kubernetes.io/metadata.name: frontend # frontend Namespace만 선택합니다.
          podSelector: # 같은 항목의 Namespace 조건과 함께 평가합니다.
            matchLabels: # 출발 Pod label을 조건으로 지정합니다.
              app: web # app=web인 웹 Pod만 선택합니다.
      ports: # 이 출발지에서 허용할 목적 포트를 정합니다.
        - protocol: TCP # 전송 계층 프로토콜을 TCP로 제한합니다.
          port: 8443 # API가 수신하는 예시 포트만 허용합니다.
  egress: # API Pod가 시작할 수 있는 연결을 적습니다.
    - to: # 허용할 데이터베이스 대상입니다.
        - namespaceSelector: # 대상 Pod가 속한 Namespace를 선택합니다.
            matchLabels: # Namespace label을 조건으로 지정합니다.
              kubernetes.io/metadata.name: data # data Namespace만 선택합니다.
          podSelector: # 같은 항목의 Namespace 조건과 함께 평가합니다.
            matchLabels: # 대상 Pod label을 조건으로 지정합니다.
              app: postgres # app=postgres인 DB Pod만 선택합니다.
      ports: # 데이터베이스에 허용할 포트를 정합니다.
        - protocol: TCP # 전송 계층 프로토콜을 TCP로 제한합니다.
          port: 5432 # PostgreSQL 기본 포트 예시를 사용합니다.
    - to: # DNS 질의가 향할 클러스터 DNS 대상을 적습니다.
        - namespaceSelector: # DNS Pod의 Namespace를 선택합니다.
            matchLabels: # DNS Namespace label을 조건으로 지정합니다.
              kubernetes.io/metadata.name: kube-system # 흔한 DNS Namespace 예시입니다.
          podSelector: # 해당 Namespace 안에서 DNS Pod를 고릅니다.
            matchLabels: # DNS Pod label을 조건으로 지정합니다.
              k8s-app: kube-dns # 흔한 CoreDNS label 예시이며 설치별 확인이 필요합니다.
      ports: # DNS 요청에 쓸 전송 프로토콜과 포트를 정합니다.
        - protocol: UDP # 일반 DNS 질의에 쓰이는 UDP를 허용합니다.
          port: 53 # DNS 서비스의 표준 포트입니다.
        - protocol: TCP # 큰 응답·재시도 등에 필요한 TCP도 허용합니다.
          port: 53 # DNS 서비스의 표준 포트입니다.
```

같은 `from` 또는 `to` 항목 안에 `namespaceSelector`와 `podSelector`를 함께 적으면 두 조건을 모두 만족하는 대상이 선택됩니다. 둘을 별도 목록 항목으로 분리하면 각각의 조건이 허용 대상이 되는 방식으로 의미가 달라집니다. 이 구분은 정책 범위를 지나치게 넓히는 실수를 막는 데 중요합니다.

이 예시는 `app=api` Pod의 모든 egress를 제한합니다. DNS 경로가 실제로 NodeLocal DNSCache, 다른 Namespace, 별도 IP 주소를 경유하면 위 label 선택자가 맞지 않을 수 있습니다. 클러스터에서 DNS Service와 Endpoint, 실제 Pod label, CNI의 서비스 NAT 처리 순서를 확인한 다음 정책을 정해야 합니다. Kubernetes 문서는 LoadBalancer·Service에서 주소가 변환되는 시점과 NetworkPolicy의 처리 순서가 플러그인·클라우드·Service 구현에 따라 달라질 수 있다고 설명합니다.

## 표준 정책과 CNI 확장 기능

| 선택지 | 적용 범위 | 고려할 점 |
| --- | --- | --- |
| Kubernetes NetworkPolicy | Namespace 안의 Pod 간 L3/L4 연결 정책 | 표준 API라 이식성이 좋지만 이를 집행하는 CNI가 필요합니다. 기본 API는 명시적 deny 규칙, 공통 게이트웨이 강제, TLS 내용 검사, 정책 이벤트 로깅을 제공하지 않습니다. |
| Calico NetworkPolicy 계열 | Kubernetes 표준 정책과 Calico 고유 정책·전역 정책 | 전역 정책·정책 순서 등 추가 기능을 쓸 수 있지만 해당 기능과 동작은 Calico 구현에 종속됩니다. 시스템 Namespace를 포함한 전체 정책은 클러스터 기능을 끊을 수 있어 범위를 신중히 제한합니다. |
| Cilium 정책 | Kubernetes 표준 정책과 CiliumNetworkPolicy 계열 | 공식 문서는 L3/L4와 일부 L7 정책을 설명합니다. L7 기능과 정책 문법은 Cilium 기능·버전 및 데이터 경로에 따라 달라지므로 Cilium 확장으로 분류합니다. |

표준 NetworkPolicy만으로 패킷이 차단되었거나 허용되었다는 로그 이벤트를 얻을 수는 없습니다. 관찰·진단은 CNI가 제공하는 흐름 기록, 정책 판정 로그, 노드 계측을 사용해야 합니다. CNI 로그의 필드와 의미는 제품마다 다르므로 Kubernetes API 자체의 동작과 혼동하지 않습니다. [Cilium 정책 문서](https://docs.cilium.io/en/stable/security/policy/)는 표준 NetworkPolicy와 Cilium 전용 정책 리소스 및 L3·L4·L7 정책 기능을 구분합니다. [Calico의 Kubernetes 기본 거부 안내](https://docs.tigera.io/calico/latest/network-policy/get-started/kubernetes-default-deny)는 표준 NetworkPolicy와 Calico 전역 정책을 구분하고 시스템 Namespace 제외 및 단계적 검증을 설명합니다.

## 안전하게 적용하고 확인하는 순서

1. 실행 중인 CNI와 NetworkPolicy 지원 여부를 먼저 확인합니다. API 서버에 객체가 생성되는 것과 데이터 경로에서 실제로 집행되는 것은 별개입니다.
2. API Pod가 사용하는 DNS, 인증, 로깅, 모니터링, 서비스 메시, 백업, 외부 API 등 의존성을 애플리케이션 담당자와 함께 목록화합니다.
3. 정책을 배포하기 전 대상 selector가 실제 Pod 집합과 일치하는지, `namespaceSelector`와 `podSelector` 조합이 AND인지 OR인지 확인합니다.
4. 관리되는 시험 Namespace에서 정책을 적용하고 정상 흐름과 차단해야 하는 흐름을 각각 확인합니다. 기존 정책도 허용 규칙을 추가할 수 있으므로 적용 중인 정책 전체를 확인합니다.
5. DNS 조회, 서비스 요청, 외부 egress, 초기화 컨테이너와 재시작을 확인합니다. 정책 변경 직후 분산된 플러그인 반영에는 시간 차이가 날 수 있습니다.
6. 의도한 정책 집행을 CNI 관측 도구와 Pod·Service 상태에서 확인하고, 업무 영향이 없을 때만 운영 환경에 단계적으로 반영합니다.
7. 정책의 소유자·목적·만료일을 기록하고, label 변경과 새 Pod 배포가 정책 선택 범위를 바꾸지 않는지 주기적으로 살펴봅니다.

## 흔한 차단 원인

| 증상 | 원인 후보 | 확인 방법 |
| --- | --- | --- |
| 정책을 만들었는데 트래픽이 계속 통과합니다. | CNI가 NetworkPolicy를 집행하지 않거나, 대상 Pod를 선택하지 못했거나, 다른 정책이 같은 방향의 연결을 허용할 수 있습니다. | CNI 지원 여부, Pod label, 적용 정책 전체와 정책 카운터를 확인합니다. |
| 웹에서 API로 연결되지 않습니다. | API ingress 정책 또는 웹 Pod egress 정책이 허용하지 않습니다. Namespace/Pod selector가 실제 label과 다를 수도 있습니다. | 출발 Pod와 도착 Pod에 적용되는 정책을 각각 확인합니다. |
| API는 DB에 연결되지만 DNS 이름은 해석하지 못합니다. | egress를 격리하면서 DNS를 허용하지 않았거나 DNS Pod label·Namespace가 클러스터와 다릅니다. | DNS Service의 실제 Endpoint, UDP와 TCP 53, NodeLocal DNSCache 구성을 확인합니다. |
| IP로 직접 호출할 때만 동작이 달라집니다. | Service NAT, 주소 변환, `ipBlock` 처리 시점이 CNI나 클라우드 구현에 따라 달라질 수 있습니다. | Pod IP, Service IP, 실제 목적지와 CNI 문서의 NAT 처리 조건을 대조합니다. |
| 일부 시스템 Pod만 통신이 끊깁니다. | 시스템 Namespace나 `hostNetwork` Pod에 표준 NetworkPolicy가 예상과 다르게 적용될 수 있습니다. | Kubernetes 버전·CNI별 hostNetwork 정책과 시스템 구성요소의 필요 통신을 확인합니다. |
| 차단 이유가 보이지 않습니다. | 표준 NetworkPolicy API에는 정책 허용·차단 로그 기능이 없습니다. | CNI의 flow observability와 정책 로그를 확인합니다. |

## 표준 API의 경계

Kubernetes 1.37 문서는 표준 NetworkPolicy API가 TLS 검사, 서비스 이름 직접 선택, 노드 신원 기반 정책, 클러스터 공통 경유지 강제, 네트워크 보안 이벤트 로깅, 명시적 deny 규칙을 제공하지 않는다고 설명합니다. 또한 Pod가 실행 중인 노드에서 오는 통신은 기본적으로 허용되므로, 표준 정책만으로 노드 자체의 접근을 막을 수 없습니다. 이 기능이 필요하면 Ingress·Gateway, 서비스 메시, 노드 방화벽, CNI 전용 확장 등을 검토해야 합니다. 추가 기능을 쓸 때에는 이식성이 줄어드는지와 해당 프로젝트의 실제 버전에서 지원되는지를 함께 확인합니다.

`hostNetwork` Pod의 정책 적용은 표준 문서상 동작이 정의되어 있지 않습니다. 대다수 플러그인 구현에서 노드 IP 트래픽과 구분되지 않을 수 있으므로, 일반 Pod에 적용한 정책이 `hostNetwork` Pod에도 동일하게 적용된다고 가정하지 않습니다.

## English summary

Kubernetes NetworkPolicy is an API for pod-level Layer 3/4 traffic control; a compatible CNI must enforce it. A pod is non-isolated by default until a policy selects it for ingress or egress. Policies are additive, and pod-to-pod traffic must be allowed by the source pod's egress policy and the destination pod's ingress policy. Egress isolation can break DNS unless the cluster's actual DNS path is explicitly allowed. Standard NetworkPolicy does not provide deny rules, policy logs, TLS inspection, or service-name targeting. The YAML is an unexecuted educational example; selectors, DNS labels, ports, and CNI behavior must be checked in the target cluster.

## 출처와 확인 범위

- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/), 공식 문서 v1.37, 2026년 11월 4일 확인. API 전제, 선택·격리, 정책 합집합, ingress와 egress 양쪽 허용, 기본 정책, DNS, 주소 변환, `hostNetwork`, 표준 API의 제한을 확인했습니다.
- [Cilium: Overview of Network Policy](https://docs.cilium.io/en/stable/security/policy/), Cilium 1.20.4 stable 문서, 2026년 11월 4일 확인. Kubernetes 표준 정책과 Cilium 전용 정책 리소스, L3/L4/L7 기능의 구분을 확인했습니다.
- [Calico: Enable a default deny policy for Kubernetes pods](https://docs.tigera.io/calico/latest/network-policy/get-started/kubernetes-default-deny), Calico 공식 문서, 2026년 11월 4일 확인. Kubernetes 기본 정책 동작, 전역 정책 적용 시 시스템 Namespace 예외, 단계적 시험을 확인했습니다.

정책 예시의 label·Namespace·포트와 통신 흐름은 이 문서를 위해 구성한 설명용 값입니다. YAML을 클러스터에 적용하거나 실제 CNI 동작을 검증하지 않았습니다.

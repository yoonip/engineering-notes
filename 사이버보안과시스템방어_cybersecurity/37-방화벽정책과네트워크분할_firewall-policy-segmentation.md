# 방화벽 정책과 네트워크 분할 운영 | Firewall Policy and Network Segmentation

자료 확인일: 2026-11-04

방화벽 운영은 포트를 열고 닫는 목록을 만드는 일에 그치지 않습니다. 어떤 업무 흐름이 왜 필요한지 확인하고, 필요한 연결만 허용하며, 규칙 변경이 실제 통신과 보안에 미친 영향을 확인하고, 더는 필요하지 않은 규칙을 없애는 과정입니다.

이 장은 사내망, 인터넷 공개 구역, 관리망, 서버망이 있는 조직을 가정한 교육 자료입니다. 주소와 포트는 설명용입니다. 특정 회사의 실제 네트워크나 특정 방화벽 제품의 설정을 옮긴 것이 아닙니다.

## 방화벽이 통제하는 것

방화벽은 서로 다른 보안 수준의 네트워크나 호스트 사이에서 통신 흐름을 허용하거나 차단합니다. 주소·프로토콜·포트만 확인하는 패킷 필터, 연결 상태를 추적하는 상태 기반 방화벽, 응용 계층의 요청까지 검사하는 게이트웨이 등 구현 방식에 따라 볼 수 있는 정보와 처리 비용이 다릅니다. 방화벽을 통과했다는 사실만으로 사용자 인증이나 응용프로그램의 권한 검사가 끝난 것은 아닙니다. [NIST SP 800-41 Rev. 1](https://csrc.nist.gov/pubs/sp/800/41/r1/final)은 방화벽 기술과 정책을 설명하고 선택·구성·시험·배포·관리 절차를 제시하지만 2009년 판입니다. 제품별 기능이나 오늘날의 기본 설정을 대신하는 자료로 사용하지 않습니다.

네트워크 분할은 시스템을 보안 요구와 역할에 따라 구역으로 나누고, 구역 사이 연결을 정책으로 제한하는 방법입니다. VLAN은 같은 물리 네트워크에서 논리적 브로드캐스트 영역을 나눌 수 있지만, VLAN만으로 두 구역 사이 트래픽이 차단되는 것은 아닙니다. 라우터 ACL, 상태 기반 방화벽, 호스트 방화벽, 클라우드 보안 규칙 등 실제 경계에서 정책이 적용되어야 합니다. 공개 서비스는 내부 업무망과 데이터베이스 사이에 DMZ를 두어 직접 연결을 줄일 수 있습니다. [CISA·FBI·NSA 및 국제 파트너의 네트워크 인프라 지침](https://www.cisa.gov/sites/default/files/2025-01/joint-guidance-enhanced-visibility-hardening-guide-for-comms-infrastructure-508c_0.pdf)은 기본 거부, 인바운드·아웃바운드 제어, 장비 역할별 분할, 별도 관리 구역과 전용 관리 단말을 권고합니다.

## 먼저 통신 흐름을 기록합니다

규칙을 만들기 전에 자산 목록과 실제 업무 흐름을 확인합니다. 방화벽 로그만으로는 사용하지 않는 연결, 특정 시간대에만 실행되는 백업, 장애 시에만 필요한 복구 경로를 놓칠 수 있으므로 서비스 담당자, 구성 문서, 네트워크 흐름 기록을 함께 살펴야 합니다.

| 출발 구역 | 도착 구역 | 업무와 예시 통신 | 정책의 의미 |
| --- | --- | --- | --- |
| 인터넷 | DMZ 역방향 프록시 | 웹 서비스 TCP 443 | 공개 웹 진입점만 허용합니다. |
| DMZ 역방향 프록시 | 응용 서버 | 서비스별 TCP 포트 | 프록시에서 승인된 응용 서버로만 전달합니다. 포트는 설계에 맞춰 정합니다. |
| 응용 서버 | 데이터베이스 구역 | 예: TCP 5432 | 해당 응용 서버에서 필요한 데이터베이스로만 연결합니다. |
| 사용자 단말 | 데이터베이스 구역 | 기본적으로 업무상 필요하지 않음 | 사용자 단말이 DB에 직접 접속하는 흐름은 차단하고 예외는 별도 승인합니다. |
| 관리용 단말 | 관리 구역의 장비 | 승인된 관리 프로토콜 | 인터넷이나 일반 사용자망에서 장비 관리면으로 바로 들어오지 못하게 합니다. |
| 내부 서버 | 인터넷 | DNS·시간 동기화·업데이트 등 승인된 목적 | 출발 서버와 목적지를 구체화하고 프록시·저장소 경유 여부를 정합니다. |

위 포트는 예시입니다. 예를 들어 5432는 PostgreSQL의 기본 포트로 알려져 있지만 조직이 실제로 사용하는 포트나 허용해야 할 서비스라는 뜻은 아닙니다. 서비스 포트는 제품 설정과 배포 구조에서 확인하고, 포트 번호만으로 연결의 정당성을 판단하지 않습니다.

각 규칙에는 최소한 고유 식별자, 출발·도착 구역과 자산, 방향, 프로토콜·포트, 업무 목적, 책임자, 승인 기록, 적용일, 재검토·만료일, 로그 정책, 변경 번호와 되돌리기 방법을 기록합니다. 주소 그룹 이름도 `any`, `servers` 같은 모호한 값보다 역할과 환경을 드러내도록 정합니다.

## 기본 거부와 상태 추적

기본 거부(default deny)는 별도로 허용하지 않은 트래픽을 차단하는 출발점입니다. 그러나 이를 운영 장비에 급히 적용하면 DNS, 인증, 모니터링, 백업, 원격 관리 경로가 끊겨 서비스 장애가 날 수 있습니다. 현재 흐름을 확인하고, 차단 영향을 시험하고, 관리 접속을 유지할 복구 절차를 준비한 뒤 적용합니다. 거부 로그는 이상 흐름을 찾는 데 유용하지만 모든 패킷을 무제한 기록하면 로그 폭주와 저장 비용 문제가 생길 수 있습니다. 이벤트를 집계·제한하고, 로그 유실 여부와 보관 정책도 확인합니다.

상태 기반 방화벽은 연결 추적 정보로 세션의 진행 상태를 판단합니다. 일반적으로 새 연결은 명시된 허용 규칙과 대조하고, 허용된 연결의 응답 패킷은 상태 정보를 통해 처리할 수 있습니다. 무상태 ACL은 각 방향의 패킷을 따로 검사하므로 양방향 규칙을 직접 설계해야 할 수 있습니다. `established` 상태 규칙을 무조건 추가하면 안 됩니다. 어느 방향·어느 구역 사이의 연결을 이어주는 규칙인지 제한해야 합니다.

## 규칙 생명주기

1. 자산·업무 담당자·서비스 흐름을 확인하고 필요한 통신을 수집합니다.
2. 출발지, 도착지, 프로토콜, 포트, 방향을 구체적으로 적고 업무상 필요와 책임자를 기록합니다.
3. 중복·가려진(shadowed) 규칙, 지나치게 넓은 대역, 사용되지 않는 규칙을 찾습니다. 규칙 우선순위와 일치 방식은 제품마다 다르므로 해당 장비의 문서를 확인합니다.
4. 변경안을 기존 정책과 비교하고 검토·승인합니다. 정책 분석 도구가 있다면 구문과 예상 영향뿐 아니라 다른 체인·라우팅·NAT 규칙과의 상호작용도 확인합니다.
5. 가능한 환경에서는 관찰 모드나 시험 구역에서 누락된 의존성을 확인한 뒤 단계적으로 배포합니다. CISA의 2025년 마이크로세그먼테이션 계획 지침은 대상 자산 선정, 의존성 확인, 정책 결정, 정책 시험과 배포를 반복하는 단계적 접근을 설명합니다. [CISA, Part One: Introduction and Planning](https://www.cisa.gov/sites/default/files/2025-07/ZT-Microsegmentation-Guidance-Part-One_508c.pdf)
6. 허용되어야 하는 정상 흐름과 차단되어야 하는 비정상 흐름을 모두 점검합니다. 카운터·로그·응용 상태·사용자 영향도 함께 확인합니다.
7. 규칙의 목적과 책임자가 사라졌거나 만료된 항목을 검토하고, 승인 절차를 거쳐 제거합니다. 설정 변경 이력은 장비 외부의 관리 저장소에도 남깁니다.

시험에서 정상 연결 하나가 성공했다는 사실은 정책 전체가 정확하다는 증거가 아닙니다. 반대로 차단 응답이 보이지 않는다고 해서 방화벽이 차단했다고 단정할 수도 없습니다. 라우팅 오류, 호스트 방화벽, 서비스 미기동, TLS 문제도 비슷한 증상을 만들 수 있으므로 양 끝단과 경로 장비의 관측값을 함께 봅니다.

## 관리망과 세분화

관리 인터페이스는 일반 업무 트래픽과 분리합니다. 가능하면 별도의 관리 네트워크를 두고, 전용 관리 단말에서 정해진 점프 경로를 통해서만 접속하게 합니다. 관리망에 접근할 수 있다는 이유로 그 안의 모든 장비 간 통신을 허용하지 않습니다. CISA 공동 지침은 운영 트래픽과 분리된 대역외 관리망, 장비 간 횡방향 관리 차단, 전용 관리 단말과 관리 구역을 권고합니다.

마이크로세그먼테이션은 기존 구역보다 작은 단위로 접근 정책을 적용하는 방식입니다. 고정 IP 대역만 사용하는 방식에서 호스트, 응용프로그램, 업무 흐름의 속성을 정책에 활용하는 방식까지 구현 범위가 다양합니다. 도구나 제품 하나를 설치한다고 자동으로 안전해지는 개념은 아닙니다. CISA는 IT·OT·IoT·클라우드를 포함한 환경별 선택지를 설명하고 조직의 자산·의존성·운영 영향에 맞춰 점진적으로 전환하도록 안내합니다. 세분화가 지나치면 정책 수와 유지 비용이 늘고, 의존성을 놓치면 장애가 발생하므로 작은 서비스 단위로 시작해 결과를 확인합니다.

## nftables 정책 예시

아래는 Linux nftables의 `inet` 전달 체인에서 문서용 주소를 사용해 한 방향의 새 TCP 연결만 허용하는 축소 예시입니다. 실제 네트워크 규칙 전체나 복사해 곧바로 적용할 수 있는 방화벽 설정이 아닙니다.

```nft
table inet lab_segmentation {
    chain forward {
        type filter hook forward priority filter; policy drop;
        ip saddr 192.0.2.0/24 ip daddr 198.51.100.20 tcp dport 443 ct state new accept
        ct state established,related accept
    }
}
```

- `table inet lab_segmentation`은 IPv4와 IPv6 규칙을 함께 둘 수 있는 `inet` 계열 표를 선언합니다. 이 예시의 규칙 본문은 IPv4 조건만 사용합니다.
- `chain forward`는 이 Linux 시스템을 통과하는 패킷을 검사하는 체인을 만듭니다. 로컬 프로세스의 입력·출력 체인과 다릅니다.
- `type filter hook forward priority filter; policy drop;`은 전달 지점의 필터 체인으로 연결하고, 명시적으로 허용되지 않은 패킷을 이 체인에서 버립니다.
- `ip saddr ... ip daddr ... tcp dport 443 ct state new accept`는 문서용 출발 주소 대역에서 문서용 서버 주소의 TCP 443으로 향하는 새 연결만 허용합니다.
- `ct state established,related accept`는 연결 추적에서 기존 연결 또는 관련 연결로 판정한 패킷을 허용합니다. 실제 구성에서는 적용 체인·구역·순서가 예상한 흐름인지 먼저 확인해야 합니다.

이 규칙은 예시 주소를 쓰므로 실제 호스트의 운영 네트워크를 나타내지 않습니다. nftables에서는 한 base chain의 `accept`가 다른 우선순위 체인의 후속 판단을 무효화하지 않을 수 있으며, `drop`은 전체 규칙 평가를 끝냅니다. 이미 존재하는 체인과 우선순위, 라우팅·NAT·IPv6 정책을 확인하지 않고 기본 거부 규칙을 추가하면 원격 접속이 끊길 수 있습니다. 이 문서의 코드는 특정 Linux 호스트에서 실행하거나 구문 검증하지 않았습니다. 적용이 필요하다면 격리된 실습 환경에서 현재 규칙을 백업하고, 문법 검사와 허용·차단 대조를 수행한 뒤에만 별도 변경 승인에 따라 진행해야 합니다. [nftables 공식 매뉴얼](https://netfilter.org/projects/nftables/manpage.html)은 base chain의 정책과 연결 추적 상태, 체인 평가 순서를 설명합니다.

## 장애를 좁히는 순서

| 증상 | 확인할 항목 | 해석할 때 주의할 점 |
| --- | --- | --- |
| 새 TCP 연결이 시간 초과됩니다. | 출발·도착 주소, 라우팅, 정책 카운터, 양쪽 방향의 패킷 관측, 서비스 listen 상태를 확인합니다. | 방화벽의 무응답 차단과 라우팅 단절은 증상이 같을 수 있습니다. |
| 연결은 되지만 응답이 돌아오지 않습니다. | 상태 기반 추적 여부, 비대칭 경로, 반대편 ACL, NAT 변환과 MTU를 확인합니다. | 연결 추적이 없는 장비에서는 응답 방향 규칙이 별도로 필요할 수 있습니다. |
| 한 응용 기능만 실패합니다. | 실제 호출 대상, 추가 포트, 이름 해석, 인증·TLS, 리다이렉트 경로를 확인합니다. | 대표 포트 하나를 허용했다고 응용 흐름이 모두 열리는 것은 아닙니다. |
| 정책 배포 뒤 관리 접속이 끊깁니다. | 대역외 콘솔·복구 계정·사전 백업·정책 자동 복구 절차를 확인합니다. | 원격 세션만 의지한 상태에서 기본 거부 정책을 바꾸지 않습니다. |
| 허용 규칙이 예상과 다르게 동작합니다. | 규칙 순서, 주소 객체 확장, 다른 base chain, NAT 전후 주소, 제품별 우선순위를 확인합니다. | 같은 키워드라도 공급사별 평가 모델과 로그 표시 방식이 다를 수 있습니다. |

## 적용 전 점검표

- 요청한 통신의 업무 목적과 소유자가 확인되었습니까?
- 출발지와 목적지가 필요한 자산으로 제한되어 있습니까?
- TCP/UDP와 포트가 실제 응용 설정·공식 문서와 일치합니까?
- 응답 경로와 DNS·시간 동기화·모니터링·백업 의존성을 확인했습니까?
- IPv4와 IPv6, 외부 인바운드와 내부 아웃바운드 정책을 각각 확인했습니까?
- 만료일·재검토일·로그·경보 기준을 정했습니까?
- 설정 백업, 콘솔 복구, 되돌리기 책임자와 영향 범위를 기록했습니까?
- 배포 뒤 정상 흐름과 금지 흐름을 둘 다 검증할 관측 지점이 있습니까?

## English summary

Firewall policy is an operational lifecycle: identify business flows, allow only required paths, review and deploy changes safely, observe both permitted and denied traffic, and retire obsolete rules. Network segmentation uses enforceable boundaries; VLANs alone do not block routed traffic. Management networks should be isolated, and microsegmentation should be introduced in phases after mapping dependencies. The nftables fragment is an unexecuted educational example with documentation-only IPv4 ranges, not a production ruleset. NIST SP 800-41 Rev. 1 is a 2009 foundational publication; current operational recommendations are cross-checked against CISA guidance published in 2024 and 2025 and the official nftables manual.

## 출처와 확인 범위

- [NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy](https://csrc.nist.gov/pubs/sp/800/41/r1/final), 2009년 9월. 공식 발행 페이지의 범위·초록 및 방화벽 정책 지침을 확인했습니다. 오래된 판본임을 밝혔으며 현대 제품별 설정 기준으로 사용하지 않았습니다.
- [Enhanced Visibility and Hardening Guidance for Communications Infrastructure](https://www.cisa.gov/sites/default/files/2025-01/joint-guidance-enhanced-visibility-hardening-guide-for-comms-infrastructure-508c_0.pdf), CISA·NSA·FBI·ASD ACSC·CCCS·NCSC-NZ, 2024년 12월 3일. 기본 거부 ACL, 인바운드·아웃바운드 통제, DMZ·VLAN 분할, 대역외 관리망, 변경 감시 부분을 확인했습니다.
- [The Journey to Zero Trust: Microsegmentation in Zero Trust, Part One: Introduction and Planning](https://www.cisa.gov/sites/default/files/2025-07/ZT-Microsegmentation-Guidance-Part-One_508c.pdf), CISA, 버전 1.0, 2025년 7월 29일. 마이크로세그먼테이션의 범위, 후보 자산·의존성 파악, 정책 선택·시험·단계적 배포 부분을 확인했습니다.
- [nftables manual](https://netfilter.org/projects/nftables/manpage.html), Netfilter 프로젝트 공식 매뉴얼, 2026년 11월 4일 확인. `inet` 계열, base chain의 정책·hook·priority, 연결 추적 상태와 accept/drop 평가 규칙을 확인했습니다.

이 문서는 위 출처의 내용을 요약하고 설명을 위해 예시 흐름과 설정 조각을 직접 작성했습니다. 코드는 실제 방화벽 장비나 Linux 호스트에서 실행하지 않았습니다.

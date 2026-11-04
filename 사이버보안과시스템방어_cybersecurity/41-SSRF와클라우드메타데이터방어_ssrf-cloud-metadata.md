# SSRF와 클라우드 메타데이터 접근 통제 | SSRF and Cloud Metadata Protection

자료 확인일: 2026-11-04

사용자가 입력한 URL을 서버가 대신 열어 주는 기능은 이미지 미리보기, 문서 가져오기, webhook 검사, 외부 데이터 가져오기 등에 쓰입니다. 서버 측 요청 위조(SSRF, Server-Side Request Forgery)는 이 기능이 허용된 목적지를 벗어나 내부 서비스나 클라우드 메타데이터 서버에 요청하게 되는 취약점입니다. 서버는 내부망 연결 권한과 서비스 계정 권한을 갖고 있을 수 있으므로, 브라우저에서 같은 주소를 여는 것보다 영향이 커질 수 있습니다.

SSRF가 항상 응답 내용을 공격자에게 보여 주는 것은 아닙니다. 응답을 읽는 기능이 있으면 데이터 노출로, 응답을 감추더라도 서버의 outbound 요청이 가능하면 내부 서비스에 대한 행위나 네트워크 탐지 신호로 이어질 수 있습니다. 구체적 영향은 서버가 닿을 수 있는 네트워크, 실행 권한, 요청 기능과 응답 반환 방식에 따라 달라집니다.

## 서버가 대신 요청할 때 바뀌는 신뢰 경계

```text
사용자 입력: URL 또는 대상 선택
             │
             ▼
응용 서버의 URL 파서·정책 검사
             │
             ▼
DNS 조회 → 서버 HTTP client → 내부·외부 대상
             │                         │
             └──── 응답 또는 부작용 ────┘
```

문제는 인터넷 사용자가 내부 네트워크에 직접 연결할 수 있느냐만이 아닙니다. 요청을 대신 보내는 애플리케이션이 내부망 라우팅, 관리 서비스 접근, 인스턴스 역할 자격 증명 등 추가 권한을 갖고 있다면 그 권한이 혼동된 대리자(confused deputy)처럼 사용될 수 있습니다. OWASP는 URL 파싱, redirect 처리, 도메인 검증, DNS rebinding, 응답 처리와 네트워크 제한을 함께 살펴보도록 안내합니다. [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

| 사용 기능 | 서버가 하는 일 | 확인할 위험 |
| --- | --- | --- |
| 이미지·문서 미리보기 | 입력한 주소에서 리소스를 내려받습니다. | 임의 목적지 접속, 큰 파일·압축 폭탄, 응답 본문의 정보 노출이 가능한지 확인합니다. |
| webhook 등록·시험 | 사용자가 지정한 주소로 이벤트나 시험 요청을 보냅니다. | 외부 공개 주소만 허용하는지, 사설망·관리 endpoint를 막는지, POST 본문과 인증 정보를 제한하는지 확인합니다. |
| URL 가져오기·변환 | 서버가 HTML·PDF·이미지 등을 읽어 다른 형식으로 처리합니다. | HTTP 외 scheme, redirect, DNS 재조회, 문서 변환기·파서의 추가 네트워크 접근을 확인합니다. |
| 내부 서비스 연동 | 정해진 서비스에 요청을 보냅니다. | 사용자 입력이 서비스 이름·경로·인증 헤더를 덮어쓰지 않는지, 호출 권한이 필요한 API로 제한됐는지 확인합니다. |

## URL 문자열 검사는 목적지 검사가 아닙니다

`문자열에 localhost가 있는가`와 같은 부분 문자열 검사는 목적지 통제를 대신하지 못합니다. URL 문법은 scheme, 사용자 정보, host, port, path, encoding과 IPv4·IPv6 표기를 포함하고, 각 언어의 파서가 값을 다르게 정규화할 수 있습니다. 정규식으로 URL 전체를 판별하는 대신 유지보수되는 URL parser를 사용하고, 파싱된 scheme·host·port를 기능 요구와 비교합니다. OWASP는 목적지 목록이 정해져 있다면 allowlist를 우선하고, 허용 도메인만 확인하는 것으로 DNS rebinding까지 해결됐다고 보지 말라고 설명합니다.

검사 이후 HTTP client가 별도 DNS 질의를 하여 다른 주소로 연결하면 검사한 목적지와 실제 연결한 주소가 달라질 수 있습니다. DNS 응답은 IPv4와 IPv6를 모두 확인하고, 조직이 허용한 주소 범위와 대조합니다. 그 다음에는 검사한 주소로 실제 연결을 고정하되 TLS 인증서 검증과 SNI, HTTP Host에는 원래 허용된 호스트 이름을 사용해야 합니다. 사용 중인 client가 이 동작을 안전하게 보장하는지 공식 문서에서 확인합니다. 이 부분은 URL 문자열 검사만으로 처리하기 어려우므로 네트워크 egress 제한과 함께 적용합니다. [OWASP SSRF Prevention Cheat Sheet의 DNS pinning 설명](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

## 안전한 URL 가져오기 흐름

아래는 제어 지점을 보여 주기 위한 의사코드입니다. `parse_url`, `resolve_all`, `fetch_pinned`는 특정 라이브러리의 실제 API가 아니며, 이 저장소에서 실행한 코드도 아닙니다. 실제 구현은 사용하는 URL parser·DNS resolver·HTTP client의 공식 문서와 운영 네트워크 정책에 맞춰야 합니다.

```text
target = parse_url_with_maintained_library(user_input)  # 표준 parser가 입력을 URL 구성요소로 나눕니다.
require(target.scheme == "https")                       # 기능에 필요한 scheme만 허용합니다.
require(exact_allowlist.contains(target.host, target.port))  # 부분 문자열이 아닌 등록된 host와 port를 비교합니다.
addresses = resolve_all(target.host)                    # A와 AAAA 응답을 모두 얻습니다.
require(addresses and all(policy.allows(ip) for ip in addresses))  # 모든 목적지가 정책 허용 범위인지 확인합니다.
response = fetch_pinned(target, addresses, redirects=False, limits=policy)  # 검증된 주소에 연결하고 redirect·응답 한도를 적용합니다.
return transform_to_expected_format(response)           # 원문 응답을 그대로 노출하지 않고 필요한 데이터만 반환합니다.
```

이 흐름은 SSRF 방어를 위한 설계 예시이며, 단독으로 프로덕션 코드를 구성하지 않습니다. 특히 `fetch_pinned`가 검증된 주소로 연결하면서 호스트명 기반 TLS 인증을 계속 수행하는지, retry나 fallback에서도 새 목적지를 다시 검사하는지 확인해야 합니다. URL이 외부로 redirect될 수 있다면 기본적으로 자동 추적을 끄고, 제품 요구상 redirect가 필요할 때에는 매 단계마다 목적지·주소·scheme 정책을 다시 적용합니다.

## 클라우드 메타데이터는 자격 증명 경계입니다

인스턴스 메타데이터는 VM의 설정이나 실행 환경 정보를 제공하고, 일부 플랫폼에서는 workload identity 자격 증명 발급에 쓰입니다. 따라서 메타데이터 endpoint는 단순한 내부 웹페이지가 아니라 해당 VM이나 workload의 신원과 권한으로 이어지는 경계입니다. 메타데이터에서 얻을 수 있는 권한의 범위는 연결된 역할·서비스 계정의 정책에 따라 달라지므로, endpoint 보호와 권한 최소화를 같이 적용해야 합니다.

| 플랫폼 | 공식 문서에서 확인한 접근 방식 | 보안 설계에서 볼 점 |
| --- | --- | --- |
| AWS EC2 IMDS | IMDSv2는 먼저 세션 token을 발급받고 이후 metadata 요청에 token을 포함합니다. 인스턴스를 token 필수로 설정하면 IMDSv1 요청은 허용되지 않습니다. 기본 token 응답 hop limit은 1이며 컨테이너가 접근해야 하는 구성에서는 호환성을 시험해야 합니다. | IMDSv2를 요구하고, 인스턴스 역할에는 필요한 작업만 허용합니다. hop limit 변경은 컨테이너 접근 경로와 공격면에 영향을 주므로 실제 배치에서 검증합니다. IMDSv2는 중요한 방어 계층이지만 애플리케이션의 임의 URL 요청이나 egress 제한을 대신하지 않습니다. |
| Google Compute Engine | 메타데이터 서버는 VM 내부 프로세스에서 접근할 수 있습니다. Google 문서는 메타데이터에 쓴 민감 정보와 서비스 계정 token에 접근할 수 있는 프로세스를 제한하고, 덜 신뢰하는 코드를 권한 있는 서비스 계정이 붙은 VM에서 실행하지 않도록 안내합니다. | VM에 부착된 서비스 계정 권한을 최소화하고, 사용자가 제공한 코드·변환 worker를 별도로 격리합니다. GKE metadata concealment도 보호 범위가 제한되며 `hostNetwork` Pod 등 적용 조건을 따로 확인해야 합니다. |
| Microsoft Azure IMDS | VM 내부의 비라우팅 주소에서 제공되며 요청에 `Metadata: true`가 있어야 하고 `X-Forwarded-For`는 없어야 합니다. | 이 헤더 조건은 요청 형식을 확인하는 방어 조치입니다. 애플리케이션이 임의 header를 보낼 수 있는 구조라면 이것만으로 SSRF가 차단된다고 보지 말고, URL 정책과 네트워크 egress를 적용합니다. |

출처: [AWS IMDS 문서](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) · [Google VM metadata 보안 고려사항](https://docs.cloud.google.com/compute/docs/metadata/overview) · [Google 서비스 계정 보안 모범 사례](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts) · [GKE metadata 보호 범위](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/protecting-cluster-metadata) · [Azure IMDS](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service)

## 계층별 방어

### 제품 기능과 응용 코드

- 임의 URL을 받지 않아도 되는 기능이면 URL 대신 내부 resource ID나 사전에 등록한 대상 ID를 받습니다.
- 외부 공개 웹 전체에 접근해야 하는 요구가 없다면 scheme·host·port를 명시적 allowlist로 제한합니다. 서브도메인을 허용할 때에는 문자열 접미사 비교가 아니라 도메인 label 경계를 확인합니다.
- URL parser 결과를 사용하고 userinfo, 예상하지 않은 port, scheme, IP literal, 비표준 encoding과 정규화 차이를 점검합니다.
- 자동 redirect는 끕니다. redirect가 제품 요구라면 매 hop마다 동일한 목적지 검사를 적용하고 횟수·총 응답 크기에 제한을 둡니다.
- connect/read timeout, 최대 응답 크기, 압축 해제 크기와 처리 시간을 제한합니다. 다운로드한 HTML·이미지·PDF·XML은 별도의 parser sandbox에서 처리하고, 원문 응답을 사용자에게 그대로 반사하지 않습니다.
- HTTP client가 proxy 환경변수, retry, IPv6 fallback, redirect, DNS 캐시를 어떻게 처리하는지 확인하고 정책에서 벗어나는 fallback을 허용하지 않습니다.

### 네트워크와 실행환경

- 다운로드·미리보기 기능은 권한이 있는 업무 서비스와 같은 네트워크에 두지 말고 별도 worker·서브넷·container security boundary로 격리합니다.
- egress는 기본 차단하고 기능상 필요한 목적지만 열어 둡니다. 단순히 알려진 metadata IP 몇 개를 막는 denylist만으로 보호하지 않습니다.
- 외부 URL fetcher에서 loopback, 사설 IPv4·IPv6, link-local, metadata endpoint, 내부 DNS 관리망, 제어 plane과 운영 포트로 가는 경로가 차단되는지 확인합니다.
- 공용 인터넷을 허용해야 한다면 전용 egress proxy를 두고 이름 해석, 연결 IP, port, redirect와 응답 크기를 한 지점에서 정책화합니다. proxy 자체가 내부 서비스에 연결할 권한은 최소화합니다.
- workload identity·VM role·서비스 계정 권한을 좁히고, 임시 token이나 비밀을 URL-fetch worker와 공유하지 않습니다.

## 허용된 환경에서의 검증표

아래 항목은 본인 소유의 스테이징 환경에서 수행할 검증 계획입니다. 이 문서를 작성하면서 실제 클라우드 계정이나 서버에 요청을 보내지 않았고, 표의 결과를 통과한 것으로 보고하지 않습니다.

| 시험 | 확인 내용 | 통과 기준 |
| --- | --- | --- |
| 허용된 정상 URL | URL parser, host·port allowlist, TLS 이름 검증 | 정해진 서비스의 기대 리소스만 가져옵니다. |
| 허용되지 않은 scheme·port·host | 앱의 정책 거부와 outbound 흐름 로그 | 네트워크 요청 전에 거부하거나 egress 경계에서 차단합니다. |
| redirect 응답 | redirect 자동 추적 여부와 다음 목적지 검증 | 기본 정책은 redirect를 따르지 않으며, 허용한 경우 각 목적지를 다시 검사합니다. |
| DNS A·AAAA 결과 변화 | 검사 때의 DNS 결과와 실제 연결 주소 | 연결은 검증한 주소에 고정되며 승인되지 않은 IPv4·IPv6 주소로 바뀌지 않습니다. |
| timeout·대용량·압축 응답 | 응답시간·수신 byte·압축 해제 크기·worker 자원 | 사전 설정한 한도에서 중단되고 worker가 계속 요청을 처리할 수 있습니다. |
| 메타데이터 경계 | fetch worker와 정상 workload에서 metadata 접근 범위 | fetch worker에는 필요한 identity가 없고, 불필요한 metadata 경로는 차단됩니다. |
| 로그와 응답 반환 | URL 자격 정보, header, 응답 본문, cloud token 노출 | 비밀이 로그·오류 응답·사용자 화면에 기록되지 않습니다. |

테스트 결과에는 실행 환경, 이미지·SDK·HTTP client 버전, DNS·egress 정책과 시각을 기록합니다. 정상 기능이 깨지지 않는지와 금지 대상이 실제 연결에서 차단되는지를 함께 확인합니다.

## 이상 징후가 확인되었을 때

1. 어떤 기능이 어떤 원본 URL을 받고 실제로 어느 IP·port로 연결했는지 application·DNS·egress 로그를 대조합니다. 로그에 secret query, Authorization, Cookie와 응답 본문이 남지 않도록 관리합니다.
2. 호출 계정이나 role에서 사용하지 않는 권한을 제거하고, metadata 접근이 의심되면 해당 workload에 발급된 자격 증명을 공급자 절차에 따라 교체·폐기합니다.
3. URL-fetch 기능의 outbound를 임시 제한하고, 내부 endpoint와 공용 endpoint별 실제 기능 요구를 확인한 뒤 allowlist를 단계적으로 복구합니다.
4. 보안 그룹이나 앱 차단만으로 원인을 해결했다고 결론 내리지 말고, parser·DNS·redirect·HTTP client·네트워크 경계를 다시 확인합니다.
5. 영향을 받은 자원과 cloud audit 기록을 보존하고 사고 대응 절차에 따라 범위와 접근 이력을 조사합니다.

## 앞 장과의 연결

[웹과 API의 입출력](05-웹과API의입출력_web-api.md)은 SSRF를 여러 입력 취약점 중 하나로 소개합니다. 이 장에서는 실제 URL fetch 기능을 앱 parser, DNS, HTTP client, egress, 클라우드 신원으로 나눠 자세히 연결합니다. [클라우드와 컨테이너](08-클라우드와컨테이너_cloud-containers.md)의 IAM·격리 원칙, [비밀정보 수명주기와 CI 자격 증명](28-비밀정보수명주기와CI자격증명_secrets-lifecycle.md)의 최소 권한과도 함께 읽으시면 됩니다.

## English summary

Server-Side Request Forgery (SSRF) occurs when a server-side fetch feature is induced to contact destinations outside its intended scope. Validate parsed scheme, exact host and port; verify resolved IPv4 and IPv6 destinations at connection time; revalidate redirects; and constrain egress from an isolated fetch worker. Cloud metadata services can expose workload identity credentials, so provider-specific controls such as AWS IMDSv2 are defense in depth, not a substitute for least privilege and network isolation. The pseudocode is conceptual and was not executed.

## 출처와 확인 범위

- [OWASP Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), OWASP 공식 방어 지침, 2026년 11월 4일 확인. 허용 목록, URL·도메인 검사, redirect 비활성화, DNS rebinding과 metadata 서비스 위험을 확인했습니다.
- [Amazon EC2: Use the Instance Metadata Service to access instance metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html), AWS 공식 사용자 안내, 2026년 11월 4일 확인. IMDSv2의 세션 token, token 필수 설정, TTL, 기본 hop limit과 컨테이너 호환 조건을 확인했습니다.
- [Amazon EC2: Configure the Instance Metadata Service options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-options.html), AWS 공식 사용자 안내, 2026년 11월 4일 확인. 계정·AMI·인스턴스 설정 우선순위와 hop limit 범위, 설정 적용 시 주의사항을 대조했습니다.
- [Google Cloud: About VM metadata](https://docs.cloud.google.com/compute/docs/metadata/overview), Google Cloud 공식 문서, 2026년 11월 4일 확인. metadata endpoint, VM 내부 접근과 민감 metadata 취급을 확인했습니다.
- [Google Cloud: Best practices for using service accounts securely](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts), Google Cloud 공식 IAM 지침, 2026년 11월 4일 확인. VM에서 실행되는 프로세스가 metadata server로 서비스 계정 token을 요청할 수 있는 신뢰 범위를 확인했습니다.
- [Google Kubernetes Engine: Protecting cluster metadata](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/protecting-cluster-metadata), GKE 공식 문서, 2026년 11월 4일 확인. metadata concealment의 보호 대상과 제한, `hostNetwork` Pod 적용 조건을 확인했습니다.
- [Microsoft Azure: Instance Metadata Service for virtual machines](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service), Microsoft Learn 공식 문서, 2026년 11월 4일 확인. VM 내부 접근 범위와 `Metadata: true`, `X-Forwarded-For` 관련 요청 조건을 확인했습니다.

의사코드는 OWASP 방어 원칙을 바탕으로 이 문서에서 직접 구성한 설계 흐름이며 특정 라이브러리·제품의 코드가 아닙니다. 스테이징 검증표는 실행 계획이고 측정·통과 기록이 아닙니다.

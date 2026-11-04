# 리버스 프록시와 WAF의 신뢰 경계 | Reverse Proxy and WAF Trust Boundaries

자료 확인일: 2026-11-04

웹 요청이 CDN이나 Web Application Firewall(WAF)을 거쳐 원본 서버로 들어오면, 원본 서버의 TCP 연결 상대는 실제 방문자가 아니라 바로 앞의 프록시일 수 있습니다. 이때 실제 방문자 주소·원래 요청 호스트·접속 프로토콜을 전달하는 HTTP 헤더는 중요한 정보지만, 클라이언트가 직접 보낸 값일 수도 있습니다. 프록시를 신뢰할 범위와 헤더를 다시 쓰는 위치를 정하지 않으면 접속 기록, IP 기반 제한, 감사 자료가 공격자 입력에 좌우됩니다.

이 장은 리버스 프록시와 WAF를 사용하는 웹 서비스의 요청 경계, 원본 서버 우회, 전달 헤더, WAF 규칙 운영을 설명합니다. NGINX·OWASP CRS·Cloudflare 설정은 각 프로젝트의 예시로 구분하며, 이 문서의 설정 조각은 실행하지 않은 교육용 예시입니다.

## 요청은 여러 개의 연결로 전달됩니다

```text
방문자 ── TLS 연결 1 ──▶ CDN·WAF ── TLS 연결 2 ──▶ 리버스 프록시 ── 내부 연결 ──▶ 응용 서버
   │                         │                           │                         │
클라이언트 요청         엣지 규칙·필터             헤더 정리·경로 전달          인증·권한·업무 처리
```

TLS가 CDN에서 종료되면 방문자와 CDN 사이, CDN과 원본 서버 사이에 각각 별도의 TLS 연결이 생길 수 있습니다. 두 구간 모두 암호화하더라도 애플리케이션이 전송한 원본 데이터는 중간 종단점에서 처리됩니다. 따라서 방문자와 원본 서버 사이에 하나의 끝까지 이어지는 TLS 세션이 있다고 표현하지 않습니다. 예를 들어 Cloudflare의 Full (strict)은 Cloudflare와 원본 서버 사이 연결에서 원본 인증서를 확인하는 모드이고, Authenticated Origin Pulls는 원본 서버가 해당 연결에서 클라이언트 인증서를 확인하도록 추가합니다. [Cloudflare Full (strict)](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/) · [Authenticated Origin Pulls](https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/)

프록시가 있는 경로에서는 세 종류의 주소를 구분해야 합니다.

| 값 | 보통 어디서 확인합니까 | 잘못 해석하면 생기는 문제 |
| --- | --- | --- |
| TCP 연결 상대 주소 | 서버 소켓의 원격 주소 | 프록시 주소만 보여 실제 방문자가 드러나지 않을 수 있습니다. |
| 전달된 방문자 주소 | `Forwarded`, `X-Forwarded-For`, 공급사 전용 헤더 등 | 요청에 헤더를 넣은 클라이언트가 값을 조작할 수 있습니다. |
| 원래 host·scheme 정보 | `Forwarded: host/proto`, `X-Forwarded-Host/Proto` 등 | 잘못 신뢰하면 외부 링크 생성, 리디렉션, 쿠키 보안 속성, 가상 호스트 판정이 틀어질 수 있습니다. |

## 전달 헤더는 그 자체로 증명이 아닙니다

표준 `Forwarded` 헤더는 프록시가 전달 과정에서 바뀌거나 사라질 수 있는 정보의 형식을 정의합니다. RFC 7239는 이 헤더가 요청을 만든 클라이언트를 포함해 경로상의 모든 노드에 의해 변경될 수 있어 그 값만 믿을 수 없다고 명시합니다. 알려진 프록시를 검증하고 신뢰 목록에 등록하더라도 그 프록시 앞에서 기록된 전체 주소 사슬이 모두 진짜라는 보증은 아닙니다. 프록시 사이 전송도 보호해야 합니다. [RFC 7239 §4, §8](https://www.rfc-editor.org/rfc/rfc7239.html)

안전한 처리 순서는 다음과 같습니다.

1. 원본 서버에 직접 접속할 수 있는 주체를 방화벽·보안 그룹·사설 연결로 제한합니다.
2. 원본 서버는 실제 연결 상대가 사전에 정한 프록시 주소인지 확인하고, 그 프록시가 제공하는 헤더만 신뢰합니다.
3. 인터넷에서 받은 `Forwarded`·`X-Forwarded-*`를 첫 신뢰 경계에서 제거하거나 검증된 값으로 덮어씁니다. 프록시가 받은 임의 헤더를 그대로 통과시키지 않습니다.
4. 프록시가 여러 대라면 연결 경로와 누가 어떤 헤더를 추가·정리하는지 문서화합니다. 원본은 임의로 헤더의 가장 왼쪽 값이나 한 개의 특정 항목을 방문자 주소로 선택하지 않습니다.
5. 응용프로그램은 연결 출발지를 IP 허용 목록이나 사용자 권한의 유일한 근거로 쓰지 않습니다. IP는 위험 신호나 보조 통제일 수 있지만 인증·인가를 대체하지 않습니다.

`Forwarded`와 `X-Forwarded-For`는 개인의 접속 주소나 내부 프록시 구조를 노출할 수 있으므로 필요한 정보만 전달하고, 로그 보관 기간과 접근 권한도 제한합니다. [RFC 7239의 보안·개인정보 고려사항](https://www.rfc-editor.org/rfc/rfc7239.html#section-8)

## NGINX의 신뢰 프록시 예시

NGINX `ngx_http_realip_module`은 신뢰하도록 설정한 주소에서 온 요청에 한해 지정 헤더를 기준으로 클라이언트 주소를 바꿔 기록할 수 있습니다. 이 모듈은 빌드에 기본 포함되지 않을 수 있습니다. 아래의 `192.0.2.0/24`는 문서 예시용 주소 대역이므로 실제 프록시 주소로 사용할 수 없습니다.

```nginx
# 아래 주소는 문서용입니다. 실제로는 직접 연결 가능한 프록시 대역만 등록합니다.
set_real_ip_from 192.0.2.0/24;
# 신뢰 프록시가 정리해 전달하는 방문자 주소 헤더를 지정합니다.
real_ip_header X-Forwarded-For;
# 오른쪽에서 왼쪽으로 신뢰 프록시를 건너뛰고 마지막 비신뢰 주소를 찾습니다.
real_ip_recursive on;
```

`set_real_ip_from`에 인터넷 전체를 넣으면 공격자가 자기 헤더를 보낼 때까지 모두 신뢰하는 셈이 되어 보호가 무너집니다. 실제 구성에서는 프록시·로드밸런서가 사용하는 IPv4와 IPv6 범위를 공급자 공식 문서와 네트워크 설정에서 확인하고, 변경된 대역의 반영을 관리합니다. `real_ip_recursive on`은 알려진 전달 경로에 맞는 주소 선택을 돕지만, 앞단 프록시가 공격자 입력을 그대로 두면 잘못된 주소를 취할 수 있으므로 헤더 정리 절차가 먼저 필요합니다. [NGINX `ngx_http_realip_module` 공식 문서](https://nginx.org/en/docs/http/ngx_http_realip_module.html)

## 원본 서버로 WAF를 우회하지 못하게 합니다

요청이 WAF를 통과해 원본 서버에 도착해도 원본 주소가 인터넷에 열려 있으면 공격자가 원본 IP를 찾아 WAF를 거치지 않고 요청할 수 있습니다. DNS 기록, 메일 서버, 과거 레코드 등에서 원본 주소가 노출될 수 있으므로 주소를 숨기는 것만으로는 부족합니다. 원본 인바운드를 필요한 프록시·파트너의 경로로 제한하고, 관리·상태 확인·백업 경로는 공개 웹 경로와 별도로 설계합니다.

Cloudflare 공식 문서는 원본 보호 방법으로 Cloudflare IP 범위 허용, Authenticated Origin Pulls의 mTLS, Cloudflare Tunnel 등을 설명합니다. IP 범위 허용은 Cloudflare에서 오는 통신인지 확인하는 네트워크 층의 통제이며, 문서도 IP 스푸핑 가능성을 한계로 표시합니다. 기본 전역 Origin Pull 인증서는 Cloudflare 네트워크에서 왔는지 확인하지만 특정 고객 계정만의 인증서는 아니므로 더 좁은 신뢰가 필요하면 자체 인증서를 사용하는 구성을 검토해야 합니다. 이는 Cloudflare 제품의 동작 예시이며 모든 CDN에 같은 설정이 있다고 일반화하지 않습니다. [Cloudflare 원본 서버 보호](https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server/) · [Cloudflare Authenticated Origin Pulls 설명](https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/explanation/)

원본 접근을 제한할 때는 IPv4와 IPv6, 모든 공개 서비스 이름, 테스트 서버, DNS 전용 레코드, 장애 전환 주소, 운영자 접근과 모니터링을 함께 확인합니다. 허용 범위를 바꾸기 전에는 프록시와 원본 사이 연결을 점검하고, 원본에 직접 접근하려는 요청이 실제로 거부되는지 승인된 환경에서 확인합니다.

## WAF의 탐지와 애플리케이션 보안은 서로 다른 통제입니다

WAF는 HTTP 요청과 응답을 검사해 알려진 패턴, 프로토콜 위반, 크기·빈도 조건 등에 따라 기록·차단하는 응용 계층 통제입니다. 계정 권한이 잘못된 요청, 업무 규칙 위반, 서비스 내부의 모든 취약점을 자동으로 해결하지 않습니다. 정상 요청이 공격 패턴과 비슷해 차단되는 오탐(false positive)도 생길 수 있고, 규칙에 걸리지 않는 공격이 통과하는 미탐(false negative)도 가능하므로 WAF의 차단 결과만으로 애플리케이션이 안전하다고 결론 내리지 않습니다.

OWASP Core Rule Set(CRS)은 ModSecurity 및 호환 WAF에서 사용하는 일반 공격 탐지 규칙입니다. CRS는 규칙 매칭을 바로 차단하는 대신 거래의 이상 점수를 누적한 뒤 임계값과 비교할 수 있습니다. 이때 임계값을 무작정 높이면 정상 차단이 줄어드는 대신 탐지된 공격도 통과할 수 있습니다. 오탐은 해당 서비스의 정상 동작과 일치하는지 확인한 뒤 필요한 경로·매개변수·규칙에 한정한 예외로 조정합니다. CRS 규칙 파일 자체를 직접 수정하면 업데이트 과정에서 수정 내용이 사라지거나 유지보수 어려움이 생길 수 있습니다. [OWASP CRS 이상 점수](https://coreruleset.org/docs/2-how-crs-works/2-1-anomaly_scoring/) · [OWASP CRS 오탐 조정](https://coreruleset.org/docs/2-how-crs-works/2-3-false-positives-and-tuning/)

WAF 규칙을 바꿀 때에는 요청 경로·메서드·콘텐츠 유형별로 정상 사용 사례를 정하고, 차단 로그의 규칙 ID와 매치 위치를 함께 기록합니다. 광범위한 규칙 묶음을 끄기보다는 특정 정상 입력에 대해서만 최소 범위로 예외를 만듭니다. 예외에는 이유, 소유자, 검토일, 규칙 업데이트 뒤 재시험 항목을 연결합니다. 로그에 비밀번호·세션 토큰·결제정보·본문 원문이 포함되지 않도록 수집 필드와 마스킹도 정합니다.

## 배포 뒤 확인할 대조 흐름

아래 항목은 승인된 시험용 서비스와 테스트 계정에서 점검할 기준입니다. 이 저장소에서 실제 웹 서버나 WAF에 요청을 보내 검증한 것은 아닙니다.

| 확인할 흐름 | 기대 결과 | 실패할 때 볼 곳 |
| --- | --- | --- |
| 실제 방문자가 프록시를 통해 정상 요청을 보냅니다. | 원본은 신뢰 경계에서 정리된 방문자 메타데이터를 기록합니다. | 프록시의 헤더 덮어쓰기, NGINX 신뢰 주소 목록, IPv4·IPv6 경로를 확인합니다. |
| 방문자가 거짓 `X-Forwarded-For` 값을 직접 보냅니다. | 앞단 프록시가 해당 값을 제거·교체하며 감사·속도 제한 판단에 쓰이지 않습니다. | 프록시가 외부 제공 헤더를 그대로 전달하는지 확인합니다. |
| 인터넷에서 원본 IP로 직접 연결을 시도합니다. | 원본의 공개 웹 서비스가 직접 요청을 받지 않거나, 프록시 인증 경계에서 거부합니다. | 보안 그룹·호스트 방화벽·IPv6 규칙·누락된 공개 DNS 레코드를 확인합니다. |
| WAF가 차단한 합법적 업로드·검색 요청을 시험합니다. | 규칙 ID와 매치 위치를 특정하고 필요한 최소 범위만 예외 처리합니다. | 요청 본문 검사 한도, 콘텐츠 유형, 애플리케이션 처리 방식, CRS 규칙과 예외 배치를 확인합니다. |
| 다른 경로·메서드·정상 사용자 요청을 회귀 확인합니다. | 예외 적용 뒤 다른 경로의 공격 탐지와 업무 흐름이 유지됩니다. | 전역 규칙 해제, 지나치게 넓은 URI/매개변수 예외, 캐시·인증 프록시를 확인합니다. |

## 운영 인계 항목

- 공개 DNS와 원본 IP 노출 경로를 누가 점검하는지 정합니다.
- 신뢰 프록시의 주소 범위와 갱신 출처, 적용 책임자, 실패 시 되돌리기를 기록합니다.
- 연결 상대 주소와 전달 헤더의 출처를 로그에서 구분합니다.
- WAF 엔진·룰셋·판본·탐지 임계값·예외 목록을 구성 관리에 포함합니다.
- WAF 예외가 추가되면 보안 담당자와 응용 서비스 소유자가 함께 필요성을 검토합니다.
- 직접 원본 요청 차단, 헤더 스푸핑 무시, 정상 요청 유지 결과를 변경 기록에 남깁니다.

## English summary

Reverse proxies create multiple network and TLS hops. Forwarded client metadata is an HTTP input, not proof of identity; trust only known proxies, sanitize client-supplied forwarding headers at the edge, and prevent direct origin access that bypasses the WAF. NGINX real-IP settings must list only actual trusted proxy ranges. WAF rule sets can produce false positives and false negatives, so tune narrow exclusions, protect sensitive logs, and keep application authorization and validation in place. The configuration is an unexecuted educational example.

## 출처와 확인 범위

- [RFC 7239: Forwarded HTTP Extension](https://www.rfc-editor.org/rfc/rfc7239.html), 2014년 6월, Standards Track. `Forwarded` 형식과 프록시 사슬, 헤더 무결성·개인정보 고려사항 §4·§8을 확인했습니다.
- [NGINX `ngx_http_realip_module`](https://nginx.org/en/docs/http/ngx_http_realip_module.html), 공식 매뉴얼, 2026년 11월 4일 확인. `set_real_ip_from`, `real_ip_header`, `real_ip_recursive`, 모듈 빌드 조건을 확인했습니다.
- [OWASP CRS Anomaly Scoring](https://coreruleset.org/docs/2-how-crs-works/2-1-anomaly_scoring/) 및 [False Positives and Tuning](https://coreruleset.org/docs/2-how-crs-works/2-3-false-positives-and-tuning/), CRS 공식 문서, 2026년 11월 4일 확인. 누적 점수와 차단 임계값, 오탐 조정, 예외 범위와 규칙 파일 직접 수정의 유지보수 위험을 확인했습니다.
- [Cloudflare Protect your origin server](https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server/), 2026년 10월 2일 갱신. 원본 IP 노출, 네트워크 허용 목록, mTLS Origin Pulls, Tunnel 등 제품별 선택지와 한계를 확인했습니다.
- [Cloudflare Authenticated Origin Pulls](https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/) 및 [작동 설명](https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/explanation/), 2026년 11월 4일 확인. 원본 서버의 클라이언트 인증서 검증, 전역 인증서와 계정 전용 인증서 차이를 확인했습니다.
- [Cloudflare Full (strict)](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/), 2026년 11월 4일 확인. Cloudflare와 원본 서버 사이 TLS 및 원본 인증서 확인 범위를 확인했습니다.

출처는 실제로 확인한 판본과 설명 범위를 표시했습니다. NGINX 설정 조각의 주소 대역은 문서용으로 직접 구성했으며 실제 서버에서 구문 검사나 요청 검증을 하지 않았습니다.

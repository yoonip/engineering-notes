# DNSSEC와 암호화 DNS, 도메인 운영 | DNSSEC, encrypted DNS and domain operations

자료 확인일: 2026-11-04

## 이 장에서 다루는 범위

DNS는 사람이 읽는 도메인 이름을 IP 주소와 여러 서비스 정보에 연결합니다. DNS 응답이 잘못 바뀌면 웹 접속뿐 아니라 메일 수신, 서비스 탐색, TLS 인증서 발급 경로까지 영향을 받을 수 있습니다. 이 장에서는 DNSSEC, DNS over TLS(DoT), DNS over HTTPS(DoH), CAA를 서로 다른 보호 수단으로 구분하고, 도메인 계정과 서명 키를 운영할 때 확인할 사항을 정리합니다.

[TLS 인증서와 PKI 운영](32-TLS인증서와PKI운영_tls-certificates-pki-operations.md)은 인증서 경로와 서비스 이름을 확인합니다. 이 장은 그보다 앞선 이름 해석과 도메인 등록·위임 경계를 다룹니다. DNSSEC와 암호화 DNS가 서로 대신할 수 없는 이유를 먼저 구분해야 합니다.

## DNS 이름을 찾는 경로

브라우저나 운영체제의 stub resolver는 보통 재귀 resolver에 질의합니다. 재귀 resolver는 캐시를 확인한 뒤 필요한 경우 root, 최상위 도메인, 권한 있는 서버를 차례로 찾아 답을 가져옵니다. 권한 있는 서버는 해당 zone의 원본 레코드를 제공합니다. 실제 환경에는 기업 내부 DNS, VPN, 전달 resolver가 끼어들 수 있으므로 장애를 조사할 때는 어느 resolver에 질의했는지부터 확인합니다.

    응용프로그램 → stub resolver → 재귀 resolver → root → TLD → 권한 있는 DNS 서버
                              ↘ 캐시된 응답 또는 내부 전달 resolver

DNS는 A·AAAA 주소 레코드 외에도 CNAME 별칭, MX 메일 서버, TXT 정책, NS 위임, DS·DNSKEY 서명 연결, CAA 인증서 발급 정책을 전달합니다. 응답의 출처와 무결성, 전송 중 기밀성, 도메인 관리 계정의 안전성은 각각 별개의 문제입니다.

## 네 가지 보호 수단은 목적이 다릅니다

| 수단 | 보호하는 구간·속성 | 확인하는 주체 | 해결하지 못하는 문제 |
| --- | --- | --- | --- |
| DNSSEC | 서명된 DNS 데이터의 출처와 무결성 | DNSSEC 검증을 수행하는 재귀 resolver | DNS 질의 기밀성, 가용성, 계정 탈취, 잘못된 원본 데이터 |
| DoT | DNS client와 선택한 resolver 사이의 전송 기밀성과 채널 인증 | TLS 연결을 맺는 DNS client | resolver 이후의 모든 경로, 원본 zone의 정확성, resolver 운영자의 질의 열람 |
| DoH | DNS 질의·응답을 HTTPS 교환으로 전달 | HTTPS client와 선택한 DoH resolver | DoT와 같은 범위 밖의 신뢰 문제, resolver 운영자의 질의 열람 |
| CAA | 인증기관이 특정 도메인 인증서를 발급할 수 있는지 제한 | 인증서를 발급하려는 CA | 이미 발급된 인증서의 검증, DNSSEC나 계정 보안, CA 자체의 오발급 전부 |

DNSSEC는 응답 데이터가 서명된 zone에서 왔고 전송 중 바뀌지 않았는지 검증하도록 돕습니다. DoT와 DoH는 사용자의 질의가 로컬 네트워크 구간에서 평문으로 보이거나 변조되는 위험을 줄입니다. 다만 암호화 DNS를 쓰더라도 선택한 resolver는 질의 이름을 처리하므로, 어느 resolver를 신뢰하는지와 조직의 로깅·정책을 함께 고려해야 합니다. DoH는 HTTPS를 이용하므로 네트워크에서 일반 웹 HTTPS와 구별하기 어려울 수 있지만, 이것이 모든 관찰·정책 통제를 없앤다는 뜻은 아닙니다.

## DNSSEC 신뢰 사슬

DNSSEC는 공개키 기반 서명으로 DNS 레코드 집합(RRset)의 출처와 무결성을 검증합니다. DNSKEY는 zone의 공개키를 담고, RRSIG는 해당 RRset에 대한 서명을 담습니다. 부모 zone은 자식 zone의 DNSKEY를 가리키는 DS 레코드를 게시합니다. resolver는 이미 신뢰하는 root trust anchor에서 시작해 부모의 서명된 DS, 자식 DNSKEY, 그리고 실제 응답의 RRSIG까지 연결을 확인합니다.

    root trust anchor
      ↓ root가 서명한 TLD의 DS
    TLD DNSKEY ── 서명된 DS ──→ 자식 zone DNSKEY
      ↓ 자식 zone DNSKEY가 서명 검증
    A/AAAA/MX 등 RRset + RRSIG

DS는 공개키 원문을 복사해 두는 레코드가 아니라 자식 DNSKEY의 요약값(digest)을 부모 zone에 연결하는 레코드입니다. 따라서 자식 zone에서 키를 교체할 때 부모의 DS와 자식의 DNSKEY가 서로 맞는 시점과 캐시 만료 시간을 고려해야 합니다. DNS 운영자가 DS를 잘못 입력하거나 키 교체를 순서에 맞지 않게 하면, 검증 resolver는 서명된 도메인의 답을 bogus로 판단해 일반적으로 SERVFAIL을 돌려줄 수 있습니다.

DNSSEC 검증 결과는 단순히 성공·실패 두 가지가 아닙니다. 검증 가능한 서명 사슬이 맞는 secure, 서명하지 않은 zone이라 검증 사슬이 없는 insecure, 서명은 주장하지만 검증이 실패하는 bogus, 정보가 부족해 판정할 수 없는 indeterminate 상태가 있습니다. insecure라는 결과는 그 zone이 악성이라는 뜻이 아니며, DNSSEC 검증을 거친 것이 아니라는 뜻입니다.

DNSSEC는 응답의 의미가 올바른지 판단하지 않습니다. 서명 키를 가진 운영자가 악성 주소를 정상적으로 서명해 게시하면 DNSSEC는 그 응답이 해당 zone의 서명된 데이터임을 확인할 뿐입니다. DNSSEC는 질의 암호화, DNS 서버 가용성, 도메인 계정 복구, 레지스트라 침해 방지 기능도 제공하지 않습니다.

## 서명 키와 부모 DS를 안전하게 교체하기

DNSSEC 운영에서 긴급 장애로 이어지기 쉬운 작업은 Key Signing Key(KSK) 또는 Combined Signing Key(CSK) 교체입니다. 부모 DS가 아직 새 키를 가리키지 않는데 이전 키를 먼저 제거하거나, 새 키의 DS를 잘못 게시하면 서로 다른 resolver 캐시가 서로 다른 키 상태를 갖는 동안 검증이 실패할 수 있습니다.

일반적인 안전 원칙은 새 키와 기존 키를 겹쳐 게시하고, 부모 DS 반영과 기존 DNSKEY·DS 캐시의 TTL이 지난 것을 확인한 뒤 이전 키를 제거하는 것입니다. 정확한 순서와 대기 시간은 서명 도구, 부모 zone, registrar, TTL, 자동화 정책에 따라 달라집니다. 공급자 콘솔에서 임의로 DS를 지우거나 DNSSEC를 껐다 켜는 방식은 장애 범위를 넓힐 수 있으므로, 해당 DNS 플랫폼의 key rollover 절차와 변경 승인 계획을 기준으로 진행합니다.

서명 유효 기간을 지나치게 짧게 두거나 서명 자동 갱신이 중단되어도 검증은 실패합니다. 서명 생성 시스템과 검증 resolver의 시각이 크게 어긋나는 경우에도 RRSIG의 inception·expiration 시간 검사가 실패할 수 있습니다. NTP 상태, signer 작업 성공 여부, zone serial, 권한 서버 간 데이터 일치, RRSIG 남은 유효 시간을 함께 관측해야 합니다.

| 증상 | 먼저 확인할 항목 | 안전한 확인 방법 |
| --- | --- | --- |
| 일부 네트워크에서만 SERVFAIL | 사용하는 재귀 resolver, 부모 DS, 자식 DNSKEY, TTL 캐시 | 여러 resolver와 권한 서버의 DS·DNSKEY 응답을 비교하고 검증 로그를 확인합니다. |
| DNSSEC를 켠 뒤 전체 도메인 응답 실패 | trust anchor와 root DNSKEY 검증 상태, resolver 시각 | resolver 로그와 독립 검증 도구를 확인합니다. 원인을 모른 채 검증을 끄지 않습니다. |
| 키 교체 직후 서비스 장애 | 새 DS가 부모에 게시됐는지, 모든 권한 서버가 새 키를 제공하는지 | 공급자의 rollover 상태와 DS/DNSKEY 조회를 확인하고 이전 키·DS 삭제 시점을 점검합니다. |
| 큰 응답에서만 시간 초과 | EDNS 크기, UDP 조각화, 방화벽과 TCP fallback | DNSSEC 레코드가 포함된 응답의 크기와 UDP/TCP 경로를 네트워크 운영자와 점검합니다. |
| 인증서 발급 시 CAA 오류 | CAA 응답, DNSSEC 검증, 권한 DNS의 CAA 처리 | 인증기관 로그와 authoritative DNS 응답을 비교합니다. CAA 오류를 우회하도록 정책을 비우지 않습니다. |

## CAA는 인증서 발급 단계의 제한입니다

CAA 레코드는 도메인 보유자가 공개 CA 중 누가 해당 이름의 인증서를 발급할 수 있는지 선언하는 DNS 정책입니다. 예를 들어 조직이 사용하는 CA만 허용하도록 설정하면, 다른 CA가 발급을 요청할 때 정책에 따라 발급을 거부해야 합니다. CA는 인증서에 들어갈 각 DNS 이름의 관련 CAA 정책을 확인합니다.

CAA는 필요하지만 인증서 발급을 완전히 보장하거나 차단하는 유일한 조건은 아닙니다. CAA에 허용 CA가 적혀 있어도 도메인 제어 확인, CA 정책, 인증서 사용자의 서버 설정은 별도로 검증해야 합니다. 반대로 CAA를 변경해도 이미 발급된 인증서가 자동으로 폐기되거나 client 검증에서 무효가 되지 않습니다. RFC 8659는 relying party가 CAA를 인증서 검증 수단으로 사용하지 않도록 구분합니다.

인증서를 발급하는 공급자가 바뀌거나 와일드카드 인증서를 추가할 때에는 현재 배포 중인 인증서와 자동 갱신 계정이 모두 허용 목록에 들어 있는지 확인합니다. CAA 변경은 DNS 위임이나 DNSSEC 서명 상태를 함께 점검하고, 발급 시험은 실제 운영 인증서에 영향을 주지 않는 staging 환경에서 먼저 진행합니다.

## 도메인 계정과 DNS 변경 경계

DNSSEC 서명은 registrar 계정 탈취를 막지 못합니다. 공격자가 도메인 관리 계정이나 DNS 공급자 API 키를 확보하면 NS, DS, A/AAAA, MX, CAA 같은 레코드를 바꾸거나 도메인 이전을 시도할 수 있습니다. 도메인 관리 계정은 일반 웹 계정과 분리해 관리하고, 제공되는 MFA·강한 고유 암호·접근 로그·변경 알림을 사용합니다. 도메인 이전 잠금이나 registry lock은 무단 이전을 줄이는 추가 통제이지만, 계정 탈취나 registrar 자체의 침해까지 막는 만능 잠금은 아닙니다.

높은 영향의 도메인은 registrar 계정, DNS 관리 계정, 자동화 API 자격 증명을 각각 분리하고, API 토큰의 zone 범위와 작업 권한을 제한합니다. 이름 서버·DS·CAA·MX 변경 알림을 받을 연락처를 실제로 감시하는 메일 계정으로 유지합니다. 등록 만료, 결제 수단, 소유자 연락처, 복구 절차도 정기적으로 확인합니다. 기업은 변경 승인자와 비상 연락망을 정하고, DNS 외부 관측 지점에서 예상 레코드와 변경 여부를 감시할 수 있습니다.

계정 침해가 의심되면 먼저 registrar와 DNS 공급자의 세션·API 키를 폐기하거나 회전하고, 소유권 및 연락처 복구 절차를 시작합니다. 변경 전후의 NS·DS·주소·MX·CAA 기록과 감사 로그를 보존합니다. DNS가 가리킨 서버와 메일 경로가 바뀌었는지 조사하고, 관련 TLS 인증서가 새로 발급됐는지 CT 로그와 CA 계정에서 확인합니다. 정상 상태로 보이는 DNS 응답이 돌아왔더라도 기존 세션·인증서·메일 전달 설정이 안전하다고 바로 결론 내리면 안 됩니다.

## 읽기 전용 진단 명령

아래 명령은 DNS를 조회하는 진단 예시입니다. 실제 도메인 변경이나 서명 작업을 수행하지 않습니다. 공개 DNS의 응답과 로컬 resolver 정책은 환경에 따라 다를 수 있으므로 출력만으로 운영 상태를 단정하지 않습니다.

    dig example.com A
    dig example.com A +dnssec
    dig example.com DS
    dig example.com DNSKEY +dnssec
    dig example.com CAA
    delv example.com A

첫 명령은 현재 설정된 resolver에 A 레코드를 묻습니다. +dnssec는 DNSSEC 관련 데이터를 요청하는 DO 표시를 설정하는 질의 옵션이며, 이 옵션을 썼다는 사실만으로 dig가 전체 신뢰 사슬을 직접 검증했다는 뜻은 아닙니다. DS와 DNSKEY 조회는 부모와 자식의 공개 레코드를 비교할 때 씁니다. CAA 조회는 발급 정책 레코드가 응답되는지 확인합니다. BIND의 delv는 DNSSEC 검증을 수행하는 진단 프로그램입니다. 사용하는 resolver, trust anchor, 네트워크 경로에 따라 결과 해석이 달라질 수 있습니다.

검증 resolver에서 SERVFAIL이 나면 먼저 같은 질의를 +cd 옵션으로 한 번 더 보낼 수 있습니다. BIND 문서에 설명된 진단 방식으로, +cd는 해당 재귀 resolver에 응답 검증을 중단하도록 요청합니다. 이때만 응답이 돌아온다면 DNSSEC 검증 문제를 의심할 단서가 됩니다. 보안 검사를 우회해 서비스 복구에 쓰는 방법으로 취급하면 안 되며, parent DS·DNSKEY·RRSIG·resolver 시각과 로그로 원인을 찾아야 합니다.

## 운영 전후 점검

- registrar·registry·DNS 호스팅 사업자와 각 계정의 관리 책임자를 기록합니다.
- 계정의 MFA, 고유 암호, 복구 연락처, 감사 로그와 변경 알림을 확인합니다.
- NS·DS·DNSKEY·RRSIG·CAA·A/AAAA·MX 레코드의 현재 운영값과 변경 승인자를 문서화합니다.
- DNSSEC 적용 전 parent DS 등록 절차, signer 장애 복구, key rollover와 만료 감시를 시험합니다.
- DoT·DoH resolver를 선택할 때 사업자, 개인정보 정책, 장애 시 fallback, 기업 필터와 로그 요구사항을 검토합니다.
- CAA에는 실제 운영·갱신에 필요한 CA와 인증서 유형을 포함하고, 사용하지 않는 발급 권한은 제거합니다.
- 정상·오류 도메인 응답을 서로 다른 검증 resolver에서 확인하고, 실패 시 담당자에게 알리는 경보를 구성합니다.
- 긴급 변경 뒤에는 DNS 응답뿐 아니라 웹 인증서, 메일 수신, 내부 서비스 검색까지 확인합니다.

## English summary

DNSSEC authenticates signed DNS data and protects its integrity when a validating resolver checks the chain from a trust anchor through parent DS and child DNSKEY records. It does not encrypt queries, provide availability, or protect registrar accounts. DNS over TLS and DNS over HTTPS protect the client-to-resolver transport, while the selected resolver still handles the query. CAA constrains certificate issuance by participating CAs; it does not validate or revoke already-issued certificates. Safe operations require controlled key rollovers, accurate parent DS records, monitored signatures, protected registrar accounts, and read-only diagnostics that distinguish a query option from actual DNSSEC validation.

## 출처

- [RFC 1034, Domain Names — Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034.html), §2·§4: DNS 이름 공간과 질의 구조입니다.
- [RFC 1035, Domain Names — Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035.html), §3·§4: DNS 메시지와 기본 레코드입니다.
- [RFC 4033, DNS Security Introduction and Requirements](https://www.rfc-editor.org/rfc/rfc4033.html), §3·§4·§5: DNSSEC가 제공하는 인증·무결성과 제공하지 않는 기밀성·가용성입니다.
- [RFC 4034, Resource Records for the DNS Security Extensions](https://www.rfc-editor.org/rfc/rfc4034.html), §2·§3: DNSKEY·RRSIG·DS 레코드 형식입니다.
- [RFC 4035, Protocol Modifications for the DNS Security Extensions](https://www.rfc-editor.org/rfc/rfc4035.html), §4·§5: 검증 resolver 동작과 인증 상태입니다.
- [RFC 9364, DNS Security Extensions (DNSSEC)](https://www.rfc-editor.org/rfc/rfc9364.html), §1·§2: DNSSEC 핵심 규격과 현재 표준 참조입니다.
- [RFC 7858, Specification for DNS over TLS](https://www.rfc-editor.org/rfc/rfc7858.html), §1·§3: TLS 기반 DNS 전송과 세션입니다.
- [RFC 8310, Usage Profiles for DNS over TLS and DNS over DTLS](https://www.rfc-editor.org/rfc/rfc8310.html), §5·§6: 암호화 DNS 연결의 resolver 인증 방식입니다.
- [RFC 8484, DNS Queries over HTTPS](https://www.rfc-editor.org/rfc/rfc8484.html), §3·§8·§10: HTTPS DNS 교환, 프라이버시, 운영 고려사항입니다.
- [RFC 8659, DNS Certification Authority Authorization](https://www.rfc-editor.org/rfc/rfc8659.html), §1·§3·§4: CAA 발급 정책, CA 처리, relying party 검증과의 구분입니다.
- [BIND 9 DNSSEC Guide](https://bind9.readthedocs.io/en/stable/dnssec-guide.html), Validation·Working with the Parent Zone·Basic DNSSEC Troubleshooting: DS 교체, SERVFAIL 진단, delv와 DNSSEC 운영 예입니다. BIND의 설명과 예시는 BIND 구현에 대한 안내로 사용했습니다.
- [Australian Cyber Security Centre, Domain Name System security for domain owners](https://www.cyber.gov.au/publication/domain-name-system-security-for-domain-owners): 도메인 계정 MFA·접근 로그·변경 알림·이전 잠금의 역할과 한계입니다.
- [ICANN SSAC SAC-044, A Registrant’s Guide to Protecting Domain Name Registration Accounts](https://www.icann.org/en/groups/ssac/documents/sac-044-en.pdf): 등록 계정 보호와 도메인 관리 절차입니다.

출처는 2026-11-04에 확인했습니다. 표준의 규범 요구와 BIND의 구현 안내를 구분했으며, 명령은 동작을 설명하는 진단 예시입니다. 실제 zone을 대상으로 실행하거나 변경했다는 의미는 아닙니다.

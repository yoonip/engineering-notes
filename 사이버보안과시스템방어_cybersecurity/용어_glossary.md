# 보안 용어 | Security glossary

[목차](README.md)

| 용어 | 이 자료에서의 뜻 |
| --- | --- |
| 자산 / Asset | 보호할 데이터·계정·키·장치·서비스입니다. |
| 공격 표면 / Attack surface | 공격자가 입력하거나 권한을 사용할 수 있는 접점입니다. |
| 취약점 / Vulnerability | 의도하지 않은 접근·변경·방해를 가능하게 하는 결함입니다. |
| 익스플로잇 / Exploit | 취약점이 실제 영향을 일으키게 사용하는 방법·코드입니다. |
| 최소권한 / Least privilege | 필요한 대상·행위·시간만 허용하는 원칙입니다. |
| 신뢰 경계 / Trust boundary | 입력이나 주체가 갖는 신뢰·권한이 달라지는 지점입니다. |
| 인증 / Authentication | 주체가 주장하는 신원을 확인하는 과정입니다. |
| 인가 / Authorization | 그 주체가 이 자원에 이 작업을 할 수 있는지 판정합니다. |
| OAuth 2.0 | 사용자가 허용한 scope에 따라 client가 보호된 API에 접근하도록 권한을 위임하는 protocol입니다. 그 자체로 로그인 사용자 신원 claim을 표준화하지는 않습니다. |
| OpenID Connect / OIDC | OAuth 2.0 위에 사용자 인증과 신원 claim 전달을 추가하는 protocol입니다. 인증 결과를 ID Token으로 전달합니다. |
| ID Token | OIDC client가 인증 결과와 subject claim을 확인하는 token입니다. issuer·audience·서명·만료와 요청에 사용한 nonce를 검증합니다. |
| Access token | resource server에 API 접근 권한을 제시하는 자격 증명입니다. 발급자·대상·scope를 확인하며 사용자 로그인 정보로 대신 쓰지 않습니다. |
| Refresh token | authorization server에 새 access token을 요청하는 자격 증명입니다. 공개 client에서는 회전 또는 sender constraint, 만료와 폐기를 관리합니다. |
| PKCE | `code_verifier`의 변환값을 authorization 요청에 묶어 authorization code를 다른 client가 교환하지 못하게 하는 OAuth 확장입니다. |
| `state` | 시작한 OAuth 요청과 callback을 연결하는 transaction 값입니다. 예측하기 어렵고 transaction·browser session에 안전하게 묶어 확인합니다. |
| `nonce` | OIDC 인증 요청과 ID Token을 연결하는 값입니다. 요청에서 보낸 값과 ID Token claim을 대조해 응답 재사용을 줄입니다. |
| BFF / Backend for Frontend | browser 앱을 위한 server-side component가 OAuth token을 보관하고 API 요청을 대신 전달하는 구조입니다. browser는 cookie session으로 BFF에 요청합니다. |
| OAuth mix-up attack | client가 여러 authorization server를 사용할 때 응답의 발급자를 잘못 연결해 code나 token을 엉뚱한 server에 보내는 공격입니다. |
| 패스키 / Passkey | FIDO 표준에 기반한 공개키 인증 자격 증명입니다. discoverable passkey는 사용자가 계정 이름을 먼저 입력하지 않아도 인증기에서 선택할 수 있습니다. 동기화형과 기기 고정형이 있습니다. |
| WebAuthn | 브라우저·인증기·relying party가 공개키 credential을 등록하고 검증하는 W3C 웹 인증 API와 사양입니다. |
| relying party / RP | WebAuthn credential을 등록한 뒤 인증 응답을 검증하는 서비스입니다. |
| RP ID | credential의 사용 범위를 묶는 relying party의 도메인 식별자입니다. 응답의 `rpIdHash`가 서버 설정과 일치해야 합니다. |
| user handle | relying party가 credential과 계정을 연결하기 위해 정하는 불투명한 계정 식별자입니다. discoverable credential 인증에서 반환될 수 있으므로 이메일·사용자 이름 같은 개인정보를 넣지 않습니다. |
| WebAuthn challenge | 서버가 ceremony마다 생성하는 신선도 값입니다. transaction과 연결하고 응답 검증 후 재사용하지 않습니다. |
| UP / User Present | 사용자가 인증기에 참여했다는 WebAuthn flag입니다. 사용자 신원을 기기에서 확인했다는 뜻인 UV와 구별합니다. |
| UV / User Verified | 인증기가 PIN·생체 확인 등으로 사용자를 로컬에서 확인했다는 WebAuthn flag입니다. 서비스가 요구하는 정책에 맞춰 요청·검증합니다. |
| 동기화형 패스키 / Syncable passkey | passkey provider가 여러 기기에서 이용할 수 있도록 credential을 동기화하는 방식입니다. provider 계정의 보안과 복구 경로도 보호 경계에 들어옵니다. |
| 기기 고정형 패스키 / Device-bound passkey | 한 보안 키나 기기에 묶여 다른 기기로 복원되지 않는 방식입니다. 분실에 대비한 추가 인증기와 복구 절차가 필요합니다. |
| BE / Backup Eligibility | WebAuthn credential이 다른 기기로 백업될 수 있도록 만들어졌는지를 나타내는 고정 속성입니다. |
| BS / Backup State | 동기화 가능한 credential의 현재 백업 상태를 나타내며 바뀔 수 있습니다. |
| attestation | 등록 시 인증기 특성에 관한 증거를 제공하는 WebAuthn 데이터입니다. 공개 서비스에서는 개인정보 영향과 기기 지원 범위를 고려합니다. |
| `signCount` | 일부 인증기가 assertion마다 갱신하는 서명 횟수입니다. 복제 탐지의 보조 신호이며 불일치만으로 복제를 확정하지 않습니다. |
| X.509 인증서 | 공개키·서비스 식별자·용도·기간을 발급자의 서명으로 묶은 인증 자료입니다. 유효성은 신뢰 경로와 client의 용도·이름 검증 정책에 따라 판단합니다. |
| PKI / Public Key Infrastructure | 공개키 인증서를 발급·검증·갱신·폐기하고 신뢰 anchor를 배포하는 조직·기술·운영 체계입니다. |
| CA / Certification Authority | 정책에 따라 인증서 서명·발급·폐기 정보를 관리하는 인증기관입니다. CA 서명만으로 인증서에 적힌 모든 내용을 무조건 신뢰하지는 않습니다. |
| trust anchor | client가 미리 신뢰하도록 설정한 인증 경로의 시작점입니다. Root CA 인증서 또는 별도로 구성한 공개키가 될 수 있습니다. |
| intermediate CA | trust anchor와 서비스 인증서 사이에서 하위 인증서를 발급하는 CA입니다. 서버는 client가 경로를 구성하는 데 필요한 중간 인증서를 보낼 수 있습니다. |
| SAN / subjectAltName | 인증서의 DNS 이름·IP 주소 등 서비스 식별자를 담는 X.509 확장입니다. TLS client는 접속한 이름에 맞는 SAN을 검증합니다. |
| ACME | 도메인 제어 확인과 인증서 발급·갱신·폐기 요청을 자동화하는 protocol입니다. |
| HTTP-01 / DNS-01 | ACME에서 HTTP challenge 경로나 DNS TXT record로 도메인 제어를 증명하는 방식입니다. |
| CRL / Certificate Revocation List | CA가 폐기한 인증서의 serial 정보를 모아 배포하는 목록입니다. client가 실제로 확인하는지는 구현·정책에 달려 있습니다. |
| OCSP | client가 특정 X.509 인증서의 폐기 상태를 확인할 수 있도록 하는 protocol입니다. |
| Certificate Transparency / CT | 공개 TLS 인증서 발급 기록을 append-only log에 남겨 운영자가 잘못 발급된 certificate를 발견하도록 돕는 체계입니다. log 기록 자체가 오발급을 막거나 certificate를 폐기하지는 않습니다. |
| mTLS / Mutual TLS | TLS client와 server 양쪽이 인증서를 제시하고 peer를 인증하는 연결 방식입니다. 인증 결과와 애플리케이션의 작업 권한은 별도로 판단합니다. |
| ACL | 자원에 접근할 수 있는 주체·작업을 정한 접근 제어 목록입니다. |
| IAM | 사용자·서비스의 신원과 자원 접근 정책을 관리하는 체계입니다. |
| tenant | 서비스에서 분리해 관리하는 고객·조직의 단위입니다. |
| scope | 토큰·역할 등에 허용한 작업 범위입니다. |
| 해시 / Hash | 바이트 입력을 정해진 길이 값으로 대응시키며 암호화와 다릅니다. |
| HMAC | 공유 비밀키를 사용하는 메시지 인증 코드입니다. |
| 전자서명 / Digital signature | 개인키로 서명하고 대응 공개키로 검증하는 인증 기법입니다. |
| nonce | 암호·프로토콜이 요구한 재사용 제한을 지켜 사용하는 값입니다. |
| salt | 비밀번호 검증값을 사용자별로 다르게 만드는 공개 난수입니다. |
| replay | 과거에 유효했던 메시지를 다시 사용하려는 행위입니다. |
| CVE / CWE | 각각 공개 취약점 식별자와 결함 유형의 분류 체계입니다. |
| SAST / DAST / SCA | 각각 정적 코드 검사·실행 서비스 검사·의존성 분석입니다. |
| fuzzing | 많은 입력을 만들어 실패·새 경로를 탐색하는 시험입니다. |
| oracle | 시험 결과가 맞는지 판정하는 독립 기대값·규칙입니다. |
| RAG | 검색한 외부 자료를 모델 입력에 연결하는 구조입니다. |
| 프롬프트 주입 | 공격자 자료의 지시가 시스템의 의도와 충돌하며 동작에 영향을 주는 문제입니다. |
| guardrail | 입력·출력·도구·정책 위반을 제한하는 통제입니다. 통제마다 범위가 다릅니다. |
| poisoning / backdoor | 자료·학습을 오염시키는 공격과 특정 조건의 원치 않는 동작을 심는 공격을 구분합니다. |
| SBOM / provenance | 구성요소 목록과 빌드 출처·과정의 근거를 구분합니다. |
| TEE / attestation | 보호된 실행 환경과 측정·신원을 확인하는 증명 절차를 구분합니다. |
| OT | 제조·발전·운송 등 물리 공정의 감시·제어 기술입니다. |
| 정밀도 / 재현율 | 각각 경보 중 실제 양성의 비율과 실제 양성 중 탐지한 비율입니다. |
| 화이트햇·블랙햇·그레이햇 | 보안 활동의 성격을 가리키는 관용어이며, 대상 소유자의 시험 허가를 대신하지 않습니다. |
| 모의침투 / Penetration test | 합의한 대상·기법·기간 안에서 공격 경로와 통제를 평가하는 보안 시험입니다. |
| 범위 / Scope | 시험이 허용된 시스템·계정·시간·기법·자료 처리·중단 조건입니다. |
| password spraying | 여러 계정에 적은 수의 비밀번호 후보를 분산해 시도하는 공격 유형입니다. |
| credential stuffing | 다른 곳에서 유출된 사용자명·비밀번호 조합을 재사용하는 공격 유형입니다. |
| 오프라인 비밀번호 추측 | 탈취된 비밀번호 검증값에 후보를 대조하는 행위로, 로그인 서버의 속도 제한만으로 막을 수 없습니다. |
| CVSS v4 | 취약점 심각도·위협·환경을 표현하는 FIRST의 공통 점수 체계입니다. Base 점수만으로 조직 위험을 뜻하지 않습니다. |
| EPSS | 공개 CVE가 향후 30일 동안 실제 악용 관측 대상이 될 확률을 추정하는 점수입니다. 자산 영향이나 완전한 위험 점수는 아닙니다. |
| ASVS / WSTG | 각각 애플리케이션 검증 요구사항과 웹 보안 시험 가이드를 제공합니다. |
| 취약점 공개 정책 / VDP | 취약점 보고 접수·범위·연락·처리를 안내하는 소유자 정책입니다. |
| AD DS | Windows Server의 Active Directory Domain Services로, 디렉터리 객체와 도메인 인증·정책을 관리합니다. |
| Tier 0·1·2 | Microsoft AD DS 계층 모델에서 각각 신원 제어면, 서버·업무 서비스, 사용자 단말·지원 업무를 구분하는 관리 신뢰 영역입니다. 다른 제품의 역할 구분과 동일하다고 단정하지 않습니다. |
| PAW | Privileged Access Workstation의 약자로, 특정 권한 계층의 관리 업무에 전용하는 강화된 작업 단말입니다. |
| 유효 권한 / Effective permissions | 직접 권한뿐 아니라 중첩 그룹·위임·서비스 계정·관리 도구를 통해 실제로 행사할 수 있는 권한입니다. |
| MDM / EMM | 각각 모바일 기기 관리와 기업 이동성 관리입니다. 기기 등록·구성·앱·업무 데이터 정책의 범위는 제품과 조직 정책에 따라 다릅니다. |
| MASVS / MASTG / MASWE | 각각 OWASP 모바일 앱 보안 검증 표준, 시험 가이드, 모바일 앱 약점 목록입니다. MASVS는 백엔드 API의 전면 검증을 대신하지 않습니다. |
| 딥링크 / Deep link | URL이나 앱 간 호출로 앱의 특정 화면·기능을 여는 경로입니다. 전달된 식별자만으로 서버 권한을 부여해서는 안 됩니다. |
| 인증서 고정 / Certificate pinning | 앱이 정상적인 시스템 인증서 검증에 추가로 특정 인증서나 공개키 조건을 확인하는 방식입니다. 키 회전과 장애 복구 계획이 필요합니다. |
| WLAN / AP | 무선 근거리 통신망과 액세스 포인트입니다. SSID는 네트워크 이름이며 그 자체로 인증이나 사용자 신원을 증명하지 않습니다. |
| EAP-TLS | 인증서 기반 TLS를 사용하는 확장 인증 프로토콜 방식입니다. 인증서 발급·검증·갱신·폐기까지 운영해야 합니다. |
| WIDS / WIPS | 각각 무선 침입 탐지와 무선 침입 방지 체계입니다. 자동 차단은 주변 장치와 업무 연결에 영향을 줄 수 있어 정책과 승인 범위가 필요합니다. |
| 랜섬웨어 / Ransomware | 데이터를 암호화하거나 접근을 방해하고 금전 요구를 하는 악성 행위입니다. 정보 탈취·공개 협박이 함께 있을 수 있습니다. |
| RPO / RTO | 각각 허용할 데이터 손실 시점과 복구에 허용되는 목표 시간입니다. 실제 복원 훈련으로 달성 가능성을 확인합니다. |
| 증거 해시 / Evidence hash | 파일 바이트열을 식별·비교하는 해시값입니다. 파일의 악성 여부, 작성자, 수집 경로를 단독으로 증명하지 않습니다. |
| 격리 / Quarantine | 의심 파일이나 영향을 받은 장치가 추가로 실행·통신·변경되지 않도록 승인된 절차로 제한하는 조치입니다. 사고 환경에 따라 격리 방법을 결정합니다. |
| SPF | SMTP `MAIL FROM` 도메인이 발신 IP의 사용을 허용하는지 확인하는 메일 발신 인증 방식입니다. 표시된 `From` 주소나 본문을 검증하지 않습니다. |
| DKIM | 메일 일부에 서명하고 DNS 공개키로 검증하는 방식입니다. 서명 도메인과 유효 서명이 곧 계정 소유자나 요청 내용의 정당성을 증명하지는 않습니다. |
| DMARC | 보이는 `From` 도메인과 정렬된 SPF 또는 DKIM 결과를 확인하고, 도메인 소유자의 정책 선호와 보고 방식을 전달하는 메일 인증 체계입니다. |
| 정렬 / Identifier alignment | DMARC에서 보이는 `From` 도메인과 SPF·DKIM 인증 식별자의 도메인 관계를 비교하는 조건입니다. 엄격·완화 모드가 있습니다. |
| BEC / Business email compromise | 메일 계정 사칭·탈취와 업무 대화 맥락을 이용해 송금·정보 공개·계정 변경 등을 유도하는 사기 유형입니다. |
| EPP / EDR / XDR | 각각 단말 예방·보호, 단말 이벤트 조사·대응, 여러 보안 영역의 통합 분석을 가리키는 제품 범주입니다. 실제 기능과 범위는 공급자별로 확인해야 합니다. |
| 단말 원격측정 / Endpoint telemetry | 단말 센서가 모은 프로세스·계정·파일·설정·연결 이벤트입니다. 센서·OS·정책에 따라 관측 범위가 달라집니다. |
| Sigma | 여러 SIEM으로 변환할 수 있는 방어용 로그 탐지 규칙의 YAML 표현 형식입니다. 로그 수집기·실행 엔진·완성된 탐지 결과와는 구분합니다. |
| 탐지 규칙 설계 / Detection engineering | 조사 가설·관측 데이터·규칙·필드 변환·검증·운영 피드백을 연결하는 방어 활동입니다. |
| 단일 이벤트 규칙 / Single-event rule | 한 로그 이벤트의 필드·값을 검사해 분석 후보를 만드는 규칙입니다. 반복·시간 관계는 별도 상관 논리가 필요합니다. |
| 상관 규칙 / Correlation rule | 여러 이벤트를 계정·호스트·주소·시간 등의 키로 묶어 개수·고유값·순서 관계를 확인하는 규칙입니다. backend가 기능을 지원하는지 확인해야 합니다. |
| 로그 수집 파이프라인 / Log ingestion pipeline | 이벤트가 원천에서 만들어진 뒤 Agent·Collector·저장소·파서·검색 시스템을 거쳐 분석 가능한 상태가 되기까지의 전달 경로입니다. |
| 수집 지연 / Ingestion lag | 원천 이벤트 시각과 수집·저장 단계에서 관측한 시각의 차이입니다. 시계가 동기화되고 두 시각의 기준이 같아야 의미 있게 비교할 수 있습니다. |
| 역압 / Backpressure | 다음 처리 단계가 포화됐을 때 이전 단계에 속도를 늦추거나 전송을 재시도하라고 알리는 동작입니다. 구현이 지원하지 않거나 대기열이 차면 데이터가 유실될 수 있습니다. |
| 로그 완전성 / Log completeness | 정해진 원천·기간·필터 기준에서 생성된 기록이 각 전달 단계에 얼마나 도달했는지 확인하는 상태입니다. 의도된 필터와 중복 제거를 반영해야 단순 건수 비교를 오해하지 않습니다. |
| 장기 자격 증명 / Long-lived credential | 사람이 직접 저장·교체해야 하는 기간이 긴 키·토큰·비밀번호입니다. 노출 후 폐기될 때까지 재사용될 수 있어 범위와 만료를 관리해야 합니다. |
| 동적 비밀정보 / Dynamic secret | 소비자나 작업이 필요할 때 발급되어 사용기간이 제한된 자격 증명입니다. 소비자가 종료되어도 발급자의 lease 만료나 폐기 처리가 따로 필요할 수 있습니다. |
| 워크로드 연합 신원 / Federated workload identity | workflow나 서비스가 외부 신원 제공자의 검증된 토큰으로 다른 서비스의 제한된 역할을 얻는 방식입니다. 토큰에 포함된 발급자·대상·주체 조건을 수신 측에서 검증합니다. |
| 비밀정보 검사 / Secret scanning | 저장소 기록·변경 등에 알려진 패턴 또는 설정한 패턴이 있는지 찾아 경보를 만드는 검사입니다. 제공자에서 실제 자격 증명을 폐기하는 기능과는 구분합니다. |
| 권한 있는 workflow / Privileged workflow | 쓰기 권한 token, secret, 배포 권한 또는 내부 자원 접근을 가진 GitHub Actions workflow입니다. 실행 코드와 입력의 신뢰 수준을 권한에 맞춰 제한해야 합니다. |
| 신뢰하지 않는 artifact / Untrusted artifact | 외부 PR 또는 낮은 권한 job이 만든 빌드 결과·시험 보고서입니다. workflow 실행 정보와 연결해도 파일 내용 자체가 안전하다는 증명은 아니므로 실행 가능한 코드로 취급하지 않습니다. |
| pwn request | 외부 PR의 변경 코드를 권한 있는 `pull_request_target` 또는 `workflow_run` 문맥에서 실행해 secret·token을 노출하는 GitHub Actions 취약 구성입니다. |
| DNS / Domain Name System | 사람이 읽는 도메인 이름을 IP 주소와 메일·서비스 관련 레코드에 연결하는 분산형 이름 시스템입니다. |
| stub resolver | 응용프로그램·운영체제에서 재귀 DNS resolver로 질의를 전달하는 클라이언트 구성요소입니다. |
| 재귀 resolver / Recursive resolver | 클라이언트 대신 DNS 계층을 따라 권한 있는 답을 찾고 캐시하는 서버입니다. DNSSEC 검증을 수행하는 resolver와 단순 전달 resolver를 구분해야 합니다. |
| 권한 있는 DNS 서버 / Authoritative name server | 자신이 관리하는 zone의 DNS 레코드를 공식 응답으로 제공하는 서버입니다. |
| DNSSEC | DNS 데이터의 출처와 무결성을 공개키 서명으로 확인하는 DNS 확장입니다. 질의 내용을 암호화하거나 DNS 가용성을 보장하지 않습니다. |
| DNSKEY | DNSSEC 서명을 검증하거나 zone 데이터를 서명하는 공개키 정보를 담는 DNS 레코드입니다. |
| DS / Delegation Signer | 부모 zone에 게시해 자식 zone의 DNSKEY를 연결하는 DNSSEC 레코드입니다. 부모 DS와 자식 키가 맞지 않으면 검증 resolver가 응답을 거부할 수 있습니다. |
| RRSIG | DNS 레코드 집합에 대한 DNSSEC 전자서명과 유효 기간을 담는 레코드입니다. |
| trust anchor | DNSSEC 검증이 신뢰 사슬을 시작할 때 미리 신뢰하도록 설정한 공개키·키 집합입니다. |
| DNSSEC validation state | 서명 사슬 검증 결과를 secure·insecure·bogus·indeterminate로 구분한 상태입니다. |
| DoT / DNS over TLS | DNS 질의·응답을 TLS 연결로 전달해 client와 resolver 사이 전송을 보호하는 방식입니다. |
| DoH / DNS over HTTPS | DNS 질의·응답을 HTTPS 요청·응답으로 전달하는 표준 방식입니다. resolver를 신뢰하는 문제는 별도로 남습니다. |
| CAA / Certification Authority Authorization | 도메인 소유자가 해당 이름의 공개 TLS 인증서를 발급할 수 있는 CA를 제한하도록 DNS에 게시하는 레코드입니다. client가 이미 발급된 인증서를 검증하는 용도는 아닙니다. |
| DNSSEC key rollover | DNSKEY와 부모 DS를 계획적으로 교체하는 작업입니다. 부모·자식 zone의 게시 상태와 캐시 TTL을 맞춰야 검증 실패를 피할 수 있습니다. |
| `dig +dnssec` | DNSSEC 레코드를 요청하는 DNS 질의 옵션입니다. 옵션을 추가한 것만으로 질의 도구가 신뢰 사슬을 검증했다고 볼 수 없습니다. |
| `delv` | BIND 9에 포함된 DNSSEC 검증 질의 도구입니다. 사용할 resolver·trust anchor·환경에 따른 한계를 함께 고려합니다. |
| DNS registrar lock | 도메인 이전이나 등록정보 변경을 제한하는 등록 사업자·registry의 정책 통제입니다. 계정 탈취나 DNS 공급자 침해를 모두 막지는 못합니다. |
| BGP / Border Gateway Protocol | 서로 다른 자율 시스템이 도달 가능한 IP prefix와 경로 정보를 교환하는 인터넷 경계 라우팅 protocol입니다. |
| AS / Autonomous System | 공통 라우팅 정책 아래 인터넷 경로를 관리하며 하나의 자율 시스템 번호(ASN)로 식별되는 네트워크 집합입니다. |
| prefix / IP prefix | IP 주소 범위와 네트워크 경계를 나타내는 표기입니다. 예를 들어 /24는 앞의 24비트가 네트워크 부분임을 나타냅니다. |
| AS_PATH | BGP 경로 속성으로, UPDATE가 거쳐 온 AS 정보를 나타냅니다. origin AS는 BGP 규격에 따라 AS_PATH에서 도출합니다. |
| RPKI / Resource Public Key Infrastructure | 인터넷 번호 자원의 할당 관계를 인증서와 서명된 객체로 표현해 라우팅 보안에 활용하는 공개키 기반 체계입니다. |
| ROA / Route Origin Authorization | 주소 자원 보유자가 특정 prefix를 어느 AS가 원점으로 광고할 수 있는지와 maxLength를 승인하는 RPKI 객체입니다. |
| VRP / Validated ROA Payload | RPKI 서명 자료를 검증한 뒤 경로 판정에 사용할 수 있도록 정규화한 prefix·origin ASN·maxLength 정보입니다. |
| ROV / Route Origin Validation | BGP 경로 prefix와 origin AS를 검증된 VRP 집합과 비교해 Valid·Invalid·NotFound 상태를 붙이는 기능입니다. |
| origin AS | 특정 BGP 경로를 원점으로 광고한다고 주장하는 AS 번호입니다. 경로의 모든 중간 AS를 검증한 결과와는 다릅니다. |
| maxLength | ROA가 허용하는 더 구체적인 광고 prefix 길이의 상한입니다. 필요 이상 넓게 허용하면 의도하지 않은 subprefix 경로도 유효해질 수 있습니다. |
| RPKI-RTR | 검증 cache가 라우터에 VRP 자료와 변경을 전달하는 protocol입니다. 라우터가 repository의 서명 객체를 직접 수집하는 흐름과 구분합니다. |
| RPKI cache | RPKI 저장소 자료를 수집·검증해 라우터에 전달하는 신뢰 구성요소입니다. 갱신 시각·session·trust anchor·전송 보호를 운영해야 합니다. |
| ROV 상태 / Origin validation state | BGP 경로를 VRP에 대조한 결과인 Valid, Invalid, NotFound입니다. 상태를 붙이는 것과 라우팅 정책에서 경로를 거부하는 것은 별도 동작입니다. |
| route leak | BGP 이웃 간 경로 전달 관계·정책을 위반해 의도하지 않은 경로가 전파되는 현상입니다. prefix 원점이 유효해도 발생할 수 있습니다. |
| BGP Role | RFC 9234가 eBGP 이웃 관계를 Provider·Customer·Peer·Route Server 등의 역할로 협상하는 capability입니다. |
| OTC / Only-to-Customer | BGP 경로가 customer·peer 방향으로 전달된 뒤 provider 등으로 재전파되지 않도록 돕는 경로 속성입니다. |
| SSH / Secure Shell | 신뢰할 수 없는 네트워크에서 원격 로그인과 포트 전달 등을 제공하는 프로토콜입니다. 전송 계층의 서버 인증과 사용자 인증은 별도 단계입니다. |
| SSH 호스트 키 / Host key | SSH 서버가 자신의 신원을 증명하는 공개키 쌍입니다. 클라이언트는 공개키 또는 CA 서명 호스트 인증서를 신뢰한 정보와 대조합니다. |
| `known_hosts` | SSH 클라이언트가 확인한 서버 호스트 키나 호스트 인증기관 정보를 저장하는 파일입니다. 항목이 있다는 사실만으로 최초 지문 확인 경로가 신뢰할 만했음을 증명하지는 않습니다. |
| 사용자 인증 키 / User authentication key | SSH 클라이언트의 사용자가 개인키 소유를 증명해 서버 계정에 로그인하는 데 사용하는 키입니다. 서버 호스트 키와 역할이 다릅니다. |
| `authorized_keys` | SSH 서버 계정에 허용할 사용자 공개키와 제한 옵션을 기록하는 파일입니다. 등록된 키의 계정 접근 권한과 서버 정책을 함께 관리해야 합니다. |
| `ssh-agent` | 개인키를 로컬 프로세스에 보관하고 클라이언트의 서명 요청을 처리하는 인증 에이전트입니다. 원격에 개인키 원문을 복사하지 않지만 전달된 소켓을 통해 인증 작업이 요청될 수 있습니다. |
| 에이전트 전달 / Agent forwarding | SSH 연결을 통해 클라이언트 인증 에이전트 소켓을 원격 호스트가 사용할 수 있게 하는 기능입니다. 원격 호스트의 침해 시 적재된 신원으로 인증 작업이 이뤄질 수 있어 기본적으로 제한합니다. |
| `ProxyJump` | SSH 클라이언트가 점프 호스트를 거쳐 최종 대상에 TCP 연결을 구성하는 설정입니다. 에이전트 전달과 다른 기능이며 최종 대상의 호스트 키 검증도 필요합니다. |
| OpenSSH 인증서 / OpenSSH certificate | CA가 공개키와 사용자·호스트 principal, 유효기간, 옵션을 서명한 OpenSSH 고유 형식입니다. X.509 인증서와 형식이 다릅니다. |
| principal | OpenSSH 인증서가 나타내는 허용 사용자 이름 또는 호스트 이름입니다. 서버는 신뢰한 CA와 principal 정책을 함께 확인합니다. |
| KRL / Key Revocation List | OpenSSH 키·인증서를 폐기 목록으로 표현하는 자료입니다. 서버에 배포되고 `RevokedKeys`로 적용되는 상태를 확인해야 합니다. |
| `StrictHostKeyChecking` | 저장된 서버 호스트 키의 변경을 검사하고 알 수 없는 키의 자동 수용을 제어하는 SSH 클라이언트 옵션입니다. |
| VPN / Virtual Private Network | 공용망 위에 논리적인 통신망을 만들고 종단점 사이 트래픽을 보호하는 기술입니다. 연결만으로 사용자·단말의 내부 서비스 권한이 생기지는 않습니다. |
| IPsec | IP 계층의 패킷을 보호하기 위한 표준 체계입니다. 정책·SA·ESP와 키 관리 방식의 실제 구성을 함께 확인해야 합니다. |
| IKEv2 / Internet Key Exchange Version 2 | IPsec peer를 인증하고 암호 설정·키·Security Association을 협상하고 관리하는 프로토콜입니다. |
| SA / Security Association | IPsec에서 보호 방향·프로토콜·키·암호 조건을 관리하는 보안 연결 상태입니다. 제어 교환인 IKE SA와 데이터 패킷을 보호하는 Child SA를 구분합니다. |
| SPD / Security Policy Database | IPsec 경계에서 패킷을 보호·통과·폐기할지 트래픽 조건에 따라 정하는 정책 데이터베이스입니다. |
| SAD / Security Association Database | 현재 성립한 IPsec SA의 키·알고리즘·상태 등 처리 정보를 관리하는 데이터베이스입니다. |
| 분할 터널 / Split tunnel | 지정된 내부 네트워크만 VPN으로 보내고 나머지 트래픽은 기존 인터넷 경로로 전달하는 구성입니다. |
| 전체 터널 / Full tunnel | 단말의 기본 인터넷 경로도 VPN으로 보내 조직의 출구 통제를 거치도록 구성한 방식입니다. IPv4·IPv6·DNS를 모두 점검해야 합니다. |
| WireGuard `AllowedIPs` | peer별 IP 범위를 지정하는 설정입니다. 송신 때는 대상 peer 선택에, 수신 때는 해당 peer가 보낼 수 있는 출발지 주소 확인에 사용됩니다. |
| cryptokey routing | WireGuard가 peer 공개키와 허용 IP를 연결해 송신 경로와 수신 출발지 검사를 함께 수행하는 방식입니다. |
| VPN MTU | 터널 캡슐화 후 경로에서 전달할 수 있는 최대 패킷 크기입니다. 지나치게 큰 값은 특정 응답 정체·단편화·재전송 문제를 일으킬 수 있습니다. |
| 네트워크 구역 / Network zone | 보안 요구와 역할이 비슷한 시스템을 묶고 경계 간 통신 정책을 적용하는 논리적 구분입니다. VLAN만으로 라우팅된 통신이 차단되는 것은 아닙니다. |
| DMZ / Demilitarized zone | 인터넷에 공개하는 서비스와 내부 업무·데이터 자원을 분리하기 위한 중간 네트워크 구역입니다. DMZ가 내부 자원에 접근할 수 있는 범위도 별도 통제해야 합니다. |
| 기본 거부 / Default deny | 명시적으로 허용한 흐름 외에는 트래픽을 거부하는 정책입니다. 적용 전에 실제 의존성, 관리 접속과 복구 경로를 확인해야 합니다. |
| 상태 기반 방화벽 / Stateful firewall | 연결 추적 정보를 이용해 패킷이 새 연결인지 기존 연결의 일부인지 판정하는 방화벽입니다. 상태 추적이 접근 허가 자체를 대신하지 않도록 방향·구역별 규칙을 제한합니다. |
| 무상태 ACL / Stateless access control list | 연결 상태를 기억하지 않고 주소·프로토콜·포트 등의 조건으로 각 패킷을 따로 허용하거나 거부하는 규칙 목록입니다. 반환 경로 정책도 별도로 고려할 수 있습니다. |
| 아웃바운드 제어 / Egress filtering | 내부 자산에서 외부 또는 다른 구역으로 나가는 통신을 제한하고 관찰하는 통제입니다. DNS·시간 동기화·업데이트 등 필수 의존성을 확인해야 합니다. |
| 마이크로세그먼테이션 / Microsegmentation | 작은 응용·자산·업무 구역 단위로 연결 정책을 적용하는 방식입니다. 자산과 의존성을 먼저 파악하고 단계적으로 배포해야 운영 중단 위험을 줄일 수 있습니다. |
| 규칙 가림 / Rule shadowing | 앞선 규칙이 더 넓은 조건으로 패킷을 먼저 처리해 뒤의 규칙이 도달 불가능하거나 효과를 내지 못하는 상황입니다. 규칙 순서와 장비별 평가 방식을 함께 봐야 합니다. |
| 연결 추적 / Connection tracking | 방화벽이 통신의 상태와 양방향 패킷 관계를 기록해 후속 패킷을 분류하는 기능입니다. 기록된 상태가 모든 추가 체인이나 다른 보안 경계의 허용을 보장하지는 않습니다. |
| Kubernetes NetworkPolicy | Pod에 적용할 ingress·egress 연결 규칙을 선언하는 Kubernetes API입니다. 실제 집행은 NetworkPolicy를 지원하는 네트워크 플러그인이 맡습니다. |
| CNI / Container Network Interface | 컨테이너 런타임과 네트워크 플러그인 사이의 연결 규격과 생태계입니다. CNI를 사용한다는 사실만으로 설치된 플러그인이 Kubernetes NetworkPolicy를 집행한다고 단정할 수 없습니다. |
| Pod 격리 / Pod isolation | NetworkPolicy가 특정 Pod를 ingress 또는 egress 방향에서 제한 대상으로 만드는 동작입니다. 두 방향은 독립적으로 격리되며 적용되지 않은 방향은 기본 허용일 수 있습니다. |
| `podSelector` | NetworkPolicy가 적용될 Pod 집합이나 통신 상대 Pod를 label로 고르는 Kubernetes 선택자입니다. |
| `namespaceSelector` | Pod가 속한 Namespace 집합을 label로 선택하는 NetworkPolicy 필드입니다. 같은 `from`·`to` 항목에 `podSelector`와 함께 쓰면 두 조건을 모두 만족하는 Pod를 가리킵니다. |
| 리버스 프록시 / Reverse proxy | 클라이언트의 요청을 받아 내부 원본 서버에 전달하고 응답을 반환하는 중간 서버입니다. TLS 종료·로드 분산·요청 전달을 맡을 수 있지만 사용자 인증을 자동으로 대신하지는 않습니다. |
| WAF / Web Application Firewall | HTTP 요청·응답을 검사해 응용 계층의 규칙에 따라 기록하거나 차단하는 통제입니다. 오탐·미탐과 애플리케이션의 권한 검사가 남습니다. |
| 전달 헤더 / Forwarding header | 프록시가 실제 연결의 방문자 주소·원래 host·scheme 등의 정보를 다음 서버에 전달하는 HTTP 헤더입니다. 클라이언트도 값을 보낼 수 있어 신뢰 프록시 경계에서 검증·정리해야 합니다. |
| 원본 서버 / Origin server | CDN·리버스 프록시 뒤에서 실제 응용프로그램과 콘텐츠를 제공하는 서버입니다. 공개 접근 경로가 열려 있으면 WAF를 우회해 직접 요청할 수 있습니다. |
| WAF 오탐 / WAF false positive | 실제로는 정상인 요청을 공격으로 잘못 판정하는 현상입니다. 서비스의 정상 동작을 확인한 뒤 제한된 경로·매개변수·규칙에 한정해 예외를 관리합니다. |
| 이상 점수 / Anomaly score | WAF 규칙의 여러 탐지 결과를 거래별 수치로 누적해 차단 임계값과 비교하는 점수입니다. 임계값을 높이면 정상 차단뿐 아니라 공격 통과도 늘 수 있습니다. |
| mTLS / Mutual TLS | TLS 연결에서 서버가 인증서를 제시하는 것뿐 아니라 클라이언트도 인증서를 제시해 서로의 신원을 확인하는 방식입니다. 신뢰 CA·인증서 범위·폐기와 키 보관이 필요합니다. |
| HTTP 메시지 framing / Message framing | HTTP 헤더와 프로토콜 규칙으로 요청·응답의 헤더와 본문이 어디서 끝나는지 정하는 방법입니다. HTTP/1.1의 길이 판정과 HTTP/2의 stream·frame 경계는 서로 다릅니다. |
| 요청 역동기화 / Request desynchronization | 프록시와 원본 서버가 같은 연결의 HTTP 바이트를 서로 다른 요청 경계로 해석해 처리 순서가 어긋나는 상태입니다. |
| HTTP 요청 밀수 / HTTP request smuggling | 여러 HTTP 수신자의 파서 차이를 이용해 중간 장비가 인식하지 못한 요청이 다른 수신자에게 전달되게 하는 취약점 계열입니다. MITRE CWE-444로 분류됩니다. |
| `Content-Length` | HTTP 메시지 본문의 바이트 길이를 나타내는 필드입니다. HTTP/1.1에서는 전송 코딩 등 RFC 9112의 우선순위 규칙과 함께 해석해야 합니다. |
| `Transfer-Encoding` | HTTP/1.1 메시지 본문에 적용된 전송 코딩을 나타내는 필드입니다. 요청 framing에 `chunked`가 쓰이면 마지막 코딩이어야 하며 길이 규칙을 RFC에 따라 처리합니다. |
| HTTP/2 다운그레이드 / HTTP/2 downgrade | 중개자가 HTTP/2 메시지를 HTTP/1.1 등 다른 표현으로 변환하는 과정입니다. 변환기가 필드와 본문을 검증하고 모호함 없이 다시 직렬화하는지 확인해야 합니다. |
| 요청 정규화 / Request normalization | 수신 요청을 표준 규칙으로 파싱·검증한 뒤 일관된 표현으로 다시 구성하는 처리입니다. 검증되지 않은 원문 헤더를 그대로 전달하는 것과 구분합니다. |
| 서버 측 요청 위조 / SSRF / Server-Side Request Forgery | 사용자가 유도한 요청을 서버가 의도하지 않은 목적지로 대신 보내도록 하는 취약점입니다. 서버의 네트워크 경로와 실행 신원에 따라 내부 서비스나 클라우드 metadata가 영향을 받을 수 있습니다. |
| DNS rebinding | 같은 도메인 이름의 DNS 응답을 시간에 따라 다른 주소로 바꾸는 동작입니다. URL 검사 때 확인한 주소와 HTTP client의 실제 연결 주소가 달라지지 않도록 검사와 연결을 묶어야 합니다. |
| 클라우드 인스턴스 메타데이터 / Instance metadata | VM의 실행 정보와 플랫폼별 identity 관련 자료를 제공하는 내부 서비스입니다. 접근 가능한 프로세스와 연결된 role·service account 권한을 함께 관리해야 합니다. |
| AWS IMDSv2 | Amazon EC2 Instance Metadata Service의 세션 token 방식입니다. 인스턴스에서 token을 요구하도록 설정할 수 있으며, hop limit과 컨테이너 호환성을 확인해야 합니다. |
| URL fetch worker | 사용자가 지정하거나 시스템에 등록된 URL에서 데이터를 가져오는 격리된 worker입니다. 웹 애플리케이션 전체의 내부망·metadata 접근 권한을 공유하지 않도록 설계합니다. |
| Same-Origin Policy / 동일 출처 정책 | 브라우저 script가 다른 origin의 데이터에 임의로 접근하지 못하게 하는 기본 정책입니다. 서버 API의 인증·인가를 수행하는 기능은 아닙니다. |
| CORS / Cross-Origin Resource Sharing | 서버 응답을 다른 origin의 browser script와 공유할 수 있는 조건을 응답 header로 선언하는 protocol입니다. 허용되지 않은 request 자체를 모든 client에서 차단하는 방화벽은 아닙니다. |
| CSP / Content Security Policy | 브라우저가 페이지에서 불러오거나 실행할 수 있는 리소스의 출처와 조건을 제한하는 response policy입니다. 안전한 입력·출력 처리와 함께 사용합니다. |
| HSTS / HTTP Strict Transport Security | HTTPS 응답으로 정책을 받은 browser가 이후 해당 host에 HTTPS 연결만 하도록 기억하는 정책입니다. 하위 도메인 적용과 preload는 전체 domain 구성을 확인한 뒤 선택합니다. |
| clickjacking | 투명하거나 겹친 frame 등으로 사용자가 의도와 다르게 다른 사이트의 조작 가능한 화면을 누르게 유도하는 UI 공격입니다. `frame-ancestors` 또는 호환 목적의 frame 정책을 검토합니다. |
| COOP / Cross-Origin-Opener-Policy | 최상위 문서와 cross-origin browsing context 사이의 opener 관계를 제한하는 response header policy입니다. popup·OAuth 흐름의 영향을 확인합니다. |
| COEP / Cross-Origin-Embedder-Policy | 문서가 no-CORS 방식으로 cross-origin 리소스를 embed할 수 있는 조건을 제한하는 response policy입니다. CORS·CORP 동의가 없는 리소스가 차단될 수 있습니다. |
| Permissions Policy | 문서와 iframe이 camera·geolocation 등 browser 기능을 사용할 수 있는 범위를 지정하는 policy입니다. OS·계정·서버 권한을 대체하지 않습니다. |

용어는 각 장의 적용 조건과 함께 읽습니다. 예를 들어 인증된 메시지도 재전송일 수 있고, 유사한 검색 결과에도 읽기 권한이 없을 수 있습니다. 정의를 판단 근거로 바꾸는 예제는 각 장에 연결했습니다.

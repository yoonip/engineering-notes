# 사이버보안과 시스템 방어 | Cybersecurity and system defense

보안의 기본 개념에서 웹·운영체제·네트워크·클라우드·firmware의 신뢰 경계를 살펴보고, 기업 계정·모바일 앱·무선망·랜섬웨어 대응까지 연결합니다. AI를 이용한 공격과 AI 시스템을 보호하는 방법도 다룹니다. 원리, 실패 조건, 방어 설계와 작은 실행 예제로 공부하는 자료입니다.

[전체 분야별 목차](../분야별목차_CATALOG.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md) · [실습](실습_labs/README.md) · [실행 결과](실습_labs/검증기록_validation.md)

## 기초에서 응용으로

처음에는 01~05장을 순서대로 읽으시면 됩니다. 이후 개발하는 시스템에 따라 Linux·메모리·클라우드·공급망·임베디드로 이어가고, AI의 공격 활용과 모델·검색·도구 보호를 공부합니다. 마지막에는 취약점 검증·로그·사고 대응과 심화 설계 가정을 연결합니다.

| 단계 | 글 | 핵심 내용 |
| --- | --- | --- |
| 기초 | [보안의 기본과 공격 흐름](01-보안의기본과공격흐름_security-foundations.md) | 자산·위협·취약점·위험, 예방·탐지·복구 |
| 기초 | [위협 모델과 설계 경계](02-위협모델과설계경계_threat-modeling.md) | 데이터 흐름·STRIDE·사업 규칙·검증 요구 |
| 기초 | [암호와 키의 신뢰](03-암호와키의신뢰_cryptography-keys.md) | 해시·HMAC·서명·AEAD·비밀번호·키 교체 |
| 기초 | [인증과 권한 검사](04-인증과권한검사_identity-access.md) | 인증·세션·피싱 저항성·객체별 권한 |
| 응용 | [웹과 API의 입출력](05-웹과API의입출력_web-api.md) | SQL·XSS·CSRF·SSRF·경로·업로드·API |
| 응용 | [Linux와 네트워크 경계](06-Linux와네트워크경계_linux-network.md) | TLS·DNS·프로세스·파일·망 분리 |
| 응용 | [메모리와 바이너리 분석](07-메모리와바이너리분석_memory-binaries.md) | 포인터·경계 검사·sanitizer·fuzzing·역공학 |
| 응용 | [클라우드와 컨테이너](08-클라우드와컨테이너_cloud-containers.md) | IAM·컨테이너·Kubernetes·비밀·격리 |
| 응용 | [소프트웨어 공급망과 배포](09-소프트웨어공급망과배포_software-supply-chain.md) | 의존성·SBOM·빌드 출처·CI·배포 키 |
| 응용 | [임베디드와 산업 시스템](10-임베디드와산업시스템_embedded-ot.md) | 부팅·업데이트·디버그·물리 경계·OT |
| AI | [AI가 바꾸는 공격과 방어](11-AI가바꾸는공격과방어_ai-enabled-threats.md) | 공격 비용·규모의 변화와 방어 AI 평가 |
| AI | [프롬프트와 검색 자료](12-프롬프트와검색자료_llm-rag-security.md) | 직접·간접 주입·검색 ACL·출력 처리 |
| AI | [AI 에이전트와 도구 권한](13-AI에이전트와도구권한_agent-tool-security.md) | 도구 허용·인수·주체·승인·실행 통제 |
| AI | [모델과 데이터의 보호](14-모델과데이터의보호_ml-lifecycle.md) | poisoning·backdoor·추출·개인정보·모델 공급망 |
| 검증·운영 | [취약점 평가와 수정 검증](15-취약점평가와수정검증_vulnerability-validation.md) | 정적·동적 검사·재현·수정·판정 |
| 검증·운영 | [로그 탐지와 사고 대응](16-로그탐지와사고대응_detection-response.md) | 합성 로그·시간창·경보·조사·복구 |
| 심화 | [고급 보안의 설계 가정](17-고급보안의설계가정_advanced-security.md) | 형식 검증·부채널·TEE·증명·양자내성 |
| 학습 경로 | [실무 점검과 학습 경로](18-실무점검과학습경로_practice-paths.md) | 업무별 읽기 순서·공식 강좌·기록 방법 |
| 허가된 평가 | [허가된 보안 시험과 책임 있는 제보](19-허가된보안시험과책임있는제보_authorized-security-testing.md) | 범위 승인·안전한 증거·취약점 보고서 작성입니다. |
| 기업 보안 | [기업 계정과 관리자 권한](20-기업계정과관리자권한_enterprise-identity.md) | 디렉터리·하이브리드 ID·권한 계층·관리자 단말·감사입니다. |
| 앱·기기 보안 | [모바일 기기와 앱 보안](21-모바일기기와앱보안_mobile-security.md) | MASVS·기기 데이터·딥링크·백엔드 권한·수명 주기입니다. |
| 네트워크 보안 | [무선랜과 기업 Wi-Fi 보안](22-무선랜과기업와이파이보안_wireless-lan-security.md) | 인증·망 분리·AP 관리·무선 탐지·운영 점검입니다. |
| 사고 대응 | [랜섬웨어와 악성코드 대응](23-랜섬웨어와악성코드대응_ransomware-malware-response.md) | 초기 대응·증거 보존·복구 검증·안전한 파일 식별입니다. |
| 메일 보안 | [메일 인증과 업무 메일 침해](24-메일인증과업무메일침해_email-authentication-bec.md) | SPF·DKIM·DMARC, 계정 탈취, 결제 변경 확인과 BEC 대응입니다. |
| 단말 보안 | [단말 탐지와 대응](25-단말탐지와대응_endpoint-detection-response.md) | EDR 구성·이벤트 조사·격리 영향·복구 확인과 탐지 품질입니다. |
| 탐지 설계 | [탐지 규칙 설계와 검증](26-탐지규칙설계와검증_detection-engineering.md) | Sigma 규칙·로그 필드 매핑·시간 상관·오탐과 운영 전 검증입니다. |
| 로그 운영 | [보안 로그 수집 파이프라인과 손실 감시](27-보안로그수집과손실감시_log-pipeline-integrity.md) | 원천 이벤트·수집 누락·파서 오류·대기열·중앙 보관 상태를 확인합니다. |
| 자격 증명 | [비밀정보 수명주기와 CI 자격 증명](28-비밀정보수명주기와CI자격증명_secrets-lifecycle.md) | 저장소 비밀 유출 대응·키 교체·GitHub Actions OIDC·최소 권한을 다룹니다. |
| CI 보안 | [외부 PR과 권한 있는 GitHub Actions workflow](29-외부PR과권한있는워크플로우_github-actions-trust-boundaries.md) | `pull_request_target`·`workflow_run`의 권한 경계, artifact·cache 취급과 PR 시험 분리를 설명합니다. |
| 인증 연동 | [OAuth 2.0과 OpenID Connect 로그인 보안](30-OAuth와OpenIDConnect인증_oauth-oidc-security.md) | authorization code·PKCE·token 검증과 browser·mobile client 구조를 연결합니다. |
| 패스키 인증 | [패스키와 WebAuthn 인증](31-패스키와WebAuthn인증_passkeys-webauthn.md) | credential 등록·challenge 검증·동기화와 계정 복구를 설명합니다. |
| TLS 인증서 | [TLS 인증서와 PKI 운영](32-TLS인증서와PKI운영_tls-certificates-pki-operations.md) | 인증 경로·서비스 이름 확인·ACME 갱신·폐기와 진단 명령을 연결합니다. |
| DNS·도메인 보안 | [DNSSEC와 암호화 DNS, 도메인 운영](33-DNS보안과도메인운영_dnssec-encrypted-dns-domain-security.md) | DNSSEC·DoT·DoH·CAA의 보호 범위와 도메인 계정·키 교체 운영을 설명합니다. |
| BGP·경로 보안 | [BGP 경로 보안과 RPKI 원점 검증](34-BGP경로보안과RPKI원점검증_bgp-rpki-origin-validation.md) | ROA·VRP·Valid/Invalid/NotFound 판정과 route leak 방어를 구분합니다. |
| 원격 접속 보안 | [SSH 접속 신원과 키 운영](35-SSH접속신원과키운영_ssh-identity-key-operations.md) | 호스트 키·사용자 키·에이전트 전달·ProxyJump·OpenSSH 인증서와 폐기 절차를 설명합니다. |

## 글과 근거의 성격

각 주제는 취약점이 성립하는 조건, 영향을 받는 신뢰 경계, 예방·탐지·복구 통제, 수정 후 확인할 결과를 연결합니다. 표준·분류표는 설계 질문을 만드는 출발점으로 사용하며 특정 서비스의 안전성을 대신 증명하지 않습니다. 취약점 시험은 소유자의 승인과 정해진 범위에서 수행해야 합니다.

## 코드와 근거의 성격

실습 코드는 이 자료를 위해 직접 작성했습니다. Python·C의 공식 API 문서를 연결하고 각 줄의 문법과 목적을 적었습니다. 기업 내부 구현을 가져왔거나 실제 운영 보안 제품을 완성한 코드라는 의미는 아닙니다.

실습은 메모리 SQLite, 합성 문서·로그·바이트열을 사용합니다. 외부 대상을 스캔하거나 계정을 공격하지 않으며 LLM·GPT API도 호출하지 않습니다. SQL 오류 대조군과 수정본, HMAC과 재전송, 객체 권한, HTML 본문 출력, 파일 해시, AI 도구 게이트, 로그 시간창, C 프레임 경계를 실제 검사합니다. 실행한 환경·명령·결과·한계는 검증 기록에서 확인합니다.

본문은 공식 표준·보안 프로젝트 문서를 토대로 작성했으며 자료 확인일은 2026-11-04입니다. 특정 판본을 사용한 글은 해당 판본을 적었습니다. 위협 전망은 전망으로, 자체 계산·예제는 자체 자료로 구분합니다. 분야 전체의 모든 전문 기법을 다루었다는 의미는 아니며 각 장에서 적용 범위와 다음 학습을 연결합니다.

## 기존 글과 연결

- [보안·암호·하드웨어 신뢰 개론](../전자컴퓨터공학_ece/38-보안암호하드웨어신뢰_security-cryptography/README.md): 암호와 부팅·메모리 신뢰의 기존 설명입니다.
- [설계와 검증 사례](../설계와검증사례_engineering-cases/README.md): 통신·저장·업데이트·동시성·복구의 실행 기록입니다.
- [하드웨어 코딩](../하드웨어코딩_hardware-coding/README.md), [반도체 설계](../반도체설계_semiconductor-design/README.md): 회로·RTL·SoC 구현과 연결합니다.
- [AI 모델과 수치 실험](../AI모델과수치실험_ai-models/README.md): 모델의 공식 구조와 자체 계산을 구분하는 기존 자료입니다.

## English

This section connects security foundations with application, network, memory, cloud, supply-chain, embedded and AI security, authorized testing, enterprise identities, mobile apps, wireless LANs, ransomware response, email authentication, endpoint detection, detection engineering, log-pipeline health, secret lifecycle management, workload identity, privileged GitHub Actions workflows, OAuth/OpenID Connect, passkeys with WebAuthn, TLS certificate operations, DNS integrity, encrypted DNS transport, domain-registration security, BGP route-origin validation, and SSH identity operations. It distinguishes client-side mobile controls from backend verification, sender-domain authentication from business-request legitimacy, origin validation from AS-path validation, endpoint alert signals from incident evidence, and SSH server host keys from user authentication keys. Educational exercises use synthetic data; operational actions remain subject to authorization and incident procedures.

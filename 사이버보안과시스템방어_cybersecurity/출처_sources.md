# 출처와 판본 | Sources and editions

[목차](README.md) · [기계 판독용 목록](sources.json)

공식 기관·표준·프로젝트 문서를 우선 사용했습니다. 아래 범위는 확인하거나 학습 경로로 연결한 절입니다. 표준의 전체 요구사항을 제품에 구현·인증했다는 뜻은 아닙니다. 웹 문서는 바뀔 수 있어 확인일과 판본을 함께 남깁니다. 확인일은 2026-11-04입니다.

| 자료 | 판본·시점 | 사용·연결 범위 |
| --- | --- | --- |
| [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) | 2026-11-04 확인 | Govern·Identify·Protect·Detect·Respond·Recover의 구성 소개 |
| [OWASP Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | 2026-11-04 확인 | 시스템 모델·위협 식별·완화·검토의 절 |
| [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) | 2026-11-04 확인 | 암호 선택·키 관리·인증 암호 절 |
| [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | 2026-11-04 확인 | 비밀번호 해싱·salt·Argon2id 절 |
| [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) | 2025-07 최종판 | 인증 보증·피싱 저항성·비밀번호·복구 관련 절 |
| [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | 2026-11-04 확인 | 최소권한·기본 거부·매 요청 검사 절 |
| [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | 2026-11-04 확인 | 매개변수 쿼리·허용 목록 절 |
| [OWASP Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | 2026-11-04 확인 | 출력 문맥·인코딩·safe sinks 절 |
| [OWASP Top 10:2025](https://top10.owasp.org/2025/) | 2025판 | 정식 목록·각 위험 범주의 명칭 |
| [IETF RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html) | 2018-08 | TLS 1.3 개요·0-RTT 재전송 관련 §2·§8 |
| [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | 2020-08 | 공식 초록·자원 중심 접근과 내부망 신뢰의 구분 |
| [SEI CERT C ARR30-C](https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts) | 2026-11-04 확인 | 배열·포인터 범위의 규칙과 예제 |
| [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) | 2026-11-04 확인 | 검출 오류·빌드 방법·제약 절 |
| [LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html) | 2026-11-04 확인 | coverage-guided fuzzing 소개·사용법·입력 목표 함수 |
| [Kubernetes Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/) | 2026-11-04 확인 | 인증·권한·네트워크·Pod 보안·이미지 절 |
| [GitHub Actions Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | 2026-11-04 확인 | 최소 토큰 권한·외부 입력·SHA 고정·신뢰하지 않는 코드 checkout |
| [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | 2022-02 SSDF 1.1 | 공식 초록·SDLC에 보안 개발 활동을 넣는 목적 |
| [NIST SP 800-193](https://csrc.nist.gov/pubs/sp/800/193/final) | 2018-05 | 공식 초록의 보호·탐지·복구 목적 |
| [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | 2023-09 | 공식 초록·OT의 성능·신뢰성·안전 제약 |
| [NCSC Impact of AI on cyber threat from now to 2027](https://www.ncsc.gov.uk/report/impact-ai-cyber-threat-now-2027) | 2025년 공개 전망, 2027년까지의 시나리오 | Key judgements·Assessment·Implications; 전망의 확률 표현 |
| [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | 2026-11-04 확인 | 직접·간접 주입·도구 권한·다층 방어 절 |
| [OWASP GenAI LLM Top 10 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/README.md) | 2026-08 공개판 | 공식 위험 항목의 명칭·순서 |
| [OWASP Agentic Top 10 for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 2025-12-09 공개, 2026판 | 에이전트 위험 항목과 공식 설명 |
| [OWASP Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/) | 2026-09-01 공개 | middleware hook·런타임 정책 집행 설명 |
| [FIRST CVSS v4.0 User Guide](https://www.first.org/cvss/v4.0/user-guide) | CVSS v4.0, 문서 버전 1.2 | Base·Threat·Environmental·Supplemental 지표와 점수 해석 |
| [FIRST EPSS FAQ](https://www.first.org/epss/faq) | 2026-11-04 확인 | 30일 악용 확률·일일 점수·환경 위험과의 차이 |
| [MITRE ATT&CK T1110 Brute Force](https://attack.mitre.org/techniques/T1110/index.html) | 2026-11-04 확인 | Password Guessing·Password Cracking·Password Spraying·Credential Stuffing의 분류 |
| [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | 2008-09-30 최종판 | 기술 보안 시험의 계획·수행·결과 분석·완화; 현행 모든 기술을 포괄하는 안내서는 아님 |
| [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | 2026-11-04 확인 | 도구 호출·최소권한·신뢰 경계·승인 절 |
| [NIST AI 100-2 E2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) | 2025-03, 공식 페이지의 정정 안내 포함 | 공식 초록의 생명주기·공격자 지식·목표에 따른 AML 분류 |
| [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final) | 2024-07 | 공식 초록의 AI 모델 생산자·시스템 생산자·구매자 범위 |
| [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/) | 2026-11-04 확인 | 전술·기술 행렬과 기법별 탐지 연결 |
| [MITRE ATLAS 공개 데이터](https://github.com/mitre-atlas/atlas-data) | 2026-11-04 확인 | 공식 저장소의 AI 위협·사례 데이터 안내 |
| [OWASP ASVS 5.0.0](https://asvs.owasp.org/) | 2025-05-30 공개된 안정판 | 요구사항 버전 표기·웹 애플리케이션 보안 검증의 목적 |
| [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | 2025-04 | 공식 초록·CSF 2.0과 연결한 탐지·대응·복구 |
| [OWASP Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | 2026-11-04 확인 | 기록할 사건·민감정보 제외·로그 위변조 대응 |
| [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) | 2024-08-13 | 공식 초록·ML-KEM의 공유 비밀 설정 목적·정정 안내 |
| [KISA 보호나라·KrCERT/CC](https://www.krcert.or.kr/) | 2026-11-04 확인 | 보안공지·취약점·보고서·침해사고 대응의 공식 진입 경로 |
| [Python sqlite3](https://docs.python.org/3.12/library/sqlite3.html) | Python 3.12 문서 | 매개변수 바인딩·메모리 DB API |
| [Python hmac](https://docs.python.org/3.12/library/hmac.html) | Python 3.12 문서 | digest·compare_digest API |
| [Python html](https://docs.python.org/3.12/library/html.html) | Python 3.12 문서 | escape의 동작과 quote 인수 |
| [IETF RFC 4231](https://www.rfc-editor.org/rfc/rfc4231.html) | 2005-12 | §4.2 HMAC-SHA-256 시험 벡터 1 |
| [NSA Ghidra](https://github.com/NationalSecurityAgency/ghidra) | 2026-11-04 확인 | 공식 README·빌드·역공학 도구 소개 |
| [Wireshark User’s Guide](https://www.wireshark.org/docs/wsug_html_chunked/) | 2026-11-04 확인 | 캡처·표시 필터·TLS 분석의 진입 경로 |
| [CodeQL documentation](https://codeql.github.com/docs/) | 2026-11-04 확인 | 공식 도구 문서의 진입 경로·정적 질의 목적 |
| [OWASP ZAP documentation](https://www.zaproxy.org/docs/) | 2026-11-04 확인 | 공식 웹 검사 도구의 문서 진입 경로 |
| [OWASP WSTG 4.2](https://owasp.org/www-project-web-security-testing-guide/v42/) | 안정판 4.2 | 웹 시험의 범위·접근법·테스트 절차 안내 |
| [PortSwigger Web Security Academy](https://portswigger.net/web-security) | 2026-11-04 확인 | 공식 무료 웹 보안 학습·제공자 실습 안내 |
| [Carnegie Mellon picoCTF](https://picoctf.org/) | 2026-11-04 확인 | 교육용 보안 문제·연습 환경·운영 주체 소개 |
| [Microsoft AD DS Tier Model](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/tier-model) | 2026-11-04 확인 | Tier 0·1·2, 관리자 작업 단말, 자격 증명 계층 분리, 단계적 도입 |
| [Microsoft Active Directory 보안 권고](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory) | 2026-11-04 확인 | 최소 권한·보안 관리자 단말·도메인 컨트롤러 보호·감사 정책 |
| [NIST SP 800-124 Rev. 2](https://csrc.nist.gov/pubs/sp/800/124/r2/final) | 2023-05 최종판 | 조직 소유·개인 소유 모바일 기기의 도입·사용·폐기, MDM/EMM·단말 보호 |
| [OWASP MASVS](https://mas.owasp.org/MASVS/) | 2026-11-04 확인 | STORAGE·CRYPTO·AUTH·NETWORK·PLATFORM·CODE·RESILIENCE·PRIVACY 통제 영역 |
| [OWASP MASTG](https://mas.owasp.org/MASTG/) | 2026-11-04 확인 | MASVS 통제를 Android·iOS 앱에서 확인하는 시험 가이드 |
| [OWASP MASVS 평가와 인증 안내](https://mas.owasp.org/MASVS/04-Assessment_and_Certification/) | 2026-11-04 확인 | 클라이언트 범위·백엔드 별도 검증·자동 도구의 한계·보고 항목 |
| [NIST SP 800-153](https://csrc.nist.gov/pubs/sp/800/153/final) | 2012-02 최종판 | WLAN 구성요소의 설계·배포·유지·모니터링 수명 주기; 현재 암호 설정 기준으로 사용하지 않음 |
| [CISA Guide to Securing Networks for Wi-Fi](https://www.cisa.gov/sites/default/files/publications/A_Guide_to_Securing_Networks_for_Wi-Fi.pdf) | 2017-03-15, DHS Cybersecurity Engineering 1.0 | 무선 위협·유선/무선 관측 결합의 배경; 미 연방기관 맞춤형 자료이며 최신 암호 설정 근거로 사용하지 않음 |
| [NIST IR 8374 Rev. 1](https://csrc.nist.gov/pubs/ir/8374/r1/final) | 2026-06 최종판 | CSF 2.0에 연결한 랜섬웨어 위험 관리·준비·대응·복구 결과 |
| [MITRE ATT&CK T1486 Data Encrypted for Impact](https://attack.mitre.org/techniques/T1486/) | 2026-11-04 확인 | 데이터 암호화를 이용한 가용성 영향의 행위 분류; 단독 귀속·판정 증거로 사용하지 않음 |
| [Microsoft PowerShell Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-7.5) | PowerShell 7.5 문서, 2026-11-04 확인 | 파일 내용의 SHA-256 계산과 결과 해석 범위 |
| [Microsoft Active Directory Forest Recovery Guide](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-guide) | Windows Server 2025·2022·2019·2016 적용 문서, 2026-11-04 확인 | 포리스트 전체 장애 복구 계획의 단계와 판본 적용 범위 |
| [Microsoft Active Directory 초기 포리스트 복구 절차](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-perform-initial-recovery) | 2026-11-04 확인 | 격리 복구, 루트 도메인 순서, SYSVOL·자격 증명·검증 주의사항 |
| [Android Keystore system](https://developer.android.com/privacy-and-security/keystore) | 2026-11-04 확인 | 키 추출 방지·사용 권한·하드웨어 지원에 따른 차이와 한계 |
| [Apple Keychain Services](https://developer.apple.com/documentation/security/keychain-services/) | 2026-11-04 확인 | 암호화된 키체인 저장소와 접근 제어 기능의 개요 |
| [Android Security checklist](https://developer.android.com/privacy-and-security/security-tips) | 2026-11-04 확인 | 앱 인증·데이터 저장·네트워크·권한·구성요소 보안 권고 |
| [Android exported component 위험](https://developer.android.com/privacy-and-security/risks/android-exported) | 2026-11-04 확인 | 다른 앱에서 실행 가능한 Android 컴포넌트의 접근 범위 |
| [IETF RFC 9190 EAP-TLS 1.3](https://www.rfc-editor.org/rfc/rfc9190.html) | 2022-02 | EAP-TLS 1.3 상호 인증·Identity 응답의 한계·인증서 폐기 확인 |
| [CISA StopRansomware Guide](https://www.cisa.gov/sites/default/files/2023-10/StopRansomware-Guide-508C-v3_1.pdf) | 2023-10 공개판 | 오프라인 백업·복원 훈련·대응 준비 권고 |
| [MITRE ATT&CK DET0215](https://attack.mitre.org/detectionstrategies/DET0215/) | 2026-05-12 수정판, 2026-11-04 확인 | 다중 플랫폼 파일 암호화 탐지 신호·자료원·분석 변수 |
| [IETF RFC 7208 SPF](https://www.rfc-editor.org/rfc/rfc7208.html) | 2014-04, Standards Track | SPF 발신 식별자·평가 결과·DNS 조회 제한 |
| [IETF RFC 6376 DKIM](https://www.rfc-editor.org/rfc/rfc6376.html) | 2011-09, Standards Track; 서명 구조 설명 범위 | DKIM 서명·selector·서명 도메인의 기본 구조 |
| [IETF RFC 9989 DMARC](https://www.rfc-editor.org/rfc/rfc9989.html) | 2026-05, Standards Track; RFC 7489 대체 | 식별자 정렬·정책·보고·배포 절차와 pct 태그 제거 |
| [IETF RFC 8601 Authentication-Results](https://www.rfc-editor.org/rfc/rfc8601.html) | 2019-05, Standards Track | 인증 결과 필드의 용도·신뢰 경계·위조 헤더 위험 |
| [FBI Business Email Compromise](https://www.fbi.gov/how-we-can-help-you/common-frauds-and-scams/business-email-compromise) | 2026-11-04 확인 | BEC 유형과 지급 요청·계좌 변경의 독립 확인 권고 |
| [Microsoft Defender for Endpoint: 단말 대응 조치](https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts) | 2026-11-04 확인 | 단말 격리·조사 자료 수집·지원 조건·업무 영향 |
| [Microsoft Defender for Endpoint: 장치 조사](https://learn.microsoft.com/en-us/defender-endpoint/investigate-machines) | 2026-11-04 확인 | 장치 시간선·프로세스 트리·경보·대응 기능의 제품별 흐름 |
| [Microsoft Defender for Endpoint: 경보 조사](https://learn.microsoft.com/en-us/defender-endpoint/investigate-alerts) | 2026-11-04 확인 | 경보 스토리·시간선·사건 분류와 조사 절차 |
| [Sigma Rule Specification v2.1.0](https://github.com/SigmaHQ/sigma-specification/blob/v2.1.0/specification/sigma-rules-specification.md) | v2.1.0 release | 단일 이벤트 규칙의 logsource·detection·필드·상태·오탐 조건 |
| [Sigma Correlation Rules Specification v2.1.0](https://github.com/SigmaHQ/sigma-specification/blob/v2.1.0/specification/sigma-correlation-rules-specification.md) | v2.1.0 release | 이벤트·고유값 집계, 그룹 키, 시간창과 backend 지원 범위 |
| [SigmaHQ pySigma](https://github.com/SigmaHQ/pySigma) | 2026-11-04 확인 | 규칙 파싱·변환과 backend·pipeline plugin의 분리 구조 |
| [SigmaHQ sigma-cli](https://github.com/SigmaHQ/sigma-cli) | 2026-11-04 확인 | 설치·plugin·변환 명령과 공식 사용 예시 |
| [Microsoft Windows Event 4625](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625) | 2026-11-04 확인 | 실패 이벤트의 생성 위치·필드·로그온 유형·모니터링 권고 |
| [Best practices for event logging and threat detection](https://www.cyber.gov.au/publication/best-practices-for-event-logging-and-threat-detection) | 2024-08-22 게시판 | 로그 원천 우선순위·시각 동기화·중앙 수집·보존·전송 보호·무결성 |
| [Priority logs for SIEM ingestion: Practitioner guidance](https://www.cyber.gov.au/publication/priority-logs-for-siem-ingestion-practitioner-guidance) | 2025-05-27 게시판 | SIEM 수집 로그의 위험 기반 우선순위·단계적 도입·유입량·건강 점검 |
| [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | Stable specification, 2026-11-04 확인 | 원천 사건 시각과 수집 관측 시각을 분리하는 로그 필드 정의 |
| [OpenTelemetry Collector internal telemetry](https://opentelemetry.io/docs/collector/internal-telemetry/) | 2026-11-04 확인 | Collector receiver·exporter·전송 큐의 상태 계측과 판본별 확인 항목 |
| [OpenTelemetry Collector resiliency](https://opentelemetry.io/docs/collector/resiliency/) | 2026-11-04 확인 | 큐·재시도·지속 저장·메시지 큐와 유실 가능 조건 |
| [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | 2026-11-04 확인 | 비밀정보 수명주기·CI/CD 접근·회전·동적 자격 증명·감사·노출 대응 |
| [GitHub Actions OIDC cloud providers](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers) | 2026-11-04 확인 | 클라우드 연합 신뢰 설정·id-token 권한·보호 환경·단기 token 교환 |
| [GitHub Actions OpenID Connect reference](https://docs.github.com/en/actions/reference/security/oidc) | 2026-11-04 확인 | iss·aud·sub claim·branch/environment 조건·2026-07-15 immutable subject 변경 |
| [GitHub Secret Scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) | 2026-11-04 확인 | 저장소 기록 검사·경보·validity check·custom pattern |
| [GitHub Push Protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) | 2026-11-04 확인 | 지원 패턴 push 차단·기능 활성화 조건·우회 감사 경보 |
| [Remediating a leaked secret in your repository](https://docs.github.com/en/code-security/tutorials/remediate-leaked-secrets/remediating-a-leaked-secret) | 2026-11-04 확인 | 노출 평가·폐기·재발급·서비스 갱신·Git 기록 정리 |
| [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | 2026-11-04 확인 | credential 폐기 우선·history rewrite·clone·fork·cache 영향 |
| [GitHub Actions Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | 2026-11-04 확인 | workflow 최소 권한·secret masking의 한계·구조화된 비밀값·생성된 민감 값 등록 |
| [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) | 2026-11-04 확인 | 기본 브랜치 문맥·PR 코드 실행 위험·cache 읽기 정책·runner 분리 |
| [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) | 2026-11-04 확인 | `pull_request`·`pull_request_target`·`workflow_run` 실행 문맥과 fork 동작 |
| [Managing GitHub Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) | 2026-11-04 확인 | fork PR workflow의 token·secret·승인 정책 |
| [Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) | 2026-11-04 확인 | 낮은 신뢰도의 workflow와 cache 쓰기 권한·poisoning 위험 |
| [Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/) | 2021년 게시, 2026-11-04 확인 | PR build·test·설치 hook에서 권한 있는 workflow로 이어지는 공격 경로 |
| [Python `json` library](https://docs.python.org/3/library/json.html) | Python 3 표준 라이브러리 문서, 2026-11-04 확인 | JSON 파싱과 `object_pairs_hook` 인터페이스 |
| [Python `pathlib`](https://docs.python.org/3/library/pathlib.html) | Python 3 표준 라이브러리 문서, 2026-11-04 확인 | 경로 객체와 바이너리 파일 읽기 |
| [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html) | 2025-01; 2026-11-04 확인 | redirect·PKCE·CSRF·implicit/password grant·token 권한·refresh token 보안 |
| [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749.html) | 2012-10; 2026-11-04 확인 | OAuth client·authorization code·token endpoint·기본 framework |
| [RFC 7636: Proof Key for Code Exchange by OAuth Public Clients](https://www.rfc-editor.org/rfc/rfc7636.html) | 2015-09; 2026-11-04 확인 | `code_verifier`·`code_challenge`·S256 검증 |
| [OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html) | Errata set 2; 2026-11-04 확인 | ID Token claim과 issuer·audience·nonce 검증 |
| [RFC 10017: OAuth 2.0 for Browser-Based Applications](https://www.rfc-editor.org/rfc/rfc10017.html) | 2026-08; IETF Best Current Practice; 2026-11-04 확인 | browser-only client·token-mediating backend·BFF의 보안 tradeoff |
| [RFC 8252: OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252.html) | 2017-10; 2026-11-04 확인 | 외부 user-agent·native app redirect·public client PKCE |
| [RFC 7009: OAuth 2.0 Token Revocation](https://www.rfc-editor.org/rfc/rfc7009.html) | 2013-08; 2026-11-04 확인 | access·refresh token 폐기 endpoint와 발급자별 연관 token 처리 |
| [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207.html) | 2022-03; 2026-11-04 확인 | authorization response의 `iss`와 등록 issuer 비교·mix-up 방어 |
| [OWASP OAuth 2.0 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html) | 2026-11-04 확인 | state·PKCE·issuer 확인 등 OAuth client 구현 점검 |
| [W3C Web Authentication: An API for accessing Public Key Credentials, Level 3](https://www.w3.org/TR/webauthn-3/) | 2026-08-25 W3C Recommendation; 2026-11-04 확인 | credential 등록·assertion 검증·challenge·origin·RP ID·UP/UV·counter·backup flag |
| [NIST SP 800-63B-4: Syncable Authenticators](https://pages.nist.gov/800-63-4/sp800-63b/syncable/) | 2025-07 최종판; 2026-11-04 확인 | BE/BS·동기화형 credential 공유·복구·attestation 고려사항 |
| [NIST SP 800-63B-4: Authenticator and Verifier Requirements](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/) | 2025-07 최종판; 2026-11-04 확인 | 피싱 저항성의 정의·수동 입력 OTP의 한계 |
| [FIDO Alliance, Synced Passkey Deployment: Emerging Practices for Consumer Use Cases](https://fidoalliance.org/wp-content/uploads/2024/05/Synced-Passkey-Deployment_-Emerging-Practices-for-Consumer-Use-Cases_2024-Final.pdf) | 2024-05; 2026-11-04 확인 | 동기화형·기기 고정형 credential의 사용자·서비스 운영 tradeoff와 계정 복구 |
| [FIDO Alliance UX Guidelines for Passkey Creation and Sign-ins](https://fidoalliance.org/wp-content/uploads/2023/05/FIDO-Alliance-UX-Guidelines-for-Passkey-Creation-and-Sign-ins.pdf) | 2023-05; 2026-11-04 확인 | discoverable FIDO credential이라는 passkey 용어와 소비자 로그인 흐름 |
| [RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280.html) | 2008-05; 2026-11-04 확인 | X.509 인증서·확장·인증서 경로 검증·CRL profile |
| [RFC 9525: Service Identity in TLS](https://www.rfc-editor.org/rfc/rfc9525.html) | 2023-11; 2026-11-04 확인 | DNS/IP reference identity, SAN 검증, CN-ID 사용 중단과 wildcard 제한 |
| [RFC 8555: Automatic Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555.html) | 2019-03; 2026-11-04 확인 | ACME account·order·HTTP-01·DNS-01·certificate revocation |
| [RFC 8737: ACME TLS-ALPN-01 Challenge](https://www.rfc-editor.org/rfc/rfc8737.html) | 2020-02; 2026-11-04 확인 | TLS ALPN protocol을 통한 domain validation challenge |
| [RFC 6960: Online Certificate Status Protocol](https://www.rfc-editor.org/rfc/rfc6960.html) | 2013-06; 2026-11-04 확인 | 인증서 상태 확인 protocol인 OCSP |
| [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/rfc/rfc9162.html) | 2021-12; Experimental; 2026-11-04 확인 | 공개 TLS 인증서 transparency log의 감사·오발급 탐지 범위 |
| [CA/Browser Forum Baseline Requirements](https://cabforum.org/working-groups/server/baseline-requirements/requirements/) | Version 2.3.1, 2026-10-04; 2026-11-04 확인 | 공개적으로 신뢰되는 TLS 서버 인증서의 발급·수명주기 기준 |
| [OpenSSL `s_client`](https://docs.openssl.org/master/man1/openssl-s_client/) | OpenSSL master command documentation; 2026-11-04 확인 | SNI·hostname·chain 검증 옵션과 `-showcerts` 출력 범위 |
| [OpenSSL `x509`](https://docs.openssl.org/master/man1/openssl-x509/) | OpenSSL master command documentation; 2026-11-04 확인 | subject·issuer·기간·SAN 출력 옵션 |
| [OpenSSL `verify`](https://docs.openssl.org/master/man1/openssl-verify/) | OpenSSL master command documentation; 2026-11-04 확인 | CA·intermediate·purpose·hostname을 통한 인증서 검증 명령 |
| [RFC 1034: Domain Names — Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034.html) | 1987-11; 2026-11-04 확인 | DNS 이름 공간과 해석 구조 §2·§4 |
| [RFC 1035: Domain Names — Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035.html) | 1987-11; 2026-11-04 확인 | DNS 메시지와 기본 레코드 §3·§4 |
| [RFC 4033: DNS Security Introduction and Requirements](https://www.rfc-editor.org/rfc/rfc4033.html) | 2005-03; RFC 6840 등으로 갱신; 2026-11-04 확인 | DNSSEC의 인증·무결성, 기밀성·가용성 범위 §3·§4 |
| [RFC 4034: Resource Records for the DNS Security Extensions](https://www.rfc-editor.org/rfc/rfc4034.html) | 2005-03; 2026-11-04 확인 | DNSKEY·RRSIG·DS·NSEC 레코드 정의 §2·§3 |
| [RFC 4035: Protocol Modifications for the DNS Security Extensions](https://www.rfc-editor.org/rfc/rfc4035.html) | 2005-03; RFC 6840 등으로 갱신; 2026-11-04 확인 | 검증 resolver 동작·secure/insecure/bogus/indeterminate 상태 §4·§5 |
| [RFC 9364: DNS Security Extensions (DNSSEC)](https://www.rfc-editor.org/rfc/rfc9364.html) | 2023-02; BCP 237; 2026-11-04 확인 | DNSSEC 핵심 RFC의 개요와 현재 모범 관행 §1·§2 |
| [RFC 7858: Specification for DNS over TLS](https://www.rfc-editor.org/rfc/rfc7858.html) | 2016-05; RFC 8310으로 사용 프로파일 보완; 2026-11-04 확인 | client-resolver 구간의 TLS 전송 기밀성·세션 §1·§3 |
| [RFC 8310: Usage Profiles for DNS over TLS and DNS over DTLS](https://www.rfc-editor.org/rfc/rfc8310.html) | 2018-03; RFC 7858 갱신; 2026-11-04 확인 | DoT·DoDTLS 사용 프로파일과 resolver 인증 §5·§6 |
| [RFC 8484: DNS Queries over HTTPS](https://www.rfc-editor.org/rfc/rfc8484.html) | 2018-10; 2026-11-04 확인 | HTTPS 기반 DNS 교환, 개인정보·운영 고려사항 §3·§8·§10 |
| [RFC 8659: DNS Certification Authority Authorization](https://www.rfc-editor.org/rfc/rfc8659.html) | 2019-11; RFC 6844 대체; 2026-11-04 확인 | CAA 발급 제한과 CA 처리, 인증서 검증과의 구분 §1·§3·§4 |
| [BIND 9 DNSSEC Guide](https://bind9.readthedocs.io/en/stable/dnssec-guide.html) | BIND 9.20 안정 문서; 2026-11-04 확인 | DNSSEC validation·parent DS·key rollover·SERVFAIL 진단·delv |
| [Australian Cyber Security Centre, Domain Name System security for domain owners](https://www.cyber.gov.au/publication/domain-name-system-security-for-domain-owners) | 2021-10 공개 자료; 2026-11-04 확인 | registrar MFA·접근 로그·변경 알림·domain lock의 보호 범위 |
| [ICANN SSAC SAC-044, A Registrant’s Guide to Protecting Domain Name Registration Accounts](https://www.icann.org/en/groups/ssac/documents/sac-044-en.pdf) | 2025 공개; 2026-11-04 확인 | 등록자 계정 보호 권고와 등록 운영 절차 |
| [RFC 6480: An Infrastructure to Support Secure Internet Routing](https://www.rfc-editor.org/rfc/rfc6480.html) | 2012-02; Informational; 2026-11-04 확인 | RPKI 구조·ROA·저장소·cache 운영 §2·§3·§6 |
| [RFC 6482: A Profile for Route Origin Authorizations (ROAs)](https://www.rfc-editor.org/rfc/rfc6482.html) | 2012-02; 2026-11-04 확인 | ROA prefix·origin AS·maxLength 구조 §3·§4 |
| [RFC 6811: BGP Prefix Origin Validation](https://www.rfc-editor.org/rfc/rfc6811.html) | 2013-01; RFC 8481·8893으로 갱신; 2026-11-04 확인 | VRP 대조와 Valid·Invalid·NotFound 판정·정책 §2·§3·§5 |
| [RFC 8481: Clarifications to BGP Origin Validation Based on RPKI](https://www.rfc-editor.org/rfc/rfc8481.html) | 2018-09; RFC 6811 갱신; 2026-11-04 확인 | 검증 상태 설정과 정책 적용의 구분 §4·§5 |
| [RFC 8210: The RPKI to Router Protocol, Version 1](https://www.rfc-editor.org/rfc/rfc8210.html) | 2017-09; RFC 6810 대체; 2026-11-04 확인 | RPKI cache와 라우터 사이 자료 전달·세션·전송 보호 §3·§4·§8·§9 |
| [RFC 9319: The Use of maxLength in the RPKI](https://www.rfc-editor.org/rfc/rfc9319.html) | 2022-10; 2026-11-04 확인 | maxLength가 허용하는 더 구체적인 경로와 ROA 구성 지침 §2·§3 |
| [RFC 7454: BGP Operations and Security](https://www.rfc-editor.org/rfc/rfc7454.html) | 2015-02; BCP 194; 2026-11-04 확인 | BGP 세션·제어면·prefix filter·최대 prefix·AS_PATH 운영 보안 §4·§5·§6·§8·§9 |
| [RFC 8212: Default External BGP Route Propagation Behavior without Policies](https://www.rfc-editor.org/rfc/rfc8212.html) | 2017-07; RFC 4271 갱신; 2026-11-04 확인 | eBGP import·export 정책이 명시되지 않았을 때 기본 거부 §1·§3 |
| [RFC 7908: Problem Definition and Classification of BGP Route Leaks](https://www.rfc-editor.org/rfc/rfc7908.html) | 2016-06; Informational; 2026-11-04 확인 | route leak의 작업 정의와 분류 §2·§3 |
| [RFC 9234: Route Leak Prevention and Detection Using Roles in UPDATE and OPEN Messages](https://www.rfc-editor.org/rfc/rfc9234.html) | 2022-05; 2026-11-04 확인 | BGP Role과 OTC 기반 경로 누출 예방·탐지 §3·§4·§5 |
| [RFC 8893: RPKI Origin Validation for BGP Export](https://www.rfc-editor.org/rfc/rfc8893.html) | 2020-09; RFC 6811 갱신; 2026-11-04 확인 | export policy의 effective origin AS 검증 §3·§4 |
| [RFC 5398: Autonomous System Number Reservation for Documentation Use](https://www.rfc-editor.org/rfc/rfc5398.html) | 2008-12; Informational; 2026-11-04 확인 | 문서 예시용 AS 번호 범위 §2·§4 |
| [RFC 5737: IPv4 Address Blocks Reserved for Documentation](https://www.rfc-editor.org/rfc/rfc5737.html) | 2010-01; Informational; 2026-11-04 확인 | 문서 예시용 IPv4 주소 prefix §3·§4 |
| [Python `ipaddress` library](https://docs.python.org/3/library/ipaddress.html) | Python 3 표준 라이브러리 문서; 2026-11-04 확인 | IPv4·IPv6 network 해석과 subnet_of API |

## 코드 출처

`실습_labs`의 코드는 공식 코드를 복사한 것이 아니라 직접 작성한 교육 예제입니다. 표준 라이브러리 API와 설계 원칙의 출처를 각 장에 연결했습니다. HMAC 검사의 공개 정답은 RFC 4231 §4.2에서 가져왔습니다. 자체 SQL 입력·문서·로그·프레임과 계산값은 외부 기관의 측정 데이터가 아닙니다.

## 접근과 판본의 범위

NIST CSRC 링크 중 일부는 표준 본문의 전체 재독이 아니라 공식 발행 페이지·초록의 범위를 사용했습니다. NCSC 자료는 2027년까지의 위협 전망이며 특정 제품의 실측 성능으로 인용하지 않았습니다. 동적으로 바뀌는 강좌·도구 페이지는 학습 경로이며 모든 실습을 실행했다는 의미는 아닙니다. CISA KEV 페이지는 이번 환경에서 직접 열람이 거부되어 해당 본문을 확인한 출처 목록에 넣지 않았습니다.

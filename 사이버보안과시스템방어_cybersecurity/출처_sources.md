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

## 코드 출처

`실습_labs`의 코드는 공식 코드를 복사한 것이 아니라 직접 작성한 교육 예제입니다. 표준 라이브러리 API와 설계 원칙의 출처를 각 장에 연결했습니다. HMAC 검사의 공개 정답은 RFC 4231 §4.2에서 가져왔습니다. 자체 SQL 입력·문서·로그·프레임과 계산값은 외부 기관의 측정 데이터가 아닙니다.

## 접근과 판본의 범위

NIST CSRC 링크 중 일부는 표준 본문의 전체 재독이 아니라 공식 발행 페이지·초록의 범위를 사용했습니다. NCSC 자료는 2027년까지의 위협 전망이며 특정 제품의 실측 성능으로 인용하지 않았습니다. 동적으로 바뀌는 강좌·도구 페이지는 학습 경로이며 모든 실습을 실행했다는 의미는 아닙니다. CISA KEV 페이지는 이번 환경에서 직접 열람이 거부되어 해당 본문을 확인한 출처 목록에 넣지 않았습니다.

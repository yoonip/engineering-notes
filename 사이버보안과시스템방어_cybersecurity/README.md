# 사이버보안과 시스템 방어 | Cybersecurity and system defense

보안의 기본 개념에서 웹·운영체제·네트워크·클라우드·firmware의 신뢰 경계를 살펴보고, AI를 이용한 공격과 AI 시스템을 보호하는 방법을 연결합니다. 원리, 실패 조건, 방어 설계와 작은 실행 예제로 공부하는 자료입니다.

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

This section connects security foundations with application, network, memory, cloud, supply-chain, embedded and AI security. Korean chapters include source editions, explicit assumptions and line-commented educational code. Offline exercises cover SQL binding, authorization, message authentication and replay state, output encoding, artifact digests, constrained agent tools, login detection and C frame bounds. The validation record identifies what was actually executed; conceptual guides and forecasts are not presented as penetration tests or production implementations.

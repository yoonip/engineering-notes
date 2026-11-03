# 실무 점검과 학습 경로 | Practice and study paths

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 선수 지식에서 실제 판단으로 이어갑니다

처음에는 HTTP 요청·응답, Linux 파일·프로세스 권한, SQL 조건식, C의 배열·포인터, Python 사전·집합·예외를 익힙니다. 보안 용어만 외우기보다 자신이 보낸 입력이 어느 프로그램과 권한을 거치는지 설명하는 연습을 합니다. 이어 인증과 권한, 암호와 키, 입력·출력 문맥을 공부한 뒤 AI·클라우드·firmware의 연결을 살펴봅니다.

| 방향 | 읽을 장 | 직접 남길 결과 |
| --- | --- | --- |
| 처음 시작 | 01~05장입니다. | 자산·신뢰 경계 그림과 SQL·권한 검사 결과입니다. |
| 서비스·클라우드 개발 | 04~06·08~09장입니다. | 역할 정책·출구 통신·배포 출처·권한 회귀 검사입니다. |
| C·펌웨어·하드웨어 | 03·06~07·10·17장입니다. | 길이 경계·키·부팅·업데이트 실패의 검사 조건입니다. |
| AI 시스템 개발 | 02·04~05·09·11~14장입니다. | 검색 ACL·모델 판본·도구 제안/실행 분리·거부 시험입니다. |
| 취약점 연구·대응 | 02·07·15~17장입니다. | 재현 입력·원인·영향·수정 전후·조사 근거입니다. |

## 분야별 공식 학습 경로

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)는 웹 검사의 구조를, [ASVS](https://asvs.owasp.org/)는 검증 요구사항을 읽는 경로입니다.
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)는 제공자가 만든 실습 환경에서 웹 취약점과 방어를 공부하는 자료입니다.
- [picoCTF](https://picoctf.org/)는 Carnegie Mellon University의 교육용 보안 문제와 연습 환경입니다.
- [MITRE ATT&CK](https://attack.mitre.org/)와 [ATLAS](https://github.com/mitre-atlas/atlas-data)는 관측 행위·AI 위협 사례를 분류해 읽는 경로입니다.
- [KISA 보호나라](https://www.krcert.or.kr/)에서는 국내 보안공지와 보고서·가이드를 원문으로 확인합니다.

이 링크는 사용 목적을 안내하는 목록이며 모든 강좌·도구·문제를 이 저장소에서 실행한 기록은 아닙니다. 비용·접근 조건과 지원 판본은 해당 원문의 현재 안내에서 확인합니다.

## 업무 문서에 남길 최소 내용

개발자는 기능·자산·입력·권한과 실패 조건을, 시험자는 환경·소스·입력·기대값·실제값을, 운영자는 적용 대상·소유자·변경 창·복구·탐지 상태를 기록합니다. 보안팀과 제품팀은 ‘심각합니다’라는 말보다 어떤 요청에서 무엇이 노출되는지와 수정의 완료 조건을 공유합니다.

AI로 찾은 취약점 후보나 수정안도 같은 기준을 적용합니다. 근거 링크만 있는 주장, 실행하지 않은 성공 출력, 소스와 다른 코드 화면을 실험 결과로 올리지 않습니다. 이 카테고리의 예제는 직접 작성한 교육 코드이고 공식 제품의 내부 코드나 검증된 현업 구현이라는 의미가 아닙니다.

## 단원 마무리 문제

1. 정상 사용자의 다른 조직 문서 접근을 막으려면 어느 단계에서 무엇을 대조해야 할까요?
2. HMAC이 맞는 옛 메시지와 새 메시지를 어떻게 구분할까요?
3. 서명된 취약한 옛 firmware를 막으면서 복구도 가능하게 하려면 무엇을 저장해야 할까요?
4. AI 모델이 ‘관리자 승인 완료’라고 출력해도 지급을 실행하면 안 되는 이유는 무엇일까요?
5. 경보 탐지율이 높아도 정밀도가 낮아질 수 있는 이유를 11장의 수치로 설명해 보세요.

답을 확인할 때는 각각 객체 권한, 상태·최신성, 버전 하한·복구 상태, 서버 승인 근거, 기저율과 오탐을 연결합니다. 도구 명령을 외운 뒤 다른 환경에 그대로 적용하는 것보다 전제와 관측 결과를 설명하는 것이 목표입니다.

## 허가된 실습은 기준과 산출물을 남깁니다

웹 검사는 [WSTG 4.2](https://owasp.org/www-project-web-security-testing-guide/v42/)를 시험 항목의 출발점으로, [ASVS 5.0.0](https://asvs.owasp.org/)을 제품 요구사항의 출발점으로 사용할 수 있습니다. WSTG는 검사 방법의 구조를 제공하고 ASVS는 구현·검증할 요구사항을 제공합니다. 자동화 도구의 결과만으로 사업 로직이나 전체 보안성을 판정하지 않습니다.

학습은 다음처럼 진행하면 결과를 비교하기 쉽습니다.

1. 공식 실습 환경이나 본인 소유의 격리된 프로젝트에서 범위를 정합니다.
2. 사전 조건·버전·입력·정상 기대 결과·실패 결과를 기록합니다.
3. [PortSwigger Web Security Academy](https://portswigger.net/web-security)나 [picoCTF](https://picoctf.org/)의 제공된 문제를 풉니다.
4. 결함의 원인을 코드·정책·자료 흐름에서 설명하고 최소 수정안을 적습니다.
5. 기존 입력 재현과 정상 동작 회귀를 모두 확인하고 결과를 기록합니다.

이 저장소의 코드 실습은 합성 데이터와 로컬 환경에서 직접 작성한 교육 예제입니다. 강좌·도구의 모든 내용을 실행한 실적, 회사 시스템 침투 경험, 취약점 보상 프로그램 참여 내역으로 표시하지 않습니다. 실제 외부 시스템 검사는 별도 서면 승인과 규칙이 있을 때만 수행합니다. 보고서 형식과 승인 범위는 [19장](19-허가된보안시험과책임있는제보_authorized-security-testing.md)에 연결합니다.

## 원문에서 이어 읽기

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 검증 요구사항·판본·프로젝트 목적입니다.
- [KISA 보호나라·KrCERT/CC](https://www.krcert.or.kr/): 보안공지·취약점·보고서·침해사고 대응의 공식 진입 경로입니다.
- [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/): 전술·기술 행렬과 기법별 탐지 연결입니다.
- [MITRE ATLAS 공개 데이터](https://github.com/mitre-atlas/atlas-data): 공식 저장소의 AI 위협·사례 데이터 안내입니다.
- [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final): 공식 초록·SDLC에 보안 개발 활동을 넣는 목적입니다.

## English

Study paths connect foundations to web, cloud, firmware, AI and incident response. Official learning resources and actual execution records are kept distinct.

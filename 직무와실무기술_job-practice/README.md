# 직무와 실무 기술 | Roles and engineering practice

삼성전자 DX·DS와 SK하이닉스의 2026년 직무기술서를 바탕으로, 담당 업무에서 어떤 개념·검사·프로그램이 연결되는지 공부합니다. 직무 이름과 언어를 외우기보다 제품·현상·측정량·판정·결과물을 따라 읽습니다.

[저장소 첫 화면](../README.md) · [JD의 업무와 기술을 읽는 방법](00-JD의업무와기술을읽는법_role-work-evidence.md) · [출처와 검토 범위](출처와검토범위_SOURCES.md)

## 회사별 원문에서 업무를 찾습니다

| 직무기술서 | 본문에서 찾을 내용 |
| --- | --- |
| [삼성전자 DX](01-삼성DX의직무와요구역량_samsung-dx-role-map.md) | 제품 회로·로봇·SW·AI·품질, 영업·마케팅·구매·환경안전·인프라와 사업부별 포지션 |
| [삼성전자 DS](02-삼성DS의직무와요구역량_samsung-ds-role-map.md) | 회로·신호·평가, 공정 설계·공정 기술·설비, 패키징·생산관리·인프라·AI/IT·재무 |
| [SK하이닉스](03-SK하이닉스의직무와요구역량_sk-hynix-role-map.md) | 설계·소자·제품·솔루션·테스트, 양산·제조·AI/IT·품질·인프라와 지원 역할 |

각 표에는 해당 PDF의 위치와 원문이 언어를 적은 위치를 함께 표시했습니다. 자격요건·우대·수행 업무를 구분하고, 일반적인 실무 활용 예를 회사의 추가 필수 요건으로 바꾸지 않습니다.

## 실제로 무엇을 만들고 검사하는지 읽습니다

| 본문 | 연결하는 업무와 개념 |
| --- | --- |
| [제품 회로·시스템 검사](04-제품회로와시스템검사_product-circuit-system-tests.md) | 전원·SI/PI·RF·통신·EMC/ESD·제품 동작과 계측 |
| [펌웨어·소프트웨어 검증](05-펌웨어와소프트웨어검증_firmware-software-validation.md) | 드라이버·HAL·버퍼·실시간·RPC·운영 플랫폼·AI 서비스의 시험 |
| [칩 설계·평가 분석](06-칩설계와평가분석_chip-design-characterization.md) | RTL·기준 모델·STA·DFT·ATE·PVT·shmoo·고장 분석 |
| [공정·설비·패키지 검사](07-공정설비와패키지의검사_process-equipment-package-tests.md) | 공정 분류·설비 제어·계측·통계·조립·인프라의 검사 |
| [메모리 제품·테스트 개발](08-메모리제품과테스트개발_memory-product-test-engineering.md) | 웨이퍼·패키지·모듈·보드, 제품 동작·성능·불량 분석과 테스트 프로그램 |
| [AI·데이터·제조 IT](09-AI데이터와제조IT_ai-data-manufacturing-it.md) | 제조 데이터·모델 평가·데이터 파이프라인·서비스·장비/물류 시스템 |

## 언어·판정·기반 지식을 연결합니다

| 본문 | 공부할 내용 |
| --- | --- |
| [C·C++·Python이 쓰이는 위치](10-C와Python이쓰이는위치_languages-in-the-workflow.md) | 제품 내부 코드, RTL 모델, 테스터·계측 호스트, SQL·분석과 서비스의 역할 |
| [검사 결과의 판정과 기록](11-검사결과의판정과기록_test-decisions-evidence.md) | PASS/FAIL·유효하지 않은 측정, 불확도·재검사·분모·표본 수와 원시 결과 |
| [기반 지식과 학습 경로](12-기반지식과학습경로_foundations-learning-path.md) | 수학·회로·SW·반도체·AI·운영 지식을 실제 설명·측정·분석 결과로 연결하는 순서 |
| [반도체 산업과 직무의 연결](13-반도체산업과직무의연결_semiconductor-value-chain.md) | 메모리·시스템 반도체, IDM·팹리스·파운드리·OSAT와 설계–제조–제품의 인계 |

## 업무 사례와 출처가 있는 코드를 읽습니다

[직무별 연결표](사례_cases/06-직무별사례와담당범위_role-case-map.md)에서 각 모집 직무의 업무 상황·장비·관측 항목·결과물을 선택합니다. [사례 목차](사례_cases/README.md)는 회로 계측, 펌웨어·통신, 칩·메모리, 공정·설비·패키지, AI·제조 IT로 이어집니다.

제조사·공개 프로젝트의 C·Python 코드는 고정 원문과 대조하고 줄별 설명을 붙였습니다. [코드 출처와 이용 조건](사례_cases/코드출처와이용조건_CODE_SOURCES.md)에 판본·라이선스·발췌와 수정 범위를 정리했습니다. 업무 상황·가정 계산·공식 예제의 로컬 실행·장비 측정 여부는 각 본문에서 구분합니다.

## 기존 자료와 이어서 공부합니다

- [반도체 제조 공정](../반도체제조공정_semiconductor-fabrication/README.md): 공정별 단면과 FinFET·GAA·DRAM·NAND·HBM의 구조를 읽습니다.
- [현장 계측과 검증](../현장계측과검증_measurement-validation/README.md): 계측기·장비 제어·펌웨어 디버깅과 칩·시스템 시험을 읽습니다.
- [설계와 검증 사례](../설계와검증사례_engineering-cases/README.md): 기존 코드와 오류 재현·원인·수정·날짜별 실행 기록을 확인합니다.
- [공학 분야별 해설](../분야_topics/README.md): 언어·컴퓨터 구조·회로·통신·제어·AI의 기반을 공부합니다.
- [학습 사이트와 채널](../학습사이트와채널_learning-resources/README.md): 대학 강의와 공식 기술 자료를 과목별로 찾습니다.

## English

These guides connect the supplied 2026 Samsung DX, Samsung DS and SK hynix job descriptions to technical foundations, tests, programming tasks and engineering evidence. Company requirements remain distinct from preferences and educational examples. The reading paths link to existing fabrication, measurement and recorded debugging material.

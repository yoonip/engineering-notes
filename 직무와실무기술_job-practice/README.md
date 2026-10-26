# 직무와 실무 기술 | Roles and engineering practice

전자·컴퓨터공학의 지식이 제품 개발, 반도체 설계·제조, 메모리 평가·양산, 설비·품질·AI·IT 업무에 어떻게 쓰이는지 공부합니다. 제품·현상·측정량·프로그램의 실행 위치·판정·결과물을 따라 읽습니다.

[저장소 첫 화면](../README.md) · [직무와 기술을 읽는 방법](00-직무와기술을읽는법_roles-and-technical-work.md) · [출처와 검토 범위](출처와검토범위_SOURCES.md)

## 제품과 업무에서 시작합니다

| 업무 영역 | 본문에서 찾을 내용 |
| --- | --- |
| [전자제품·시스템 개발](01-전자제품과시스템개발의직무_product-system-roles.md) | 회로·통신·로봇·임베디드 SW·AI·품질과 생산·구매·서비스의 연결 |
| [반도체 설계·제조](02-반도체설계와제조의직무_semiconductor-design-manufacturing-roles.md) | 회로·소자·RTL·검증, 공정·설비·패키징·테스트와 제조 운영 |
| [메모리 제품·양산](03-메모리제품과양산의직무_memory-product-production-roles.md) | 메모리 구조·제품 평가·솔루션 HW/SW·양산 테스트·불량 분석·품질·제조 IT |

각 글은 직접 다루는 대상, 필요한 입력, 남길 결과물과 다른 업무로 넘기는 인터페이스를 설명합니다. 조직마다 직무 이름과 분업 방식은 다를 수 있으므로 기술이 쓰이는 위치를 중심으로 읽습니다.

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

[직무별 연결표](사례_cases/06-직무별사례와담당범위_role-case-map.md)에서 업무 상황·장비·관측 항목·결과물을 선택합니다. [사례 목차](사례_cases/README.md)는 회로 계측, 펌웨어·통신, 칩·메모리, 공정·설비·패키지, AI·제조 IT로 이어집니다.

제조사·공개 프로젝트의 C·Python 코드는 고정 원문과 대조하고 줄별 설명을 붙였습니다. [코드 출처와 이용 조건](사례_cases/코드출처와이용조건_CODE_SOURCES.md)에 판본·라이선스·발췌와 수정 범위를 정리했습니다. 업무 상황·가정 계산·공식 예제의 로컬 실행·장비 측정 여부는 각 본문에서 구분합니다.

## 기존 자료와 이어서 공부합니다

- [산업별 전자와 컴퓨팅](../산업별전자와컴퓨팅_industry-systems/README.md): 자동차·가전·방산항공우주·해양조선·발전·산업설비·기업 IT·의료·철도에서 제품과 하위 시스템, 인터페이스와 검사 결과물을 연결합니다.
- [반도체 제조 공정](../반도체제조공정_semiconductor-fabrication/README.md): 공정별 단면과 FinFET·GAA·DRAM·NAND·HBM의 구조를 읽습니다.
- [현장 계측과 검증](../현장계측과검증_measurement-validation/README.md): 계측기·장비 제어·펌웨어 디버깅과 칩·시스템 시험을 읽습니다.
- [설계와 검증 사례](../설계와검증사례_engineering-cases/README.md): 기존 코드와 오류 재현·원인·수정·날짜별 실행 기록을 확인합니다.
- [전자·컴퓨터공학](../전자컴퓨터공학_ece/README.md): 언어·컴퓨터 구조·회로·통신·제어·AI의 기반을 공부합니다.
- [학습 사이트와 채널](../학습사이트와채널_learning-resources/README.md): 대학 강의와 공식 기술 자료를 과목별로 찾습니다.

## English

These guides connect electronics and computing to product development, semiconductor design and manufacturing, memory engineering, tests, quality, operations and AI/IT. Each role is explained through its inputs, work products, interfaces and evidence. The reading paths link technical foundations to source-attributed code and recorded debugging material.

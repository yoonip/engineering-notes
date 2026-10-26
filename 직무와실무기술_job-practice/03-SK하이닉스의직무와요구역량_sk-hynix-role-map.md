# SK하이닉스의 직무와 요구 역량 | SK hynix role and skill map

[직무·실무 목차](README.md) · [메모리 제품·테스트 개발](08-메모리제품과테스트개발_memory-product-test-engineering.md) · [AI·데이터·제조 IT](09-AI데이터와제조IT_ai-data-manufacturing-it.md) · [출처와 판본](출처와검토범위_SOURCES.md)

이 글은 『2026 하반기 SK하이닉스 Talent hy-way(신입) Job Description』의 직무 본문을 기준으로 합니다. 쪽수는 표지를 1쪽으로 센 PDF 순서입니다. 2–24쪽의 직무를 모두 아래 표에 연결했고, 1쪽은 표지, 25쪽은 지원·전형 안내로 구분했습니다. 문서 확인일은 2026-10-26입니다.

JD는 업무의 범위와 기대 경험을 설명하는 문서입니다. 아래에서 ‘언어 명시’는 해당 페이지에 이름이 실제로 나온 경우이며, ‘프로그래밍 경험’과 ‘데이터 분석’만 나온 페이지를 임의로 C·Python 필수 직무로 바꾸지 않았습니다. 상세한 검사 방법과 학습 예시는 뒤의 해설에서 별도로 설명합니다.

## 1. 직무별로 만드는 결과물

| PDF 쪽 | 직무·표시된 지역 | 원문 업무를 이해하기 위한 요약 | 언어·소프트웨어의 원문 명시 | 연결할 학습 내용 |
| --- | --- | --- | --- | --- |
| 2 | 설계 · 이천/분당 | 회로·배치·회로 검증과 CAD 방법론으로 메모리 설계를 구현합니다. | C code 기반 System·RTL 검증을 명시합니다. | [설계·평가](06-칩설계와평가분석_chip-design-characterization.md), 아래 설계 검증 구분 |
| 3 | 소자 · 이천/청주/용인 | 공정 통합, 소자 특성, FA·CA, 모델링·신뢰성·설계 규칙·OPC를 연결합니다. | Programming(C, Python 등), TCAD Simulation을 명시합니다. | [공정·설비 검사](07-공정설비와패키지의검사_process-equipment-package-tests.md), [소자·공정 기초](../반도체제조공정_semiconductor-fabrication/00-소자와공정의기초_devices-process-basics.md) |
| 4 | R&D 공정 · 이천/분당 | 포토·식각·확산·박막·세정/CMP·웨이퍼 본딩·계측·장비와 Foundry 공정을 개발합니다. | 특정 언어 이름은 제시하지 않습니다. | [공정 순서·단면](../반도체제조공정_semiconductor-fabrication/10-로직과메모리의공정차이_logic-memory-integration.md), [공정 검사](07-공정설비와패키지의검사_process-equipment-package-tests.md) |
| 5 | Product Engineering · 이천/분당/청주 | 제품 특성·품질·양산성을 평가하고 테스트와 불량 분석을 연결합니다. | Programming을 활용한 문제 해결 경험을 적습니다. | [메모리 제품·테스트](08-메모리제품과테스트개발_memory-product-test-engineering.md) |
| 6 | Solution SW · 분당 | SSD·시스템 구조, 펌웨어·알고리즘·검증 인프라, AI 메모리용 시스템 소프트웨어를 개발합니다. | C/C++, Assembly, Verilog·SystemVerilog, ARM 임베디드 경험, Cursor·Claude Code 등 AI IDE를 명시합니다. | [펌웨어·SW 검증](05-펌웨어와소프트웨어검증_firmware-software-validation.md), [SSD 검사](08-메모리제품과테스트개발_memory-product-test-engineering.md) |
| 7 | Solution HW · 분당 | SSD 보드·전원, SI/PI/EMC, 실장 공정, 열·기구를 함께 설계·평가합니다. | AI/ML 기반 공정 분석을 적지만 특정 언어 이름은 제시하지 않습니다. | [제품 회로·시스템 검사](04-제품회로와시스템검사_product-circuit-system-tests.md), [계측기](../현장계측과검증_measurement-validation/계측기_instruments/README.md) |
| 8 | PKG개발 · 이천 | 패키지 제품·소재·공정·장비와 고객 요구를 연결합니다. | 데이터 기반 문제 해결 경험을 적습니다. | [패키징](../반도체제조공정_semiconductor-fabrication/08-패키징과첨단집적_packaging.md), [HBM 적층](../반도체제조공정_semiconductor-fabrication/14-HBM의TSV와적층공정_hbm-tsv-stacking.md) |
| 9 | IT · 이천/분당 | 업무 애플리케이션·플랫폼·데이터 파이프라인·마스터 데이터·인프라를 구축·운영합니다. | C, C++, C#, Java, Python, JavaScript, SQL과 React·Spring Boot·Redis, LLM API·LangChain·Hugging Face·RAG 경험을 명시합니다. | [제조 IT·데이터](09-AI데이터와제조IT_ai-data-manufacturing-it.md) |
| 10 | System Architecture / Software Solution · 분당 | 데이터센터·xPU·메모리 시스템 구조와 AI 모델·플랫폼·시스템 SW를 연구합니다. | UCIe, CXL, NVLink, 이더넷, 컨테이너·Kubernetes 등 경험을 적습니다. 특정 프로그래밍 언어 이름은 제시하지 않습니다. | [AI·시스템 성능](09-AI데이터와제조IT_ai-data-manufacturing-it.md), [고성능 계산](../분야_topics/42-고성능병렬계산_hpc-parallel/README.md) |
| 11 | 양산기술 · 이천/청주/용인 | 양산 공정·장비 조건과 파생 제품을 다루고 AMHS 설계·운영·제어도 설명합니다. | TEST·분석 프로그램 등 프로그래밍 경험을 적습니다. | [공정·설비 검사](07-공정설비와패키지의검사_process-equipment-package-tests.md), [AMHS](09-AI데이터와제조IT_ai-data-manufacturing-it.md#4-amhs는-데이터와-실제-이동을-함께-맞춥니다) |
| 12 | 양산기술(P&T) · 이천/청주 | Package·Test 공정을 운영하고 수율·품질·소재·장비를 관리합니다. | 데이터 분석·문제 해결 경험을 적습니다. | [제품·테스트와 양산의 차이](08-메모리제품과테스트개발_memory-product-test-engineering.md#1-비슷해-보이는-직무가-다른-결과물을-만듭니다) |
| 13 | 기반기술 · 이천/청주/용인 | DM·AT·Mask·소재·Machine Engineering·결함/환경 제어를 담당합니다. | AI 모델·알고리즘의 적용 경험을 적습니다. | [AI·계측 연결](09-AI데이터와제조IT_ai-data-manufacturing-it.md), [공정 계측](07-공정설비와패키지의검사_process-equipment-package-tests.md) |
| 14 | 품질보증 · 이천/청주 | 제품 인증, 양산 품질, 고객 품질, 불량 분석으로 제품 전 주기를 관리합니다. | 프로그래밍 관련 역량·경험을 적습니다. | [메모리 검사·품질](08-메모리제품과테스트개발_memory-product-test-engineering.md) |
| 15 | 양산관리 · 이천/청주/용인 | 생산 계획·진도·생산능력·물류의 데이터와 시뮬레이션을 다룹니다. | SQL, Python 및 엑셀·파워포인트를 명시합니다. | [생산 데이터의 연결](09-AI데이터와제조IT_ai-data-manufacturing-it.md) |
| 16 | Utility기술(공조·배기, 배관) · 이천/청주/용인 | 청정 환경·냉동공조·공급 배관·hook-up을 설계·운영합니다. | 배관 분야에서 AutoCAD 경험을 적습니다. | 아래 Utility 구분, [인프라·검사](07-공정설비와패키지의검사_process-equipment-package-tests.md) |
| 17 | Utility기술(Gas, Chemical, 수처리) · 이천/청주/용인 | 가스·약액·초순수·공업용수·폐수 공급/처리와 중앙 감시를 다룹니다. | 데이터 분석 도구, CAD·공정 모사 도구 경험을 적습니다. | 아래 공급 품질·배출 품질, [공정·설비](07-공정설비와패키지의검사_process-equipment-package-tests.md) |
| 18 | Utility기술(전기, 제어) · 이천/청주/용인 | 전력 인프라·설비 감시/제어·에너지 효율을 관리합니다. | PLC 프로그래밍·산업 네트워크·머신러닝 경험을 적습니다. | 아래 전기·제어 구분, [제어와 감시](09-AI데이터와제조IT_ai-data-manufacturing-it.md) |
| 19 | Utility기술(건축, BIM/5D) · 이천/청주/용인 | 건설·유지관리와 3D 데이터 기반 Virtual FAB를 다룹니다. | AutoCAD, Revit, Navisworks, Dynamo 등을 명시합니다. | 아래 BIM·설비 연결, [데이터 거버넌스](09-AI데이터와제조IT_ai-data-manufacturing-it.md) |
| 20 | SHE(안전) · 이천/청주/용인 | 공정·예방 안전, 로봇/ICT 안전, 협력업체, 소방·방재, 안전 문화를 다룹니다. | 특정 언어 이름은 제시하지 않습니다. | 아래 SHE의 관측 대상 |
| 21 | SHE(보건) · 이천/청주/용인 | 작업환경·국소배기·노출·보호구와 구성원 건강 관리를 다룹니다. | 특정 언어 이름은 제시하지 않습니다. | 아래 안전·보건·환경 구분 |
| 22 | SHE(환경, 화학물질관리) · 이천/청주/용인 | 오염물질·화학물질 문서·온실가스·수환경과 규제 대응을 다룹니다. | Office 활용·외국어 경험을 적습니다. | 아래 환경 데이터의 기준·이력 |
| 23 | SHE(P&S기술) · 이천/청주/용인 | Dry Pump·Scrubber와 부속 장비를 예방 정비하고 성능 데이터를 분석합니다. | 특정 언어 이름은 제시하지 않습니다. | 아래 진공·배기 처리 구분 |
| 24 | 영업 / 마케팅 / 상품기획 / 신제품사업화 · 이천/서울 | 수요·기술·고객 인증·제품 로드맵·수익성을 연결합니다. | 특정 프로그래밍 언어 이름은 제시하지 않습니다. | 아래 기술·사업 연결과 [데이터 분석](09-AI데이터와제조IT_ai-data-manufacturing-it.md) |

지역 표시는 이 판의 직무 제목에 적힌 범위입니다. 25쪽은 최종 근무지 결정과 입사 후 변경 가능성을 별도로 설명합니다.

## 2. 설계·소자·제품·양산이 이어지는 방식

한 제품에서 오류가 발견되더라도 같은 팀이 모든 원인을 같은 방법으로 찾지는 않습니다.

| 단계 | 설명할 수 있어야 하는 내용 | 대표 산출물의 예 |
| --- | --- | --- |
| 설계 | 회로가 어떤 입력·시간·전압 조건에서 요구 동작을 해야 하는지 정합니다. | 회로/RTL, 배치 데이터, 시뮬레이션·coverage 기록입니다. |
| 소자·R&D 공정 | 그 회로를 구현할 소자·재료·공정의 특성과 분포를 만듭니다. | 소자 모델, 공정 통합 기준, 계측·불량 분석 자료입니다. |
| Product Engineering | 설계·공정·고객 조건을 실제 제품 시험으로 연결합니다. | 테스트 항목·프로그램, 특성 분포, 불량 분석과 판정 근거입니다. |
| 양산기술·P&T | 많은 제품을 반복 생산하는 과정에서 조건·장비·검사를 안정적으로 운영합니다. | 공정/설비 이력, 수율·처리량·시험 시간과 변경 전후 비교입니다. |
| 품질보증 | 인증·양산·출하·고객 문제에서 필요한 품질 근거를 관리합니다. | 인증 평가, 출하 검사·변경 관리, 고객 불량의 조사·대책 기록입니다. |

위 산출물은 원문 업무를 학습 관점으로 연결한 예입니다. 특정 사내 문서명이나 결재 체계를 뜻하지 않습니다. 실제 검사가 어떻게 달라지는지는 [메모리 제품과 테스트 개발](08-메모리제품과테스트개발_memory-product-test-engineering.md)에서 이어집니다.

설계의 C code 검증에서는 ‘계산이 맞는가’와 ‘정해진 클록·리셋·버스 규칙을 지키는가’를 나눕니다. C 참조 모델이 계산의 기대값을 만들고 RTL 시뮬레이션이 시간에 따른 신호를 다룰 수 있습니다. 한쪽의 통과가 다른 쪽의 전 검증을 대신하지 않습니다. [하드웨어 검증 기초](../분야_topics/14-하드웨어검증_hardware-verification/README.md)와 [칩 설계·평가](06-칩설계와평가분석_chip-design-characterization.md)를 함께 읽으시면 좋습니다.

## 3. Utility·기반기술·SHE에서 ‘검사’가 가리키는 것

원문 13쪽의 기반기술은 계측·분석·마스크·소재·장비·결함/환경 제어를 함께 묶습니다. DM은 원문에서 Defect & Metrology Inspection, AT는 Analysis Technology로 풀어 적습니다. 반면 4쪽의 EPM, d-MTS 등은 이 PDF에 상세 정의가 없으므로 약어만 보고 회사 내부 지표를 새로 정의하지 않습니다.

| 분야 | 확인하려는 대상 | 처음 구분할 개념 |
| --- | --- | --- |
| 공조·배기 | 청정 환경과 공기·열·배출의 상태입니다. | 온도·습도·압력·유량·입자·배출 농도는 서로 다른 값입니다. |
| 가스·약액·물 공급 | 공정에 필요한 자원을 필요한 상태로 공급하는 일입니다. | 공급량, 순도, 압력, 오염과 폐수 배출 품질을 나눕니다. |
| 전기 | 설비에 안정적인 전력을 공급하는 일입니다. | 전력 사용량과 순간 전압 강하·정전·보호 동작은 다른 관측입니다. |
| 제어 | 센서의 관측을 제어기·작동기 동작으로 연결합니다. | 측정·설정값·알람·인터록·실제 구동 상태를 구분합니다. |
| 건축·BIM | 건물·설비·배관 등의 공간·변경 데이터를 맞춥니다. | 보기 좋은 3D 모델과 실제 설치 좌표·설비 ID가 일치하는 모델은 다릅니다. |
| P&S | 원문이 풀어 쓴 Pump & Scrubber입니다. | 펌프가 진공·배기를 만드는 기능과 스크러버가 배출물을 처리하는 기능을 구분합니다. |
| 안전·보건·환경 | 사고 위험, 작업자 노출·건강, 환경 영향의 서로 다른 대상을 관리합니다. | 제품 불량률과 작업자 노출값·환경 배출값은 같은 품질 지표가 아닙니다. |

이 표는 관측 대상을 구분하는 학습 설명입니다. 법정 검사 기준·작업 허가·설비 조작 절차를 대신하는 표가 아닙니다. 해당 현장의 승인된 절차와 판본이 있는 기준에 측정 기록을 연결하는 것이 중요합니다.

## 4. 영업·상품기획도 기술 구조를 읽습니다

원문 24쪽은 DRAM/NAND·컨트롤러·인터페이스·임베디드 시스템·AI 이해와 고객·내부 조직의 소통을 연결합니다. 따라서 기술 설명을 숫자로 바꾸는 능력이 중요합니다. 예를 들어 고객의 ‘메모리가 빠르다’는 요구를 대역폭, 지연시간, 용량, 전력, 사용 온도와 검증 조건으로 풀어야 제품·평가 조직과 같은 요구를 논의할 수 있습니다.

상품기획은 목표 사양과 로드맵을, 신제품사업화는 고객 인증과 출시 시점을, 마케팅은 시장·수익성·메시지를, 영업은 고객·수요·공급·판매를 함께 다룹니다. 해당 페이지가 하나의 제목으로 제시한 범위를 임의로 하나의 코딩 직무로 합치지 않습니다. 수요나 수익성을 분석할 때의 데이터 기준은 [제조 IT·데이터](09-AI데이터와제조IT_ai-data-manufacturing-it.md)에서 설명합니다.

## 5. 원문에 나온 도구를 공부하는 순서

1. 먼저 제품·공정·시험의 대상을 구분합니다. [반도체 제품별 단면](../반도체제조공정_semiconductor-fabrication/10-로직과메모리의공정차이_logic-memory-integration.md)을 읽고 DRAM 셀·NAND 셀·TSV가 맡는 역할부터 정리합니다.
2. 다음으로 입력·관측·기대값·판정 기준을 적습니다. [메모리 테스트](08-메모리제품과테스트개발_memory-product-test-engineering.md)의 시험 항목 표를 사용합니다.
3. 그 과정에서 필요한 프로그램을 고릅니다. [C·Python의 위치](10-C와Python이쓰이는위치_languages-in-the-workflow.md)에서 타깃 코드·시험 러너·데이터 분석의 차이를 봅니다.
4. 마지막으로 원본 데이터·도구 판본·조건·결과를 묶습니다. [판정과 기록](11-검사결과의판정과기록_test-decisions-evidence.md)에서 다른 사람이 같은 결과를 다시 확인할 수 있는 형태를 읽습니다.

AI IDE 경험도 6쪽에 적혀 있지만 도구 이름을 안다는 것과 요구 동작을 검증한다는 것은 다릅니다. 생성한 코드의 입력 범위·경계·메모리 접근·오류 처리와 테스트 근거를 설명할 수 있어야 합니다. 이 부분은 [펌웨어·소프트웨어 검증](05-펌웨어와소프트웨어검증_firmware-software-validation.md)과 연결됩니다.

## 출처와 확인 범위

기준 원본은 『2026 하반기 SK하이닉스 Talent hy-way(신입) Job Description』 25쪽입니다. 모든 페이지를 이미지로 렌더링하여 제목·지역·업무·경험 항목을 확인했습니다. 위 매핑은 원문 업무의 자체 요약이며, 상세 해설의 외부 근거는 각 연결 문서에 적었습니다. 파일 판본·해시와 원문 범위는 [출처 문서](출처와검토범위_SOURCES.md)에 있습니다.

## English

This map covers every role page in the supplied 2026 second-half SK hynix job description. Named programming languages are separated from general programming or data-analysis experience. The reading paths connect design, devices, product engineering, manufacturing, IT, utilities, SHE and commercial roles to their different work products and evidence requirements.

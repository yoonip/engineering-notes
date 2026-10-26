# 산업별 기술 설명의 출처와 확인 범위 | Sources and reading scope

[산업 목차](README.md) · [회사와 사업 분야](09-기업과사업분야_company-domain-map.md)

이 분류는 제품·설비·서비스를 전자·컴퓨터 기술과 연결해 읽는 학습 자료입니다. 기업의 사업 소개는 제품과 역할을 확인하는 근거로, 표준 기관·정부·공개 프로젝트의 기술 문서는 원리·인터페이스·검증 범위를 설명하는 근거로 사용했습니다. 구체적인 주장의 출처는 각 본문 가까이에 연결했습니다. 확인 기준일은 2026-10-26입니다.

## 1. 자료별 역할

| 자료 | 사용한 범위 | 구분할 내용 |
| --- | --- | --- |
| 기업·기관의 공식 소개 | 회사 이름·제품·서비스·공개된 시스템 구성입니다. | 홍보 문구만으로 경쟁 우위·채용 필수 요건·사내 구현을 확정하지 않습니다. |
| 정부·표준 기관 자료 | 원리·용어·해당 문서의 적용 조건·검증 책임입니다. | 공개 개요와 규격 전문, 초안과 최종본, 한 분야의 기준과 다른 분야의 적용을 구분합니다. |
| 공식 SDK·공개 소프트웨어 문서 | 컴포넌트·인터페이스·코드 구조·도구의 역할입니다. | 공개 구현이 있다는 사실과 특정 회사의 실제 채택은 별개의 주장입니다. |
| 기존 저장소의 코드·실험 기록 | 고정 원문·라이선스·줄별 해설·명시된 로컬 실행 조건입니다. | 산업 제품 전체의 시험이나 장비 실측으로 확대하지 않습니다. |
| 자체 그림·계산·업무 상황 | 정보 흐름·단위 관계·고장 조사 경계를 설명하는 예입니다. | 실제 회사의 설계도·검사 기준·현장 측정값으로 표시하지 않습니다. |

회사별 사업 자료의 직접 링크는 [기업 연결표](09-기업과사업분야_company-domain-map.md)에 모았습니다. 아래는 본문을 이해하는 데 중요한 기술 자료와 읽은 범위입니다.

## 2. 시스템·임베디드·네트워크

| 자료·판본 | 읽은 범위와 연결 |
| --- | --- |
| [NASA Systems Engineering Handbook 웹 부록](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) | 부록 D·E의 요구·검증 및 확인 매트릭스입니다. 시스템 요구를 관측 가능한 결과와 연결하는 데 사용했습니다. |
| [IEEE TSN 작업반](https://1.ieee802.org/tsn/) · [802.1AS-2025 개정 프로젝트 소개](https://1.ieee802.org/maintenance/802-1as-2025-revision-timing-and-synchronization-for-time-sensitive-applications/) | 시간에 민감한 네트워크와 동기화의 공개 범위 설명입니다. 후자는 개정 프로젝트 페이지이며 초안 표기를 규격 확정으로 읽지 않았습니다. |
| [NIST SP 800-82 Rev.3, 2023 최종본](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | OT와 성능·신뢰성·안전 조건을 고려하는 보안의 공개 개요입니다. 2026년에 안내된 Rev.4 초안과 구분했습니다. |
| [RFC 9110, 2022](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) | 9.2.2절의 HTTP 메서드 멱등성입니다. 메서드의 의미와 애플리케이션 업무 처리·중복 방지의 관계를 나누었습니다. |
| [MQTT 5.0 OASIS Standard, 2019](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) | 4.3절의 QoS 전달 의미입니다. 메시지 전달 보장과 외부 장치의 물리적 동작·업무 성공은 구분했습니다. |
| [Kubernetes 컴포넌트](https://kubernetes.io/docs/concepts/overview/components/) | 제어 평면과 노드의 역할 설명입니다. 문서 조사이며 클러스터 설치·장애 시험 기록이 아닙니다. |
| [NCCL User Guide의 collective operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html) | 확인 화면의 2.32.3 문서에서 AllReduce 등 연산의 의미를 읽었습니다. 특정 서버의 성능 측정으로 사용하지 않았습니다. |
| [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) | 로그·메트릭·트레이스의 목적과 관측 범위입니다. |

## 3. 자동차·가전·디스플레이·광학

| 자료 | 읽은 범위와 연결 |
| --- | --- |
| [현대자동차의 2020 E-GMP 발표](https://www.hyundai.com/worldwide/en/newsroom/detail/0000000812) · [기아 플랫폼 소개](https://worldwide.kia.com/en/innovation/performance/platform) | 전동화 구조·플랫폼 설명입니다. 과거 발표의 사양을 현행 전 차종의 사양으로 확대하지 않았습니다. |
| [현대모비스 기술](https://www.mobis.com/en/tech/tech.do) · [HL만도 chassis](https://www.hlmando.com/en/solution/chassis.do) | 전동화·센서·제동·조향·현가 등 제품 분류를 확인했습니다. 회사별 부품 구조·내부 코드를 추정하지 않았습니다. |
| [한국타이어 2025 기술 소개 PDF](https://www.hankooktire.com/content/dam/hankooktire/local/pdf/why-hankook/2025_Hankook_Tire_Technology_Introduction_ENG.pdf#page=50) | 50쪽의 TMS·TireHealth·FleetSupporter·logger를 포함한 공개 기술 소개입니다. 차량 TPMS와 자료의 TMS를 같은 약어로 처리하지 않았습니다. |
| [LS그룹의 2026년 7월 공식 발표](https://www.lsholdings.com/ko/media/news/6161346d33756d394970597242657444556c344a2b466c6e6e77584733564b35) | LS엠트론 농기계의 위치·통신·작업 지원 연결입니다. 목표·발표와 모든 기종의 기본 사양은 구분했습니다. |
| [LG전자 사업 소개](https://www.lg.com/global/about-lg/corporate-information/) · [LG디스플레이 OLED 설명](https://www.lgdisplay.com/eng/product/tv-display/transparent-oled) · [LG이노텍 광학 제품](https://www.lginnotek.com/product/op/01/list.do?locale=en) | 완제품·패널·광학 모듈의 사업 역할과 원리 설명입니다. 패널 방식·구동·광학 검사·연결 서비스는 각 본문에서 나누었습니다. |
| [webOS OSE 문서](https://www.webosose.org/docs/) · [libcamera 구조](https://docs.libcamera.org/master/libcamera_architecture.html) | 공개 SW의 구조·카메라 파이프라인입니다. LG 양산 제품의 비공개 코드와 동일하다고 설명하지 않았습니다. |
| [EMVA 1288 공식 자료](https://www.emva.org/standards-technology/emva-1288/emva-standard-1288-downloads-2/) | Release 4.0 Linear·General의 적용 구분입니다. 이미지 센서·카메라의 특성화와 광학계·AF/OIS 전체의 시험을 구분했습니다. |

구동기·전원·MIPI·패널·색/밝기·MTF 등 세부 원문은 [가전·디스플레이·광학 본문](02-가전과디스플레이및광학_consumer-display-optics.md)의 해당 절에 연결했습니다.

## 4. 방산전자·항공우주·해양조선

| 자료 | 읽은 범위와 연결 |
| --- | --- |
| [FAA AC 20-115D](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf) · [AC 20-152A](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-152A.pdf) | 각각 2017년·2022년 문서의 목적과 적용, 소프트웨어·전자 하드웨어 개발 보증의 범위입니다. 군용·우주 전체에 자동 적용하거나 환경·방사선 시험을 대신한다고 쓰지 않았습니다. |
| [NASA JSC 방사선 설명](https://www.nasa.gov/reference/jsc-radiation/) · [NEPP 방사선 자료](https://nepp.nasa.gov/pages/Radiation.cfm) | 전자 부품의 방사선 영향과 평가 범위입니다. 개별 부품의 우주 적합성 시험 결과는 제시하지 않았습니다. |
| [NASA cFS](https://cfs.gsfc.nasa.gov/) · [JPL F Prime](https://fprime.jpl.nasa.gov/) | 공개 비행 SW 프레임워크의 역할과 자료입니다. 본문에서 새 비행 제어 코드를 구현하지 않았습니다. |
| [IMO AIS](https://www.imo.org/en/ourwork/safety/pages/ais.aspx) · [IMO MASS Code 채택 발표](https://www.imo.org/en/mediacentre/pressbriefings/pages/imo-adopts-mass-code.aspx) | AIS의 정보 교환과 MASS의 2026-05-22 채택·2026-07-01 적용, SOLAS Chapter 1 화물선 범위, 이후 로드맵을 구분했습니다. |
| [IMO 주파수 제어 전동기](https://greenvoyage2050.imo.org/technology/frequency-controlled-electric-motors/) · [ABB 육상 전원 변환기](https://new.abb.com/power-converters-inverters/grid-interconnections/shore-to-ship-converters) | 전동기용 VFD와 선박·육상 전원 사이의 SFC를 구분했습니다. |
| [HD현대마린솔루션 HiCONiS](https://www.hd-marinesolution.com/kr/business/digital/integrated-control/contents) | IAS·PMS 등 공개 기능입니다. PMS·기관 자동화·항해 센서·상위 에너지 최적화는 역할별로 읽습니다. |

그 밖의 기업·선박·우주 기관의 공개 자료와 시험 도구는 [방산·항공우주](03-방산전자와항공우주_defense-aerospace.md), [해양·조선](04-해양조선과선박시스템_marine-shipbuilding.md)의 해당 절에 연결했습니다. 원문 그림을 복사해 실제 기체·선박 내부 구조로 제시하지 않았습니다.

## 5. 발전·플랜트·산업자동화

| 자료 | 읽은 범위와 연결 |
| --- | --- |
| [두산에너빌리티 원자력·MMIS](https://www.doosanenerbility.com/en/business/nuclear_large) · [가스터빈 시험 인프라](https://www.doosanenerbility.com/en/business/gas_turbine_infra) | 사업·계측제어·시험 설비의 공개 범위입니다. |
| [IAEA SSG-39, 2016](https://www-pub.iaea.org/MTCD/Publications/PDF/Pub1694_web.pdf) | 2.14–2.24절의 수명주기·V&V, 4.28–4.40절의 독립성·공통원인고장·다양성입니다. 원전 운전 설정이나 운전 코드를 제공한 자료가 아닙니다. |
| [IEC 62264-1:2013](https://webstore.iec.ch/en/publication/6675) · [IEC 62381:2024](https://webstore.iec.ch/en/publication/67572) | 공개 소개의 기업·제어 정보 모델과 공장·현장·통합 시험 범위입니다. 유료 규격 전문을 확보한 것으로 표시하지 않았습니다. |
| [포스코DX EIC](https://www.poscodx.com/kor/business/eicEngineering) · [현대엔지니어링 그룹 소개](https://www.hyundaimotorgroup.com/ko/group/hyundai-engineering) | 전기·계장·컴퓨터, 제조 IT 연계와 FEED/EPC의 사업 연결입니다. |
| [CODESYS 태스크 설정](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_task_configuration.html) · [OPC UA](https://opcfoundation.org/about/opc-technologies/opc-ua/) · [buildingSMART IFC](https://technical.buildingsmart.org/standards/IFC/) | 태스크·주기·우선순위, 정보 교환, 시설 데이터 모델의 공개 개념입니다. |
| [OpenFAST](https://openfast.readthedocs.io/en/main/) · [PyPSA](https://docs.pypsa.org/latest/) | 공식 개요와 해석 대상입니다. 발전소 실측이나 자체 시뮬레이션 실행 결과로 바꾸지 않았습니다. |

기관·센서·구동·전력망·설비·정비·OT 보안의 나머지 근거는 [발전·전력망](05-원자력과발전및전력망_nuclear-generation-grid.md), [산업자동화·플랜트](06-산업자동화와플랜트및기계_industrial-automation-machinery.md)에 나누어 두었습니다.

## 6. 의료·철도·도시 인프라

| 자료 | 읽은 범위와 연결 |
| --- | --- |
| [NIBIB MRI](https://www.nibib.nih.gov/science-education/science-topics/magnetic-resonance-imaging-mri) · [초음파](https://www.nibib.nih.gov/science-education/science-topics/ultrasound) | 신호 획득·자기장·공간 구분·음파 송수신의 공개 원리입니다. |
| [DICOM PS3.1](https://dicom.nema.org/medical/dicom/current/output/chtml/part01/chapter_1.html) | 확인 시점은 2026d입니다. PS3.1·PS3.2·PS3.3의 본문에 지정한 범위에서 객체·좌표·conformance를 읽었습니다. current 주소는 후속 판본으로 바뀔 수 있습니다. |
| [FDA Digital Health Terms](https://www.fda.gov/medical-devices/digital-health-center-excellence/digital-health-terms) | 디지털 의료·장치·소프트웨어의 용어 구분입니다. 해당 글의 문서·설명회 판본은 본문에 따로 표시했습니다. |
| [ERA ERTMS](https://www.era.europa.eu/domains/infrastructure/european-rail-traffic-management-system-ertms_en) | ETCS·ATO·RMR과 현행 공개 구성입니다. 차량 구동·TCMS·열차 제어·무선 통신의 역할을 나누었습니다. |
| FHWA·EPA·USGS | 도로 센서의 관측 원리, 수질 센서·탁도의 자료 품질, 구조 응답·기록 시스템의 상태 감시입니다. 직접 자료는 [의료·철도·도시 본문](08-의료와철도및도시시스템_medical-rail-cities.md)의 해당 절에 연결했습니다. |

## 7. 계산·그림·코드와 확인하지 않은 범위

흐름도는 제품의 역할과 정보 흐름을 설명하기 위해 직접 구성했습니다. 지연 합계·전류 환산·자료량·영상 전송량·왕복 시간 등 수치는 본문에서 가정을 밝힌 단위 계산입니다. 실제 검사 규격·제어 설정·제품 성능으로 제시하지 않았습니다.

코드의 출처·판본·이용 조건은 [공개 사례의 고정 원문과 이용 조건](../직무와실무기술_job-practice/사례_cases/코드출처와이용조건_CODE_SOURCES.md)에서 확인합니다. 이 산업 분류는 문서 조사와 학습용 설명이며 장비·임상·실차·선박·발전소의 시험 기록이 아닙니다.

출처의 일부 페이지는 검색 본문만 읽히거나 직접 접근이 제한되었습니다. NRC·현대엘리베이터 포털 등 해당 사례는 각 본문의 확인 범위에 표시했습니다. 회사 배포 자료를 PR Newswire에서 읽은 SK키파운드리 항목도 출처 성격을 따로 표시했습니다. 확인하지 못한 내부 설계·채택·고객 적용·인증·비교 성능은 채워 넣지 않았습니다.

## English

Company pages establish public business scope. Technical explanations cite standards bodies, public agencies, official documentation and original projects near the relevant claims. Public summaries, draft standards and full normative texts have different scopes. Authored diagrams, calculations and fault scenarios are educational explanations. No new industrial control implementation, hardware measurement, clinical test or certification is claimed.

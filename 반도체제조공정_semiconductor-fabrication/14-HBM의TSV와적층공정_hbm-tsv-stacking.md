# HBM의 TSV와 적층 공정 | HBM TSV and die-stacking integration

[공정 목차](README.md) · [로직·메모리 비교](10-로직과메모리의공정차이_logic-memory-integration.md) · [패키징 기초](08-패키징과첨단집적_packaging.md)

HBM은 DRAM 셀을 만드는 공정과, 완성한 다이를 얇게 만들고 수직으로 연결하는 공정을 함께 보아야 이해할 수 있습니다. 저장 셀의 전하는 각 DRAM 다이 안에 남고, TSV와 다이 사이 접합은 데이터·전원 등을 전달합니다. TSV 자체가 저장 커패시터인 것은 아닙니다.

이 글은 베이스 다이 위에 DRAM 코어 다이를 쌓는 대표적인 HBM 구조를 설명합니다. 공개 자료의 via-middle 흐름을 기준으로 하며, 제조사별 전체 양산 조건이나 모든 세대의 공통 레시피를 뜻하지 않습니다. 확인 기준일은 2026-10-26입니다.

## 1. 같은 단면에서 세 가지 크기를 구분합니다

![3D NAND의 셀 층과 HBM의 DRAM 다이·TSV·다이 사이 접합을 비교한 자체 개념도](그림_figures/3DNAND와HBM의적층단위_nand-hbm-stacking.svg)

왼쪽은 한 웨이퍼 안의 셀 층, 오른쪽은 따로 제조한 DRAM 다이의 접합입니다. 오른쪽 메모리 다이 세 장은 연결 관계를 보여 주는 예이며 제품의 표준 적층수를 뜻하지 않습니다. 실제 회로·범프·배선의 크기 비율은 생략했습니다.

| 관찰 범위 | 단면에 보이는 것 | 만드는 공정과 기능 |
| --- | --- | --- |
| DRAM 셀 | 접근 트랜지스터·저장 커패시터·word line·bit line | 한 비트의 저장과 접근을 담당합니다. [DRAM 공정](13-DRAM과3DNAND의공정단면_dram-3d-nand-integration.md)과 연결됩니다. |
| DRAM 다이와 TSV | 다이 내부 회로·수직 금속 경로·앞뒤 접속부 | 여러 층 사이의 신호·전원 경로를 제공합니다. 실리콘 안의 금속은 주변 회로와 절연해야 합니다. |
| HBM 스택과 시스템 패키지 | 코어 다이·베이스 다이·다이 간 접합·인터포저·로직 | 여러 메모리 다이의 연결을 GPU·ASIC 등의 외부 인터페이스로 이어 줍니다. |

위아래로 쌓인 DRAM은 3D 구조입니다. 이 HBM 스택을 GPU 옆에 나란히 놓아 인터포저로 연결한 전체 패키지는 2.5D로 설명할 수 있습니다. 같은 모듈에서 ‘HBM 내부의 수직 적층’과 ‘GPU–HBM 사이의 수평 연결’이 동시에 존재합니다. [SK하이닉스 GTC 2019 발표, 인쇄 7쪽의 HBM in 2.5D SiP](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9978-an-in-depth-study-of-hbm-presented-by-sk-hynix.pdf#page=8)는 두 범위를 나란히 보여 줍니다. 당시의 용량·속도·로드맵은 현대 제품 사양으로 사용하지 않습니다.

베이스 다이는 스택 아래에서 외부 연결과 필요한 로직 기능을 맡는 다이입니다. 구체적인 기능 배분은 세대·제품에 따라 달라집니다. SK하이닉스의 [2024-04-19 TSMC 협력 발표](https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/)는 HBM3E까지의 자체 베이스 다이와 HBM4용 TSMC 로직 공정 도입 계획을 구분합니다. DRAM 코어 다이와 베이스 다이가 반드시 같은 소자 공정에서 제조되는 것은 아닙니다. 이 협력 발표를 모든 제조사의 공통 분업으로 읽지는 않습니다.

## 2. 공식 그림으로 공정과 연결 위치를 봅니다

아래는 원문과 해당 그림으로 바로 가는 링크입니다. 그림을 저장소에 재배포하지 않고 제공처의 원문으로 연결했습니다.

| 공식 자료와 그림 | 그림을 읽는 순서 | 함께 구분할 내용 |
| --- | --- | --- |
| [SK하이닉스 Episode 8, Figure 6: TSV Packaging Process](https://news.skhynix.com/en/semiconductor-back-end-process-episode-8-the-process-stages-of-wafer-level-packages/) · [그림 원본](https://d18r0a86za96sg.cloudfront.net/wp-content/uploads/2026/05/27161230/SK-hynix_Semiconductor-Back-End-Episode-8_Image-06.png) | ①–③의 막힌 TSV와 Cu/CMP, ④의 회로 배선, ⑦–⑩의 뒤쪽 노출·접속을 비교합니다. | 원문의 그림 출처는 Hanol Publishing입니다. 마지막 패키지 예를 모든 HBM의 최종 외형으로 적용하지 않습니다. |
| [같은 글 Figure 7: WSS](https://news.skhynix.com/en/semiconductor-back-end-process-episode-8-the-process-stages-of-wafer-level-packages/) · [그림 원본](https://d18r0a86za96sg.cloudfront.net/wp-content/uploads/2026/05/27161235/SK-hynix_Semiconductor-Back-End-Episode-8_Image-07.png) | 접착제 도포 → 캐리어 접합 → 뒤쪽 연삭 → 뒤쪽 범프 → 분리·세정을 따라갑니다. | 캐리어는 가공 중의 지지체이며 완성 스택에 남는 메모리 다이가 아닙니다. |
| [SK하이닉스 MR-MUF 설명의 TC-NCF/MR-MUF 비교](https://news.skhynix.com/en/rulebreaker-revolutions-mr-muf-unlocks-hbm-heat-control/) · [그림 원본](https://d18r0a86za96sg.cloudfront.net/wp-content/uploads/2026/05/27145807/SK-hynix_Rulebreaker_1_MR-MUF_01.png) | 왼쪽의 층별 필름과 오른쪽의 적층 사이를 채우는 액상 몰드 재료를 비교합니다. | 이 그림은 SK하이닉스가 제시한 방식 비교입니다. 색이나 묘사만으로 타사 최신 제품의 열 성능을 정하지 않습니다. |
| [TSMC CoWoS-S·R·L 구조](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm) | 세 구조의 HBM 아래에서 이어지는 실리콘·RDL·국부 연결을 비교합니다. | HBM 내부 공정이 아니라 여러 다이를 시스템으로 연결하는 단계입니다. |
| [TSMC SoIC의 chiplet 분할·재집적 그림](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm) | Features의 (a)–(d)와 Holistic 3D System Integration을 비교합니다. | 로직 등의 3D 집적을 HBM 내부의 DRAM 적층과 구분합니다. |

## 3. TSV 형성과 뒤쪽 노출의 순서

via-middle은 소자를 만든 FEOL 뒤, 본격적인 회로 금속배선 BEOL 전에 TSV를 형성하는 구분입니다. 처음에는 웨이퍼를 완전히 뚫지 않는 막힌 구멍, blind via로 만들 수 있습니다. 이후 뒤쪽 실리콘을 줄여 금속 끝을 노출하면 앞뒤를 잇는 경로가 됩니다. 처음 식각 깊이와 최종 다이 두께가 함께 설계되는 이유입니다. [SK하이닉스 Episode 8의 Via middle 정의](https://news.skhynix.com/en/semiconductor-back-end-process-episode-8-the-process-stages-of-wafer-level-packages/), [Fraunhofer IZM의 TSV Integration 본문](https://www.izm.fraunhofer.de/en/abteilungen/wafer-level-system-integration/process_technologies/TSV_TGV_integration/TSV_integration.html)

| 대표 단계 | 단면에서 달라지는 부분 | 다음 단계와 연결되는 조건 |
| --- | --- | --- |
| 1. 코어·베이스 다이의 소자 형성 | DRAM 셀 또는 로직 소자를 형성합니다. | TSV 위치와 주변 회로 공간을 함께 설계합니다. |
| 2. TSV 구멍 식각 | 실리콘 내부에 깊은 공간이 생깁니다. | 깊이·측벽·바닥 상태를 확인합니다. |
| 3. 절연 라이너·배리어·시드 | 구멍 벽에 서로 다른 기능의 얇은 막이 생깁니다. | 절연성, 확산 억제, 도금 전도 경로를 구분합니다. |
| 4. Cu 채움과 표면 CMP | 구멍은 금속으로 채워지고 과잉 표면막은 제거됩니다. | 내부 void와 표면 높이는 다른 검사 항목입니다. |
| 5. BEOL·외부 패드 | 소자와 TSV를 회로 배선에 연결합니다. | 회로 금속배선의 BEOL과 이후 조립 공정을 구분합니다. |

위 표는 [Fraunhofer IZM의 막힌 구멍·절연·Cu 채움·배선 설명](https://www.izm.fraunhofer.de/en/abteilungen/wafer-level-system-integration/process_technologies/TSV_TGV_integration/TSV_integration.html)과 앞의 via-middle 정의를 연결한 대표 흐름입니다. 라이너는 전기 절연, 배리어는 Cu 확산 억제, 시드는 전해도금을 시작할 전도 경로를 맡습니다. 하나의 ‘보호막’으로 묶으면 절연 불량과 도금 불연속의 원인을 구별하기 어렵습니다.

via-first·via-last라는 다른 통합 위치도 있습니다. TSV를 넣는 시점이 달라지면 허용 열 이력, 노출된 재료, 회로·배선과의 정렬 조건도 달라집니다. ‘TSV 공정’이라는 이름만으로 위 표의 순서가 확정되지는 않습니다.

## 4. 웨이퍼의 뒤쪽을 가공하고 다이를 준비합니다

Amkor의 [2.5D/3D TSV 설명](https://amkor.com/technology/25d-3d-tsv/)은 이미 TSV가 형성된 웨이퍼를 받아 박막화·노출·뒤쪽 배선을 수행하는 범위를 명시합니다. 같은 TSV 관련 업무라도 구멍을 처음 만드는 공정과 뒤쪽에서 접속을 완성하는 공정은 담당 범위가 다를 수 있습니다.

| 대표 단계 | 단면과 취급 상태의 변화 | 확인할 항목 |
| --- | --- | --- |
| 앞면 범프·웨이퍼 검사 | 접속부를 만들고 다이별 전기적 상태를 선별합니다. | 범프 위치, 접촉 상태, 최초 시험과 수리·재시험 이력입니다. |
| 임시 접합 | 회로 면 쪽을 캐리어로 지지합니다. | 접착층의 빈 공간·접합 강도·범프 보호입니다. |
| 뒤쪽 연삭·TSV reveal | 실리콘을 줄여 TSV 끝에 접근하고 노출합니다. | 남은 두께, 전체 두께 편차, 손상과 노출 높이입니다. |
| 뒤쪽 절연·접속 형성 | 뒤쪽 절연막과 필요한 재배선·접속부를 만듭니다. | Cu 접속부와 주변 절연막의 높이·연속성입니다. |
| 캐리어 분리·다이 분리 | 얇은 다이를 테이프 등으로 지지하며 개별화합니다. | 잔류 접착제, 균열, 휨, 위치와 다이 식별 정보입니다. |

RDL, redistribution layer는 기존 접속 위치를 필요한 위치로 이어 주는 재배선층입니다. 모든 다이의 앞뒤에서 같은 수의 RDL을 만드는 것은 아닙니다. 공정 구성에 따라 범프·검사·임시 지지의 세부 위치도 달라집니다. 표의 취급 흐름은 Amkor의 MEOL 항목과 [SK하이닉스의 WSS 재료 설명](https://news.skhynix.com/en/semiconductor-back-end-process-episode-10-roles-of-materials-in-wafer-level-packaging/)을 함께 근거로 합니다.

WSS, wafer support system은 얇은 웨이퍼를 가공할 수 있도록 지지하는 체계입니다. 접착제는 뒤쪽 가공 중에는 버티고 분리할 때에는 회로·범프에 손상과 잔류물을 줄여야 합니다. 따라서 캐리어를 붙였다고 휨이나 파손 가능성이 완전히 없어지는 것은 아닙니다. 임시 접합층의 상태와 박막화 후 실제 형상을 확인해야 합니다.

## 5. MR-MUF·TC-NCF·하이브리드 본딩

TSV는 다이 안의 수직 도체이고 본딩은 서로 다른 다이의 경계를 잇는 작업입니다. TSV가 있어도 다이 사이 접속이 끊기면 수직 경로는 완성되지 않습니다.

| 접합 방식 | 다이 경계에서 하는 일 | 단면·공정에서 달라지는 관리 항목 |
| --- | --- | --- |
| MR-MUF | mass reflow로 적층 다이의 범프를 접속하고, molded underfill로 틈을 채워 보호합니다. | 솔더 접합, 틈 채움, 수지 경화와 얇은 다이의 위치·휨을 함께 관리합니다. |
| TC-NCF | 비전도성 필름을 사용하면서 열·압력으로 접합합니다. | 필름과 범프가 함께 놓인 좁은 틈의 접합·재료 이동·변형을 관리합니다. |
| 하이브리드 본딩 | 금속–금속과 절연체–절연체를 직접 접합합니다. | 솔더 범프 높이보다 표면 높이·거칠기·입자·정렬·Cu 패드의 상태가 중요해집니다. |

MR-MUF의 액상 재료는 금속 신호선을 대신하는 접착 전극이 아닙니다. 전기 접속은 범프 등의 금속 경로가 맡고, 주변 몰드 재료는 틈 채움·보호·열·기계적 특성에 관여합니다. MR과 MUF도 역할이 다른 작업입니다. [SK하이닉스의 MR-MUF 정의와 개발 설명, 2024-07-30](https://news.skhynix.com/en/rulebreaker-revolutions-mr-muf-unlocks-hbm-heat-control/)

삼성전자의 [HBM3E 12H 개발 발표](https://semiconductor.samsung.com/kr/news-events/news/samsung-develops-industry-first-36gb-hbm3e-12h-dram/)는 Advanced TC NCF와 신호·방열 목적에 따른 다른 크기의 범프를 설명합니다. 이는 해당 제품 설계의 사례이며 TC-NCF가 항상 특정한 간격·범프 크기를 가져야 한다는 정의는 아닙니다.

하이브리드 본딩은 솔더를 더 얇게 만든다는 설명만으로 충분하지 않습니다. NIST는 Cu·SiO₂ 접합 준비 구조의 표면 기계적 성질을 AFM으로 측정하는 연구를 소개합니다. AFM은 미세 탐침으로 표면을 읽고 힘에 대한 반응도 측정하는 장비입니다. 접합 전 평탄도·재료 반응을 다루는 문제로 옮겨 간다는 점이 중요합니다. [NIST, 2026-01-29의 hybrid bonding 정의·측정 대상](https://www.nist.gov/news-events/news/2026/01/nanoscale-mechanical-characterization-hybrid-bonding-ready-structures)

### 공식 자료에서 확인한 적용 상태

| 자료 시점 | 확인한 상태 | 공정 비교에 쓰는 범위 |
| --- | --- | --- |
| [SK하이닉스 2024-09-26 발표](https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-the-world-first-12-layer-hbm3e/) | 12단 HBM3E 양산 시작과 Advanced MR-MUF 적용을 발표했습니다. | 박막 다이의 휨과 적층 안정성에 대응한 회사 보고입니다. |
| [삼성전자 HBM3E 제품 본문](https://semiconductor.samsung.com/dram/hbm/hbm3e/) | 2026-10-26 확인한 본문은 12단 제품의 양산과 Advanced TC NCF를 설명합니다. | 과거 개발 발표와 구분한 제품 페이지의 상태입니다. |
| [SK하이닉스 2026-06-18 발표](https://news.skhynix.com/en/sk-hynix-ships-samples-of-12-layer-next-gen-hbm4e-2/) | 12단 HBM4E 샘플 출하와 Advanced MR-MUF를 발표했습니다. | 이 발표의 샘플 출하를 양산 출하로 바꾸지 않습니다. |
| [SK하이닉스 Advanced Memory Package Architecture](https://research.skhynix.com/research-areas/advanced-package/advanced-memory-package-architecture) | 미세 범프에서 하이브리드 본딩으로의 전환을 연구 방향으로 설명합니다. | 모든 현행 HBM에 하이브리드 본딩이 적용되었다는 근거는 아닙니다. |

위 표는 비교에 사용한 자료의 상태를 식별하기 위한 것입니다. 제조사 전체의 현재 제품 목록이나 시장 순위를 나타내지 않습니다.

## 6. 완성 스택과 GPU를 연결하는 단계

CoWoS는 TSMC의 2.5D 집적 계열이며 HBM 내부 범프 접합 방식의 이름이 아닙니다. [공식 CoWoS 본문의 각 구조 설명](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)은 다음처럼 나뉩니다.

| 구조 | 로직·HBM 사이의 연결 구조 | 단면에서 볼 부분 |
| --- | --- | --- |
| CoWoS-S | 실리콘 인터포저를 사용합니다. | HBM 아래의 실리콘과 그 안팎의 접속을 봅니다. |
| CoWoS-R | 폴리머와 Cu 배선으로 된 RDL 인터포저를 사용합니다. | 모든 연결 면적이 한 장의 실리콘이라고 읽지 않습니다. |
| CoWoS-L | RDL 기반 인터포저에 국부 실리콘 연결인 LSI 등을 결합합니다. | 넓은 재배선과 조밀한 국부 연결을 구분합니다. |

SoIC는 다이·웨이퍼 수준 3D 집적 계열입니다. [TSMC SoIC 본문](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm)은 서로 다른 기능·크기·공정의 칩렛을 집적하고, 그 결과를 다시 CoWoS 등에 통합할 수 있다고 설명합니다. SoIC로 만든 로직 적층체, 옆에 놓인 HBM 스택, 이를 잇는 인터포저가 한 시스템에 함께 들어갈 수 있습니다. 각 기술 이름을 제품 전체의 유일한 공정명으로 이해하면 연결 경계가 혼동됩니다.

HBM 베이스 다이, 실리콘 인터포저, 유기 패키지 기판은 서로 다른 부품입니다. 셋을 모두 ‘기판’이라고만 부르기보다, 회로가 있는 다이인지·다이 사이를 잇는 배선 구조인지·보드 쪽 외부 접속을 맡는 기판인지 구분해 읽습니다.

## 7. 불량이 생긴 경계를 먼저 찾습니다

다음은 공개된 고장 기구를 학습용 조사 순서로 연결한 자체 진단 예입니다. 실제 HBM을 제조하거나 아래 조치의 효과를 측정한 기록은 아닙니다.

| 관찰된 증상 | 서로 다른 원인 후보 | 나누어 확인하는 방법 | 조치 방향과 재확인 |
| --- | --- | --- | --- |
| 뒤쪽 노출 후 TSV 높이가 위치별로 다릅니다. | 남은 Si 두께 편차, reveal·CMP 차이, 열 이력에 따른 Cu 돌출입니다. | 박막화 직후·열처리 후의 같은 위치를 비교하고 Si 두께와 Cu 상대 높이를 따로 측정합니다. | 제거량만 늘리기 전에 변화가 시작된 단계를 찾습니다. 절연 상태·접속 저항도 다시 확인합니다. |
| 일부 다이 경계에서 전기적 연결이 끊깁니다. | 정렬, 다이 휨, 접속부 오염·미접합, 내부 TSV 불량입니다. | 적층 전 다이 결과, 접합 후 연결 시험, 휨·접합 단면을 대조합니다. | 위치·열·표면 문제를 나눈 뒤 해당 공정으로 되돌아갑니다. 재시험 통과만으로 접합 신뢰성을 판정하지 않습니다. |
| 충전 재료의 void 또는 박리가 관찰됩니다. | 젖음·공급·경화·오염·틈 변화입니다. | 계면 위치와 틈 높이, 재료 이력, 초음파·단면을 연결합니다. | 재료·주입·경화 중 확인된 원인을 평가합니다. 전기·열·기계 결과를 함께 봅니다. |
| 고부하에서만 메모리 오류가 늘어납니다. | 온도 상승, 전원 강하, 신호 여유 부족, 잠재 접속 결함입니다. | 온도·전류·동작 패턴을 맞추고 스택·채널·site별 분포를 비교합니다. | 냉각만 바꾸어 원인을 확정하지 않습니다. 전원·신호 조건을 분리한 대조 시험이 필요합니다. |

Cu 돌출의 근거인 Liu 외의 [2018년 연구 초록](https://www.jstage.jst.go.jp/article/jiepeng/11/0/11_E17-014-1/_article/-char/en)은 가열·냉각 중 되돌아오는 열팽창과 남는 소성변형을 구분합니다. Cu와 주변 구조의 열팽창 차이가 응력을 만들고 비가역 변형으로 이어질 수 있다는 설명입니다. 이 논문의 시편·온도를 최신 HBM의 실제 불량률이나 허용값으로 옮기지 않습니다.

임시 접착층의 void·박리·잔류물은 [SK하이닉스 WSS 재료 설명](https://news.skhynix.com/en/semiconductor-back-end-process-episode-10-roles-of-materials-in-wafer-level-packaging/)에서, 언더필 흐름과 외부 접합의 실제 연구 사례는 [패키징 장의 13절](08-패키징과첨단집적_packaging.md#13-주요-변수와-계측)에서 이어집니다. 적층체의 열 문제는 실리콘 두께만 아니라 접합층·보호재·전력 분포·전체 방열 경로와 함께 보아야 합니다.

## 8. 적층 전 검사와 적층 후 검사는 다른 결함을 찾습니다

KGD, known good die는 정해진 검사 조건을 통과한 개별 다이입니다. KGSD, known good stacked die는 적층한 상태에서 필요한 검사를 거친 스택을 가리킵니다. 적층 전에 다이가 통과했어도 이후 생긴 TSV 노출·접합·열·취급 문제까지 통과한 것은 아닙니다.

[Advantest의 2023-11-29 기술 설명 자료, 인쇄 16쪽](https://www.advantest.com/document/en/investors/ir-library/briefing/E_IR_technical_briefing_231129.pdf#page=16)은 DRAM·로직 웨이퍼 검사와 적층 웨이퍼 검사를 구분한 예를 보여 줍니다. [Teradyne의 2025-08-04 Magnum 7H 발표](https://investors.teradyne.com/news-events/press-releases/detail/419/teradyne-unveils-magnum-7h---the-next-generation-memory-tester-for-high-bandwidth-memory-devices)는 분리 전 KGSD·chip-on-wafer와 분리 후 HBM 시험을 지원하는 구성을 설명합니다. 시험 장비가 지원하는 검사 위치와 모든 고객의 실제 검사 순서는 구분합니다.

| 검사 위치 | 새로 확인할 대상 |
| --- | --- |
| 개별 코어·베이스 다이 | 셀·로직·소자·배선·접속의 주어진 시험 조건입니다. |
| 적층 후 | 다이 간 연결, 적층 때문에 달라진 전원·열·신호 조건입니다. |
| 다이·스택 분리 후 | 분리·취급에 따른 변화와 최종 접속 상태입니다. |
| 로직과 패키지 통합 후 | 로직–HBM 경로와 실제 시스템 동작의 상호작용입니다. |

### 자체 계산: 양품 다이만 골라도 접합 수율은 남습니다

8개 코어 다이와 1개 베이스 다이를 쓰는 가상 구조를 가정합니다. 선택하지 않은 각 다이가 양품일 확률은 0.99, 다이 사이 한 접합 경계 전체가 정상일 확률은 0.995이며 서로 독립이라고 가정합니다. 코어–코어 7곳과 코어–베이스 1곳으로 접합 경계는 8곳입니다.

    선택 전 모든 다이·경계가 정상일 확률
    = 0.99^9 × 0.995^8 ≈ 0.8776 = 87.76%

    완벽하게 선별한 양품 다이만 사용한 뒤의 접합 통과 확률
    = 0.995^8 ≈ 0.9607 = 96.07%

여기서 0.995는 범프 한 개의 확률이 아니라 한 경계의 필요한 연결 전체를 묶은 가정입니다. 이 모형은 실제 제조 수율 예측이 아닙니다. 공통 원인, 수리, 검사 누락과 접합 간 상관관계도 생략했습니다. 계산이 보여 주는 것은 적층 전 선별과 적층 후 접합 관리가 서로 대체되지 않는다는 점입니다.

## 출처와 확인 범위

| 자료·시점 | 읽은 범위와 사용한 내용 |
| --- | --- |
| [SK하이닉스 Episode 8, 2023-10-05](https://news.skhynix.com/en/semiconductor-back-end-process-episode-8-the-process-stages-of-wafer-level-packages/) | TSV Package Process·WSS 본문과 Figure 6·7 원본을 확인했습니다. via-middle 정의·앞뒤 가공·지지체의 관계를 사용했습니다. |
| [Fraunhofer IZM, TSV Integration](https://www.izm.fraunhofer.de/en/abteilungen/wafer-level-system-integration/process_technologies/TSV_TGV_integration/TSV_integration.html) | 본문·Capabilities·R&D Services의 blind via·절연·배리어/시드·Cu·reveal을 확인했습니다. 연구기관의 장비 치수 범위를 HBM 제품 사양으로 사용하지 않았습니다. |
| [Amkor, 2.5D/3D TSV Packaging](https://amkor.com/technology/25d-3d-tsv/) | 도입부·MEOL 목록의 수입 웨이퍼 조건, 임시 지지·박막화·노출·뒤쪽 접속 범위를 확인했습니다. |
| [SK하이닉스 Episode 10, 2023-12-11](https://news.skhynix.com/en/semiconductor-back-end-process-episode-10-roles-of-materials-in-wafer-level-packaging/) | WSS의 캐리어·임시 접착제·테이프와 void·박리·잔류물 조건을 확인했습니다. |
| [SK하이닉스 MR-MUF, 2024-07-30](https://news.skhynix.com/en/rulebreaker-revolutions-mr-muf-unlocks-hbm-heat-control/) | 정의·TC-NCF/MR-MUF 비교 그림·소재와 얇은 다이 취급을 확인했습니다. 공급사의 열 성능 수치를 경쟁 제품의 공통 우열로 옮기지 않았습니다. |
| [삼성전자 HBM3E 12H 개발 발표](https://semiconductor.samsung.com/kr/news-events/news/samsung-develops-industry-first-36gb-hbm3e-12h-dram/) | Advanced TC NCF·범프 크기·샘플 제공과 당시 양산 계획을 확인했습니다. 현재 상태와 혼동하지 않았습니다. |
| [삼성전자 HBM3E 제품 본문](https://semiconductor.samsung.com/dram/hbm/hbm3e/) | 12단 제품 양산 설명과 Advanced TC NCF의 역할입니다. |
| [SK하이닉스 12단 HBM3E, 2024-09-26](https://news.skhynix.com/en/sk-hynix-begins-volume-production-of-the-world-first-12-layer-hbm3e/) | 양산 시작·박막 다이·Advanced MR-MUF 적용입니다. |
| [SK하이닉스 HBM4E, 2026-06-18](https://news.skhynix.com/en/sk-hynix-ships-samples-of-12-layer-next-gen-hbm4e-2/) | 샘플 출하와 사용한 접합 기술입니다. |
| [SK하이닉스–TSMC 협력, 2024-04-19](https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/) | 베이스 다이 역할·당시의 HBM4 로직 공정 계획·CoWoS 통합 협력입니다. |
| [SK하이닉스 Advanced Memory Package Architecture](https://research.skhynix.com/research-areas/advanced-package/advanced-memory-package-architecture) | Next-Generation HBM의 TSV·미세 범프·하이브리드 본딩·베이스 다이 연구 방향입니다. 본문 안의 외부 홍보 이미지는 구조 근거로 쓰지 않았습니다. |
| [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm) · [SoIC](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm) | S·R·L의 재료·연결 구조 설명과 SoIC의 chiplet·CoWoS 통합 설명입니다. |
| [NIST, 2026-01-29](https://www.nist.gov/news-events/news/2026/01/nanoscale-mechanical-characterization-hybrid-bonding-ready-structures) | 금속/절연체 직접 접합과 Cu/SiO₂ 접합 준비 구조의 AFM 측정 범위입니다. |
| [Liu 외, Transactions of JIEP 11, 2018](https://www.jstage.jst.go.jp/article/jiepeng/11/0/11_E17-014-1/_article/-char/en) | 공식 초록·서지·DOI 10.5104/jiepeng.11.E17-014-1입니다. 열팽창·소성변형을 사용했으며 전문 전체를 읽었다는 뜻은 아닙니다. |
| [SK하이닉스 GTC 2019 발표](https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9978-an-in-depth-study-of-hbm-presented-by-sk-hynix.pdf) | 인쇄 7·10·12·13쪽의 HBM 스택·2.5D·검사·접속 구분입니다. 당시 미래 계획은 현재 실적으로 쓰지 않았습니다. |
| [Advantest, 2023-11-29](https://www.advantest.com/document/en/investors/ir-library/briefing/E_IR_technical_briefing_231129.pdf) | 인쇄 16쪽의 적층 전/후 검사 예와 전원·속도·시험 시간 과제입니다. |
| [Teradyne, 2025-08-04](https://investors.teradyne.com/news-events/press-releases/detail/419/teradyne-unveils-magnum-7h---the-next-generation-memory-tester-for-high-bandwidth-memory-devices) | 분리 전·후 HBM 검사와 코어/베이스 로직 시험 기능입니다. 특정 고객의 채택·수율은 추정하지 않았습니다. |

날짜가 없는 제품·기술 페이지는 2026-10-26에 확인했습니다. 자체 표와 계산은 공식 도면의 복제나 직접 제조·측정 결과가 아닙니다.

## English

HBM combines DRAM fabrication with TSV integration, wafer thinning, die-to-die joining and staged testing. This chapter follows a representative via-middle flow, separates temporary carriers from base dies, and distinguishes internal stack assembly from CoWoS system integration. Official figures are linked at their publishers. MR-MUF, TC-NCF and hybrid bonding are compared by their joining interfaces and process requirements; dated production reports, sample shipments and research directions remain distinct.

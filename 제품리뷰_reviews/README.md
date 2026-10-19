# 제품과 기술 리뷰 | Product and technology reviews

반도체·기기·AI·로봇·우주·운송·방산·의료 기술을 39편으로 읽습니다. 무엇을 하는 제품인지부터 원리, 가능해진 배경, 경쟁 방식, 실제 시험과 남은 제약까지 설명합니다. 각 글에 기초 용어, 직접 따라갈 계산과 확인 문제 세 개를 넣었습니다. 자료 확인일은 2026-10-20이며 개별 시험의 실시일·제품 판은 본문에 따로 표시합니다.

## 분야별 목록

| 분야 | 리뷰 수 | 대상과 질문 |
| --- | ---: | --- |
| [반도체와 산업 컴퓨팅](반도체와산업컴퓨팅_chips-industrial/README.md) | 10 | HBM, ASML, GPU, GAA·후면 전력, 칩렛, CXL, SSD, SoC, 자동화 공장, 디지털트윈 |
| [기기와 모빌리티](기기와모빌리티_devices-mobility/README.md) | 10 | 폴더블, OLED·microLED, XR, 전자종이, Wi-Fi 7, Thunderbolt·USB4, 배터리, F1, 수술 로봇, 광자계수 CT |
| [AI와 로봇](AI와로봇_ai-robotics/README.md) | 10 | ChatGPT·Claude, Gemini, 기기 내 AI, DLSS·FSR·XeSS, FSD·Waymo, Optimus, Atlas, Spot, BCI, 양자컴퓨터 |
| [우주와 운송](우주와운송_space-transport/README.md) | 4 | Falcon 9, Starship, Starlink, Roadster의 추진·열·통신·제어 |
| [방산 전자](방산전자_defense-electronics/README.md) | 2 | AESA·GaN 레이더, Iron Beam·DragonFire의 광학·전력·운용 조건 |
| [의약품과 생명공학](의약품과생명공학_biomedical/README.md) | 3 | 위고비·마운자로와 후속 약물, 카스게비의 유전자 편집, CAR-T의 세포치료 |

같은 글에서 다룬 경쟁 제품을 따로 세어 리뷰 수를 늘리지 않습니다. 공급사별 모델 카드는 [AI 모델 실험](../AI모델실험_model-lab/README.md), 여러 기술의 현황은 [기술 동향](../기술동향_technology/README.md), 연구 방법의 자세한 분석은 [논문 해설](../논문해설_papers/README.md)로 이어집니다.

## 궁금한 질문에서 시작하기

| 질문 | 먼저 읽을 글 | 다음으로 연결할 개념 |
| --- | --- | --- |
| 메모리를 쌓으면 왜 빨라지나요? | [HBM](반도체와산업컴퓨팅_chips-industrial/hbm.md) | 대역폭·용량·지연 → [CXL](반도체와산업컴퓨팅_chips-industrial/cxl-memory.md) |
| ASML의 장비는 왜 만들기 어렵나요? | [EUV 노광](반도체와산업컴퓨팅_chips-industrial/euv-lithography.md) | 광원·다층 거울·정렬·노광량·생산량 |
| 화면을 접거나 아주 밝게 만들 수 있나요? | [폴더블](기기와모빌리티_devices-mobility/foldables2026.md) | 재료·힌지·내구성 → [표시판](기기와모빌리티_devices-mobility/oled-microled2026.md) |
| AI가 다르면 답변도 왜 달라지나요? | [ChatGPT·Claude](AI와로봇_ai-robotics/chatgpt-claude.md) | 학습·도구·문맥·평가 조건 → [Gemini](AI와로봇_ai-robotics/gemini.md) |
| 생성한 FPS와 실제 반응 속도는 같나요? | [DLSS·FSR·XeSS](AI와로봇_ai-robotics/dlss-fsr-xess.md) | 렌더링·재구성·생성·입력 지연 |
| 로봇이 시연을 하면 공장에서도 일하나요? | [Optimus](AI와로봇_ai-robotics/tesla-optimus.md)·[Atlas](AI와로봇_ai-robotics/boston-dynamics-atlas.md) | 개입·복구·연속 성공 → [공장 자동화](반도체와산업컴퓨팅_chips-industrial/automated-factories.md) |
| 극한의 속도와 열을 어떻게 제어하나요? | [F1](기기와모빌리티_devices-mobility/f1_2026.md)·[Starship](우주와운송_space-transport/starship2026.md) | 에너지 회수·공력·냉각·재진입 |
| 의료기기의 높은 수치가 임상 이익인가요? | [수술 로봇](기기와모빌리티_devices-mobility/surgical-robots2026.md)·[광자계수 CT](기기와모빌리티_devices-mobility/photon-counting-ct2026.md) | 허가 범위·측정 과제·환자 결과·비교 설계 |
| 호르몬·유전자·면역세포가 어떻게 치료제가 되나요? | [위고비·마운자로](의약품과생명공학_biomedical/wegovy-mounjaro2026.md)·[카스게비](의약품과생명공학_biomedical/casgevy-crispr2026.md)·[CAR-T](의약품과생명공학_biomedical/car-t2026.md) | 발견·분자 설계·임상 분모·장기 효과·현행 허가 |

## 출처와 숫자를 읽는 방법

공식 사양·배포·허가는 제조사와 관련 기관의 원문에서 확인합니다. 실제 성능은 연구 논문, 공개 시험과 신뢰할 만한 전문 매체의 직접 측정·현장 취재도 대조합니다. 자료에 기기 제공·초청·협찬·구매 링크 수수료가 밝혀져 있으면 그 조건을 함께 적습니다. 독립 매체의 방문과 독립적인 장기 성능 감사도 다른 근거입니다.

수치에는 버전·시험 시점·장치·작업·설정·분모를 붙입니다. 최고 사양, 특정 조건의 시험 결과, 제조사 전망, 자체 계산을 서로 바꾸어 쓰지 않습니다. 예약·시제품 시연·판매·고객 인도·실제 운용도 구별합니다. 영상은 본문에서 확인한 범위를 밝히며 설명문만 읽고 장면 전체를 분석했다고 적지 않습니다.

이 39편은 공개 자료를 읽은 기술 리뷰입니다. 직접 제품을 구매·운전·측정한 실험과는 다릅니다. 공개된 비교 자료가 부족한 제품은 그 부분을 명시하며 상상한 순위를 만들지 않습니다.

## 함께 읽을 실습과 평가

| 글 | 확인할 내용 | 근거의 형태 |
| --- | --- | --- |
| [SQLite WAL](SQLite의동시접근_SQLITE.md) | 두 연결의 읽기·쓰기, 스냅샷·잠금·체크포인트 | 저장소의 실제 트랜잭션 실행과 추가 계산 |
| [모델 평가 지표](모델평가지표_MODEL_EVALUATION.md) | 정확도·오류·정밀도·재현율·확률·속도 | 자체 예제와 공개 평가 정의 |
| [도구와 환경](../도구와환경_tools/README.md) | 언어·컴파일러·시뮬레이터·계측 도구 | 공식 문서와 저장소의 실행 예제 |

## English

Thirty-nine Korean reviews explain semiconductors, devices, AI, robotics, space transport, defense electronics and biomedical technologies. Each pairs principles and terminology with product evidence, comparison conditions, worked calculations and three questions. Manufacturer documentation is cross-checked against research, original measurements and field reporting where available. Announced targets, demonstrations, reservations and actual operation are distinguished. Medical articles distinguish discovery, clinical evidence and current regional approvals. These are literature reviews; the SQLite article separately records a local executable experiment.

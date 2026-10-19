# 연구 및 학술 활동

[처음으로](../README.md) · [분야별 목차](../CATALOG.md) · [GitHub 프로필](https://github.com/yoonip)

AI 모델의 연산·메모리 에너지 분석과 저전력 회로 설계를 연구했다. 수치 모델과 회로·RTL 시뮬레이션을 연계하고, FPGA와 계측 장비를 이용한 하드웨어 제어 환경을 구축했다.

## 주요 연구와 프로젝트

### 저전력 인공신경망 연산

석사 연구에서는 엣지 디바이스용 인공신경망의 연산 전력을 줄이기 위한 하드웨어·소프트웨어 공동 설계를 다뤘다. INT6/INT8 MAC의 하위 부분곱을 선택적으로 비활성화하는 Bit-Drop 회로와 PyTorch 양자화 모델을 연계했다. Cadence Virtuoso/Spectre의 45nm 회로 시뮬레이션과 CIFAR-10의 ResNet-18 평가를 통해 전력과 분류 정확도의 관계를 분석했다.

석사학위논문: 엣지 디바이스를 위한 인공 신경망의 저전력 연산 기법 / Low-power computing techniques of artificial neural networks for edge devices, 국민대학교, 2025.

### 65nm 8KB SRAM

산학협력 프로젝트에서 8KB SRAM의 회로와 레이아웃, 측정용 TEG를 설계했다. DVS와 Reverse Body Bias를 적용해 누설 전류를 분석하고, PVT 코너 검증과 Calibre DRC/LVS·PEX를 수행했다. 누설 전류와 쓰기 지연은 조건별 시뮬레이션 결과로 비교했다.

### AI 에너지 모델링과 DRAM-PIM

ResNet-18과 GPT·Llama 계열의 모델 구조를 대상으로 가중치 메모리 접근과 MAC 연산의 에너지를 수치 모델로 분석했다. 배치 크기와 에너지 스케일링에 따른 병목 변화를 비교했다. DRAM-PIM 연산 블록은 SystemVerilog로 구현하고 Cadence Xcelium에서 기능과 사이클 동작을 검증했다.

한국연구재단 석사과정생연구장려금 과제에서는 트랜스포머 DRAM-PIM을 주제로 2024–2025년 연구를 수행했다. 과제 제안부터 구현·검증과 결과 정리까지 1인 과제로 진행했다.

### FPGA 기반 혼성신호 계측 자동화

Opal Kelly XEM8320과 SYZYGY 인터페이스를 이용해 디지털 패턴을 전송하고 ADC/DAC 응답을 수집하는 환경을 구축했다. Verilog의 제어 로직·FIFO와 FrontPanel API 기반 C++·Python 호스트 소프트웨어를 연계했다. 계측 데이터 수집과 시각화를 자동화하고, 오실로스코프와 로직 아날라이저로 인터페이스 동작을 확인했다.

### 태양에너지 하베스팅 시스템

태양광의 세기에 따라 Active와 Sleep 시간 비율을 조절하는 자가발전 Arduino 시스템을 설계했다. 회로·PCB와 C/C++ 펌웨어를 구현하고, ADC로 에너지원의 상태를 읽어 동작 모드를 제어했다. 관련 연구는 2022년 전기전자학회논문지에 게재됐다.

### T5 기반 점자 역번역

점자를 한글 문장으로 변환하는 역점역 모델을 개발했다. 팀장으로 데이터 처리와 학습 환경 구성을 맡았으며, 6비트 점자를 정수 토큰으로 표현하고 PyTorch·Hugging Face·T5를 사용했다. 학습 자원에 맞춰 말뭉치를 선별해 데이터 파이프라인을 구성했다. 이 프로젝트로 2022년 캡스톤디자인 경진대회 시제품 부문 대상을 수상했다.

## 참여 연구 주제

| 구분 | 연구 주제 | 담당 내용 |
| --- | --- | --- |
| 국가사업 참여 | BEOL 저항변화 시냅스 어레이 기반 인공신경망 | 회로 설계, AI 학습·추론, FPGA 테스트 환경 구축 |
| 국가사업 참여 | 3D FeRAM의 집적 기술 및 회로·아키텍처 | 회로 설계 및 AI 학습·추론 |
| 국가사업 참여 | 멤리스터-IGZO DRAM 혼합소자 기반 로컬학습 | 회로 설계 및 AI 학습·추론 |
| 국가사업 참여 | RRAM 기반 혼성신호 뉴로모픽 구조와 로컬학습 회로 | 회로 설계 및 AI 학습·추론 |
| 석사과정생연구장려금 | 트랜스포머 DRAM-PIM | 과제 제안, 모델링, RTL 구현·검증, 결과 정리 |
| 산학협력 | Ultra Low Leakage SRAM | 회로·레이아웃, PVT 분석, DRC/LVS·PEX |

## 논문 및 기술 글

### 2025 · AI 모델의 에너지 분석

Ilpyung Yoon, Jihwan Mun, Kyeong-Sik Min. “Comparative Study on Energy Consumption of Neural Networks by Scaling of Weight-Memory Energy Versus Computing Energy for Implementing Low-Power Edge Intelligence.” Electronics, 14(13), 2718, 2025. 제1저자.

[출판 정보](https://doi.org/10.3390/electronics14132718)

CNN과 트랜스포머의 가중치 메모리 접근·MAC 연산 에너지를 비교했다. 모델 구조, 배치 크기, 에너지 스케일링에 따라 어느 부분의 효율 개선이 중요한지 분석했다.

### 2024 · 멤리스터 크로스바 매핑 최적화

Seung-Myeong Cho, Rina Yoon, Ilpyeong Yoon, Jihwan Moon, Seokjin Oh, Kyeong-Sik Min. “Optimization of Memristor Crossbar’s Mapping Using Lagrange Multiplier Method and Genetic Algorithm for Reducing Crossbar’s Area and Delay Time.” Information, 15(7), 409, 2024. 공동저자.

[출판 정보](https://doi.org/10.3390/info15070409)

라그랑주 승수법과 유전 알고리즘을 이용해 CNN의 크로스바 자원 배분을 최적화했다. 면적 제약과 지연 제약을 각각 적용하고, 제약 없는 조건에서는 면적·지연 곱을 목적함수로 다뤘다.

### 2024 · Unconventional 컴퓨팅 하드웨어 기술

윤일평, 조승명, 윤리나, 문지환, 민경식. “Unconventional 컴퓨팅 하드웨어 기술.” 전자공학회지, 51(3), 2024년 3월. 제1저자, 특집 글.

[대한전자공학회 목차](https://paper.cricit.kr/user/listview/ieie2018/gby_cmag.asp?dbcode=&organCode=ieie&organCode2=ieie04&seid=&step=4&usernum=0&yearmonth=202403)

### 2022 · 자가발전 Arduino 시스템

윤일평, 조승명, 안지용, 오석진, 민경식. “태양에너지 하베스팅을 위한 자가발전아두이노 시스템의 설계 및 동작.” 전기전자학회논문지, 26(3), 483–487, 2022. 제1저자.

[출판 정보](https://doi.org/10.7471/ikeee.2022.26.3.483) · [KCI](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002883800)

태양광의 변화에 맞춰 Active/Sleep 동작 비율을 조절하는 시스템을 설계하고 동작을 검증했다.

## 학회 발표와 수상

| 연도 | 수상 | 기관·주제 |
| --- | --- | --- |
| 2025 | 우수인재상 | 국민대학교 |
| 2024 | 우수논문상 | 한국전기전자학회 · 이벤트 처리를 위한 신경망 멤리스터 회로 |
| 2023 | 우수논문상 | 한국전기전자학회 · 로컬학습 구현을 위한 멤리스터 크로스바 학습 방법 |
| 2022 | 캡스톤디자인 경진대회 시제품 부문 대상 | 국민대학교 · T5 기반 점자 역번역 |
| 2022 | 캡스톤디자인 경진대회 지식재산 부문 은상 | 국민대학교 · 온도·압력에 따라 개폐하는 스마트 냄비 뚜껑 |
| 2022 | 지식재산캠프 금상 | 국민대학교 |

## 연구 환경과 기술

| 분야 | 사용 기술 |
| --- | --- |
| 회로·물리 검증 | Cadence Virtuoso·Spectre, Calibre DRC/LVS·PEX, PVT 분석 |
| RTL·FPGA | Verilog, SystemVerilog, Verilog-A, Xcelium, Vivado, Opal Kelly FrontPanel |
| 소프트웨어·AI | Python, C/C++, MATLAB, PyTorch, Hugging Face |
| 시스템 | CentOS·Ubuntu, Bash, GPU 서버, CUDA·cuDNN 환경 구성 |
| 계측 | Keithley 4200A-SCS, HP 4155B, 프로브 스테이션, 오실로스코프, 로직 아날라이저 |

IDEC·국민대학교 설계 실습에서는 Verilog/VHDL, FPGA와 Full-custom 설계, DRC/LVS 및 Linux 환경 관련 실습을 지원했다.

## 연락

연구·개발 협업, 기술 교류 및 채용 제안: [dlfvud777@naver.com](mailto:dlfvud777@naver.com)

## Overview

Research on low-power AI hardware, memory circuits, neural-network energy modeling, and FPGA-based measurement automation. Work spans circuit design and physical verification, SystemVerilog implementation, hardware control, and software tools for analysis and validation.

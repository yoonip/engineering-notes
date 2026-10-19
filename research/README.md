# 연구 및 학술 활동

[처음으로](../README.md) · [분야별 목차](../CATALOG.md) · [GitHub 프로필](https://github.com/yoonip)

저전력 AI 연산, 메모리 회로, 신경망 에너지 모델링과 FPGA 계측 자동화 연구에 참여했다.

## 주요 연구와 프로젝트

### 저전력 인공신경망 연산

엣지 디바이스에서 인공신경망의 연산 전력을 줄이는 연구다. INT6/INT8 MAC의 일부 연산을 생략하는 Bit-Drop 회로와 모델 양자화를 연계해 전력과 분류 정확도의 관계를 분석한다. 회로 시뮬레이션과 신경망 평가를 함께 다루는 하드웨어·소프트웨어 공동 설계가 중심이다.

석사학위논문: 엣지 디바이스를 위한 인공 신경망의 저전력 연산 기법 / Low-power computing techniques of artificial neural networks for edge devices, 국민대학교, 2025.

### 65nm 8KB SRAM

대기 모드의 누설 전류를 줄이기 위한 65nm 8KB SRAM 산학협력 연구다. 전압·바이어스 조절과 회로·물리 구조를 검토하고, 조건별 시뮬레이션을 통해 누설 전류와 동작 특성의 관계를 살핀다.

### AI 에너지 모델링과 DRAM-PIM

CNN과 트랜스포머의 가중치 메모리 접근·연산 에너지를 분석하고, 메모리 내부 연산 구조를 검토하는 연구다. 모델 구조와 배치 크기에 따른 에너지 병목을 비교하고, DRAM-PIM의 동작을 RTL로 표현해 확인한다.

트랜스포머 DRAM-PIM 연구는 2024–2025년 한국연구재단 석사과정생연구장려금 과제로 진행됐다.

### FPGA 기반 혼성신호 계측 자동화

FPGA로 디지털 패턴을 전송하고 ADC/DAC 응답을 수집하는 혼성신호 계측 환경에 관한 프로젝트다. 하드웨어 제어와 측정 데이터의 수집·시각화를 연결해 반복 계측을 자동화하는 것이 목적이다.

### 태양에너지 하베스팅 시스템

태양광의 세기에 따라 Active와 Sleep 시간 비율을 조절하는 자가발전 Arduino 시스템이다. 에너지원의 상태를 읽어 동작 모드를 조절함으로써 수집 가능한 에너지에 맞춰 시스템이 작동하도록 한다.

### T5 기반 점자 역번역

점자를 문맥에 맞는 한글 문장으로 변환하는 T5 기반 역점역 프로젝트다. 6비트 점자의 구조와 문장 데이터를 활용해 점자·한글의 대응 관계를 학습한다.

## 참여 연구 주제

| 구분 | 주제 |
| --- | --- |
| 국가사업 | BEOL 저항변화 시냅스 어레이 기반 인공신경망 |
| 국가사업 | 3D FeRAM의 집적 기술 및 회로·아키텍처 |
| 국가사업 | 멤리스터-IGZO DRAM 혼합소자 기반 로컬학습 |
| 국가사업 | RRAM 기반 혼성신호 뉴로모픽 구조와 로컬학습 회로 |
| 석사과정생연구장려금 | 트랜스포머 DRAM-PIM |
| 산학협력 | Ultra Low Leakage SRAM |

## 논문 및 기술 글

### 2025 · AI 모델의 에너지 분석

“Comparative Study on Energy Consumption of Neural Networks by Scaling of Weight-Memory Energy Versus Computing Energy for Implementing Low-Power Edge Intelligence.” Electronics, 14(13), 2718, 2025.

[출판 정보](https://doi.org/10.3390/electronics14132718)

CNN과 트랜스포머의 가중치 메모리 접근·MAC 연산 에너지를 비교한 연구다. 모델 구조, 배치 크기와 에너지 스케일링에 따른 병목 변화를 다룬다.

### 2024 · 멤리스터 크로스바 매핑 최적화

“Optimization of Memristor Crossbar’s Mapping Using Lagrange Multiplier Method and Genetic Algorithm for Reducing Crossbar’s Area and Delay Time.” Information, 15(7), 409, 2024.

[출판 정보](https://doi.org/10.3390/info15070409)

라그랑주 승수법과 유전 알고리즘을 이용한 CNN 크로스바 자원 배분 연구다. 면적·지연 제약에 따른 최적화와 면적·지연 곱의 최소화를 다룬다.

### 2024 · Unconventional 컴퓨팅 하드웨어 기술

“Unconventional 컴퓨팅 하드웨어 기술.” 전자공학회지, 51(3), 2024년 3월. 특집 글.

[대한전자공학회 목차](https://paper.cricit.kr/user/listview/ieie2018/gby_cmag.asp?dbcode=&organCode=ieie&organCode2=ieie04&seid=&step=4&usernum=0&yearmonth=202403)

### 2022 · 자가발전 Arduino 시스템

“태양에너지 하베스팅을 위한 자가발전아두이노 시스템의 설계 및 동작.” 전기전자학회논문지, 26(3), 483–487, 2022.

[출판 정보](https://doi.org/10.7471/ikeee.2022.26.3.483) · [KCI](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002883800)

태양광의 변화에 맞춰 Active/Sleep 동작 비율을 조절하는 시스템의 설계와 동작을 다룬다.

## 수상

| 연도 | 수여기관 | 상명 |
| --- | --- | --- |
| 2025 | 국민대학교 | 우수인재상 |
| 2024 | 한국전기전자학회 | 학술지 우수논문상 |
| 2023 | 한국전기전자학회 | 학술지 우수논문상 |
| 2022 | 국민대학교 공학교육혁신센터 | KMU 캡스톤디자인 경진대회 시제품(융합) 부문 대상 |
| 2022 | 국민대학교 공학교육혁신센터 | 지식재산캠프 금상 |
| 2022 | 국민대학교 | 캡스톤디자인 경진대회 지식재산 부문 은상 |

## 기술 분야

반도체 회로와 디지털 하드웨어 설계, 펌웨어, 실리콘 검증, 계측 자동화와 AI 모델 분석을 다룬다.

| 분야 | 기술·도구 |
| --- | --- |
| 반도체·메모리 회로 | CMOS, SRAM, DRAM-PIM, AI 가속기, MAC·Adder Tree |
| SRAM 아키텍처 | Bank·Sub-block·Bitcell Array, WL Driver, Decoder, MUX, Sense Amplifier |
| 회로 설계·시뮬레이션 | Cadence Virtuoso·Spectre, Verilog-A, PVT 분석, SNM, DVS·RBB |
| 레이아웃·물리 검증 | Full-Chip Layout·Tape-out, TEG Layout, Calibre DRC/LVS·PEX, Assura |
| 공정·설계 환경 | 45nm·65nm PDK, EDA·Ruledeck 환경 |
| RTL 설계·검증 | Verilog, SystemVerilog, FIFO·Clock Domain, 사이클 단위 기능 검증, Xcelium, QuestaSim |
| 혼성신호 모델링 | XMODEL, Glister, Modelzen |
| FPGA·Bring-up | Vivado, Opal Kelly XEM8320, Nexys 4 DDR, SYZYGY, FrontPanel API |
| 하드웨어·펌웨어 | Raspberry Pi, Arduino, MCU, 임베디드 펌웨어, Linux 드라이버, 전원 회로·PCB, SPI·GPIO, ADC/DAC |
| Post-Silicon 검증 | Silicon Bring-up, 소자 특성·파라미터 분석, DC·펄스 계측, Probe-card Testing |
| 계측·테스트 자동화 | 테스트 벡터·시퀀스, Telemetry·Logging, 데이터 수집·시각화, Tkinter·Matplotlib |
| 시스템 디버깅 | JTAG·OpenOCD, 신호 무결성·버스 타이밍 분석 |

## 언어와 개발 환경

| 분야 | 언어·도구 |
| --- | --- |
| 시스템·임베디드 프로그래밍 | C, C++ |
| 분석·자동화·수치해석 | Python, MATLAB, Bash |
| AI·모델 분석 | PyTorch, TensorFlow, Hugging Face, CNN·LLM·T5, 모델 양자화, 메모리·MAC·KV Cache 에너지 모델링, Memory-bound·Compute-bound 분석 |
| 개발·GPU 환경 | Linux(CentOS·Ubuntu), GPU 서버, Jupyter Notebook, CUDA·cuDNN, Docker, Git |

## 계측 장비

| 구분 | 장비 |
| --- | --- |
| 반도체·소자 계측 | Keithley 4200A-SCS(SMU·고속 PMU), HP 4155B |
| 프로빙·온도 제어 | 진공 프로브 스테이션, 프로브 카드, Hot Chuck |
| 파형 관측 | 디지털 오실로스코프 |
| 디지털 신호 분석 | 로직 아날라이저 |

## 영어

TOEIC Speaking IH (Intermediate High)

| 구분 | 활용 |
| --- | --- |
| 읽기 | 영문 논문·기술 문서와 시사 기사 독해 |
| 쓰기 | 연구 내용과 기술 경험을 영어 문서로 정리 |
| 말하기 | 일상 및 업무 관련 주제에 대한 영어 의사소통 |

## 연락

연구·개발 협업, 기술 교류 및 채용 제안: [dlfvud777@naver.com](mailto:dlfvud777@naver.com)

## Overview

Research on low-power AI hardware, memory circuits, neural-network energy modeling, and FPGA-based measurement automation. Work spans circuit design and physical verification, SystemVerilog implementation, hardware control, and software tools for analysis and validation.

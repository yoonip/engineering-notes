# 윤일평 | Yoon IlPyung

[한국어](#윤일평--yoon-ilpyung) · [English](#english)

저전력 AI 하드웨어와 메모리·연산 구조 연구에 참여해 온 윤일평입니다. 국민대학교 지능형반도체 및 디스플레이 전공으로 석사 학위를 취득했으며, ISL에서 연구했습니다.

주요 참여 연구는 저전력 AI 연산, SRAM, DRAM-PIM과 FPGA 계측 자동화입니다. AI 모델의 에너지 효율, 메모리 구조와 회로·시스템의 동작을 다룹니다.

[연구·프로젝트·학술 활동](https://github.com/yoonip/engineering-notes/blob/main/research/README.md) · [engineering-notes](https://github.com/yoonip/engineering-notes) · [분야별 목차](https://github.com/yoonip/engineering-notes/blob/main/CATALOG.md)

## 참여 연구

| 주제 | 프로젝트 개요 |
| --- | --- |
| 저전력 AI 연산 | Bit-Drop과 모델 양자화에 따른 전력·정확도 관계 |
| SRAM | 65nm 8KB SRAM, 누설 저감, PVT 분석과 물리 검증 |
| DRAM-PIM | AI 워크로드의 에너지 병목과 메모리 내부 연산 구조 |
| FPGA·계측 자동화 | FPGA와 ADC/DAC를 연결한 혼성신호 제어 및 데이터 수집 |
| 임베디드·AI 응용 | 태양에너지 하베스팅 시스템, T5 기반 점자 역번역 모델 |

## 한국연구재단 연구과제

| 항목 | 내용 |
| --- | --- |
| 연구과제명 | 트랜스포머 DRAM-PiM 연구 |
| 사업명 | 2024년도 석사과정생연구장려금지원사업 |
| 지원기관 | 한국연구재단 |
| 과제번호 | RS-2024-00395426 |
| 총연구기간 | 2024.07.01. ~ 2025.06.30. |
| 소속기관 | 국민대학교 |

## 기술 분야

반도체 회로와 디지털 하드웨어 설계, 펌웨어, 실리콘 검증, 계측 자동화와 AI 모델 분석을 다룹니다.

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
| MCU·임베디드 플랫폼 | STM32, ESP32, Arm Cortex-M, Raspberry Pi, Arduino, STM32CubeIDE, PlatformIO |
| 하드웨어·펌웨어 | MCU, 임베디드 펌웨어, Linux 드라이버, 전원 회로·PCB, UART·SPI·GPIO, ADC/DAC, 부팅·메모리 맵·인터럽트·DMA·FreeRTOS |
| Post-Silicon 검증 | Silicon Bring-up, 소자 특성·파라미터 분석, DC·펄스 계측, Probe-card Testing |
| 계측·테스트 자동화 | 테스트 벡터·시퀀스, Telemetry·Logging, 데이터 수집·시각화, Tkinter·Matplotlib |
| 시스템 디버깅 | JTAG·SWD, ST-Link, OpenOCD, GDB, 신호 무결성·버스 타이밍 분석 |
| 아키텍처·가상 실습 | Arm·RISC-V, Renode, Spike, 명령 단위 실행·메모리 회귀검사·오류 주입 |

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

## 논문 및 기술 글

- 2025 · AI 모델의 메모리·연산 에너지 비교 연구 — Electronics. [DOI](https://doi.org/10.3390/electronics14132718)
- 2024 · 멤리스터 크로스바 매핑 최적화 — Information. [DOI](https://doi.org/10.3390/info15070409)
- 2024 · Unconventional 컴퓨팅 하드웨어 기술 — 전자공학회지 특집 글. [학회 목차](https://paper.cricit.kr/user/listview/ieie2018/gby_cmag.asp?dbcode=&organCode=ieie&organCode2=ieie04&seid=&step=4&usernum=0&yearmonth=202403)
- 2022 · 태양에너지 하베스팅을 위한 자가발전아두이노 시스템의 설계 및 동작 — 전기전자학회논문지. [DOI](https://doi.org/10.7471/ikeee.2022.26.3.483)

## 수상

| 연도 | 수여기관 | 상명 |
| --- | --- | --- |
| 2025 | 국민대학교 | 우수인재상 |
| 2024 | 한국전기전자학회 | 학술지 우수논문상 |
| 2023 | 한국전기전자학회 | 학술지 우수논문상 |
| 2022 | 국민대학교 공학교육혁신센터 | KMU 캡스톤디자인 경진대회 시제품(융합) 부문 대상 |
| 2022 | 국민대학교 공학교육혁신센터 | 지식재산캠프 금상 |
| 2022 | 국민대학교 | 캡스톤디자인 경진대회 지식재산 부문 은상 |

## 학력 및 연구실

- 국민대학교 지능형반도체 및 디스플레이 석사
- 국민대학교 전자공학부 학사
- ISL

## 연구자 정보

| 항목 | 내용 |
| --- | --- |
| 이름 | 윤일평 |
| 국가연구자번호(IRIS) | 12944496 |

## 영어

TOEIC Speaking IH (Intermediate High)

| 구분 | 활용 |
| --- | --- |
| 읽기 | 영문 논문·기술 문서와 시사 기사 독해 |
| 쓰기 | 연구 내용과 기술 경험을 영어 문서로 정리 |
| 말하기 | 일상 및 업무 관련 주제에 대한 영어 의사소통 |

## 기록과 연락

[engineering-notes](https://github.com/yoonip/engineering-notes)에 전자·컴퓨터공학과 AI의 개념, 구현 방법, 코드 분석을 정리합니다. [AI 기업과 모델](https://github.com/yoonip/engineering-notes/blob/main/model-lab/PROVIDERS.md), [알고리즘과 코딩테스트](https://github.com/yoonip/engineering-notes/tree/main/topics/08-problem-solving), [지원·시험·면접](https://github.com/yoonip/engineering-notes/tree/main/topics/55-applications-assessments) 기록을 함께 다룹니다.

연구·개발 협업, 기술 교류 및 채용 제안: [dlfvud777@naver.com](mailto:dlfvud777@naver.com)

## English

I am Yoon IlPyung. My research experience spans low-power AI hardware, memory, and computing architectures. I hold a master's degree in Intelligent Semiconductors and Displays from Kookmin University and conducted research at ISL.

The research I have participated in covers low-power AI computation, SRAM, DRAM-PIM, and FPGA-based measurement automation. These projects address the energy efficiency of AI models, memory architectures, and circuit and system operation.

[Research, Projects, and Publications](https://github.com/yoonip/engineering-notes/blob/main/research/README.md) · [engineering-notes](https://github.com/yoonip/engineering-notes) · [Topic Index](https://github.com/yoonip/engineering-notes/blob/main/CATALOG.md)

### Research Participation

| Topic | Project Overview |
| --- | --- |
| Low-power AI computation | Power and accuracy trade-offs associated with Bit-Drop and model quantization |
| SRAM | 65nm 8KB SRAM, leakage reduction, PVT analysis, and physical verification |
| DRAM-PIM | Energy bottlenecks in AI workloads and processing-in-memory architectures |
| FPGA and measurement automation | Mixed-signal control and data acquisition through FPGA connections to ADCs and DACs |
| Embedded and AI applications | Solar energy harvesting systems and T5-based Braille back-translation models |

### National Research Foundation of Korea Project

| Field | Details |
| --- | --- |
| Project title | Transformer DRAM-PiM Research |
| Program | 2024 Research Grant Program for Master's Students |
| Funding organization | National Research Foundation of Korea |
| Project number | RS-2024-00395426 |
| Total research period | July 1, 2024 – June 30, 2025 |
| Affiliated institution | Kookmin University |

### Technical Areas

My technical work spans semiconductor circuits, digital hardware design, firmware, silicon validation, measurement automation, and AI model analysis.

| Area | Technologies and Tools |
| --- | --- |
| Semiconductor and memory circuits | CMOS, SRAM, DRAM-PIM, AI accelerators, MAC, Adder Tree |
| SRAM architecture | Bank, Sub-block, Bitcell Array, WL Driver, Decoder, MUX, Sense Amplifier |
| Circuit design and simulation | Cadence Virtuoso, Spectre, Verilog-A, PVT analysis, SNM, DVS, RBB |
| Layout and physical verification | Full-Chip Layout, Tape-out, TEG Layout, Calibre DRC/LVS, PEX, Assura |
| Process and design environments | 45nm and 65nm PDKs, EDA and Ruledeck environments |
| RTL design and verification | Verilog, SystemVerilog, FIFO, clock domains, cycle-level functional verification, Xcelium, QuestaSim |
| Mixed-signal modeling | XMODEL, Glister, Modelzen |
| FPGA and bring-up | Vivado, Opal Kelly XEM8320, Nexys 4 DDR, SYZYGY, FrontPanel API |
| MCU and embedded platforms | STM32, ESP32, Arm Cortex-M, Raspberry Pi, Arduino, STM32CubeIDE, PlatformIO |
| Hardware and firmware | MCU, embedded firmware, Linux drivers, power circuits, PCB, UART, SPI, GPIO, ADC/DAC, boot process, memory maps, interrupts, DMA, FreeRTOS |
| Post-silicon validation | Silicon Bring-up, device characterization and parameter analysis, DC and pulse measurements, Probe-card Testing |
| Measurement and test automation | Test vectors and sequences, Telemetry, Logging, data acquisition and visualization, Tkinter, Matplotlib |
| System debugging | JTAG, SWD, ST-Link, OpenOCD, GDB, signal integrity and bus timing analysis |
| Architecture and virtual labs | Arm, RISC-V, Renode, Spike, instruction-level execution, memory regression testing, fault injection |

### Programming Languages and Development Environments

| Area | Languages and Tools |
| --- | --- |
| Systems and embedded programming | C, C++ |
| Analysis, automation, and numerical computing | Python, MATLAB, Bash |
| AI and model analysis | PyTorch, TensorFlow, Hugging Face, CNN, LLM, T5, model quantization, energy modeling for memory, MAC, and KV Cache, memory-bound and compute-bound analysis |
| Development and GPU environments | Linux (CentOS, Ubuntu), GPU servers, Jupyter Notebook, CUDA, cuDNN, Docker, Git |

### Measurement Equipment

| Category | Equipment |
| --- | --- |
| Semiconductor and device measurements | Keithley 4200A-SCS (SMU, high-speed PMU), HP 4155B |
| Probing and temperature control | Vacuum probe station, probe card, Hot Chuck |
| Waveform observation | Digital oscilloscope |
| Digital signal analysis | Logic analyzer |

### Publications and Technical Articles

- 2025 · Comparative study of memory and computation energy in AI models — Electronics. [DOI](https://doi.org/10.3390/electronics14132718)
- 2024 · Memristor crossbar mapping optimization — Information. [DOI](https://doi.org/10.3390/info15070409)
- 2024 · Unconventional Computing Hardware Technologies — Special feature article in The Magazine of the IEIE. [Magazine contents](https://paper.cricit.kr/user/listview/ieie2018/gby_cmag.asp?dbcode=&organCode=ieie&organCode2=ieie04&seid=&step=4&usernum=0&yearmonth=202403)
- 2022 · Design and operation of a self-powered Arduino system for solar energy harvesting — Journal of IKEEE. [DOI](https://doi.org/10.7471/ikeee.2022.26.3.483)

### Awards

| Year | Awarding Institution | Award |
| --- | --- | --- |
| 2025 | Kookmin University | Outstanding Talent Award |
| 2024 | Institute of Korean Electrical and Electronics Engineers | Outstanding Journal Paper Award |
| 2023 | Institute of Korean Electrical and Electronics Engineers | Outstanding Journal Paper Award |
| 2022 | Center for Engineering Education Innovation, Kookmin University | Grand Prize, Prototype (Convergence) Category, KMU Capstone Design Competition |
| 2022 | Center for Engineering Education Innovation, Kookmin University | Gold Prize, Intellectual Property Camp |
| 2022 | Kookmin University | Silver Prize, Intellectual Property Category, Capstone Design Competition |

### Education and Research Lab

- Master's degree in Intelligent Semiconductors and Displays, Kookmin University
- Bachelor's degree in Electronic Engineering, Kookmin University
- ISL

### Researcher Information

| Field | Details |
| --- | --- |
| Name | Yoon IlPyung |
| National Researcher Number (IRIS, Korea) | 12944496 |

### English Proficiency

TOEIC Speaking IH (Intermediate High)

| Skill | Use |
| --- | --- |
| Reading | Reading English-language research papers, technical documentation, and current affairs articles |
| Writing | Documenting research and technical experience in English |
| Speaking | Communicating in English about everyday and work-related topics |

### Notes and Contact

In [engineering-notes](https://github.com/yoonip/engineering-notes), I document concepts, implementation methods, and code analysis across electronics, computer engineering, and AI. The repository also covers [AI companies and models](https://github.com/yoonip/engineering-notes/blob/main/model-lab/PROVIDERS.md), [algorithms and coding tests](https://github.com/yoonip/engineering-notes/tree/main/topics/08-problem-solving), and [applications, assessments, and interviews](https://github.com/yoonip/engineering-notes/tree/main/topics/55-applications-assessments).

For research and development collaboration, technical exchange, and career opportunities: [dlfvud777@naver.com](mailto:dlfvud777@naver.com)

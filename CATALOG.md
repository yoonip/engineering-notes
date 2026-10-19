# 분야별 목차

회로와 소자에서 시스템·소프트웨어·AI로 이어지는 개념을 정리했다. 각 문서에서 기본 원리와 활용처를 설명하고, 관련 도구와 참고 자료를 함께 정리했다.

## 개발 환경과 기초

- [Linux & Bash](topics/01-linux-bash/README.md) — 터미널, 셸, Bash · 파일과 권한 · 프로세스와 개발 환경
- [Git & Development Tools](topics/02-git-development-tools/README.md) — 작업에서 공유까지 · 편집, 빌드, 실행 환경
- [Python & Jupyter](topics/03-python-jupyter/README.md) — 환경을 나누는 이유 · 계산과 시각화
- [C, C++ & Python](topics/04-c-cpp-python/README.md) — C: 데이터와 메모리 · C++: 자원 수명과 추상화 · Python과 다른 언어의 연결
- [MATLAB & Scientific Computing](topics/05-matlab-scientific/README.md) — 행렬 연산과 원소별 연산 · 수치 해석과 모델링
- [수식을 코드로](topics/06-math-to-code/README.md) — 미분방정식에서 반복문으로 · 수치적으로 같은 식인가
- [컴퓨터공학 기초](topics/07-cs-foundations/README.md) — 자료구조와 실행 비용 · 운영체제와 동시성 · 저장, 통신, 빌드
- [알고리즘과 코딩테스트](topics/08-problem-solving/README.md) — 알고리즘을 선택하는 기준 · 입력 크기와 자료구조 · 이진 탐색의 경계

## 회로·반도체·하드웨어

- [회로와 전자공학](topics/09-circuits-electronics/README.md) — RLC와 시간·주파수 응답 · 능동 소자와 증폭
- [반도체 소자](topics/10-semiconductors/README.md) — MOSFET에서 CMOS로 · 구조와 재료 · 소자 모델과 공정 변동
- [Analog IC · Cadence · Spectre](topics/11-analog-ic-cadence/README.md) — 도구의 역할 · 해석이 알려주는 것 · 회로도에서 레이아웃으로
- [PCB & Hardware Design](topics/12-pcb-hardware/README.md) — 부품과 제조 데이터 · 신호와 전원의 경로
- [Verilog · SystemVerilog · RTL](topics/13-verilog-systemverilog/README.md) — 조합논리와 순차논리 · FSM·파이프라인·메모리
- [Hardware Verification](topics/14-hardware-verification/README.md) — 시뮬레이션과 coverage · Assertion과 formal
- [FPGA & ASIC](topics/15-fpga-asic/README.md) — 구현 흐름 · 타이밍과 PPA

## 프로세서·임베디드·제어

- [Arm · RISC-V · Computer Architecture](topics/16-arm-riscv/README.md) — Arm과 RISC-V · 명령 실행과 메모리
- [Firmware & RTOS](topics/17-firmware-rtos/README.md) — 리셋에서 main까지 · 주변장치와 시간 · RTOS의 동시성
- [Embedded Linux](topics/18-embedded-linux/README.md) — 부팅의 구성요소 · 빌드와 이식
- [OpenOCD · GDB · Debugging](topics/19-openocd-debugging/README.md) — 연결 구조 · 관찰 도구의 차이
- [Interfaces & Communications](topics/20-interfaces-communications/README.md) — 보드와 장치 사이 · 네트워크와 온칩 연결
- [신호처리와 제어](topics/21-signals-control/README.md) — 샘플링과 변환 · 필터와 피드백
- [Robotics · Arduino · Raspberry Pi](topics/22-robotics-boards/README.md) — 보드의 역할 · 운동과 관측 · 소프트웨어와 시뮬레이션

## AI·GPU·연구 기록

- [AI · Machine Learning · Deep Learning](topics/23-ai-machine-learning/README.md) — 학습과 평가 · 모델 구조 · 자동미분 예제
- [GPU Architecture](topics/24-gpu-architecture/README.md) — 실행과 메모리 · 처리량과 병목 읽기
- [CUDA & GPU Optimization](topics/25-cuda-performance/README.md) — 실행 단위와 데이터 이동 · 라이브러리와 직접 작성한 kernel
- [AI Models & APIs](topics/26-open-model-lab/README.md) — 모델을 구성하는 파일 · 수정과 비교
- [논문 · 코드 · 특허](topics/27-papers-code-patents/README.md) — 논문과 코드의 연결 · 특허와 문헌 관리
- [자동화와 기술 기록](topics/28-automation-portfolio/README.md) — 스크립트와 CI · 문서 생성 도구

## 전자 시스템과 설계 확장

- [전자기학 · RF · 안테나](topics/29-electromagnetics-rf/README.md) — 반사와 정합 · RF 회로와 안테나
- [통신이론과 무선 시스템](topics/30-communications-wireless/README.md) — 변조, 부호화, 채널 · 다중 반송파와 다중 안테나
- [전력전자와 에너지](topics/31-power-energy/README.md) — 변환기와 스위칭 · 소자와 구동
- [Mixed-Signal · ADC · DAC · Clock](topics/32-mixed-signal-data-converters/README.md) — 샘플링과 양자화 · 정적·동적 지표와 클록
- [Memory & Storage](topics/33-memory-storage/README.md) — 소자와 인터페이스 · SSD와 신뢰성
- [SoC & Interconnects](topics/34-soc-interconnects/README.md) — 버스와 네트워크 · 주소와 데이터 일관성
- [EDA & Open Hardware](topics/35-eda-open-hardware/README.md) — 흐름을 잇는 데이터 · PDK와 도구
- [Packaging · Chiplets · Thermal](topics/36-packaging-thermal/README.md) — 연결 구조 · 전원과 열
- [센서와 계측](topics/37-sensors-instrumentation/README.md) — 신호 경로와 오차 · 장비와 자동 측정

## 시스템·데이터·병렬 처리

- [Security · Cryptography · Hardware Trust](topics/38-security-cryptography/README.md) — 암호의 역할 · 부팅과 실행의 신뢰
- [Compilers · Languages · Runtimes](topics/39-compilers-languages/README.md) — AST에서 machine code로 · 도구와 실행 방식
- [Databases & Data Engineering](topics/40-databases-data-engineering/README.md) — SQL과 실행 계획 · 파이프라인과 검색
- [Cloud & Distributed Systems](topics/41-cloud-distributed/README.md) — 실패와 일관성 · 배포와 운영
- [HPC & Parallel Computing](topics/42-hpc-parallel/README.md) — 공유 메모리와 분산 메모리 · GPU와 분산 작업

## AI 응용과 소프트웨어

- [Computer Vision](topics/43-computer-vision/README.md) — 영상 처리와 기하 · 인식 과제와 구조
- [Language · Speech · Multimodal AI](topics/44-language-speech-multimodal/README.md) — 언어와 음성 · 여러 입력을 함께 다루기
- [AI Training & Optimization](topics/45-ai-training-optimization/README.md) — 학습을 구성하는 상태 · 자원 사용을 줄이는 방법
- [AI Applications · Agents · Evaluation](topics/46-ai-agents-evaluation/README.md) — API와 도구 실행 · RAG와 workflow · 평가의 단위
- [Edge AI · TinyML · NPU](topics/47-edge-tinyml/README.md) — 모델에서 장치 실행으로 · 경량화와 측정
- [Software Design & Quality](topics/48-software-quality/README.md) — 테스트의 범위 · 분석과 진단
- [Graphics & Rendering](topics/49-graphics-simulation/README.md) — 좌표에서 pixel까지 · 광선과 재질
- [물리·과학 시뮬레이션](topics/50-physical-scientific-simulation/README.md) — 이산화와 해법 · 해석 대상과 검증
- [DFT · Test · Manufacturing](topics/51-test-manufacturing/README.md) — Scan과 pattern · 내장 테스트와 양산
- [Web · API · Applications](topics/52-web-api-applications/README.md) — 통신과 데이터 · 화면과 서버
- [Mobile & Cross-Platform](topics/53-mobile-crossplatform/README.md) — 플랫폼과 연결 · 자원과 사용자 경험

## 연구와 지원 경험

- [새로운 소자와 컴퓨팅](topics/54-research-frontiers/README.md) — Neuromorphic와 메모리 연산 · 빛, 양자, 생체 인터페이스
- [지원 · 시험 · 면접](topics/55-applications-assessments/README.md) — 기업별 전형 기록 · 코딩테스트 · 연락

[AI 기업과 모델](model-lab/PROVIDERS.md) · [코드 예제](examples/README.md) · [English overview](README.en.md)

## English

Concepts connecting circuits and semiconductor devices with systems, software, and AI. Each document explains the principles and applications, with related tools and references.

### Development environments and foundations

- [Linux & Bash](topics/01-linux-bash/README.md) — Terminal, shell, and Bash · Files and permissions · Processes and development environments
- [Git & Development Tools](topics/02-git-development-tools/README.md) — From local changes to a shared repository · Editing, building, and running
- [Python & Jupyter Environments](topics/03-python-jupyter/README.md) — Project environments · Computing and visualization
- [C, C++ & Python](topics/04-c-cpp-python/README.md) — C: data and memory · C++: resource lifetime and abstraction · Connecting Python and other languages
- [MATLAB & Scientific Computing](topics/05-matlab-scientific/README.md) — Matrix and elementwise operations · Numerical analysis and modeling
- [Math to Code](topics/06-math-to-code/README.md) — From differential equations to loops · Numerical behavior of equivalent expressions
- [Computer Science Foundations](topics/07-cs-foundations/README.md) — Data structures and execution cost · Operating systems and concurrency · Storage, communication, and builds
- [Problem Solving](topics/08-problem-solving/README.md) — Choosing an algorithm · Input size and data structures · Binary-search boundaries

### Circuits, semiconductors, and hardware

- [Circuits & Electronics](topics/09-circuits-electronics/README.md) — RLC circuits in time and frequency · Active devices and amplification
- [Semiconductor Devices](topics/10-semiconductors/README.md) — From MOSFETs to CMOS · Structures and materials · Device models and process variation
- [Analog IC Design: Cadence & Spectre](topics/11-analog-ic-cadence/README.md) — Tool roles · Simulation analyses · From schematic to layout
- [PCB & Hardware Design](topics/12-pcb-hardware/README.md) — Components and manufacturing files · Signal and power paths
- [Verilog, SystemVerilog & RTL](topics/13-verilog-systemverilog/README.md) — Combinational and sequential logic · FSMs, pipelines, and memory
- [Hardware Verification](topics/14-hardware-verification/README.md) — Simulation and coverage · Assertions and formal verification
- [FPGA & ASIC Design](topics/15-fpga-asic/README.md) — Implementation flow · Timing and PPA

### Processors, embedded systems, and control

- [Arm, RISC-V & Computer Architecture](topics/16-arm-riscv/README.md) — Arm and RISC-V · Instruction execution and memory
- [Firmware & RTOS](topics/17-firmware-rtos/README.md) — From reset to main · Peripherals and timing · RTOS concurrency
- [Embedded Linux](topics/18-embedded-linux/README.md) — Boot components · Building and porting
- [OpenOCD, GDB & Instrumentation](topics/19-openocd-debugging/README.md) — Connection layers · Observation tools
- [Interfaces & Communications](topics/20-interfaces-communications/README.md) — Between boards and devices · Networks and on-chip links
- [Signals, DSP & Control](topics/21-signals-control/README.md) — Sampling and transforms · Filters and feedback
- [Robotics, Arduino & Raspberry Pi](topics/22-robotics-boards/README.md) — Board roles · Motion and observation · Software and simulation

### AI, GPUs, and research notes

- [AI, PyTorch & TensorFlow](topics/23-ai-machine-learning/README.md) — Training and evaluation · Model structures · Automatic differentiation examples
- [GPU & Graphics Hardware](topics/24-gpu-architecture/README.md) — Execution and memory · Throughput and bottlenecks
- [CUDA & GPU Optimization](topics/25-cuda-performance/README.md) — Execution units and data movement · Libraries and custom kernels
- [AI Providers, Public Models & APIs](topics/26-open-model-lab/README.md) — Model files · Modification and comparison
- [Paper, Code & Patent Reviews](topics/27-papers-code-patents/README.md) — Connecting papers and code · Patents and references
- [Automation & Portfolio](topics/28-automation-portfolio/README.md) — Scripts and CI · Documentation tools

### Electronic systems and design

- [Electromagnetics, RF & Antennas](topics/29-electromagnetics-rf/README.md) — Reflections and impedance matching · RF circuits and antennas
- [Communication Systems & Information Theory](topics/30-communications-wireless/README.md) — Modulation, coding, and channels · Multicarrier and multi-antenna systems
- [Power Electronics & Energy](topics/31-power-energy/README.md) — Converters and switching · Devices and drive circuits
- [Mixed-Signal, Data Converters & Clocks](topics/32-mixed-signal-data-converters/README.md) — Sampling and quantization · Static and dynamic metrics · Clocks
- [Memory & Storage Systems](topics/33-memory-storage/README.md) — Devices and interfaces · SSDs and reliability
- [SoC & Interconnects](topics/34-soc-interconnects/README.md) — Buses and networks · Addressing and data coherence
- [EDA & Open Hardware Ecosystems](topics/35-eda-open-hardware/README.md) — Data connecting the design flow · PDKs and tools
- [Packaging, Chiplets, Thermal & Reliability](topics/36-packaging-thermal/README.md) — Interconnection structures · Power and heat
- [Sensors, Instrumentation & Experiments](topics/37-sensors-instrumentation/README.md) — Signal paths and errors · Instruments and automated measurements

### Systems, data, and parallel computing

- [Security, Cryptography & Hardware Trust](topics/38-security-cryptography/README.md) — Roles of cryptography · Trust in boot and execution
- [Compilers, Languages & Runtimes](topics/39-compilers-languages/README.md) — From AST to machine code · Tools and execution models
- [Databases & Data Engineering](topics/40-databases-data-engineering/README.md) — SQL and query plans · Pipelines and search
- [Cloud, Distributed Systems & Operations](topics/41-cloud-distributed/README.md) — Failures and consistency · Deployment and operations
- [HPC, Parallel & Distributed Computing](topics/42-hpc-parallel/README.md) — Shared and distributed memory · GPUs and distributed workloads

### AI applications and software

- [Computer Vision & Image Processing](topics/43-computer-vision/README.md) — Image processing and geometry · Recognition tasks and architectures
- [Language, Speech & Multimodal AI](topics/44-language-speech-multimodal/README.md) — Language and speech · Combining multiple input types
- [AI Training, Optimization & Compression](topics/45-ai-training-optimization/README.md) — Training state · Reducing resource use
- [AI Applications, Agents & Evaluation](topics/46-ai-agents-evaluation/README.md) — APIs and tool execution · RAG and workflows · Evaluation units
- [Edge AI, TinyML & NPUs](topics/47-edge-tinyml/README.md) — From a model to device execution · Compression and measurement
- [Software Quality, Design & Testing](topics/48-software-quality/README.md) — Testing scope · Analysis and diagnostics
- [Computer Graphics, Rendering & Simulation](topics/49-graphics-simulation/README.md) — From coordinates to pixels · Rays and materials
- [Physics, Multiphysics & Scientific Simulation](topics/50-physical-scientific-simulation/README.md) — Discretization and solvers · Physical models and validation
- [DFT, Semiconductor Test & Manufacturing](topics/51-test-manufacturing/README.md) — Scan and patterns · Built-in tests and production
- [Web, APIs & Desktop Applications](topics/52-web-api-applications/README.md) — Communication and data · Frontends and servers
- [Mobile, Cross-Platform & Device Integration](topics/53-mobile-crossplatform/README.md) — Platforms and integration · Resources and user experience

### Research and application experiences

- [Research Frontiers](topics/54-research-frontiers/README.md) — Neuromorphic and memory-based computation · Light, quantum systems, and biological interfaces
- [Applications, Resumes & Assessment Experiences](topics/55-applications-assessments/README.md) — Company application records · Coding tests · Contact

[AI models and providers](model-lab/PROVIDERS.md) · [Code examples](examples/README.md) · [English introduction](README.en.md)

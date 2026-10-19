# 도구 찾아보기

도구가 담당하는 일과 관련 문서를 함께 묶었다.

## 역할별 설명

| 도구·기술 | 역할 |
|---|---|
| Linux | 프로세스·메모리·파일·장치를 관리하는 커널. 배포판과 임베디드 운영 환경의 기반이다. |
| Ubuntu · Debian · Fedora · Arch Linux | 커널과 사용자 프로그램·패키지 관리를 묶은 Linux 배포판. 패키지 형식과 배포 정책이 다르다. |
| WSL2 | Windows에서 Linux 커널 기반 환경을 실행하는 기능. 호스트와 파일·장치·GPU 지원 조건을 함께 갖는다. |
| Bash · Zsh | 명령 해석과 프로그램 실행을 맡는 셸. 반복 작업을 스크립트로 구성한다. |
| SSH · tmux · rsync | 각각 원격 접속, 터미널 세션 관리, 파일 동기화에 쓰인다. |
| Git · GitHub · GitLab | Git은 변경 이력 도구, GitHub·GitLab은 저장소와 협업·CI 서비스다. |
| VS Code · Vim · Neovim | 소스 편집기. 실제 컴파일·실행 도구는 별도로 연결한다. |
| GCC · Clang · LLVM | GCC·Clang은 컴파일러 생태계이고 LLVM은 IR·최적화·대상 코드 생성의 기반을 제공한다. |
| Make · Ninja · CMake · Meson | Make·Ninja는 빌드 작업 실행, CMake·Meson은 빌드 구성 생성에 사용된다. |
| Docker · Podman | 컨테이너 이미지로 사용자 공간 의존성과 실행 환경을 묶고 관리한다. |
| Python · pip · venv · uv | Python 실행과 패키지 설치·환경 분리·프로젝트 의존성 관리를 구성하는 도구들이다. |
| Conda · Mamba | Python과 바이너리 의존성을 환경 단위로 관리한다. pip의 패키지 관리 범위와 다르다. |
| Jupyter Notebook · JupyterLab · IPython | Notebook은 계산 문서, Lab은 작업 UI, IPython은 Python 대화형 실행·kernel 생태계다. |
| NumPy · SciPy | 다차원 배열과 과학 계산. 선형대수·최적화·적분·신호처리를 코드로 연결한다. |
| pandas · Matplotlib · Seaborn · Plotly | 표 데이터 처리와 정적·통계·대화형 시각화에 쓰인다. |
| MATLAB · Simulink · Octave | 행렬 기반 계산, 블록선도 모델링, MATLAB 호환 수치 계산 환경이다. |
| SymPy · Mathematica · Maple · Julia | 기호 계산 또는 수치 알고리즘 표현에 쓰인다. 수식 변환과 수치 근사는 다른 작업이다. |
| Virtuoso · Spectre · ADE | 회로도·레이아웃 환경, 회로 시뮬레이터, 해석 조건·결과 관리 환경을 각각 담당한다. |
| SKILL · OCEAN · Tcl | EDA 도구의 기능 확장·해석·결과 처리·설계 흐름 자동화에 쓰이는 언어와 인터페이스다. |
| Custom Compiler · HSPICE · PrimeSim · Eldo | Custom IC 설계·회로 해석을 구성하는 상용 도구 계열이다. |
| LTspice · ngspice · Xschem | 회로 시뮬레이션과 schematic 작업에 쓰인다. 공정 모델과 netlist가 해석 입력을 이룬다. |
| KiCad · Altium · OrCAD/Allegro · PADS/Xpedition · EasyEDA | 회로도와 PCB 설계 도구. 연결과 부품·배치배선·제조 데이터를 다룬다. |
| Verilog · SystemVerilog · VHDL | 하드웨어 기술 언어. 합성 가능한 설계와 시뮬레이션·검증의 언어 범위가 다르다. |
| Verilog-A · Verilog-AMS | 아날로그 동작과 mixed-signal 모델을 표현한다. |
| Chisel · SpinalHDL · Amaranth · HLS | 고수준 언어에서 하드웨어를 구성하거나 생성하는 접근이다. |
| Verilator · Icarus Verilog · Questa · Xcelium · VCS | RTL 시뮬레이션·검증 도구. 언어 지원과 실행 방식이 다르다. |
| GTKWave · cocotb · UVM · SymbiYosys | 각각 파형 보기, Python 검증, 검증 구성·재사용, 공개 formal 흐름에 쓰인다. |
| Vivado · Vitis · Quartus · Radiant | 대상 FPGA의 논리 구현·시스템 개발·배치배선 흐름을 제공한다. |
| Yosys · nextpnr · OpenROAD · OpenLane | 합성과 FPGA·ASIC 물리 구현을 구성하는 공개 도구·흐름이다. |
| Genus · Innovus · Design Compiler · Fusion Compiler · PrimeTime | ASIC 합성·물리 구현·타이밍 분석을 구성하는 상용 도구다. |
| KLayout · Magic · Netgen | 레이아웃 열람·편집과 회로 비교 등 공개 IC 설계 흐름에 쓰인다. |
| SKY130 · GF180MCU · IHP SG13G2 | 공개 공정 자료를 통해 소자·layer·rule·설계 흐름을 다룰 수 있는 PDK 생태계다. |
| Arm · RISC-V · x86-64 · MIPS · AVR | 명령어와 소프트웨어 실행을 정의하는 아키텍처·ISA 생태계다. |
| PicoRV32 · Ibex · CVA6 · Rocket · BOOM | 구조와 복잡도가 다른 공개 RISC-V CPU 구현 프로젝트다. |
| QEMU · gem5 | 각각 시스템·명령 실행 에뮬레이션과 컴퓨터 구조 시뮬레이션에 쓰인다. |
| STM32 · ESP32 · nRF · RP2040/RP2350 | MCU 제품군. 코어·주변장치·무선 기능·개발 도구가 다르다. |
| FreeRTOS · Zephyr · ThreadX · RT-Thread | 태스크·스케줄링·동기화 등 임베디드 실행 기반을 제공한다. |
| Buildroot · Yocto · U-Boot · BusyBox | 시스템 이미지·배포판 구성, 부팅, 작은 사용자 공간 명령 모음을 담당한다. |
| OpenOCD · GDB · LLDB · pyOCD · probe-rs | 소스 수준 디버깅과 프로브·대상 장치 연결을 구성하는 도구다. |
| ST-Link · J-Link · SWO · ETM | 디버그 프로브 제품과 장치 trace 기능. 대상별 지원 범위가 다르다. |
| Saleae · PulseView · sigrok | 디지털 파형과 프로토콜을 수집·해석하는 하드웨어·소프트웨어 생태계다. |
| Arduino · Raspberry Pi · BeagleBone · Jetson | MCU·SBC·AI 연산 보드 등 개발 목적과 실행 환경이 다른 보드 생태계다. |
| ROS 2 · MoveIt · Nav2 | 로봇 기능 간 통신, 조작 계획, 이동 로봇 내비게이션을 구성한다. |
| Gazebo · MuJoCo · Isaac Sim | 로봇과 물리 환경을 시뮬레이션한다. 센서·동역학 모델이 실제 환경과의 차이를 만든다. |
| PyTorch · TensorFlow · Keras · JAX | 텐서 연산과 자동미분·모델 학습을 구성하는 framework 생태계다. |
| scikit-learn · XGBoost · LightGBM · CatBoost | 전통적인 머신러닝·gradient boosting 모델과 평가 흐름에 쓰인다. |
| Transformers · Datasets · Tokenizers · Safetensors | 모델 인터페이스, 데이터 처리, token 변환, tensor 저장 형식을 제공한다. |
| Lightning · fastai | 모델 학습 코드와 실행 흐름을 구성하는 상위 라이브러리다. |
| CUDA · cuBLAS · cuDNN · CUTLASS | NVIDIA GPU 실행 플랫폼과 선형대수·신경망·행렬 연산 구성요소다. |
| Triton · Nsight Systems · Nsight Compute | GPU kernel 작성과 시스템·kernel 수준 성능 분석을 담당한다. |
| ROCm · HIP · SYCL · oneAPI · OpenCL · Metal | 여러 하드웨어와 운영 환경의 가속기 연산을 구성하는 생태계다. |
| TensorRT · OpenVINO · ONNX | 추론 최적화·실행과 모델 교환 표현을 담당한다. 모델 형식과 실행기는 같은 개념이 아니다. |
| LiteRT · TensorFlow Lite Micro · CMSIS-NN · ExecuTorch · TVM | 모바일·MCU·엣지 모델 실행과 변환·kernel·컴파일에 쓰인다. |
| PEFT · TRL · Accelerate · DeepSpeed · FSDP · DDP | Adapter 학습·후학습·장치 배치·분산 학습 상태와 통신을 다룬다. |
| MLflow · Weights & Biases · TensorBoard · Optuna | 실험의 parameter·metric·산출물 기록과 탐색을 담당한다. |
| LangChain · LlamaIndex · DSPy · MCP | 모델 응용·검색·workflow 구성과 도구·자료 연결에 쓰인다. |
| lm-evaluation-harness · Ragas · promptfoo | 언어 모델·RAG·prompt 응용의 평가와 회귀 확인에 쓰인다. |
| OpenCV · Kornia · torchvision · timm · Detectron2 · MMDetection | 영상 연산·모델·학습·검출 구성요소를 제공한다. |
| torchaudio · SentencePiece | 음성 처리와 tokenization 도구. 입력 표현이 이후 모델 계산과 연결된다. |
| HFSS · CST · ADS · AWR · Sonnet · openEMS · scikit-rf | 전자기장·RF 회로·network 데이터 해석에 쓰인다. |
| GNU Radio · USRP | 소프트웨어 신호처리 블록을 실제 무선 송수신 장치와 연결하는 SDR 생태계다. |
| PLECS · PSIM | 스위칭 전력단과 제어의 시뮬레이션에 쓰인다. |
| PyVISA · SCPI · LabVIEW · NI-DAQ | 계측기 통신 명령, 장비 접근, 제어·수집 환경을 구성한다. |
| COMSOL · Ansys · OpenFOAM · FEniCS · MEEP · LAMMPS | 다물리·유체·유한요소·전자기·분자동역학 등 서로 다른 물리 문제를 푼다. |
| SQLite · PostgreSQL · MySQL · DuckDB · Redis | 내장형·서버형·분석형·메모리형 등 데이터 저장과 질의 방식이 다른 시스템이다. |
| Parquet · Arrow · Spark · Kafka · FAISS · pgvector | 저장·메모리 표현, 대규모 처리·이벤트 전달·벡터 검색을 구성한다. |
| Kubernetes · Terraform · Prometheus · Grafana · OpenTelemetry | 배포·인프라 선언·수치 관측·시각화·trace를 구성한다. |
| OpenMP · MPI · NCCL · Slurm · Ray · Dask | 공유 메모리·분산 통신·GPU 통신·작업 관리·분산 실행에 쓰인다. |
| pytest · unittest · GoogleTest · Catch2 · CTest · Hypothesis | 단위·통합·속성 기반 테스트의 작성과 실행에 쓰인다. |
| ASan · UBSan · TSan · Valgrind · clang-tidy · Ruff · CodeQL | 실행 중 오류와 정적 코드 문제를 찾는 진단·분석 도구다. |
| OpenGL · Vulkan · DirectX · WebGPU · GLSL · HLSL | 그래픽·GPU 연산 API와 shader 언어다. |
| Blender · Mitsuba · PBRT · Unreal · Unity | 장면 제작·물리 렌더링·실시간 그래픽과 시뮬레이션에 쓰인다. |
| Tessent · TestMAX · Modus | DFT와 제조 테스트의 구조·pattern 생성·분석에 관련된 도구다. |
| FastAPI · Flask · Django · Node.js · Spring | 서버·API·웹 애플리케이션을 구성하는 서로 다른 생태계다. |
| React · Vue · Svelte · TypeScript | 웹 UI 구성과 코드의 정적 형식 검사에 쓰인다. |
| Qt · PySide · Electron · Streamlit · Gradio | 데스크톱 UI와 데이터·모델용 화면을 구성한다. |
| Kotlin · Java · Swift · Flutter · Dart · React Native · KMP | 모바일과 여러 플랫폼의 애플리케이션 코드를 구성한다. |
| Quarto · Jekyll · Hugo · MkDocs · Sphinx · Doxygen · Jupyter Book | 글·계산 문서·사이트·API 문서를 생성한다. |
| GitHub Actions · GitLab CI · Python · Bash · PowerShell | 저장소 이벤트와 스크립트를 연결해 빌드·검사·문서 생성을 자동 실행한다. |
| Zotero · BibTeX · arXiv · IEEE Xplore · ACM DL · KIPRIS | 문헌을 검색하고 서지 정보·인용을 관리하는 경로와 도구다. |

## 분야별 문서

### [Linux & Bash](../topics/01-linux-bash/README.md)

운영체제·셸·원격 접속·프로세스·파일 관리

Ubuntu, Debian, Fedora, Arch Linux, WSL2, Bash, Zsh, systemd, SSH, tmux, rsync

### [Git & Development Tools](../topics/02-git-development-tools/README.md)

버전 관리·편집·컴파일·빌드·컨테이너

Git, GitHub, GitLab, GitHub CLI/Desktop, VS Code, Vim/Neovim, GCC, Clang/LLVM, Make, CMake, Meson, Ninja, Docker, Podman

### [Python & Jupyter](../topics/03-python-jupyter/README.md)

Python 의존성·노트북·수치 배열·표·그래프

Python, pip, uv, venv, Conda/Mamba, Jupyter Notebook/Lab, IPython, NumPy, SciPy, pandas, Matplotlib, Seaborn, Plotly

### [C, C++ & Python](../topics/04-c-cpp-python/README.md)

언어·메모리 수명·자료구조·언어 연결

C, C++, Python, Rust, Go, Java, C#, JavaScript/TypeScript, Julia, R, Tcl, Lua, Assembly

### [MATLAB & Scientific Computing](../topics/05-matlab-scientific/README.md)

수치·기호 계산·동적 모델링

MATLAB, Simulink, GNU Octave, SciPy, SymPy, Mathematica, Maple, Julia

### [수식을 코드로](../topics/06-math-to-code/README.md)

이산화·수치 해법·오차 분석

Calculus, Linear Algebra, Probability, Statistics, ODE/PDE, Numerical Analysis, Optimization, Information Theory, Graph Theory

### [컴퓨터공학 기초](../topics/07-cs-foundations/README.md)

운영체제·자료구조·실행 모델

Linux, xv6, OSTEP topics, Networking, TCP/IP, Filesystems, Databases, Compilers, Concurrency

### [알고리즘과 코딩테스트](../topics/08-problem-solving/README.md)

알고리즘 문제·채점 환경

프로그래머스 / Programmers, 백준 / Baekjoon, LeetCode, Codeforces, AtCoder, HackerRank, Codility, SWEA

### [회로와 전자공학](../topics/09-circuits-electronics/README.md)

소자·회로 모델·주파수 응답

RLC, Op-Amp, BJT, MOSFET, CMOS, Filters, Oscillators, Regulators, SPICE, Breadboard Measurements

### [반도체 소자](../topics/10-semiconductors/README.md)

소자 물리·compact model·TCAD

PN, MOS, BJT, CMOS, FinFET, GAA, SOI, SiC/GaN, BSIM, SRAM/DRAM/NAND, TCAD

### [Analog IC · Cadence · Spectre](../topics/11-analog-ic-cadence/README.md)

회로도·회로 시뮬레이션·레이아웃·검증

Cadence Virtuoso, Spectre, ADE, SKILL, OCEAN, Synopsys Custom Compiler, HSPICE, PrimeSim, Siemens Eldo, LTspice, ngspice, Xschem

### [PCB & Hardware Design](../topics/12-pcb-hardware/README.md)

PCB 설계·제조 데이터·신호 해석

KiCad, Altium Designer, OrCAD, Allegro, PADS, Xpedition, EasyEDA, IBIS, SI/PI, EMC/EMI, DFM

### [Verilog · SystemVerilog · RTL](../topics/13-verilog-systemverilog/README.md)

회로 기술·하드웨어 생성

Verilog, SystemVerilog, VHDL, Verilog-A/AMS, Chisel, SpinalHDL, Amaranth, HLS

### [Hardware Verification](../topics/14-hardware-verification/README.md)

시뮬레이션·파형·assertion·formal

UVM, SVA, cocotb, Verilator, Icarus Verilog, GTKWave, Questa, Xcelium, VCS, SymbiYosys, Formal/Equivalence

### [FPGA & ASIC](../topics/15-fpga-asic/README.md)

합성·배치배선·STA

AMD/Xilinx Vivado/Vitis, Intel/Altera Quartus, Lattice Radiant, Yosys, nextpnr, OpenROAD/OpenLane, Genus/Innovus, Design Compiler/Fusion Compiler, PrimeTime

### [Arm · RISC-V · Computer Architecture](../topics/16-arm-riscv/README.md)

ISA·CPU 구현·에뮬레이션

Arm Cortex-M/A/R, RISC-V RV32/RV64, x86-64, MIPS, AVR, PicoRV32, Ibex, CVA6, Rocket Chip, BOOM, gem5, QEMU

### [Firmware & RTOS](../topics/17-firmware-rtos/README.md)

MCU·드라이버·실시간 실행

STM32, ESP32/ESP-IDF, Nordic nRF, NXP, TI, Microchip AVR/PIC/SAM, Renesas, RP2040/RP2350, FreeRTOS, Zephyr, ThreadX, RT-Thread

### [Embedded Linux](../topics/18-embedded-linux/README.md)

부팅·배포판 빌드·보드 지원

Linux Kernel, U-Boot, Device Tree, Buildroot, Yocto/OpenEmbedded, BusyBox, QEMU, BSP, Drivers

### [OpenOCD · GDB · Debugging](../topics/19-openocd-debugging/README.md)

디버거·프로브·trace·파형 관찰

OpenOCD, GDB, LLDB, J-Link, ST-Link, pyOCD, probe-rs, JTAG, SWD, SWO, ETM, Saleae, PulseView, Sigrok

### [Interfaces & Communications](../topics/20-interfaces-communications/README.md)

보드·장치·온칩·네트워크 연결

UART, SPI, I2C, I3C, CAN/CAN-FD, USB, Ethernet, PCIe, MIPI, DDR, AXI/AHB/APB, MQTT, Modbus, BLE, Wi-Fi, Zigbee, LoRa

### [신호처리와 제어](../topics/21-signals-control/README.md)

필터·상태 추정·제어

FFT, FIR/IIR, PID, State Space, LQR/LQG, MPC, Kalman/EKF/UKF, System Identification, SciPy Signal, MATLAB Control

### [Robotics · Arduino · Raspberry Pi](../topics/22-robotics-boards/README.md)

보드·센서·로봇 통신·계획·시뮬레이션

Arduino, Raspberry Pi, STM32 Nucleo, ESP32, BeagleBone, Jetson, ROS 2, MoveIt, Nav2, Gazebo, MuJoCo, Isaac Sim, SLAM

### [AI · Machine Learning · Deep Learning](../topics/23-ai-machine-learning/README.md)

모델 구성·학습·자동미분

PyTorch, TensorFlow/Keras, JAX, scikit-learn, XGBoost, LightGBM, CatBoost, Hugging Face, Lightning, fastai

### [GPU Architecture](../topics/24-gpu-architecture/README.md)

실행 자원·GPU 메모리·그래픽 API

NVIDIA, AMD, Intel, Apple GPU, SIMT/SIMD, Cache/VRAM, HBM/GDDR, PCIe/NVLink, Roofline, Vulkan, OpenGL, DirectX

### [CUDA & GPU Optimization](../topics/25-cuda-performance/README.md)

GPU 연산·라이브러리·profiling

CUDA, cuBLAS, cuDNN, CUTLASS, Triton, Nsight, ROCm/HIP, SYCL/oneAPI, OpenCL, Metal, OpenMP/OpenACC, TensorRT, OpenVINO

### [AI Models & APIs](../topics/26-open-model-lab/README.md)

모델 배포·가중치·API·runtime

OpenAI, Google/DeepMind, Microsoft, Meta, Anthropic, Samsung, DeepSeek, Qwen, Mistral, IBM, NVIDIA, LG, NAVER, Kakao, Upstage, SKT

### [논문 · 코드 · 특허](../topics/27-papers-code-patents/README.md)

문헌 검색·코드·서지 관리

arXiv, IEEE, ACM, NeurIPS, ICML, ICLR, CVPR, ISSCC, DAC, DATE, KIPRIS, Google Patents, Zotero, BibTeX

### [자동화와 기술 기록](../topics/28-automation-portfolio/README.md)

스크립트·CI·문서 생성

Python, Bash, PowerShell, GitHub Actions, GitLab CI, Docker, Quarto, Jekyll, Hugo, MkDocs, Sphinx, Doxygen, Jupyter Book

### [전자기학 · RF · 안테나](../topics/29-electromagnetics-rf/README.md)

전자기장·RF 회로·S-parameter

HFSS, CST, ADS, AWR, Sonnet, openEMS, scikit-rf, VNA, Spectrum Analyzer

### [통신이론과 무선 시스템](../topics/30-communications-wireless/README.md)

신호처리 블록·SDR

GNU Radio, SDR, USRP, RTL-SDR, OFDM, QAM, MIMO, LDPC, Polar Codes

### [전력전자와 에너지](../topics/31-power-energy/README.md)

전력단·제어 시뮬레이션

PLECS, PSIM, LTspice, Simulink, Buck/Boost, LLC, BMS, PMIC

### [Mixed-Signal · ADC · DAC · Clock](../topics/32-mixed-signal-data-converters/README.md)

변환기·클록·정적·동적 지표

SAR ADC, Delta-Sigma, DAC, PLL, DLL, CDR, Spectre, Verilog-AMS

### [Memory & Storage](../topics/33-memory-storage/README.md)

메모리·저장 프로토콜·I/O 측정

SRAM, DRAM, NAND, DDR, LPDDR, GDDR, HBM, NVMe, fio, CXL

### [SoC & Interconnects](../topics/34-soc-interconnects/README.md)

주소·버스·일관성

AXI, AMBA, TileLink, Wishbone, NoC, PCIe, CXL, Chiplet, CHI

### [EDA & Open Hardware](../topics/35-eda-open-hardware/README.md)

PDK·표준 셀·공개 EDA 흐름

Cadence, Synopsys, Siemens EDA, Yosys, OpenROAD, OpenLane, KLayout, Magic, Netgen, SKY130, GF180, IHP SG13G2

### [Packaging · Chiplets · Thermal](../topics/36-packaging-thermal/README.md)

전기·열·구조 모델

Chiplets, UCIe, 2.5D/3D IC, Interposer, COMSOL, Ansys, Thermal RC, EM/IR

### [센서와 계측](../topics/37-sensors-instrumentation/README.md)

계측 명령·장비 연결·데이터 수집

SCPI, PyVISA, Sigrok, PulseView, LabVIEW, NI DAQ, Oscilloscope, VNA

### [Security · Cryptography · Hardware Trust](../topics/38-security-cryptography/README.md)

암호·부팅 신뢰·코드 진단

TLS, AES, RSA, ECC, Secure Boot, TrustZone, TPM, Sanitizers, Fuzzing, CodeQL

### [Compilers · Languages · Runtimes](../topics/39-compilers-languages/README.md)

frontend·IR·코드 생성·runtime

LLVM, MLIR, GCC, Clang, Rust, Go, Java/JVM, CPython, Julia, Tcl, SKILL

### [Databases & Data Engineering](../topics/40-databases-data-engineering/README.md)

질의·저장 형식·stream·검색

SQLite, PostgreSQL, MySQL, DuckDB, Redis, Parquet, Arrow, Spark, Kafka, FAISS, pgvector

### [Cloud & Distributed Systems](../topics/41-cloud-distributed/README.md)

인프라·배포·관측

AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Prometheus, Grafana, OpenTelemetry

### [HPC & Parallel Computing](../topics/42-hpc-parallel/README.md)

병렬화·통신·작업 관리

OpenMP, MPI, OpenACC, SIMD, AVX/NEON, NCCL, Slurm, Ray, Dask, perf

### [Computer Vision](../topics/43-computer-vision/README.md)

영상 연산·모델·기하

OpenCV, torchvision, timm, ResNet, ViT, YOLO, SAM, DINO, Detectron2, MMDetection, Kornia

### [Language · Speech · Multimodal AI](../topics/44-language-speech-multimodal/README.md)

token·언어·음성·시각 표현

BERT, T5, GPT, Whisper, wav2vec, CLIP, LLaVA, Transformers, torchaudio, SentencePiece

### [AI Training & Optimization](../topics/45-ai-training-optimization/README.md)

분산 학습·adapter·양자화·실험 관리

PEFT, TRL, Accelerate, DeepSpeed, FSDP, DDP, MLflow, W&B, TensorBoard, Optuna, bitsandbytes

### [AI Applications · Agents · Evaluation](../topics/46-ai-agents-evaluation/README.md)

도구 연결·검색·workflow·평가

OpenAI APIs, Claude API, Gemini API, LangChain, LlamaIndex, DSPy, MCP, lm-evaluation-harness, Ragas, promptfoo

### [Edge AI · TinyML · NPU](../topics/47-edge-tinyml/README.md)

모델 변환·장치 추론

ONNX Runtime, TensorRT, OpenVINO, LiteRT/TFLite, TFLite Micro, CMSIS-NN, ExecuTorch, TVM, Jetson, Coral

### [Software Design & Quality](../topics/48-software-quality/README.md)

테스트·정적 분석·메모리 진단

pytest, unittest, GoogleTest, Catch2, CTest, Hypothesis, Valgrind, ASan/UBSan/TSan, clang-tidy, Ruff

### [Graphics & Rendering](../topics/49-graphics-simulation/README.md)

shader·장면·렌더링

OpenGL, Vulkan, DirectX, WebGPU, GLSL, HLSL, Blender, Mitsuba, PBRT, Unreal, Unity

### [물리·과학 시뮬레이션](../topics/50-physical-scientific-simulation/README.md)

방정식·mesh·수치 해법

COMSOL, Ansys, HFSS, CST, OpenFOAM, FEniCS, MEEP, openEMS, LAMMPS

### [DFT · Test · Manufacturing](../topics/51-test-manufacturing/README.md)

테스트 접근·pattern·제조 검사

DFT, Scan, ATPG, MBIST/LBIST, ATE, JTAG/Boundary Scan, Tessent, TestMAX, Modus

### [Web · API · Applications](../topics/52-web-api-applications/README.md)

서버·API·UI·dashboard

FastAPI, Flask, Django, Node.js, Spring, React, Vue, Svelte, TypeScript, Qt/PySide, Electron, Streamlit, Gradio

### [Mobile & Cross-Platform](../topics/53-mobile-crossplatform/README.md)

모바일 UI·장치 연결·추론

Kotlin, Java, Android, Swift, iOS, Flutter, Dart, React Native, Kotlin Multiplatform, Core ML

### [새로운 소자와 컴퓨팅](../topics/54-research-frontiers/README.md)

소자·새로운 연산 구조

SNN, Neuromorphic, Event Camera, Quantum, Photonics, Compute-in-Memory, Memristor, Wearables

### [지원 · 시험 · 면접](../topics/55-applications-assessments/README.md)

문서·평가·지원 과정

국민대학교 / Kookmin University, 기업별 전형 / Company Applications, Resume/CV, 코딩테스트 / Coding Tests, 역량검사 / Competency Assessments

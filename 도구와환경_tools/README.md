# 도구 찾아보기

도구별 역할과 관련 문서를 정리했습니다.

처음 설치와 실행의 관계를 정리하실 때에는 [개발 환경의 구성](개발환경_GETTING_STARTED.md), 언어·runtime·모델·단위를 구분하실 때에는 [기술 용어](기술용어_TERMINOLOGY.md)부터 읽으시면 됩니다.

A guide to what each tool does and where its related notes are kept.

## 역할별 설명

| 도구·기술 | 역할 | Role |
|---|---|---|
| Linux | 프로세스·메모리·파일·장치를 관리하는 커널. 배포판과 임베디드 운영 환경의 기반입니다. | A kernel that manages processes, memory, files, and devices; the foundation of Linux distributions and embedded Linux systems. |
| Ubuntu · Debian · Fedora · Arch Linux | 커널과 사용자 프로그램·패키지 관리를 묶은 Linux 배포판. 패키지 형식과 배포 정책이 다릅니다. | Linux distributions that combine the kernel, user programs, and package management; package formats and release policies differ. |
| WSL2 | Windows에서 Linux 커널 기반 환경을 실행하는 기능. 파일·장치·GPU 사용은 호스트와의 연결 및 지원 조건에 영향을 받습니다. | Runs a Linux-kernel environment on Windows. File access, devices, and GPUs also depend on host integration and support. |
| Bash · Zsh | 명령 해석과 프로그램 실행을 맡는 셸. 반복 작업을 스크립트로 구성합니다. | Shells that interpret commands and launch programs, with scripting for repeated work. |
| SSH · tmux · rsync | 각각 원격 접속, 터미널 세션 관리, 파일 동기화에 쓰입니다. | Remote access, terminal-session management, and file synchronization, respectively. |
| Git · GitHub · GitLab | Git은 변경 이력 도구, GitHub·GitLab은 저장소와 협업·CI 서비스입니다. | Git tracks changes. GitHub and GitLab host repositories and provide collaboration and CI services. |
| VS Code · Vim · Neovim | 소스 편집기. 실제 컴파일·실행 도구는 별도로 연결합니다. | Source editors that connect to separate tools for compilation and execution. |
| GCC · Clang · LLVM | GCC·Clang은 컴파일러 생태계이고 LLVM은 IR·최적화·대상 코드 생성의 기반을 제공합니다. | GCC and Clang are compiler ecosystems. LLVM provides intermediate representations, optimization, and target code generation. |
| Make · Ninja · CMake · Meson | Make·Ninja는 빌드 작업 실행, CMake·Meson은 빌드 구성 생성에 사용됩니다. | Make and Ninja run build steps; CMake and Meson generate build configurations. |
| Docker · Podman | 컨테이너 이미지로 사용자 공간 의존성과 실행 환경을 묶고 관리합니다. | Package and manage user-space dependencies and execution environments as container images. |
| Python · pip · venv · uv | Python 실행과 패키지 설치·환경 분리·프로젝트 의존성 관리를 구성하는 도구들입니다. | Python execution, package installation, isolated environments, and project dependency management. |
| Conda · Mamba | Python과 바이너리 의존성을 환경 단위로 관리합니다. pip의 패키지 관리 범위와 다릅니다. | Manage Python and binary dependencies as environments, with a different scope from pip package management. |
| Jupyter Notebook · JupyterLab · IPython | Notebook은 계산 문서, Lab은 작업 UI, IPython은 Python 대화형 실행·kernel 생태계입니다. | Notebook is a computational document; Lab provides its workspace UI; IPython supports interactive Python execution and kernels. |
| NumPy · SciPy | 다차원 배열과 과학 계산. 선형대수·최적화·적분·신호처리를 코드로 연결합니다. | Multidimensional arrays and scientific computing, including linear algebra, optimization, integration, and signal processing. |
| pandas · Matplotlib · Seaborn · Plotly | 표 데이터 처리와 정적·통계·대화형 시각화에 쓰입니다. | Tabular data processing and static, statistical, and interactive visualization. |
| MATLAB · Simulink · Octave | 행렬 기반 계산, 블록선도 모델링, MATLAB 호환 수치 계산 환경입니다. | Matrix-based computation, block-diagram modeling, and MATLAB-compatible numerical computing, respectively. |
| SymPy · Mathematica · Maple · Julia | 기호 계산 또는 수치 알고리즘 표현에 쓰입니다. 수식 변환과 수치 근사는 다른 작업입니다. | Symbolic computation and numerical algorithms. Transforming expressions and approximating numerical values are distinct tasks. |
| Virtuoso · Spectre · ADE | 회로도·레이아웃 환경, 회로 시뮬레이터, 해석 조건·결과 관리 환경을 각각 담당합니다. | Schematic/layout design, circuit simulation, and analysis-condition/result management, respectively. |
| SKILL · OCEAN · Tcl | EDA 도구의 기능 확장·해석·결과 처리·설계 흐름 자동화에 쓰이는 언어와 인터페이스입니다. | Languages and interfaces for EDA extensions, simulation, result processing, and design-flow automation. |
| Custom Compiler · HSPICE · PrimeSim · Eldo | Custom IC 설계·회로 해석을 구성하는 상용 도구 계열입니다. | Commercial tools for custom IC design and circuit simulation. |
| LTspice · ngspice · Xschem | 회로 시뮬레이션과 schematic 작업에 쓰입니다. 공정 모델과 netlist가 해석 입력을 이룹니다. | Circuit simulation and schematic tools, using device models and netlists as simulation inputs. |
| KiCad · Altium · OrCAD/Allegro · PADS/Xpedition · EasyEDA | 회로도와 PCB 설계 도구. 연결과 부품·배치배선·제조 데이터를 다룹니다. | Schematic and PCB tools covering connectivity, components, placement, routing, and manufacturing data. |
| Verilog · SystemVerilog · VHDL | 하드웨어 기술 언어. 합성 가능한 설계와 시뮬레이션·검증의 언어 범위가 다릅니다. | Hardware description languages whose simulation and verification features extend beyond their synthesizable subsets. |
| Verilog-A · Verilog-AMS | 아날로그 동작과 mixed-signal 모델을 표현합니다. | Describe analog behavior and mixed-signal models. |
| Chisel · SpinalHDL · Amaranth · HLS | 고수준 언어에서 하드웨어를 구성하거나 생성하는 접근입니다. | Construct or generate hardware using higher-level languages. |
| Verilator · Icarus Verilog · Questa · Xcelium · VCS | RTL 시뮬레이션·검증 도구. 언어 지원과 실행 방식이 다릅니다. | RTL simulation and verification tools with different language support and execution models. |
| GTKWave · cocotb · UVM · SymbiYosys | 각각 파형 보기, Python 검증, 검증 구성·재사용, 공개 formal 흐름에 쓰입니다. | Waveform viewing, Python-based verification, reusable verification infrastructure, and open formal workflows, respectively. |
| Vivado · Vitis · Quartus · Radiant | 대상 FPGA의 논리 구현·시스템 개발·배치배선 흐름을 제공합니다. | Logic implementation, system development, and placement and routing for supported FPGA devices. |
| Yosys · nextpnr · OpenROAD · OpenLane | 합성과 FPGA·ASIC 물리 구현을 구성하는 공개 도구·흐름입니다. | Open tools and flows for synthesis and FPGA/ASIC physical implementation. |
| Genus · Innovus · Design Compiler · Fusion Compiler · PrimeTime | ASIC 합성·물리 구현·타이밍 분석을 구성하는 상용 도구입니다. | Commercial tools for ASIC synthesis, physical implementation, and timing analysis. |
| KLayout · Magic · Netgen | 레이아웃 열람·편집과 회로 비교 등 공개 IC 설계 흐름에 쓰입니다. | Layout viewing, editing, and circuit comparison in open IC design flows. |
| SKY130 · GF180MCU · IHP SG13G2 | 공개 공정 자료를 통해 소자·layer·rule·설계 흐름을 다룰 수 있는 PDK 생태계입니다. | PDK ecosystems exposing devices, layers, rules, and design flows through published process data. |
| Arm · RISC-V · x86-64 · MIPS · AVR | 명령어와 소프트웨어 실행을 정의하는 아키텍처·ISA 생태계입니다. | Architecture and ISA ecosystems defining instructions and software-visible execution. |
| PicoRV32 · Ibex · CVA6 · Rocket · BOOM | 구조와 복잡도가 다른 공개 RISC-V CPU 구현 프로젝트입니다. | Open RISC-V CPU implementations with different structures and complexity. |
| QEMU · gem5 | 각각 시스템·명령 실행 에뮬레이션과 컴퓨터 구조 시뮬레이션에 쓰입니다. | System/instruction emulation and computer-architecture simulation, respectively. |
| STM32 · ESP32 · nRF · RP2040/RP2350 | MCU 제품군. 코어·주변장치·무선 기능·개발 도구가 다릅니다. | MCU families with different cores, peripherals, wireless capabilities, and development tools. |
| FreeRTOS · Zephyr · ThreadX · RT-Thread | 태스크·스케줄링·동기화 등 임베디드 실행 기반을 제공합니다. | Embedded execution services such as tasks, scheduling, and synchronization. |
| Buildroot · Yocto · U-Boot · BusyBox | 시스템 이미지·배포판 구성, 부팅, 작은 사용자 공간 명령 모음을 담당합니다. | System-image/distribution construction, booting, and a compact collection of user-space commands. |
| OpenOCD · GDB · LLDB · pyOCD · probe-rs | 소스 수준 디버깅과 프로브·대상 장치 연결을 구성하는 도구입니다. | Tools for source-level debugging and connecting probes to target devices. |
| ST-Link · J-Link · SWO · ETM | 디버그 프로브 제품과 장치 trace 기능. 대상별 지원 범위가 다릅니다. | Debug probe products and device trace facilities, with target-dependent support. |
| Saleae · PulseView · sigrok | 디지털 파형과 프로토콜을 수집·해석하는 하드웨어·소프트웨어 생태계입니다. | Hardware and software for capturing and interpreting digital waveforms and protocols. |
| Arduino · Raspberry Pi · BeagleBone · Jetson | MCU·SBC·AI 연산 보드 등 개발 목적과 실행 환경이 다른 보드 생태계입니다. | Board ecosystems spanning MCUs, single-board computers, and AI compute devices, with different execution environments. |
| ROS 2 · MoveIt · Nav2 | 로봇 기능 간 통신, 조작 계획, 이동 로봇 내비게이션을 구성합니다. | Communication between robot functions, manipulation planning, and mobile-robot navigation, respectively. |
| Gazebo · MuJoCo · Isaac Sim | 로봇과 물리 환경을 시뮬레이션합니다. 센서·동역학 모델이 실제 환경과의 차이를 만듭니다. | Robot and physical-environment simulation; sensor and dynamics models affect agreement with real systems. |
| PyTorch · TensorFlow · Keras · JAX | 텐서 연산과 자동미분·모델 학습을 구성하는 framework 생태계입니다. | Frameworks for tensor computation, automatic differentiation, and model training. |
| scikit-learn · XGBoost · LightGBM · CatBoost | 전통적인 머신러닝·gradient boosting 모델과 평가 흐름에 쓰입니다. | Traditional machine learning, gradient-boosting models, and evaluation workflows. |
| Transformers · Datasets · Tokenizers · Safetensors | 모델 인터페이스, 데이터 처리, token 변환, tensor 저장 형식을 제공합니다. | Model interfaces, dataset processing, token conversion, and tensor storage formats, respectively. |
| Lightning · fastai | 모델 학습 코드와 실행 흐름을 구성하는 상위 라이브러리입니다. | Higher-level libraries for organizing training code and execution. |
| CUDA · cuBLAS · cuDNN · CUTLASS | NVIDIA GPU 실행 플랫폼과 선형대수·신경망·행렬 연산 구성요소입니다. | The NVIDIA GPU execution platform and libraries/components for linear algebra, neural networks, and matrix computation. |
| Triton · Nsight Systems · Nsight Compute | GPU kernel 작성과 시스템·kernel 수준 성능 분석을 담당합니다. | GPU kernel development, system-wide profiling, and kernel-level profiling, respectively. |
| ROCm · HIP · SYCL · oneAPI · OpenCL · Metal | 여러 하드웨어와 운영 환경의 가속기 연산을 구성하는 생태계입니다. | Accelerator-computing ecosystems covering different hardware and operating environments. |
| TensorRT · OpenVINO · ONNX | 추론 최적화·실행과 모델 교환 표현을 담당합니다. 모델 형식과 실행기는 같은 개념이 아닙니다. | Inference optimization/execution and a model interchange representation. Model formats and runtimes have different roles. |
| LiteRT · TensorFlow Lite Micro · CMSIS-NN · ExecuTorch · TVM | 모바일·MCU·엣지 모델 실행과 변환·kernel·컴파일에 쓰입니다. | Model conversion, kernels, compilation, and execution for mobile, MCU, and edge devices. |
| PEFT · TRL · Accelerate · DeepSpeed · FSDP · DDP | Adapter 학습·후학습·장치 배치·분산 학습 상태와 통신을 다룹니다. | Adapter training, post-training, device placement, distributed training state, and communication. |
| MLflow · Weights & Biases · TensorBoard · Optuna | 실험의 parameter·metric·산출물 기록과 탐색을 담당합니다. | Tracking experiment parameters, metrics, and artifacts, and searching parameter configurations. |
| LangChain · LlamaIndex · DSPy · MCP | 모델 응용·검색·workflow 구성과 도구·자료 연결에 쓰입니다. | Model applications, retrieval, workflows, and connections to tools and data sources. |
| lm-evaluation-harness · Ragas · promptfoo | 언어 모델·RAG·prompt 응용의 평가와 회귀 확인에 쓰입니다. | Evaluation and regression checks for language models, RAG, and prompt-based applications. |
| OpenCV · Kornia · torchvision · timm · Detectron2 · MMDetection | 영상 연산·모델·학습·검출 구성요소를 제공합니다. | Image operations, model components, training, and object detection. |
| torchaudio · SentencePiece | 음성 처리와 tokenization 도구. 입력 표현이 이후 모델 계산과 연결됩니다. | Audio processing and tokenization; input representations determine what reaches the model. |
| HFSS · CST · ADS · AWR · Sonnet · openEMS · scikit-rf | 전자기장·RF 회로·network 데이터 해석에 쓰입니다. | Electromagnetic-field, RF-circuit, and network-data analysis. |
| GNU Radio · USRP | 소프트웨어 신호처리 블록을 실제 무선 송수신 장치와 연결하는 SDR 생태계입니다. | A software-defined-radio ecosystem connecting signal-processing blocks to physical transceiver hardware. |
| PLECS · PSIM | 스위칭 전력단과 제어의 시뮬레이션에 쓰입니다. | Simulation of switching power stages and their control systems. |
| PyVISA · SCPI · LabVIEW · NI-DAQ | 계측기 통신 명령, 장비 접근, 제어·수집 환경을 구성합니다. | Instrument commands, device access, control, and data-acquisition environments. |
| COMSOL · Ansys · OpenFOAM · FEniCS · MEEP · LAMMPS | 다물리·유체·유한요소·전자기·분자동역학 등 서로 다른 물리 문제를 풉니다. | Solvers for different physical problems, including multiphysics, fluid flow, finite elements, electromagnetics, and molecular dynamics. |
| SQLite · PostgreSQL · MySQL · DuckDB · Redis | 내장형·서버형·분석형·메모리형 등 데이터 저장과 질의 방식이 다른 시스템입니다. | Data storage and query systems spanning embedded, server-based, analytical, and in-memory designs. |
| Parquet · Arrow · Spark · Kafka · FAISS · pgvector | 저장·메모리 표현, 대규모 처리·이벤트 전달·벡터 검색을 구성합니다. | Storage/in-memory representations, large-scale processing, event transport, and vector search. |
| Kubernetes · Terraform · Prometheus · Grafana · OpenTelemetry | 배포·인프라 선언·수치 관측·시각화·trace를 구성합니다. | Deployment, declarative infrastructure, metrics, visualization, and tracing. |
| OpenMP · MPI · NCCL · Slurm · Ray · Dask | 공유 메모리·분산 통신·GPU 통신·작업 관리·분산 실행에 쓰입니다. | Shared-memory parallelism, distributed communication, GPU communication, job scheduling, and distributed execution. |
| pytest · unittest · GoogleTest · Catch2 · CTest · Hypothesis | 단위·통합·속성 기반 테스트의 작성과 실행에 쓰입니다. | Writing and running unit, integration, and property-based tests. |
| ASan · UBSan · TSan · Valgrind · clang-tidy · Ruff · CodeQL | 실행 중 오류와 정적 코드 문제를 찾는 진단·분석 도구입니다. | Runtime diagnostics and static analysis for detecting memory, concurrency, and code problems. |
| OpenGL · Vulkan · DirectX · WebGPU · GLSL · HLSL | 그래픽·GPU 연산 API와 shader 언어입니다. | Graphics/GPU-computing APIs and shader languages. |
| Blender · Mitsuba · PBRT · Unreal · Unity | 장면 제작·물리 렌더링·실시간 그래픽과 시뮬레이션에 쓰입니다. | Scene creation, physically based rendering, real-time graphics, and simulation. |
| Tessent · TestMAX · Modus | DFT와 제조 테스트의 구조·pattern 생성·분석에 관련된 도구입니다. | Tools for DFT structures, manufacturing-test pattern generation, and analysis. |
| FastAPI · Flask · Django · Node.js · Spring | 서버·API·웹 애플리케이션을 구성하는 서로 다른 생태계입니다. | Ecosystems for servers, APIs, and web applications. |
| React · Vue · Svelte · TypeScript | 웹 UI 구성과 코드의 정적 형식 검사에 쓰입니다. | Web UI development and static type checking. |
| Qt · PySide · Electron · Streamlit · Gradio | 데스크톱 UI와 데이터·모델용 화면을 구성합니다. | Desktop interfaces and UIs for data and model applications. |
| Kotlin · Java · Swift · Flutter · Dart · React Native · KMP | 모바일과 여러 플랫폼의 애플리케이션 코드를 구성합니다. | Languages and frameworks for mobile and cross-platform applications. |
| Quarto · Jekyll · Hugo · MkDocs · Sphinx · Doxygen · Jupyter Book | 글·계산 문서·사이트·API 문서를 생성합니다. | Generate articles, computational documents, sites, and API documentation. |
| GitHub Actions · GitLab CI · Python · Bash · PowerShell | 저장소 이벤트와 스크립트를 연결해 빌드·검사·문서 생성을 자동 실행합니다. | Connect repository events to scripts that automate builds, checks, and documentation generation. |
| Zotero · BibTeX · arXiv · IEEE Xplore · ACM DL · KIPRIS | 문헌을 검색하고 서지 정보·인용을 관리하는 경로와 도구입니다. | Sources and tools for finding literature and managing bibliographic records and citations. |

## 분야별 문서 · Topic documents

### [Linux & Bash](../분야_topics/01-linux-bash/README.md)

운영체제·셸·원격 접속·프로세스·파일 관리

Operating systems, shells, remote access, processes, and files

Ubuntu, Debian, Fedora, Arch Linux, WSL2, Bash, Zsh, systemd, SSH, tmux, rsync

### [Git & Development Tools](../분야_topics/02-개발도구_git-development-tools/README.md)

버전 관리·편집·컴파일·빌드·컨테이너

Version control, editing, compilation, builds, and containers

Git, GitHub, GitLab, GitHub CLI/Desktop, VS Code, Vim/Neovim, GCC, Clang/LLVM, Make, CMake, Meson, Ninja, Docker, Podman

### [Python & Jupyter](../분야_topics/03-python-jupyter/README.md)

Python 의존성·노트북·수치 배열·표·그래프

Python dependencies, notebooks, arrays, tables, and plots

Python, pip, uv, venv, Conda/Mamba, Jupyter Notebook/Lab, IPython, NumPy, SciPy, pandas, Matplotlib, Seaborn, Plotly

### [C, C++ & Python](../분야_topics/04-c-cpp-python/README.md)

언어·메모리 수명·자료구조·언어 연결

Languages, memory lifetime, data structures, and language interoperability

C, C++, Python, Rust, Go, Java, C#, JavaScript/TypeScript, Julia, R, Tcl, Lua, Assembly

### [MATLAB & Scientific Computing](../분야_topics/05-과학계산_matlab-scientific/README.md)

수치·기호 계산·동적 모델링

Numerical and symbolic computation, and dynamic modeling

MATLAB, Simulink, GNU Octave, SciPy, SymPy, Mathematica, Maple, Julia

### [수식을 코드로 · Math to Code](../분야_topics/06-수식과코드_math-to-code/README.md)

이산화·수치 해법·오차 분석

Discretization, numerical solvers, and error analysis

Calculus, Linear Algebra, Probability, Statistics, ODE/PDE, Numerical Analysis, Optimization, Information Theory, Graph Theory

### [컴퓨터공학 기초 · Computer Science Foundations](../분야_topics/07-컴퓨터공학기초_cs-foundations/README.md)

운영체제·자료구조·실행 모델

Operating systems, data structures, and execution models

Linux, xv6, OSTEP topics, Networking, TCP/IP, Filesystems, Databases, Compilers, Concurrency

### [알고리즘과 코딩테스트 · Problem Solving](../분야_topics/08-알고리즘_problem-solving/README.md)

알고리즘 문제·채점 환경

Algorithm problems and judging environments

Programmers, Baekjoon, LeetCode, Codeforces, AtCoder, HackerRank, Codility, SWEA

### [회로와 전자공학 · Circuits & Electronics](../분야_topics/09-회로전자공학_circuits-electronics/README.md)

소자·회로 모델·주파수 응답

Devices, circuit models, and frequency response

RLC, Op-Amp, BJT, MOSFET, CMOS, Filters, Oscillators, Regulators, SPICE, Breadboard Measurements

### [반도체 소자 · Semiconductor Devices](../분야_topics/10-반도체소자_semiconductors/README.md)

소자 물리·compact model·TCAD

Device physics, compact models, and TCAD

PN, MOS, BJT, CMOS, FinFET, GAA, SOI, SiC/GaN, BSIM, SRAM/DRAM/NAND, TCAD

### [Analog IC · Cadence · Spectre](../분야_topics/11-아날로그IC설계_analog-ic-cadence/README.md)

회로도·회로 시뮬레이션·레이아웃·검증

Schematics, circuit simulation, layout, and verification

Cadence Virtuoso, Spectre, ADE, SKILL, OCEAN, Synopsys Custom Compiler, HSPICE, PrimeSim, Siemens Eldo, LTspice, ngspice, Xschem

### [PCB & Hardware Design](../분야_topics/12-PCB하드웨어설계_pcb-hardware/README.md)

PCB 설계·제조 데이터·신호 해석

PCB design, manufacturing files, and signal analysis

KiCad, Altium Designer, OrCAD, Allegro, PADS, Xpedition, EasyEDA, IBIS, SI/PI, EMC/EMI, DFM

### [Verilog · SystemVerilog · RTL](../분야_topics/13-RTL설계_verilog-systemverilog/README.md)

회로 기술·하드웨어 생성

Hardware description and generation

Verilog, SystemVerilog, VHDL, Verilog-A/AMS, Chisel, SpinalHDL, Amaranth, HLS

### [Hardware Verification](../분야_topics/14-하드웨어검증_hardware-verification/README.md)

시뮬레이션·파형·assertion·formal

Simulation, waveforms, assertions, and formal verification

UVM, SVA, cocotb, Verilator, Icarus Verilog, GTKWave, Questa, Xcelium, VCS, SymbiYosys, Formal/Equivalence

### [FPGA & ASIC](../분야_topics/15-FPGA-ASIC설계_fpga-asic/README.md)

합성·배치배선·STA

Synthesis, placement and routing, and static timing analysis

AMD/Xilinx Vivado/Vitis, Intel/Altera Quartus, Lattice Radiant, Yosys, nextpnr, OpenROAD/OpenLane, Genus/Innovus, Design Compiler/Fusion Compiler, PrimeTime

### [Arm · RISC-V · Computer Architecture](../분야_topics/16-프로세서구조_arm-riscv/README.md)

ISA·CPU 구현·에뮬레이션

ISAs, CPU implementations, and emulation

Arm Cortex-M/A/R, RISC-V RV32/RV64, x86-64, MIPS, AVR, PicoRV32, Ibex, CVA6, Rocket Chip, BOOM, gem5, QEMU

### [Firmware & RTOS](../분야_topics/17-펌웨어-RTOS_firmware-rtos/README.md)

MCU·드라이버·실시간 실행

MCUs, drivers, and real-time execution

STM32, ESP32/ESP-IDF, Nordic nRF, NXP, TI, Microchip AVR/PIC/SAM, Renesas, RP2040/RP2350, FreeRTOS, Zephyr, ThreadX, RT-Thread

### [Embedded Linux](../분야_topics/18-임베디드Linux_embedded-linux/README.md)

부팅·배포판 빌드·보드 지원

Booting, distribution builds, and board support

Linux Kernel, U-Boot, Device Tree, Buildroot, Yocto/OpenEmbedded, BusyBox, QEMU, BSP, Drivers

### [OpenOCD · GDB · Debugging](../분야_topics/19-시스템디버깅_openocd-debugging/README.md)

디버거·프로브·trace·파형 관찰

Debuggers, probes, trace, and waveform observation

OpenOCD, GDB, LLDB, J-Link, ST-Link, pyOCD, probe-rs, JTAG, SWD, SWO, ETM, Saleae, PulseView, Sigrok

### [Interfaces & Communications](../분야_topics/20-인터페이스통신_interfaces-communications/README.md)

보드·장치·온칩·네트워크 연결

Board, device, on-chip, and network connections

UART, SPI, I2C, I3C, CAN/CAN-FD, USB, Ethernet, PCIe, MIPI, DDR, AXI/AHB/APB, MQTT, Modbus, BLE, Wi-Fi, Zigbee, LoRa

### [신호처리와 제어 · Signals, DSP & Control](../분야_topics/21-신호처리제어_signals-control/README.md)

필터·상태 추정·제어

Filters, state estimation, and control

FFT, FIR/IIR, PID, State Space, LQR/LQG, MPC, Kalman/EKF/UKF, System Identification, SciPy Signal, MATLAB Control

### [Robotics · Arduino · Raspberry Pi](../분야_topics/22-로봇제어_robotics-boards/README.md)

보드·센서·로봇 통신·계획·시뮬레이션

Boards, sensors, robot communication, planning, and simulation

Arduino, Raspberry Pi, STM32 Nucleo, ESP32, BeagleBone, Jetson, ROS 2, MoveIt, Nav2, Gazebo, MuJoCo, Isaac Sim, SLAM

### [AI · Machine Learning · Deep Learning](../분야_topics/23-AI머신러닝_ai-machine-learning/README.md)

모델 구성·학습·자동미분

Model construction, training, and automatic differentiation

PyTorch, TensorFlow/Keras, JAX, scikit-learn, XGBoost, LightGBM, CatBoost, Hugging Face, Lightning, fastai

### [GPU Architecture](../분야_topics/24-GPU구조_gpu-architecture/README.md)

실행 자원·GPU 메모리·그래픽 API

Execution resources, GPU memory, and graphics APIs

NVIDIA, AMD, Intel, Apple GPU, SIMT/SIMD, Cache/VRAM, HBM/GDDR, PCIe/NVLink, Roofline, Vulkan, OpenGL, DirectX

### [CUDA & GPU Optimization](../분야_topics/25-CUDA성능최적화_cuda-performance/README.md)

GPU 연산·라이브러리·profiling

GPU computation, libraries, and profiling

CUDA, cuBLAS, cuDNN, CUTLASS, Triton, Nsight, ROCm/HIP, SYCL/oneAPI, OpenCL, Metal, OpenMP/OpenACC, TensorRT, OpenVINO

### [AI Models & APIs](../분야_topics/26-AI모델-API_open-model-lab/README.md)

모델 배포·가중치·API·runtime

Model distribution, weights, APIs, and runtimes

OpenAI, Google/DeepMind, Microsoft, Meta, Anthropic, Samsung, DeepSeek, Qwen, Mistral, IBM, NVIDIA, LG, NAVER, Kakao, Upstage, SKT

### [논문 · 코드 · 특허 · Paper, Code & Patent Reviews](../분야_topics/27-논문코드특허_papers-code-patents/README.md)

문헌 검색·코드·서지 관리

Literature searches, source code, and reference management

arXiv, IEEE, ACM, NeurIPS, ICML, ICLR, CVPR, ISSCC, DAC, DATE, KIPRIS, Google Patents, Zotero, BibTeX

### [자동화와 기술 기록 · Automation & Portfolio](../분야_topics/28-자동화기술기록_automation-portfolio/README.md)

스크립트·CI·문서 생성

Scripts, CI, and documentation generation

Python, Bash, PowerShell, GitHub Actions, GitLab CI, Docker, Quarto, Jekyll, Hugo, MkDocs, Sphinx, Doxygen, Jupyter Book

### [전자기학 · RF · 안테나 · Electromagnetics, RF & Antennas](../분야_topics/29-전자기학-RF_electromagnetics-rf/README.md)

전자기장·RF 회로·S-parameter

Electromagnetic fields, RF circuits, and S-parameters

HFSS, CST, ADS, AWR, Sonnet, openEMS, scikit-rf, VNA, Spectrum Analyzer

### [통신이론과 무선 시스템 · Communication Systems & Information Theory](../분야_topics/30-통신이론무선시스템_communications-wireless/README.md)

신호처리 블록·SDR

Signal-processing blocks and software-defined radio

GNU Radio, SDR, USRP, RTL-SDR, OFDM, QAM, MIMO, LDPC, Polar Codes

### [전력전자와 에너지 · Power Electronics & Energy](../분야_topics/31-전력전자에너지_power-energy/README.md)

전력단·제어 시뮬레이션

Power-stage and control simulation

PLECS, PSIM, LTspice, Simulink, Buck/Boost, LLC, BMS, PMIC

### [Mixed-Signal · ADC · DAC · Clock](../분야_topics/32-혼성신호-ADC-DAC_mixed-signal-data-converters/README.md)

변환기·클록·정적·동적 지표

Data converters, clocks, and static and dynamic metrics

SAR ADC, Delta-Sigma, DAC, PLL, DLL, CDR, Spectre, Verilog-AMS

### [Memory & Storage](../분야_topics/33-메모리저장장치_memory-storage/README.md)

메모리·저장 프로토콜·I/O 측정

Memory, storage protocols, and I/O measurement

SRAM, DRAM, NAND, DDR, LPDDR, GDDR, HBM, NVMe, fio, CXL

### [SoC & Interconnects](../분야_topics/34-SoC연결구조_soc-interconnects/README.md)

주소·버스·일관성

Addressing, buses, and coherence

AXI, AMBA, TileLink, Wishbone, NoC, PCIe, CXL, Chiplet, CHI

### [EDA & Open Hardware](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/README.md)

PDK·표준 셀·공개 EDA 흐름

PDKs, standard cells, and open EDA flows

Cadence, Synopsys, Siemens EDA, Yosys, OpenROAD, OpenLane, KLayout, Magic, Netgen, SKY130, GF180, IHP SG13G2

### [Packaging · Chiplets · Thermal](../분야_topics/36-패키징열설계_packaging-thermal/README.md)

전기·열·구조 모델

Electrical, thermal, and structural models

Chiplets, UCIe, 2.5D/3D IC, Interposer, COMSOL, Ansys, Thermal RC, EM/IR

### [센서와 계측 · Sensors, Instrumentation & Experiments](../분야_topics/37-센서계측_sensors-instrumentation/README.md)

계측 명령·장비 연결·데이터 수집

Instrument commands, device connections, and data acquisition

SCPI, PyVISA, Sigrok, PulseView, LabVIEW, NI DAQ, Oscilloscope, VNA

### [Security · Cryptography · Hardware Trust](../분야_topics/38-보안암호하드웨어신뢰_security-cryptography/README.md)

암호·부팅 신뢰·코드 진단

Cryptography, boot trust, and code diagnostics

TLS, AES, RSA, ECC, Secure Boot, TrustZone, TPM, Sanitizers, Fuzzing, CodeQL

### [Compilers · Languages · Runtimes](../분야_topics/39-컴파일러언어런타임_compilers-languages/README.md)

frontend·IR·코드 생성·runtime

Frontends, intermediate representations, code generation, and runtimes

LLVM, MLIR, GCC, Clang, Rust, Go, Java/JVM, CPython, Julia, Tcl, SKILL

### [Databases & Data Engineering](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/README.md)

질의·저장 형식·stream·검색

Queries, storage formats, streams, and search

SQLite, PostgreSQL, MySQL, DuckDB, Redis, Parquet, Arrow, Spark, Kafka, FAISS, pgvector

### [Cloud & Distributed Systems](../분야_topics/41-클라우드분산시스템_cloud-distributed/README.md)

인프라·배포·관측

Infrastructure, deployment, and observability

AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Prometheus, Grafana, OpenTelemetry

### [HPC & Parallel Computing](../분야_topics/42-고성능병렬계산_hpc-parallel/README.md)

병렬화·통신·작업 관리

Parallel execution, communication, and job management

OpenMP, MPI, OpenACC, SIMD, AVX/NEON, NCCL, Slurm, Ray, Dask, perf

### [Computer Vision](../분야_topics/43-컴퓨터비전_computer-vision/README.md)

영상 연산·모델·기하

Image operations, models, and geometry

OpenCV, torchvision, timm, ResNet, ViT, YOLO, SAM, DINO, Detectron2, MMDetection, Kornia

### [Language · Speech · Multimodal AI](../분야_topics/44-언어음성멀티모달AI_language-speech-multimodal/README.md)

token·언어·음성·시각 표현

Tokens, language, speech, and visual representations

BERT, T5, GPT, Whisper, wav2vec, CLIP, LLaVA, Transformers, torchaudio, SentencePiece

### [AI Training & Optimization](../분야_topics/45-AI학습최적화_ai-training-optimization/README.md)

분산 학습·adapter·양자화·실험 관리

Distributed training, adapters, quantization, and experiment tracking

PEFT, TRL, Accelerate, DeepSpeed, FSDP, DDP, MLflow, W&B, TensorBoard, Optuna, bitsandbytes

### [AI Applications · Agents · Evaluation](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/README.md)

도구 연결·검색·workflow·평가

Tool integration, retrieval, workflows, and evaluation

OpenAI APIs, Claude API, Gemini API, LangChain, LlamaIndex, DSPy, MCP, lm-evaluation-harness, Ragas, promptfoo

### [Edge AI · TinyML · NPU](../분야_topics/47-엣지AI-TinyML_edge-tinyml/README.md)

모델 변환·장치 추론

Model conversion and on-device inference

ONNX Runtime, TensorRT, OpenVINO, LiteRT/TFLite, TFLite Micro, CMSIS-NN, ExecuTorch, TVM, Jetson, Coral

### [Software Design & Quality](../분야_topics/48-소프트웨어설계품질_software-quality/README.md)

테스트·정적 분석·메모리 진단

Testing, static analysis, and memory diagnostics

pytest, unittest, GoogleTest, Catch2, CTest, Hypothesis, Valgrind, ASan/UBSan/TSan, clang-tidy, Ruff

### [Graphics & Rendering](../분야_topics/49-그래픽스렌더링_graphics-simulation/README.md)

shader·장면·렌더링

Shaders, scenes, and rendering

OpenGL, Vulkan, DirectX, WebGPU, GLSL, HLSL, Blender, Mitsuba, PBRT, Unreal, Unity

### [물리·과학 시뮬레이션 · Physics, Multiphysics & Scientific Simulation](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/README.md)

방정식·mesh·수치 해법

Equations, meshes, and numerical solvers

COMSOL, Ansys, HFSS, CST, OpenFOAM, FEniCS, MEEP, openEMS, LAMMPS

### [DFT · Test · Manufacturing](../분야_topics/51-반도체테스트제조_test-manufacturing/README.md)

테스트 접근·pattern·제조 검사

Test access, patterns, and manufacturing checks

DFT, Scan, ATPG, MBIST/LBIST, ATE, JTAG/Boundary Scan, Tessent, TestMAX, Modus

### [Web · API · Applications](../분야_topics/52-Web-API응용_web-api-applications/README.md)

서버·API·UI·dashboard

Servers, APIs, UIs, and dashboards

FastAPI, Flask, Django, Node.js, Spring, React, Vue, Svelte, TypeScript, Qt/PySide, Electron, Streamlit, Gradio

### [Mobile & Cross-Platform](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/README.md)

모바일 UI·장치 연결·추론

Mobile UIs, device integration, and inference

Kotlin, Java, Android, Swift, iOS, Flutter, Dart, React Native, Kotlin Multiplatform, Core ML

### [새로운 소자와 컴퓨팅 · Research Frontiers](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/README.md)

소자·새로운 연산 구조

Devices and new computing architectures

SNN, Neuromorphic, Event Camera, Quantum, Photonics, Compute-in-Memory, Memristor, Wearables

### [지원 · 시험 · 면접 · Applications, Resumes & Assessment Experiences](../소개_about/지원기록_APPLICATIONS.md)

문서·평가·지원 과정

Documents, assessments, and application processes

Kookmin University, Company Applications, Resume/CV, Coding Tests, Competency Assessments

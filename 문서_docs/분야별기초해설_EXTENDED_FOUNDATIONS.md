# 분야별 기초 해설 | Technical foundations by topic

[전체 목차](../분야별목차_CATALOG.md) · [수학·물리와 공학 기초](공학기초_FOUNDATIONS.md) · [문서별 출처](확장출처_EXTENDED_SOURCES.json)

개발 환경과 소프트웨어, 회로와 하드웨어, GPU와 AI를 연결하는 기초 해설 36편이다. 각 글은 개념과 용도를 설명하고, 필요한 수식의 전제와 유도, 참조 구현, 독립 검증을 연결한다. 수학식이 중심이 아닌 주제에서는 상태·불변식·실행 순서로 동작을 설명한다.

아래 표에서 한국어 본문을 열고, 각 글의 English 절에서 같은 내용을 영어로 읽을 수 있다. 수치 예제의 가정과 검증 범위는 결과와 함께 적었다. 실제 보드·전용 도구에서 확인하는 절차는 참조 모델의 자동 검사와 구분해 설명한다.

These 36 foundation articles connect development environments, software, circuits, hardware, GPUs and AI. Each links concepts and applications with assumptions and derivations, reference implementations and independent checks. State, invariants and execution order explain topics where equations are not the central tool.

Each link opens the Korean explanation followed by an equivalent English section. Numerical assumptions and verification scope accompany the results. Procedures for physical boards and specialized tools are distinguished from automated reference-model checks.

## 개발 환경·시스템·소프트웨어 | Environments, systems and software

| 분야 / Area | 해설 / Article |
| --- | --- |
| Linux·Bash<br>Linux & Bash | [Linux에서 프로그램, 권한과 파이프가 만나는 곳](../분야_topics/01-linux-bash/해설_notes/Linux에서프로그램권한과파이프가만나_processes-permissions-pipelines.md) · [English](../분야_topics/01-linux-bash/해설_notes/Linux에서프로그램권한과파이프가만나_processes-permissions-pipelines.md#english) |
| Git과 개발 도구<br>Git & Development Tools | [Git 이력과 다시 만들 수 있는 결과물](../분야_topics/02-개발도구_git-development-tools/해설_notes/Git이력과다시만들수있는결과물_commit-dag-reproducible-builds.md) · [English](../분야_topics/02-개발도구_git-development-tools/해설_notes/Git이력과다시만들수있는결과물_commit-dag-reproducible-builds.md#english) |
| Python·Jupyter<br>Python & Jupyter Environments | [Python 환경과 Jupyter 실행 상태를 구분하기](../분야_topics/03-python-jupyter/해설_notes/Python환경과Jupyter실행상태_environments-kernel-state-reproducibility.md) · [English](../분야_topics/03-python-jupyter/해설_notes/Python환경과Jupyter실행상태_environments-kernel-state-reproducibility.md#english) |
| MATLAB과 과학 계산<br>MATLAB & Scientific Computing | [MATLAB 수치해석: 답의 오차와 잔차는 왜 다를까](../분야_topics/05-과학계산_matlab-scientific/해설_notes/MATLAB수치해석_linear-solves-conditioning-residuals.md) · [English](../분야_topics/05-과학계산_matlab-scientific/해설_notes/MATLAB수치해석_linear-solves-conditioning-residuals.md#english) |
| 알고리즘과 문제 해결<br>Problem Solving | [복잡도와 자료구조: heap으로 최단 경로 찾기](../분야_topics/08-알고리즘_problem-solving/해설_notes/복잡도와자료구조_complexity-heaps-shortest-paths.md) · [English](../분야_topics/08-알고리즘_problem-solving/해설_notes/복잡도와자료구조_complexity-heaps-shortest-paths.md#english) |
| 임베디드 Linux<br>Embedded Linux | [Embedded Linux: 부팅, Device Tree와 드라이버의 경계](../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/boot-devicetree-driver-boundaries.md) · [English](../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/boot-devicetree-driver-boundaries.md#english) |
| OpenOCD·GDB와 시스템 디버깅<br>OpenOCD, GDB & Instrumentation | [OpenOCD와 GDB: 연결, 정지 상태와 관찰의 의미](../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/OpenOCD와GDB_debug-transport-state-observation.md) · [English](../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/OpenOCD와GDB_debug-transport-state-observation.md#english) |
| 로봇 제어·Arduino·Raspberry Pi<br>Robotics, Arduino & Raspberry Pi | [차동구동 로봇: 바퀴 회전에서 위치 추정까지](../분야_topics/22-로봇제어_robotics-boards/해설_notes/차동구동로봇_differential-drive-kinematics-odometry.md) · [English](../분야_topics/22-로봇제어_robotics-boards/해설_notes/차동구동로봇_differential-drive-kinematics-odometry.md#english) |
| 논문·코드·특허<br>Paper, Code & Patent Reviews | [논문·코드·특허 읽기: 주장과 재현 근거를 연결하기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md) · [English](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md#english) |
| 자동화와 기술 기록<br>Automation & Portfolio | [자동화의 기본: 검증, 재실행과 원자적 게시](../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/자동화의기본_ci-idempotency-atomic-publication.md) · [English](../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/자동화의기본_ci-idempotency-atomic-publication.md#english) |
| 소프트웨어 설계와 품질<br>Software Quality, Design & Testing | [소프트웨어 검증: 예제, 계약과 변환 성질](../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/소프트웨어검증_contracts-properties-metamorphic-testing.md) · [English](../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/소프트웨어검증_contracts-properties-metamorphic-testing.md#english) |
| 모바일과 크로스플랫폼<br>Mobile, Cross-Platform & Device Integration | [모바일 UI 상태: 생명주기와 늦게 도착한 결과](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/모바일UI상태_ui-state-lifecycle-stale-results.md) · [English](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/모바일UI상태_ui-state-lifecycle-stale-results.md#english) |

## 회로·하드웨어·통신 | Circuits, hardware and communications

| 분야 / Area | 해설 / Article |
| --- | --- |
| 아날로그 IC 설계·Cadence·Spectre<br>Analog IC Design: Cadence & Spectre | [동작점에서 주파수 응답까지: 소신호와 AC 해석](../분야_topics/11-아날로그IC설계_analog-ic-cadence/해설_notes/동작점에서주파수응답까지_small-signal-ac-operating-point.md) · [English](../분야_topics/11-아날로그IC설계_analog-ic-cadence/해설_notes/동작점에서주파수응답까지_small-signal-ac-operating-point.md#english) |
| PCB와 하드웨어 설계<br>PCB & Hardware Design | [전원은 배선까지 포함한다: PDN, decoupling과 귀환 전류](../분야_topics/12-PCB하드웨어설계_pcb-hardware/해설_notes/전원은배선까지포함한다_pdn-decoupling-return-current.md) · [English](../분야_topics/12-PCB하드웨어설계_pcb-hardware/해설_notes/전원은배선까지포함한다_pdn-decoupling-return-current.md#english) |
| 하드웨어 검증<br>Hardware Verification | [검증에서 무엇을 확인했는가: assertion, coverage와 formal](../분야_topics/14-하드웨어검증_hardware-verification/해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md) · [English](../분야_topics/14-하드웨어검증_hardware-verification/해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md#english) |
| FPGA·ASIC 설계<br>FPGA & ASIC Design | [너무 늦어도, 너무 빨라도 문제다: setup·hold와 STA](../분야_topics/15-FPGA-ASIC설계_fpga-asic/해설_notes/너무늦어도너무빨라도문제다_setup-hold-static-timing.md) · [English](../분야_topics/15-FPGA-ASIC설계_fpga-asic/해설_notes/너무늦어도너무빨라도문제다_setup-hold-static-timing.md#english) |
| Arm·RISC-V와 프로세서 구조<br>Arm, RISC-V & Computer Architecture | [명령어가 보는 메모리: ISA, byte 순서와 load/store](../분야_topics/16-프로세서구조_arm-riscv/해설_notes/명령어가보는메모리_isa-byte-order-load-store.md) · [English](../분야_topics/16-프로세서구조_arm-riscv/해설_notes/명령어가보는메모리_isa-byte-order-load-store.md#english) |
| 통신이론과 무선 시스템<br>Communication Systems & Information Theory | [잡음 속에서 bit를 고르기: BPSK, Eb/N0와 BER](../분야_topics/30-통신이론무선시스템_communications-wireless/해설_notes/잡음속에서bit를고르기_bpsk-awgn-ber.md) · [English](../분야_topics/30-통신이론무선시스템_communications-wireless/해설_notes/잡음속에서bit를고르기_bpsk-awgn-ber.md#english) |
| 전력전자와 에너지<br>Power Electronics & Energy | [스위칭으로 낮은 전압 만들기: buck의 CCM과 ripple](../분야_topics/31-전력전자에너지_power-energy/해설_notes/스위칭으로낮은전압만들기_buck-ccm-ripple.md) · [English](../분야_topics/31-전력전자에너지_power-energy/해설_notes/스위칭으로낮은전압만들기_buck-ccm-ripple.md#english) |
| SoC와 연결 구조<br>SoC & Interconnects | [준비된 순간에만 옮기기: ready/valid와 backpressure](../분야_topics/34-SoC연결구조_soc-interconnects/해설_notes/준비된순간에만옮기기_ready-valid-backpressure.md) · [English](../분야_topics/34-SoC연결구조_soc-interconnects/해설_notes/준비된순간에만옮기기_ready-valid-backpressure.md#english) |
| EDA와 오픈 하드웨어<br>EDA & Open Hardware Ecosystems | [RTL에서 layout까지: 서로 다른 검증을 연결하는 EDA 흐름](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/RTL에서layout까지_rtl-netlist-timing-physical-checks.md) · [English](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/RTL에서layout까지_rtl-netlist-timing-physical-checks.md#english) |
| 패키징·Chiplet·열 설계<br>Packaging, Chiplets, Thermal & Reliability | [열은 바로 빠져나가지 않는다: thermal RC와 과도 온도](../분야_topics/36-패키징열설계_packaging-thermal/해설_notes/열은바로빠져나가지않는다_thermal-rc-steady-transient.md) · [English](../분야_topics/36-패키징열설계_packaging-thermal/해설_notes/열은바로빠져나가지않는다_thermal-rc-steady-transient.md#english) |
| DFT·반도체 테스트·제조<br>DFT, Semiconductor Test & Manufacturing | [보이지 않는 내부 상태를 검사하기: scan, ATPG와 fault coverage](../분야_topics/51-반도체테스트제조_test-manufacturing/해설_notes/보이지않는내부상태를검사하기_scan-atpg-fault-coverage.md) · [English](../분야_topics/51-반도체테스트제조_test-manufacturing/해설_notes/보이지않는내부상태를검사하기_scan-atpg-fault-coverage.md#english) |
| 차세대 소자와 컴퓨팅<br>Research Frontiers | [전류의 합으로 내적 계산하기: memristive PIM과 비이상성](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/해설_notes/전류의합으로내적계산하기_memristive-pim-dot-products.md) · [English](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/해설_notes/전류의합으로내적계산하기_memristive-pim-dot-products.md#english) |

## GPU·AI·데이터·응용 | GPUs, AI, data and applications

| 분야 / Area | 해설 / Article |
| --- | --- |
| GPU 구조<br>GPU Architecture | [GPU의 warp, 메모리 접근, occupancy](../분야_topics/24-GPU구조_gpu-architecture/해설_notes/GPU의warp메모리접근occupan_warp-memory-occupancy.md) · [English](../분야_topics/24-GPU구조_gpu-architecture/해설_notes/GPU의warp메모리접근occupan_warp-memory-occupancy.md#english) |
| AI 모델과 API<br>AI Providers, Public Models & APIs | [모델 파일에서 다음 토큰까지: 가중치, 토큰화, sampling](../분야_topics/26-AI모델-API_open-model-lab/해설_notes/모델파일에서다음토큰까지_weights-tokenizers-and-sampling.md) · [English](../분야_topics/26-AI모델-API_open-model-lab/해설_notes/모델파일에서다음토큰까지_weights-tokenizers-and-sampling.md#english) |
| 데이터베이스와 데이터 공학<br>Databases & Data Engineering | [DB의 인덱스, 트랜잭션, SQL 집계](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/DB의인덱스트랜잭션SQL집계_indexes-transactions-and-aggregation.md) · [English](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/DB의인덱스트랜잭션SQL집계_indexes-transactions-and-aggregation.md#english) |
| 클라우드와 분산 시스템<br>Cloud, Distributed Systems & Operations | [복제본의 교집합: quorum과 일관성의 조건](../분야_topics/41-클라우드분산시스템_cloud-distributed/해설_notes/복제본의교집합_quorums-failures-and-consistency.md) · [English](../분야_topics/41-클라우드분산시스템_cloud-distributed/해설_notes/복제본의교집합_quorums-failures-and-consistency.md#english) |
| 고성능·병렬 계산<br>HPC, Parallel & Distributed Computing | [병렬 계산의 분할, reduction, 통신 비용](../분야_topics/42-고성능병렬계산_hpc-parallel/해설_notes/병렬계산의분할reduction통신비용_partition-reduction-and-communication.md) · [English](../분야_topics/42-고성능병렬계산_hpc-parallel/해설_notes/병렬계산의분할reduction통신비용_partition-reduction-and-communication.md#english) |
| 컴퓨터 비전과 영상 처리<br>Computer Vision & Image Processing | [카메라 모델, 영상 필터, CV 검증](../분야_topics/43-컴퓨터비전_computer-vision/해설_notes/카메라모델영상필터CV검증_camera-filtering-and-validation.md) · [English](../분야_topics/43-컴퓨터비전_computer-vision/해설_notes/카메라모델영상필터CV검증_camera-filtering-and-validation.md#english) |
| AI 학습과 최적화<br>AI Training, Optimization & Compression | [학습의 계산과 평가: loss, batch, 학습률, data leakage](../분야_topics/45-AI학습최적화_ai-training-optimization/해설_notes/학습의계산과평가_loss-batches-schedules-and-leakage.md) · [English](../분야_topics/45-AI학습최적화_ai-training-optimization/해설_notes/학습의계산과평가_loss-batches-schedules-and-leakage.md#english) |
| AI 응용·에이전트·평가<br>AI Applications, Agents & Evaluation | [RAG와 도구 실행: 검색, 근거, 평가의 경계](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md) · [English](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md#english) |
| 엣지 AI·TinyML·NPU<br>Edge AI, TinyML & NPUs | [정수 양자화: scale, zero-point, 배포 오차](../분야_topics/47-엣지AI-TinyML_edge-tinyml/해설_notes/정수양자화_integer-quantization-and-deployment-error.md) · [English](../분야_topics/47-엣지AI-TinyML_edge-tinyml/해설_notes/정수양자화_integer-quantization-and-deployment-error.md#english) |
| 그래픽스와 렌더링<br>Computer Graphics, Rendering & Simulation | [좌표 변환에서 pixel까지: 동차 좌표와 rasterization](../분야_topics/49-그래픽스렌더링_graphics-simulation/해설_notes/좌표변환에서pixel까지_transforms-projection-and-rasterization.md) · [English](../분야_topics/49-그래픽스렌더링_graphics-simulation/해설_notes/좌표변환에서pixel까지_transforms-projection-and-rasterization.md#english) |
| 물리·과학 시뮬레이션<br>Physics, Multiphysics & Scientific Simulation | [수치해석의 V&V: 수렴, 잔차, 보존을 따로 확인하기](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/해설_notes/수치해석의VV_verification-convergence-and-conservation.md) · [English](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/해설_notes/수치해석의VV_verification-convergence-and-conservation.md#english) |
| Web·API·응용 프로그램<br>Web, APIs & Desktop Applications | [HTTP API의 계약: 멱등성, pagination, 입력 검증](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/HTTPAPI의계약_http-idempotency-pagination-validation.md) · [English](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/HTTPAPI의계약_http-idempotency-pagination-validation.md#english) |

## 구현과 검증 | Implementation and verification

[확장 예제와 실행 방법](../예제_examples/확장기초_extended/README.md)에서 하드웨어, 시스템, AI·데이터 모델의 구현과 검산을 확인할 수 있다. 도식과 도표의 표기 방식은 [편집 기준](도식편집기준_FIGURE_STYLE.md)에 정리했다.

The [extended examples](../예제_examples/확장기초_extended/README.md) provide implementations and independent checks for hardware, systems, and AI/data models. [The figure-style guide](도식편집기준_FIGURE_STYLE.md) records visual conventions.

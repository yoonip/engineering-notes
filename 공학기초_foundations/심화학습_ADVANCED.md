# 심화 해설과 구현 | Advanced explanations and implementations

[전체 목차](../분야별목차_CATALOG.md) · [기초 해설](분야별학습_TOPIC_GUIDES.md) · [심화 실행 예제](../예제_examples/심화_advanced/README.md) · [문서별 출처](../참고자료_references/심화출처_ADVANCED_SOURCES.md)

기초 개념에서 한 걸음 더 들어가, 계산식이 나오는 과정과 실행 가능한 구현을 연결한 60편입니다. 회로의 노드 방정식, RTL의 수 표현, RTOS 자원 대기, 학습의 역전파처럼 분야마다 중요한 동작을 직접 계산합니다.

각 글은 한국어 설명 뒤에 같은 내용을 영어로 담습니다. 수식은 가정과 중간 단계를 함께 적고, 코드에는 독립적인 기준 계산·경계 조건·불변식 검사를 연결했습니다. 상태 전이가 중심인 주제는 수식 대신 실행 순서와 반례를 따라갑니다.

실행 명령과 입력은 본문과 예제 README에서 확인할 수 있습니다. 수치 모델의 검사와 실제 도구 실행은 결과 기록에 구분했습니다. 새 도표는 이 저장소의 계산 결과에서 생성하며, PNG와 편집 가능한 SVG·생성 코드를 함께 제공합니다.

## English

These 60 advanced articles connect step-by-step reasoning with executable implementations: nodal circuit equations, fixed-point RTL, RTOS resource dependencies, backpropagation and more. Each Korean explanation is followed by an equivalent English section.

Derivations state assumptions and intermediate steps. Independent calculations, boundary cases and invariants check the implementations. State-oriented topics use transitions and counterexamples where equations alone would not explain the behavior.

Commands and inputs appear in the articles and example READMEs. Verification records distinguish computational models from actual tool execution. New plots are generated from the repository calculations and include PNGs, editable SVGs and generation code.

## 개발 환경·소프트웨어 | Environments and software

| 분야 / Area | 심화 해설 / Advanced article |
| --- | --- |
| 01 Linux·Bash<br>Linux & Bash | [파이프가 꽉 찼을 때: backpressure와 종료 조건](../분야_topics/01-linux-bash/해설_notes/파이프역압력_pipe-backpressure.md) · [English](../분야_topics/01-linux-bash/해설_notes/파이프역압력_pipe-backpressure.md#english) |
| 02 Git과 개발 도구<br>Git & Development Tools | [바뀐 입력만 다시 만들기: 내용 기반 빌드와 캐시](../분야_topics/02-개발도구_git-development-tools/해설_notes/내용기반빌드_content-addressed-build.md) · [English](../분야_topics/02-개발도구_git-development-tools/해설_notes/내용기반빌드_content-addressed-build.md#english) |
| 03 Python·Jupyter<br>Python & Jupyter Environments | [노트북 결과를 다시 얻으려면: 데이터와 분할의 재현성](../분야_topics/03-python-jupyter/해설_notes/데이터와분할재현성_data-split-reproducibility.md) · [English](../분야_topics/03-python-jupyter/해설_notes/데이터와분할재현성_data-split-reproducibility.md#english) |
| 04 C·C++·Python<br>C, C++ & Python | [C의 고정 크기 ring buffer: 경계와 소유권부터](../분야_topics/04-c-cpp-python/해설_notes/고정크기링버퍼_bounded-ring-buffer.md) · [English](../분야_topics/04-c-cpp-python/해설_notes/고정크기링버퍼_bounded-ring-buffer.md#english) |
| 05 MATLAB과 과학 계산<br>MATLAB & Scientific Computing | [비선형 방정식: 빠른 Newton과 안전한 구간 좁히기](../분야_topics/05-과학계산_matlab-scientific/해설_notes/구간을지키는근찾기_safeguarded-root-finding.md) · [English](../분야_topics/05-과학계산_matlab-scientific/해설_notes/구간을지키는근찾기_safeguarded-root-finding.md#english) |
| 07 컴퓨터공학 기초<br>Computer Science Foundations | [같은 계산, 다른 메모리 배치: AoS·SoA와 캐시](../분야_topics/07-컴퓨터공학기초_cs-foundations/해설_notes/배치와캐시_memory-layout-locality.md) · [English](../분야_topics/07-컴퓨터공학기초_cs-foundations/해설_notes/배치와캐시_memory-layout-locality.md#english) |
| 08 알고리즘과 문제 해결<br>Problem Solving | [A*: 좋은 예상값으로 탐색을 줄이고 정답은 지키기](../분야_topics/08-알고리즘_problem-solving/해설_notes/휴리스틱최단경로_astar-reopening.md) · [English](../분야_topics/08-알고리즘_problem-solving/해설_notes/휴리스틱최단경로_astar-reopening.md#english) |
| 27 논문·코드·특허<br>Paper, Code & Patent Reviews | [재현 실험 설계: 같은 조건에서 차이를 비교하기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md) · [English](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md#english) |
| 28 자동화와 기술 기록<br>Automation & Portfolio | [CI를 줄여도 검증은 빠뜨리지 않기: 변경 영향과 캐시](../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/변경영향과CI캐시_incremental-ci-cache.md) · [English](../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/변경영향과CI캐시_incremental-ci-cache.md#english) |
| 38 보안·암호·하드웨어 신뢰<br>Security, Cryptography & Hardware Trust | [인증된 메시지도 다시 올 수 있다: replay window](../분야_topics/38-보안암호하드웨어신뢰_security-cryptography/해설_notes/인증후재전송검사_authenticated-replay-window.md) · [English](../분야_topics/38-보안암호하드웨어신뢰_security-cryptography/해설_notes/인증후재전송검사_authenticated-replay-window.md#english) |
| 39 컴파일러·언어·런타임<br>Compilers, Languages & Runtimes | [작은 수식 언어 만들기: 우선순위에서 stack bytecode까지](../분야_topics/39-컴파일러언어런타임_compilers-languages/해설_notes/수식에서바이트코드_expression-bytecode.md) · [English](../분야_topics/39-컴파일러언어런타임_compilers-languages/해설_notes/수식에서바이트코드_expression-bytecode.md#english) |
| 48 소프트웨어 설계와 품질<br>Software Quality, Design & Testing | [테스트가 실패한 뒤: 재현 가능한 반례와 shrinking](../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/실패입력줄이기_property-counterexample-shrinking.md) · [English](../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/실패입력줄이기_property-counterexample-shrinking.md#english) |
| 52 Web·API·응용 프로그램<br>Web, APIs & Desktop Applications | [두 사용자의 수정이 겹치면: ETag와 조건부 갱신](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/버전조건부갱신_optimistic-concurrency-etag.md) · [English](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/버전조건부갱신_optimistic-concurrency-etag.md#english) |
| 53 모바일과 크로스플랫폼<br>Mobile, Cross-Platform & Device Integration | [UI 상태를 한곳에서 바꾸기: reducer와 비동기 효과](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/UI이벤트리듀서_ui-event-reducer.md) · [English](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/UI이벤트리듀서_ui-event-reducer.md#english) |

## 회로·반도체·하드웨어 | Circuits, semiconductors and hardware

| 분야 / Area | 심화 해설 / Advanced article |
| --- | --- |
| 09 회로와 전자공학<br>Circuits & Electronics | [회로를 행렬로 풀기: Modified Nodal Analysis](../분야_topics/09-회로전자공학_circuits-electronics/해설_notes/회로를행렬로풀기_mna.md) · [English](../분야_topics/09-회로전자공학_circuits-electronics/해설_notes/회로를행렬로풀기_mna.md#english) |
| 10 반도체 소자<br>Semiconductor Devices | [작은 전류의 증폭 효율: subthreshold와 gm/Id](../분야_topics/10-반도체소자_semiconductors/해설_notes/작은전류의증폭효율_subthreshold.md) · [English](../분야_topics/10-반도체소자_semiconductors/해설_notes/작은전류의증폭효율_subthreshold.md#english) |
| 11 아날로그 IC 설계·Cadence·Spectre<br>Analog IC Design: Cadence & Spectre | [피드백을 걸면 이득과 대역폭은 어떻게 바뀌는가](../분야_topics/11-아날로그IC설계_analog-ic-cadence/해설_notes/피드백과대역폭_feedback.md) · [English](../분야_topics/11-아날로그IC설계_analog-ic-cadence/해설_notes/피드백과대역폭_feedback.md#english) |
| 12 PCB와 하드웨어 설계<br>PCB & Hardware Design | [커패시터를 더 달았는데 왜 전원 임피던스가 커질까요](../분야_topics/12-PCB하드웨어설계_pcb-hardware/해설_notes/커패시터사이의공진_pdn-antiresonance.md) · [English](../분야_topics/12-PCB하드웨어설계_pcb-hardware/해설_notes/커패시터사이의공진_pdn-antiresonance.md#english) |
| 13 Verilog·SystemVerilog·RTL<br>Verilog, SystemVerilog & RTL | [고정소수점 곱셈: 비트 폭, 반올림, 포화를 따로 결정하기](../분야_topics/13-RTL설계_verilog-systemverilog/해설_notes/고정소수점의경계_fixed-point.md) · [English](../분야_topics/13-RTL설계_verilog-systemverilog/해설_notes/고정소수점의경계_fixed-point.md#english) |
| 14 하드웨어 검증<br>Hardware Verification | [개수는 맞는데 순서는 틀렸다: 작은 모델의 전수검사](../분야_topics/14-하드웨어검증_hardware-verification/해설_notes/불변식의빈틈_model-checking.md) · [English](../분야_topics/14-하드웨어검증_hardware-verification/해설_notes/불변식의빈틈_model-checking.md#english) |
| 15 FPGA·ASIC 설계<br>FPGA & ASIC Design | [여러 주기를 쓰는 경로: multicycle과 hold 관계](../분야_topics/15-FPGA-ASIC설계_fpga-asic/해설_notes/여러주기를쓰는경로_multicycle.md) · [English](../분야_topics/15-FPGA-ASIC설계_fpga-asic/해설_notes/여러주기를쓰는경로_multicycle.md#english) |
| 16 Arm·RISC-V와 프로세서 구조<br>Arm, RISC-V & Computer Architecture | [페이지 안에서 캐시를 찾기: VIPT와 alias 조건](../분야_topics/16-프로세서구조_arm-riscv/해설_notes/페이지안의캐시인덱스_vipt.md) · [English](../분야_topics/16-프로세서구조_arm-riscv/해설_notes/페이지안의캐시인덱스_vipt.md#english) |
| 29 전자기학·RF·안테나<br>Electromagnetics, RF & Antennas | [사분파장 정합: 선로 길이로 임피던스 바꾸기](../분야_topics/29-전자기학-RF_electromagnetics-rf/해설_notes/사분파장정합_quarter-wave.md) · [English](../분야_topics/29-전자기학-RF_electromagnetics-rf/해설_notes/사분파장정합_quarter-wave.md#english) |
| 30 통신이론과 무선 시스템<br>Communication Systems & Information Theory | [정합필터로 읽는 QPSK: 에너지와 잡음의 눈금 맞추기](../분야_topics/30-통신이론무선시스템_communications-wireless/해설_notes/정합필터로읽는QPSK_qpsk.md) · [English](../분야_topics/30-통신이론무선시스템_communications-wireless/해설_notes/정합필터로읽는QPSK_qpsk.md#english) |
| 31 전력전자와 에너지<br>Power Electronics & Energy | [부하가 갑자기 바뀔 때: buck의 평균 과도모델](../분야_topics/31-전력전자에너지_power-energy/해설_notes/부하변화의과도응답_buck-transient.md) · [English](../분야_topics/31-전력전자에너지_power-energy/해설_notes/부하변화의과도응답_buck-transient.md#english) |
| 32 혼성신호·ADC·DAC·클록<br>Mixed-Signal, Data Converters & Clocks | [전이 전압으로 읽는 ADC 선형성: DNL과 INL](../분야_topics/32-혼성신호-ADC-DAC_mixed-signal-data-converters/해설_notes/전이전압의오차_adc-linearity.md) · [English](../분야_topics/32-혼성신호-ADC-DAC_mixed-signal-data-converters/해설_notes/전이전압의오차_adc-linearity.md#english) |
| 33 메모리와 저장장치<br>Memory & Storage Systems | [SRAM을 읽을 때 저장 노드가 올라가는 이유](../분야_topics/33-메모리저장장치_memory-storage/해설_notes/SRAM읽기교란_read-disturb.md) · [English](../분야_topics/33-메모리저장장치_memory-storage/해설_notes/SRAM읽기교란_read-disturb.md#english) |
| 34 SoC와 연결 구조<br>SoC & Interconnects | [멀리 있는 버퍼를 넘치지 않게 쓰기: credit flow control](../분야_topics/34-SoC연결구조_soc-interconnects/해설_notes/크레딧으로흐름제어_credit-flow.md) · [English](../분야_topics/34-SoC연결구조_soc-interconnects/해설_notes/크레딧으로흐름제어_credit-flow.md#english) |
| 35 EDA와 오픈 하드웨어<br>EDA & Open Hardware Ecosystems | [다른 회로, 같은 상태 전이: equivalence를 확인하는 기준](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/같은상태전이_equivalence.md) · [English](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/같은상태전이_equivalence.md#english) |
| 36 패키징·Chiplet·열 설계<br>Packaging, Chiplets, Thermal & Reliability | [die와 package가 다른 속도로 뜨거워질 때: 두 노드 열망](../분야_topics/36-패키징열설계_packaging-thermal/해설_notes/두노드의열흐름_thermal-network.md) · [English](../분야_topics/36-패키징열설계_packaging-thermal/해설_notes/두노드의열흐름_thermal-network.md#english) |
| 37 센서와 계측<br>Sensors, Instrumentation & Experiments | [직선 교정의 불확도: 기울기와 절편을 함께 다루기](../분야_topics/37-센서계측_sensors-instrumentation/해설_notes/직선교정의불확도_linear-calibration.md) · [English](../분야_topics/37-센서계측_sensors-instrumentation/해설_notes/직선교정의불확도_linear-calibration.md#english) |
| 51 DFT·반도체 테스트·제조<br>DFT, Semiconductor Test & Manufacturing | [다른 출력이 같은 signature가 될 때: aliasing을 계산하기](../분야_topics/51-반도체테스트제조_test-manufacturing/해설_notes/서명이같아지는오류_signature-aliasing.md) · [English](../분야_topics/51-반도체테스트제조_test-manufacturing/해설_notes/서명이같아지는오류_signature-aliasing.md#english) |
| 54 차세대 소자와 컴퓨팅<br>Research Frontiers | [PIM 출력 교정: gain·offset을 고칠 수 있는 범위](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/해설_notes/PIM출력교정_pim-calibration.md) · [English](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/해설_notes/PIM출력교정_pim-calibration.md#english) |

## 펌웨어·시스템·제어 | Firmware, systems and control

| 분야 / Area | 심화 해설 / Advanced article |
| --- | --- |
| 17 펌웨어·RTOS<br>Firmware & RTOS | [RTOS의 우선순위 역전: 누가 mutex를 놓을 수 있을까요](../분야_topics/17-펌웨어-RTOS_firmware-rtos/해설_notes/우선순위역전_priority-inheritance.md) · [English](../분야_topics/17-펌웨어-RTOS_firmware-rtos/해설_notes/우선순위역전_priority-inheritance.md#english) |
| 18 임베디드 Linux<br>Embedded Linux | [Embedded Linux의 readiness: 바이트를 끝까지 읽는 상태](../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/준비이벤트와레코드_poll-record-streams.md) · [English](../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/준비이벤트와레코드_poll-record-streams.md#english) |
| 19 OpenOCD·GDB와 시스템 디버깅<br>OpenOCD, GDB & Instrumentation | [Watchpoint: 값이 바뀐 순간과 메모리 접근은 다르다](../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/접근을잡는관찰점_watchpoints-access-values.md) · [English](../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/접근을잡는관찰점_watchpoints-access-values.md#english) |
| 20 인터페이스와 통신<br>Interfaces & Communications | [I2C 레지스터 읽기: repeated START와 마지막 NACK](../분야_topics/20-인터페이스통신_interfaces-communications/해설_notes/I2C묶음전송_i2c-combined-transactions.md) · [English](../분야_topics/20-인터페이스통신_interfaces-communications/해설_notes/I2C묶음전송_i2c-combined-transactions.md#english) |
| 21 신호처리와 제어<br>Signals, DSP & Control | [이산 PI 제어: 표본 주기, 안정성과 적분 포화](../분야_topics/21-신호처리제어_signals-control/해설_notes/이산PI와적분포화_sampled-pi-antiwindup.md) · [English](../분야_topics/21-신호처리제어_signals-control/해설_notes/이산PI와적분포화_sampled-pi-antiwindup.md#english) |
| 22 로봇 제어·Arduino·Raspberry Pi<br>Robotics, Arduino & Raspberry Pi | [바퀴 속도 PI 제어: 포화된 모터에 적분을 계속 더하면](../분야_topics/22-로봇제어_robotics-boards/해설_notes/속도PI와포화_speed-pi-anti-windup.md) · [English](../분야_topics/22-로봇제어_robotics-boards/해설_notes/속도PI와포화_speed-pi-anti-windup.md#english) |

## AI·GPU·데이터 | AI, GPUs and data

| 분야 / Area | 심화 해설 / Advanced article |
| --- | --- |
| 23 AI·머신러닝·딥러닝<br>AI, Machine Learning & Deep Learning | [작은 MLP로 역전파를 끝까지 계산하기](../분야_topics/23-AI머신러닝_ai-machine-learning/해설_notes/다층신경망역전파_mlp-backprop.md) · [English](../분야_topics/23-AI머신러닝_ai-machine-learning/해설_notes/다층신경망역전파_mlp-backprop.md#english) |
| 24 GPU 구조<br>GPU Architecture | [타일 재사용과 shared-memory bank conflict](../분야_topics/24-GPU구조_gpu-architecture/해설_notes/타일메모리와은행충돌_tiled-memory.md) · [English](../분야_topics/24-GPU구조_gpu-architecture/해설_notes/타일메모리와은행충돌_tiled-memory.md#english) |
| 25 CUDA와 GPU 성능 최적화<br>CUDA & GPU Optimization | [경계 tile까지 계산하는 행렬곱: CPU 기준선과 CUDA kernel](../분야_topics/25-CUDA성능최적화_cuda-performance/해설_notes/경계타일행렬곱_tiled-matmul.md) · [English](../분야_topics/25-CUDA성능최적화_cuda-performance/해설_notes/경계타일행렬곱_tiled-matmul.md#english) |
| 26 AI 모델과 API<br>AI Providers, Public Models & APIs | [Beam search의 목적함수와 KV cache의 메모리 예산](../분야_topics/26-AI모델-API_open-model-lab/해설_notes/빔탐색과캐시예산_beam-cache-budget.md) · [English](../분야_topics/26-AI모델-API_open-model-lab/해설_notes/빔탐색과캐시예산_beam-cache-budget.md#english) |
| 40 데이터베이스와 데이터 공학<br>Databases & Data Engineering | [SQLite WAL에서 snapshot과 낙관적 갱신을 관찰하기](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md) · [English](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md#english) |
| 41 클라우드와 분산 시스템<br>Cloud, Distributed Systems & Operations | [Lamport clock: 시각을 맞추지 않고 인과 순서를 기록하기](../분야_topics/41-클라우드분산시스템_cloud-distributed/해설_notes/논리시계와인과관계_lamport-clocks.md) · [English](../분야_topics/41-클라우드분산시스템_cloud-distributed/해설_notes/논리시계와인과관계_lamport-clocks.md#english) |
| 42 고성능·병렬 계산<br>HPC, Parallel & Distributed Computing | [Parallel prefix scan: 누적합으로 위치를 배정하기](../분야_topics/42-고성능병렬계산_hpc-parallel/해설_notes/트리누적합과압축_parallel-prefix.md) · [English](../분야_topics/42-고성능병렬계산_hpc-parallel/해설_notes/트리누적합과압축_parallel-prefix.md#english) |
| 43 컴퓨터 비전과 영상 처리<br>Computer Vision & Image Processing | [Bilinear warp: 없는 pixel 사이의 값을 어떻게 계산할까요](../분야_topics/43-컴퓨터비전_computer-vision/해설_notes/역매핑과쌍선형보간_bilinear-warp.md) · [English](../분야_topics/43-컴퓨터비전_computer-vision/해설_notes/역매핑과쌍선형보간_bilinear-warp.md#english) |
| 44 언어·음성·멀티모달 AI<br>Language, Speech & Multimodal AI | [Attention의 역전파와 causal KV cache 검증](../분야_topics/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/어텐션역전파와캐시_attention-gradients.md) · [English](../분야_topics/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/어텐션역전파와캐시_attention-gradients.md#english) |
| 45 AI 학습과 최적화<br>AI Training, Optimization & Compression | [Adam의 상태, bias correction과 학습 재개](../분야_topics/45-AI학습최적화_ai-training-optimization/해설_notes/Adam상태와재시작_adam-state.md) · [English](../분야_topics/45-AI학습최적화_ai-training-optimization/해설_notes/Adam상태와재시작_adam-state.md#english) |
| 46 AI 응용·에이전트·평가<br>AI Applications, Agents & Evaluation | [Macro·micro 지표와 평가의 불확실성](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/평가지표와불확실성_metrics-uncertainty.md) · [English](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/평가지표와불확실성_metrics-uncertainty.md#english) |
| 47 엣지 AI·TinyML·NPU<br>Edge AI, TinyML & NPUs | [채널별 정수 양자화와 오차의 크기](../분야_topics/47-엣지AI-TinyML_edge-tinyml/해설_notes/채널별정수양자화_per-channel-quantization.md) · [English](../분야_topics/47-엣지AI-TinyML_edge-tinyml/해설_notes/채널별정수양자화_per-channel-quantization.md#english) |
| 49 그래픽스와 렌더링<br>Computer Graphics, Rendering & Simulation | [원근 투영 뒤에도 표면의 속성을 맞추는 보간](../분야_topics/49-그래픽스렌더링_graphics-simulation/해설_notes/원근보정속성보간_perspective-interpolation.md) · [English](../분야_topics/49-그래픽스렌더링_graphics-simulation/해설_notes/원근보정속성보간_perspective-interpolation.md#english) |

## 수학·물리·추론·인문사회 | Mathematics, physics, reasoning and humanities

| 분야 / Area | 심화 해설 / Advanced article |
| --- | --- |
| 06 수식과 코드<br>Math to Code | [작은 특잇값이 오차를 키울 때: ridge 정규화](../분야_topics/06-수식과코드_math-to-code/해설_notes/정규화와작은특잇값_ridge-spectral-filtering.md) · [English](../분야_topics/06-수식과코드_math-to-code/해설_notes/정규화와작은특잇값_ridge-spectral-filtering.md#english) |
| 50 물리·과학 시뮬레이션<br>Physics, Multiphysics & Scientific Simulation | [미분방정식에서 요소 행렬까지: 1차원 열전도 FEM](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/해설_notes/열전도유한요소_weak-form-linear-fem.md) · [English](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/해설_notes/열전도유한요소_weak-form-linear-fem.md#english) |
| 56 물리 기초<br>Physics Foundations | [두 진동자가 연결되면: 정상 모드와 에너지 검증](../분야_topics/56-물리기초_physics-foundations/해설_notes/결합진동과정상모드_coupled-modes-verlet.md) · [English](../분야_topics/56-물리기초_physics-foundations/해설_notes/결합진동과정상모드_coupled-modes-verlet.md#english) |
| 57 추론·독해·적성시험<br>Reasoning, Reading and Aptitude Assessments | [주장의 반례를 계산하기: CNF와 DPLL](../추론과시험_reasoning/57-추론적성시험_reasoning-assessments/해설_notes/반례탐색과단위전파_sat-dpll-counterexamples.md) · [English](../추론과시험_reasoning/57-추론적성시험_reasoning-assessments/해설_notes/반례탐색과단위전파_sat-dpll-counterexamples.md#english) |
| 58 철학과 비판적 사고<br>Philosophy and Critical Thinking | [증거는 믿음을 어떻게 바꾸는가: 모형 비교와 Bayes factor](../인문사회_humanities/58-철학비판적사고_philosophy-critical-thinking/해설_notes/증거와모형비교_bayes-factors-and-beliefs.md) · [English](../인문사회_humanities/58-철학비판적사고_philosophy-critical-thinking/해설_notes/증거와모형비교_bayes-factors-and-beliefs.md#english) |
| 59 경제·선택·지표<br>Economics, Choices and Indicators | [산업 간 연결을 행렬로 읽기: 투입산출 모형과 고정점](../인문사회_humanities/59-경제선택지표_economics/해설_notes/산업연관과고정점_leontief-input-output.md) · [English](../인문사회_humanities/59-경제선택지표_economics/해설_notes/산업연관과고정점_leontief-input-output.md#english) |
| 60 사회·제도·증거<br>Society, Institutions and Evidence | [전체 비율이 층별 비교를 뒤집을 때: Simpson 역설과 표준화](../인문사회_humanities/60-사회제도증거_society-institutions/해설_notes/집계와표준화_simpson-standardized-rates.md) · [English](../인문사회_humanities/60-사회제도증거_society-institutions/해설_notes/집계와표준화_simpson-standardized-rates.md#english) |
| 61 법의 기초와 법령 읽기<br>Law Foundations and Legal Reading | [법령의 시간을 데이터로 읽기: 공포일, 시행일과 이력 조회](../인문사회_humanities/61-법령읽기_law-foundations/해설_notes/법령이력과시간구간_version-timelines-and-scope.md) · [English](../인문사회_humanities/61-법령읽기_law-foundations/해설_notes/법령이력과시간구간_version-timelines-and-scope.md#english) |

# 심화 학습의 출처 | Advanced sources

해설에서 사용한 자료를 글별로 모았습니다. 자료 목록의 확인 기준일은 2026-10-19입니다. 각 글의 정의·수식·가정 가까이에 있는 인용과 함께 읽으시면 근거의 범위를 확인하기 쉽습니다.

[전체 참고 자료](README.md)

## 글별 참고 자료

### 1. 파이프가 꽉 찼을 때: backpressure와 종료 조건

[해설 읽기](../분야_topics/01-linux-bash/해설_notes/파이프역압력_pipe-backpressure.md)

- [man7.org · pipe.7.html](https://man7.org/linux/man-pages/man7/pipe.7.html)
- [man7.org · poll.2.html](https://man7.org/linux/man-pages/man2/poll.2.html)

### 2. 바뀐 입력만 다시 만들기: 내용 기반 빌드와 캐시

[해설 읽기](../분야_topics/02-개발도구_git-development-tools/해설_notes/내용기반빌드_content-addressed-build.md)

- [git-scm.com · Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
- [bazel.build · caching](https://bazel.build/remote/caching)

### 3. 노트북 결과를 다시 얻으려면: 데이터와 분할의 재현성

[해설 읽기](../분야_topics/03-python-jupyter/해설_notes/데이터와분할재현성_data-split-reproducibility.md)

- [docs.python.org · random.html](https://docs.python.org/3/library/random.html#notes-on-reproducibility)
- [docs.python.org · csv.html](https://docs.python.org/3/library/csv.html)

### 4. C의 고정 크기 ring buffer: 경계와 소유권부터

[해설 읽기](../분야_topics/04-c-cpp-python/해설_notes/고정크기링버퍼_bounded-ring-buffer.md)

- [open-std.org · n1570.pdf](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)
- [cmu-sei.github.io · arr30-c](https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/rules/arrays-arr/arr30-c/)

### 5. 비선형 방정식: 빠른 Newton과 안전한 구간 좁히기

[해설 읽기](../분야_topics/05-과학계산_matlab-scientific/해설_notes/구간을지키는근찾기_safeguarded-root-finding.md)

- [dlmf.nist.gov · 3.8](https://dlmf.nist.gov/3.8)
- [mathworks.com · fzero.html](https://www.mathworks.com/help/matlab/ref/fzero.html)

### 6. 작은 특잇값이 오차를 키울 때: ridge 정규화

[해설 읽기](../분야_topics/06-수식과코드_math-to-code/해설_notes/정규화와작은특잇값_ridge-spectral-filtering.md)

- [ocw.mit.edu · 14S_E88WE3WkoIxxEUDt7A1ifKOugzJPE_transcript.pdf](https://ocw.mit.edu/courses/18-642-topics-in-mathematics-with-applications-in-finance-fall-2024/14S_E88WE3WkoIxxEUDt7A1ifKOugzJPE_transcript.pdf)
- [web.stanford.edu · Lecture13.pdf](https://web.stanford.edu/class/ee269/Lecture13.pdf)

### 7. 같은 계산, 다른 메모리 배치: AoS·SoA와 캐시

[해설 읽기](../분야_topics/07-컴퓨터공학기초_cs-foundations/해설_notes/배치와캐시_memory-layout-locality.md)

- [cs.cornell.edu · caches.html](https://www.cs.cornell.edu/courses/cs3410/2025fa/notes/caches.html)
- [docs.python.org · array.html](https://docs.python.org/3/library/array.html)

### 8. A*: 좋은 예상값으로 탐색을 줄이고 정답은 지키기

[해설 읽기](../분야_topics/08-알고리즘_problem-solving/해설_notes/휴리스틱최단경로_astar-reopening.md)

- [inst.eecs.berkeley.edu · informed.html](https://inst.eecs.berkeley.edu/~cs188/textbook/search/informed.html)
- [cs.cmu.edu · index.html](https://www.cs.cmu.edu/~15281/coursenotes/search/index.html)

### 9. 회로를 행렬로 풀기: Modified Nodal Analysis

[해설 읽기](../분야_topics/09-회로전자공학_circuits-electronics/해설_notes/회로를행렬로풀기_mna.md)

- [analog-electronics.tudelft.nl · NetworkTheory-1_Modified_Nodal_Analysis.html](https://analog-electronics.tudelft.nl/webbook/SED/_build/html/network_theory/NetworkTheory-1_Modified_Nodal_Analysis.html)
- [ngspice.sourceforge.io · ngspice-manual.pdf](https://ngspice.sourceforge.io/docs/ngspice-manual.pdf)

### 10. 작은 전류의 증폭 효율: subthreshold와 gm/Id

[해설 읽기](../분야_topics/10-반도체소자_semiconductors/해설_notes/작은전류의증폭효율_subthreshold.md)

- [ocw.mit.edu · 282ca336565ffdd1aeda1c212c3b0696_MIT6_012F09_lec12.pdf](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/282ca336565ffdd1aeda1c212c3b0696_MIT6_012F09_lec12.pdf)
- [infoscience.epfl.ch · EPFL_TH9146.pdf](https://infoscience.epfl.ch/record/265275/files/EPFL_TH9146.pdf)

### 11. 피드백에 따른 이득과 대역폭 | Feedback gain and bandwidth

[해설 읽기](../분야_topics/11-아날로그IC설계_analog-ic-cadence/해설_notes/피드백과대역폭_feedback.md)

- [analog.com · mt-033.pdf](https://www.analog.com/media/en/training-seminars/tutorials/mt-033.pdf)
- [analog-electronics.tudelft.nl · freq_compensation_Phase_margin_design.html](https://analog-electronics.tudelft.nl/webbook/SED/_build/html/freq_compensation/freq_compensation_Phase_margin_design.html)

### 12. 커패시터를 더 달았는데 왜 전원 임피던스가 커질까요

[해설 읽기](../분야_topics/12-PCB하드웨어설계_pcb-hardware/해설_notes/커패시터사이의공진_pdn-antiresonance.md)

- [analog.com · MT-101.pdf](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)
- [bears.ece.ucsb.edu · real_world_decoupling.pdf](https://bears.ece.ucsb.edu/class/ece124d/real_world_decoupling.pdf)

### 13. 고정소수점 곱셈: 비트 폭, 반올림, 포화를 따로 결정하기

[해설 읽기](../분야_topics/13-RTL설계_verilog-systemverilog/해설_notes/고정소수점의경계_fixed-point.md)

- [docs.amd.com · Quantization-Modes](https://docs.amd.com/r/2021.1-English/ug1399-vitis-hls/Quantization-Modes)
- [mathworks.com · rounding.html](https://www.mathworks.com/help/fixedpoint/ug/rounding.html)

### 14. 개수는 맞아도 순서가 다른 경우: 작은 모델의 전수검사

[해설 읽기](../분야_topics/14-하드웨어검증_hardware-verification/해설_notes/불변식의빈틈_model-checking.md)

- [symbiyosys.readthedocs.io · verilog.html](https://symbiyosys.readthedocs.io/en/latest/verilog.html)
- [blogs.sw.siemens.com · the-beginning-of-the-end-for-coverage](https://blogs.sw.siemens.com/verificationhorizons/2019/06/03/the-beginning-of-the-end-for-coverage/)

### 15. 여러 주기를 쓰는 경로: multicycle과 hold 관계

[해설 읽기](../분야_topics/15-FPGA-ASIC설계_fpga-asic/해설_notes/여러주기를쓰는경로_multicycle.md)

- [docs.amd.com · Relaxing-the-Setup-Requirement-While-Keeping-Hold-Unchanged](https://docs.amd.com/r/2020.2-English/ug1387-acap-hardware-ip-platform-dev-methodology/Relaxing-the-Setup-Requirement-While-Keeping-Hold-Unchanged?contentId=mDPen7K8UpE03COFvi9s_g)
- [docs.altera.com · relaxing-setup-with-multicycle-set_multicyle_path](https://docs.altera.com/r/docs/683243/25.3/quartus-prime-pro-edition-user-guide-timing-analyzer/relaxing-setup-with-multicycle-set_multicyle_path)

### 16. 페이지 안에서 캐시를 찾기: VIPT와 alias 조건

[해설 읽기](../분야_topics/16-프로세서구조_arm-riscv/해설_notes/페이지안의캐시인덱스_vipt.md)

- [developer.arm.com · page-colouring-on-armv6-and-a-bit-on-armv7](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/page-colouring-on-armv6-and-a-bit-on-armv7)
- [cs.cmu.edu · lec5_6-cache.pdf](https://www.cs.cmu.edu/~15346-s21/lectures/lec5_6-cache.pdf)

### 17. 뮤텍스 대기와 우선순위 상속 | Mutex waits and priority inheritance

[해설 읽기](../분야_topics/17-펌웨어-RTOS_firmware-rtos/해설_notes/우선순위역전_priority-inheritance.md)

- [docs.kernel.org · rt-mutex-design.html](https://docs.kernel.org/locking/rt-mutex-design.html)
- [docs.zephyrproject.org · mutexes.html](https://docs.zephyrproject.org/latest/kernel/services/synchronization/mutexes.html)

### 18. Embedded Linux의 readiness: 바이트를 끝까지 읽는 상태

[해설 읽기](../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/준비이벤트와레코드_poll-record-streams.md)

- [man7.org · poll.2.html](https://man7.org/linux/man-pages/man2/poll.2.html)
- [man7.org · select.2.html](https://man7.org/linux/man-pages/man2/select.2.html)
- [docs.python.org · selectors.html](https://docs.python.org/3/library/selectors.html)

### 19. Watchpoint: 값이 바뀐 순간과 메모리 접근은 다릅니다

[해설 읽기](../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/접근을잡는관찰점_watchpoints-access-values.md)

- [sourceware.org · Set-Watchpoints.html](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html)
- [openocd.org · General-Commands.html](https://openocd.org/doc/html/General-Commands.html#Breakpoint-and-Watchpoint-commands)
- [openocd.org · General-Commands.html](https://openocd.org/doc/html/General-Commands.html)

### 20. I2C 레지스터 읽기: repeated START와 마지막 NACK

[해설 읽기](../분야_topics/20-인터페이스통신_interfaces-communications/해설_notes/I2C묶음전송_i2c-combined-transactions.md)

- [nxp.com · UM10204.pdf](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)
- [docs.kernel.org · i2c-protocol.html](https://docs.kernel.org/i2c/i2c-protocol.html)

### 21. 이산 PI 제어: 표본 주기, 안정성과 적분 포화

[해설 읽기](../분야_topics/21-신호처리제어_signals-control/해설_notes/이산PI와적분포화_sampled-pi-antiwindup.md)

- [mathworks.com · anti-windup-control-using-a-pid-controller.html](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html)
- [mathworks.com · pidcontroller.html](https://www.mathworks.com/help/simulink/slref/pidcontroller.html)

### 22. 바퀴 속도 PI 제어: 포화된 모터에 적분을 계속 더하면

[해설 읽기](../분야_topics/22-로봇제어_robotics-boards/해설_notes/속도PI와포화_speed-pi-anti-windup.md)

- [ocw.mit.edu · d98dc04f3311eb4e8c786a342dd07f87_MIT2_017JF09_ch11.pdf](https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/d98dc04f3311eb4e8c786a342dd07f87_MIT2_017JF09_ch11.pdf)
- [mathworks.com · anti-windup-control-using-a-pid-controller.html](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html)

### 23. 작은 MLP로 역전파를 끝까지 계산하기

[해설 읽기](../분야_topics/23-AI머신러닝_ai-machine-learning/해설_notes/다층신경망역전파_mlp-backprop.md)

- [cs231n.github.io · optimization-2](https://cs231n.github.io/optimization-2/)
- [web.stanford.edu · cs224n-2019-notes03-neuralnets.pdf](https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes03-neuralnets.pdf)
- [docs.pytorch.org · torch.nn.Linear.html](https://docs.pytorch.org/docs/2.9/generated/torch.nn.Linear.html)

### 24. 타일 재사용과 shared-memory bank conflict

[해설 읽기](../분야_topics/24-GPU구조_gpu-architecture/해설_notes/타일메모리와은행충돌_tiled-memory.md)

- [docs.nvidia.com · writing-cuda-kernels.html](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)
- [docs.nvidia.com · index.html](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab)
- [docs.nvidia.com · index.html](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory)

### 25. 경계 tile까지 계산하는 행렬곱: CPU 기준선과 CUDA kernel

[해설 읽기](../분야_topics/25-CUDA성능최적화_cuda-performance/해설_notes/경계타일행렬곱_tiled-matmul.md)

- [docs.nvidia.com · index.html](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab)
- [docs.nvidia.com · writing-cuda-kernels.html](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

### 26. Beam search의 목적함수와 KV cache의 메모리 예산

[해설 읽기](../분야_topics/26-AI모델-API_open-model-lab/해설_notes/빔탐색과캐시예산_beam-cache-budget.md)

- [huggingface.co · generation_strategies](https://huggingface.co/docs/transformers/en/generation_strategies)
- [huggingface.co · cache_explanation](https://huggingface.co/docs/transformers/en/cache_explanation)

### 27. 재현 실험 설계: 같은 조건에서 차이를 비교하기

[해설 읽기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md)

- [sigir.org · acm-sigir-artifact-badging](https://sigir.org/general-information/acm-sigir-artifact-badging/)
- [itl.nist.gov · pri332.htm](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm)
- [itl.nist.gov · prc311.htm](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm)

### 28. CI를 줄여도 검증은 빠뜨리지 않기: 변경 영향과 캐시

[해설 읽기](../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/변경영향과CI캐시_incremental-ci-cache.md)

- [docs.github.com · dependency-caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)
- [reproducible-builds.org · recording](https://reproducible-builds.org/docs/recording/)

### 29. 사분파장 정합: 선로 길이로 임피던스 바꾸기

[해설 읽기](../분야_topics/29-전자기학-RF_electromagnetics-rf/해설_notes/사분파장정합_quarter-wave.md)

- [ittc.ku.edu · section_5_4_The_Quarter_Wave_Transformer_present.pdf](https://www.ittc.ku.edu/~jstiles/723/handouts/section_5_4_The_Quarter_Wave_Transformer_present.pdf)
- [optics.ansys.com · 360042041094-Quarter-wave-impedance-transformer](https://optics.ansys.com/hc/en-us/articles/360042041094-Quarter-wave-impedance-transformer)

### 30. 정합필터로 읽는 QPSK: 에너지와 잡음의 눈금 맞추기

[해설 읽기](../분야_topics/30-통신이론무선시스템_communications-wireless/해설_notes/정합필터로읽는QPSK_qpsk.md)

- [ocw.mit.edu · ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf](https://ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf)
- [mathworks.com · analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html)

### 31. 부하가 갑자기 바뀔 때: buck의 평균 과도모델

[해설 읽기](../분야_topics/31-전력전자에너지_power-energy/해설_notes/부하변화의과도응답_buck-transient.md)

- [ti.com · slva057.pdf](https://www.ti.com/lit/an/slva057/slva057.pdf)
- [analog.com · maxrefdes1269.pdf](https://www.analog.com/media/en/reference-design-documentation/reference-designs/maxrefdes1269.pdf)

### 32. 전이 전압으로 읽는 ADC 선형성: DNL과 INL

[해설 읽기](../분야_topics/32-혼성신호-ADC-DAC_mixed-signal-data-converters/해설_notes/전이전압의오차_adc-linearity.md)

- [ti.com · sbaa004a.pdf](https://www.ti.com/lit/an/sbaa004a/sbaa004a.pdf)
- [analog.com · inldnl-measurements-for-types-of-highspeed-adcs.html](https://www.analog.com/en/resources/technical-articles/inldnl-measurements-for-types-of-highspeed-adcs.html)

### 33. SRAM을 읽을 때 저장 노드가 올라가는 이유

[해설 읽기](../분야_topics/33-메모리저장장치_memory-storage/해설_notes/SRAM읽기교란_read-disturb.md)

- [people.eecs.berkeley.edu · bsriram.pdf](https://people.eecs.berkeley.edu/~tking/theses/bsriram.pdf)
- [people.eecs.berkeley.edu · VLSI10-Seng.pdf](https://people.eecs.berkeley.edu/~bora/Conferences/2010/VLSI10-Seng.pdf)

### 34. 멀리 있는 버퍼를 넘치지 않게 쓰기: credit flow control

[해설 읽기](../분야_topics/34-SoC연결구조_soc-interconnects/해설_notes/크레딧으로흐름제어_credit-flow.md)

- [intel.com · transaction-layer.html](https://www.intel.com/content/www/us/en/docs/programmable/683660/15-1/transaction-layer.html)
- [pcisig.com · pci-express%C2%AE-60-specification-functionality-updates-%E2%80%93-part-2](https://pcisig.com/blog/pci-express%C2%AE-60-specification-functionality-updates-%E2%80%93-part-2)

### 35. 다른 회로, 같은 상태 전이: equivalence를 확인하는 기준

[해설 읽기](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/같은상태전이_equivalence.md)

- [yosyshq.readthedocs.io · latest](https://yosyshq.readthedocs.io/projects/eqy/en/latest/)
- [openroad-flow-scripts.readthedocs.io · UserGuide.html](https://openroad-flow-scripts.readthedocs.io/en/latest/user/UserGuide.html)

### 36. die와 package가 다른 속도로 뜨거워질 때: 두 노드 열망

[해설 읽기](../분야_topics/36-패키징열설계_packaging-thermal/해설_notes/두노드의열흐름_thermal-network.md)

- [analog.com · use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)
- [ti.com · 6243719539001](https://www.ti.com/video/6243719539001)

### 37. 직선 교정의 불확도: 기울기와 절편을 함께 다루기

[해설 읽기](../분야_topics/37-센서계측_sensors-instrumentation/해설_notes/직선교정의불확도_linear-calibration.md)

- [itl.nist.gov · calibrat.htm](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/calibrat.htm)
- [bipm.org · JCGM_100_2008_E.pdf](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf)

### 38. 인증된 메시지의 재전송: replay window

[해설 읽기](../분야_topics/38-보안암호하드웨어신뢰_security-cryptography/해설_notes/인증후재전송검사_authenticated-replay-window.md)

- [rfc-editor.org · rfc4303.html](https://www.rfc-editor.org/rfc/rfc4303.html)
- [rfc-editor.org · rfc5116.html](https://www.rfc-editor.org/rfc/rfc5116.html)

### 39. 작은 수식 언어 만들기: 우선순위에서 stack bytecode까지

[해설 읽기](../분야_topics/39-컴파일러언어런타임_compilers-languages/해설_notes/수식에서바이트코드_expression-bytecode.md)

- [llvm.org · LangImpl02.html](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html)
- [docs.python.org · ast.html](https://docs.python.org/3/library/ast.html)

### 40. SQLite WAL에서 snapshot과 낙관적 갱신을 관찰하기

[해설 읽기](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md)

- [sqlite.org · wal.html](https://www.sqlite.org/wal.html)
- [sqlite.org · isolation.html](https://www.sqlite.org/isolation.html)
- [sqlite.org · lang_transaction.html](https://www.sqlite.org/lang_transaction.html)

### 41. Lamport clock: 시각을 맞추지 않고 인과 순서를 기록하기

[해설 읽기](../분야_topics/41-클라우드분산시스템_cloud-distributed/해설_notes/논리시계와인과관계_lamport-clocks.md)

- [lamport.azurewebsites.net · time-clocks.pdf](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)
- [cs.yale.edu · LogicalClocks.html](https://www.cs.yale.edu/homes/aspnes/pinewiki/LogicalClocks.html)
- [cs.cornell.edu · clocks.html](https://www.cs.cornell.edu/courses/cs614/1999sp/notes99/clocks.html)

### 42. Parallel prefix scan: 누적합으로 위치를 배정하기

[해설 읽기](../분야_topics/42-고성능병렬계산_hpc-parallel/해설_notes/트리누적합과압축_parallel-prefix.md)

- [cs.cmu.edu · Ble93.pdf](https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf)
- [developer.nvidia.com · chapter-39-parallel-prefix-sum-scan-cuda](https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda)

### 43. 역매핑과 쌍선형 보간 / Inverse mapping and bilinear interpolation

[해설 읽기](../분야_topics/43-컴퓨터비전_computer-vision/해설_notes/역매핑과쌍선형보간_bilinear-warp.md)

- [docs.opencv.org · group__imgproc__transform.html](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html)
- [docs.pytorch.org · torch.nn.functional.grid_sample.html](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.grid_sample.html)

### 44. Attention의 역전파와 causal KV cache 검증

[해설 읽기](../분야_topics/44-언어음성멀티모달AI_language-speech-multimodal/해설_notes/어텐션역전파와캐시_attention-gradients.md)

- [arxiv.org · 1706.03762](https://arxiv.org/pdf/1706.03762)
- [docs.pytorch.org · torch.nn.functional.scaled_dot_product_attention.html](https://docs.pytorch.org/docs/2.9/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [huggingface.co · cache_explanation](https://huggingface.co/docs/transformers/en/cache_explanation)

### 45. Adam의 상태, bias correction과 학습 재개

[해설 읽기](../분야_topics/45-AI학습최적화_ai-training-optimization/해설_notes/Adam상태와재시작_adam-state.md)

- [arxiv.org · 1412.6980](https://arxiv.org/pdf/1412.6980)
- [docs.pytorch.org · torch.optim.Adam.html](https://docs.pytorch.org/docs/2.9/generated/torch.optim.Adam.html)

### 46. Macro·micro 지표와 평가의 불확실성

[해설 읽기](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/평가지표와불확실성_metrics-uncertainty.md)

- [nlp.stanford.edu · evaluation-of-text-classification-1.html](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-text-classification-1.html)
- [developers.google.com · accuracy-precision-recall](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)
- [itl.nist.gov · prc241.htm](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)

### 47. 채널별 정수 양자화와 오차의 크기

[해설 읽기](../분야_topics/47-엣지AI-TinyML_edge-tinyml/해설_notes/채널별정수양자화_per-channel-quantization.md)

- [developers.google.com · quantization_spec](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)
- [onnx.ai · onnx__QuantizeLinear.html](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html)

### 48. 테스트가 실패한 뒤: 재현 가능한 반례와 shrinking

[해설 읽기](../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/실패입력줄이기_property-counterexample-shrinking.md)

- [hypothesis.readthedocs.io · replaying-failures.html](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
- [docs.python.org · unittest.html](https://docs.python.org/3/library/unittest.html)

### 49. 원근 투영 뒤에도 표면의 속성을 맞추는 보간

[해설 읽기](../분야_topics/49-그래픽스렌더링_graphics-simulation/해설_notes/원근보정속성보간_perspective-interpolation.md)

- [registry.khronos.org · glspec46.core.pdf](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)
- [learn.microsoft.com · rasterization-rules](https://learn.microsoft.com/en-us/windows/win32/direct3d9/rasterization-rules)

### 50. 미분방정식에서 요소 행렬까지: 1차원 열전도 FEM

[해설 읽기](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/해설_notes/열전도유한요소_weak-form-linear-fem.md)

- [ocw.mit.edu · c9f0e715af0009fa2677b428dbaf3c0a_lec19.pdf](https://ocw.mit.edu/courses/6-336j-introduction-to-numerical-simulation-sma-5211-fall-2003/c9f0e715af0009fa2677b428dbaf3c0a_lec19.pdf)
- [people.math.sc.edu · fem1d_bvp_linear.html](https://people.math.sc.edu/burkardt/f_src/fem1d_bvp_linear/fem1d_bvp_linear.html)

### 51. 다른 출력이 같은 signature가 될 때: aliasing을 계산하기

[해설 읽기](../분야_topics/51-반도체테스트제조_test-manufacturing/해설_notes/서명이같아지는오류_signature-aliasing.md)

- [citeseerx.ist.psu.edu · document](https://citeseerx.ist.psu.edu/document?doi=a210ff0bfb04cb20d21c45e5a74880ebf2cea1a8&repid=rep1&type=pdf)
- [www-verimag.imag.fr · ieeetc91.html](https://www-verimag.imag.fr/~caspi/PAPIERS/ieeetc91.html)

### 52. 두 사용자의 수정이 겹치면: ETag와 조건부 갱신

[해설 읽기](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/버전조건부갱신_optimistic-concurrency-etag.md)

- [rfc-editor.org · rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html)
- [google.aip.dev · 154](https://google.aip.dev/154)
- [rfc-editor.org · rfc6585.html](https://www.rfc-editor.org/rfc/rfc6585.html#section-3)

### 53. UI 상태를 한곳에서 바꾸기: reducer와 비동기 효과

[해설 읽기](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/UI이벤트리듀서_ui-event-reducer.md)

- [developer.android.com · architecture](https://developer.android.com/develop/ui/compose/architecture)
- [developer.android.com · state-production](https://developer.android.com/topic/architecture/ui-layer/state-production)

### 54. PIM 출력 교정: gain·offset을 고칠 수 있는 범위

[해설 읽기](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/해설_notes/PIM출력교정_pim-calibration.md)

- [research.ibm.com · the-hardware-behind-analog-ai](https://research.ibm.com/blog/the-hardware-behind-analog-ai)
- [nist.gov · hardware-accelerators-neural-networks](https://www.nist.gov/programs-projects/hardware-accelerators-neural-networks)

### 55. 두 진동자가 연결되면: 정상 모드와 에너지 검증

[해설 읽기](../분야_topics/56-물리기초_physics-foundations/해설_notes/결합진동과정상모드_coupled-modes-verlet.md)

- [ocw.mit.edu · 7648a5c6cdbda42f39b05dae04ce2aa9_MIT16_07F09_Lec19.pdf](https://ocw.mit.edu/courses/16-07-dynamics-fall-2009/7648a5c6cdbda42f39b05dae04ce2aa9_MIT16_07F09_Lec19.pdf)
- [ocw.mit.edu · b4f512207b1e991ffdfa8df5f519b6eb_MIT8_03SCF16_Lec4.pdf](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/b4f512207b1e991ffdfa8df5f519b6eb_MIT8_03SCF16_Lec4.pdf)

### 56. 주장의 반례를 계산하기: CNF와 DPLL

[해설 읽기](../언어이해와추리논증_reading-reasoning/추리논증_reasoning/반례탐색_SAT.md)

- [cs.cmu.edu · 16-dpll.pdf](https://www.cs.cmu.edu/~15414/s25/lectures/16-dpll.pdf)
- [web.stanford.edu · NOT04.pdf](https://web.stanford.edu/class/cs357/NOT04.pdf)

### 57. 증거와 믿음의 관계: 모형 비교와 베이즈 요인

[해설 읽기](../인문사회_humanities/58-철학비판적사고_philosophy-critical-thinking/해설_notes/증거와모형비교_bayes-factors-and-beliefs.md)

- [plato.stanford.edu · epistemology-bayesian](https://plato.stanford.edu/entries/epistemology-bayesian/)
- [ocw.mit.edu · 9c7b5d5cfb5ad8127c4b9c1a0442f29b_MIT18_655S16_LecNote3.pdf](https://ocw.mit.edu/courses/18-655-mathematical-statistics-spring-2016/9c7b5d5cfb5ad8127c4b9c1a0442f29b_MIT18_655S16_LecNote3.pdf)

### 58. 산업 간 연결을 행렬로 읽기: 투입산출 모형과 고정점

[해설 읽기](../인문사회_humanities/59-경제선택지표_economics/해설_notes/산업연관과고정점_leontief-input-output.md)

- [bea.gov · RIMSII_User_Guide.pdf](https://www.bea.gov/sites/default/files/methodologies/RIMSII_User_Guide.pdf)
- [bea.gov · concepts-methods-io-accounts](https://www.bea.gov/resources/methodologies/concepts-methods-io-accounts)

### 59. 전체 비율이 층별 비교를 뒤집을 때: Simpson 역설과 표준화

[해설 읽기](../인문사회_humanities/60-사회제도증거_society-institutions/해설_notes/집계와표준화_simpson-standardized-rates.md)

- [online.stat.psu.edu · Lesson06](https://online.stat.psu.edu/stat100/Lesson06)
- [online.stat.psu.edu · Lesson04](https://online.stat.psu.edu/stat507/Lesson04)
- [doi.org · 0962280211398037](https://doi.org/10.1177/0962280211398037)

### 60. 법령의 시간을 데이터로 읽기: 공포일, 시행일과 이력 조회

[해설 읽기](../인문사회_humanities/61-법령읽기_law-foundations/해설_notes/법령이력과시간구간_version-timelines-and-scope.md)

- [open.law.go.kr · guideResult.do](https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=lsNwInfoGuide)
- [law.go.kr · lsInfoP.do](https://www.law.go.kr/lsInfoP.do?efYd=20240814&lsiSeq=260405)

## 데이터와 문서

[JSON 원본](심화출처_ADVANCED_SOURCES.json)은 문서 경로와 출처 URL을 연결하는 데이터입니다. 출처 문서 생성과 경로 검사에서 사용합니다. 읽기용 목록은 이 Markdown 문서입니다.

기준일은 자료 목록의 기록 날짜이며 모든 외부 페이지를 매번 재검증했다는 뜻은 아닙니다. 구체적인 인용 범위와 실행 여부는 각 해설과 검증 기록에 있습니다.

## English

This readable index groups the references by article. The JSON record retains article paths and source URLs for generation and path checks. Read the citations beside each claim for the scope of support; the inventory date is not a claim of continuous link verification.

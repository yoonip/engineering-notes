# 분야별 학습의 출처 | Technical topic sources

해설에서 사용한 자료를 글별로 모았습니다. 자료 목록의 확인 기준일은 2026-10-21입니다. 각 글의 정의·수식·가정 가까이에 있는 인용과 함께 읽으시면 근거의 범위를 확인하기 쉽습니다.

[전체 참고 자료](README.md)

## 글별 참고 자료

### 1. Linux에서 프로그램, 권한과 파이프가 만나는 곳

[해설 읽기](../분야_topics/01-linux-bash/해설_notes/프로세스-권한-파이프_processes-permissions-pipelines.md)

- [man7.org · fork.2.html](https://man7.org/linux/man-pages/man2/fork.2.html)
- [man7.org · path_resolution.7.html](https://man7.org/linux/man-pages/man7/path_resolution.7.html)
- [man7.org · pipe.7.html](https://man7.org/linux/man-pages/man7/pipe.7.html)
- [gnu.org · Pipelines.html](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)
- [gnu.org · Mode-Structure.html](https://www.gnu.org/software/coreutils/manual/html_node/Mode-Structure.html)

### 2. Git 이력과 다시 만들 수 있는 결과물

[해설 읽기](../분야_topics/02-개발도구_git-development-tools/해설_notes/Git이력과다시만들수있는결과물_commit-dag-reproducible-builds.md)

- [git-scm.com · Git-Branching-Branches-in-a-Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [git-scm.com · Git-Internals-Git-Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
- [reproducible-builds.org · definition](https://reproducible-builds.org/docs/definition/)

### 3. Python 환경과 Jupyter 실행 상태를 구분하기

[해설 읽기](../분야_topics/03-python-jupyter/해설_notes/Python환경과Jupyter실행상태_environments-kernel-state-reproducibility.md)

- [docs.python.org · venv.html](https://docs.python.org/3/library/venv.html)
- [ipython.readthedocs.io · kernel_install.html](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)
- [jupyterlab.readthedocs.io · notebook.html](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html)

### 4. MATLAB 수치해석: 답의 오차와 잔차는 왜 다를까요

[해설 읽기](../분야_topics/05-과학계산_matlab-scientific/해설_notes/MATLAB수치해석_linear-solves-conditioning-residuals.md)

- [mathworks.com · systems-of-linear-equations.html](https://www.mathworks.com/help/matlab/math/systems-of-linear-equations.html)
- [mathworks.com · cond.html](https://www.mathworks.com/help/matlab/ref/cond.html)

### 5. 복잡도와 자료구조: heap으로 최단 경로 찾기

[해설 읽기](../분야_topics/08-알고리즘_problem-solving/해설_notes/복잡도와자료구조_complexity-heaps-shortest-paths.md)

- [docs.python.org · heapq.html](https://docs.python.org/3/library/heapq.html)
- [docs.python.org · heapq.html](https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes)
- [ocw.mit.edu · 6277a1f06100c26a7ff21031af6757b5_MIT6_006F11_lec16.pdf](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/6277a1f06100c26a7ff21031af6757b5_MIT6_006F11_lec16.pdf)

### 6. 동작점에서 주파수 응답까지: 소신호와 AC 해석

[해설 읽기](../분야_topics/11-아날로그IC설계_analog-ic-cadence/해설_notes/동작점에서주파수응답까지_small-signal-ac-operating-point.md)

- [community.cadence.com · 1379372](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/49506/dc-operating-point-for-different-analyses/1379372)
- [ocw.mit.edu · 44ed13d9b5e46dd459d9bca431fc547a_lec23.pdf](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/44ed13d9b5e46dd459d9bca431fc547a_lec23.pdf)
- [ocw.mit.edu · 7a51249eb734152c5ce95df393cf4f1f_lec19.pdf](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2005/7a51249eb734152c5ce95df393cf4f1f_lec19.pdf)
- [analog.com · ltspice-ac-analysis-using-the-step-command.html](https://www.analog.com/en/resources/technical-articles/ltspice-ac-analysis-using-the-step-command.html)

### 7. 전원 배선까지 함께 보기: PDN, decoupling과 귀환 전류

[해설 읽기](../분야_topics/12-PCB하드웨어설계_pcb-hardware/해설_notes/전원은배선까지포함한다_pdn-decoupling-return-current.md)

- [analog.com · MT-101.pdf](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)
- [ti.com · scaa082a.pdf](https://www.ti.com/lit/an/scaa082a/scaa082a.pdf)

### 8. Assertion·coverage·formal의 검증 범위

[해설 읽기](../분야_topics/14-하드웨어검증_hardware-verification/해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md)

- [blogs.sw.siemens.com · the-beginning-of-the-end-for-coverage](https://blogs.sw.siemens.com/verificationhorizons/2019/06/03/the-beginning-of-the-end-for-coverage/)
- [symbiyosys.readthedocs.io · verilog.html](https://symbiyosys.readthedocs.io/en/latest/verilog.html)

### 9. 너무 늦거나 빠른 신호의 문제: setup·hold와 STA

[해설 읽기](../분야_topics/15-FPGA-ASIC설계_fpga-asic/해설_notes/너무늦어도너무빨라도문제다_setup-hold-static-timing.md)

- [docs.amd.com · Reviewing-Timing-Slack](https://docs.amd.com/r/en-US/ug1388-acap-system-integration-validation-methodology/Reviewing-Timing-Slack)
- [docs.amd.com · Removal-Relationship](https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/Hold/Removal-Relationship)
- [ocw.mit.edu · c5s1](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/)

### 10. 명령어가 보는 메모리: ISA, byte 순서와 load/store

[해설 읽기](../분야_topics/16-프로세서구조_arm-riscv/해설_notes/명령어가보는메모리_isa-byte-order-load-store.md)

- [docs.riscv.org · riscv-unprivileged.pdf](https://docs.riscv.org/reference/isa/_attachments/riscv-unprivileged.pdf)
- [notes.cs61c.org · rv-load-store](https://notes.cs61c.org/content/rv-data-transfer/rv-load-store/)

### 11. Embedded Linux: 부팅, Device Tree와 드라이버의 경계

[해설 읽기](../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/boot-devicetree-driver-boundaries.md)

- [docs.kernel.org · booting.html](https://docs.kernel.org/arch/arm64/booting.html)
- [docs.kernel.org · usage-model.html](https://docs.kernel.org/devicetree/usage-model.html)
- [docs.kernel.org · binding.html](https://docs.kernel.org/driver-api/driver-model/binding.html)

### 12. OpenOCD와 GDB: 연결, 정지 상태와 관찰의 의미

[해설 읽기](../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/OpenOCD와GDB_debug-transport-state-observation.md)

- [openocd.org · Debug-Adapter-Configuration.html](https://openocd.org/doc/html/Debug-Adapter-Configuration.html)
- [openocd.org · GDB-and-OpenOCD.html](https://openocd.org/doc/html/GDB-and-OpenOCD.html)
- [openocd.org · General-Commands.html](https://openocd.org/doc/html/General-Commands.html)
- [sourceware.org · Continuing-and-Stepping.html](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Continuing-and-Stepping.html)

### 13. 차동구동 로봇: 바퀴 회전에서 위치 추정까지

[해설 읽기](../분야_topics/22-로봇제어_robotics-boards/해설_notes/차동구동로봇_differential-drive-kinematics-odometry.md)

- [control.ros.org · userdoc.html](https://control.ros.org/rolling/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html)
- [roboticsbook.org · S52_diffdrive_actions.html](https://www.roboticsbook.org/S52_diffdrive_actions.html)

### 14. GPU의 warp, 메모리 접근, occupancy

[해설 읽기](../분야_topics/24-GPU구조_gpu-architecture/해설_notes/GPU메모리와실행자원_warp-memory-occupancy.md)

- [docs.nvidia.com · index.html](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- [docs.nvidia.com · index.html](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#coalesced-access-to-global-memory)
- [docs.nvidia.com · index.html](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy)
- [docs.nvidia.com · writing-cuda-kernels.html](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html)

### 15. 모델 파일에서 다음 토큰까지: 가중치, 토큰화, sampling

[해설 읽기](../분야_topics/26-AI모델-API_open-model-lab/해설_notes/모델파일에서다음토큰까지_weights-tokenizers-and-sampling.md)

- [huggingface.co · model-cards](https://huggingface.co/docs/hub/main/en/model-cards)
- [huggingface.co · pipeline](https://huggingface.co/docs/tokenizers/main/en/pipeline)
- [huggingface.co · generation_strategies](https://huggingface.co/docs/transformers/main/en/generation_strategies)

### 16. 논문·코드·특허 읽기: 주장과 재현 근거를 연결하기

[해설 읽기](../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md)

- [docs.github.com · licensing-a-repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
- [spdx.dev · handling-license-info](https://spdx.dev/learn/handling-license-info/)
- [nationalacademies.org · 6](https://www.nationalacademies.org/read/25303/chapter/6)
- [wipo.int · faq_patents](https://www.wipo.int/en/web/patents/faq_patents)

### 17. 자동화의 기본: 검증, 재실행과 원자적 게시

[해설 읽기](../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/자동화의기본_ci-idempotency-atomic-publication.md)

- [docs.github.com · workflow-syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [docs.python.org · os.html](https://docs.python.org/3/library/os.html#os.replace)
- [man7.org · rename.2.html](https://man7.org/linux/man-pages/man2/rename.2.html)

### 18. 잡음 속에서 bit를 고르기: BPSK, Eb/N0와 BER

[해설 읽기](../분야_topics/30-통신이론무선시스템_communications-wireless/해설_notes/잡음속에서bit를고르기_bpsk-awgn-ber.md)

- [ocw.mit.edu · ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf](https://ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/ecba60e6759f2eb6683f340cc5fed6b2_MIT16_36s09_lec11.pdf)
- [mathworks.com · analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html](https://www.mathworks.com/help/comm/ug/analytical-expressions-used-in-berawgn-function-and-bit-error-rate-analysis-app.html)

### 19. 스위칭으로 낮은 전압 만들기: buck의 CCM과 ripple

[해설 읽기](../분야_topics/31-전력전자에너지_power-energy/해설_notes/스위칭으로낮은전압만들기_buck-ccm-ripple.md)

- [analog.com · maxrefdes1269.pdf](https://www.analog.com/media/en/reference-design-documentation/reference-designs/maxrefdes1269.pdf)
- [ti.com · slva057.pdf](https://www.ti.com/lit/an/slva057/slva057.pdf)
- [ti.com · slva477b.pdf](https://www.ti.com/lit/an/slva477b/slva477b.pdf)

### 20. 준비된 순간에만 옮기기: ready/valid와 backpressure

[해설 읽기](../분야_topics/34-SoC연결구조_soc-interconnects/해설_notes/준비된순간에만옮기기_ready-valid-backpressure.md)

- [developer.arm.com · IHI0022H_amba_axi_protocol_spec.pdf](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf)
- [docs.amd.com · VALID-Handshake](https://docs.amd.com/r/en-US/pg043_v_vid_in_axi4s/READY/VALID-Handshake)

### 21. RTL에서 layout까지: 서로 다른 검증을 연결하는 EDA 흐름

[해설 읽기](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/해설_notes/RTL에서layout까지_rtl-netlist-timing-physical-checks.md)

- [openroad-flow-scripts.readthedocs.io · UserGuide.html](https://openroad-flow-scripts.readthedocs.io/en/latest/user/UserGuide.html)
- [klayout.org · lvs_overview.html](https://www.klayout.org/downloads/master/doc-qt5/manual/lvs_overview.html)

### 22. 시간에 따라 달라지는 방열: thermal RC와 과도 온도

[해설 읽기](../분야_topics/36-패키징열설계_packaging-thermal/해설_notes/열은바로빠져나가지않는다_thermal-rc-steady-transient.md)

- [analog.com · use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html](https://www.analog.com/en/resources/technical-articles/use-thermal-analysis-to-predict-an-ics-transient-behavior-and-avoid-overheating.html)
- [ti.com · GUID-D4E3F3F5-260D-45A1-862A-6E9A3052DC5A](https://www.ti.com/document-viewer/lit/html/SSZTB80/GUID-D4E3F3F5-260D-45A1-862A-6E9A3052DC5A)
- [ti.com · spra953d.pdf](https://www.ti.com/lit/an/spra953d/spra953d.pdf)
- [ti.com · 6243719539001](https://www.ti.com/video/6243719539001)

### 23. DB의 인덱스, 트랜잭션, SQL 집계

[해설 읽기](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/DB의인덱스트랜잭션SQL집계_indexes-transactions-and-aggregation.md)

- [docs.python.org · sqlite3.html](https://docs.python.org/3.12/library/sqlite3.html#transaction-control)
- [postgresql.org · functions-aggregate.html](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [postgresql.org · tutorial-transactions.html](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [sqlite.org · queryplanner.html](https://www.sqlite.org/queryplanner.html)

### 24. 복제본의 교집합: quorum과 일관성의 조건

[해설 읽기](../분야_topics/41-클라우드분산시스템_cloud-distributed/해설_notes/복제본의교집합_quorums-failures-and-consistency.md)

- [raft.github.io · raft.pdf](https://raft.github.io/raft.pdf)
- [allthingsdistributed.com · amazon-dynamo-sosp2007.pdf](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

### 25. 병렬 계산의 분할, reduction, 통신 비용

[해설 읽기](../분야_topics/42-고성능병렬계산_hpc-parallel/해설_notes/병렬계산의분할reduction통신비용_partition-reduction-and-communication.md)

- [hpc-tutorials.llnl.gov · collective_communication_routines](https://hpc-tutorials.llnl.gov/mpi/collective_communication_routines/)
- [hpc.llnl.gov · introduction-parallel-computing-tutorial](https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial)

### 26. 카메라 모델, 영상 필터, CV 검증

[해설 읽기](../분야_topics/43-컴퓨터비전_computer-vision/해설_notes/카메라모델영상필터CV검증_camera-filtering-and-validation.md)

- [docs.opencv.org · group__imgproc__filter.html](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html)
- [docs.opencv.org · group__calib3d.html](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)

### 27. 학습의 계산과 평가: loss, batch, 학습률, data leakage

[해설 읽기](../분야_topics/45-AI학습최적화_ai-training-optimization/해설_notes/학습의계산과평가_loss-batches-schedules-and-leakage.md)

- [developers.google.com · dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)
- [docs.pytorch.org · torch.optim.SGD.html](https://docs.pytorch.org/docs/2.14/generated/torch.optim.SGD.html)
- [docs.pytorch.org · torch.optim.lr_scheduler.CosineAnnealingLR.html](https://docs.pytorch.org/docs/2.14/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html)

### 28. RAG와 도구 실행: 검색, 근거, 평가의 경계

[해설 읽기](../분야_topics/46-AI응용에이전트평가_ai-agents-evaluation/해설_notes/RAG와도구실행_retrieval-tools-and-evaluation.md)

- [ai.google.dev · function-calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [learn.microsoft.com · retrieval-augmented-generation-overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [nlp.stanford.edu · evaluation-of-ranked-retrieval-results-1.html](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)
- [nlp.stanford.edu · tf-idf-weighting-1.html](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html)

### 29. 정수 양자화: scale, zero-point, 배포 오차

[해설 읽기](../분야_topics/47-엣지AI-TinyML_edge-tinyml/해설_notes/정수양자화_integer-quantization-and-deployment-error.md)

- [developers.google.com · quantization_spec](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec)
- [onnx.ai · onnx__QuantizeLinear.html](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html)

### 30. 소프트웨어 검증: 예제, 계약과 변환 성질

[해설 읽기](../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/소프트웨어검증_contracts-properties-metamorphic-testing.md)

- [hypothesis.readthedocs.io · introduction.html](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html)
- [swehb.nasa.gov · SWE-066+-+Perform+Testing](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695449/SWE-066+-+Perform+Testing)
- [nist.gov · metamorphic-testing-cybersecurity](https://www.nist.gov/publications/metamorphic-testing-cybersecurity)
- [teach.cs.toronto.edu · hypothesis.html](https://www.teach.cs.toronto.edu/~csc148h/notes/testing/hypothesis.html)

### 31. 좌표 변환에서 pixel까지: 동차 좌표와 rasterization

[해설 읽기](../분야_topics/49-그래픽스렌더링_graphics-simulation/해설_notes/좌표변환에서pixel까지_transforms-projection-and-rasterization.md)

- [modernrobotics.northwestern.edu · 3-3-1-homogeneous-transformation-matrices](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/)
- [registry.khronos.org · glspec46.core.pdf](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf)

### 32. 수치해석의 V&V: 수렴, 잔차, 보존을 따로 확인하기

[해설 읽기](../분야_topics/50-과학시뮬레이션_physical-scientific-simulation/해설_notes/수치해석의VV_verification-convergence-and-conservation.md)

- [grc.nasa.gov · overview.html](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html)
- [grc.nasa.gov · valassess.html](https://www.grc.nasa.gov/www/wind/valid/tutorial/valassess.html)
- [grc.nasa.gov · verassess.html](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html)

### 33. 보이지 않는 내부 상태를 검사하기: scan, ATPG와 fault coverage

[해설 읽기](../분야_topics/51-반도체테스트제조_test-manufacturing/해설_notes/보이지않는내부상태를검사하기_scan-atpg-fault-coverage.md)

- [community.cadence.com · training-insight-dive-into-atpg-flow-with-cadence-modus-dft-software-solution](https://community.cadence.com/cadence_blogs_8/b/di/posts/training-insight-dive-into-atpg-flow-with-cadence-modus-dft-software-solution)
- [synopsys.com · what-is-design-for-test.html](https://www.synopsys.com/glossary/what-is-design-for-test.html)

### 34. HTTP API의 계약: 멱등성, pagination, 입력 검증

[해설 읽기](../분야_topics/52-Web-API응용_web-api-applications/해설_notes/HTTPAPI의계약_http-idempotency-pagination-validation.md)

- [google.aip.dev · 158](https://google.aip.dev/158)
- [google.aip.dev · 193](https://google.aip.dev/193)
- [rfc-editor.org · rfc9110.html](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

### 35. 모바일 UI 상태: 생명주기와 늦게 도착한 결과

[해설 읽기](../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/모바일UI상태_ui-state-lifecycle-stale-results.md)

- [developer.android.com · saving-states](https://developer.android.com/topic/libraries/architecture/saving-states)
- [developer.android.com · viewmodel](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [kotlinlang.org · collect-latest.html](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect-latest.html)

### 36. 전류의 합으로 내적 계산하기: memristive PIM과 비이상성

[해설 읽기](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/해설_notes/전류의합으로내적계산하기_memristive-pim-dot-products.md)

- [research.ibm.com · the-hardware-behind-analog-ai](https://research.ibm.com/blog/the-hardware-behind-analog-ai)
- [research.ibm.com · demonstration-of-4-quadrant-analog-in-memory-matrix-multiplication-in-a-single-modulation](https://research.ibm.com/publications/demonstration-of-4-quadrant-analog-in-memory-matrix-multiplication-in-a-single-modulation)
- [nist.gov · hardware-accelerators-neural-networks](https://www.nist.gov/programs-projects/hardware-accelerators-neural-networks)

### 37. 측정에서 진단과 치료까지

[해설 읽기](../분야_topics/62-의공학의료AI_medical-engineering/해설_notes/측정에서진단과치료까지_medical-ai-evidence.md)

- [nibib.nih.gov · magnetic-resonance-imaging-mri](https://www.nibib.nih.gov/science-education/science-topics/magnetic-resonance-imaging-mri)
- [fda.gov · statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda)
- [doi.org · s41591-020-1034-x](https://doi.org/10.1038/s41591-020-1034-x)

## 데이터와 문서

[JSON 원본](확장출처_EXTENDED_SOURCES.json)은 문서 경로와 출처 URL을 연결하는 데이터입니다. 출처 문서 생성과 경로 검사에서 사용합니다. 읽기용 목록은 이 Markdown 문서입니다.

기준일은 자료 목록의 기록 날짜이며 모든 외부 페이지를 매번 재검증했다는 뜻은 아닙니다. 구체적인 인용 범위와 실행 여부는 각 해설과 검증 기록에 있습니다.

## English

This readable index groups the references by article. The JSON record retains article paths and source URLs for generation and path checks. Read the citations beside each claim for the scope of support; the inventory date is not a claim of continuous link verification.

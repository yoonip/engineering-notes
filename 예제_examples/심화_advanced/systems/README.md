# Systems 심화 실행 예제 / Advanced systems examples

## 한국어

Python 3.10 이상과 표준 라이브러리로 실행한다. 외부 package 설치는 필요하지 않다. 아래 명령은 저장소 루트 기준이다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" all
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

`all` 대신 표의 demo 이름을 넣으면 한 주제만 실행한다. `advanced_models.py`는 상태 전이와 계산을, `demo.py`는 입력과 출력 관찰을, `test_advanced_models.py`는 독립 참조·경계·순열 검사를 담는다. 출력 JSON은 매 실행에서 계산하며 임의로 작성한 측정 결과가 아니다. 예시 입력 중 실측이 아닌 값은 구성값으로 설명한다.

42개 테스트를 CPython 3.12.14와 Windows에서 실행했다. socket 예제는 실제 local socketpair와 selector를 사용했다. 그 밖의 큐·cache·scheduler·bus·debug·보안·UI 모델 결과를 Linux syscall, RTOS 보드, I2C 파형, GDB, MATLAB, HTTP 서버 또는 모바일 framework의 실행 결과로 보지 않는다. 보드 timing과 실제 toolchain은 각 문서의 별도 검증 범위를 따른다.

`ring_buffer.c`는 C11 단일 실행 흐름용 고정 큐다. C compiler 실행은 검증 결과에 포함하지 않았다. C11 toolchain이 있는 경우 이 디렉터리에서 다음처럼 실행할 수 있다.

```sh
cc -std=c11 -Wall -Wextra -Werror ring_buffer.c -o ring_buffer
./ring_buffer
```

## English

Use Python 3.10 or later and its standard library; no external packages are required. Run the commands above from the repository root. Replace `all` with a demo name below to run one topic. `advanced_models.py` contains transitions and computations, `demo.py` shows inputs and observations, and `test_advanced_models.py` provides independent references, boundaries, and permutation checks. JSON outputs are computed on each run. Nonmeasured illustration inputs are identified as constructed values.

All 42 tests ran on CPython 3.12.14 and Windows. The socket example exercised a real local socketpair and selector. Other queue, cache, scheduler, bus, debug, security, and UI model outputs do not establish execution on Linux syscalls, RTOS boards, I2C waveforms, GDB, MATLAB, HTTP servers, or mobile frameworks. Each article states the remaining target/tool verification boundary.

`ring_buffer.c` is a C11 fixed queue for one execution flow. C compilation is not part of the reported verification. The compiler commands above can be run from this directory with a C11 toolchain.

## 해설과 demo / Articles and demos

| 분야 / Topic | 해설 / Article | Demo |
| --- | --- | --- |
| 01 | [파이프역압력_pipe-backpressure](../../../분야_topics/01-linux-bash/해설_notes/파이프역압력_pipe-backpressure.md) | `pipe` |
| 02 | [내용기반빌드_content-addressed-build](../../../분야_topics/02-개발도구_git-development-tools/해설_notes/내용기반빌드_content-addressed-build.md) | `build` |
| 03 | [데이터와분할재현성_data-split-reproducibility](../../../분야_topics/03-python-jupyter/해설_notes/데이터와분할재현성_data-split-reproducibility.md) | `data` |
| 04 | [고정크기링버퍼_bounded-ring-buffer](../../../분야_topics/04-c-cpp-python/해설_notes/고정크기링버퍼_bounded-ring-buffer.md) | `ring` |
| 05 | [구간을지키는근찾기_safeguarded-root-finding](../../../분야_topics/05-과학계산_matlab-scientific/해설_notes/구간을지키는근찾기_safeguarded-root-finding.md) | `root` |
| 07 | [배치와캐시_memory-layout-locality](../../../분야_topics/07-컴퓨터공학기초_cs-foundations/해설_notes/배치와캐시_memory-layout-locality.md) | `cache` |
| 08 | [휴리스틱최단경로_astar-reopening](../../../분야_topics/08-알고리즘_problem-solving/해설_notes/휴리스틱최단경로_astar-reopening.md) | `astar` |
| 17 | [우선순위역전_priority-inheritance](../../../분야_topics/17-펌웨어-RTOS_firmware-rtos/해설_notes/우선순위역전_priority-inheritance.md) | `rtos` |
| 18 | [준비이벤트와레코드_poll-record-streams](../../../분야_topics/18-임베디드Linux_embedded-linux/해설_notes/준비이벤트와레코드_poll-record-streams.md) | `poll` |
| 19 | [접근을잡는관찰점_watchpoints-access-values](../../../분야_topics/19-시스템디버깅_openocd-debugging/해설_notes/접근을잡는관찰점_watchpoints-access-values.md) | `watch` |
| 20 | [I2C묶음전송_i2c-combined-transactions](../../../분야_topics/20-인터페이스통신_interfaces-communications/해설_notes/I2C묶음전송_i2c-combined-transactions.md) | `i2c` |
| 22 | [속도PI와포화_speed-pi-anti-windup](../../../분야_topics/22-로봇제어_robotics-boards/해설_notes/속도PI와포화_speed-pi-anti-windup.md) | `pi` |
| 27 | [쌍체비교와재현실험_paired-reproducible-experiments](../../../분야_topics/27-논문코드특허_papers-code-patents/해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md) | `experiment` |
| 28 | [변경영향과CI캐시_incremental-ci-cache](../../../분야_topics/28-자동화기술기록_automation-portfolio/해설_notes/변경영향과CI캐시_incremental-ci-cache.md) | `ci` |
| 38 | [인증후재전송검사_authenticated-replay-window](../../../분야_topics/38-보안암호하드웨어신뢰_security-cryptography/해설_notes/인증후재전송검사_authenticated-replay-window.md) | `replay` |
| 39 | [수식에서바이트코드_expression-bytecode](../../../분야_topics/39-컴파일러언어런타임_compilers-languages/해설_notes/수식에서바이트코드_expression-bytecode.md) | `parser` |
| 48 | [실패입력줄이기_property-counterexample-shrinking](../../../분야_topics/48-소프트웨어설계품질_software-quality/해설_notes/실패입력줄이기_property-counterexample-shrinking.md) | `property` |
| 52 | [버전조건부갱신_optimistic-concurrency-etag](../../../분야_topics/52-Web-API응용_web-api-applications/해설_notes/버전조건부갱신_optimistic-concurrency-etag.md) | `api` |
| 53 | [UI이벤트리듀서_ui-event-reducer](../../../분야_topics/53-모바일크로스플랫폼_mobile-crossplatform/해설_notes/UI이벤트리듀서_ui-event-reducer.md) | `ui` |

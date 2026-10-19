# 심화 실행 예제 | Advanced executable examples

수식과 상태 모델을 실제로 계산하는 예제를 모았습니다. 각 디렉터리의 README는 해당 해설, 실행 명령, 검산 방법을 연결합니다. Python 예제와 테스트는 표준 라이브러리로 실행하며, 도표를 다시 그릴 때만 Matplotlib이 필요합니다.

These examples compute the equations and state models in the advanced articles. Each directory links explanations, commands and independent checks. Python examples and tests use the standard library; regenerating plots additionally requires Matplotlib.

| 예제 / Examples | 주요 구현 / Implementations | 독립 검증 / Independent checks |
| --- | --- | --- |
| [회로와 하드웨어 / Circuits and hardware](hardware/README.md) | MNA, PDN, 고정소수점 RTL, QPSK, ADC, SRAM, credit flow, 열·보정 / thermal and calibration models | 회로 법칙, 전수 상태, 유리수, 다항식 나눗셈, 실제 RTL 시뮬레이션 / circuit laws, exhaustive states, rational arithmetic, polynomial division, RTL simulation |
| [시스템과 소프트웨어 / Systems and software](systems/README.md) | Ring buffer, A*, RTOS, I2C, parser, cache, replay window, API, UI | BFS, deque, 고정밀 근, AST, 순열·경계, 실제 socket / high-precision roots, permutations, boundaries, actual sockets |
| [AI와 데이터 / AI and data](ai_data/README.md) | MLP, attention, Adam, tiling, beam search, WAL, quantization, projection | 수치미분, 직접 합산, 독립 기준 구현, 실제 SQLite 연결 / numerical gradients, direct sums, independent references, actual SQLite connections |
| [수학·제어·추론 / Mathematics, control and reasoning](math_reasoning/README.md) | Ridge, PI, FEM, coupled modes, SAT, Bayes factor, input–output, standardization, timelines | 해석해·유리수·격자 수렴·전수 탐색 / analytic solutions, rational arithmetic, mesh convergence, exhaustive search |

## 통합 검사 | Integrated checks

저장소 루트에서 실행합니다. 기초·추론·확장·심화 모델을 별도 프로세스로 검사하므로 서로 다른 예제의 모듈 이름이 충돌하지 않습니다.

Run from the repository root. Separate processes isolate the foundation, reasoning, extended and advanced model suites.

```bash
python 예제_examples/run_checks.py --report results/verification.json
```

검사별 결과와 Python 버전은 [통합 기록](../VALIDATION.json)에, RTL·CLI 등의 실행 범위는 각 예제의 README와 결과 파일에 담았습니다. 이 통합 명령은 Python 모델 검사이며 RTL 도구 실행은 하드웨어 README의 별도 명령으로 수행합니다.

[The integrated record](../VALIDATION.json) lists suite results and Python versions. Individual READMEs and result files document RTL and CLI execution. The integrated command checks Python models; the hardware README provides the separate RTL-tool command.

[심화 해설 60편 / 60 advanced articles](../../공학기초_foundations/심화학습_ADVANCED.md)

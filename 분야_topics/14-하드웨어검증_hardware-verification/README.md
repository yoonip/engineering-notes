# 하드웨어 검증 | Hardware Verification

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

하드웨어 검증은 설계가 명세대로 동작하는지 확인하는 과정이다. 테스트벤치는 입력 자극과 기준 모델, 자동 비교와 오류 보고를 연결해 같은 검사를 반복할 수 있게 한다.

## 시뮬레이션과 coverage

Directed test는 특정 동작을 직접 자극하고, constrained-random test는 제약 안에서 다양한 입력을 만든다. 코드 coverage는 실행된 코드 구조, 기능 coverage는 명세에서 정한 상황이 얼마나 관찰되었는지 다룬다. 수치가 높아도 비교 기준이 잘못되면 기능 오류를 놓칠 수 있다.

## Assertion과 formal

SystemVerilog Assertions는 신호 관계와 시간 조건을 표현한다. 예를 들어 요청 뒤 정해진 시간 안에 응답해야 한다는 규칙을 쓸 수 있다. Formal 검증은 가정과 속성 아래에서 가능한 상태를 논리적으로 분석한다. 증명 결과는 설정한 환경 가정과 속성의 범위 안에서 해석한다.

UVM은 검증 구성요소와 재사용을 위한 방법론·라이브러리다. Verilator·Icarus Verilog·Questa·Xcelium·VCS는 지원 범위가 다른 시뮬레이션 도구이고, GTKWave는 파형을 보는 도구다. cocotb는 Python 기반 검증, SymbiYosys는 공개 formal 흐름에서 쓰인다. 회귀 검증은 변경 뒤 기존 기능이 유지되는지 반복 확인한다.

## 관련 기술

UVM, SVA, cocotb, Verilator, Icarus Verilog, GTKWave, Questa, Xcelium, VCS, SymbiYosys, Formal/Equivalence

## 참고 자료

- [cocotb documentation](https://docs.cocotb.org/en/stable/)
- [Verilator documentation](https://verilator.org/guide/latest/)

## 기초 해설

- [검증에서 무엇을 확인했는가: assertion, coverage와 formal](해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md)

## English

Hardware verification checks a design against its specification. A testbench connects input stimulus, a reference model, automatic comparisons, and error reporting, making the checks repeatable beyond visual inspection of a few waveforms.

### Simulation and coverage

Directed tests exercise specific behaviors. Constrained-random tests generate varied inputs within a set of rules. Code coverage measures exercised implementation structures, while functional coverage tracks situations defined by the specification. High coverage can still miss bugs if the expected-result model is wrong.

### Assertions and formal verification

SystemVerilog Assertions express signal relationships and timing conditions, such as a response arriving within a bounded time after a request. Formal verification analyzes possible states under explicit assumptions and properties. The relevance of the result depends on whether those assumptions match the intended environment.

UVM provides a methodology and library for reusable verification components. Verilator, Icarus Verilog, Questa, Xcelium, and VCS have different simulation capabilities; GTKWave displays waveforms. cocotb supports Python-based testbenches, and SymbiYosys supports open formal workflows. Regression testing repeats checks after changes to catch unintended effects.

### Foundation article

- [검증에서 무엇을 확인했는가: assertion, coverage와 formal](해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md#english)

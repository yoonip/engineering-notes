# 하드웨어 검증 | Hardware Verification

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

하드웨어 검증은 설계가 명세대로 동작하는지 확인하는 과정입니다. 테스트벤치는 입력 자극과 기준 모델, 자동 비교와 오류 보고를 연결해 같은 검사를 반복할 수 있게 합니다.

## 시뮬레이션과 coverage

Directed test는 특정 동작을 직접 자극하고, constrained-random test는 제약 안에서 다양한 입력을 만듭니다. 코드 coverage는 실행된 코드 구조, 기능 coverage는 명세에서 정한 상황이 얼마나 관찰되었는지 다룹니다. 수치가 높아도 비교 기준이 잘못되면 기능 오류를 놓칠 수 있습니다.

## Assertion과 formal

SystemVerilog Assertions는 신호 관계와 시간 조건을 표현합니다. 예를 들어 요청 뒤 정해진 시간 안에 응답해야 한다는 규칙을 쓸 수 있습니다. Formal 검증은 가정과 속성 아래에서 가능한 상태를 논리적으로 분석합니다. 증명 결과는 설정한 환경 가정과 속성의 범위 안에서 해석합니다.

UVM은 검증 구성요소와 재사용을 위한 방법론·라이브러리입니다. Verilator·Icarus Verilog·Questa·Xcelium·VCS는 지원 범위가 다른 시뮬레이션 도구이고, GTKWave는 파형을 보는 도구입니다. cocotb는 Python 기반 검증, SymbiYosys는 공개 formal 흐름에서 쓰입니다. 회귀 검증은 변경 뒤 기존 기능이 유지되는지 반복 확인합니다.

## 수락한 전송만 기준 모델에 넣습니다

입력 값이 보였다는 사실과 회로가 그 입력을 수락했다는 사실은 다릅니다. 자체 예제에서는 클록 상승 에지 직전의 `valid`와 `ready`가 모두 1이고 reset이 아닐 때만 한 건을 수락한다고 정합니다. valid는 보낼 값이 있다는 표시이고 ready는 받을 수 있다는 표시입니다. ready가 0인 동안 같은 항목을 유지하면 valid가 여러 에지에서 1이어도 전송은 한 건입니다.

아래는 직접 구성한 신호 관측 목록입니다. 사이클 2·3의 항목 102는 대기 중이며 사이클 4에서 한 번만 수락합니다. reset이 우선이라는 가정도 입력에 포함했습니다.

```python
# 각 튜플은 (사이클, reset, valid, ready, 항목ID)이며 ()로 고정 묶음을 만듭니다.
edges = [(0, 1, 1, 1, 101), (1, 0, 1, 1, 101), (2, 0, 1, 0, 102),
         (3, 0, 1, 0, 102), (4, 0, 1, 1, 102), (5, 0, 0, 1, 103), (6, 0, 1, 1, 103)]
accepted = [(cycle, item) for cycle, reset, valid, ready, item in edges
            if not reset and valid and ready]  # 목록 내포에서 수락 조건을 만족한 항목만 남깁니다.
wrong = [item for _, reset, valid, _, item in edges if not reset and valid]  # 잘못된 대조는 ready를 무시합니다.
print(accepted)  # [(1, 101), (4, 102), (6, 103)]으로 세 건입니다.
print(wrong)  # [101, 102, 102, 102, 103]으로 같은 항목을 중복 계산합니다.
```

출력에서도 valid가 1인 모든 사이클을 새 결과로 세면 대기 중인 같은 결과를 중복 비교할 수 있습니다. 반대로 `zip(expected, actual)`만 비교하면 짧은 쪽 끝에서 반복이 멈춰 마지막 결과 누락을 놓칠 수 있습니다. 항목별 값·순서·수락 시각과 전체 개수, 마지막에 남은 기대 결과를 함께 확인해야 합니다. ID가 없는 순서 보장 인터페이스라면 수락 순서의 큐로 대응시킬 수 있습니다.

관측 시점도 계약입니다. 에지 직전의 입력·수락 상태와 순차논리 갱신 뒤의 출력을 섞으면 한 사이클 차이가 생깁니다. [cocotb Timing Model](https://docs.cocotb.org/en/stable/timing_model.html#valuechange-risingedge-fallingedge)은 에지 감지와 그 에지에 반응한 HDL 평가 완료를 구분합니다. 에지 감지 직후 출력이 갱신됐다고 가정하지 않고 사용하는 시뮬레이터와 테스트벤치의 샘플링 시점을 명시합니다. 해당 문서는 2026-10-21에 열람했으며, 위 Python 목록 계산에서 cocotb나 HDL을 실행한 것은 아닙니다.

[RTL과 기준 모델 비교 사례](../../설계와검증사례_engineering-cases/RTL내적기의비트폭과전송계약_rtl-dot-handshake.md)는 실제 HDL 컴파일·실행과 Python 기대값을 연결합니다. 위 일곱 에지는 전송 수락의 산술을 설명하는 별도 교육 예제입니다. 기능 시뮬레이션의 값·순서 일치는 실제 칩의 클록 주파수·setup/hold·CDC·전력 검증과 구분합니다.

## 관련 기술

UVM, SVA, cocotb, Verilator, Icarus Verilog, GTKWave, Questa, Xcelium, VCS, SymbiYosys, Formal/Equivalence

## 참고 자료

- [cocotb documentation](https://docs.cocotb.org/en/stable/)
- [Verilator documentation](https://verilator.org/guide/latest/)

## 기초 해설

- [Assertion·coverage·formal의 검증 범위](해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md)

## English

Hardware verification checks a design against its specification. A testbench connects input stimulus, a reference model, automatic comparisons, and error reporting, making the checks repeatable beyond visual inspection of a few waveforms.

### Simulation and coverage

Directed tests exercise specific behaviors. Constrained-random tests generate varied inputs within a set of rules. Code coverage measures exercised implementation structures, while functional coverage tracks situations defined by the specification. High coverage can still miss bugs if the expected-result model is wrong.

### Assertions and formal verification

SystemVerilog Assertions express signal relationships and timing conditions, such as a response arriving within a bounded time after a request. Formal verification analyzes possible states under explicit assumptions and properties. The relevance of the result depends on whether those assumptions match the intended environment.

UVM provides a methodology and library for reusable verification components. Verilator, Icarus Verilog, Questa, Xcelium, and VCS have different simulation capabilities; GTKWave displays waveforms. cocotb supports Python-based testbenches, and SymbiYosys supports open formal workflows. Regression testing repeats checks after changes to catch unintended effects.

### Match accepted transactions

In the constructed ready/valid contract, reset takes priority and a transaction is accepted only when valid and ready are both high at the active edge. Seven sample edges contain three accepted items; ignoring ready counts five and duplicates item 102. Compare values, order, timing and total count, including unmatched final expectations. Specify sampling before and after sequential updates. The Python trace arithmetic is separate from the linked HDL execution case.

### Foundation article

- [Assertion·coverage·formal의 검증 범위](해설_notes/검증에서무엇을확인했는가_assertions-coverage-formal.md#english)


## 심화 해설 | Advanced article

- [개수는 맞아도 순서가 다른 경우: 작은 모델의 전수검사](해설_notes/불변식의빈틈_model-checking.md) · [English](해설_notes/불변식의빈틈_model-checking.md#english)

# 다른 회로, 같은 상태 전이: equivalence를 확인하는 기준

[EDA 목차](../README.md) · [Python 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [RTL](../../../예제_examples/심화_advanced/hardware/counter_equiv.sv) · [실행기](../../../예제_examples/심화_advanced/hardware/run_rtl.py)

## 한국어

### 코드 모양이 달라도 같은 회로일 수 있습니다

`q+1`로 쓴 카운터와 각 비트의 XOR·carry를 직접 연결한 카운터는 소스 모양이 다릅니다. 중요한 것은 같은 상태와 입력에서 다음 상태와 관찰 가능한 출력이 같으냐는 것입니다. 합성 도구도 RTL을 gate 구조로 바꾸므로 이런 비교가 필요합니다. 다만 기능이 같다는 결과는 지연·전력·배치가 같다는 뜻이 아닙니다.

[YosysHQ EQY](https://yosyshq.readthedocs.io/projects/eqy/en/latest/)는 formal equivalence 도구의 역할을 설명합니다. [OpenROAD flow 문서](https://openroad-flow-scripts.readthedocs.io/en/latest/user/UserGuide.html)는 합성, 물리 구현, DRC·LVS를 구분합니다. 이 예제는 두 표현의 카운터를 Python으로 전수 비교하고 실제 RTL 시뮬레이션으로 대조합니다. EQY·Yosys 합성이나 physical flow를 실행했다는 주장은 하지 않습니다.

### 카운터의 기능 계약

8비트 상태 q, enable e, synchronous active-high reset r을 둡니다. reset은 enable보다 우선합니다. reset이 아니면 enable=1에서만 1 증가하고 255 다음은 0입니다.

```math
q'=\begin{cases}
0&r=1\\
(q+1)\bmod256&r=0,\ e=1\\
q&r=0,\ e=0.
\end{cases}
```

bit-slice 표현에서는 carry0=e, 다음 비트 $`q'_k=q_k\oplus carry_k`$, $`carry_{k+1}=q_k\land carry_k`$입니다. 가장 낮은 비트는 매 enable마다 뒤집힙니다. 그 위 비트는 아래 비트가 모두 1이고 enable일 때만 뒤집힙니다. 이는 이진수 덧셈에서 올림이 전파되는 규칙과 같습니다. 최상위 carry를 버리면 modulo 256이 됩니다.

### 초기 상태와 상태 전이의 동등성

두 모델의 초기 상태가 같고 모든 q,e,r에서 next-state 함수가 같다고 하겠습니다. 첫 cycle 뒤 상태가 같고, 같은 함수와 같은 입력을 다시 적용하므로 두 번째 상태도 같습니다. 이 귀납을 반복하면 임의 길이 입력열에서 같다는 결론을 얻습니다. Python 테스트는 256×2×2=1024개 상태·입력 조합을 전부 비교합니다.

하지만 실제 RTL의 uninitialized X, reset 종류, enable의 알려지지 않은 값, blocking/nonblocking scheduling은 0/1 정수 함수에 모두 들어 있지 않습니다. 이 때문에 Python 전수 비교만으로 실제 RTL equivalence proof를 했다고 부르지 않습니다. RTL에서는 reset으로 알려진 상태를 만든 뒤 같은 clock edge에서 비교합니다.

### 실제 Icarus 실행

```bash
python demo.py --case equivalence
python -m unittest -v test_models.HardwareModels.test_counter_all_states_inputs test_models.HardwareModels.test_counter_reset_and_wrap
python run_rtl.py
```

`counter_equiv.sv`의 첫 module은 덧셈 연산자로, 두 번째는 bit-slice XOR/AND로 next state를 만듭니다. testbench는 reset 1 cycle, 연속 enable 256 cycle로 한 바퀴, LFSR 입력으로 reset·enable을 바꾸는 10000 cycle을 실행합니다. 두 RTL 출력과 별도 scoreboard를 매 edge의 nonblocking 갱신 뒤 비교합니다. 총 10257 cycle이 Icarus 12.0에서 통과했습니다.

| 검증 | 이번 예제가 실제 한 것 | 결과가 보장하지 않는 것 |
|---|---|---|
| Python 전수 비교 | 1024개 전이 | HDL scheduling·X 의미 |
| RTL 시뮬레이션 | 10257 cycle | 모든 RTL trace의 formal proof |
| 합성 후 equivalence | 실행하지 않음 | gate 변환의 등가성 |
| 구현 후 STA·physical check | 실행하지 않음 | timing·DRC·LVS |

### 합성 후 비교로 확장할 때

실제 flow에서는 gold RTL, gate netlist, library cell의 기능 모델과 clock/reset 조건을 고정합니다. scan·test enable·clock gating 조건, 메모리 초기화, black box, unreachable state 처리도 명시합니다. state encoding이나 retiming으로 레지스터 대응이 달라지면 단순 신호별 equality보다 정교한 매칭이 필요합니다. `PASS`뿐 아니라 unmatched·unproven partition과 assumption을 함께 읽습니다.

equivalence가 통과해도 setup/hold, CDC, analog interface나 layout 규칙은 별도 검사입니다. 반대로 timing이 좋아졌다고 기능이 보존됐다는 뜻도 아닙니다. 이 예제는 작은 회로에서 어떤 동일성을 확인했는지, 그리고 어느 도구 단계까지 실제 실행했는지를 구분하는 출발점입니다.

## English

### Different descriptions can implement the same function

A counter written as `q+1` can match one built from explicit XOR and carry logic. Equivalence asks whether equal states and inputs produce equal next states and observable outputs. It does not imply equal delay, power or placement.

[YosysHQ EQY](https://yosyshq.readthedocs.io/projects/eqy/en/latest/) describes formal equivalence checking, while [OpenROAD's flow guide](https://openroad-flow-scripts.readthedocs.io/en/latest/user/UserGuide.html) separates synthesis, physical implementation and DRC/LVS. This example exhaustively compares Python state functions and runs actual RTL simulation. It does not report an EQY proof, Yosys synthesis or physical-flow execution.

### Contract and bit-level derivation

The state is an eight-bit q. Reset is synchronous, active high and dominant over enable. Otherwise enable increments modulo 256; a disabled counter holds its state. For a bit-slice implementation, carry0=enable, the next bit is qk XOR carryk, and the outgoing carry is qk AND carryk. A bit toggles only when enable and all lower bits propagate a carry. Dropping the final carry produces modulo-256 arithmetic.

If initial states agree and both next-state functions agree for every state and input, induction establishes agreement for every finite input sequence. The Python test compares all 256×2×2=1024 state/input combinations. Reset, hold and wrap-around also have explicit checks.

This integer model does not include HDL unknown values, uninitialized registers or scheduling semantics. Accordingly, it is not by itself a proof about the actual RTL. The RTL comparison first establishes known state with reset and checks after nonblocking updates.

### Executed RTL comparison

Run the commands above. One module uses the addition operator; the other uses XOR/AND carry slices. The testbench performs one reset cycle, 256 enabled cycles and 10000 LFSR-driven reset/enable cycles. Both outputs are compared with a separate scoreboard after each clock edge. Icarus 12.0 passed all 10257 cycles.

Thus the performed checks are 1024 exhaustive Python transitions and a finite 10257-cycle RTL simulation. Neither is a reported post-synthesis equivalence proof, and no STA, DRC or LVS was executed for these examples.

### Extending to a synthesis flow

A post-synthesis comparison needs fixed gold RTL, gate netlist, functional library models and clock/reset assumptions. Specify scan/test modes, clock gating, memory initialization, black boxes and unreachable-state treatment. State recoding or retiming can require more than a register-name equality check. Examine unmatched or unproven partitions and assumptions as well as a final status.

Even a formal equivalence pass leaves setup/hold, CDC, analog interfaces and physical rules to other analyses. Improved timing likewise does not establish functional preservation. The example keeps the checked relation and the actually executed tool stage explicit.

## 출처 / Sources

- YosysHQ, *EQY Documentation*: formal hardware equivalence and configuration boundaries.
- OpenROAD Team, *Flow User Guide*: synthesis, implementation and physical verification roles. Links appear above.

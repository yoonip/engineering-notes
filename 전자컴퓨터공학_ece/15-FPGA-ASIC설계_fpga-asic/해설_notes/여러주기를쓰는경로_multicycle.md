# 여러 주기를 쓰는 경로: multicycle과 hold 관계

[FPGA·ASIC 목차](../README.md) · [시간 관계 모델](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 느린 계산과 느린 클록은 다릅니다

클록은 10 ns마다 뛰지만 어떤 레지스터는 clock enable이 세 번에 한 번만 켜질 수 있습니다. 중간 에지에서는 데이터를 사용하지 않고 세 번째 에지에서만 받는 구조라면, timing 분석에도 3주기의 launch–capture 간격을 반영합니다. 조합 회로에 허용되는 지연은 이 간격에서 clock-to-Q, setup time 등 필요한 시간을 뺀 값입니다. multicycle은 이 기능상의 관계를 timing 도구에 알려 주는 제약입니다. 계산이 느려서 timing을 못 맞췄다는 이유만으로 주기를 늘려 적는 해결책은 아닙니다.

이 글은 launch와 capture가 같은 주파수·같은 위상의 한 clock이고, 관련 enable이 N주기마다 함께 열리며 중간 capture가 기능적으로 무효인 경우만 다룹니다. 다른 주파수, 위상 이동, latch, CDC에는 같은 숫자 규칙을 그대로 적용하지 않습니다. [AMD의 enable 기반 예](https://docs.amd.com/r/2020.2-English/ug1387-acap-hardware-ip-platform-dev-methodology/Relaxing-the-Setup-Requirement-While-Keeping-Hold-Unchanged?contentId=mDPen7K8UpE03COFvi9s_g)와 [Altera Timing Analyzer 25.3](https://docs.altera.com/r/docs/683243/25.3/quartus-prime-pro-edition-user-guide-timing-analyzer/relaxing-setup-with-multicycle-set_multicyle_path)의 setup/hold 쌍을 교차 확인했습니다.

### setup edge를 옮기면 hold도 함께 살펴야 합니다

launch edge를 0으로 두고 capture clock의 도착이 launch보다 s만큼 늦다고 정의합니다. clock-to-Q, 조합 지연, setup/hold time과 uncertainty U는 모두 같은 시간 단위입니다. 기본 한 주기 setup slack은 $`T+s-t_{cq,max}-d_{max}-t_{setup}-U`$입니다. N주기 capture로 바꾸면 다음이 됩니다.

```math
Slack_{setup}=NT+s-t_{cq,max}-d_{max}-t_{setup}-U.
```

같은 clock의 일반적인 multicycle 의미에서 setup만 N으로 옮기면 연동된 hold 검사 edge가 (N−1)T로 이동합니다. hold multiplier H로 이를 되돌리는 단순 모델은 다음과 같습니다.

```math
t_{hold,edge}=(N-1-H)T,
\quad Slack_{hold}=t_{cq,min}+d_{min}-t_{hold,edge}-s-t_{hold}-U.
```

H=N−1이면 hold edge는 다시 0입니다. setup만 완화하고 원래 hold를 유지하는 의도가 이 경우에 해당합니다. 양의 skew는 setup에는 도움이 되지만 hold에는 불리하다는 부호도 확인할 수 있습니다.

### 숫자로 보는 paired constraint

T=10 ns, s=0.1 ns, $`t_{cq,max}=1`$, $`d_{max}=12`$, setup=1 ns, $`t_{cq,min}=0.3`$, $`d_{min}=0.5`$, hold=0.2 ns, U=0이라 하겠습니다.

| 설정 | setup slack | hold slack |
|---|---:|---:|
| 기본 N=1, H=0 | −3.9 ns | 0.5 ns |
| N=3만 지정, H=0 | 16.1 ns | −19.5 ns |
| N=3, H=2 | 16.1 ns | 0.5 ns |

setup이 좋아졌는데 hold가 갑자기 매우 나빠진 이유는 배선이 변해서가 아니라 검사 edge의 의미가 달라졌기 때문입니다. 같은 clock과 명확히 한정한 레지스터 집합을 대상으로 하는 개념적인 Tcl 예는 다음과 같습니다.

```tcl
set_multicycle_path 3 -setup -from [get_cells src_reg*] -to [get_cells dst_reg*]; # []는 셀 목록을 구하고, setup 검사를 3주기 간격으로 지정합니다.
set_multicycle_path 2 -hold  -from [get_cells src_reg*] -to [get_cells dst_reg*]; # hold 에지를 2주기 되돌려 원래 같은 에지 검사를 유지합니다.
```

`get_cells`와 register matching, hierarchy 표기, start/end 기본값은 사용하는 도구에서 확인해야 합니다. 특히 clock 전체에 예외를 주면 의도하지 않은 다른 경로까지 완화될 수 있습니다. 먼저 정확한 startpoint와 endpoint 목록이 잡혔는지 보고, 변경 전후의 launch/capture edge를 timing report에서 읽습니다.

### 실행 검산과 실제 적용 조건

```bash
python demo.py --case multicycle
python -m unittest -v test_models.HardwareModels.test_multicycle_setup_and_hold
```

참조모델은 N=3이 setup slack을 2T 늘리고, H=2를 함께 주면 원래 hold slack이 보존됨을 확인합니다. H=0은 hold 여유를 2T 줄이는 반례로 남깁니다. 이 검산은 edge 회계에 대한 Python 계산이며 실제 netlist STA 실행은 아닙니다.

기능 검증에서는 중간 주기에 destination이 값을 사용하지 않는지, source enable과 destination enable이 정확히 같은 규약을 따르는지, reset 후 첫 enable의 위상이 맞는지를 확인합니다. 값이 매 주기 바뀌거나 destination이 중간 결과를 사용한다면 multicycle 예외가 실제 오류를 가릴 수 있습니다. 최종 판단에는 min/max corner, OCV·uncertainty·clock routing을 포함한 구현 후 STA가 필요합니다. 예외 제약은 회로의 기능을 바꾸지 않습니다.

## English

### A slow operation is not necessarily a slow clock

A clock can tick every 10 ns while a register group enables once every three cycles. If intermediate captures are unused and the destination accepts data only on the third edge, a multicycle constraint communicates the three-period launch–capture interval. The available combinational delay excludes clock-to-Q, setup time and other timing adjustments. It is not justified merely because an otherwise single-cycle path misses timing.

This treatment assumes one same-frequency, same-phase clock, matching enables every N cycles and functionally irrelevant intermediate captures. Different frequencies, shifted clocks, latches and CDC require their own edge analysis. The paired setup/hold interpretation is checked against [AMD's enable-based example](https://docs.amd.com/r/2020.2-English/ug1387-acap-hardware-ip-platform-dev-methodology/Relaxing-the-Setup-Requirement-While-Keeping-Hold-Unchanged?contentId=mDPen7K8UpE03COFvi9s_g) and [Altera Timing Analyzer 25.3](https://docs.altera.com/r/docs/683243/25.3/quartus-prime-pro-edition-user-guide-timing-analyzer/relaxing-setup-with-multicycle-set_multicyle_path).

### Deriving the edge relationships

Let launch occur at zero and positive skew s mean that the capture clock arrives later. With all values in the same time unit, N-cycle setup slack is $`NT+s-t_{cq,max}-d_{max}-t_{setup}-U`$. In the common same-clock interpretation, shifting setup to N cycles also shifts the associated hold edge to (N−1)T. A hold adjustment H moves that edge to $`(N-1-H)T`$. Hold slack then equals minimum data arrival minus that edge, skew, hold time and uncertainty, as displayed above.

Choosing H=N−1 restores the original zero-edge hold relationship. Positive skew improves setup slack and worsens hold slack. These signs are useful checks on the derivation.

### Numerical example and constraint scope

For T=10 ns, s=0.1 ns, maximum clock-to-Q 1 ns, maximum combinational delay 12 ns and setup 1 ns, the ordinary setup slack is −3.9 ns. Minimum clock-to-Q 0.3 ns, minimum delay 0.5 ns and hold 0.2 ns give hold slack 0.5 ns, with zero uncertainty.

Setting setup to three cycles increases setup slack to 16.1 ns. Without the paired hold adjustment, the modeled hold slack becomes −19.5 ns. Adding hold multiplier two restores 0.5 ns. No routing changed: the timing edge interpretation changed.

The conceptual Tcl pair above must be adapted to the tool's object matching, hierarchy and start/end conventions. A clock-wide exception can affect unintended paths. Inspect actual startpoints, endpoints and reported launch/capture edges before accepting the result.

### Checks and physical implementation

Run the demo and named test above. They independently check the expected setup improvement of 2T, preserved hold for H=2 and worsened hold for H=0. This is a Python edge-accounting model, not netlist STA.

Functional verification must confirm that intermediate destination captures are unused, that source and destination enables obey the intended schedule and that reset preserves the first enabled edge. A changing source or an intermediate consumer can invalidate the exception. Final implementation still needs min/max-corner STA with clock routing, variation and uncertainty. A timing exception does not change circuit behavior.

## 출처 / Sources

- AMD, *UG1387*, 2020.2 (2021-03-26), “Relaxing the Setup Requirement While Keeping Hold Unchanged”: relaxing setup while retaining hold for clock-enabled paths.
- Altera, *Quartus Prime Pro Timing Analyzer 25.3*, 2026-09-03: N setup and N−1 hold examples. Links are given above.

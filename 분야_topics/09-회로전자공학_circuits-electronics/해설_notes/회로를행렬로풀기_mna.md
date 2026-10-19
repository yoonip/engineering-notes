# 회로를 행렬로 풀기: Modified Nodal Analysis

[회로·전자공학 목차](../README.md) · [실행 코드](../../../예제_examples/심화_advanced/hardware/models.py) · [검산](../../../예제_examples/심화_advanced/hardware/test_models.py)

## 한국어

### 전압을 모르는 곳마다 식을 하나씩

저항 두 개의 분압은 암산으로도 풀 수 있다. 하지만 전압원이 여러 노드 사이에 떠 있고 가지가 늘어나면, 식을 빠뜨리지 않고 만드는 방법이 필요하다. 노드 해석은 각 접점에서 들어오는 전류와 나가는 전류가 같다는 KCL을 쓴다. MNA는 여기에 전압원을 흐르는 전류도 미지수로 넣는다. 전압원이 전류를 정해 주지 않는 문제를 미지수 하나와 전압 조건 하나를 더해서 해결하는 셈이다. 이 구성과 전압원 연결 부호는 [TU Delft의 MNA 설명](https://analog-electronics.tudelft.nl/webbook/SED/_build/html/network_theory/NetworkTheory-1_Modified_Nodal_Analysis.html)에서 확인할 수 있다.

이 글의 회로는 선형 DC 저항, 독립 전압원, 독립 전류원으로 제한한다. 기준 노드 0의 전압을 0 V로 잡는다. 전압 단위는 V, 전류는 A, 저항은 Ω, conductance는 S다. 기준 노드는 계산의 출발점이며 회로도에 그려진 모든 전압원의 음극이 접지라는 뜻은 아니다.

### 저항과 전원을 행렬에 넣는 과정

노드 p에서 q로 흐르는 저항 전류는 다음과 같다.

```math
i_{pq}=g(v_p-v_q),\qquad g=1/R.
```

p의 KCL에는 $`+gv_p-gv_q`$, q의 KCL에는 $`-gv_p+gv_q`$가 들어간다. 따라서 저항 하나가 G의 두 대각 성분에 +g, 두 교차 성분에 −g를 더한다. 한쪽이 접지면 그 행과 열은 만들지 않는다. 전류원이 p에서 q로 I를 보내면 우변의 p에는 −I, q에는 +I를 더한다. 우변은 노드에 주입되는 전류로 정의했기 때문이다.

전압원 E의 양극이 p, 음극이 q라면 가지 전류 $`i_E`$를 p→q 방향으로 정의한다. p의 KCL에 $`+i_E`$, q의 KCL에 $`-i_E`$를 넣고 $`v_p-v_q=E`$를 추가한다. 독립 전압원만 있는 경우 전체 식은 다음 형태가 된다.

```math
\begin{bmatrix}G&B\\B^T&0\end{bmatrix}
\begin{bmatrix}v\\i_E\end{bmatrix}
=\begin{bmatrix}j\\e\end{bmatrix}.
```

G는 저항 연결, B는 전압원의 위치와 방향, j는 전류원 주입, e는 전압원 값을 나타낸다. 실제 계산에서는 역행렬을 직접 만들기보다 선형계를 푼다. [ngspice 매뉴얼](https://ngspice.sourceforge.io/docs/ngspice-manual.pdf)의 소자 표기, 독립 전원, 행렬 기반 해석과도 대조했다. 여기의 작은 dense solver는 교육용이며 ngspice의 sparse solver나 비선형 반복 해석을 재현하지 않는다.

### 숫자로 부호까지 확인하기

3 V 전압원, 위쪽 1 kΩ, 아래쪽 2 kΩ의 분압 회로에서 $`v_1=3`$, $`v_2=2`$ V다. 전압원 전류를 양극→음극으로 잡으면 −1 mA가 나온다. 음수는 전압원이 반대 방향으로 전류를 내보낸다는 뜻이다.

| 확인량 | 계산 | 결과 |
|---|---|---|
| 중간 노드 KCL | (3−2)/1000 − 2/2000 | 0 A |
| 위 저항 전력 | (3−2)²/1000 | 1 mW |
| 아래 저항 전력 | 2²/2000 | 2 mW |
| 전압원 흡수 전력 | 3×(−1 mA) | −3 mW |

흡수 전력 합이 0이므로 저항이 소비한 전력을 전원이 공급한다. 노드 1과 2가 각각 1 kΩ으로 접지되고 그 사이에 2 V 전압원이 있으면 해는 +1 V, −1 V다. 떠 있는 전압원의 두 단자를 모두 접지로 처리하면 이 결과를 얻을 수 없다.

### 구현과 독립 검산

예제 폴더에서 다음 명령을 실행한다.

```bash
python demo.py --case mna
python -m unittest -v test_models.HardwareModels.test_mna_divider_and_power test_models.HardwareModels.test_mna_floating_source test_models.HardwareModels.test_mna_current_and_singular
```

`mna()`는 소자별 stamp를 합치고 부분 피벗 소거법을 호출한다. 검산은 같은 행렬을 다시 풀어 비교하는 데 그치지 않는다. 손계산 분압비, 각 노드 KCL, 모든 소자의 전력 합, 떠 있는 전압원의 대칭해를 각각 확인한다. 접지와 연결되지 않은 저항망은 절대 전압이 정해지지 않으므로 특이행렬 오류를 낸다.

아주 작은 저항과 큰 저항이 함께 있으면 단위 스케일과 conditioning도 문제다. 코드의 절대 피벗 경계는 일반적인 회로 수치 안정성을 보장하지 않는다. 커패시터·인덕터의 과도 응답은 적분식과 초기조건을, 다이오드·MOS는 동작점 반복과 소자 모델을 추가해야 한다. 여기서 확인한 결과는 선형 참조모델의 결과이며 실제 회로 측정이나 SPICE 실행 결과는 아니다.

## English

### One equation for each unknown node voltage

A two-resistor divider is easy to solve by hand. Larger networks need a systematic way to assemble equations without missing a branch. Nodal analysis applies KCL at each junction. Modified Nodal Analysis adds the currents through voltage sources to the unknown vector, then adds the sources' voltage constraints. [TU Delft's MNA chapter](https://analog-electronics.tudelft.nl/webbook/SED/_build/html/network_theory/NetworkTheory-1_Modified_Nodal_Analysis.html) explains this construction and its connection signs.

The model here contains linear DC resistors and independent voltage and current sources. Node 0 is the reference at 0 V. Voltages, currents, resistances and conductances use V, A, Ω and S. Selecting a reference does not ground the negative terminal of every source.

### From branch laws to matrix stamps

A resistor from p to q carries $`i_{pq}=g(v_p-v_q)`$, with $`g=1/R`$. Its two KCL equations contribute +g to the two diagonal entries of G and −g to the cross entries. A grounded terminal has no separate row or column. A current source carrying I from p to q adds −I at p and +I at q on the right-hand side, which is defined as injected current.

For a voltage source E, define its current from its positive terminal p toward its negative terminal q. Add that current to p's outgoing KCL, subtract it at q, and append $`v_p-v_q=E`$. With independent voltage sources, the matrix is $`[G\ B;B^T\ 0][v;i_E]=[j;e]`$, as displayed above. G represents resistors, B source incidence, j injected currents and e source voltages. Solve the linear system rather than explicitly computing its inverse. The [ngspice manual](https://ngspice.sourceforge.io/docs/ngspice-manual.pdf) provides an independent check on element notation, independent sources and matrix-based analysis. This small dense solver does not reproduce ngspice's sparse or nonlinear algorithms.

### Numerical example and signs

A 3 V source with a 1 kΩ upper resistor and a 2 kΩ lower resistor gives node voltages 3 V and 2 V. The source current, defined from positive to negative terminal, is −1 mA. The upper resistor dissipates 1 mW and the lower one 2 mW; the source absorbs −3 mW. Their sum is zero. The middle-node current residual is also zero: (3−2)/1000−2/2000 A.

A second example connects each of two nodes to ground through 1 kΩ and places a floating 2 V source between them. Their voltages are +1 V and −1 V. Grounding both source terminals would destroy the intended circuit.

### Implementation, checks and limits

Run `python demo.py --case mna` from the linked example directory. The three named unit tests above compare the stamped solution against a hand-derived divider, node KCL, total power balance, a floating-source symmetry case and a current-source case. A floating resistor network is rejected because its absolute voltage has no unique solution.

The implementation uses partial-pivot elimination with an absolute pivot threshold; this is not a general conditioning guarantee for arbitrarily scaled circuits. Capacitors and inductors require integration and initial conditions, while diodes and MOS devices require operating-point iteration and device models. These are linear reference-model results, not measured circuit data or a recorded SPICE run.

## 출처 / Sources

- TU Delft, *Modified Nodal Analysis*: KCL augmentation, incidence signs and block matrix.
- ngspice, *User's Manual*: independent-source conventions and matrix-based circuit analysis. Links appear at the relevant explanations above.

# 전원은 배선까지 포함한다: PDN, decoupling과 귀환 전류

[PCB와 하드웨어](../README.md) · [참조 모델](../../../예제_examples/확장기초_extended/hardware/models.py) · [검산](../../../예제_examples/확장기초_extended/hardware/test_models.py)

## 한국어

### 전원 핀에서 보는 전압

전원장치가 1 V를 표시해도 IC의 두 전원 핀 사이가 언제나 1 V인 것은 아니다. 부하 전류가 빠르게 바뀌면 전원·귀환 경로의 저항과 인덕턴스에 전압이 생긴다. PDN(power delivery network)은 regulator, bulk capacitor, PCB plane·via·배선, package와 on-die 전원 경로를 함께 다룬다. Decoupling capacitor는 전류가 필요한 위치 가까이에서 전하를 공급하지만 연결 경로가 길면 그 효과가 줄어든다. [ADI MT-101](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)

부하가 보는 작은 변화는 주파수 영역에서 $`\Delta V(f)=-Z_{PDN}(f)\Delta I(f)`$로 나타낼 수 있다. 부하 전류 증가를 양수로 두었을 때의 부호다. 허용 변동 $`\Delta V_{allow}`$와 대표 전류 변화 $`\Delta I`$의 비

$$Z_{target}=\Delta V_{allow}/\Delta I$$

는 설계의 출발점이다. 50 mV와 1 A라면 50 mΩ이다. 다만 실제 전압은 전류의 스펙트럼과 PDN의 위상·공진에 좌우되므로 모든 상황을 보증하는 단일 규격으로 읽지는 않는다.

### 저항, 전하 부족과 배선 인덕턴스

이상화하면 서로 다른 현상이 다음 식으로 드러난다.

| 현상 | 식 | 의미 |
|---|---|---|
| 저항 손실 | $`\Delta V=R\Delta I`$ | 전류가 커질수록 DC drop 증가 |
| capacitor 방전 | $`C\Delta V=\int\Delta i\,dt`$ | 공급이 뒤늦는 동안 전하를 내어 줌 |
| 인덕턴스 | $`v_L=L\,di/dt`$ | 전류 변화가 빠를수록 큰 전압 발생 |

다른 공급이 없는 동안 1 A를 100 ns 공급하고 전압 하락을 50 mV 이내로 제한하려면 이상적으로 $`C\ge2`$ µF다. 실제 부품은 DC bias·온도·공차로 유효 C가 달라진다. ESR 20 mΩ의 1 A 변화는 20 mV의 저항성 변화를, 1 nH에서 1 A/ns는 1 V의 유도 전압 규모를 만든다. 이 세 수치의 최대값이 같은 순간에 발생한다고 단순히 더하지는 않는다.

실제 capacitor를 C·ESR·ESL의 직렬 모델로 줄이면

$$Z_C(j\omega)=ESR+j\left(\omega ESL-\frac1{\omega C}\right),\qquad
f_{SR}=\frac1{2\pi\sqrt{ESL\,C}}.$$

자기공진 아래에서는 주로 capacitive, 위에서는 inductive하다. 100 nF, 1 nH의 공진은 약 15.9 MHz다. ESR을 생략하면 공진점의 임피던스를 비현실적으로 0으로 만들 수 있다. 여러 용량을 병렬로 넣어도 배선 인덕턴스와 함께 antiresonance가 생길 수 있어 “종류가 많을수록 좋다”는 결론은 나오지 않는다. [ADI의 기생 성분·공진 설명](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)

### 신호의 돌아오는 길도 회로다

전류는 신호선으로 갔다가 반드시 돌아온다. 저주파와 고주파에서는 전류 분포가 다르며, 빠른 single-ended 신호에서는 인접한 연속 reference plane이 작은 loop inductance를 제공한다. Plane의 틈을 가로질러 route하면 귀환이 우회해 loop와 결합이 커질 수 있다. DC 저항만 보고 가장 넓은 구리로 흐른다고 설명해서는 안 된다. 실제 분포는 전자기장과 전체 임피던스로 정해진다. [TI SCAA082A, §1.6](https://www.ti.com/lit/an/scaa082a/scaa082a.pdf)

층을 바꿀 때는 reference가 어떻게 이어지는지도 본다. 같은 ground reference라면 가까운 ground stitching via가 도움이 될 수 있다. 서로 다른 전원 plane 사이의 귀환에는 적절한 AC 연결과 전원 구조 검토가 필요하며 ground via 하나가 모든 전환을 해결하지 않는다. Capacitor의 전원 쪽 연결만 짧고 ground via가 멀어도 loop inductance가 남는다. 목표는 핀과 capacitor 사이의 전체 왕복 경로를 짧고 낮은 인덕턴스로 만드는 것이다.

### 모델, 구현과 검증

`pdn_impedance`는 $`R_s+j\omega L_s`$ 전원 경로와 여러 직렬 RLC capacitor 가지의 admittance를 합한다. 이상적 전원은 AC ground이고 부하 위치는 단일 노드다. 이 모델은 board·package의 분포 공진이나 regulator 제어루프를 포함하지 않는다. 테스트는 단일 가지의 공진에서 $`\vert Z\vert =ESR`$인지 확인하고, 병렬망에 1 A를 주었을 때 각 가지 전류의 합이 1 A인지 독립 KCL로 검사한다.

보드 평가에서는 regulator·부품의 허용 범위를 먼저 맞추고, DC bias가 반영된 C와 package/via 추정치를 넣어 impedance sweep을 한다. 다음으로 실제 부하 step의 전압을 짧은 ground 연결로 측정하고 probe 대역폭·부하를 기록한다. VNA 측정은 fixture·reference plane 보정과 낮은 임피던스 측정법이 필요하다. 회로 모델의 공진 계산과 실제 EMI 적합성 시험은 별개의 증거다.

## English

### Voltage at the device pins

A supply displaying 1 V does not guarantee a constant 1 V between an IC's power pins. Rapid current changes develop voltage across resistance and inductance in both supply and return paths. A PDN includes regulators, bulk capacitors, board planes, vias and traces, package connections and on-die distribution. Local decoupling supplies charge near the load, but long connections reduce its effectiveness. [ADI MT-101](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)

For a positive increase in load current, a small-signal model gives $`\Delta V(f)=-Z_{PDN}(f)\Delta I(f)`$. The ratio $`Z_{target}=\Delta V_{allow}/\Delta I`$ is a useful initial budget: 50 mV for 1 A gives 50 mΩ. Actual droop also depends on the current spectrum, impedance phase and resonances; this ratio alone is not a universal guarantee.

### Resistance, missing charge and inductance

The basic mechanisms are $`\Delta V=R\Delta I`$, $`C\Delta V=\int\Delta i\,dt`$, and $`v_L=L\,di/dt`$. Supplying 1 A for 100 ns with no other source contribution and at most 50 mV of ideal capacitor droop requires at least 2 µF. Effective capacitance changes with DC bias, temperature and tolerance. A 20 mΩ ESR produces a 20 mV resistive change for 1 A; 1 nH at 1 A/ns corresponds to 1 V of inductive voltage. Their separate peak estimates need not occur simultaneously.

A series C–ESR–ESL approximation gives

$$Z_C=ESR+j(\omega ESL-1/(\omega C)),\qquad f_{SR}=1/(2\pi\sqrt{ESL\,C}).$$

The branch is mainly capacitive below self-resonance and inductive above it. For 100 nF and 1 nH, resonance is about 15.9 MHz. Omitting ESR can create an unrealistic zero impedance. Multiple capacitor values may form antiresonances with interconnect inductance; more varieties are not automatically better. [ADI parasitic and resonance models](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf)

### Return current is part of the circuit

Signal current must return to its source. Its distribution changes with frequency. A nearby continuous reference plane provides a low-inductance return for a fast single-ended signal; crossing a plane split can force a detour and increase loop coupling. DC resistance alone cannot describe the distribution, which follows the electromagnetic field and complete impedance. [TI SCAA082A, §1.6](https://www.ti.com/lit/an/scaa082a/scaa082a.pdf)

A layer transition also changes the reference geometry. A nearby stitching via can connect ground references, whereas transitions between different power planes require appropriate AC connectivity and power-structure analysis. One ground via does not resolve every case. A capacitor with a short supply connection but distant return via still has a large loop. Both halves of the pin-to-capacitor path matter.

### Model, implementation and verification

`pdn_impedance` sums admittances of a source path $`R_s+j\omega L_s`$ and series-RLC capacitor branches. The ideal supply is AC ground and the load is one lumped node. Distributed board/package resonances and regulator feedback are excluded. Tests check that a branch reaches $`\vert Z\vert =ESR`$ at resonance and independently sum all branch currents for a 1 A excitation.

Board evaluation begins with regulator/component limits, bias-adjusted capacitance and package/via estimates, followed by impedance sweeps. Measure an actual load step with a short probe return, recording bandwidth and loading. VNA work requires fixture/reference-plane calibration and a method suitable for low impedance. A circuit-model resonance check and an EMI compliance test provide different evidence.

## 출처 대조 / Source cross-check

ADI의 실제 capacitor·decoupling 모델과 TI의 귀환 전류·loop 설명을 대조했다. 수치 예는 위 식으로 계산했다. / ADI's component model was cross-checked against TI's return-path explanation; numerical examples were derived from the stated equations. 확인 / checked: 2026-10-19.

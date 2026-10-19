# 하드웨어 기초 참조 모델 / Hardware reference models

## 한국어

[models.py](models.py)는 회로 식과 디지털 계약을 작은 Python 모델로 표현한다. [test_models.py](test_models.py)는 해석적 한계, 독립 계산, 완전 열거와 통계적 simulation으로 가정을 확인한다. 외부 패키지가 필요하지 않으며 저장소 root에서 다음처럼 실행한다.

```text
python -m unittest discover -s 예제_examples/확장기초_extended/hardware -p "test_*.py" -v
```

| 분야 | 구현 | 독립 확인과 경계 |
|---|---|---|
| 소신호 AC | `cs_gain` | KCL 잔차, DC gain, 한 pole의 −3 dB, 비선형 잔차의 진폭 제곱 비례 |
| PDN | `capacitor_impedance`, `pdn_impedance` | 자기공진의 ESR, 주입 전류와 가지 전류 합 |
| 상태 검증 | `counter_next`, `reachable_counter` | D=1…16의 모든 상태·요청, BFS 도달 집합·경계 반례 |
| STA | `timing_slack` | 절대 edge 시각의 차, skew 부호·주기 변화 |
| Byte memory | `ByteMemory` | 별도 표준 encoding, endian·부호·정렬·범위 |
| BPSK | `bpsk_ber`, `bpsk_errors` | Gaussian tail 수치 적분, 3조건 총 600,000 bit simulation |
| Buck CCM | `buck_ccm` | volt-second balance, 삼각 전류의 별도 전하 적분 |
| Ready/valid | `ReadyValidBuffer` | token scoreboard, stall 안정성, drain·reset |
| EDA 개념 | `full_adder_gates`, `dag_arrivals` | 8입력 truth table, 별도 경로 열거의 최대 지연 |
| Thermal | `thermal_step`, `thermal_pulse_steady` | 별도 ODE 적분 수렴, 정상 한계·주기 고정점 |
| Scan·ATPG | `logic_output`, `detected_faults`, `scan_shift` | activation/propagation 직접 조건, pattern 부분집합 열거·직렬 bit 순서 |
| PIM | `crossbar_currents`, `differential_conductances`, `quantize_symmetric` | 직접 내적, row KCL, 양자화 오차·clipping |

입력은 각 글에 정의된 단위와 범위를 따른다. `timing_slack`은 한 clock의 인접 setup/same-edge hold만, PDN은 단일 부하 노드만, buck은 이상적 양의 CCM만, thermal은 일정 ambient의 한 pole만 다룬다. Byte memory는 자연 정렬된 유한 RAM이며 CPU나 MMIO가 아니다. 버퍼는 2-entry·empty bypass 없음·갱신 전 수락 판단을 사용한다. PIM의 row 저항은 분포 배선망이 아닌 공통 직렬저항이다.

[VALIDATION.json](VALIDATION.json)은 실제 실행한 Python 검산의 범위를 남긴다. 실제 RTL simulator·formal solver·합성·배치배선·STA·DRC/LVS·Spectre·회로 제작·ATE·실물 온도·무선 측정의 실행 결과와는 구분한다.

## English

[models.py](models.py) expresses circuit equations and digital contracts as small Python models. [test_models.py](test_models.py) checks assumptions through analytic limits, independent calculations, exhaustive enumeration and statistical simulation. No external package is required; run the command above from the repository root.

The twelve areas cover small-signal KCL/poles, PDN resonance and current balance, complete counter transitions/reachability, absolute-event timing and skew, byte encoding/sign/alignment, Gaussian-tail integration and 600,000 simulated BPSK bits, buck volt-second/charge balance, ready/valid token scoreboarding, full-adder truth tables and explicit DAG paths, thermal ODE convergence/fixed points, fault activation/propagation and scan order, and PIM dot products/row KCL/quantization.

Use each article's units and assumptions. Timing covers adjacent setup and same-edge hold for one clock. PDN has one lumped load node; buck assumes ideal positive CCM; thermal uses constant ambient and one pole. Byte memory is aligned finite RAM, not a CPU or MMIO model. The buffer has two entries, no empty bypass and pre-edge acceptance. PIM row resistance is one common series element, not distributed wiring.

[VALIDATION.json](VALIDATION.json) records the executed Python checks. Their results are distinct from RTL simulation, formal solving, synthesis, placement/routing, STA, DRC/LVS, Spectre, fabrication, ATE or physical thermal/radio measurements.

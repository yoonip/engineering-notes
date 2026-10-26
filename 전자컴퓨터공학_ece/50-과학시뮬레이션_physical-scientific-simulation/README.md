# 물리·과학 시뮬레이션 | Physics, Multiphysics & Scientific Simulation

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

과학 시뮬레이션은 물리 모델을 유한한 데이터와 계산으로 근사하는 작업입니다. 그림이 정밀해 보여도 그것만으로 모델이 정확하다고 판단할 수는 없습니다. 방정식, 재료, 경계조건, 초기조건, 수치 해법이 함께 결과를 정합니다.

## 이산화와 해법

유한차분은 격자점 사이의 차이로 미분을 근사하고, 유한요소는 영역을 요소로 나누고 약형을 이용해 해를 구하며, 유한체적은 제어체적의 보존 관계를 다룹니다. 시간 적분에서는 안정성과 정확도가 다른 조건이며, 더 작은 step이 항상 모든 모델 오류를 해결하지는 않습니다.

## 해석 대상과 검증

전자기·열·구조·유체·소자 문제는 서로 다른 방정식과 재료 모델을 사용합니다. Mesh refinement는 격자를 세분화했을 때 결과가 어떻게 변하는지 봅니다. Verification은 계산이 의도한 수학 문제를 올바르게 풀었는지, validation은 모델이 실제 현상을 충분히 표현하는지와 관련됩니다.

COMSOL·Ansys·HFSS·CST는 다물리·전자기 해석, OpenFOAM은 유체, FEniCS는 유한요소, MEEP·openEMS는 전자기, LAMMPS는 분자동역학 계산에 쓰입니다. 해석해·보존량·독립된 계산·측정값은 각각 다른 방식으로 결과를 확인하는 기준이 됩니다.

## 혼합 탱크에서 보존식부터 세우는 예

직접 만든 예로 부피가 일정한 물탱크의 농도 변화를 계산해 보겠습니다. 액체가 같은 유량으로 들어오고 나가며 탱크 내부가 완전히 섞인다고 가정합니다. 탱크 부피를 `V`, 유량을 `Q`, 유입 농도를 `C_in`, 탱크 안과 출구의 농도를 `C`라고 쓰겠습니다. 반응과 누출은 없다고 가정합니다. 같은 탱크라도 잘 섞이지 않으면 이 모형을 그대로 쓸 수 없습니다.

```math
\frac{d(VC)}{dt}=Q C_{in}-Q C
\frac{dC}{dt}=\frac{Q}{V}(C_{in}-C),\qquad
C(t)=C_{in}+(C(0)-C_{in})e^{-Qt/V}
```

왼쪽은 탱크 안 물질량의 변화이고 오른쪽은 들어오는 양에서 나가는 양을 뺀 값입니다. 부피가 일정할 때에만 두 번째 식처럼 `V`를 밖으로 빼낼 수 있습니다. 농도와 총량을 혼동하면 단위는 맞아 보이는 코드에서도 물질이 생기거나 사라지는 오류가 날 수 있습니다.

가상의 `V=20 L`, `Q=10 L/h`, `C_in=1 g/L`, `C(0)=0`을 넣으면 2시간 후 농도는 약 `0.6321 g/L`입니다. 시간상수 `τ=V/Q=2 h`는 초기값과 최종값의 차이가 약 36.8%로 줄어드는 시간입니다. 두 시간이 지나면 완전히 유입 농도와 같아진다는 뜻이 아닙니다. 이 계산은 실제 반응기 측정이 아닌 보존식의 해석 예입니다.

## 시간 간격을 바꿔 수치 계산을 확인합니다

앞 식을 전진 오일러 방법으로 계산하면 현재 변화율을 시간 간격 `Δt`만큼 적용하여 다음 값을 얻습니다.

```math
C_{k+1}=C_k+\frac{Q\Delta t}{V}(C_{in}-C_k)
```

`Δt=1 h`이면 첫 두 단계는 0→0.5→0.75입니다. 2시간의 해석해 0.6321보다 큽니다. `Δt=0.5 h`로 네 번 계산하면 0.6836, `Δt=0.25 h`로 여덟 번 계산하면 약 0.6564가 됩니다. 간격을 줄이며 같은 시점의 결과가 해석해에 가까워지는지 볼 수 있습니다. 실행 코드를 바꾸지 않아도 작은 표와 산술로 확인할 수 있는 검증입니다.

| 시간 간격 | 2시간까지 단계 수 | 계산 농도 | 해석해와 절대 차이 |
| --- | --- | --- | --- |
| 1 h | 2 | 0.7500 g/L | 약 0.1179 g/L |
| 0.5 h | 4 | 0.6836 g/L | 약 0.0515 g/L |
| 0.25 h | 8 | 0.6564 g/L | 약 0.0243 g/L |

오차가 줄어드는 것은 이 수학 모형을 더 잘 계산한다는 근거입니다. 실제 탱크에 사각지대가 있거나 센서가 느리게 반응한다면 이 모형과 실측은 여전히 어긋날 수 있습니다. 수치해의 수렴과 현실을 설명하는 타당성을 분리해야 하는 이유입니다.

## 안정성과 물리적으로 자연스러운 변화도 다릅니다

목표값과의 차이를 `e_k=C_k−C_in`이라고 두면 다음 단계의 차이는 `(1−QΔt/V)e_k`입니다. 절댓값이 1보다 작아야 오차가 줄어드는 단순 안정 조건을 얻습니다. 그러나 계수가 음수이면 목표값을 넘나들며 진동합니다. 안정하다는 말이 농도가 항상 단조롭게 증가하거나 모든 값이 물리적으로 자연스럽다는 뜻은 아닙니다.

이 예에서 `Δt=3 h`이면 계수가 −0.5이므로 계산은 수렴하더라도 0→1.5→0.75처럼 목표 농도를 넘습니다. 반응·농축이 없고 유입 농도가 1인 이 완전혼합 모형의 연속 해와 맞지 않는 변화입니다. 시간 간격을 선택할 때에는 단순 발산 여부뿐 아니라 양수성·단조성 등 문제에 필요한 성질도 확인합니다.

## 잔차·보존·측정 오차를 나눠 봅니다

잔차는 계산값이 선택한 방정식을 얼마나 잘 만족하는지 나타냅니다. 잔차가 작아도 잘못된 경계조건을 입력했다면 다른 문제의 정답을 정확히 구했을 수 있습니다. 보존 확인은 들어온 총량과 나간 총량, 내부 증가량을 연결합니다. 이는 계산 내부의 중요한 확인이지만 완전혼합 가정이 맞는지까지 입증하지는 않습니다.

실측과 비교할 때에는 관측 위치와 센서 응답 시간도 모델에 포함해야 합니다. 탱크 안 평균 농도 모형을 벽 근처 센서의 순간값과 무조건 대조하면 혼합 오류와 센서 지연을 혼동할 수 있습니다. 입력 유량의 단위가 L/min인지 L/h인지 확인하는 것 역시 복잡한 해석기 설정 못지않게 중요합니다. [연속 바이오제조 리뷰](../../제품기술분석_product-technology/진단과바이오제조_diagnostics-biomanufacturing/연속바이오제조의공정과비용_continuous-biomanufacturing2026.md)는 평균 체류 시간과 실제 분포의 차이를 설명합니다.

## 확인 문제

1. 시간 간격을 줄여 답이 수렴하면 완전혼합 가정도 검증된 것일까요?
2. 시간상수가 2시간이면 두 시간 후 농도가 최종값과 정확히 같을까요?
3. 수치해가 발산하지 않으면 모든 중간값도 물리적으로 타당할까요?

<details>
<summary>해설 보기</summary>

1. 아닙니다. 선택한 모형의 계산 오차를 확인한 것입니다. 실제 혼합과 비교하는 자료가 별도로 필요합니다.
2. 아닙니다. 이 예에서는 최종 변화량의 약 63.2%에 도달합니다.
3. 아닙니다. 안정한 계산도 과도한 시간 간격에서 진동하거나 농도 범위를 벗어날 수 있습니다.

</details>

## 관련 기술

COMSOL, Ansys, HFSS, CST, OpenFOAM, FEniCS, MEEP, openEMS, LAMMPS

## 참고 자료

- [FEniCS documentation](https://fenicsproject.org/documentation/)

## 기초 해설

- [수치해석의 V&V: 수렴, 잔차, 보존을 따로 확인하기](해설_notes/수치해석의VV_verification-convergence-and-conservation.md)

## English

### Physical and scientific simulation

Scientific simulation approximates physical models through finite data and computation. A detailed plot alone does not establish model accuracy. Equations, materials, boundary and initial conditions, and numerical methods all shape the result.

### Discretization and solvers

Finite differences approximate derivatives between grid points. Finite elements divide a domain into elements and construct solutions from a weak formulation. Finite volumes enforce conservation over control volumes. In time integration, stability and accuracy are separate concerns; reducing the step size does not remove every modeling error.

### Analysis targets and validation

Electromagnetic, thermal, structural, fluid, and device simulations use different equations and material models. Mesh-refinement studies examine how results change as the mesh becomes finer. Verification asks whether the intended mathematical problem is solved correctly; validation asks whether the model adequately describes the real phenomenon.

COMSOL, Ansys, HFSS, and CST support multiphysics or electromagnetic analysis. OpenFOAM supports fluid simulation, FEniCS supports finite elements, MEEP and openEMS support electromagnetics, and LAMMPS supports molecular dynamics. Analytical solutions, conserved quantities, independent calculations, and measurements provide different ways to check results.

### Foundation article

- [수치해석의 V&V: 수렴, 잔차, 보존을 따로 확인하기](해설_notes/수치해석의VV_verification-convergence-and-conservation.md#english)


## 심화 해설 | Advanced article

- [미분방정식에서 요소 행렬까지: 1차원 열전도 FEM](해설_notes/열전도유한요소_weak-form-linear-fem.md) · [English](해설_notes/열전도유한요소_weak-form-linear-fem.md#english)

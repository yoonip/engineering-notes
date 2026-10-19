# 물리·과학 시뮬레이션 | Physics, Multiphysics & Scientific Simulation

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

과학 시뮬레이션은 물리 모델을 유한한 데이터와 계산으로 근사하는 작업이다. 그림이 정밀해 보여도 그것만으로 모델이 정확하다고 판단할 수는 없다. 방정식, 재료, 경계조건, 초기조건, 수치 해법이 함께 결과를 정한다.

## 이산화와 해법

유한차분은 격자점 사이의 차이로 미분을 근사하고, 유한요소는 영역을 요소로 나누고 약형을 이용해 해를 구하며, 유한체적은 제어체적의 보존 관계를 다룬다. 시간 적분에서는 안정성과 정확도가 다른 조건이며, 더 작은 step이 항상 모든 모델 오류를 해결하지는 않는다.

## 해석 대상과 검증

전자기·열·구조·유체·소자 문제는 서로 다른 방정식과 재료 모델을 사용한다. Mesh refinement는 격자를 세분화했을 때 결과가 어떻게 변하는지 본다. Verification은 계산이 의도한 수학 문제를 올바르게 풀었는지, validation은 모델이 실제 현상을 충분히 표현하는지와 관련된다.

COMSOL·Ansys·HFSS·CST는 다물리·전자기 해석, OpenFOAM은 유체, FEniCS는 유한요소, MEEP·openEMS는 전자기, LAMMPS는 분자동역학 계산에 쓰인다. 해석해·보존량·독립된 계산·측정값은 각각 다른 방식으로 결과를 확인하는 기준이 된다.

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

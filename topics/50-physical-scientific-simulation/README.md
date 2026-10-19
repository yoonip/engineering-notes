# 물리·과학 시뮬레이션

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

과학 시뮬레이션은 물리 모델을 유한한 데이터와 계산으로 근사하는 작업이다. 결과의 정밀한 그림만으로 모델의 정확성을 판단하기는 어렵다. 방정식, 재료, 경계조건, 초기조건, 수치 해법이 함께 결과를 정한다.

## 이산화와 해법

유한차분은 격자점 사이의 차이로 미분을 근사하고, 유한요소는 영역을 요소로 나누어 약형 기반의 해를 구성하며, 유한체적은 제어체적의 보존 관계를 다룬다. 시간 적분에서는 안정성과 정확도가 다른 조건이며, 더 작은 step이 항상 모든 모델 오류를 해결하지는 않는다.

## 해석 대상과 검증

전자기·열·구조·유체·소자 문제는 서로 다른 방정식과 재료 모델을 사용한다. Mesh refinement는 격자를 세분화했을 때 결과가 어떻게 변하는지 본다. Verification은 계산이 의도한 수학 문제를 올바르게 풀었는지, validation은 모델이 실제 현상을 충분히 표현하는지와 관련된다.

COMSOL·Ansys·HFSS·CST는 다물리·전자기 해석, OpenFOAM은 유체, FEniCS는 유한요소, MEEP·openEMS는 전자기, LAMMPS는 분자동역학 생태계다. 해석해·보존량·독립된 계산·측정값은 결과를 점검하는 서로 다른 근거가 된다.

## 관련 기술

COMSOL, Ansys, HFSS, CST, OpenFOAM, FEniCS, MEEP, openEMS, LAMMPS

## 참고 자료

- [FEniCS documentation](https://fenicsproject.org/documentation/)

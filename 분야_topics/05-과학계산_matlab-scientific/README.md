# MATLAB과 과학 계산 | MATLAB & Scientific Computing

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

MATLAB은 행렬 중심의 수치 계산과 시각화 환경이다. 신호처리, 제어, 통신, 모델 기반 설계에서 많이 쓰이며 Simulink는 블록선도로 동적 시스템을 구성한다. GNU Octave도 수치 계산에 쓰이며 MATLAB 문법과 상당 부분 호환된다.

## 행렬 연산과 원소별 연산

MATLAB의 `A * B`는 행렬 곱이고 `A .* B`는 같은 위치 원소끼리의 곱이다. Python·NumPy에서는 `A @ B`가 행렬 곱, `A * B`가 원소별 곱이다. MATLAB의 인덱스는 1부터, Python의 인덱스는 0부터 시작한다.

```matlab
R = 1e3;
C = 1e-6;
t = linspace(0, 5*R*C, 501);
v = 3.3 * (1 - exp(-t/(R*C)));
plot(t*1e3, v);
xlabel('Time [ms]'); ylabel('Voltage [V]'); grid on;
```

## 수치 해석과 모델링

적분기는 연속 시간의 미분방정식을 유한한 계산 단계로 근사한다. 고정 스텝과 가변 스텝은 계산량과 오차 조절 방식이 다르다. Simulink에서는 연속·이산 블록의 시간 기준과 솔버 설정이 결과에 영향을 준다.

SciPy는 Python의 과학 계산, SymPy·Mathematica·Maple은 기호 계산, Julia는 수치 계산 코드 작성에 쓰인다. 기호적으로 얻은 식, 부동소수점으로 계산한 값, 시뮬레이터의 근삿값은 각각의 가정과 오차가 있다.

## 관련 기술

MATLAB, Simulink, GNU Octave, SciPy, SymPy, Mathematica, Maple, Julia

## 참고 자료

- [MATLAB matrices and arrays](https://www.mathworks.com/help/matlab/learn_matlab/matrices-and-arrays.html)
- [SciPy documentation](https://docs.scipy.org/doc/scipy/)

## 기초 해설

- [MATLAB 수치해석: 답의 오차와 잔차는 왜 다를까](해설_notes/MATLAB수치해석_linear-solves-conditioning-residuals.md)

## English

MATLAB is an environment for matrix-oriented numerical computing and visualization, widely used in signal processing, control, communication, and model-based design. Simulink represents dynamic systems as block diagrams. GNU Octave supports much of MATLAB's syntax for numerical work.

### Matrix and elementwise operations

In MATLAB, `A * B` is matrix multiplication and `A .* B` multiplies corresponding elements. In Python with NumPy, the corresponding operators are `A @ B` and `A * B`. MATLAB indexing starts at 1, while Python indexing starts at 0. The example above plots an RC charging response over five time constants.

### Numerical analysis and modeling

An integrator approximates a continuous-time differential equation through a finite sequence of computational steps. Fixed-step and variable-step solvers control workload and error differently. In Simulink, the time bases of continuous and discrete blocks and the solver settings affect the result.

SciPy provides scientific computing in Python. SymPy, Mathematica, and Maple support symbolic computation, and Julia is another language for numerical work. A symbolic expression, a floating-point calculation, and a simulator's approximation each come with their own assumptions and sources of error.

### Foundation article

- [MATLAB 수치해석: 답의 오차와 잔차는 왜 다를까](해설_notes/MATLAB수치해석_linear-solves-conditioning-residuals.md#english)


## 심화 해설 | Advanced article

- [비선형 방정식: 빠른 Newton과 안전한 구간 좁히기](해설_notes/구간을지키는근찾기_safeguarded-root-finding.md) · [English](해설_notes/구간을지키는근찾기_safeguarded-root-finding.md#english)

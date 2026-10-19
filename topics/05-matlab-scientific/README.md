# MATLAB & Scientific Computing

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

MATLAB은 행렬 중심의 수치 계산과 시각화 환경이다. 신호처리, 제어, 통신, 모델 기반 설계에서 많이 쓰이며 Simulink는 블록선도로 동적 시스템을 구성한다. GNU Octave는 MATLAB 문법과 상당 부분 호환되는 수치 계산 도구다.

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

SciPy는 Python의 과학 계산, SymPy·Mathematica·Maple은 기호 계산, Julia는 수치 계산 코드 작성에 쓰인다. 기호적으로 얻은 식, 부동소수점으로 계산한 값, 시뮬레이터의 근삿값은 서로 다른 오차와 가정을 갖는다.

## 관련 기술

MATLAB, Simulink, GNU Octave, SciPy, SymPy, Mathematica, Maple, Julia

## 참고 자료

- [MATLAB matrices and arrays](https://www.mathworks.com/help/matlab/learn_matlab/matrices-and-arrays.html)
- [SciPy documentation](https://docs.scipy.org/doc/scipy/)

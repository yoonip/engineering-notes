# 기술 노트: RC 충전 응답

## 모델

이상적인 전압원·저항·커패시터의 직렬 회로를 다룹니다. 커패시터의 초기 전압은 0이고, 입력 Vin은 일정합니다. 이때 전압 변화는 `dv/dt=(Vin-v)/(RC)`로 나타냅니다.

## 해

해는 `v(t)=Vin*(1-exp(-t/(RC)))`입니다. 시정수는 `tau=RC`이고, t=tau일 때 최종 전압의 약 63.2%에 도달합니다. 이상적인 1차 회로 모델에서 얻는 결과입니다.

## 수식과 코드

[Euler 근사 코드](../예제_examples/rc_euler.py)는 미분방정식을 반복문으로 계산합니다. [Jupyter 문서](../예제_examples/rc_response.ipynb)에서는 수식·수치·그래프를 함께 살펴봅니다. 모델의 가정과 수식, 구현, 비교 기준을 연결해 응답을 확인합니다.

## English

### Model

Consider a series circuit with an ideal voltage source, resistor, and capacitor. The capacitor starts at 0 V, and the input Vin is constant. Its voltage follows `dv/dt=(Vin-v)/(RC)`.

### Solution

The solution is `v(t)=Vin*(1-exp(-t/(RC)))`. The time constant is `tau=RC`. At t=tau, the voltage reaches approximately 63.2% of its final value. This result follows from the ideal first-order circuit model.

### Equations and code

The [Euler approximation](../예제_examples/rc_euler.py) computes the differential equation with a loop. The [Jupyter notebook](../예제_examples/rc_response.ipynb) brings together the equations, numerical results, and plots. The response can be checked by connecting the model assumptions, equations, implementation, and comparison criteria.

# 기술 노트: RC 충전 응답

## 모델

이상적인 전압원·양의 일정한 저항·커패시터의 직렬 회로를 다룹니다. 커패시터의 초기 전압은 0이고, 입력 Vin은 일정하며 별도 부하와 누설은 생략합니다. 이때 전압 변화는 `dv/dt=(Vin-v)/(RC)`로 나타냅니다. [MIT 6.002 Lecture 12, pp.5–11](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/84f4b553fc6a1ddd7007465041c4e213_6002_l12.pdf)의 커패시터 법칙·노드 방정식·초기값 해가 기준입니다.

## 해

해는 `v(t)=Vin*(1-exp(-t/(RC)))`입니다. 시정수는 `tau=RC`이고, t=tau일 때 최종 전압의 약 63.2%에 도달합니다. 이상적인 1차 회로 모델에서 얻는 결과입니다.

## 수식과 코드

[Euler 근사 코드](../예제_examples/rc_euler.py)는 미분방정식을 반복문으로 계산합니다. [Jupyter 문서](../예제_examples/rc_response.ipynb)에서는 수식·수치·그래프를 함께 살펴봅니다. 모델의 가정과 수식, 구현, 비교 기준을 연결해 응답을 확인합니다.

연결된 `rc_euler.py`의 입력은 R=1 kΩ·C=1 μF·Vin=3.3 V, 간격 10 μs·500단계입니다. 아래 손계산의 C=100 μF·Vin=5 V·간격 0.05 s와는 다른 입력입니다. 둘 다 같은 RC 식을 사용하지만 수치 결과를 직접 같은 실행 결과로 비교하지 않습니다.

## 왜 처음에는 빨리, 나중에는 천천히 변합니까?

커패시터는 전하를 저장하며, 전압을 올리려면 전하를 더 보내야 합니다. 커패시턴스 C는 같은 전압 변화에 얼마나 많은 전하가 필요한지 나타내는 양입니다. 저항 R은 전류와 전압 차이를 연결합니다. 이 회로에서 저항에 걸리는 전압은 `Vin−v`이고 전류는 `(Vin−v)/R`입니다.

커패시터 전류 `i=C·dv/dt`와 연결하면 `C·dv/dt=(Vin−v)/R`가 됩니다. 처음에는 v=0이므로 차이가 크고, 충전될수록 v가 Vin에 가까워져 전류가 줄어듭니다. 커패시터 전압이 전압원과 즉시 같아지는 회로로 생각하면 이 변화를 설명할 수 없습니다.

## 단위를 넣어 계산하기

직접 정한 값은 `R=1kΩ=1000Ω`, `C=100μF=0.0001F`, `Vin=5V`입니다. 시정수는 `RC=0.1초`입니다. 시정수는 최종 전압과 같아지는 시간이 아니라, 오차가 처음의 약 36.8%로 줄어드는 시간입니다.

| 시각 | 시정수로 쓴 시간 | 이론식의 커패시터 전압 |
| --- | --- | ---: |
| 0초 | 0τ | 0V |
| 0.1초 | 1τ | 약 3.16060V |
| 0.3초 | 3τ | 약 4.75106V |
| 0.5초 | 5τ | 약 4.96631V |

5τ에서도 수학적으로 정확히 5V가 되지는 않습니다. 실제 설계에서는 허용 오차 안에 들어왔는지를 정해야 합니다. 예를 들어 최종값의 99% 이상이라는 조건이면 `1−exp(−t/τ)≥0.99`에서 `t≥τ ln100≈4.605τ`입니다. 이 값은 이상적인 모델의 계산이며 실제 부품 측정 결과는 아닙니다.

## 반복 계산의 한 걸음을 읽기

Euler 근사는 현재 기울기가 짧은 시간 동안 유지된다고 보고 다음 값을 계산합니다.

$$v_{n+1}=v_n+\Delta t\frac{V_{in}-v_n}{RC}$$

위 회로에서 `Δt=0.05초`, `v₀=0`으로 정하면 첫 계산은 `0+0.05×5/0.1=2.5V`입니다. 같은 시각의 이론식은 약 1.96735V이므로 첫걸음의 차이는 약 0.53265V입니다. 계산이 쉬운 대신 곡선의 변화를 직선 한 걸음으로 대신한 오차가 생깁니다.

이 선형 문제에서 Euler 값이 최종값에 가까워지는 안정 조건은 `|1−Δt/τ|<1`, 즉 `0<Δt<2τ`입니다. 이 조건과 각 시각의 근사 정확도가 충분하다는 조건은 다릅니다. 예를 들어 τ보다 큰 걸음은 최종값 주변을 번갈아 넘을 수 있습니다. 시간 간격을 줄이고 이론식과의 차이도 함께 확인해야 합니다.

## 직접 확인하기

1. R을 두 배로 하고 C와 Vin을 유지하면 최종 전압과 시정수는 각각 어떻게 됩니까?
2. 초기 전압이 0인 이 회로가 1τ에서 최종값의 100%에 도달합니까?
3. Euler 한 걸음이 이론값과 다르면 미분방정식 자체가 틀렸다는 뜻입니까?

<details>
<summary>답과 이유</summary>

1. 이상적인 최종 전압은 Vin으로 같고, 시정수 RC는 두 배가 됩니다.
2. 약 63.2%에 도달합니다. 최종값과의 차이가 약 36.8% 남습니다.
3. 아닙니다. 수치 근사 오차와 모델의 타당성을 구분해야 합니다. 먼저 시간 간격과 계산식을 확인합니다.

</details>

출처는 MIT 6.002의 *Capacitors and First-Order Systems*, Lecture 12입니다. PDF 본문은 Fall 2000 강의이며 Spring 2007 OCW 과정에 보관된 판본입니다. 실제 회로에서는 전원·측정기의 영향, 부품 허용 오차와 누설 등이 이 모델과 다른 결과를 만들 수 있습니다.

## English

### Model

Consider a series circuit with an ideal constant voltage source and positive constant R and C, without a separate load or leakage. The capacitor starts at 0 V and follows `dv/dt=(Vin-v)/(RC)`. [MIT 6.002 Lecture 12, pp.5–11](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/84f4b553fc6a1ddd7007465041c4e213_6002_l12.pdf) derives the element law, node equation and initial-value solution. Its pages are labeled Fall 2000 and archived in the Spring 2007 OCW course.

### Solution

The solution is `v(t)=Vin*(1-exp(-t/(RC)))`. The time constant is `tau=RC`. At t=tau, the voltage reaches approximately 63.2% of its final value. This result follows from the ideal first-order circuit model.

### Equations and code

The [Euler approximation](../예제_examples/rc_euler.py) computes the differential equation with a loop. The [Jupyter notebook](../예제_examples/rc_response.ipynb) brings together the equations, numerical results, and plots. The response can be checked by connecting the model assumptions, equations, implementation, and comparison criteria.

The linked script uses 1 kΩ, 1 μF and 3.3 V with 500 steps of 10 μs. The Korean hand calculation uses 100 μF, 5 V and a 0.05 s step. These illustrate the same equation with different inputs; their numerical results are not the same run.

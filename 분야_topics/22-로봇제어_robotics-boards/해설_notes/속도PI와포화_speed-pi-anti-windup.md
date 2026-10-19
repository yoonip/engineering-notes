# 바퀴 속도 PI 제어: 포화된 모터에 적분을 계속 더하면

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 위치 계산 다음에는 속도를 맞춘다

차동구동의 기구학은 원하는 전진·회전 속도를 좌우 바퀴의 목표 속도로 바꾼다. 그러나 목표값을 motor PWM에 그대로 넣어 실제 속도를 보장할 수는 없다. 부하, 마찰과 전압에 따라 같은 명령에서도 속도가 달라진다. encoder로 측정한 속도와 목표를 비교해 명령을 조정하는 폐루프가 필요하다. 여기서는 한 바퀴의 속도 제어를 분리해 다룬다.

오차 $`e=r-\omega`$에서 비례 항은 현재 차이에 반응하고 적분 항은 남아 있는 차이를 시간에 걸쳐 누적한다. PI는 PID에서 미분 항을 사용하지 않는 형태다. encoder 차분의 노이즈를 무조건 미분으로 키우지 않기 위해 이 작은 모델에서는 PI를 선택한다. 실제 PID의 미분 필터와 측정값 기반 미분은 별도 설계다. [MIT Control fundamentals](https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/d98dc04f3311eb4e8c786a342dd07f87_MIT2_017JF09_ch11.pdf)

### 제어기와 plant를 함께 정의한다

연속시간 PI는 $`u^*=K_pe+I`$, $`\dot I=K_ie`$다. 예제의 명령 u는 -1~1의 무차원 값, 속도는 rad/s, 시간은 s로 둔다. 따라서 gain의 단위도 이 정의에 맞아야 한다. plant는

```math
\tau\dot\omega+\omega=Ku,\qquad \tau\gt0.
```

샘플 간 u가 일정하다는 zero-order hold 가정으로 미분방정식을 적분하면

```math
\omega_{k+1}=a\omega_k+K(1-a)u_k,\qquad a=e^{-\Delta t/\tau}.
```

이 식은 해당 1차 plant의 샘플 구간 해다. 실제 모터의 전류·전압, backlash와 정지 마찰까지 포함하는 정밀 모델은 아니다. 포화가 없는 연속계에서 PI를 연결한 특성 다항식은 $`\tau s^2+(1+KK_p)s+KK_i`$다. 양의 계수 조건은 이 2차 연속 모델의 안정성 분석에 도움이 되지만, 임의의 샘플 주기·지연·포화를 가진 디지털 시스템을 자동 보증하지 않는다.

### 포화 중 누적되는 적분을 제한한다

출력은 $`u=\min(u_{max},\max(u_{min},u^*))`$로 제한한다. 도달할 수 없는 목표에서 계속 적분하면 내부 I가 커져 목표를 낮춘 뒤에도 회복이 늦다. 이것이 windup이다. MathWorks는 back-calculation과 conditional integration인 clamping을 별도의 anti-windup 방식으로 설명한다. [MathWorks anti-windup](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html)

`PIController.update()`는 먼저 $`I_c=I+K_i\Delta t e`$를 계산한다. 이 후보로 만든 출력이 상한 밖이고 e도 양수이거나 하한 밖이고 e도 음수이면 적분 갱신을 거부한다. 그 외에는 후보를 받아들여 포화를 풀어 주는 방향의 변화는 허용한다. 최종 출력은 실제 채택한 I로 다시 계산해 제한한다. 이 순서를 코드와 설명에서 같게 유지한다.

### 구성 예시로 무엇을 확인했나

demo는 $`\tau=0.3`$, K=2, 샘플 주기 0.02 s, $`K_p=0.8`$, $`K_i=2`$에서 목표 1 rad/s를 추종한다. 500단계 후 속도·최대 속도·마지막 명령을 출력한다. 목표·gain·부하는 설명용 구성값이며 실제 로봇의 동정 결과가 아니다. 계산량과 controller 상태는 한 단계당 상수다.

테스트는 이 도달 가능한 목표에서 마지막 오차가 1e-6보다 작고 모든 명령이 범위 안인지 확인한다. 별도 테스트는 매우 큰 오차를 1,000번 주어도 바깥 방향 적분이 쌓이지 않는지 본다. dt=0은 거부한다. 모델 통과는 보드 안정성이나 안전 정지 검증이 아니며, 실제 측정에서는 encoder 단위·샘플 jitter·명령 포화·적분 초기화·전류 제한을 함께 확인해야 한다. 좌우 controller를 조합할 때에는 바퀴별 오차뿐 아니라 body yaw 오차도 별도 상태로 살핀다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" pi
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### After kinematics, regulate wheel speed

Differential-drive kinematics converts desired body motion into wheel-speed targets. Mapping those targets directly to PWM does not guarantee actual speed because load, friction, and supply voltage vary. A closed loop compares encoder-derived speed with the target. This example isolates one wheel's speed loop.

For error $`e=r-\omega`$, proportional action responds to the present difference and integral action accumulates persistent error. PI is PID without derivative action. This model avoids amplifying noisy encoder differences with an unfiltered derivative; derivative filtering and measurement-based derivative action are separate design choices. [MIT Control fundamentals](https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/d98dc04f3311eb4e8c786a342dd07f87_MIT2_017JF09_ch11.pdf)

### Define controller and plant together

Continuous PI uses $`u^*=K_pe+I`$ and $`\dot I=K_ie`$. Command u is dimensionless from -1 to 1, speed is rad/s, and time is seconds; gains must match those units. The plant is

```math
\tau\dot\omega+\omega=Ku,\qquad \tau\gt0.
```

Holding u constant over each sample interval gives the exact sampled solution of this plant:

```math
\omega_{k+1}=a\omega_k+K(1-a)u_k,\qquad a=e^{-\Delta t/\tau}.
```

It omits detailed motor electrical dynamics, backlash, and static friction. Without saturation, continuous PI yields characteristic polynomial $`\tau s^2+(1+KK_p)s+KK_i`$. Positive coefficients inform stability of this second-order continuous model, not an arbitrary delayed, sampled, saturated implementation.

### Stop accumulation that drives farther into saturation

Output is limited by $`u=\min(u_{max},\max(u_{min},u^*))`$. An unreachable target can otherwise grow I until recovery remains slow even after lowering the target. MathWorks distinguishes back-calculation and clamping/conditional integration as anti-windup strategies. [MathWorks anti-windup](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html)

`update()` first proposes $`I_c=I+K_i\Delta t e`$. It rejects the update if the candidate output exceeds the upper bound with positive error or the lower bound with negative error. Other updates, including those unwinding saturation, are allowed. It then recomputes and clamps the output using the accepted integral value.

### What the constructed example verifies

The demo uses $`\tau=0.3`$, K=2, a 0.02-second sample period, $`K_p=0.8`$, and $`K_i=2`$ to track 1 rad/s. It prints final speed, peak speed, and final command after 500 steps. These are chosen illustration parameters, not identification results from a robot. Per-step work and controller storage are constant.

Tests require final error below 1e-6 for this reachable target and all commands within bounds. A separate 1,000-step large-error test checks that outward integral does not accumulate. A zero timestep is rejected. Passing the model does not establish board stability or safe stopping. Target verification additionally needs encoder units, sample jitter, saturation, integral initialization, and current limits. Combining two wheel loops also requires examining body yaw error separately.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" pi
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [MIT 2.017J: Control fundamentals](https://ocw.mit.edu/courses/2-017j-design-of-electromechanical-robotic-systems-fall-2009/d98dc04f3311eb4e8c786a342dd07f87_MIT2_017JF09_ch11.pdf): 폐루프와 PI/PID / feedback and PI/PID
- [MathWorks: Anti-windup control](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html): 포화·clamping / saturation and clamping

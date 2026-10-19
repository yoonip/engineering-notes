# 차동구동 로봇: 바퀴 회전에서 위치 추정까지

[Robotics & Boards](../README.md) · [계산 코드](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 두 바퀴로 움직임을 나누어 보기

차동구동 로봇은 좌우 바퀴의 속도 차이로 방향을 바꾼다. 여기서는 평면, 강체 차체, 미끄럼 없는 구름, 같은 유효 반지름 r, 바퀴 간격 L을 가정한다. 좌표는 차체 앞쪽 x, 왼쪽 y, 반시계 방향 yaw를 양수로 정한다. 모터의 전기적 회전 부호와 이 정의의 전진 부호는 장착 방향에 따라 다를 수 있다. [Dellaert·Hutchinson, Differential Drive](https://www.roboticsbook.org/S52_diffdrive_actions.html)

바퀴 각속도 $`\dot\phi_L,\dot\phi_R`$의 단위는 rad/s다. 접지점의 구름 조건에서 바퀴의 전진 속도는 각각 $`r\dot\phi_L,r\dot\phi_R`$이고, 차체 중심의 속도와 회전은

$$v=\frac r2(\dot\phi_R+\dot\phi_L),\qquad
\omega=\frac rL(\dot\phi_R-\dot\phi_L).$$

합은 전진, 차는 회전을 정한다. 반대로 원하는 $`(v,\omega)`$에서

$$\dot\phi_L=\frac{v-L\omega/2}{r},\qquad
\dot\phi_R=\frac{v+L\omega/2}{r}.$$

r과 L이 양수라는 조건이 필요하다. 최대 바퀴 속도를 넘는 명령은 실제로 구현되지 않으며, 좌우를 따로 제한하면 원래의 곡률도 바뀔 수 있다. 속도·가속도 제한과 command timeout을 기구학 식과 별도로 다루는 이유다. [ROS 2 diff_drive_controller](https://control.ros.org/rolling/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html)

### 바퀴에서 이동 거리를 얻기

엔코더 각도 변화 $`\Delta\phi`$에 r을 곱하면 바퀴 이동 거리다. count를 각도로 바꿀 때는 한 바퀴당 count의 정의, quadrature 배율과 감속비를 일치시킨다. $`\Delta s_L,\Delta s_R`$가 주어지면

$$\Delta s=(\Delta s_R+\Delta s_L)/2,\qquad
\Delta\theta=(\Delta s_R-\Delta s_L)/L.$$

이는 바퀴 이동을 누적한 odometry이며 절대 위치를 직접 측정한 값은 아니다. 미끄럼·반지름 오차·기어 유격·시간 동기 오차가 누적된다. ROS의 `open_loop` 방식처럼 명령 속도로 적분한 값은 엔코더 feedback을 사용한 추정과도 구분한다. 반지름은 거리 배율에, 바퀴 간격은 주로 곡선 운동의 회전에 영향을 준다. [ROS 파라미터와 feedback 설명](https://control.ros.org/rolling/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html)

### 원호 적분과 직진 극한

한 측정 구간에서 일정한 차체 v와 $`\omega`$를 가정하면 $`\dot x=v\cos\theta`$, $`\dot y=v\sin\theta`$를 적분할 수 있다. $`a=\Delta\theta/2`$, $`\mathrm{sinc}(a)=\sin(a)/a`$이고 $`\mathrm{sinc}(0)=1`$로 놓으면

$$x'=x+\Delta s\mathrm{sinc}(a)\cos(\theta+a),\qquad
y'=y+\Delta s\mathrm{sinc}(a)\sin(\theta+a),\qquad
\theta'=\theta+\Delta\theta.$$

구간 중간 방향을 쓰되 sinc로 원호 길이와 chord의 차이를 반영한 식이다. 회전량이 0에 가까워도 나눗셈이 불안정해지지 않도록 예제는 작은 a에서 $`1-a^2/6+a^4/120`$을 쓴다. 이것은 구간별 일정 곡률 모형의 정확한 적분과 그 수치 근사이며, 바퀴 거리만으로 구간 안의 임의 운동을 모두 복원했다는 뜻은 아니다.

### 검증과 실제 보정

`wheel_rates`는 역기구학을, `odometry_step`은 위 적분을 구현한다. 독립적인 기준은 양쪽 같은 거리일 때 직진, 반대 거리일 때 제자리 회전, 한 바퀴가 정지한 90도 원호다. 같은 일정 곡률 운동을 100개 구간으로 나누어도 같은 위치가 되는지와 역방향 이동으로 복귀하는지도 테스트한다.

실제 로봇에서는 알려진 거리와 회전각을 외부 기준으로 측정해 r·L을 보정한다. 바닥과 속도, 하중을 기록하고 오차 분포와 covariance를 추정한다. 이상 기구학 테스트를 통과했다고 실물의 주행 안전성·정확도·센서 융합까지 검증된 것은 아니다.

## English

### Separate translation and turning

Assume a planar rigid differential-drive robot, rolling without slip, equal effective wheel radius r, and positive separation L. Body x points forward, y left, and positive yaw is counterclockwise. Electrical motor signs can differ from forward wheel signs because of mounting. [Dellaert and Hutchinson](https://www.roboticsbook.org/S52_diffdrive_actions.html)

Wheel rates in rad/s give forward wheel speeds $`r\dot\phi_L,r\dot\phi_R`$. Their sum gives center velocity $`v=r(\dot\phi_R+\dot\phi_L)/2`$ and their difference gives $`\omega=r(\dot\phi_R-\dot\phi_L)/L`$. Inverting gives $`\dot\phi_L=(v-L\omega/2)/r`$ and $`\dot\phi_R=(v+L\omega/2)/r`$. Positive r and L are required.

Commands beyond actuator limits are not physically realized. Independently clipping wheels can change curvature. Velocity/acceleration limits and stale-command timeouts therefore remain separate from kinematics. [ROS controller](https://control.ros.org/rolling/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html)

### Integrate measured travel

Wheel travel is r times encoder angle change. Counts-to-angle conversion must match counts per revolution, quadrature convention, and gearing. Given travel increments, $`\Delta s=(\Delta s_R+\Delta s_L)/2`$ and $`\Delta\theta=(\Delta s_R-\Delta s_L)/L`$.

Odometry integrates wheel movement rather than directly measuring absolute position. Slip, geometry errors, backlash, and timestamp mismatch accumulate. Integrating commanded velocity in open-loop mode differs from using encoder feedback. Radius affects distance scale; separation particularly affects turning. [Feedback and parameters](https://control.ros.org/rolling/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html)

### Arc integration and the straight-line limit

For constant body v and $`\omega`$ over one interval, integrate $`\dot x=v\cos\theta`$ and $`\dot y=v\sin\theta`$. With $`a=\Delta\theta/2`$ and unnormalized sinc, the displacement is $`\Delta s\mathrm{sinc}(a)(\cos(\theta+a),\sin(\theta+a))`$, and heading increases by $`\Delta\theta`$. Define sinc at zero as one. This corrects the midpoint direction for the difference between arc and chord.

The implementation uses $`1-a^2/6+a^4/120`$ near zero to avoid unstable division. The expression integrates a piecewise constant-curvature model; wheel increments alone do not recover arbitrary within-interval motion.

### Verification and calibration

`wheel_rates` and `odometry_step` implement inverse kinematics and integration. Checks use independent straight, in-place spin, and stationary-wheel quarter-circle cases, plus 100-way subdivision and inverse travel under the same model.

A physical robot needs external distance/angle references to calibrate r and L. Record floor, speed, and load and estimate error distributions and covariance. Ideal kinematics tests do not establish physical driving accuracy, safety, or sensor-fusion validity.

## 출처 / Sources

저자 공개 교재의 기구학을 ROS controller의 기하·feedback·제한 규칙과 대조했다. / The authors' textbook kinematics were checked against ROS geometry, feedback, and limit semantics. 확인 / checked: 2026-10-19.

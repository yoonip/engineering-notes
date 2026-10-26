# MATLAB·Octave 질량·스프링 상태공간과 수치 적분

이 예제는 질량·스프링·감쇠기의 자유 운동을 행렬로 표현하고, 행렬 지수·해석해·실제 ODE 솔버·직접 구현한 RK4를 같은 조건에서 비교합니다. GNU Octave 11.3.0의 실제 `.m` 파서와 런타임에서 실행한 수치 실습입니다. MATLAB과 Simulink 실행 기록은 포함하지 않습니다.

소스는 [mass_spring_demo.m](mass_spring_demo.m), 실제 명령·소스 SHA·수치 결과는 [example.json](example.json)에 기록합니다. 공식 문서의 코드 예제를 복사하지 않고 이 비교를 위해 직접 작성한 예제입니다.

## MATLAB과 GNU Octave의 역할

MATLAB은 수치 계산 언어이자 상용 개발 환경입니다. MathWorks의 산업 자료는 MATLAB·Simulink를 이용하는 대상 모델링, 제어기 설계, 검증과 코드 생성의 흐름을 설명합니다. 이 실습은 그중 작은 선형 모델의 수치 계산만 다룹니다. 산업용 제어기의 배포나 검증 결과로 해석하지 않습니다. [MathWorks 제어 시스템 자료](https://www.mathworks.com/solutions/control-systems.html)

GNU Octave는 행렬 계산과 수치 실험을 지원하며 MATLAB과 주로 호환되는 별도 언어·실행 환경입니다. 이 파일은 공통 문법과 기본 함수만 사용하지만, 두 제품의 모든 함수·툴박스·솔버 구현이 같다는 뜻은 아닙니다. 실제 실행 결과의 제품명은 GNU Octave입니다. [GNU Octave 소개](https://octave.org/about)

| 대상 | 이 예제에서의 역할 | 확인 범위 |
| --- | --- | --- |
| MATLAB 문법과 함수 인터페이스 | 열벡터, 행렬 연산, 함수 핸들, `ode45`·`expm` 사용법입니다. | 공식 문서와 공통 구문을 참고합니다. |
| GNU Octave 11.3.0 | 이 `.m` 파일을 해석하고 실제 수치를 계산합니다. | 아래 496개 검사의 실행 대상입니다. |
| Simulink·추가 제어 툴박스 | 이 예제의 의존성이 아닙니다. | 실행하거나 모델 파일을 만들지 않습니다. |

## 물리 모델과 상태의 단위

외력이 없는 운동방정식은 `m x'' + c x' + k x = 0`입니다. 질량은 1 kg, 감쇠 계수는 0.4 N·s/m, 스프링 상수는 4 N/m로 정합니다. 위치 `x`는 m, 속도 `v=x'`는 m/s, 시간은 s입니다.

상태를 열벡터 `y=[x;v]`로 두면 다음과 같습니다.

`y' = A y`, `A=[0,1;-4,-0.4]`입니다. 첫 행은 `x'=v`, 둘째 행은 `v'=-4x-0.4v`를 뜻합니다. 따라서 상태 행렬의 모든 원소가 같은 단위를 갖는 것은 아닙니다. 위치와 속도의 오차도 한 개의 단위 없는 값으로 합치지 않고 각각 비교합니다.

시작 상태는 `[1;0]`, `[0;1]`, `[-0.5;0.3]`의 세 경우입니다. 동일한 0~5초 구간에서 각 경우를 독립적으로 계산합니다. `initials(:,index)`는 현재 열을 선택하므로 행벡터 `[1,0]`와 구별해야 합니다.

## 독립 기준과 적분 방법

부족감쇠 조건 `m>0, k>0, c>=0, c²<4mk`에서 `alpha=c/(2m)`, `omega_n²=k/m`, `omega=sqrt(omega_n²-alpha²)`로 둡니다. 직접 정리한 해석식은 다음과 같습니다.

`x(t)=exp(-alpha*t)*(x0*cos(omega*t)+(v0+alpha*x0)/omega*sin(omega*t))`입니다.

이를 미분하면 `v(t)=exp(-alpha*t)*(v0*cos(omega*t)-(alpha*v0+omega_n²*x0)/omega*sin(omega*t))`입니다. 이 식은 수치 적분기의 출력을 기준값으로 재사용하지 않습니다. 임계감쇠와 과감쇠도 물리적으로 가능한 상태이지만 이 파일의 해석식 지원 범위에는 포함하지 않습니다.

상수 행렬의 해 `expm(A*t)*y0`와 위 식을 153개 상태에서 비교합니다. `expm`은 행렬 지수이고 `exp`는 원소별 지수입니다. `exp(A*t)`로 바꾸면 서로 결합된 위치·속도 상태의 해를 계산하지 못합니다. [MathWorks expm](https://www.mathworks.com/help/matlab/ref/expm.html)

실제 `ode45` 호출은 함수 핸들 `@(t,y) A*y`를 사용합니다. 자율계라 `t`를 계산식에 쓰지 않더라도 솔버가 요구하는 두 입력을 유지합니다. 상대 허용치는 `1e-9`, 위치·속도의 성분별 절대 허용치는 각각 `1e-11`로 정합니다. 출력 요청 시각 51개는 적응형 솔버의 내부 시간 간격과 구별해야 합니다. [GNU Octave ODE 문서](https://docs.octave.org/latest/Matlab_002dcompatible-solvers.html), [MATLAB ode45 문서](https://www.mathworks.com/help/matlab/ref/ode45.html)

직접 구현한 고정 간격 RK4는 시작점, 두 중간 후보, 끝 후보의 미분을 `1:2:2:1`로 결합합니다. 이 방식의 4차 수렴은 `ode45`와 같은 알고리즘이라는 뜻이 아닙니다. 이 예제에서는 간격을 반으로 줄일 때 관측되는 위치 오차의 감소율을 따로 계산합니다.

## 입력부터 결과까지의 흐름

1. 물리 계수와 두 성분의 초기 상태를 열벡터로 구성합니다.
2. 같은 시각의 해석해와 행렬 지수를 비교하고 에너지 미분식을 검사합니다.
3. 세 초기 상태에 대해 실제 `ode45`를 호출하고 위치·속도·시작 상태·요청 시각을 비교합니다.
4. 50·100·200개 구간의 RK4를 실행하고, 최대 오차와 관측 수렴 차수를 계산합니다.
5. 영 평형, 감쇠가 없는 경계, 지원 범위 밖의 여덟 입력을 검사합니다.
6. 모든 조건이 참이면 결과 JSON을 저장하고 PASS 집계를 출력합니다.

직접 계산한 첫 RK4 구간의 예입니다. `y0=[1;0]`, `h=0.1`이면 `k1=[0;-4]`, `k2=[-0.2;-3.92]`, `k3=[-0.196;-3.8816]`, `k4=[-0.38816;-3.766336]`입니다. 가중합을 적용한 첫 상태는 약 `[0.9803306667;-0.3894922667]`입니다. 여기서 `k1` 등의 이름은 스프링 상수 `stiffness`가 아니라 단계별 미분을 뜻합니다.

대표 추적은 실제 200구간 RK4에서 읽은 값입니다. 표시는 소수점 아래 9자리로 반올림하며, 원래 값은 JSON에 보관합니다.

| 시간 s | 위치 m | 속도 m/s | 상태의 의미 |
| --- | ---: | ---: | --- |
| 0.00 | 1.000000000 | 0.000000000 | 변위 1 m에서 정지로 출발합니다. |
| 1.25 | -0.570415659 | -0.952519786 | 평형점을 지나 음의 방향으로 움직입니다. |
| 2.50 | 0.098550538 | 1.177393798 | 양의 방향으로 되돌아옵니다. |
| 3.75 | 0.224157952 | -0.877624285 | 양의 변위에서 음의 방향으로 움직입니다. |
| 5.00 | -0.336851830 | 0.370691200 | 감쇠된 진동을 계속합니다. |

## 실제 검사와 수치 결과

2026-10-26에 GNU Octave 11.3.0의 명령행 런타임으로 실행했습니다. 종료 코드는 0, 표준 오류는 빈 문자열입니다.

```text
PASS matlab-octave checks=496 matrix_cases=153 ode_cases=3 rk4_grids=3 rejected_inputs=8
```

| 검사 | 실제 개수 | 기준 |
| --- | ---: | --- |
| 해석해·행렬 지수의 위치·속도, 에너지 미분 | 459 | 3개 초기 상태 × 51개 시각 × 3개 조건입니다. |
| 실제 `ode45` 실행 | 12 | 3개 초기 상태마다 시각·위치·속도·초기 상태를 비교합니다. |
| 고정 간격 RK4 | 12 | 3개 격자마다 위치·속도·표본 에너지 감소·에너지 부호를 확인합니다. |
| 격자 세분화의 관측 차수 | 2 | 인접한 두 격자 쌍의 위치 오차 비율을 비교합니다. |
| 영 평형과 무감쇠 경계 | 3 | 0 상태 보존, 무감쇠 위치와 에너지 드리프트를 검사합니다. |
| 지원 계약 밖 입력의 거절 | 8 | 지정한 오류 식별자가 실제 발생하는지 확인합니다. |
| 합계 | 496 | 지정한 유한한 예제의 실제 조건 검사 수입니다. |

세 `ode45` 실행의 최대 위치 오차는 약 `2.376e-10 m`, 최대 속도 오차는 약 `4.706e-10 m/s`입니다. 설정한 허용치는 내부 오차 제어를 위한 값이므로 모든 문제에서 이 전역 오차를 보장하는 수치는 아닙니다.

| RK4 간격 s | 최대 위치 오차 m | 최대 속도 오차 m/s |
| ---: | ---: | ---: |
| 0.1 | 4.833180e-5 | 9.967298e-5 |
| 0.05 | 3.000444e-6 | 6.179480e-6 |
| 0.025 | 1.864959e-7 | 3.846482e-7 |

관측 차수 `log2(거친 격자 오차/고운 격자 오차)`는 4.009725, 4.007960입니다. 매끄러운 이 고정 문제에서 4차에 가까운 감소를 확인한 결과입니다. 임의의 큰 시간 간격, 강성 계, 불연속 입력에 대한 보증으로 일반화하지 않습니다.

에너지는 `E=mv²/2+kx²/2`이며 해석적으로 `dE/dt=-cv²`입니다. 선택한 세 격자에서는 표본 에너지의 증가가 없는지 검사합니다. RK4가 임의의 간격에서 에너지를 정확히 보존하거나 항상 감소시킨다는 주장은 아닙니다. 무감쇠 경계에서는 에너지 2 J에 대한 수치 드리프트를 별도로 비교합니다.

거절 검사는 질량 0, 강성 0, 음의 감쇠, 임계감쇠, NaN 질량, 행벡터 초기 상태, 무한대 초기 위치, 적분 단계 0입니다. 임계감쇠의 거절은 물리 모델이 잘못되었다는 뜻이 아니라 이 부족감쇠 해석식의 지원 범위를 명시하는 동작입니다.

## 재현 명령과 도구

[공식 Windows 배포](https://octave.org/download)의 GNU Octave 11.3.0을 사용했습니다. 검증 환경에서는 압축 배포 중 CLI 실행 파일, 필요한 DLL·수치 모듈·기본 함수만 임시 경로에 추출했습니다. 그래픽 도구나 추가 패키지는 요구하지 않습니다. 공식 배포 자체는 이 저장소에 포함하지 않습니다.

Octave가 PATH에 있으면 이 폴더에서 다음과 같이 실행합니다. 결과 파일의 위치는 호출 인자로 정합니다.

```powershell
octave-cli --no-window-system --quiet --no-init-file --no-site-file --no-history --eval "mass_spring_demo('result.json');"
```

실제 검증은 소스를 임시 작업 폴더로 바이트 그대로 복사한 뒤 위 인자로 실행했습니다. 원본과 실행 사본의 SHA-256은 모두 `7ca29390fc773ff6271e57226976fa3f94b6929874e7051fbb11f80dec334b98`입니다. 독립 추출 런타임의 `OCTAVE_HOME`과 DLL 검색 경로는 실행 프로세스에만 지정했습니다. 정확한 실행 파일 경로, 작업 폴더와 환경 변수는 JSON에 기록합니다.

MATLAB에서 같은 함수를 시험하려면 파일이 있는 폴더에서 `report = mass_spring_demo('result.json');`를 호출할 수 있습니다. 다만 이 기록에서는 MATLAB을 실행하지 않았으며, 사용 버전의 `jsonencode`·`ode45` 지원과 결과는 해당 환경에서 별도로 확인해야 합니다. GNU Octave와 MATLAB의 내부 적응 간격이나 반올림 결과가 같다고 가정하지 않습니다.

## 문법과 언어 차이

| 문법·도구 | 이 파일의 사용 목적 | 다른 언어에서의 주의점 |
| --- | --- | --- |
| `[x;v]`, `(:,index)` | 세미콜론은 다음 행, 콜론은 모든 행을 선택합니다. | C/C++ 배열과 Python 리스트에는 같은 열벡터 의미가 자동으로 생기지 않습니다. |
| `*`와 `.*` | 행렬 상태 갱신과 시각별 성분 곱을 구분합니다. | NumPy에서는 행렬 곱이 `@`이고 `*`가 원소별 곱입니다. |
| `.'` | 복소수 켤레 없이 행·열 방향을 바꿉니다. | `'`는 켤레 전치이므로 복소수 모델에서는 차이가 생깁니다. |
| `@(t,y)` | 솔버에 미분 함수를 전달합니다. | C의 함수 포인터나 C++ 람다와 역할이 비슷하지만 호출 인터페이스는 솔버마다 다릅니다. |
| `expm`·`ode45` | 기본 수치 라이브러리의 실제 연산을 호출합니다. | C/C++ 표준 라이브러리에는 이 행렬 ODE API가 없으며 Python도 별도 수치 패키지가 필요합니다. |
| `error`·오류 식별자 | 예상한 계약 거절만 통과로 집계합니다. | 단순히 예외가 하나 발생했다는 이유로 파서 오류까지 성공으로 세면 안 됩니다. |

## 적용 조건과 한계

행렬 상태공간은 작은 진동 모델의 초기값 계산, 단위·배열 방향 확인, 적분 간격 선정의 기초 실습에 사용할 수 있습니다. 실제 장치에 연결하려면 질량·감쇠·강성의 식별, 센서 오차, 비선형 마찰과 포화, 외력, 계산 주기와 안전 조건을 따로 다뤄야 합니다.

이 실습은 이상적인 1자유도 선형 수동 계의 자유 응답입니다. 피드백 제어, 하드웨어 입출력, 실시간 타깃, 동역학 전체 검증을 구현하지 않습니다. 내부 RK4 함수도 선택한 2성분 행렬 문제를 위한 도우미이며 임의의 ODE 입력을 모두 검증하는 범용 라이브러리가 아닙니다.

## 복습 요약

위치와 속도를 한 열벡터에 넣어 미분방정식을 행렬 곱으로 표현합니다. 별도로 유도한 삼각함수 해를 기준으로 행렬 지수와 실제 ODE 적분을 비교하고, 고정 간격 RK4의 격자를 줄여 수렴을 확인합니다. 단위별 오차, 초기 조건과 지원 범위 검사를 함께 기록해야 수치가 맞다는 판단의 범위를 알 수 있습니다.

## 공식 출처와 라이선스

- [GNU Octave 소개](https://octave.org/about)는 언어의 수치 계산 목적과 MATLAB 호환 범위를 설명합니다. GNU Octave 실행 파일은 GPLv3 또는 이후 버전 조건으로 배포합니다.
- [GNU Octave 공식 배포](https://octave.org/download)는 사용한 Windows 배포의 출처입니다. 다운로드한 파일의 관측 SHA는 JSON에 보관합니다.
- [GNU Octave ODE 문서](https://docs.octave.org/latest/Matlab_002dcompatible-solvers.html)는 `ode45`의 인터페이스·요청 시각·허용치 설명을 참고한 자료입니다. 확인 당시 온라인 매뉴얼의 버전 표시는 11.1.0이며 실제 실행 버전은 11.3.0입니다.
- [MathWorks ode45](https://www.mathworks.com/help/matlab/ref/ode45.html), [MathWorks expm](https://www.mathworks.com/help/matlab/ref/expm.html)은 MATLAB 함수 계약과 행렬 지수의 의미를 확인한 공식 문서입니다.
- [MathWorks 제어 시스템 자료](https://www.mathworks.com/solutions/control-systems.html)는 산업에서의 모델링·설계·시험 연결을 설명하는 제품 자료입니다. 여기에서 제시하는 제품별 기능이나 산업 결과를 이 작은 실습에서 재현했다는 뜻은 아닙니다.

아래 소스는 이 실습을 위해 직접 작성했습니다. 도구와 공식 문서의 라이선스를 새 소스의 라이선스와 동일하게 취급하지 않으며, 배포 도구나 공식 문서의 전문을 이 폴더에 복사하지 않습니다.

## 전체 소스와 줄별 메모

각 의미 있는 실행 줄의 `%` 뒤에 문법 또는 해당 줄의 목적을 짧게 적습니다.

```matlab
function report = mass_spring_demo(output_path) % 질량·스프링의 수치 계산과 실제 비교 실행
  if nargin < 1, output_path = ''; end % 파일을 지정하지 않으면 반환값과 로그만 사용
  mass = 1.0; damping = 0.4; stiffness = 4.0; % kg·N s/m·N/m의 수동 계
  final_time = 5.0; checks = 0; % 5초 계산과 실제 검사 수
  A = [0, 1; -stiffness / mass, -damping / mass]; % 위치·속도의 행렬 상태공간
  initials = [1, 0, -0.5; 0, 1, 0.3]; % 변위 시작·속도 시작·비대칭 초기 상태
  times = linspace(0, final_time, 51).'; % ODE 출력과 비교할 열벡터 시각
  ode_cases = struct([]); % 초기 상태별 실제 오차를 저장할 구조체 목록
  for index = 1:size(initials, 2) % 세 초기 상태를 독립적으로 계산
    y0 = initials(:, index); % 현재 위치와 속도를 열벡터로 선택
    validate_problem(mass, damping, stiffness, y0); % 지지하는 물리 매개변수와 상태 모양 확인
    exact = closed_form(mass, damping, stiffness, y0, times); % 삼각함수로 푼 독립 해석해
    for sample = 1:numel(times) % 행렬 지수와 해석해를 같은 51시각에 대조
      matrix_state = expm(A * times(sample)) * y0; % 원소별 exp가 아닌 행렬 지수
      checks = verify(checks, abs(matrix_state(1) - exact(1, sample)) < 2e-12, 'matrix position'); % 미터 오차 비교
      checks = verify(checks, abs(matrix_state(2) - exact(2, sample)) < 4e-12, 'matrix velocity'); % m/s 오차를 따로 비교
      acceleration = -stiffness / mass * exact(1, sample) - damping / mass * exact(2, sample); % 운동방정식의 가속도
      energy_rate = mass * exact(2, sample) * acceleration + stiffness * exact(1, sample) * exact(2, sample); % 에너지의 연쇄 미분
      checks = verify(checks, abs(energy_rate + damping * exact(2, sample)^2) < 2e-12, 'dissipation identity'); % dE/dt=−c v² 대조
    end % 행렬·해석해·에너지 관계의 시각별 검사 끝
    options = odeset('RelTol', 1e-9, 'AbsTol', [1e-11, 1e-11]); % 적응형 ODE의 상대·성분별 절대 허용치
    [actual_times, states] = ode45(@(t, y) A * y, times, y0, options); % 실제 런타임의 비강성 ODE 적분
    target = closed_form(mass, damping, stiffness, y0, actual_times).'; % ODE의 행별 출력과 같은 배열 방향
    position_error = max(abs(states(:, 1) - target(:, 1))); % 위치의 최대 절대 오차 m
    velocity_error = max(abs(states(:, 2) - target(:, 2))); % 속도의 최대 절대 오차 m/s
    checks = verify(checks, numel(actual_times) == numel(times) && max(abs(actual_times - times)) < 1e-12, 'requested ODE times'); % 요청한 관측 시각 확인
    checks = verify(checks, position_error < 5e-7, 'ode45 position'); % 전체 출력 시각의 위치 정합
    checks = verify(checks, velocity_error < 1e-6, 'ode45 velocity'); % 속도 정합을 별도 단위로 확인
    checks = verify(checks, max(abs(states(1, :).'-y0)) < 1e-14, 'ode45 initial state'); % 적분 전 초기 조건 보존
    ode_cases(index) = struct('initial_state', y0, 'samples', numel(actual_times), 'maximum_position_error_m', position_error, 'maximum_velocity_error_m_s', velocity_error); % 실제 ODE 결과 기록
  end % 초기 상태 세 경우의 실제 ODE 실행 끝
  step_counts = [50, 100, 200]; grid_results = struct([]); % 고정 간격 RK4의 수렴 비교
  for index = 1:numel(step_counts) % 같은 5초를 세 시간 간격으로 적분
    steps = step_counts(index); % 현재 적분 단계 수
    [grid_times, grid_states] = integrate_rk4(A, initials(:, 1), final_time, steps); % 직접 구현한 고정 간격 적분
    exact = closed_form(mass, damping, stiffness, initials(:, 1), grid_times); % 적분 결과를 쓰지 않는 해석해
    position_error = max(abs(grid_states(1, :) - exact(1, :))); % 위치의 전체 최대 오차
    velocity_error = max(abs(grid_states(2, :) - exact(2, :))); % 속도의 전체 최대 오차
    energy = mass * grid_states(2, :).^2 / 2 + stiffness * grid_states(1, :).^2 / 2; % 실제 수치 상태의 줄 단위 에너지
    checks = verify(checks, position_error < 1e-4, 'RK4 position'); % 거친 격자도 큰 오차 없이 계산
    checks = verify(checks, velocity_error < 2e-4, 'RK4 velocity'); % 같은 격자의 속도 비교
    checks = verify(checks, all(diff(energy) <= 1e-10), 'sampled damped energy'); % 이 선택 간격에서의 에너지 감소
    checks = verify(checks, all(energy >= 0), 'nonnegative mechanical energy'); % 수동 계의 에너지 부호
    grid_results(index) = struct('steps', steps, 'step_s', final_time / steps, 'maximum_position_error_m', position_error, 'maximum_velocity_error_m_s', velocity_error, 'maximum_energy_increase_J', max(diff(energy))); % 실제 격자 결과
  end % 고정 간격 세 실행 끝
  observed_orders = zeros(1, 2); % 인접 격자의 관측 수렴 차수
  for index = 1:2 % 간격을 반으로 줄인 두 쌍
    observed_orders(index) = log2(grid_results(index).maximum_position_error_m / grid_results(index + 1).maximum_position_error_m); % 위치 오차 감소의 로그
    checks = verify(checks, observed_orders(index) > 3.5 && observed_orders(index) < 4.5, 'fourth order convergence'); % 이번 매끄러운 문제의 4차 수렴
  end % 실제 수렴 차수 확인 끝
  [~, zero_states] = integrate_rk4(A, [0; 0], final_time, 50); % 평형 상태의 경계 입력
  checks = verify(checks, all(zero_states(:) == 0), 'zero equilibrium'); % 0 상태에 가짜 운동이 생기지 않기
  undamped_A = [0, 1; -4, 0]; % 감쇠가 0인 보존계의 경계
  [undamped_times, undamped_states] = integrate_rk4(undamped_A, [1; 0], final_time, 200); % 같은 RK4로 경계 계산
  undamped_exact = closed_form(1, 0, 4, [1; 0], undamped_times); % c=0에서도 쓰는 원래 해석식
  undamped_energy = undamped_states(2, :).^2 / 2 + 2 * undamped_states(1, :).^2; % 단위 질량 계의 역학적 에너지
  checks = verify(checks, max(abs(undamped_states(1, :) - undamped_exact(1, :))) < 2e-6, 'undamped position'); % 무감쇠 위치 경계
  checks = verify(checks, max(abs(undamped_energy - 2)) < 1e-6, 'undamped energy drift'); % 보존계에서도 수치 오차는 별도 확인
  unsupported = {@() validate_problem(0, 0.4, 4, [1; 0]), @() validate_problem(1, 0.4, 0, [1; 0]), @() validate_problem(1, -0.1, 4, [1; 0]), @() validate_problem(1, 4, 4, [1; 0]), @() validate_problem(NaN, 0.4, 4, [1; 0]), @() validate_problem(1, 0.4, 4, [1, 0]), @() validate_problem(1, 0.4, 4, [Inf; 0]), @() integrate_rk4(A, [1; 0], 5, 0)}; % 잘못되거나 해석식 지원 밖인 여덟 입력
  rejected = 0; % 지정한 이유로 거절된 입력 수
  for index = 1:numel(unsupported) % 원본 매개변수를 바꾸지 않고 오류 입력 실행
    caught = false; % 이 호출의 지정 오류 발생 여부
    try % 지원 계약을 벗어나는 함수 호출
      unsupported{index}(); % 오류가 나야 하는 입력 적용
    catch failure % 런타임의 실제 오류 객체 확인
      caught = strncmp(failure.identifier, 'mass_spring:', 12); % 관계없는 파서·수치 오류를 통과로 세지 않기
    end % 오류 관측 끝
    checks = verify(checks, caught, 'unsupported input rejection'); % 정해진 계약 오류가 실제 발생
    rejected = rejected + 1; % 확인한 거절 한 건 집계
  end % 여덟 지원 계약 검사 끝
  [trace_times, trace_states] = integrate_rk4(A, [1; 0], final_time, 200); % 대표 0.025초 격자의 입력부터 결과 추적
  sample_indices = [1, 51, 101, 151, 201]; trace = struct([]); % 0·1.25·2.5·3.75·5초 선택
  for index = 1:numel(sample_indices) % 문서용 실제 상태를 같은 적분기에서 읽기
    sample = sample_indices(index); % 선택한 배열 위치
    trace(index) = struct('time_s', trace_times(sample), 'position_m', trace_states(1, sample), 'velocity_m_s', trace_states(2, sample)); % 서로 다른 단위를 이름으로 구분
  end % 대표 시점 추적 끝
  report = struct('status', 'passed_actual_m_runtime_checks', 'runtime_version', version, 'checks', checks, 'matrix_cases', 153, 'ode_cases', ode_cases, 'rk4_grids', grid_results, 'observed_orders', observed_orders, 'rejected_inputs', rejected, 'state_matrix', A, 'mass_kg', mass, 'damping_Ns_m', damping, 'stiffness_N_m', stiffness, 'trace', trace); % 실제 수치와 확인 범위
  if exist('OCTAVE_VERSION', 'builtin') > 0, report.runtime_name = 'GNU Octave'; else, report.runtime_name = 'MATLAB'; end % 실제 해석기를 기록
  if ~isempty(output_path) % 요청한 경우만 결과 JSON 생성
    handle = fopen(output_path, 'w'); % 지정한 임시 결과 파일 열기
    if handle < 0, error('mass_spring:output', 'cannot open output file'); end % 쓰기 실패를 완료로 표시하지 않기
    cleanup = onCleanup(@() fclose(handle)); % 오류가 나도 열린 파일 닫기
    fprintf(handle, '%s\n', jsonencode(report)); % JSON 직렬화도 실제 .m 런타임에서 수행
    clear cleanup; % 저장 뒤 파일 닫기
  end % 선택 결과 파일 작성 끝
  fprintf('PASS matlab-octave checks=%d matrix_cases=153 ode_cases=3 rk4_grids=3 rejected_inputs=%d\n', checks, rejected); % 실제 완료 집계
end % 기본 실행 함수 끝

function validate_problem(mass, damping, stiffness, y0) % 이 해석식이 지원하는 문제의 입력 계약
  parameters = {mass, damping, stiffness}; % 단위가 다른 세 스칼라를 개별 검사
  for index = 1:3 % 각 입력의 자료형과 유한성
    value = parameters{index}; % 현재 매개변수
    if ~isnumeric(value) || ~isscalar(value) || ~isreal(value) || ~isfinite(value), error('mass_spring:parameter', 'finite real scalars required'); end % 비유한·벡터 매개변수 거절
  end % 수치 매개변수 검사 끝
  if mass <= 0 || stiffness <= 0 || damping < 0 || damping^2 >= 4 * mass * stiffness, error('mass_spring:regime', 'positive m,k and underdamped c>=0 required'); end % 임계·과감쇠는 별도 해석식 필요
  if ~isnumeric(y0) || ~isreal(y0) || ~isequal(size(y0), [2, 1]) || ~all(isfinite(y0)), error('mass_spring:state', 'finite 2-by-1 initial state required'); end % 위치·속도의 열벡터 계약
end % 지원 문제 검사 끝

function states = closed_form(mass, damping, stiffness, y0, times) % 고정 계수의 독립 자유감쇠 해석해
  validate_problem(mass, damping, stiffness, y0); % 분모와 감쇠 구간 확인
  if ~isreal(times) || any(~isfinite(times(:))) || any(times(:) < 0), error('mass_spring:time', 'finite nonnegative times required'); end % 앞으로의 유한 시각만 사용
  t = reshape(times, 1, []); % 해석해는 시각별 열을 갖게 정리
  alpha = damping / (2 * mass); natural_squared = stiffness / mass; % 감쇠율과 고유각속도 제곱
  omega = sqrt(natural_squared - alpha^2); % 부족감쇠 진동의 양의 각속도
  decay = exp(-alpha * t); % 원소별 시간 감쇠 인자
  x = decay .* (y0(1) * cos(omega * t) + (y0(2) + alpha * y0(1)) / omega * sin(omega * t)); % 초기 위치·속도를 반영한 해
  v = decay .* (y0(2) * cos(omega * t) - (alpha * y0(2) + natural_squared * y0(1)) / omega * sin(omega * t)); % 같은 위치 식을 미분한 속도
  states = [x; v]; % 위치와 속도를 서로 다른 행에 보관
end % 삼각함수 기준 계산 끝

function [times, states] = integrate_rk4(A, y0, duration, steps) % 행렬 ODE의 직접 고정 간격 적분
  if ~isscalar(steps) || ~isfinite(steps) || steps < 1 || fix(steps) ~= steps, error('mass_spring:steps', 'positive integer steps required'); end % 빈 격자와 소수 단계 거절
  step = duration / steps; times = linspace(0, duration, steps + 1); % 일정한 시간 간격과 관측 시각
  states = zeros(2, steps + 1); states(:, 1) = y0; % 초기 조건을 첫 열에 배치
  for index = 1:steps % 실제 각 시간 구간을 전진
    current = states(:, index); % 구간 시작의 위치·속도
    k1 = A * current; % 시작 상태의 행렬 미분
    k2 = A * (current + step * k1 / 2); % 첫 중간 후보의 미분
    k3 = A * (current + step * k2 / 2); % 두 번째 중간 후보의 미분
    k4 = A * (current + step * k3); % 끝 후보의 미분
    states(:, index + 1) = current + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6; % 1·2·2·1 가중치의 RK4 갱신
  end % 모든 시간 구간 적분 끝
end % 고정 간격 적분 함수 끝

function count = verify(count, condition, message) % 실제 실행한 비교 수와 실패 이유
  count = count + 1; % 조건 한 개를 실제 검사한 집계
  if ~condition, error('mass_spring:check', '%s', message); end % 틀린 수치나 누락된 경계를 실패로 처리
end % 공통 검사 함수 끝
```

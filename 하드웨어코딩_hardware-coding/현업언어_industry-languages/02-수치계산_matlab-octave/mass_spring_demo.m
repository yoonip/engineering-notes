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

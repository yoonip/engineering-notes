from math import copysign, fsum, hypot, isfinite, sqrt
from statistics import NormalDist


def _finite(*values):
    if not all(isfinite(v) for v in values):
        raise ValueError("유한한 값이 필요합니다.")


def _steps(steps):
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps는 양의 정수여야 합니다.")


def resistance_uncertainty(voltage, current, u_voltage, u_current, correlation=0.0):
    """전압·전류의 SI 값으로 저항과 1차 근사 표준불확도를 구한다."""
    _finite(voltage, current, u_voltage, u_current, correlation)
    if current == 0 or min(u_voltage, u_current) < 0 or abs(correlation) > 1:
        raise ValueError("전류, 불확도, 상관계수의 범위를 확인하세요.")
    resistance = voltage / current
    a = u_voltage / current
    b = -resistance * (u_current / current)
    # 두 입력의 상관관계도 포함하며 마지막 반올림 오차만 0으로 제한한다.
    variance = fsum((a * a, b * b, 2 * correlation * a * b))
    return resistance, sqrt(max(0.0, variance))


def least_squares_qr(matrix, observations, rtol=1e-12):
    """열 독립인 실수 m×n 행렬의 최소제곱을 Householder QR로 푼다."""
    a = [list(map(float, row)) for row in matrix]
    b = list(map(float, observations))
    m = len(a)
    n = len(a[0]) if m else 0
    if not n or m < n or len(b) != m or any(len(row) != n for row in a):
        raise ValueError("m >= n인 직사각 행렬과 길이 m의 관측값이 필요합니다.")
    _finite(rtol, *b, *(v for row in a for v in row))
    if not 0 < rtol < 1:
        raise ValueError("rtol은 0과 1 사이여야 합니다.")
    threshold = rtol * max(hypot(*(a[i][j] for i in range(m))) for j in range(n))
    for k in range(n):
        tail_norm = hypot(*(a[i][k] for i in range(k, m)))
        if tail_norm <= threshold:
            raise ValueError("열이 종속이거나 선택한 허용오차에서 분리되지 않습니다.")
        # 부호를 반대로 선택해 비슷한 두 수의 뺄셈을 피한다.
        v = [a[i][k] / tail_norm for i in range(k, m)]
        v[0] += copysign(1.0, v[0])
        v_norm = hypot(*v)
        v = [value / v_norm for value in v]
        for j in range(k, n):
            projection = 2 * fsum(v[i-k] * a[i][j] for i in range(k, m))
            for i in range(k, m):
                a[i][j] -= projection * v[i-k]
        projection = 2 * fsum(v[i-k] * b[i] for i in range(k, m))
        for i in range(k, m):
            b[i] -= projection * v[i-k]
        for i in range(k+1, m):
            a[i][k] = 0.0
    x = [0.0] * n
    # 역행렬을 만들지 않고 상삼각 연립방정식을 뒤에서부터 푼다.
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - fsum(a[i][j] * x[j] for j in range(i+1, n))) / a[i][i]
    return x


def mean_variance(values):
    """한 번의 순회로 표본 수·평균·불편 표본분산을 구한다."""
    count, mean, m2 = 0, 0.0, 0.0
    for value in values:
        _finite(value)
        count += 1
        delta = value - mean
        mean += delta / count
        m2 += delta * (value - mean)
    if count < 2:
        raise ValueError("표본분산에는 두 개 이상의 값이 필요합니다.")
    return count, mean, max(0.0, m2 / (count-1))


def normal_mean_interval(mean, sigma, count, confidence=0.95):
    """알려진 모집단 표준편차를 쓰는 정규 평균 신뢰구간을 구한다."""
    _finite(mean, sigma, confidence)
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("표본 수는 양의 정수여야 합니다.")
    if sigma < 0 or not 0 < confidence < 1:
        raise ValueError("표준편차와 신뢰수준의 범위를 확인하세요.")
    probability = 0.5 + confidence / 2
    if not probability < 1:
        raise ValueError("표현 가능한 정밀도 안의 신뢰수준이 필요합니다.")
    width = NormalDist().inv_cdf(probability) * sigma / sqrt(count)
    return mean-width, mean+width


def decay_euler(initial, tau, duration, steps):
    """y'=-y/tau의 전진 Euler 최종값을 계산한다."""
    _finite(initial, tau, duration)
    _steps(steps)
    if tau <= 0 or duration < 0:
        raise ValueError("tau > 0, duration >= 0이어야 합니다.")
    ratio = (duration / steps) / tau
    if ratio >= 2:
        raise ValueError("감쇠를 재현하려면 dt/tau < 2여야 합니다.")
    value = initial
    for _ in range(steps):
        value -= ratio * value
    return value


def oscillator_verlet(mass, stiffness, initial_x, initial_v, duration, steps):
    """무감쇠 선형 진동자의 (시간, 위치, 속도)를 순서대로 반환한다."""
    _finite(mass, stiffness, initial_x, initial_v, duration)
    _steps(steps)
    if mass <= 0 or stiffness <= 0 or duration < 0:
        raise ValueError("질량·강성은 양수이고 기간은 음수가 아니어야 합니다.")
    dt = duration / steps
    omega2 = stiffness / mass
    if dt * sqrt(omega2) >= 2:
        raise ValueError("이 선형 모델에서는 dt*omega < 2가 필요합니다.")
    x, v = initial_x, initial_v
    yield 0.0, x, v
    for step in range(1, steps+1):
        # 반 시간만큼 속도를 먼저 바꿔 위치와 속도의 갱신을 대칭으로 맞춘다.
        half_v = v - 0.5 * dt * omega2 * x
        x += dt * half_v
        v = half_v - 0.5 * dt * omega2 * x
        yield step * dt, x, v


def heat_ftcs(initial, diffusivity, length, duration, steps):
    """양 끝 온도를 고정한 1차원 균질 열방정식의 최종 온도를 구한다."""
    values = list(map(float, initial))
    _finite(diffusivity, length, duration, *values)
    _steps(steps)
    if len(values) < 3 or diffusivity <= 0 or length <= 0 or duration < 0:
        raise ValueError("격자 세 점 이상, 양의 확산계수·길이, 음수 아닌 시간이 필요합니다.")
    dx = length / (len(values)-1)
    ratio = diffusivity * (duration / steps) / (dx * dx)
    if not isfinite(ratio) or ratio > 0.5:
        raise ValueError("FTCS 안정 조건 alpha*dt/dx^2 <= 1/2를 만족해야 합니다.")
    buffer = values.copy()
    for _ in range(steps):
        # 같은 시간의 이웃값만 읽도록 두 버퍼를 교환한다.
        for i in range(1, len(values)-1):
            buffer[i] = values[i] + ratio * (values[i-1] - 2*values[i] + values[i+1])
        values, buffer = buffer, values
    return values

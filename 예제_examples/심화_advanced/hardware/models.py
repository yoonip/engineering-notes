"""회로, RTL, 통신과 계측의 작은 참조모델."""
from collections import deque
from dataclasses import dataclass
import cmath
import math
import random


def solve_linear(matrix, rhs):
    """부분 피벗 소거법으로 작은 정방 선형계를 푼다."""
    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("정방행렬과 같은 길이의 우변이 필요합니다")
    a = [list(map(float, row)) + [float(b)] for row, b in zip(matrix, rhs)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-18:
            raise ValueError("유일한 해가 없거나 수치적으로 특이합니다")
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        for j in range(col, n + 1):
            a[col][j] /= p
        for row in range(n):
            if row != col:
                factor = a[row][col]
                for j in range(col, n + 1):
                    a[row][j] -= factor * a[col][j]
    return [row[-1] for row in a]


def mna(nodes, resistors, voltage_sources=(), current_sources=()):
    """접지 0 이외의 노드전압과 전압원 양극→음극 전류를 반환한다."""
    index = {node: i for i, node in enumerate(nodes)}
    if 0 in index or len(index) != len(nodes):
        raise ValueError("노드 목록은 접지를 제외하고 중복이 없어야 합니다")
    n = len(nodes)
    size = n + len(voltage_sources)
    a = [[0.0] * size for _ in range(size)]
    b = [0.0] * size
    def pos(node):
        return None if node == 0 else index[node]
    for p, q, resistance in resistors:
        if resistance <= 0:
            raise ValueError("저항은 양수여야 합니다")
        pi, qi, g = pos(p), pos(q), 1.0 / resistance
        if pi is not None:
            a[pi][pi] += g
        if qi is not None:
            a[qi][qi] += g
        if pi is not None and qi is not None:
            a[pi][qi] -= g
            a[qi][pi] -= g
    for p, q, current in current_sources:
        # 양극으로 지정한 노드에서 음극 노드로 전류가 흐른다.
        for node, sign in ((p, -1), (q, 1)):
            i = pos(node)
            if i is not None:
                b[i] += sign * current
    for k, (p, q, voltage) in enumerate(voltage_sources):
        for node, sign in ((p, 1), (q, -1)):
            i = pos(node)
            if i is not None:
                a[i][n + k] += sign
                a[n + k][i] += sign
        b[n + k] = voltage
    x = solve_linear(a, b)
    return {0: 0.0, **dict(zip(nodes, x[:n]))}, x[n:]


def thermal_voltage(temperature=300.0):
    if temperature <= 0:
        raise ValueError("절대온도는 양수여야 합니다")
    return 1.380649e-23 * temperature / 1.602176634e-19


def weak_inversion(vgs, vds, vth=0.45, n=1.5, i0=1e-7, temperature=300.0):
    if n < 1 or i0 <= 0 or vds < 0:
        raise ValueError("n≥1, I0>0, VDS≥0 범위의 모델입니다")
    ut = thermal_voltage(temperature)
    return i0 * math.exp((vgs - vth) / (n * ut)) * -math.expm1(-vds / ut)


def feedback_one_pole(omega, a0=1e5, pole=2 * math.pi * 10, beta=0.1):
    a = a0 / (1 + 1j * omega / pole)
    return a / (1 + beta * a)


def two_pole_margin(loop_dc=1e4, pole1=2 * math.pi * 10, pole2=2 * math.pi * 1e5):
    if loop_dc <= 1 or min(pole1, pole2) <= 0:
        raise ValueError("직류 루프이득>1, 양의 극점이 필요합니다")
    def loop(w):
        return loop_dc / ((1 + 1j * w / pole1) * (1 + 1j * w / pole2))
    lo, hi = 0.0, max(pole1, pole2) * loop_dc
    for _ in range(100):
        mid = (lo + hi) / 2
        if abs(loop(mid)) > 1:
            lo = mid
        else:
            hi = mid
    wc = (lo + hi) / 2
    pm = 180 - math.degrees(math.atan(wc / pole1) + math.atan(wc / pole2))
    return wc, pm


def pdn_impedance(omega, branches):
    if omega <= 0:
        raise ValueError("각주파수는 양수여야 합니다")
    admittance = 0j
    for resistance, inductance, capacitance in branches:
        if resistance < 0 or inductance <= 0 or capacitance <= 0:
            raise ValueError("R≥0, L>0, C>0 이어야 합니다")
        z = resistance + 1j * (omega * inductance - 1 / (omega * capacitance))
        if abs(z) < 1e-30:
            return 0j
        admittance += 1 / z
    if abs(admittance) < 1e-20:
        raise ValueError("무손실 병렬 공진에서 임피던스가 발산합니다")
    return 1 / admittance


def qmul16(a, b):
    """16비트 부호 정수, 소수 8비트 곱셈을 짝수 반올림 후 포화한다."""
    if not all(-32768 <= x <= 32767 for x in (a, b)):
        raise ValueError("16비트 부호 범위를 벗어났습니다")
    product = a * b
    magnitude = abs(product)
    whole, remainder = divmod(magnitude, 256)
    if remainder > 128 or (remainder == 128 and whole % 2):
        whole += 1
    rounded = -whole if product < 0 else whole
    return max(-32768, min(32767, rounded))


def queue_transition(state, valid, data, ready, capacity=2, mutant=False):
    """출력과 입력 수락은 갱신 전 상태에서 결정한다."""
    pop = bool(state) and ready
    push = valid and len(state) < capacity
    consumed = state[0] if pop else None
    next_state = state[1:] if pop else state
    if push:
        next_state = ((data,) + next_state) if mutant else next_state + (data,)
    return next_state, push, pop, consumed


def explore_queue(capacity=2):
    seen, work = {()}, deque([()])
    transitions = 0
    while work:
        state = work.popleft()
        for valid in (False, True):
            for data in (0, 1):
                for ready in (False, True):
                    nxt, push, pop, _ = queue_transition(state, valid, data, ready, capacity)
                    assert len(nxt) == len(state) + int(push) - int(pop)
                    assert 0 <= len(nxt) <= capacity
                    transitions += 1
                    if nxt not in seen:
                        seen.add(nxt)
                        work.append(nxt)
    return seen, transitions


def multicycle_slacks(period, setup_cycles, hold_adjust, cq_max, d_max, setup,
                      cq_min, d_min, hold, skew=0.0, uncertainty=0.0):
    if period <= 0 or setup_cycles < 1 or not 0 <= hold_adjust <= setup_cycles - 1:
        raise ValueError("같은 주파수·위상 클록의 유효한 주기 수가 필요합니다")
    setup_edge = setup_cycles * period
    hold_edge = (setup_cycles - 1 - hold_adjust) * period
    return (setup_edge + skew - cq_max - d_max - setup - uncertainty,
            cq_min + d_min - hold_edge - skew - hold - uncertainty)


def cache_index(address, line_bytes, sets):
    for value in (line_bytes, sets):
        if value <= 0 or value & (value - 1):
            raise ValueError("크기는 양의 2의 거듭제곱이어야 합니다")
    return address // line_bytes % sets


def vipt_safe(page_bytes, line_bytes, sets):
    cache_index(0, line_bytes, sets)
    if page_bytes <= 0 or page_bytes & (page_bytes - 1):
        raise ValueError("페이지 크기는 2의 거듭제곱이어야 합니다")
    return line_bytes * sets <= page_bytes


def line_input_impedance(z_line, z_load, electrical_length):
    if z_line <= 0:
        raise ValueError("양의 실수 특성임피던스가 필요합니다")
    c, s = math.cos(electrical_length), math.sin(electrical_length)
    denominator = z_line * c + 1j * z_load * s
    if abs(denominator) < 1e-18:
        raise ValueError("개방회로에 해당하는 특이점입니다")
    return z_line * (z_load * c + 1j * z_line * s) / denominator


def qpsk_theory(ebn0_db):
    gamma = 10 ** (ebn0_db / 10)
    bit_error = 0.5 * math.erfc(math.sqrt(gamma))
    return bit_error, 2 * bit_error - bit_error**2


def qpsk_simulate(ebn0_db, symbols=20000, samples=4, seed=17):
    if symbols <= 0 or samples <= 0:
        raise ValueError("양의 심벌 수와 표본 수가 필요합니다")
    rng = random.Random(seed)
    gamma = 10 ** (ebn0_db / 10)
    sigma = math.sqrt(1 / (2 * gamma))
    pulse = 1 / math.sqrt(samples)
    bit_errors = symbol_errors = 0
    for _ in range(symbols):
        wrong = 0
        for _axis in range(2):
            bit = rng.randrange(2)
            amplitude = 1 if bit == 0 else -1
            statistic = sum((amplitude * pulse + rng.gauss(0, sigma)) * pulse
                            for _sample in range(samples))
            wrong += (statistic < 0) != bool(bit)
        bit_errors += wrong
        symbol_errors += wrong > 0
    return bit_errors / (2 * symbols), symbol_errors / symbols


def rk4_step(derivative, state, dt):
    if dt <= 0:
        raise ValueError("시간 간격은 양수여야 합니다")
    k1 = derivative(state)
    k2 = derivative(tuple(x + dt * k / 2 for x, k in zip(state, k1)))
    k3 = derivative(tuple(x + dt * k / 2 for x, k in zip(state, k2)))
    k4 = derivative(tuple(x + dt * k for x, k in zip(state, k3)))
    return tuple(x + dt * (a + 2*b + 2*c + d) / 6
                 for x, a, b, c, d in zip(state, k1, k2, k3, k4))


def buck_load_step(time, dt, vin=12.0, duty=0.5, inductance=100e-6,
                   capacitance=100e-6, old_r=12.0, new_r=6.0):
    if min(vin, inductance, capacitance, old_r, new_r) <= 0 or not 0 < duty < 1 or time < 0:
        raise ValueError("양의 소자값과 0<D<1 조건이 필요합니다")
    equilibrium = duty * vin
    state = (equilibrium / old_r, equilibrium)
    def derivative(x):
        i, v = x
        return ((equilibrium - v) / inductance, (i - v / new_r) / capacitance)
    elapsed = 0.0
    while elapsed < time:
        step = min(dt, time - elapsed)
        state = rk4_step(derivative, state, step)
        elapsed += step
    return state


def buck_underdamped_voltage(time, vin=12.0, duty=0.5, inductance=100e-6,
                             capacitance=100e-6, old_r=12.0, new_r=6.0):
    alpha = 1 / (2 * new_r * capacitance)
    discriminant = 1 / (inductance * capacitance) - alpha**2
    if discriminant <= 0:
        raise ValueError("저감쇠 조건에서만 쓰는 해입니다")
    wd = math.sqrt(discriminant)
    veq = duty * vin
    initial_slope = (veq / old_r - veq / new_r) / capacitance
    return veq + initial_slope * math.exp(-alpha * time) * math.sin(wd * time) / wd


def adc_linearity(transitions):
    m = len(transitions) + 1
    if m < 4 or m & (m - 1):
        raise ValueError("2비트 이상의 ADC 전이값 목록이 필요합니다")
    if any(b < a for a, b in zip(transitions, transitions[1:])):
        raise ValueError("전이 전압은 감소할 수 없습니다")
    lsb = (transitions[-1] - transitions[0]) / (m - 2)
    if lsb <= 0:
        raise ValueError("양의 전체 범위가 필요합니다")
    dnl = [(b - a) / lsb - 1 for a, b in zip(transitions, transitions[1:])]
    inl = [(t - (transitions[0] + k * lsb)) / lsb for k, t in enumerate(transitions)]
    return lsb, dnl, inl


def sram_read_node(time, vdd=1.0, access_r=20000.0, pull_down_r=10000.0, capacitance=1e-15):
    if time < 0 or min(vdd, access_r, pull_down_r, capacitance) <= 0:
        raise ValueError("비음수 시간과 양의 소자값이 필요합니다")
    equilibrium = vdd * pull_down_r / (access_r + pull_down_r)
    tau = access_r * pull_down_r / (access_r + pull_down_r) * capacitance
    return equilibrium * -math.expm1(-time / tau)


def credit_simulate(cycles=100, capacity=8, forward_delay=3, return_delay=3, seed=3, stalls=False):
    if min(cycles, capacity, forward_delay, return_delay) <= 0:
        raise ValueError("주기·용량·전달 지연은 양수여야 합니다")
    rng = random.Random(seed)
    credits = capacity
    data, returns, queue = deque(), deque(), deque()
    sent, consumed, max_queue = [], [], 0
    for tick in range(cycles):
        while returns and returns[0] <= tick:
            returns.popleft()
            credits += 1
        while data and data[0][0] <= tick:
            _, token = data.popleft()
            queue.append(token)
        max_queue = max(max_queue, len(queue))
        if queue and (not stalls or rng.random() > 0.35):
            consumed.append(queue.popleft())
            returns.append(tick + return_delay)
        if credits and (not stalls or rng.random() > 0.15):
            token = len(sent)
            sent.append(token)
            data.append((tick + forward_delay, token))
            credits -= 1
        assert credits + len(data) + len(queue) + len(returns) == capacity
        assert len(queue) <= capacity
    return {"sent": sent, "consumed": consumed, "credits": credits,
            "data_inflight": len(data), "queued": len(queue),
            "returns_inflight": len(returns), "max_queue": max_queue}


def counter_behavioral(q, enable, reset, width=8):
    return 0 if reset else (q + bool(enable)) & ((1 << width) - 1)


def counter_structural(q, enable, reset, width=8):
    if reset:
        return 0
    result, carry = 0, bool(enable)
    for bit in range(width):
        old = (q >> bit) & 1
        result |= (old ^ carry) << bit
        carry = bool(old and carry)
    return result


def thermal_two_node(time, dt, power=2.0, rjc=2.0, rca=8.0, cj=0.1, cc=1.0):
    if time < 0 or min(rjc, rca, cj, cc, dt) <= 0 or power < 0:
        raise ValueError("유효한 열망 매개변수가 필요합니다")
    def derivative(x):
        j, c, _ = x
        return ((power - (j - c) / rjc) / cj,
                ((j - c) / rjc - c / rca) / cc, c / rca)
    state, elapsed = (0.0, 0.0, 0.0), 0.0
    while elapsed < time:
        step = min(dt, time - elapsed)
        state = rk4_step(derivative, state, step)
        elapsed += step
    return state


@dataclass(frozen=True)
class LineFit:
    slope: float
    intercept: float
    residual_variance: float
    slope_variance: float
    intercept_variance: float
    covariance: float


def fit_line(xs, ys):
    if len(xs) != len(ys) or len(xs) < 3:
        raise ValueError("세 쌍 이상의 자료가 필요합니다")
    n = len(xs)
    xb, yb = sum(xs) / n, sum(ys) / n
    sxx = sum((x - xb)**2 for x in xs)
    if sxx == 0:
        raise ValueError("서로 다른 기준값이 필요합니다")
    slope = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sxx
    intercept = yb - slope * xb
    variance = sum((y - slope*x - intercept)**2 for x, y in zip(xs, ys)) / (n - 2)
    return LineFit(slope, intercept, variance, variance / sxx,
                   variance * (1/n + xb*xb/sxx), -xb * variance / sxx)


def inverse_calibrate(reading, fit, reading_uncertainty=0.0):
    if fit.slope == 0 or reading_uncertainty < 0:
        raise ValueError("0이 아닌 기울기와 비음수 불확도가 필요합니다")
    x = (reading - fit.intercept) / fit.slope
    variance = (reading_uncertainty**2 + fit.intercept_variance +
                x*x*fit.slope_variance + 2*x*fit.covariance) / fit.slope**2
    return x, math.sqrt(max(0.0, variance))


def signature(bits, width=3, polynomial=0b1011):
    if width < 1 or polynomial.bit_length() != width + 1 or polynomial % 2 == 0:
        raise ValueError("상수항과 최고차항이 1인 생성다항식이 필요합니다")
    state, mask = 0, (1 << width) - 1
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("입력은 비트열이어야 합니다")
        feedback = ((state >> (width - 1)) & 1) ^ bit
        state = (state << 1) & mask
        if feedback:
            state ^= polynomial & mask
    return state


def gf2_remainder(value, polynomial):
    if value < 0 or polynomial < 2:
        raise ValueError("비음수 피제수와 1차 이상의 다항식이 필요합니다")
    degree = polynomial.bit_length() - 1
    while value and value.bit_length() - 1 >= degree:
        value ^= polynomial << (value.bit_length() - 1 - degree)
    return value


def pim_affine_calibration(weights, voltage, gains, offsets, fits=None):
    if not weights or len(gains) != len(weights) or len(offsets) != len(weights):
        raise ValueError("출력 열 수가 일치해야 합니다")
    if any(len(row) != len(voltage) for row in weights):
        raise ValueError("행렬과 입력 차원이 일치해야 합니다")
    ideal = [sum(w*v for w, v in zip(row, voltage)) for row in weights]
    measured = [g*y + o for y, g, o in zip(ideal, gains, offsets)]
    if fits is None:
        return ideal, measured
    if len(fits) != len(weights):
        raise ValueError("출력마다 교정식이 필요합니다")
    corrected = [inverse_calibrate(y, fit)[0] for y, fit in zip(measured, fits)]
    return ideal, measured, corrected

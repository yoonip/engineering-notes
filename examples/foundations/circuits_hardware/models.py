import math


def _positive(**values):
    for name, value in values.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")


def rc_step(t, resistance, capacitance, vin=1.0, initial=0.0):
    _positive(resistance=resistance, capacitance=capacitance)
    if not math.isfinite(t) or t < 0:
        raise ValueError("t must be finite and nonnegative")
    return initial + (vin - initial) * -math.expm1(-t / (resistance * capacitance))


def rc_euler(steps, dt, resistance, capacitance, vin=1.0, initial=0.0):
    _positive(dt=dt, resistance=resistance, capacitance=capacitance)
    if not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    value = initial
    # 전체 이력 대신 현재 상태만 저장해 추가 메모리를 일정하게 유지한다.
    for _ in range(steps):
        value += dt * (vin - value) / (resistance * capacitance)
    return value


def rlc_free(t, resistance, inductance, capacitance, initial=1.0, slope=0.0):
    _positive(inductance=inductance, capacitance=capacitance)
    if resistance < 0 or not math.isfinite(resistance) or t < 0 or not math.isfinite(t):
        raise ValueError("R and t must be finite and nonnegative")
    alpha = resistance / (2 * inductance)
    omega0 = 1 / math.sqrt(inductance * capacitance)
    discriminant = alpha * alpha - omega0 * omega0
    if math.isclose(alpha, omega0, rel_tol=1e-12):
        return math.exp(-alpha * t) * (initial + (slope + alpha * initial) * t)
    if discriminant < 0:
        omega_d = math.sqrt(-discriminant)
        return math.exp(-alpha * t) * (
            initial * math.cos(omega_d * t)
            + (slope + alpha * initial) * math.sin(omega_d * t) / omega_d
        )
    # 작은 극을 뺄셈으로 구할 때의 유효숫자 손실을 줄인다.
    root = math.sqrt(discriminant)
    s2 = -alpha - root
    s1 = omega0 * omega0 / s2
    a = (slope - s2 * initial) / (s1 - s2)
    b = (s1 * initial - slope) / (s1 - s2)
    return a * math.exp(s1 * t) + b * math.exp(s2 * t)


def rlc_rk4(steps, dt, resistance, inductance, capacitance, vin=0.0,
            initial=1.0, current=0.0):
    _positive(dt=dt, inductance=inductance, capacitance=capacitance)
    if resistance < 0 or not math.isfinite(resistance):
        raise ValueError("R must be finite and nonnegative")
    if not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    def derivative(v, i):
        return i / capacitance, (vin - resistance * i - v) / inductance
    v, i = initial, current
    for _ in range(steps):
        a, b = derivative(v, i)
        c, d = derivative(v + dt * a / 2, i + dt * b / 2)
        e, f = derivative(v + dt * c / 2, i + dt * d / 2)
        g, h = derivative(v + dt * e, i + dt * f)
        v += dt * (a + 2 * c + 2 * e + g) / 6
        i += dt * (b + 2 * d + 2 * f + h) / 6
    return v, i


def nmos_current(vgs, vds, threshold, beta):
    _positive(beta=beta)
    if not all(math.isfinite(v) for v in (vgs, vds, threshold)) or vds < 0:
        raise ValueError("finite voltages and Vds >= 0 required")
    overdrive = vgs - threshold
    if overdrive <= 0:
        return 0.0
    if vds < overdrive:
        return beta * (overdrive * vds - vds * vds / 2)
    return beta * overdrive * overdrive / 2


class SyncFifo:
    def __init__(self, depth):
        if not isinstance(depth, int) or depth <= 0:
            raise ValueError("depth must be a positive integer")
        self.depth = depth
        self.memory = [None] * depth
        self.reset()

    def reset(self):
        self.read_pointer = self.write_pointer = self.count = 0

    def cycle(self, write, read, data=None):
        # 수락 여부는 모두 클록 직전의 점유량으로 판정한다.
        accepted_read = bool(read and self.count > 0)
        accepted_write = bool(write and self.count < self.depth)
        result = None
        if accepted_read:
            result = self.memory[self.read_pointer]
            self.read_pointer = (self.read_pointer + 1) % self.depth
        if accepted_write:
            self.memory[self.write_pointer] = data
            self.write_pointer = (self.write_pointer + 1) % self.depth
        self.count += int(accepted_write) - int(accepted_read)
        return accepted_write, accepted_read, result


def direct_mapped_hits(addresses, line_bytes, lines):
    if not isinstance(line_bytes, int) or not isinstance(lines, int) or min(line_bytes, lines) <= 0:
        raise ValueError("cache dimensions must be positive integers")
    tags = [None] * lines
    for address in addresses:
        if not isinstance(address, int) or address < 0:
            raise ValueError("addresses must be nonnegative integers")
        block = address // line_bytes
        slot = block % lines
        tag = block // lines
        hit = tags[slot] == tag
        tags[slot] = tag
        yield hit


def amat(hit_time, miss_rate, additional_penalty):
    if (not all(math.isfinite(x) for x in (hit_time, miss_rate, additional_penalty))
            or not 0 <= miss_rate <= 1 or min(hit_time, additional_penalty) < 0):
        raise ValueError("invalid cache timing or miss rate")
    return hit_time + miss_rate * additional_penalty


def reflection(load, z0):
    _positive(z0=z0)
    if load == math.inf:
        return 1.0
    if not math.isfinite(load) or load < 0:
        raise ValueError("resistive load must be nonnegative or infinity")
    return (load - z0) / (load + z0)


def load_steps(vsource, rsource, rload, z0, delay, arrivals=8):
    _positive(z0=z0, delay=delay)
    if not math.isfinite(rsource) or rsource < 0:
        raise ValueError("source resistance must be finite and nonnegative")
    if not isinstance(arrivals, int) or arrivals < 0:
        raise ValueError("arrivals must be a nonnegative integer")
    gamma_l, gamma_s = reflection(rload, z0), reflection(rsource, z0)
    incoming, level = vsource * z0 / (rsource + z0), 0.0
    for index in range(arrivals):
        level += incoming * (1 + gamma_l)
        yield (2 * index + 1) * delay, level
        incoming *= gamma_l * gamma_s


def probe_transfer(frequency, source_resistance, probe_resistance, probe_capacitance):
    _positive(probe_resistance=probe_resistance)
    if (not all(math.isfinite(x) for x in (frequency, source_resistance, probe_capacitance))
            or min(frequency, source_resistance, probe_capacitance) < 0):
        raise ValueError("frequency, source R and probe C must be nonnegative")
    admittance = 1 / probe_resistance + 2j * math.pi * frequency * probe_capacitance
    return 1 / (1 + source_resistance * admittance)


def resistance_uncertainty(voltage, current, u_voltage, u_current, covariance=0.0):
    if (not all(math.isfinite(x) for x in (voltage, current, u_voltage, u_current, covariance))
            or current == 0 or min(u_voltage, u_current) < 0):
        raise ValueError("nonzero current and nonnegative uncertainties required")
    if abs(covariance) > u_voltage * u_current:
        raise ValueError("covariance violates Cauchy-Schwarz bound")
    a, b = 1 / current, -voltage / (current * current)
    variance = (a * u_voltage) ** 2 + (b * u_current) ** 2 + 2 * a * b * covariance
    # 완전 상관일 때의 미세한 음수 반올림만 제거한다.
    return math.sqrt(max(0.0, variance))

"""신호·제어·AI의 작은 참조 모델. 단위와 가정은 연결된 문서에 설명한다."""

import math


def _finite(*values):
    if not all(math.isfinite(v) for v in values):
        raise ValueError("유한한 수가 필요하다")


def sample_cosine(frequency, sampling_rate, count, phase=0.0):
    _finite(frequency, sampling_rate, phase)
    if sampling_rate <= 0 or not isinstance(count, int) or count < 0:
        raise ValueError("양의 표본율과 음이 아닌 정수 길이가 필요하다")
    return [math.cos(2 * math.pi * frequency * n / sampling_rate + phase)
            for n in range(count)]


def alias_frequency(frequency, sampling_rate):
    _finite(frequency, sampling_rate)
    if sampling_rate <= 0:
        raise ValueError("표본율은 양수여야 한다")
    # 실수 코사인의 주파수를 첫 Nyquist 구간으로 접는다.
    return abs((frequency + sampling_rate / 2) % sampling_rate - sampling_rate / 2)


def adc_midrise(value, bits, lower=0.0, upper=1.0):
    _finite(value, lower, upper)
    if not isinstance(bits, int) or not 1 <= bits <= 24 or upper <= lower:
        raise ValueError("1~24비트와 증가하는 입력 범위가 필요하다")
    levels = 1 << bits
    step = (upper - lower) / levels
    code = min(levels - 1, max(0, math.floor((value - lower) / step)))
    # 코드 구간의 중앙을 복원값으로 삼는 수학적 양자화 모델이다.
    reconstruction = lower + (code + 0.5) * step
    return code, reconstruction


def ideal_snr_db(bits):
    if not isinstance(bits, int) or bits <= 0:
        raise ValueError("양의 정수 비트 수가 필요하다")
    return 20 * bits * math.log10(2) + 10 * math.log10(1.5)


def first_order_zoh(tau, sample_period, dc_gain=1.0):
    _finite(tau, sample_period, dc_gain)
    if tau <= 0 or sample_period <= 0:
        raise ValueError("시정수와 주기는 양수여야 한다")
    a = math.exp(-sample_period / tau)
    b = -dc_gain * math.expm1(-sample_period / tau)
    return a, b


def feedback_response(a, b, gain, reference, steps, initial=0.0, limit=None):
    _finite(a, b, gain, reference, initial)
    if not isinstance(steps, int) or steps < 0:
        raise ValueError("음이 아닌 정수 길이가 필요하다")
    if limit is not None and (not math.isfinite(limit) or limit <= 0):
        raise ValueError("입력 한계는 양수여야 한다")
    state = initial
    trace = [state]
    for _ in range(steps):
        control = gain * (reference - state)
        if limit is not None:
            control = min(limit, max(-limit, control))
        state = a * state + b * control
        trace.append(state)
    return trace


def sigmoid(value):
    _finite(value)
    # 음수와 양수를 나눠 지수의 오버플로를 피한다.
    if value >= 0:
        return 1 / (1 + math.exp(-value))
    ex = math.exp(value)
    return ex / (1 + ex)


def logistic_loss_gradient(samples, labels, weight, bias):
    if len(samples) != len(labels) or not samples:
        raise ValueError("길이가 같은 비어 있지 않은 자료가 필요하다")
    _finite(weight, bias, *samples, *labels)
    if any(y < 0 or y > 1 for y in labels):
        raise ValueError("목표값은 0~1이어야 한다")
    losses, dw, db = [], [], []
    for x, y in zip(samples, labels):
        z = weight * x + bias
        _finite(z)
        losses.append(max(z, 0.0) - z * y + math.log1p(math.exp(-abs(z))))
        delta = sigmoid(z) - y
        dw.append(delta * x)
        db.append(delta)
    count = len(samples)
    return math.fsum(losses) / count, (math.fsum(dw) / count, math.fsum(db) / count)


def train_logistic(samples, labels, iterations=100, rate=0.1):
    _finite(rate)
    if rate <= 0 or not isinstance(iterations, int) or iterations < 0:
        raise ValueError("양의 학습률과 음이 아닌 정수 반복 수가 필요하다")
    w, b = 0.0, 0.0
    for _ in range(iterations):
        _, (dw, db) = logistic_loss_gradient(samples, labels, w, b)
        w, b = w - rate * dw, b - rate * db
    final, _ = logistic_loss_gradient(samples, labels, w, b)
    return w, b, final


def _matrix(values):
    if not values or not values[0] or any(len(row) != len(values[0]) for row in values):
        raise ValueError("비어 있지 않은 직사각 행렬이 필요하다")
    for row in values:
        _finite(*row)


def attention(queries, keys, values, allowed=None):
    _matrix(queries)
    _matrix(keys)
    _matrix(values)
    if len(keys) != len(values) or len(queries[0]) != len(keys[0]):
        raise ValueError("Q/K의 차원과 K/V의 행 수가 맞아야 한다")
    if allowed is not None and (len(allowed) != len(queries) or
                                any(len(row) != len(keys) for row in allowed)):
        raise ValueError("마스크 모양은 질의 수 × 키 수여야 한다")
    scale = math.sqrt(len(keys[0]))
    result = []
    for i, query in enumerate(queries):
        indices = [j for j in range(len(keys)) if allowed is None or allowed[i][j]]
        if not indices:
            raise ValueError("각 질의에는 하나 이상의 허용된 키가 필요하다")
        scores = [math.fsum(q * k for q, k in zip(query, keys[j])) / scale for j in indices]
        _finite(*scores)
        # 행별 최대값을 빼면 가중치는 같고 exp의 오버플로를 피할 수 있다.
        maximum = max(scores)
        exps = [math.exp(s - maximum) for s in scores]
        denominator = math.fsum(exps)
        weights = [e / denominator for e in exps]
        result.append([math.fsum(w * values[j][d] for w, j in zip(weights, indices))
                       for d in range(len(values[0]))])
    return result


def roofline(work_flop, traffic_byte, peak_flops, bandwidth_byte_s):
    _finite(work_flop, traffic_byte, peak_flops, bandwidth_byte_s)
    if min(work_flop, traffic_byte, peak_flops, bandwidth_byte_s) <= 0:
        raise ValueError("일량·전송량·성능·대역폭은 양수여야 한다")
    intensity = work_flop / traffic_byte
    compute_time = work_flop / peak_flops
    memory_time = traffic_byte / bandwidth_byte_s
    # 두 자원이 이상적으로 겹쳐 동작할 때의 하한 시간이다.
    lower_bound = max(compute_time, memory_time)
    return {"intensity_flop_byte": intensity,
            "ceiling_flop_s": min(peak_flops, bandwidth_byte_s * intensity),
            "time_lower_bound_s": lower_bound,
            "limiting_resource": "compute" if compute_time >= memory_time else "memory"}


def amdahl(parallel_fraction, workers):
    _finite(parallel_fraction)
    if not 0 <= parallel_fraction <= 1 or not isinstance(workers, int) or workers <= 0:
        raise ValueError("병렬 비율은 0~1, 처리기 수는 양의 정수여야 한다")
    return 1 / ((1 - parallel_fraction) + parallel_fraction / workers)

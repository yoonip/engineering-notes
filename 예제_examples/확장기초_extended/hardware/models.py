"""회로·디지털 설계의 가정을 드러낸 표준 라이브러리 참조 모델."""

from collections import deque
import math
import random


def positive(*values):
    if any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError("유한한 양수가 필요합니다")


def cs_gain(gm, rd, ro, rl, capacitance, frequency):
    positive(gm, rd, ro, rl, capacitance)
    if frequency < 0 or not math.isfinite(frequency):
        raise ValueError("주파수는 유한한 0 이상의 값이어야 합니다")
    conductance = 1 / rd + 1 / ro + 1 / rl
    return -gm / complex(conductance, 2 * math.pi * frequency * capacitance)


def capacitor_impedance(c, esr, esl, frequency):
    positive(c, frequency)
    if esr < 0 or esl < 0:
        raise ValueError("ESR과 ESL은 음수가 될 수 없습니다")
    omega = 2 * math.pi * frequency
    return complex(esr, omega * esl - 1 / (omega * c))


def pdn_impedance(source_r, source_l, capacitors, frequency):
    positive(source_r, frequency)
    if source_l < 0 or not capacitors:
        raise ValueError("전원 경로와 커패시터를 확인해야 합니다")
    source_z = complex(source_r, 2 * math.pi * frequency * source_l)
    admittance = 1 / source_z
    for c, esr, esl in capacitors:
        z = capacitor_impedance(c, esr, esl, frequency)
        if z == 0:
            return 0j
        admittance += 1 / z
    return 1 / admittance


def counter_next(n, inc, dec, depth):
    if depth < 1 or not 0 <= n <= depth:
        raise ValueError("점유량 범위를 벗어났습니다")
    # 같은 에지의 요청은 갱신 전 점유량으로 수락합니다.
    return n + int(bool(inc) and n < depth) - int(bool(dec) and n > 0)


def reachable_counter(depth):
    positive(depth)
    pending, visited = deque([0]), {0}
    while pending:
        n = pending.popleft()
        for inc in (False, True):
            for dec in (False, True):
                nxt = counter_next(n, inc, dec, depth)
                if nxt not in visited:
                    visited.add(nxt)
                    pending.append(nxt)
    return visited


def timing_slack(period, launch_clock, capture_clock, cq_max, data_max,
                 setup, cq_min, data_min, hold, u_setup=0, u_hold=0):
    positive(period)
    if any(x < 0 for x in (cq_max, data_max, setup, cq_min, data_min,
                           hold, u_setup, u_hold)):
        raise ValueError("이 단순 모델의 지연과 불확도는 0 이상입니다")
    if cq_min > cq_max or data_min > data_max:
        raise ValueError("최소 지연이 최대 지연보다 큽니다")
    skew = capture_clock - launch_clock
    return (period + skew - cq_max - data_max - setup - u_setup,
            cq_min + data_min - skew - hold - u_hold)


class ByteMemory:
    def __init__(self, size):
        if not isinstance(size, int) or size < 1:
            raise ValueError("메모리 크기를 확인해야 합니다")
        self.data = bytearray(size)

    def _check(self, address, width, endian):
        if width not in (1, 2, 4, 8) or endian not in ("little", "big"):
            raise ValueError("폭 또는 byte 순서가 잘못되었습니다")
        if address < 0 or address + width > len(self.data):
            raise IndexError("메모리 범위를 벗어났습니다")
        if address % width:
            raise ValueError("이 모델은 자연 정렬만 허용합니다")

    def store(self, address, width, value, endian="little"):
        self._check(address, width, endian)
        value &= (1 << (8 * width)) - 1
        for offset in range(width):
            significance = offset if endian == "little" else width - 1 - offset
            self.data[address + offset] = (value >> (8 * significance)) & 255

    def load(self, address, width, endian="little", signed=False):
        self._check(address, width, endian)
        value = 0
        for offset in range(width):
            significance = offset if endian == "little" else width - 1 - offset
            value |= self.data[address + offset] << (8 * significance)
        if signed and value & (1 << (8 * width - 1)):
            value -= 1 << (8 * width)
        return value


def bpsk_ber(gamma):
    if gamma < 0 or not math.isfinite(gamma):
        raise ValueError("Eb/N0는 선형 비율로 입력합니다")
    return 0.5 * math.erfc(math.sqrt(gamma))


def bpsk_errors(gamma_db, bits, seed=2026):
    if bits < 1:
        raise ValueError("비트 수는 양수여야 합니다")
    gamma = 10 ** (gamma_db / 10)
    sigma = math.sqrt(1 / (2 * gamma))
    rng, errors = random.Random(seed), 0
    for _ in range(bits):
        symbol = 1 if rng.getrandbits(1) else -1
        received = symbol + rng.gauss(0, sigma)
        errors += ((received >= 0) != (symbol > 0))
    return errors


def buck_ccm(vin, vout, inductance, frequency, capacitance, current, esr=0):
    positive(vin, vout, inductance, frequency, capacitance, current)
    if vout >= vin or esr < 0:
        raise ValueError("이상적인 강압 CCM 조건을 확인해야 합니다")
    duty = vout / vin
    ripple = (vin - vout) * duty / (inductance * frequency)
    if current <= ripple / 2:
        raise ValueError("양의 CCM 조건을 만족하지 않습니다")
    return {"duty": duty, "ripple": ripple, "imin": current - ripple / 2,
            "imax": current + ripple / 2,
            "capacitive_ripple": ripple / (8 * frequency * capacitance),
            "esr_ripple": ripple * esr}


class ReadyValidBuffer:
    """조합 READY 경로가 없는 2-entry 동기 버퍼의 에지 모델."""

    def __init__(self):
        self._items = deque()

    def cycle(self, in_valid, in_data, out_ready, reset=False):
        ready = len(self._items) < 2
        valid = bool(self._items)
        data = self._items[0] if valid else None
        if reset:
            self._items.clear()
            return False, False, None, False, False
        accepted_in = bool(in_valid and ready)
        accepted_out = bool(out_ready and valid)
        if accepted_out:
            self._items.popleft()
        if accepted_in:
            self._items.append(in_data)
        return ready, valid, data, accepted_in, accepted_out


def full_adder_gates(a, b, carry):
    return (a ^ b ^ carry, (a & b) | (carry & (a ^ b)))


def dag_arrivals(delays, predecessors):
    """위상 순서로 나열한 고정 지연 DAG를 해석합니다."""
    # 각 노드의 지연을 입력의 가장 늦은 도착 시각에 더합니다.
    arrivals = {}
    for node, delay in delays.items():
        if delay < 0:
            raise ValueError("지연은 0 이상이어야 합니다")
        inputs = predecessors.get(node, ())
        if any(parent not in arrivals for parent in inputs):
            raise ValueError("위상 순서가 아닙니다")
        arrivals[node] = delay + max((arrivals[p] for p in inputs), default=0)
    return arrivals


def thermal_step(rth, cth, power, duration, initial_rise=0):
    positive(rth, cth)
    if duration < 0 or power < 0:
        raise ValueError("시간과 발열량은 0 이상이어야 합니다")
    alpha = math.exp(-duration / (rth * cth))
    return initial_rise * alpha + power * rth * (-math.expm1(-duration / (rth * cth)))


def thermal_pulse_steady(rth, cth, power, on_time, off_time):
    positive(rth, cth, on_time, off_time)
    if power < 0:
        raise ValueError("발열량은 0 이상이어야 합니다")
    tau = rth * cth
    peak = power * rth * (-math.expm1(-on_time / tau)) / (-math.expm1(-(on_time + off_time) / tau))
    return peak * math.exp(-off_time / tau), peak


def logic_output(a, b, c, fault=None):
    values = {"a": a, "b": b, "c": c}
    if fault and fault[0] in values:
        values[fault[0]] = fault[1]
    values["n"] = values["a"] & values["b"]
    if fault and fault[0] == "n":
        values["n"] = fault[1]
    values["y"] = values["n"] | values["c"]
    if fault and fault[0] == "y":
        values["y"] = fault[1]
    return values["y"]


FAULTS = tuple((site, stuck) for site in ("a", "b", "c", "n", "y") for stuck in (0, 1))


def detected_faults(patterns):
    return {fault for fault in FAULTS
            if any(logic_output(*pattern) != logic_output(*pattern, fault=fault) for pattern in patterns)}


def scan_shift(state, serial_in):
    if not state or serial_in not in (0, 1) or any(bit not in (0, 1) for bit in state):
        raise ValueError("비어 있지 않은 0/1 scan state가 필요합니다")
    return [serial_in, *state[:-1]], state[-1]


def crossbar_currents(conductances, voltages, row_resistance=0):
    if not conductances or len(conductances) != len(voltages):
        raise ValueError("행 개수를 확인해야 합니다")
    columns = len(conductances[0])
    if columns < 1 or row_resistance < 0:
        raise ValueError("열 개수와 행 저항을 확인해야 합니다")
    currents = [0.0] * columns
    for row, source in zip(conductances, voltages):
        if len(row) != columns or any(g < 0 for g in row):
            raise ValueError("직사각형의 비음수 conductance가 필요합니다")
        # 각 행 앞의 공통 직렬저항만 모델링하며 분포 배선저항은 제외합니다.
        voltage = source / (1 + row_resistance * sum(row))
        for column, g in enumerate(row):
            currents[column] += voltage * g
    return currents


def differential_conductances(weights, gmin, scale):
    positive(gmin, scale)
    plus = [[gmin + scale * max(w, 0) for w in row] for row in weights]
    minus = [[gmin + scale * max(-w, 0) for w in row] for row in weights]
    return plus, minus


def quantize_symmetric(value, bound, bits):
    positive(bound)
    if not isinstance(bits, int) or bits < 1:
        raise ValueError("비트 수를 확인해야 합니다")
    levels = (1 << bits) - 1
    clipped = max(-bound, min(bound, value))
    code = math.floor((clipped + bound) * levels / (2 * bound) + 0.5)
    return -bound + 2 * bound * code / levels

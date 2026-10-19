"""심화 문서의 계산·데이터베이스·상태 예제를 실행한다."""

from dataclasses import dataclass, field
import heapq
import math
from pathlib import Path
import sqlite3
import tempfile


def _finite(values):
    if any(not math.isfinite(value) for value in values):
        raise ValueError("유한한 수가 필요합니다")


def softmax(scores):
    if not scores:
        raise ValueError("빈 점수는 사용할 수 없습니다")
    _finite(scores)
    peak = max(scores)
    exponents = [math.exp(value - peak) for value in scores]
    total = math.fsum(exponents)
    return [value / total for value in exponents]


def mlp_loss_gradient(parameters, inputs, label, hidden=3):
    """입력 2개·tanh 은닉층·출력 2개의 표본 손실과 모든 미분을 구한다."""
    if hidden < 1 or len(inputs) != 2 or len(parameters) != 5 * hidden + 2 or label not in (0, 1):
        raise ValueError("모델의 크기 또는 레이블이 잘못되었습니다")
    _finite([*parameters, *inputs])
    h = hidden
    w1 = [parameters[2*j:2*j+2] for j in range(h)]
    b1 = parameters[2*h:3*h]
    w2 = [parameters[3*h:4*h], parameters[4*h:5*h]]
    b2 = parameters[5*h:5*h+2]
    activation = [math.tanh(math.fsum(w*x for w, x in zip(row, inputs)) + bias)
                  for row, bias in zip(w1, b1)]
    logits = [math.fsum(w*a for w, a in zip(row, activation)) + bias
              for row, bias in zip(w2, b2)]
    peak = max(logits)
    loss = peak + math.log(math.fsum(math.exp(z - peak) for z in logits)) - logits[label]
    probability = softmax(logits)
    dz = [probability[i] - (i == label) for i in range(2)]
    dh = [math.fsum(w2[i][j] * dz[i] for i in range(2)) * (1 - activation[j]**2)
          for j in range(h)]
    gradient = [dh[j] * inputs[k] for j in range(h) for k in range(2)]
    gradient += dh
    gradient += [dz[i] * activation[j] for i in range(2) for j in range(h)]
    gradient += dz
    return loss, gradient, probability


def mlp_batch(parameters, xs, labels, hidden=3):
    if not xs or len(xs) != len(labels):
        raise ValueError("입력과 레이블의 길이가 맞아야 합니다")
    results = [mlp_loss_gradient(parameters, x, y, hidden) for x, y in zip(xs, labels)]
    count = len(results)
    return (math.fsum(row[0] for row in results) / count,
            [math.fsum(row[1][j] for row in results) / count for j in range(len(parameters))])


def tiled_loads(m, n, k, tile):
    if any(type(value) is not int or value < 1 for value in (m, n, k, tile)):
        raise ValueError("행렬 크기와 타일은 양의 정수여야 합니다")
    a_reads = m*k*((n+tile-1)//tile)
    b_reads = k*n*((m+tile-1)//tile)
    return {"naive_input_elements": 2*m*n*k, "tiled_input_elements": a_reads+b_reads,
            "output_elements": m*n, "shared_bytes_fp32": 2*tile*tile*4}


def shared_bank_conflict(word_addresses, banks=32):
    """같은 주소의 broadcast는 하나로 세는 단일 명령의 은행 모형이다."""
    if banks < 1 or any(type(x) is not int or x < 0 for x in word_addresses):
        raise ValueError("주소와 은행 수가 잘못되었습니다")
    by_bank = [set() for _ in range(banks)]
    for address in word_addresses:
        by_bank[address % banks].add(address)
    return max(map(len, by_bank), default=0)


def matmul_tiled(a, b, tile=16):
    if not a or not b or not a[0] or not b[0] or type(tile) is not int or tile < 1:
        raise ValueError("비어 있지 않은 행렬과 양의 타일이 필요합니다")
    m, k, n = len(a), len(a[0]), len(b[0])
    if len(b) != k or any(len(row) != k for row in a) or any(len(row) != n for row in b):
        raise ValueError("행렬 크기가 맞지 않습니다")
    result = [[0.0] * n for _ in range(m)]
    for ii in range(0, m, tile):
        for kk in range(0, k, tile):
            for jj in range(0, n, tile):
                for i in range(ii, min(ii+tile, m)):
                    for p in range(kk, min(kk+tile, k)):
                        value = a[i][p]
                        for j in range(jj, min(jj+tile, n)):
                            result[i][j] += value * b[p][j]
    return result


def beam_search(transitions, width, steps, eos=None):
    """고정 최대 길이, 길이 보정 없는 로그 확률로 후보를 가지치기한다."""
    if type(width) is not int or width < 1 or type(steps) is not int or steps < 0:
        raise ValueError("탐색 크기가 잘못되었습니다")
    vocabulary = len(transitions[-1])
    if vocabulary < 1 or any(len(row) != vocabulary for row in transitions.values()):
        raise ValueError("어휘 크기가 맞지 않습니다")
    if eos is not None and not 0 <= eos < vocabulary:
        raise ValueError("종료 토큰이 범위를 벗어났습니다")
    for row in transitions.values():
        if any(p < 0 or not math.isfinite(p) for p in row) or not math.isclose(math.fsum(row), 1):
            raise ValueError("전이 확률의 합은 1이어야 합니다")
    beams = [((), 0.0)]
    for _ in range(steps):
        candidates = []
        for sequence, score in beams:
            if sequence and sequence[-1] == eos:
                candidates.append((sequence, score))
                continue
            row = transitions[sequence[-1] if sequence else -1]
            candidates.extend((sequence+(token,), score+math.log(p))
                              for token, p in enumerate(row) if p > 0)
        beams = heapq.nsmallest(width, candidates, key=lambda item: (-item[1], item[0]))
    return beams


def kv_bytes(batch, layers, kv_heads, tokens, head_dim, element_bytes=2):
    if any(type(x) is not int or x < 0 for x in (batch, layers, kv_heads, tokens, head_dim, element_bytes)):
        raise ValueError("크기는 음이 아닌 정수여야 합니다")
    return 2 * batch * layers * kv_heads * tokens * head_dim * element_bytes


def sqlite_wal_snapshot():
    """실제 SQLite 연결 두 개로 snapshot과 버전 조건 변경을 관찰한다."""
    with tempfile.TemporaryDirectory(prefix="advanced-wal-") as directory:
        path = str(Path(directory) / "snapshot.sqlite3")
        reader = sqlite3.connect(path, isolation_level=None, timeout=0.1)
        writer = sqlite3.connect(path, isolation_level=None, timeout=0.1)
        try:
            mode = reader.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            if mode.lower() != "wal":
                raise RuntimeError("이 예제는 WAL을 지원하는 로컬 파일시스템이 필요합니다")
            reader.execute("CREATE TABLE counter(id INTEGER PRIMARY KEY, value INTEGER, version INTEGER)")
            reader.execute("INSERT INTO counter VALUES(1, 0, 0)")
            reader.execute("BEGIN")
            first = reader.execute("SELECT value,version FROM counter WHERE id=1").fetchone()
            writer.execute("BEGIN IMMEDIATE")
            changed = writer.execute("UPDATE counter SET value=value+1, version=version+1 WHERE id=1 AND version=0").rowcount
            writer.execute("COMMIT")
            same_snapshot = reader.execute("SELECT value,version FROM counter WHERE id=1").fetchone()
            try:
                reader.execute("UPDATE counter SET value=value+1 WHERE id=1")
            except sqlite3.OperationalError as error:
                promotion_error = error.sqlite_errorcode
            else:
                raise AssertionError("오래된 읽기 snapshot이 쓰기로 승격되었습니다")
            finally:
                if reader.in_transaction:
                    reader.execute("ROLLBACK")
            current = reader.execute("SELECT value,version FROM counter WHERE id=1").fetchone()
            stale_write = writer.execute("UPDATE counter SET value=value+1, version=version+1 WHERE id=1 AND version=0").rowcount
            return {"journal_mode": mode, "first": first, "same_snapshot": same_snapshot,
                    "current": current, "changed_rows": changed,
                    "stale_changed_rows": stale_write, "promotion_error": promotion_error}
        finally:
            reader.close()
            writer.close()


@dataclass
class LamportClock:
    value: int = 0

    def local(self):
        self.value += 1
        return self.value

    def send(self):
        return self.local()

    def receive(self, message_time):
        if type(message_time) is not int or message_time < 0:
            raise ValueError("메시지 시각은 음이 아닌 정수여야 합니다")
        self.value = max(self.value, message_time) + 1
        return self.value


def exclusive_scan(values):
    """0을 항등원으로 하는 정수 합 scan의 트리 단계를 직렬 재현한다."""
    if any(type(value) is not int for value in values):
        raise ValueError("정수 합 scan입니다")
    n = len(values)
    if n == 0:
        return [], {"additions": 0, "levels": 0}
    size = 1 << (n-1).bit_length()
    tree = list(values) + [0] * (size-n)
    stride = 2
    while stride <= size:
        for right in range(stride-1, size, stride):
            tree[right] += tree[right-stride//2]
        stride *= 2
    tree[-1] = 0
    stride = size
    while stride >= 2:
        for right in range(stride-1, size, stride):
            left = right-stride//2
            tree[left], tree[right] = tree[right], tree[right]+tree[left]
        stride //= 2
    return tree[:n], {"additions": 2*(size-1), "levels": 2*(size.bit_length()-1)}


def _check_image(image):
    if not image or not image[0] or any(len(row) != len(image[0]) for row in image):
        raise ValueError("직사각형 영상이 필요합니다")


def bilinear(image, x, y, border=0.0):
    _check_image(image)
    _finite([x, y, border])
    return _bilinear_unchecked(image, x, y, border)


def _bilinear_unchecked(image, x, y, border):
    # 전체 영상을 변환할 때 직사각형 검사를 픽셀마다 반복하지 않는다.
    left, top = math.floor(x), math.floor(y)
    dx, dy = x-left, y-top
    def pixel(ix, iy):
        return image[iy][ix] if 0 <= iy < len(image) and 0 <= ix < len(image[0]) else border
    return math.fsum(pixel(left+i, top+j) * (dx if i else 1-dx) * (dy if j else 1-dy)
                     for j in range(2) for i in range(2))


def warp_affine(image, inverse_map, output_width, output_height, border=0.0):
    _check_image(image)
    if len(inverse_map) != 2 or any(len(row) != 3 for row in inverse_map):
        raise ValueError("목적지에서 원본으로 가는 2×3 행렬이 필요합니다")
    _finite([border, *(value for row in inverse_map for value in row)])
    if min(output_width, output_height) < 1:
        raise ValueError("출력 크기는 양수여야 합니다")
    return [[_bilinear_unchecked(image, inverse_map[0][0]*x+inverse_map[0][1]*y+inverse_map[0][2],
                      inverse_map[1][0]*x+inverse_map[1][1]*y+inverse_map[1][2], border)
             for x in range(output_width)] for y in range(output_height)]


def attention_forward_backward(query, keys, values, upstream, allowed=None):
    """단일 query의 출력과 입력 Q·K·V에 대한 벡터 미분을 구한다."""
    if not query or not keys or len(keys) != len(values) or not values[0]:
        raise ValueError("비어 있지 않은 Q·K·V가 필요합니다")
    d, dv, n = len(query), len(values[0]), len(keys)
    if any(len(row) != d for row in keys) or any(len(row) != dv for row in values) or len(upstream) != dv:
        raise ValueError("attention 차원이 맞지 않습니다")
    mask = [True]*n if allowed is None else list(allowed)
    if len(mask) != n or not any(mask) or any(type(x) is not bool for x in mask):
        raise ValueError("적어도 한 key를 허용하는 Boolean mask가 필요합니다")
    _finite([*query, *upstream, *(x for row in keys for x in row), *(x for row in values for x in row)])
    scale = 1 / math.sqrt(d)
    scores = [math.fsum(q*k for q, k in zip(query, row))*scale for row in keys]
    active = [j for j in range(n) if mask[j]]
    active_p = softmax([scores[j] for j in active])
    probability = [0.0]*n
    for j, p in zip(active, active_p):
        probability[j] = p
    output = [math.fsum(probability[j]*values[j][i] for j in range(n)) for i in range(dv)]
    dp = [math.fsum(g*v for g, v in zip(upstream, row)) for row in values]
    average = math.fsum(p*value for p, value in zip(probability, dp))
    ds = [p*(value-average) for p, value in zip(probability, dp)]
    dq = [scale*math.fsum(ds[j]*keys[j][i] for j in range(n)) for i in range(d)]
    dk = [[scale*ds[j]*q for q in query] for j in range(n)]
    dvalues = [[p*g for g in upstream] for p in probability]
    return output, (dq, dk, dvalues), probability


@dataclass
class KVCache:
    keys: list = field(default_factory=list)
    values: list = field(default_factory=list)

    def append_and_attend(self, query, key, value):
        if len(query) != len(key) or not query or not value:
            raise ValueError("query와 key 차원이 같아야 합니다")
        if self.keys and (len(key) != len(self.keys[0]) or len(value) != len(self.values[0])):
            raise ValueError("cache 차원이 바뀔 수 없습니다")
        _finite([*query, *key, *value])
        self.keys.append(tuple(key))
        self.values.append(tuple(value))
        return attention_forward_backward(query, self.keys, self.values, [0.0]*len(value))[0]


@dataclass
class Adam:
    parameters: list
    rate: float = 0.01
    beta1: float = 0.9
    beta2: float = 0.999
    epsilon: float = 1e-8
    step_count: int = 0
    first: list = field(default_factory=list)
    second: list = field(default_factory=list)

    def __post_init__(self):
        self.parameters = list(self.parameters)
        _finite([*self.parameters, self.rate, self.beta1, self.beta2, self.epsilon])
        if not self.parameters or self.rate <= 0 or self.epsilon <= 0 or not 0 <= self.beta1 < 1 or not 0 <= self.beta2 < 1 or self.step_count < 0:
            raise ValueError("Adam 설정이 잘못되었습니다")
        if not self.first:
            self.first = [0.0]*len(self.parameters)
        if not self.second:
            self.second = [0.0]*len(self.parameters)
        if len(self.first) != len(self.parameters) or len(self.second) != len(self.parameters):
            raise ValueError("Adam 상태 크기가 맞지 않습니다")
        _finite([*self.first, *self.second])
        if any(v < 0 for v in self.second):
            raise ValueError("두 번째 모멘트는 음수가 될 수 없습니다")

    def update(self, gradient):
        if len(gradient) != len(self.parameters):
            raise ValueError("gradient 크기가 맞지 않습니다")
        _finite(gradient)
        self.step_count += 1
        t = self.step_count
        for i, g in enumerate(gradient):
            self.first[i] = self.beta1*self.first[i] + (1-self.beta1)*g
            self.second[i] = self.beta2*self.second[i] + (1-self.beta2)*g*g
            corrected_first = self.first[i]/(1-self.beta1**t)
            corrected_second = self.second[i]/(1-self.beta2**t)
            self.parameters[i] -= self.rate*corrected_first/(math.sqrt(corrected_second)+self.epsilon)
        return self.parameters[:]


def clip_gradient(gradient, maximum_norm):
    if maximum_norm <= 0 or not math.isfinite(maximum_norm):
        raise ValueError("노름 상한은 유한한 양수여야 합니다")
    _finite(gradient)
    norm = math.hypot(*gradient)
    factor = min(1.0, maximum_norm/norm) if norm else 1.0
    return [factor*g for g in gradient], norm


def classification_metrics(truth, predicted, classes):
    if not truth or len(truth) != len(predicted) or not classes or len(set(classes)) != len(classes):
        raise ValueError("평가 입력 크기가 잘못되었습니다")
    if not set(truth+predicted) <= set(classes):
        raise ValueError("정의되지 않은 class입니다")
    counts = {label: [0, 0, 0] for label in classes}
    # 표본은 한 번만 읽고 클래스별 TP·FP·FN을 누적한다.
    for actual, guess in zip(truth, predicted):
        if actual == guess:
            counts[actual][0] += 1
        else:
            counts[guess][1] += 1
            counts[actual][2] += 1
    rows = []
    for label in classes:
        tp, fp, fn = counts[label]
        f1 = 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0
        rows.append({"class": label, "tp": tp, "fp": fp, "fn": fn, "f1": f1})
    total_tp = sum(row["tp"] for row in rows)
    denominator = sum(2*row["tp"]+row["fp"]+row["fn"] for row in rows)
    return {"per_class": rows, "macro_f1": math.fsum(row["f1"] for row in rows)/len(rows),
            "micro_f1": 2*total_tp/denominator if denominator else 0.0,
            "accuracy": total_tp/len(truth)}


def wilson_interval(successes, count, z=1.959963984540054):
    if type(successes) is not int or type(count) is not int or count < 1 or not 0 <= successes <= count or z <= 0 or not math.isfinite(z):
        raise ValueError("성공 횟수와 표본 수가 잘못되었습니다")
    p = successes/count
    denominator = 1 + z*z/count
    center = (p + z*z/(2*count))/denominator
    half = z*math.sqrt(p*(1-p)/count + z*z/(4*count*count))/denominator
    return max(0.0, center-half), min(1.0, center+half)


def per_channel_linear(inputs, weights):
    if not inputs or not weights or any(len(row) != len(inputs) for row in weights):
        raise ValueError("입력과 weight 차원이 맞지 않습니다")
    _finite([*inputs, *(x for row in weights for x in row)])
    input_scale = max(map(abs, inputs))/127 or 1.0
    quantized_input = [max(-127, min(127, round(x/input_scale))) for x in inputs]
    scales, accumulators, outputs = [], [], []
    for row in weights:
        scale = max(map(abs, row))/127 or 1.0
        qw = [max(-127, min(127, round(w/scale))) for w in row]
        accumulator = sum(x*w for x, w in zip(quantized_input, qw))
        scales.append(scale)
        accumulators.append(accumulator)
        outputs.append(input_scale*scale*accumulator)
    return outputs, {"input_scale": input_scale, "weight_scales": scales, "accumulators": accumulators}


def perspective_interpolate(screen_weights, attributes, clip_w):
    if len(screen_weights) != 3 or len(attributes) != 3 or len(clip_w) != 3:
        raise ValueError("삼각형 꼭짓점 세 개가 필요합니다")
    _finite([*screen_weights, *attributes, *clip_w])
    if any(w <= 0 for w in clip_w) or any(a < 0 for a in screen_weights) or not math.isclose(math.fsum(screen_weights), 1):
        raise ValueError("양의 clip w와 내부 점의 무게가 필요합니다")
    corrected = [a/w for a, w in zip(screen_weights, clip_w)]
    denominator = math.fsum(corrected)
    return math.fsum(a*f for a, f in zip(corrected, attributes))/denominator

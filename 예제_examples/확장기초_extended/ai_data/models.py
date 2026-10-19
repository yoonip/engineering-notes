"""GPU·데이터·모델·수치해석의 작은 계산 모델."""

from bisect import bisect_right
from collections import Counter
import heapq
import json
import math
import re
import sqlite3


def memory_sectors(addresses, word_bytes=4, sector_bytes=32):
    """한 번의 워프 메모리 명령이 건드리는 구간 수를 센다."""
    if word_bytes <= 0 or sector_bytes <= 0:
        raise ValueError("구간 크기는 양수여야 합니다")
    sectors = set()
    for address in addresses:
        if not isinstance(address, int) or address < 0:
            raise ValueError("주소는 음이 아닌 정수여야 합니다")
        sectors.update(range(address // sector_bytes,
                             (address + word_bytes - 1) // sector_bytes + 1))
    return len(sectors)


def occupancy_bound(block_threads, registers_per_thread, shared_per_block,
                    max_threads=2048, registers=65536, shared=65536,
                    max_blocks=16, max_warps=64):
    """할당 단위·분할 제약을 생략한 자원 기반 상한이다."""
    if min(block_threads, max_threads, registers, shared, max_blocks, max_warps) <= 0:
        raise ValueError("용량과 블록 크기는 양수여야 합니다")
    if registers_per_thread < 0 or shared_per_block < 0:
        raise ValueError("사용량은 음수가 될 수 없습니다")
    warps = (block_threads + 31) // 32
    limits = [max_blocks, max_threads // block_threads, max_warps // warps]
    if registers_per_thread:
        limits.append(registers // (registers_per_thread * block_threads))
    if shared_per_block:
        limits.append(shared // shared_per_block)
    blocks = min(limits)
    return blocks, blocks * warps / max_warps


def token_probabilities(logits, temperature=1.0, top_k=None):
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("유한한 로짓과 양의 온도가 필요합니다")
    if any(not math.isfinite(x) for x in logits):
        raise ValueError("로짓은 유한해야 합니다")
    if top_k is not None and (type(top_k) is not int or not 1 <= top_k <= len(logits)):
        raise ValueError("top_k 범위가 잘못되었습니다")
    keep = (set(range(len(logits))) if top_k is None else
            set(heapq.nlargest(top_k, range(len(logits)), key=lambda i: (logits[i], -i))))
    peak = max(logits[i] for i in keep)
    values = [math.exp((x - peak) / temperature) if i in keep else 0.0
              for i, x in enumerate(logits)]
    total = math.fsum(values)
    return [x / total for x in values]


def sample_token(probabilities, uniform):
    if not 0 <= uniform < 1 or not probabilities:
        raise ValueError("난수는 [0,1) 범위여야 합니다")
    if any(not math.isfinite(p) or p < 0 for p in probabilities):
        raise ValueError("확률은 유한하고 음이 아니어야 합니다")
    if not math.isclose(math.fsum(probabilities), 1.0, abs_tol=1e-12):
        raise ValueError("확률 합은 1이어야 합니다")
    cumulative = 0.0
    last_positive = 0
    for i, probability in enumerate(probabilities):
        if probability > 0:
            last_positive = i
        cumulative += probability
        if uniform < cumulative:
            return i
    return last_positive


def sales_totals(rows):
    """금액을 정수 최소 화폐 단위로 저장하고 SQL로 묶는다."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute("CREATE TABLE sales (region TEXT NOT NULL, amount INTEGER NOT NULL)")
        connection.executemany("INSERT INTO sales VALUES (?, ?)", rows)
        connection.execute("CREATE INDEX sales_region ON sales(region)")
        return dict(connection.execute(
            "SELECT region, SUM(amount) FROM sales GROUP BY region ORDER BY region"))


def transfer(connection, source, destination, amount):
    """자체 트랜잭션을 소유하며 잔액 부족·수신 계좌 누락 시 롤백한다."""
    if type(amount) is not int or amount <= 0 or source == destination:
        raise ValueError("서로 다른 계좌와 양의 정수 금액이 필요합니다")
    if connection.in_transaction:
        raise ValueError("열린 트랜잭션이 없어야 합니다")
    # 연결의 자동 트랜잭션 설정에 의존하지 않고 이 함수의 범위를 직접 연다.
    connection.execute("BEGIN")
    try:
        debit = connection.execute(
            "UPDATE accounts SET balance=balance-? WHERE id=? AND balance>=?",
            (amount, source, amount))
        if debit.rowcount != 1:
            raise ValueError("계좌가 없거나 잔액이 부족합니다")
        credit = connection.execute(
            "UPDATE accounts SET balance=balance+? WHERE id=?", (amount, destination))
        if credit.rowcount != 1:
            raise ValueError("수신 계좌가 없습니다")
        connection.execute("COMMIT")
    except BaseException:
        if connection.in_transaction:
            connection.execute("ROLLBACK")
        raise


def quorum_overlap(n, read_size, write_size):
    if any(type(v) is not int for v in (n, read_size, write_size)):
        raise ValueError("복제 수는 정수여야 합니다")
    if n < 1 or not 1 <= read_size <= n or not 1 <= write_size <= n:
        raise ValueError("쿼럼 범위가 잘못되었습니다")
    return max(0, read_size + write_size - n)


def balanced_partitions(size, workers):
    if type(size) is not int or type(workers) is not int or size < 0 or workers < 1:
        raise ValueError("크기는 음이 아닌 정수, 작업자 수는 양의 정수여야 합니다")
    quotient, remainder = divmod(size, workers)
    ranges, start = [], 0
    for worker in range(workers):
        stop = start + quotient + (worker < remainder)
        ranges.append((start, stop))
        start = stop
    return ranges


def pairwise_sum(values):
    """트리 합산 순서를 직렬로 재현한다."""
    layer = list(values)
    if not layer:
        return 0
    while len(layer) > 1:
        layer = [layer[i] + layer[i + 1] if i + 1 < len(layer) else layer[i]
                 for i in range(0, len(layer), 2)]
    return layer[0]


def tree_reduction_time(workers, payload_bytes, latency, seconds_per_byte):
    if workers < 1 or workers & (workers - 1):
        raise ValueError("이 모델은 2의 거듭제곱 작업자 수를 사용합니다")
    if min(payload_bytes, latency, seconds_per_byte) < 0:
        raise ValueError("비용은 음수가 될 수 없습니다")
    return (workers.bit_length() - 1) * (latency + payload_bytes * seconds_per_byte)


def pinhole(point, fx, fy, cx=0.0, cy=0.0):
    if len(point) != 3 or not all(math.isfinite(x) for x in (*point, fx, fy, cx, cy)):
        raise ValueError("유한한 3차원 점과 내부 파라미터가 필요합니다")
    x, y, z = point
    if z <= 0 or fx <= 0 or fy <= 0:
        raise ValueError("이 모델은 카메라 앞의 점과 양의 초점거리를 사용합니다")
    return fx * x / z + cx, fy * y / z + cy


def correlate_valid(image, kernel):
    if not image or not kernel or not image[0] or not kernel[0]:
        raise ValueError("빈 영상이나 커널은 사용할 수 없습니다")
    height, width = len(image), len(image[0])
    kh, kw = len(kernel), len(kernel[0])
    if any(len(row) != width for row in image) or any(len(row) != kw for row in kernel):
        raise ValueError("행 길이가 같아야 합니다")
    if kh > height or kw > width:
        raise ValueError("커널이 영상보다 큽니다")
    return [[math.fsum(image[y + j][x + i] * kernel[j][i]
                       for j in range(kh) for i in range(kw))
             for x in range(width - kw + 1)] for y in range(height - kh + 1)]


def linear_loss_gradient(xs, ys, weight):
    if not xs or len(xs) != len(ys):
        raise ValueError("같은 길이의 비어 있지 않은 데이터가 필요합니다")
    errors = [weight * x - y for x, y in zip(xs, ys)]
    return (math.fsum(error * error for error in errors) / (2 * len(xs)),
            math.fsum(error * x for error, x in zip(errors, xs)) / len(xs))


def cosine_learning_rate(step, total_steps, maximum, minimum=0.0):
    if total_steps <= 0 or not 0 <= step <= total_steps or not 0 <= minimum <= maximum:
        raise ValueError("학습률과 단계 범위가 잘못되었습니다")
    return minimum + (maximum - minimum) * (1 + math.cos(math.pi * step / total_steps)) / 2


def tfidf_rank(documents, query):
    """공백·단어 기반의 작은 기준선이며 언어 모델 토크나이저와 다르다."""
    tokens = lambda text: Counter(re.findall(r"\w+", text.casefold()))
    counts = [tokens(document) for document in documents]
    q = tokens(query)
    df = Counter(term for count in counts for term in count)
    n = len(counts)
    idf = {term: 1 + math.log((n + 1) / (frequency + 1)) for term, frequency in df.items()}
    qv = {term: frequency * idf[term] for term, frequency in q.items() if term in idf}
    qnorm = math.sqrt(math.fsum(x * x for x in qv.values()))
    scores = []
    for i, count in enumerate(counts):
        dv = {term: frequency * idf[term] for term, frequency in count.items()}
        norm = math.sqrt(math.fsum(x * x for x in dv.values()))
        score = math.fsum(value * dv.get(term, 0) for term, value in qv.items())
        scores.append((i, score / (norm * qnorm) if norm and qnorm else 0.0))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def retrieval_metrics(ranking, relevant, k):
    if k < 1 or len(set(ranking)) != len(ranking) or not relevant:
        raise ValueError("중복 없는 순위, 정답 집합, 양의 k가 필요합니다")
    found = [i + 1 for i, item in enumerate(ranking[:k]) if item in relevant]
    return {"recall": len(found) / len(relevant),
            "reciprocal_rank": 1 / found[0] if found else 0.0}


def bounded_tool(name, arguments):
    """등록된 합산 함수만 실행하며 명령 문자열은 해석하지 않는다."""
    if name != "sum_numbers" or set(arguments) != {"values"}:
        raise ValueError("등록되지 않은 함수나 인자입니다")
    values = arguments["values"]
    if not isinstance(values, list) or len(values) > 100:
        raise ValueError("값은 최대 100개인 목록이어야 합니다")
    if any(type(x) not in (int, float) or abs(x) > 1e6 or not math.isfinite(x) for x in values):
        raise ValueError("값의 형식 또는 범위가 잘못되었습니다")
    return math.fsum(values)


def quantize(value, scale, zero_point, qmin=-128, qmax=127):
    if not math.isfinite(value) or not math.isfinite(scale) or scale <= 0:
        raise ValueError("유한한 값과 양의 스케일이 필요합니다")
    if any(type(x) is not int for x in (zero_point, qmin, qmax)) or not qmin <= zero_point <= qmax:
        raise ValueError("정수 범위가 잘못되었습니다")
    return min(qmax, max(qmin, round(value / scale) + zero_point))


def dequantize(value, scale, zero_point):
    if scale <= 0 or not math.isfinite(scale):
        raise ValueError("스케일은 유한한 양수여야 합니다")
    return scale * (value - zero_point)


def transform_point(matrix, point):
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix) or len(point) != 3:
        raise ValueError("4×4 행렬과 3차원 점이 필요합니다")
    homogeneous = (*point, 1.0)
    result = [math.fsum(a * b for a, b in zip(row, homogeneous)) for row in matrix]
    if result[3] == 0:
        raise ValueError("유한한 직교 좌표로 바꿀 수 없습니다")
    return tuple(value / result[3] for value in result[:3])


def barycentric(point, a, b, c):
    def cross(u, v):
        return u[0] * v[1] - u[1] * v[0]
    sub = lambda u, v: (u[0] - v[0], u[1] - v[1])
    area = cross(sub(b, a), sub(c, a))
    if area == 0:
        raise ValueError("삼각형이 퇴화했습니다")
    first = cross(sub(b, point), sub(c, point)) / area
    second = cross(sub(c, point), sub(a, point)) / area
    return first, second, 1 - first - second


def poisson_sine(intervals):
    """-u''=π²sin(πx), u(0)=u(1)=0을 삼중 대각 소거로 푼다."""
    if type(intervals) is not int or intervals < 2:
        raise ValueError("구간 수는 2 이상의 정수여야 합니다")
    h, n = 1 / intervals, intervals - 1
    diagonal = [2.0] * n
    rhs = [h * h * math.pi ** 2 * math.sin(math.pi * (i + 1) * h) for i in range(n)]
    for i in range(1, n):
        factor = -1 / diagonal[i - 1]
        diagonal[i] += factor
        rhs[i] -= factor * rhs[i - 1]
    interior = [0.0] * n
    interior[-1] = rhs[-1] / diagonal[-1]
    for i in range(n - 2, -1, -1):
        interior[i] = (rhs[i] + interior[i + 1]) / diagonal[i]
    return [0.0, *interior, 0.0]


def decay_euler(steps, duration=1.0):
    if type(steps) is not int or steps < 1 or not 0 < duration / steps < 2:
        raise ValueError("안정 구간의 양의 시간 간격이 필요합니다")
    value, dt = 1.0, duration / steps
    for _ in range(steps):
        value -= dt * value
    return value


class IdempotencyStore:
    """단일 프로세스·직렬 호출에서의 요청 중복 제거 모델."""
    def __init__(self):
        self.responses = {}
        self.created = 0

    def create(self, key, body):
        if not isinstance(key, str) or not key or len(key) > 128:
            raise ValueError("요청 키가 잘못되었습니다")
        if not isinstance(body, dict) or set(body) != {"name"}:
            raise ValueError("허용되지 않은 필드입니다")
        if not isinstance(body["name"], str) or not 1 <= len(body["name"].strip()) <= 80:
            raise ValueError("이름 길이가 잘못되었습니다")
        canonical = json.dumps(body, sort_keys=True, ensure_ascii=False, allow_nan=False)
        if key in self.responses:
            previous, response = self.responses[key]
            if previous != canonical:
                raise ValueError("같은 키로 다른 요청을 보낼 수 없습니다")
            return dict(response)
        self.created += 1
        response = {"id": self.created, "name": body["name"]}
        self.responses[key] = (canonical, response)
        return dict(response)


def page_after(sorted_unique_ids, cursor=None, limit=20):
    """정렬·유일성이 보장된 고정 스냅샷에서 키셋 페이지를 구한다."""
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("페이지 크기는 1~100의 정수여야 합니다")
    start = 0 if cursor is None else bisect_right(sorted_unique_ids, cursor)
    page = list(sorted_unique_ids[start:start + limit])
    next_cursor = page[-1] if start + len(page) < len(sorted_unique_ids) else None
    return page, next_cursor

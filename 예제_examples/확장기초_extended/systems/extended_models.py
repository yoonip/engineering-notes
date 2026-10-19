"""시스템 개념을 검산하는 작은 모형. 실제 운영체제나 장치 에뮬레이터는 아니다."""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import hashlib
import heapq
from itertools import count
import json
import math
import os
from pathlib import Path
import tempfile


def unix_mode_allows(mode: int, owner: bool, group: bool, requested: int) -> bool:
    if not 0 <= mode <= 0o777 or not 0 <= requested <= 7:
        raise ValueError("일반 rwx 비트 범위가 필요하다")
    # 소유자에 해당하면 그룹·기타 권한으로 다시 시도하지 않는다.
    shift = 6 if owner else 3 if group else 0
    available = (mode >> shift) & 7
    return available & requested == requested


def pipeline_status(statuses: Sequence[int], pipefail: bool = False) -> int:
    if not statuses or any(type(s) is not int or not 0 <= s <= 255 for s in statuses):
        raise ValueError("하나 이상의 셸 종료 상태가 필요하다")
    return next((s for s in reversed(statuses) if s), 0) if pipefail else statuses[-1]


def dependency_order(parents: Mapping[str, Sequence[str]]) -> list[str]:
    children = {name: [] for name in parents}
    remaining = {}
    for name, prerequisites in parents.items():
        unique = set(prerequisites)
        if not unique <= parents.keys():
            raise ValueError("정의되지 않은 선행 노드")
        remaining[name] = len(unique)
        for prerequisite in unique:
            children[prerequisite].append(name)
    ready = [name for name, n in remaining.items() if n == 0]
    heapq.heapify(ready)
    result = []
    while ready:
        node = heapq.heappop(ready)
        result.append(node)
        for child in children[node]:
            remaining[child] -= 1
            if remaining[child] == 0:
                heapq.heappush(ready, child)
    if len(result) != len(parents):
        raise ValueError("순환 의존성")
    return result


def snapshot_digest(files: Mapping[str, bytes]) -> str:
    digest = hashlib.sha256()
    # 길이를 넣어 파일명·내용 경계의 모호함을 없앤다. Git 객체 형식과는 다르다.
    for name in sorted(files):
        encoded = name.encode("utf-8")
        data = files[name]
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def run_cells(operations: Sequence[tuple[str, str, int]]) -> dict[str, int]:
    state = {}
    for operation, name, value in operations:
        if operation == "set":
            state[name] = value
        elif operation == "add":
            state[name] += value
        else:
            raise ValueError("알 수 없는 셀 연산")
    return state


def _matrix2(a: Sequence[Sequence[float]]) -> list[list[float]]:
    if len(a) != 2 or any(len(row) != 2 for row in a):
        raise ValueError("2×2 행렬이 필요하다")
    matrix = [[float(v) for v in row] for row in a]
    if not all(math.isfinite(v) for row in matrix for v in row):
        raise ValueError("유한한 원소가 필요하다")
    return matrix


def solve2(a: Sequence[Sequence[float]], b: Sequence[float]) -> tuple[float, float]:
    matrix = _matrix2(a)
    if len(b) != 2 or not all(math.isfinite(v) for v in b):
        raise ValueError("유한한 길이 2 우변이 필요하다")
    rhs = [float(v) for v in b]
    if abs(matrix[1][0]) > abs(matrix[0][0]):
        matrix.reverse()
        rhs.reverse()
    if matrix[0][0] == 0:
        raise ValueError("특이 행렬")
    factor = matrix[1][0] / matrix[0][0]
    pivot = matrix[1][1] - factor * matrix[0][1]
    if pivot == 0:
        raise ValueError("특이 행렬")
    y = (rhs[1] - factor * rhs[0]) / pivot
    x = (rhs[0] - matrix[0][1] * y) / matrix[0][0]
    if not all(math.isfinite(v) for v in (x, y)):
        raise ValueError("계산 범위를 벗어난 결과")
    return x, y


def condition_inf2(a: Sequence[Sequence[float]]) -> float:
    matrix = _matrix2(a)
    (a00, a01), (a10, a11) = matrix
    determinant = a00*a11 - a01*a10
    if determinant == 0:
        return math.inf
    norm_a = max(abs(a00)+abs(a01), abs(a10)+abs(a11))
    norm_inverse = max(abs(a11)+abs(a01), abs(a10)+abs(a00)) / abs(determinant)
    return norm_a * norm_inverse


def backward_error(a, b, x) -> float:
    matrix = _matrix2(a)
    if len(b) != 2 or len(x) != 2 or not all(math.isfinite(v) for v in (*b, *x)):
        raise ValueError("유한한 길이 2 벡터가 필요하다")
    residual = max(abs(b[i] - sum(matrix[i][j]*x[j] for j in range(2))) for i in range(2))
    scale = max(sum(abs(v) for v in row) for row in matrix)*max(map(abs, x)) + max(map(abs, b))
    return residual / scale if scale else 0.0


def dijkstra(graph: Mapping[object, Sequence[tuple[object, int]]], source: object) -> dict:
    nodes = set(graph)
    for edges in graph.values():
        for target, weight in edges:
            if type(weight) is not int or weight < 0:
                raise ValueError("음이 아닌 정수 가중치가 필요하다")
            nodes.add(target)
    if source not in nodes:
        raise ValueError("시작 노드가 없다")
    distance = {node: math.inf for node in nodes}
    distance[source] = 0
    tickets = count()
    queue = [(0, next(tickets), source)]
    while queue:
        current, _, node = heapq.heappop(queue)
        if current != distance[node]:
            continue
        for target, weight in graph.get(node, ()):
            candidate = current + weight
            if candidate < distance[target]:
                distance[target] = candidate
                heapq.heappush(queue, (candidate, next(tickets), target))
    return distance


def probe_model(compatible: Sequence[str], supported: set[str], required: set[str], available: set[str]) -> str:
    if not set(compatible) & supported:
        return "no-match"
    return "bound" if required <= available else "deferred"


@dataclass
class DebugTarget:
    pc: int = 0
    halted: bool = False

    def halt(self) -> None:
        self.halted = True

    def resume(self) -> None:
        self.halted = False

    def read_pc(self) -> int:
        if not self.halted:
            raise RuntimeError("정지 상태가 필요하다")
        return self.pc

    def step_model(self, instruction_bytes: int) -> None:
        if not self.halted or type(instruction_bytes) is not int or instruction_bytes <= 0:
            raise ValueError("정지 상태와 양의 명령 길이가 필요하다")
        # 분기·예외·주변장치 동작을 제외한 상태 전이 모형이다.
        self.pc += instruction_bytes


def wheel_rates(v: float, omega: float, radius: float, separation: float) -> tuple[float, float]:
    if not all(math.isfinite(z) for z in (v, omega, radius, separation)) or radius <= 0 or separation <= 0:
        raise ValueError("유한한 속도와 양의 기하 치수가 필요하다")
    return (v - omega*separation/2)/radius, (v + omega*separation/2)/radius


def odometry_step(pose, left_distance: float, right_distance: float, separation: float) -> tuple[float, float, float]:
    if len(pose) != 3 or not all(math.isfinite(z) for z in (*pose, left_distance, right_distance, separation)) or separation <= 0:
        raise ValueError("유한한 자세·거리와 양의 바퀴 간격이 필요하다")
    x, y, theta = pose
    ds = (left_distance + right_distance)/2
    dtheta = (right_distance - left_distance)/separation
    half = dtheta/2
    sinc = 1 - half*half/6 + half**4/120 if abs(half) < 1e-4 else math.sin(half)/half
    return x + ds*sinc*math.cos(theta+half), y + ds*sinc*math.sin(theta+half), theta+dtheta


def publish_json(path: Path, payload: object, validate: Callable[[object], bool] = lambda value: True) -> bool:
    if not validate(payload):
        raise ValueError("게시 전 검증 실패")
    data = (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")
    if path.exists() and path.read_bytes() == data:
        return False
    descriptor, temporary = tempfile.mkstemp(prefix=".publish-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return True


def encode_records(records: Sequence[bytes], max_record: int = 1024, max_total: int = 8192) -> bytes:
    if not 0 <= max_record <= 65535 or max_total < 0:
        raise ValueError("범위 제한이 잘못되었다")
    output = bytearray()
    for record in records:
        if not isinstance(record, bytes) or len(record) > max_record or len(output)+2+len(record) > max_total:
            raise ValueError("레코드 범위 초과")
        output.extend(len(record).to_bytes(2, "big"))
        output.extend(record)
    return bytes(output)


def decode_records(data: bytes, max_record: int = 1024, max_total: int = 8192) -> list[bytes]:
    if not 0 <= max_record <= 65535 or max_total < 0 or len(data) > max_total:
        raise ValueError("입력 범위 초과")
    records = []
    offset = 0
    while offset < len(data):
        if len(data)-offset < 2:
            raise ValueError("잘린 길이 필드")
        size = int.from_bytes(data[offset:offset+2], "big")
        offset += 2
        if size > max_record or size > len(data)-offset:
            raise ValueError("잘리거나 범위를 넘은 레코드")
        records.append(data[offset:offset+size])
        offset += size
    return records


@dataclass
class LatestResults:
    generation: int = 0
    query: str = ""
    phase: str = "idle"
    result: tuple = ()
    closed: bool = False

    def begin(self, query: str) -> int:
        if self.closed:
            raise RuntimeError("화면이 닫혔다")
        self.generation += 1
        self.query, self.phase, self.result = query, "loading", ()
        return self.generation

    def finish(self, ticket: int, result: Sequence) -> bool:
        if self.closed or ticket != self.generation or self.phase != "loading":
            return False
        self.result, self.phase = tuple(result), "ready"
        return True

    def close(self) -> None:
        self.closed = True
        self.generation += 1

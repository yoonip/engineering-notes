"""심화 해설의 실행 가능한 상태 모델과 계산 예제."""

from __future__ import annotations

import csv
import hashlib
import heapq
import hmac
import io
import json
import math
import re
import selectors
import socket
import statistics
from collections import OrderedDict, deque
from dataclasses import dataclass, replace
from itertools import count


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


class BoundedStream:
    def __init__(self, capacity):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("capacity")
        self.capacity, self.data, self.closed = capacity, deque(), False

    def write(self, data):
        if self.closed:
            raise ValueError("closed writer")
        n = min(len(data), self.capacity - len(self.data))
        self.data.extend(data[:n])
        return n

    def read(self, size):
        if type(size) is not int or size <= 0:
            raise ValueError("size")
        if not self.data and not self.closed:
            raise BlockingIOError("empty, writer open")
        return bytes(self.data.popleft() for _ in range(min(size, len(self.data))))

    def close_writer(self):
        self.closed = True


def action_key(inputs, command, toolchain, environment):
    if not all(isinstance(k, str) and isinstance(v, bytes) for k, v in inputs.items()):
        raise ValueError("inputs")
    envelope = {"schema": 1, "inputs": {k: digest(v) for k, v in inputs.items()},
                "command": list(command), "toolchain": toolchain, "environment": environment}
    return digest(canonical(envelope))


class ArtifactCache:
    def __init__(self):
        self.entries = {}

    def put(self, key, content):
        self.entries[key] = (digest(content), bytes(content))

    def get(self, key):
        if key not in self.entries:
            return None
        expected, data = self.entries[key]
        if digest(data) != expected:
            raise ValueError("cache corruption")
        return bytes(data)


def load_measurements(raw):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
    if reader.fieldnames != ["id", "value"]:
        raise ValueError("schema")
    rows, seen = [], set()
    for row in reader:
        if set(row) != {"id", "value"} or row["value"] is None:
            raise ValueError("row width")
        name = row["id"]
        value = float(row["value"])
        if not name or name in seen or not math.isfinite(value):
            raise ValueError("row")
        seen.add(name)
        rows.append((name, value))
    return sorted(rows)


def split_ids(rows, seed, test_count):
    if not 0 <= test_count <= len(rows):
        raise ValueError("test_count")
    ids = [name for name, _ in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate id")
    ranked = sorted(ids, key=lambda name: (digest(canonical([seed, name])), name))
    test = set(ranked[:test_count])
    return sorted(set(ids) - test), sorted(test)


class ByteRing:
    def __init__(self, capacity):
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("capacity")
        self.storage = bytearray(capacity)
        self.head = self.tail = self.used = 0

    def push(self, value):
        if type(value) is not int or not 0 <= value <= 255:
            raise ValueError("byte")
        if self.used == len(self.storage):
            return False
        self.storage[self.head] = value
        self.head = (self.head + 1) % len(self.storage)
        self.used += 1
        return True

    def pop(self):
        if not self.used:
            return None
        value = self.storage[self.tail]
        self.tail = (self.tail + 1) % len(self.storage)
        self.used -= 1
        return value


@dataclass(frozen=True)
class RootResult:
    x: float
    lo: float
    hi: float
    residual: float
    iterations: int


def bracketed_newton(f, derivative, lo, hi, tolerance=1e-10, max_steps=200):
    if not all(math.isfinite(v) for v in (lo, hi, tolerance, hi-lo)) or lo >= hi or tolerance <= 0:
        raise ValueError("bracket")
    flo, fhi = f(lo), f(hi)
    if not math.isfinite(flo) or not math.isfinite(fhi):
        raise ValueError("nonfinite function")
    if flo == 0:
        return RootResult(lo, lo, lo, 0.0, 0)
    if fhi == 0:
        return RootResult(hi, hi, hi, 0.0, 0)
    if (flo > 0) == (fhi > 0):
        raise ValueError("no sign change")
    for step in range(1, max_steps + 1):
        mid = lo + (hi - lo) / 2
        if (hi - lo) / 2 <= tolerance:
            return RootResult(mid, lo, hi, abs(f(mid)), step - 1)
        if mid == lo or mid == hi:
            raise ArithmeticError("floating-point bracket stagnation")
        fm, slope = f(mid), derivative(mid)
        if not math.isfinite(fm):
            raise ValueError("nonfinite function")
        candidate = mid
        if math.isfinite(slope) and slope != 0:
            newton = mid - fm / slope
            margin = (hi - lo) * 0.1
            if lo + margin <= newton <= hi - margin:
                candidate = newton
        fc = f(candidate)
        if not math.isfinite(fc):
            raise ValueError("nonfinite function")
        if fc == 0:
            return RootResult(candidate, candidate, candidate, 0.0, step)
        if (flo > 0) == (fc > 0):
            lo, flo = candidate, fc
        else:
            hi, fhi = candidate, fc
    raise ArithmeticError("iteration limit")


def cache_trace(addresses, line_bytes=64, lines=4):
    if line_bytes <= 0 or lines <= 0:
        raise ValueError("cache geometry")
    resident, misses = OrderedDict(), 0
    for address in addresses:
        if address < 0:
            raise ValueError("address")
        line = address // line_bytes
        if line not in resident:
            misses += 1
            if len(resident) == lines:
                resident.popitem(last=False)
        else:
            resident.move_to_end(line)
        resident[line] = None
    return misses


def grid_graph(width, height, blocked=()):
    blocked = set(blocked)
    graph = {}
    for y in range(height):
        for x in range(width):
            if (x, y) not in blocked:
                graph[x, y] = [(p, 1.0) for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                               if 0 <= p[0] < width and 0 <= p[1] < height and p not in blocked]
    return graph


def astar(graph, start, goal, heuristic):
    if start not in graph or goal not in graph:
        raise ValueError("endpoint")
    for edges in graph.values():
        for node, weight in edges:
            if node not in graph or not math.isfinite(weight) or weight < 0:
                raise ValueError("edge")
    hs = {v: heuristic(v) for v in graph}
    if any(not math.isfinite(h) or h < 0 for h in hs.values()) or hs[goal] != 0:
        raise ValueError("heuristic")
    serial, distance, parent = count(), {start: 0.0}, {}
    frontier, expanded = [(hs[start], next(serial), 0.0, start)], 0
    while frontier:
        _, _, cost, node = heapq.heappop(frontier)
        if cost != distance[node]:
            continue
        expanded += 1
        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return cost, list(reversed(path)), expanded
        for other, weight in graph[node]:
            new = cost + weight
            if new < distance.get(other, math.inf):
                distance[other], parent[other] = new, node
                heapq.heappush(frontier, (new + hs[other], next(serial), new, other))
    return math.inf, [], expanded


def inherited_priorities(base, owners, waiting):
    if any(task not in base for task in owners.values()) or any(task not in base for task in waiting):
        raise ValueError("task")
    effective = dict(base)
    # 우선순위 값은 유한한 집합에서만 증가하므로 고정점에 도달한다.
    changed = True
    while changed:
        changed = False
        for waiter, lock in waiting.items():
            owner = owners.get(lock)
            if owner is not None and effective[owner] < effective[waiter]:
                effective[owner] = effective[waiter]
                changed = True
    return effective


def inversion_trace(inherit):
    remaining, trace = {"L": 3, "M": 4, "H": 1}, []
    base, owner = {"L": 1, "M": 2, "H": 3}, "L"
    while any(remaining.values()):
        waiting = {"H": "mutex"} if owner else {}
        priorities = inherited_priorities(base, {"mutex": owner}, waiting) if inherit and owner else base
        ready = [t for t, ticks in remaining.items() if ticks and not (t == "H" and owner)]
        task = max(ready, key=lambda t: priorities[t])
        remaining[task] -= 1
        trace.append(task)
        if task == "L" and remaining[task] == 0:
            owner = None
    return trace


class LineReceiver:
    def __init__(self, limit=80):
        if limit <= 0:
            raise ValueError("limit")
        self.limit, self.pending, self.done = limit, bytearray(), False

    def feed(self, chunk):
        if self.done:
            raise ValueError("after EOF")
        records = []
        for byte in chunk:
            if byte == 10:
                records.append(bytes(self.pending))
                self.pending.clear()
            else:
                if len(self.pending) == self.limit:
                    raise ValueError("line too long")
                self.pending.append(byte)
        return records

    def eof(self):
        self.done = True
        if self.pending:
            raise ValueError("truncated final record")


def socket_records(raw):
    if len(raw) > 1024:
        raise ValueError("fixture limit")
    receiver, records = LineReceiver(), []
    with _socket_pair_context() as pair:
        reader, writer = pair
        writer.sendall(raw)
        writer.shutdown(socket.SHUT_WR)
        reader.setblocking(False)
        with selectors.DefaultSelector() as selector:
            selector.register(reader, selectors.EVENT_READ)
            while True:
                if not selector.select(timeout=1.0):
                    raise TimeoutError("fixture readiness")
                try:
                    data = reader.recv(3)
                except BlockingIOError:
                    continue
                if not data:
                    receiver.eof()
                    return records
                records.extend(receiver.feed(data))


class _socket_pair_context:
    def __enter__(self):
        self.pair = socket.socketpair()
        return self.pair

    def __exit__(self, *_):
        for endpoint in self.pair:
            endpoint.close()


def watch_hits(events, address, size, access="write", detect_same=True):
    if address < 0 or size <= 0 or access not in {"read", "write", "access"}:
        raise ValueError("watch region")
    hits = []
    for index, (kind, begin, before, after) in enumerate(events):
        if kind not in {"read", "write"} or begin < 0 or len(before) != len(after):
            raise ValueError("event")
        overlap = max(address, begin) < min(address + size, begin + len(after))
        wanted = access == "access" or kind == access
        first, last = max(address, begin) - begin, min(address + size, begin + len(after)) - begin
        changed = overlap and before[first:last] != after[first:last]
        if overlap and wanted and (kind == "read" or detect_same or changed):
            hits.append(index)
    return hits


def i2c_register_read(address, register, data):
    if type(address) is not int or not 0 <= address < 128 or not 0 <= register < 256 or not data:
        raise ValueError("7-bit address, byte register, positive length")
    events = [("START",), ("TX", address << 1), ("ACK",),
              ("TX", register), ("ACK",), ("RESTART",),
              ("TX", (address << 1) | 1), ("ACK",)]
    for i, byte in enumerate(data):
        events.extend([("RX", byte), ("NACK",) if i == len(data)-1 else ("ACK",)])
    return events + [("STOP",)]


@dataclass
class PIController:
    kp: float
    ki: float
    lower: float
    upper: float
    integral: float = 0.0

    def update(self, target, measured, dt):
        if not all(math.isfinite(x) for x in (target, measured, dt, self.kp, self.ki,
                                             self.lower, self.upper, self.integral)):
            raise ValueError("finite parameters")
        if dt <= 0 or self.kp < 0 or self.ki < 0 or self.lower >= self.upper:
            raise ValueError("controller parameters")
        error = target - measured
        candidate = self.integral + self.ki * dt * error
        raw = self.kp * error + candidate
        if not ((raw > self.upper and error > 0) or (raw < self.lower and error < 0)):
            self.integral = candidate
        return min(self.upper, max(self.lower, self.kp * error + self.integral))


def simulate_speed(controller, target=1.0, dt=0.02, steps=500, tau=0.3, gain=2.0):
    if tau <= 0 or dt <= 0:
        raise ValueError("plant parameters")
    speed, history = 0.0, []
    decay = math.exp(-dt / tau)
    for _ in range(steps):
        command = controller.update(target, speed, dt)
        speed = decay * speed + gain * (1 - decay) * command
        history.append((speed, command))
    return history


def paired_summary(a, b):
    if len(a) != len(b) or len(a) < 2 or not all(math.isfinite(x) for x in [*a, *b]):
        raise ValueError("paired finite samples")
    differences = [y - x for x, y in zip(a, b)]
    mean = statistics.fmean(differences)
    variance = statistics.variance(differences)
    return mean, math.sqrt(variance / len(differences)), differences


def affected_targets(dependencies, changed):
    all_nodes = set(dependencies)
    all_nodes.update(v for deps in dependencies.values() for v in deps)
    if not set(changed) <= all_nodes:
        raise ValueError("unknown change")
    state, reverse = {}, {n: [] for n in all_nodes}

    def visit(node):
        if state.get(node) == 1:
            raise ValueError("dependency cycle")
        if state.get(node) == 2:
            return
        state[node] = 1
        for dep in dependencies.get(node, ()):
            visit(dep)
        state[node] = 2

    for node in all_nodes:
        visit(node)
        for dep in dependencies.get(node, ()):
            reverse[dep].append(node)
    affected, queue = set(changed), deque(changed)
    while queue:
        for node in reverse[queue.popleft()]:
            if node not in affected:
                affected.add(node)
                queue.append(node)
    return sorted(n for n in affected if n in dependencies)


class ReplayReceiver:
    def __init__(self, key, context=b"example-v1", width=32):
        if len(key) < 32 or type(width) is not int or not 1 <= width <= 4096:
            raise ValueError("key/window")
        self.key, self.context, self.width = bytes(key), bytes(context), width
        self.highest, self.bitmap = 0, 0

    def tag(self, sequence, payload):
        if type(sequence) is not int or not 1 <= sequence < 2**64 or len(payload) > 4096:
            raise ValueError("sequence/payload")
        message = canonical([self.context.hex(), sequence, bytes(payload).hex()])
        return hmac.digest(self.key, message, "sha256")

    def accept(self, sequence, payload, tag):
        expected = self.tag(sequence, payload)
        if not hmac.compare_digest(expected, tag):
            return False
        if sequence > self.highest:
            shift = sequence - self.highest
            self.bitmap = 1 if shift >= self.width else ((self.bitmap << shift) | 1) & ((1 << self.width)-1)
            self.highest = sequence
            return True
        offset = self.highest - sequence
        if offset >= self.width or self.bitmap & (1 << offset):
            return False
        self.bitmap |= 1 << offset
        return True


def compile_expression(source):
    if len(source) > 512:
        raise ValueError("source limit")
    tokens, position = [], 0
    pattern = re.compile(r"[0-9]+|[()+*\-]")
    while position < len(source):
        if source[position].isspace():
            position += 1
            continue
        match = pattern.match(source, position)
        if not match:
            raise ValueError("token")
        tokens.append(match.group())
        position = match.end()
    index, code = 0, []

    def expression(minimum=0, depth=0):
        nonlocal index
        if depth > 64 or index == len(tokens):
            raise ValueError("depth/operand")
        token = tokens[index]
        index += 1
        if token.isdigit():
            code.append(("PUSH", int(token)))
        elif token == "-":
            expression(30, depth+1)
            code.append(("NEG",))
        elif token == "(":
            expression(0, depth+1)
            if index == len(tokens) or tokens[index] != ")":
                raise ValueError("closing parenthesis")
            index += 1
        else:
            raise ValueError("operand")
        precedence = {"+": 10, "-": 10, "*": 20}
        while index < len(tokens) and precedence.get(tokens[index], -1) >= minimum:
            operator = tokens[index]
            index += 1
            expression(precedence[operator]+1, depth+1)
            code.append(({"+": "ADD", "-": "SUB", "*": "MUL"}[operator],))

    expression()
    if index != len(tokens):
        raise ValueError("trailing tokens")
    return code


def execute(code):
    stack = []
    for instruction in code:
        if not isinstance(instruction, tuple) or not instruction:
            raise ValueError("invalid instruction")
        op = instruction[0]
        if op == "PUSH" and len(instruction) == 2 and type(instruction[1]) is int:
            stack.append(instruction[1])
        elif op == "NEG" and len(instruction) == 1 and stack:
            stack[-1] = -stack[-1]
        elif op in {"ADD", "SUB", "MUL"} and len(instruction) == 1 and len(stack) >= 2:
            right, left = stack.pop(), stack.pop()
            stack.append(left+right if op == "ADD" else left-right if op == "SUB" else left*right)
        else:
            raise ValueError("invalid bytecode/stack")
    if len(stack) != 1:
        raise ValueError("final stack")
    return stack[0]


def shrink_failure(values, fails):
    result = list(values)
    if not fails(result):
        raise ValueError("input does not fail")
    index = 0
    while index < len(result):
        candidate = result[:index] + result[index+1:]
        if fails(candidate):
            result = candidate
            index = 0
        else:
            index += 1
    return result


class VersionedResource:
    def __init__(self, value):
        self.value, self.version = str(value), 1

    @property
    def etag(self):
        return '"v%d"' % self.version

    def read(self):
        return self.value, self.etag

    def put(self, value, if_match):
        if if_match is None:
            return 428
        if if_match != self.etag:
            return 412
        if not isinstance(value, str) or not value or len(value) > 256:
            return 400
        self.value, self.version = value, self.version + 1
        return 200


@dataclass(frozen=True)
class UIState:
    query: str = ""
    generation: int = 0
    loading: bool = False
    result: tuple = ()
    error: str | None = None
    active: bool = True


def reduce_ui(state, event):
    kind = event[0]
    if kind == "search" and state.active:
        query = event[1]
        if not isinstance(query, str) or len(query) > 128:
            raise ValueError("query")
        new = replace(state, query=query, generation=state.generation+1,
                      loading=True, error=None, result=())
        return new, ("fetch", new.generation, query)
    if kind in {"success", "failure"}:
        if not state.active or event[1] != state.generation or not state.loading:
            return state, None
        if kind == "success":
            return replace(state, loading=False, result=tuple(event[2]), error=None), None
        return replace(state, loading=False, error=str(event[2]), result=()), None
    if kind == "stop":
        return replace(state, active=False, loading=False, generation=state.generation+1), None
    if kind == "start":
        return replace(state, active=True), None
    if kind == "search":
        return state, None
    raise ValueError("event")

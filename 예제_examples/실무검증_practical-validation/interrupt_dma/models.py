"""W1C·버퍼 소유권·write-back 캐시의 결정적인 호스트 모형입니다."""
LINE = 32  # 캐시 유지 연산의 단위를 이 모형에서는 32바이트로 고정합니다.


def integer(value: int, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:  # bool을 정수 입력에서 제외합니다.
        raise ValueError(f"integer in [{low}, {high}] required")
    return value


def w1c_after(pending: int, handled_mask: int, rmw: bool) -> dict:
    integer(pending, 0, 255)
    integer(handled_mask, 0, 255)
    written = pending | handled_mask if rmw else handled_mask  # |는 비트 OR입니다.
    after = pending & ~written & 255  # W1C는 쓴 값이 1인 위치만 소거합니다.
    return {"pending_before": pending, "handled_mask": handled_mask,
            "written": written, "pending_after": after}


def buffer_reuse(first: int, second: int, replacement: int, respect_owner: bool) -> dict:
    slots = {name: {"state": "FREE", "value": None} for name in ("A", "B")}
    events = []  # list에 완료·인계·재사용 시도를 순서대로 기록합니다.

    def record(label: str) -> None:
        events.append({"step": label, "slots": {name: state.copy() for name, state in slots.items()}})

    def fill(name: str, value: int) -> bool:
        slot = slots[name]
        if respect_owner and slot["state"] != "FREE":
            return False  # READY/CPU 상태의 버퍼를 새 DMA에 넘기지 않습니다.
        slot["state"] = "DMA"
        slot["value"] = value  # 이 추상 사건은 DMA가 메모리에 쓴 값을 뜻합니다.
        record(f"fill_{name}_{value}")
        slot["state"] = "READY"  # 완료 관측 뒤 인계 대기 상태로 바꿉니다.
        record(f"complete_{name}_{value}")
        return True

    fill("A", first)
    slots["A"]["state"] = "CPU"  # 소비자가 완료 버퍼 A를 인수합니다.
    record("claim_A")
    fill("B", second)  # B도 완료돼 인계 대기 중입니다.
    allowed = fill("A", replacement)  # A를 소비자가 반환하기 전 재사용하려는 대조입니다.
    observed = slots["A"]["value"]
    record("read_A")
    return {"reuse_allowed": allowed, "cpu_observed": observed,
            "outstanding_B": slots["B"]["value"], "events": events}


def covered_lines(start: int, length: int, total: int = 128) -> list[int]:
    integer(start, 0, total)
    integer(length, 0, total - start)
    if length == 0:
        return []  # 길이 0은 어떤 line에도 유지 연산을 하지 않습니다.
    lo = start // LINE * LINE  # //는 정수 나눗셈이며 시작을 아래 경계로 내립니다.
    hi = (start + length + LINE - 1) // LINE * LINE
    return list(range(lo, hi, LINE))  # range는 끝을 제외한 일정 간격의 정수를 만듭니다.


class CacheMemory:
    def __init__(self, size: int = 128):
        if size % LINE or size <= 0:
            raise ValueError("memory size must be a positive cache-line multiple")
        self.ram = bytearray(size)  # bytearray는 변경 가능한 바이트 저장 공간입니다.
        self.lines = {}  # dict는 line 주소와 캐시 복사본·dirty 상태를 연결합니다.

    def line(self, address: int) -> dict:
        base = address // LINE * LINE
        if base not in self.lines:  # not in은 아직 캐시에 없는 주소인지 확인합니다.
            self.lines[base] = {"data": self.ram[base:base + LINE], "dirty": False}
        return self.lines[base]

    def cpu_read(self, start: int, length: int) -> bytes:
        covered_lines(start, length, len(self.ram))
        return bytes(self.line(i)["data"][i % LINE] for i in range(start, start + length))

    def cpu_write(self, start: int, data: bytes) -> None:
        covered_lines(start, len(data), len(self.ram))
        for offset, value in enumerate(data):  # enumerate는 위치와 값을 함께 제공합니다.
            address = start + offset
            line = self.line(address)
            line["data"][address % LINE] = value
            line["dirty"] = True  # RAM에 아직 반영하지 않은 CPU 쓰기를 표시합니다.

    def dma_read(self, start: int, length: int) -> bytes:
        covered_lines(start, length, len(self.ram))
        return bytes(self.ram[start:start + length])  # DMA는 이 모형에서 RAM만 봅니다.

    def dma_write(self, start: int, data: bytes) -> None:
        covered_lines(start, len(data), len(self.ram))
        self.ram[start:start + len(data)] = data

    def clean(self, start: int, length: int) -> None:
        for base in covered_lines(start, length, len(self.ram)):
            line = self.lines.get(base)
            if line is not None and line["dirty"]:
                self.ram[base:base + LINE] = line["data"]  # line 전체의 모형 값을 반영합니다.
                line["dirty"] = False

    def invalidate(self, start: int, length: int) -> None:
        for base in covered_lines(start, length, len(self.ram)):
            self.lines.pop(base, None)  # pop은 캐시 사본을 버리며 dirty도 자동 보존하지 않습니다.


def tx_case(address: int, payload: bytes, clean_before: bool) -> dict:
    memory = CacheMemory()
    memory.cpu_write(address, payload)
    if clean_before:
        memory.clean(address, len(payload))
    return {"dma_hex": memory.dma_read(address, len(payload)).hex(),
            "cpu_hex": memory.cpu_read(address, len(payload)).hex()}


def rx_case(address: int, payload: bytes, invalidate_after: bool) -> dict:
    memory = CacheMemory()
    memory.clean(address, len(payload))
    memory.invalidate(address, len(payload))  # 사전 전용 line 처리를 표현합니다.
    memory.cpu_read(address, len(payload))  # DMA 쓰기 전 오래된 사본이 채워지는 경우를 가정합니다.
    memory.dma_write(address, payload)
    if invalidate_after:
        memory.invalidate(address, len(payload))
    return {"ram_hex": memory.dma_read(address, len(payload)).hex(),
            "cpu_hex": memory.cpu_read(address, len(payload)).hex()}


def dirty_rx_case(address: int, payload: bytes, prepare_before: bool) -> dict:
    memory = CacheMemory()
    memory.cpu_write(address, bytes([7]) * len(payload))
    if prepare_before:
        memory.clean(address, len(payload))
        memory.invalidate(address, len(payload))
    memory.dma_write(address, payload)
    memory.clean(address, len(payload))  # 사전 처리가 없으면 남은 dirty 사본이 새 RAM을 덮습니다.
    memory.invalidate(address, len(payload))
    return {"cpu_hex": memory.cpu_read(address, len(payload)).hex(),
            "ram_hex": memory.dma_read(address, len(payload)).hex()}


def neighbor_case(payload: bytes, flag_address: int, flag_value: int, post_clean: bool) -> dict:
    memory = CacheMemory()
    memory.clean(0, len(payload))
    memory.invalidate(0, len(payload))
    memory.cpu_write(flag_address, bytes([flag_value]))  # 공유 line이면 오래된 RX 사본도 dirty가 됩니다.
    memory.dma_write(0, payload)
    if post_clean:
        memory.clean(0, len(payload))  # 결함 대조: 사후 clean으로 오래된 RX를 다시 쓰는 경우입니다.
    memory.invalidate(0, len(payload))
    return {"cpu_hex": memory.cpu_read(0, len(payload)).hex(),
            "flag": memory.cpu_read(flag_address, 1)[0]}

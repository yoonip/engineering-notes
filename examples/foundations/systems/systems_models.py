from dataclasses import dataclass
from fractions import Fraction
import hashlib
import hmac
import struct


def signed_word(raw: int, bits: int) -> int:
    if bits < 1 or not 0 <= raw < (1 << bits):
        raise ValueError("invalid word")
    return raw - (1 << bits) if raw & (1 << (bits - 1)) else raw


def quantize(value: Fraction, bits: int, fractional: int) -> int:
    if bits < 2 or not 0 <= fractional < bits:
        raise ValueError("invalid format")
    # 정확한 유리수에서 짝수 쪽 반올림을 수행한 뒤 표현 범위로 제한한다.
    code = round(Fraction(value) * (1 << fractional))
    return max(-(1 << (bits - 1)), min((1 << (bits - 1)) - 1, code))


def fixed_multiply(a: int, b: int, bits: int, fractional: int) -> int:
    if bits < 2 or not 0 <= fractional < bits:
        raise ValueError("invalid format")
    lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    if not (lo <= a <= hi and lo <= b <= hi):
        raise ValueError("invalid operand")
    # 곱의 소수 비트가 두 배가 되므로 원래 스케일로 한 번 되돌린다.
    code = round(Fraction(a * b, 1 << fractional))
    return max(lo, min(hi, code))


def binary32_value(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", value))[0]


def initialize_ram(flash: bytes, ram_size: int, data_load: int, data_start: int,
                   data_size: int, bss_start: int, bss_size: int) -> bytearray:
    values = (ram_size, data_load, data_start, data_size, bss_start, bss_size)
    if any(v < 0 for v in values):
        raise ValueError("negative range")
    if data_load + data_size > len(flash):
        raise ValueError("flash range")
    if data_start + data_size > ram_size or bss_start + bss_size > ram_size:
        raise ValueError("ram range")
    if data_size and bss_size and max(data_start, bss_start) < min(
            data_start + data_size, bss_start + bss_size):
        raise ValueError("overlapping ranges")
    # 초기화 대상 밖의 값을 보존하는지도 검사할 수 있도록 표시값을 둔다.
    ram = bytearray([0xA5]) * ram_size
    ram[data_start:data_start + data_size] = flash[data_load:data_load + data_size]
    ram[bss_start:bss_start + bss_size] = bytes(bss_size)
    return ram


class DmaBuffer:
    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("invalid size")
        self.memory = bytearray(size)
        self.cache = bytearray(size)
        self.valid = True
        self.dirty = False
        self.owner = "CPU"

    def _cpu(self):
        if self.owner != "CPU":
            raise RuntimeError("buffer is not CPU-owned")

    def cpu_write(self, payload: bytes):
        self._cpu()
        if len(payload) != len(self.memory):
            raise ValueError("size mismatch")
        self.cache[:] = payload
        self.valid, self.dirty = True, True

    def cpu_read(self) -> bytes:
        self._cpu()
        if not self.valid:
            self.cache[:] = self.memory
            self.valid = True
        return bytes(self.cache)

    def start_tx(self):
        self._cpu()
        # 이 모델은 버퍼 전체를 독립된 캐시 라인 범위로 가정한다.
        if self.dirty:
            self.memory[:] = self.cache
        self.dirty = False
        self.owner = "DEVICE_TX"

    def finish_tx(self) -> bytes:
        if self.owner != "DEVICE_TX":
            raise RuntimeError("no transmit transfer")
        result = bytes(self.memory)
        self.owner = "CPU"
        return result

    def start_rx(self):
        self._cpu()
        # 수신 전에 기존 변경을 정리하고 CPU가 이 버퍼를 건드리지 않게 한다.
        if self.dirty:
            self.memory[:] = self.cache
        self.dirty, self.valid, self.owner = False, False, "DEVICE_RX"

    def finish_rx(self, payload: bytes):
        if self.owner != "DEVICE_RX":
            raise RuntimeError("no receive transfer")
        if len(payload) != len(self.memory):
            raise ValueError("size mismatch")
        self.memory[:] = payload
        self.owner = "DONE_RX"

    def acquire_rx(self):
        if self.owner != "DONE_RX":
            raise RuntimeError("receive is not complete")
        # 완료 확인 뒤 다시 무효화하여 CPU가 새 메모리를 읽게 한다.
        self.valid, self.dirty, self.owner = False, False, "CPU"


def crc16_x25(data: bytes) -> int:
    crc = 0xFFFF
    for octet in data:
        crc ^= octet
        for _ in range(8):
            crc = (crc >> 1) ^ (0x8408 if crc & 1 else 0)
    return crc ^ 0xFFFF


def encode_frame(payload: bytes, max_payload: int = 1024) -> bytes:
    if max_payload < 0 or len(payload) > max_payload:
        raise ValueError("payload too long")
    raw = payload + crc16_x25(payload).to_bytes(2, "little")
    result = bytearray([0x7E])
    for octet in raw:
        if octet in (0x7D, 0x7E):
            result.extend((0x7D, octet ^ 0x20))
        else:
            result.append(octet)
    result.append(0x7E)
    return bytes(result)


class FrameParser:
    def __init__(self, max_payload: int = 1024):
        if max_payload < 0:
            raise ValueError("negative capacity")
        self.max_raw = max_payload + 2
        self.buffer = bytearray()
        self.active = False
        self.escaped = False
        self.dropping = False

    def feed(self, chunk: bytes):
        for octet in chunk:
            if octet == 0x7E:
                if self.active and not self.dropping and not self.escaped:
                    if len(self.buffer) >= 2:
                        raw = bytes(self.buffer)
                        if crc16_x25(raw[:-2]) == int.from_bytes(raw[-2:], "little"):
                            yield raw[:-2]
                self.buffer.clear()
                self.active, self.escaped, self.dropping = True, False, False
            elif not self.active or self.dropping:
                continue
            elif self.escaped:
                self.escaped = False
                self._append(octet ^ 0x20)
            elif octet == 0x7D:
                self.escaped = True
            else:
                self._append(octet)

    def _append(self, octet: int):
        if len(self.buffer) == self.max_raw:
            # 경계가 나올 때까지 버려 재동기화한다. 메모리는 상한을 넘지 않는다.
            self.buffer.clear()
            self.dropping, self.escaped = True, False
        else:
            self.buffer.append(octet)


@dataclass(frozen=True)
class Page:
    frame: int
    readable: bool = True
    writable: bool = False


def translate(address: int, page_table: dict[int, Page], write: bool = False,
              page_bits: int = 12) -> int:
    if address < 0 or page_bits < 1:
        raise ValueError("invalid address")
    vpn, offset = divmod(address, 1 << page_bits)
    page = page_table.get(vpn)
    if page is None:
        raise MemoryError("unmapped page")
    if page.frame < 0:
        raise ValueError("invalid frame")
    if (write and not page.writable) or (not write and not page.readable):
        raise PermissionError("page protection")
    return (page.frame << page_bits) + offset


def verify_tag(key: bytes, message: bytes, tag: bytes) -> bool:
    if len(key) < 32:
        raise ValueError("this example requires a 256-bit key")
    # 직접 비교 연산 대신 표준 라이브러리의 비교 함수를 사용한다.
    expected = hmac.digest(key, message, hashlib.sha256)
    return hmac.compare_digest(expected, tag)

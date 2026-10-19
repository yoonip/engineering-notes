import binascii
from fractions import Fraction
import hashlib
import hmac
import itertools
import random
import unittest

from systems_models import (
    DmaBuffer, FrameParser, Page, binary32_value, crc16_x25, encode_frame,
    fixed_multiply, initialize_ram, quantize, signed_word, translate, verify_tag,
)


def reflected(value, bits):
    return int(f"{value:0{bits}b}"[::-1], 2)


def independent_crc(data):
    # 표준 라이브러리의 정방향 다항식 연산과 비트 반전으로 교차 검사한다.
    mirrored = bytes(reflected(b, 8) for b in data)
    return reflected(binascii.crc_hqx(mirrored, 0xFFFF), 16) ^ 0xFFFF


class NumbersTests(unittest.TestCase):
    def test_all_eight_bit_words(self):
        for raw in range(256):
            expected = int.from_bytes(bytes([raw]), "little", signed=True)
            self.assertEqual(signed_word(raw, 8), expected)

    def test_quantization_error_and_saturation(self):
        for numerator in range(-1024, 1025):
            value = Fraction(numerator, 1024)
            code = quantize(value, 8, 6)
            self.assertLessEqual(abs(Fraction(code, 64) - value), Fraction(1, 128))
        self.assertEqual(quantize(Fraction(100), 8, 6), 127)
        self.assertEqual(quantize(Fraction(-100), 8, 6), -128)

    def test_ties_even_and_product(self):
        self.assertEqual(quantize(Fraction(1, 8), 8, 2), 0)
        self.assertEqual(quantize(Fraction(3, 8), 8, 2), 2)
        for a, b in itertools.product(range(-16, 16), repeat=2):
            value = Fraction(a * b, 8)
            floor = value.numerator // value.denominator
            candidates = [floor, floor + 1]
            expected = min(candidates, key=lambda n: (abs(n - value), n % 2))
            expected = max(-16, min(15, expected))
            self.assertEqual(fixed_multiply(a, b, 5, 3), expected)

    def test_float_spacing(self):
        self.assertEqual(binary32_value(2**24 + 1), 2**24)
        self.assertEqual(binary32_value(2**24 + 2), 2**24 + 2)
        self.assertNotEqual(binary32_value(0.1), 0.1)

    def test_bad_formats(self):
        for args in [(Fraction(1), 1, 0), (Fraction(1), 8, 8)]:
            with self.assertRaises(ValueError):
                quantize(*args)
        with self.assertRaises(ValueError):
            fixed_multiply(16, 1, 5, 3)
        with self.assertRaises(ValueError):
            signed_word(256, 8)


class StartupTests(unittest.TestCase):
    def test_copy_zero_and_preserved_bytes(self):
        result = initialize_ram(bytes(range(64)), 32, 10, 4, 6, 16, 8)
        self.assertEqual(result[4:10], bytes(range(10, 16)))
        self.assertEqual(result[16:24], bytes(8))
        self.assertTrue(all(result[i] == 0xA5 for i in list(range(4)) +
                            list(range(10, 16)) + list(range(24, 32))))

    def test_boundary_and_invalid_layout(self):
        self.assertEqual(initialize_ram(b"", 0, 0, 0, 0, 0, 0), b"")
        for args in [(b"ab", 8, 1, 0, 2, 4, 1),
                     (b"ab", 8, 0, 7, 2, 0, 1),
                     (b"ab", 8, 0, 0, 2, 1, 1),
                     (b"ab", 8, -1, 0, 2, 4, 1)]:
            with self.assertRaises(ValueError):
                initialize_ram(*args)


class DmaTests(unittest.TestCase):
    def test_tx_clean_and_exclusive_ownership(self):
        buf = DmaBuffer(4)
        buf.cpu_write(b"abcd")
        self.assertEqual(buf.memory, bytes(4))
        buf.start_tx()
        with self.assertRaises(RuntimeError):
            buf.cpu_write(b"efgh")
        self.assertEqual(buf.finish_tx(), b"abcd")

    def test_rx_invalidates_old_cache(self):
        buf = DmaBuffer(4)
        buf.cpu_write(b"old!")
        buf.start_rx()
        with self.assertRaises(RuntimeError):
            buf.cpu_read()
        with self.assertRaises(RuntimeError):
            buf.acquire_rx()
        buf.finish_rx(b"new!")
        with self.assertRaises(RuntimeError):
            buf.cpu_read()
        buf.acquire_rx()
        self.assertEqual(buf.cpu_read(), b"new!")

    def test_repeated_transfers_and_length(self):
        buf = DmaBuffer(2)
        for i in range(100):
            payload = i.to_bytes(2, "little")
            buf.cpu_write(payload)
            buf.start_tx()
            self.assertEqual(buf.finish_tx(), payload)
            buf.start_rx()
            with self.assertRaises(ValueError):
                buf.finish_rx(b"x")
            buf.finish_rx(payload[::-1])
            buf.acquire_rx()
            self.assertEqual(buf.cpu_read(), payload[::-1])


class ProtocolTests(unittest.TestCase):
    def test_known_vector_and_residue(self):
        self.assertEqual(crc16_x25(b"123456789"), 0x906E)
        codeword = b"123456789" + bytes.fromhex("6e90")
        self.assertEqual(crc16_x25(codeword) ^ 0xFFFF, 0xF0B8)

    def test_independent_reference(self):
        rng = random.Random(31)
        for size in list(range(64)) + [255, 256, 1024]:
            data = rng.randbytes(size)
            self.assertEqual(crc16_x25(data), independent_crc(data))

    def test_all_octets_fragmented_and_empty_frame(self):
        payloads = [b"", bytes(range(256)), b"a\x7d\x7eb"]
        wire = b"noise" + b"".join(map(encode_frame, payloads))
        for step in [1, 2, 3, 7, 257, len(wire)]:
            parser = FrameParser()
            decoded = []
            for start in range(0, len(wire), step):
                decoded.extend(parser.feed(wire[start:start + step]))
            self.assertEqual(decoded, payloads)

    def test_every_single_bit_error(self):
        raw = b"abcdefgh" + crc16_x25(b"abcdefgh").to_bytes(2, "little")
        for bit in range(len(raw) * 8):
            damaged = bytearray(raw)
            damaged[bit // 8] ^= 1 << (bit % 8)
            self.assertNotEqual(crc16_x25(damaged[:-2]),
                                int.from_bytes(damaged[-2:], "little"))

    def test_bounded_memory_recovery_and_escape_abort(self):
        parser = FrameParser(8)
        self.assertEqual(list(parser.feed(b"\x7e" + b"x" * 10000)), [])
        self.assertLessEqual(len(parser.buffer), 10)
        self.assertEqual(list(parser.feed(encode_frame(b"ok", 8))), [b"ok"])
        self.assertEqual(list(parser.feed(b"\x7eabc\x7d\x7e")), [])
        self.assertEqual(list(parser.feed(encode_frame(b"next", 8))), [b"next"])
        with self.assertRaises(ValueError):
            encode_frame(bytes(9), 8)


class MemoryTests(unittest.TestCase):
    def test_offset_alias_and_permissions(self):
        first = {1: Page(9, writable=True), 2: Page(9)}
        second = {1: Page(20)}
        for offset in [0, 1, 2048, 4095]:
            self.assertEqual(translate(4096 + offset, first), 9 * 4096 + offset)
            self.assertEqual(translate(8192 + offset, first), 9 * 4096 + offset)
            self.assertEqual(translate(4096 + offset, second), 20 * 4096 + offset)
        with self.assertRaises(PermissionError):
            translate(8192, first, write=True)
        with self.assertRaises(MemoryError):
            translate(12288, first)

    def test_lost_update_schedule(self):
        # 읽기와 쓰기가 분리된 증가 연산 두 개를 모든 순서로 섞는다.
        outcomes = set()
        for schedule in set(itertools.permutations("AABB")):
            counter, phase, local = 0, {"A": 0, "B": 0}, {}
            for task in schedule:
                if phase[task] == 0:
                    local[task] = counter
                else:
                    counter = local[task] + 1
                phase[task] += 1
            outcomes.add(counter)
        self.assertEqual(outcomes, {1, 2})


class AuthenticationTests(unittest.TestCase):
    def test_rfc4231_case6(self):
        key = b"\xaa" * 131
        message = b"Test Using Larger Than Block-Size Key - Hash Key First"
        expected = bytes.fromhex(
            "60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54")
        self.assertTrue(verify_tag(key, message, expected))

    def test_mutations_and_replay_boundary(self):
        key, message = bytes(range(32)), b"device=7;seq=123;value=40"
        tag = hmac.digest(key, message, hashlib.sha256)
        self.assertTrue(verify_tag(key, message, tag))
        self.assertFalse(verify_tag(key, message + b"0", tag))
        self.assertFalse(verify_tag(bytes(reversed(key)), message, tag))
        self.assertFalse(verify_tag(key, message, tag[:-1]))
        # 같은 정상 메시지는 다시 통과하므로 재전송 공격 방지는 별도 상태가 필요하다.
        self.assertTrue(verify_tag(key, message, tag))
        with self.assertRaises(ValueError):
            verify_tag(b"short", message, tag)


if __name__ == "__main__":
    unittest.main()

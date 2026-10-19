"""Software-only teaching exercise; no board or FrontPanel SDK is accessed.

The invented teaching format is 8 interleaved channels, 16-bit unsigned
little-endian codes. The binary framing is defined by this exercise.
"""

import argparse
import csv
import json
import struct
from pathlib import Path

CHANNELS = 8
FRAME_BYTES = CHANNELS * 2
READ_BYTES = 4096
FRAMES_PER_BLOCK = READ_BYTES // FRAME_BYTES
SCENARIOS = (
    "clean", "byte_swap", "channel_swap", "drop_frame",
    "short_read", "zero_fill", "timeout",
)


def expected_frame(sequence):
    """Top bits distinguish channels; low 12 bits contain a wrapping count."""
    return [channel * 4096 + (sequence % 4096) for channel in range(CHANNELS)]


def encode_frames(first, count):
    return b"".join(struct.pack("<8H", *expected_frame(i))
                    for i in range(first, first + count))


class MockTransport:
    def __init__(self, scenario):
        self.scenario = scenario
        self.next_sequence = 0
        self.block = 0

    def read(self, requested_bytes):
        if requested_bytes % FRAME_BYTES:
            raise ValueError("Teaching frames require a multiple of 16 bytes")
        count = requested_bytes // FRAME_BYTES
        first = self.next_sequence
        self.next_sequence += count
        damaged = self.block == 1 and self.scenario != "clean"
        self.block += 1
        if damaged and self.scenario == "timeout":
            raise TimeoutError("Injected timeout: no real device was contacted")
        payload = bytearray(encode_frames(first, count))
        if damaged and self.scenario == "byte_swap":
            for index in range(0, len(payload), 2):
                payload[index:index + 2] = payload[index:index + 2][::-1]
        elif damaged and self.scenario == "channel_swap":
            for index in range(0, len(payload), FRAME_BYTES):
                payload[index:index + 4] = payload[index + 2:index + 4] + payload[index:index + 2]
        elif damaged and self.scenario == "drop_frame":
            # Remove one complete frame; keep the requested byte count by
            # supplying one extra future frame. The sequence offset persists.
            cut = 11 * FRAME_BYTES
            del payload[cut:cut + FRAME_BYTES]
            payload.extend(encode_frames(self.next_sequence, 1))
            self.next_sequence += 1
        elif damaged and self.scenario == "short_read":
            del payload[-FRAME_BYTES:]
        elif damaged and self.scenario == "zero_fill":
            payload[:] = bytes(len(payload))
        return bytes(payload)


def check_payload(payload, block):
    if len(payload) != READ_BYTES:
        return "FAIL", f"short_read expected={READ_BYTES} actual={len(payload)}"
    first = block * FRAMES_PER_BLOCK
    for offset, actual in enumerate(struct.iter_unpack("<8H", payload)):
        wanted = expected_frame(first + offset)
        for channel, (observed, expected) in enumerate(zip(actual, wanted)):
            if observed != expected:
                return "FAIL", (f"mismatch frame={first + offset} ch={channel} "
                                f"expected=0x{expected:04X} actual=0x{observed:04X}")
    return "PASS", "known pattern matched"


def adc_straight_binary_to_volts(code, vmin, vmax, bits=16):
    """Ideal lower-edge convention; not a calibrated real measurement."""
    if not 0 <= code < (1 << bits):
        raise ValueError("ADC code out of range")
    if vmax <= vmin:
        raise ValueError("Invalid voltage span")
    return vmin + code * (vmax - vmin) / (1 << bits)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("lab_results"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    summary = {}
    for scenario in SCENARIOS:
        transport = MockTransport(scenario)
        scenario_rows = []
        for block in range(4):
            payload = b""
            try:
                payload = transport.read(READ_BYTES)
                status, reason = check_payload(payload, block)
            except TimeoutError as exc:
                status, reason = "FAIL", str(exc)
            row = {
                "scenario": scenario, "block": block,
                "requested_bytes": READ_BYTES, "received_bytes": len(payload),
                "status": status, "reason": reason,
            }
            rows.append(row)
            scenario_rows.append(row)
            if status == "FAIL" and payload:
                (args.out / f"{scenario}_block_{block:02d}.bin").write_bytes(payload)
        failures = sum(row["status"] == "FAIL" for row in scenario_rows)
        summary[scenario] = failures
        print(f"{scenario:12s}: {failures} failing block(s)")

    with (args.out / "blocks.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # This checks the exercise's intended result, not any actual hardware.
    assert summary["clean"] == 0
    assert all(summary[scenario] > 0 for scenario in SCENARIOS if scenario != "clean")
    print("\nIdeal 16-bit straight-binary example, configured span -5.12..+5.12 V:")
    for code in (0, 32768, 65535):
        voltage = adc_straight_binary_to_volts(code, -5.12, 5.12)
        print(f"0x{code:04X}: {voltage:+.8f} V")
    metadata = {
        "mode": "SOFTWARE_SIMULATION_ONLY",
        "format": "invented 8 channels x uint16 little-endian per frame",
        "read_bytes": READ_BYTES,
        "real_hardware_validated": False,
        "summary_failing_blocks": summary,
    }
    (args.out / "manifest.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved teaching results: {args.out.resolve()}")


if __name__ == "__main__":
    main()

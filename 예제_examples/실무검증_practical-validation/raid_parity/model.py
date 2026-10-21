"""One bounded XOR stripe in host files; not Linux md or a disk driver."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import sys

MEMBERS = ("D0.bin", "D1.bin", "P.bin")
OLD = (bytes.fromhex("10111213"), bytes.fromhex("a0a1a2a3"), bytes.fromhex("b0b0b0b0"))
NEW = (bytes.fromhex("20212223"), bytes.fromhex("a0a1a2a3"), bytes.fromhex("80808080"))
HEADER = struct.Struct("<4sII12s")
MUTATIONS = ("none", "trust-dirty", "replay-incomplete", "accept-two-missing", "skip-generation")


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def xor(left, right):
    require(len(left) == len(right) == 4, "MEMBER_LENGTH")
    return bytes(a ^ b for a, b in zip(left, right))


def encode_meta(generation, dirty=False):
    require(type(generation) is int and 1 <= generation <= 65534, "GENERATION")
    require(type(dirty) is bool and (not dirty or generation < 65534), "GENERATION_PENDING")
    return (json.dumps({"format": "XOR1", "stripe": 0, "generation": generation,
                        "pending": generation + 1 if dirty else None, "dirty": dirty},
                       sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def write_sync(path, data, mode="xb"):
    with path.open(mode) as stream:
        require(stream.write(data) == len(data), "SHORT_WRITE")
        stream.flush()
        os.fsync(stream.fileno())


def redo_record(generation=8, values=NEW, stripe=0):
    require(len(values) == 3 and all(len(v) == 4 for v in values), "REDO_PAYLOAD")
    header = HEADER.pack(b"RDL1", stripe, generation, b"".join(values))
    return header + hashlib.sha256(header).digest()


def decode_redo(raw, expected, mutation="none"):
    if mutation == "replay-incomplete" and len(raw) == HEADER.size:
        header = raw
    else:
        require(len(raw) == HEADER.size + 32, "REDO_LENGTH")
        header = raw[:HEADER.size]
        require(hashlib.sha256(header).digest() == raw[HEADER.size:], "REDO_DIGEST")
    magic, stripe, generation, payload = HEADER.unpack(header)
    require(magic == b"RDL1" and stripe == 0, "REDO_IDENTITY")
    require(1 <= generation <= 65534, "REDO_GENERATION_RANGE")
    if mutation != "skip-generation":
        require(generation == expected, "REDO_GENERATION")
    values = tuple(payload[i:i + 4] for i in (0, 4, 8))
    require(xor(values[0], values[1]) == values[2], "REDO_PARITY")
    return generation, values


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "DUPLICATE_META_KEY")
        result[key] = value
    return result


def load(directory):
    require(directory.is_dir() and not directory.is_symlink(), "SOURCE_DIRECTORY")
    paths = list(directory.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in paths), "SOURCE_ENTRY")
    require({p.name for p in paths} <= set(MEMBERS) | {"meta.json", "redo.bin"}, "SOURCE_NAMES")
    require((directory / "meta.json").is_file(), "META_MISSING")
    require((directory / "meta.json").stat().st_size <= 512, "META_LENGTH")
    meta = json.loads((directory / "meta.json").read_text("ascii"), object_pairs_hook=unique_pairs)
    require(type(meta) is dict and set(meta) == {"format", "stripe", "generation", "pending", "dirty"}, "META_FIELDS")
    require(meta["format"] == "XOR1" and type(meta["stripe"]) is int and meta["stripe"] == 0, "META_IDENTITY")
    require(type(meta["generation"]) is int and 1 <= meta["generation"] <= 65534, "META_GENERATION")
    require(type(meta["dirty"]) is bool, "META_DIRTY")
    if meta["dirty"]:
        require(type(meta["pending"]) is int and meta["pending"] == meta["generation"] + 1 and meta["pending"] <= 65534, "META_PENDING")
    else:
        require(meta["pending"] is None, "META_PENDING")
    values = []
    for name in MEMBERS:
        path = directory / name
        if not path.exists():
            values.append(None)
        else:
            require(path.stat().st_size == 4, "MEMBER_LENGTH")
            values.append(path.read_bytes())
    log = directory / "redo.bin"
    require(not log.exists() or log.stat().st_size <= 56, "REDO_LENGTH")
    return meta, tuple(values), log.read_bytes() if log.exists() else None


def snapshot(directory):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir()}


def inspect(directory):
    meta, values, raw = load(directory)
    missing = [MEMBERS[i] for i, value in enumerate(values) if value is None]
    parity = None if missing else xor(values[0], values[1]) == values[2]
    return {"generation": meta["generation"], "dirty": meta["dirty"], "pending": meta["pending"],
            "members": [v.hex() if v is not None else None for v in values], "missing": missing,
            "parity_matches": parity, "redo_bytes": len(raw) if raw is not None else None,
            "status": "NEEDS_RECOVERY_DATA" if meta["dirty"] else "CLEAN_MARKER"}


def reconstruct(values, mutation="none"):
    values = list(values)
    missing = [i for i, value in enumerate(values) if value is None]
    if len(missing) >= 2 and mutation == "accept-two-missing":
        values[missing.pop(0)] = b"\x00" * 4
    require(len(missing) <= 1, "TOO_MANY_MISSING")
    if missing:
        index = missing[0]
        present = [value for value in values if value is not None]
        require(len(present) == 2, "TOO_MANY_MISSING")
        values[index] = xor(present[0], present[1])
    require(xor(values[0], values[1]) == values[2], "PARITY_MISMATCH")
    return tuple(values)


def recover(source, output, mutation="none"):
    require(not output.exists() and not output.is_symlink(), "OUTPUT_EXISTS")
    require(source.resolve() != output.resolve() and source.resolve() not in output.resolve().parents, "OUTPUT_LOCATION")
    meta, values, raw = load(source)
    before = snapshot(source)
    missing = sum(value is None for value in values)
    require(missing <= 1 or mutation == "accept-two-missing", "TOO_MANY_MISSING")
    generation = meta["generation"]
    method = "CLEAN_XOR"
    if meta["dirty"] and mutation != "trust-dirty":
        require(raw is not None, "NEEDS_RECOVERY_DATA")
        generation, values = decode_redo(raw, meta["pending"], mutation)
        method = "FULL_STRIPE_REDO"
    else:
        values = reconstruct(values, mutation)
        if raw is not None and not meta["dirty"]:
            _, recorded = decode_redo(raw, generation, mutation)
            require(values == recorded, "CLEAN_REDO_MISMATCH")
    require(snapshot(source) == before, "SOURCE_CHANGED")
    output.mkdir()
    for name, value in zip(MEMBERS, values):
        write_sync(output / name, value)
    if method == "FULL_STRIPE_REDO" or (raw is not None and not meta["dirty"]):
        write_sync(output / "redo.bin", redo_record(generation, values))
    write_sync(output / "meta.json", encode_meta(generation))
    checked_meta, checked_values, _ = load(output)
    require(checked_values == values and checked_meta["generation"] == generation, "COPY_READBACK")
    require(snapshot(source) == before, "SOURCE_CHANGED")
    return {"status": "RECOVERED", "method": method, "generation": generation,
            "members": [v.hex() for v in values], "source_sha256": before,
            "output_sha256": snapshot(output)}


def seed(directory):
    require(not directory.exists(), "OUTPUT_EXISTS")
    directory.mkdir()
    for name, value in zip(MEMBERS, OLD):
        write_sync(directory / name, value)
    write_sync(directory / "meta.json", encode_meta(7))
    return inspect(directory)


def interrupt(directory, order, stop, journal):
    meta, values, raw = load(directory)
    require(not meta["dirty"] and meta["generation"] == 7 and values == OLD and raw is None, "SEED_REQUIRED")
    write_sync(directory / "meta.json", encode_meta(7, True), "wb")
    if stop == "dirty":
        return inspect(directory)
    if journal != "none":
        log = redo_record()
        write_sync(directory / "redo.bin", log if journal == "full" else log[:24])
    if stop == "log":
        return inspect(directory)
    sequence = ((0, "D0.bin"), (2, "P.bin")) if order == "data-first" else ((2, "P.bin"), (0, "D0.bin"))
    for number, (index, name) in enumerate(sequence, 1):
        write_sync(directory / name, NEW[index], "wb")
        if stop == f"member{number}":
            return inspect(directory)
    write_sync(directory / "meta.json", encode_meta(8), "wb")
    return inspect(directory)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("seed", "interrupt", "inspect", "recover", "unsafe-d1"))
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--order", choices=("data-first", "parity-first"), default="data-first")
    parser.add_argument("--stop", choices=("dirty", "log", "member1", "member2", "clean"), default="member1")
    parser.add_argument("--journal", choices=("full", "incomplete", "none"), default="full")
    parser.add_argument("--mutation", choices=MUTATIONS, default="none")
    args = parser.parse_args()
    try:
        if args.operation == "seed":
            result = seed(args.directory)
        elif args.operation == "interrupt":
            result = interrupt(args.directory, args.order, args.stop, args.journal)
        elif args.operation == "inspect":
            result = inspect(args.directory)
        elif args.operation == "unsafe-d1":
            _, values, _ = load(args.directory)
            require(values[0] is not None and values[2] is not None, "D0_P_REQUIRED")
            result = {"status": "UNTRUSTED_DIAGNOSTIC", "computed_d1": xor(values[0], values[2]).hex()}
        else:
            require(args.output is not None, "OUTPUT_REQUIRED")
            result = recover(args.directory, args.output, args.mutation)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, OSError, UnicodeError, struct.error) as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error)}, sort_keys=True))
        return 3


if __name__ == "__main__":
    sys.exit(main())

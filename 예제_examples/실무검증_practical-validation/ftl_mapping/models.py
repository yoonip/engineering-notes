"""실제 파일의 DATA/ERASE 사건과 매핑 저널로 작은 FTL 상태를 재구성합니다."""
import argparse
import json
import os  # 선택 prefix 동기화 뒤 자식 프로세스만 명시 종료합니다.
from pathlib import Path
import struct  # native padding 대신 기록 크기와 little endian을 고정합니다.
import zlib

PAGES, LPNS, BLOCK_PAGES, LIMIT = 12, 3, 3, 65536
NONE = 0xFFFFFFFF
PHYSICAL = struct.Struct("<4sBBHIIII4s")  # 내용 28바이트와 뒤 CRC4로 총32입니다.
MAPPING = struct.Struct("<4sBBH9I")  # 내용44바이트와 뒤 CRC4로 총48입니다.
CRC = struct.Struct("<I")
MUTATIONS = ("none", "publish-first", "erase-old-first", "wrong-page-identity", "stale-gc", "ignore-trim")


class FtlError(ValueError):
    """형식·소유권·순서·용량 계약을 거부합니다."""


def require(condition, reason):
    if not condition:  # -O에서 제거되는 assert 대신 명시적 예외를 사용합니다.
        raise FtlError(reason)


def integer(value, low, high, reason="INTEGER_RANGE"):
    require(type(value) is int and low <= value <= high, reason)
    return value  # bool을 정수 주소·번호로 받지 않습니다.


def payload(value):
    require(type(value) is str and len(value) == 8, "DATA_HEX")
    try:
        raw = bytes.fromhex(value)
    except ValueError:
        raise FtlError("DATA_HEX") from None
    require(len(raw) == 4, "DATA_HEX")
    return raw


def protected(content):
    return content + CRC.pack(zlib.crc32(content))


def physical_record(kind, sequence, address, lpn=NONE, version=0, data=bytes(4)):
    integer(sequence, 1, 65535, "PHYSICAL_SEQUENCE_RANGE")
    require(kind in (1, 2), "PHYSICAL_KIND")
    integer(address, 0, 11 if kind == 1 else 3, "PHYSICAL_ADDRESS")
    if kind == 1:
        integer(lpn, 0, 2, "LPN_RANGE")
        integer(version, 1, 65535, "VERSION_RANGE")
    else:
        require(lpn == NONE and version == 0 and data == bytes(4), "ERASE_FIELDS")
    require(type(data) is bytes and len(data) == 4, "DATA_BYTES")
    return protected(PHYSICAL.pack(b"PAGE", 1, kind, 0, sequence, address, lpn, version, data))


def token(state, lpn):
    entry = state["entries"][lpn]
    return [state["versions"][lpn], NONE if entry is None else entry["ppn"],
            0 if entry is None else entry["incarnation"]]


def mapping_record(kind, sequence, lpn, version, ppn, incarnation, base, page_crc):
    integer(sequence, 1, 65535, "MAP_SEQUENCE_RANGE")
    integer(lpn, 0, 2, "LPN_RANGE")
    require(kind in (1, 2, 3), "MAP_KIND")
    return protected(MAPPING.pack(b"L2P1", 1, kind, 0, sequence, lpn, version,
                                  ppn, incarnation, *base, page_crc))


def fixed_records(raw, magic, size):
    require(type(raw) is bytes and len(raw) <= LIMIT, "FILE_SIZE")
    require(raw.startswith(magic), "FILE_MAGIC")
    body = raw[4:]
    full = len(body) // size
    records = []
    for index in range(full):
        record = body[index * size:(index + 1) * size]
        require(CRC.unpack(record[-4:])[0] == zlib.crc32(record[:-4]), "RECORD_CRC")
        records.append(record)
    return records, len(body) % size  # 부족한 마지막 고정 기록만 보류합니다.


def decode_physical(raw):
    records, tail = fixed_records(raw, b"DAT1", 32)
    pages = {}
    for expected, record in enumerate(records, 1):
        magic, revision, kind, reserved, sequence, address, lpn, version, data = PHYSICAL.unpack(record[:-4])
        require((magic, revision, reserved) == (b"PAGE", 1, 0), "PHYSICAL_HEADER")
        require(sequence == expected, "PHYSICAL_SEQUENCE")
        # 재부호화로 필드의 범위와 ERASE 특수값도 확인합니다.
        require(physical_record(kind, sequence, address, lpn, version, data) == record, "PHYSICAL_FIELDS")
        if kind == 1:
            require(address not in pages, "PROGRAM_OCCUPIED_PAGE")
            pages[address] = {"lpn": lpn, "version": version, "incarnation": sequence,
                              "hex": data.hex(), "crc": CRC.unpack(record[-4:])[0]}
        else:
            for ppn in range(address * BLOCK_PAGES, (address + 1) * BLOCK_PAGES):
                pages.pop(ppn, None)  # ERASE 사건은 블록의 세 주소를 free 상태로 만듭니다.
    return pages, len(records), tail


def decode_mapping(raw, mutation="none"):
    records, tail = fixed_records(raw, b"MAP1", 48)
    state = {"entries": [None] * LPNS, "versions": [0] * LPNS}
    for expected, record in enumerate(records, 1):
        fields = MAPPING.unpack(record[:-4])
        magic, revision, kind, reserved = fields[:4]
        sequence, lpn, version, ppn, incarnation, bv, bp, bi, page_crc = fields[4:]
        require((magic, revision, reserved) == (b"L2P1", 1, 0), "MAP_HEADER")
        require(sequence == expected and sequence <= 65535, "MAP_SEQUENCE")
        integer(lpn, 0, 2, "LPN_RANGE")
        integer(version, 1, 65535, "VERSION_RANGE")
        require(kind in (1, 2, 3), "MAP_KIND")
        if not (kind == 2 and mutation == "stale-gc"):
            require([bv, bp, bi] == token(state, lpn), "MAP_BASE_CHANGED")
        require(version == bv + (0 if kind == 2 else 1), "LOGICAL_VERSION")
        if kind == 3:
            require((ppn, incarnation, page_crc) == (NONE, 0, 0), "TRIM_FIELDS")
            if mutation == "ignore-trim":
                continue  # 의도적 오류: 확정 tombstone을 무시해 이전 자료를 다시 노출합니다.
            entry = None
        else:
            integer(ppn, 0, 11, "PPN_RANGE")
            integer(incarnation, 1, 65535, "INCARNATION_RANGE")
            if kind == 2:
                require(bp != NONE and (ppn, incarnation) != (bp, bi), "MOVE_FIELDS")
            entry = {"ppn": ppn, "incarnation": incarnation, "version": version, "crc": page_crc}
        state["entries"][lpn], state["versions"][lpn] = entry, version
    return state, len(records), tail


def read_limited(path):
    with path.open("rb") as stream:
        return stream.read(LIMIT + 1)


def read_state(root, mutation="none"):
    require(mutation in MUTATIONS, "MUTATION")
    pages, data_count, data_tail = decode_physical(read_limited(root / "physical.log"))
    state, map_count, map_tail = decode_mapping(read_limited(root / "mapping.log"), mutation)
    used = set()
    for lpn, entry in enumerate(state["entries"]):
        if entry is None:
            continue
        ppn = entry["ppn"]
        require(ppn not in used, "DUPLICATE_LIVE_PPN")
        used.add(ppn)
        require(ppn in pages, "MAPPED_PAGE_MISSING")
        page = pages[ppn]
        require((page["lpn"], page["version"], page["incarnation"]) ==
                (lpn, entry["version"], entry["incarnation"]), "PAGE_IDENTITY")
        require(page["crc"] == entry["crc"], "PAGE_MAP_CRC")
    state.update(pages=pages, data_records=data_count, map_records=map_count,
                 tails={"data": data_tail, "map": map_tail})
    return state


def summary(state):
    entries, pages = state["entries"], state["pages"]
    valid = sum(entry is not None for entry in entries)
    return {"values": [None if entry is None else pages[entry["ppn"]]["hex"] for entry in entries],
            "versions": state["versions"], "ppns": [None if entry is None else entry["ppn"] for entry in entries],
            "incarnations": [None if entry is None else entry["incarnation"] for entry in entries],
            "valid": valid, "stale": len(pages) - valid, "free": PAGES - len(pages),
            "data_records": state["data_records"], "map_records": state["map_records"], "tails": state["tails"]}


def ready(root, mutation="none"):
    state = read_state(root, mutation)
    require(not any(state["tails"].values()), "TAIL_NEEDS_REPAIR")
    return state


def append_record(root, name, record, stage, selected, cut):
    chosen = stage == selected
    integer(cut, 0, len(record), "CUT_RANGE") if chosen else None
    prefix = record[:cut] if chosen else record
    path = root / name
    require(path.stat().st_size + len(prefix) <= LIMIT, "FILE_FULL")
    with path.open("ab") as stream:
        require(stream.write(prefix) == len(prefix), "SHORT_WRITE")
        stream.flush()
        os.fsync(stream.fileno())
    if chosen:
        print(json.dumps({"status": "CUT", "stage": stage, "prefix": cut}), flush=True)
        os._exit(23)  # 명시적 자식 종료이며 OS/장치 전원 차단이 아닙니다.


def free_page(state, outside=None):
    candidates = [ppn for ppn in range(PAGES) if ppn not in state["pages"] and
                  (outside is None or ppn // BLOCK_PAGES != outside)]
    require(bool(candidates), "NO_FREE_PAGE")
    return candidates[0]


def erase_block(root, block, stage="none", cut=0, force=False, mutation="none"):
    integer(block, 0, 3, "BLOCK_RANGE")
    require(stage in ("none", "erase"), "ERASE_STAGE")
    state = ready(root, mutation)
    if not force:
        require(all(entry is None or entry["ppn"] // BLOCK_PAGES != block for entry in state["entries"]), "ERASE_LIVE_BLOCK")
    record = physical_record(2, state["data_records"] + 1, block)
    append_record(root, "physical.log", record, "erase", stage, cut)


def seed(root, values):
    require(type(values) is list and len(values) == LPNS, "SEED_VALUES")
    data = [payload(value) for value in values]
    root.mkdir(parents=True, exist_ok=False)
    for name, magic in (("physical.log", b"DAT1"), ("mapping.log", b"MAP1")):
        with (root / name).open("xb") as stream:
            stream.write(magic)
            stream.flush()
            os.fsync(stream.fileno())
    for lpn, ppn in enumerate((0, 3, 6)):
        physical = physical_record(1, lpn + 1, ppn, lpn, 1, data[lpn])
        append_record(root, "physical.log", physical, "data", "none", 0)
        mapping = mapping_record(1, lpn + 1, lpn, 1, ppn, lpn + 1, [0, NONE, 0], CRC.unpack(physical[-4:])[0])
        append_record(root, "mapping.log", mapping, "map", "none", 0)


def write(root, lpn, value, stage="none", cut=0, mutation="none"):
    integer(lpn, 0, 2, "LPN_RANGE")
    data = payload(value)
    require(stage in ("none", "data", "map"), "WRITE_STAGE")
    before = ready(root, mutation)
    base = token(before, lpn)
    version = integer(base[0] + 1, 1, 65535, "VERSION_RANGE")
    if mutation == "erase-old-first" and before["entries"][lpn] is not None:
        erase_block(root, before["entries"][lpn]["ppn"] // BLOCK_PAGES, force=True, mutation=mutation)
        pages, count, tail = decode_physical(read_limited(root / "physical.log"))
        before.update(pages=pages, data_records=count)
    require(PAGES - len(before["pages"]) >= 2, "GC_RESERVE_REQUIRED")  # 일반 쓰기는 임시 페이지 하나를 남깁니다.
    ppn, incarnation = free_page(before), before["data_records"] + 1
    physical = physical_record(1, incarnation, ppn, (lpn + 1) % LPNS if mutation == "wrong-page-identity" else lpn, version, data)
    mapping = mapping_record(1, before["map_records"] + 1, lpn, version, ppn, incarnation, base, CRC.unpack(physical[-4:])[0])
    if mutation == "publish-first":
        append_record(root, "mapping.log", mapping, "map", stage, cut)
    append_record(root, "physical.log", physical, "data", stage, cut)
    pages, _, _ = decode_physical(read_limited(root / "physical.log"))
    page = pages[ppn]
    require((page["lpn"], page["version"], page["hex"]) == (lpn, version, value.lower()), "WRITE_READBACK_IDENTITY")
    if mutation != "publish-first":
        append_record(root, "mapping.log", mapping, "map", stage, cut)


def trim(root, lpn, stage="none", cut=0, mutation="none"):
    integer(lpn, 0, 2, "LPN_RANGE")
    require(stage in ("none", "map"), "TRIM_STAGE")
    state = ready(root, mutation)
    base = token(state, lpn)
    version = integer(base[0] + 1, 1, 65535, "VERSION_RANGE")
    record = mapping_record(3, state["map_records"] + 1, lpn, version, NONE, 0, base, 0)
    append_record(root, "mapping.log", record, "map", stage, cut)


def plan_gc(root, block, job_path):
    integer(block, 0, 3, "BLOCK_RANGE")
    state = ready(root)
    live = [{"lpn": lpn, "token": token(state, lpn), "hex": state["pages"][entry["ppn"]]["hex"], "crc": entry["crc"]}
            for lpn, entry in enumerate(state["entries"]) if entry is not None and entry["ppn"] // BLOCK_PAGES == block]
    capacity = sum(ppn not in state["pages"] and ppn // BLOCK_PAGES != block for ppn in range(PAGES))
    require(capacity >= len(live), "NO_GC_TEMP_SPACE")
    with job_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"block": block, "live": live}, stream, separators=(",", ":"))
        stream.flush()
        os.fsync(stream.fileno())
    return {"block": block, "live_pages": len(live), "temporary_pages_available": capacity}


def finish_gc(root, job_path, stage="none", cut=0, mutation="none"):
    require(stage in ("none", "data", "map", "erase"), "GC_STAGE")
    job = json.loads(job_path.read_text(encoding="utf-8"))
    require(type(job) is dict and set(job) == {"block", "live"}, "JOB_KEYS")
    block = integer(job["block"], 0, 3, "BLOCK_RANGE")
    require(type(job["live"]) is list and len(job["live"]) <= BLOCK_PAGES, "JOB_LIVE")
    state, seen = ready(root, mutation), set()
    for item in job["live"]:
        require(type(item) is dict and set(item) == {"lpn", "token", "hex", "crc"}, "JOB_ITEM")
        lpn = integer(item["lpn"], 0, 2, "LPN_RANGE")
        require(lpn not in seen, "JOB_DUPLICATE_LPN")
        seen.add(lpn)
        require(type(item["token"]) is list and len(item["token"]) == 3, "JOB_TOKEN")
        version, ppn, incarnation = item["token"]
        integer(version, 1, 65535, "VERSION_RANGE")
        integer(ppn, 0, 11, "PPN_RANGE")
        integer(incarnation, 1, 65535, "INCARNATION_RANGE")
        require(ppn // BLOCK_PAGES == block, "JOB_SOURCE_BLOCK")
        payload(item["hex"])
        integer(item["crc"], 0, NONE, "PAGE_CRC_RANGE")
        if mutation != "stale-gc":
            require(item["token"] == token(state, lpn), "STALE_GC_SNAPSHOT")
        source = state["pages"].get(ppn)
        require(source is not None and (source["lpn"], source["version"], source["incarnation"], source["hex"], source["crc"]) ==
                (lpn, version, incarnation, item["hex"], item["crc"]), "GC_SOURCE_CHANGED")
    capacity = sum(ppn not in state["pages"] and ppn // BLOCK_PAGES != block for ppn in range(PAGES))
    require(capacity >= len(job["live"]), "NO_GC_TEMP_SPACE")
    require(bool(job["live"]) or stage in ("none", "erase"), "NO_GC_COPY_STAGE")
    for item in job["live"]:
        state = ready(root, mutation)
        ppn, incarnation = free_page(state, outside=block), state["data_records"] + 1
        lpn, version = item["lpn"], item["token"][0]
        physical = physical_record(1, incarnation, ppn, lpn, version, payload(item["hex"]))
        append_record(root, "physical.log", physical, "data", stage, cut)
        copied, _, _ = decode_physical(read_limited(root / "physical.log"))
        require(copied[ppn]["hex"] == item["hex"], "GC_READBACK")
        mapping = mapping_record(2, state["map_records"] + 1, lpn, version, ppn, incarnation, item["token"], CRC.unpack(physical[-4:])[0])
        append_record(root, "mapping.log", mapping, "map", stage, cut)
    erase_block(root, block, stage, cut, mutation=mutation)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--action", choices=("seed", "write", "trim", "plan-gc", "finish-gc", "inspect", "erase-empty"), required=True)
    parser.add_argument("--lpn", type=int, default=0)
    parser.add_argument("--data", default="aaaa0001")
    parser.add_argument("--block", type=int, default=0)
    parser.add_argument("--job", type=Path)
    parser.add_argument("--stage", choices=("none", "data", "map", "erase"), default="none")
    parser.add_argument("--cut", type=int, default=0)
    parser.add_argument("--mutation", choices=MUTATIONS, default="none")
    args = parser.parse_args()
    try:
        if args.action == "seed":
            fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
            seed(args.root, fixture["seed_values"])
            result = {"status": "SEEDED"}
        elif args.action == "write":
            write(args.root, args.lpn, args.data, args.stage, args.cut, args.mutation)
            result = {"status": "WRITTEN"}
        elif args.action == "trim":
            trim(args.root, args.lpn, args.stage, args.cut, args.mutation)
            result = {"status": "TRIMMED"}
        elif args.action == "plan-gc":
            require(args.job is not None, "JOB_PATH")
            result = {"status": "PLANNED", **plan_gc(args.root, args.block, args.job)}
        elif args.action == "finish-gc":
            require(args.job is not None, "JOB_PATH")
            finish_gc(args.root, args.job, args.stage, args.cut, args.mutation)
            result = {"status": "COLLECTED"}
        elif args.action == "erase-empty":
            erase_block(args.root, args.block, args.stage, args.cut, mutation=args.mutation)
            result = {"status": "ERASED"}
        else:
            result = {"status": "RECOVERED", **summary(read_state(args.root, args.mutation))}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (FtlError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc), "exception": type(exc).__name__}, ensure_ascii=False))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

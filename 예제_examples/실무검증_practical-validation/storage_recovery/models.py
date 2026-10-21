"""자체 DATA/COMMIT 저널을 실제 파일로 기록하고 새 프로세스에서 읽습니다."""
import argparse  # 명령행에서 작업·경로·중단 위치를 받습니다.
import hashlib
import json
import os  # flush 뒤 fsync와 명시적인 자식 종료에 사용합니다.
from pathlib import Path
import struct  # 정수와 바이트의 크기·순서를 명시합니다.
import sys
import zlib  # CRC32는 우발적 변경 검출용이며 인증이 아닙니다.

FILE_MAGIC = b"JNL1"
HEADER = struct.Struct("<4sBBHI")  # <는 little endian, H는 2바이트, I는 4바이트입니다.
U32 = struct.Struct("<I")
MAX_PAYLOAD, MAX_LOG, MAX_SEQ = 128, 65536, 65535
MUTATIONS = ("none", "apply-uncommitted", "ignore-crc", "ignore-sequence", "commit-first")


class JournalError(ValueError):
    """파일 형식·기록 순서·입력 계약을 만족하지 않습니다."""


def require(condition, reason):
    if not condition:  # 명시적 예외이므로 Python -O에서도 남습니다.
        raise JournalError(reason)


def integer(value, low, high):
    require(type(value) is int and low <= value <= high, f"INTEGER_{low}_{high}")
    return value  # bool은 int의 하위 형이지만 이 입력에서는 받지 않습니다.


def values_bytes(values):
    require(type(values) is dict and set(values) == {"credit", "stock"}, "VALUE_KEYS")
    for value in values.values():  # 두 필드 모두 고정한 정수 범위를 검사합니다.
        integer(value, 0, 1000)
    return json.dumps(values, sort_keys=True, separators=(",", ":")).encode("ascii")


def frame(kind, seq, payload):
    integer(kind, 1, 2)
    integer(seq, 1, MAX_SEQ)
    require(type(payload) is bytes and 1 <= len(payload) <= MAX_PAYLOAD, "PAYLOAD_LENGTH")
    require(kind != 2 or len(payload) == 4, "COMMIT_LENGTH")
    header = HEADER.pack(b"REC1", 1, kind, len(payload), seq)
    content = header + payload  # +는 header와 payload의 bytes를 연결합니다.
    return content + U32.pack(zlib.crc32(content))


def transaction(seq, values):
    data = frame(1, seq, values_bytes(values))
    commit = frame(2, seq, data[-4:])  # COMMIT payload에 DATA의 CRC 값을 넣어 서로 묶습니다.
    return data, commit


def recover_bytes(raw, mutation="none"):
    require(type(raw) is bytes and len(raw) <= MAX_LOG, "LOG_SIZE")
    require(raw.startswith(FILE_MAGIC), "FILE_HEADER")
    require(mutation in MUTATIONS, "MUTATION")
    state, sequence, pending = {}, 0, None  # {}는 복구 상태, None은 미확정 DATA가 없다는 표시입니다.
    offset = committed_end = len(FILE_MAGIC)
    commits, tail_kind = [], "CLEAN"
    while offset < len(raw):
        if len(raw) - offset < HEADER.size:
            tail_kind = "INCOMPLETE_FRAME"  # 온전한 header조차 없는 끝부분입니다.
            break
        magic, version, kind, length, seq = HEADER.unpack_from(raw, offset)
        require(magic == b"REC1", "FRAME_MAGIC")
        require(version == 1, "FRAME_VERSION")
        require(kind in (1, 2), "FRAME_KIND")
        integer(seq, 1, MAX_SEQ)
        integer(length, 1, MAX_PAYLOAD)
        require(kind != 2 or length == 4, "COMMIT_LENGTH")
        end = offset + HEADER.size + length + U32.size
        if end > len(raw):
            tail_kind = "INCOMPLETE_FRAME"  # 선언된 마지막 frame의 나머지가 없습니다.
            break
        payload = raw[offset + HEADER.size:end - U32.size]
        stored_crc = U32.unpack_from(raw, end - U32.size)[0]
        actual_crc = zlib.crc32(raw[offset:end - U32.size])
        if mutation != "ignore-crc":
            require(stored_crc == actual_crc, "FRAME_CRC")
        if kind == 1:
            require(pending is None, "SECOND_DATA_BEFORE_COMMIT")
            if mutation != "ignore-sequence":
                require(seq == sequence + 1, "DATA_SEQUENCE")
            try:
                values = json.loads(payload.decode("ascii"))
            except (UnicodeError, ValueError):
                raise JournalError("DATA_JSON") from None
            require(values_bytes(values) == payload, "DATA_CANONICAL")
            pending = (seq, values, actual_crc)
            if mutation == "apply-uncommitted":
                state.update(values)  # 의도적 오류: COMMIT을 받기 전에 응용 값을 바꿉니다.
        else:
            require(pending is not None, "COMMIT_WITHOUT_DATA")
            require(seq == pending[0], "COMMIT_SEQUENCE")
            require(payload == U32.pack(pending[2]), "COMMIT_BINDING")
            state.update(pending[1])  # 같은 seq·DATA CRC의 COMMIT을 확인한 뒤에만 게시합니다.
            sequence, pending, committed_end = seq, None, end
            commits.append(seq)  # append는 확정된 트랜잭션 번호를 리스트 끝에 붙입니다.
        offset = end
    if tail_kind == "CLEAN" and pending is not None:
        tail_kind = "UNCOMMITTED_DATA"
    return {"state": state, "sequence": sequence, "commits": commits,
            "committed_end": committed_end, "tail_kind": tail_kind,
            "ignored_bytes": len(raw) - committed_end, "file_bytes": len(raw)}


def read_journal(root, mutation="none"):
    with (root / "journal.bin").open("rb") as stream:  # with는 파일을 닫는 범위를 정합니다.
        raw = stream.read(MAX_LOG + 1)  # 상한보다 한 바이트만 더 읽어 과대 파일을 거부합니다.
    result = recover_bytes(raw, mutation)
    return raw, result


def synced_write(path, raw, mode):
    with path.open(mode) as stream:
        require(stream.write(raw) == len(raw), "SHORT_WRITE")
        stream.flush()  # Python의 사용자 공간 출력 버퍼를 비웁니다.
        os.fsync(stream.fileno())  # 이 호스트의 동기화 요청이며 실제 전원 손실 시험은 아닙니다.


def seed(root, request):
    require(type(request) is dict and set(request) == {"seq", "values"}, "REQUEST_KEYS")
    require(request["seq"] == 1 and type(request["seq"]) is int, "SEED_SEQUENCE")
    data, commit = transaction(request["seq"], request["values"])
    root.mkdir(parents=True, exist_ok=False)
    synced_write(root / "journal.bin", FILE_MAGIC + data + commit, "xb")


def append(root, request, cut=-1, mutation="none"):
    require(type(request) is dict and set(request) == {"seq", "values"}, "REQUEST_KEYS")
    raw, old = read_journal(root)  # writer의 시작 검사에는 오류 주입용 reader를 사용하지 않습니다.
    require(old["tail_kind"] == "CLEAN", "TAIL_NEEDS_REPAIR")
    require(type(request["seq"]) is int and request["seq"] == old["sequence"] + 1, "APPEND_SEQUENCE")
    data, commit = transaction(request["seq"], request["values"])
    batch = commit + data if mutation == "commit-first" else data + commit
    require(len(raw) + len(batch) <= MAX_LOG, "LOG_FULL")
    integer(cut, -1, len(batch))
    prefix = batch if cut == -1 else batch[:cut]  # [:cut]은 끝 인덱스를 제외한 prefix입니다.
    synced_write(root / "journal.bin", prefix, "ab")
    result = {"status": "APPENDED" if cut == -1 else "CUT", "appended_bytes": len(prefix)}
    if cut != -1:
        print(json.dumps(result), flush=True)
        os._exit(23)  # fsync한 선택 prefix 뒤 자식만 명시 종료합니다.
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--action", choices=("seed", "append", "recover"), required=True)
    parser.add_argument("--cut", type=int, default=-1)
    parser.add_argument("--mutation", choices=MUTATIONS, default="none")
    args = parser.parse_args()
    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        if args.action == "seed":
            seed(args.root, fixture["seed"])
            result = {"status": "SEEDED"}
        elif args.action == "append":
            result = append(args.root, fixture["update"], args.cut, args.mutation)
        else:
            raw, recovered = read_journal(args.root, args.mutation)
            result = {"status": "RECOVERED", **recovered, "journal_sha256": hashlib.sha256(raw).hexdigest()}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (JournalError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "REJECTED", "exception": type(exc).__name__, "reason": str(exc)}, ensure_ascii=False))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

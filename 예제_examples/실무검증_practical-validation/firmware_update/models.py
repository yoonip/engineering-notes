"""파일 두 슬롯과 CRC 메타데이터 두 부를 사용하는 업데이트 교육 모형입니다."""
import argparse  # 명령행으로 별도 프로세스의 동작을 고릅니다.
import copy  # 이전 상태와 새 상태의 사전이 섞이지 않게 복사합니다.
import hashlib  # SHA-256으로 바이트 손상을 비교합니다. 서명 인증은 아닙니다.
import json  # 상태를 정해진 JSON 바이트로 저장합니다.
import os  # flush 뒤 fsync와 의도적인 프로세스 종료에 사용합니다.
from pathlib import Path  # 파일 경로를 객체로 다룹니다.
import zlib  # CRC32는 찢어진 기록의 오류 검출용이며 인증 코드가 아닙니다.


class UpdateError(ValueError):
    """업데이트·부팅 계약을 만족하지 않을 때 발생합니다."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise UpdateError(message)  # assert를 사용하지 않아 -O에서도 검사합니다.


def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def metadata_bytes(state: dict) -> bytes:
    return canonical({"state": state, "crc32": zlib.crc32(canonical(state))})


def valid_state(state: dict) -> None:
    require(type(state) is dict and set(state) == {"generation", "active", "pending", "attempted", "images"}, "metadata keys")
    require(type(state["generation"]) is int and 0 <= state["generation"] <= 1000000, "generation range")
    require(state["active"] in ("A", "B"), "active slot")
    require(state["pending"] in (None, "A", "B") and state["pending"] != state["active"], "pending slot")
    require(type(state["attempted"]) is bool and (state["pending"] is not None or not state["attempted"]), "trial state")
    images = state["images"]
    require(type(images) is dict and state["active"] in images and set(images) <= {"A", "B"}, "image manifests")
    require(state["pending"] is None or state["pending"] in images, "pending manifest missing")
    for item in images.values():
        require(type(item) is dict and set(item) == {"length", "sha256"}, "manifest keys")
        require(type(item["length"]) is int and 1 <= item["length"] <= 32, "image length range")
        digest = item["sha256"]
        require(type(digest) is str and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "SHA256 syntax")


def load_state(root: Path) -> dict:
    valid = []
    for index in (0, 1):
        path = root / f"record{index}.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            require(set(record) == {"state", "crc32"} and type(record["crc32"]) is int, "record envelope")
            require(record["crc32"] == zlib.crc32(canonical(record["state"])), "metadata CRC")
            valid_state(record["state"])
            valid.append(record["state"])
        except (OSError, ValueError, TypeError, KeyError):
            continue  # 읽을 수 없거나 찢어진 기록은 다른 유효 기록으로 대체합니다.
    require(bool(valid), "no valid metadata record; recovery required")
    highest = max(item["generation"] for item in valid)
    newest = [item for item in valid if item["generation"] == highest]
    require(all(item == newest[0] for item in newest), "conflicting same-generation records")
    return newest[0]


def crash(label: str) -> None:
    print(json.dumps({"status": "CUT", "checkpoint": label}), flush=True)
    os._exit(23)  # context 정리 없이 끝내지만 실제 컴퓨터 전원을 끄지는 않습니다.


def write_prefix(path: Path, data: bytes, prefix: int | None, label: str) -> None:
    count = len(data) if prefix is None else prefix
    require(type(count) is int and 0 <= count <= len(data), "prefix range")
    with path.open("wb") as stream:  # wb는 파일을 비우고 바이트를 씁니다.
        stream.write(data[:count])  # [:count]는 선택한 기록 위치 앞까지만 남깁니다.
        stream.flush()
        os.fsync(stream.fileno())  # OS에 파일 동기화를 요청하며 flash 내구성을 증명하지 않습니다.
        if prefix is not None:
            crash(label)


def commit(root: Path, previous: dict, updated: dict, phase: str, cut: str, mutation: str) -> dict:
    state = copy.deepcopy(updated)
    state["generation"] = previous["generation"] + 1
    valid_state(state)
    data = metadata_bytes(state)
    index = 0 if mutation == "single-record" else state["generation"] % 2
    positions = {"zero": 0, "one": 1, "half": len(data)//2, "last": len(data)-1, "full": len(data)}
    token = cut.split(":", 1) if ":" in cut else []
    prefix = positions[token[1]] if token and token[0] == phase else None
    write_prefix(root / f"record{index}.json", data, prefix, cut)
    return state


def validate_image(root: Path, slot: str, manifest: dict, mutation: str) -> None:
    data = (root / f"slot{slot}.bin").read_bytes()
    require(len(data) == manifest["length"], "image length mismatch")
    if mutation != "skip-hash":
        require(hashlib.sha256(data).hexdigest() == manifest["sha256"], "image SHA256 mismatch")


def seed(root: Path, fixture: dict) -> dict:
    root.mkdir(parents=True, exist_ok=False)
    old = fixture["old"]
    write_prefix(root / "slotA.bin", bytes.fromhex(old["hex"]), None, "")
    state = {"generation": 0, "active": "A", "pending": None, "attempted": False,
             "images": {"A": old["manifest"]}}
    valid_state(state)
    write_prefix(root / "record0.json", metadata_bytes(state), None, "")
    return {"status": "SEEDED", "generation": 0}


def install(root: Path, fixture: dict, cut: str, mutation: str) -> dict:
    state = load_state(root)
    require(state["pending"] is None, "update already pending")
    validate_image(root, state["active"], state["images"][state["active"]], mutation)
    target = state["active"] if mutation == "erase-active" else ("B" if state["active"] == "A" else "A")
    incoming = fixture["new"]
    candidate = copy.deepcopy(state)
    candidate["images"][target] = incoming["manifest"]
    valid_state(candidate)
    require(1 <= len(bytes.fromhex(incoming["hex"])) <= 32, "input payload length")
    prefix = int(cut.split(":")[1]) if cut.startswith("image:") else None
    write_prefix(root / f"slot{target}.bin", bytes.fromhex(incoming["hex"]), prefix, cut)
    validate_image(root, target, incoming["manifest"], mutation)
    if cut == "verified":
        crash(cut)
    if mutation == "confirm-early":
        candidate.update(active=target, pending=None, attempted=False)
    else:
        candidate.update(pending=target, attempted=False)
    committed = commit(root, state, candidate, "pending", cut, mutation)
    return {"status": "STAGED", "target": target, "generation": committed["generation"]}


def response(state: dict, selected: str, mode: str) -> dict:
    return {"status": "BOOT", "selected": selected, "mode": mode,
            "generation": state["generation"], "active": state["active"],
            "pending": state["pending"], "attempted": state["attempted"]}


def boot(root: Path, cut: str, mutation: str) -> dict:
    state = load_state(root)
    validate_image(root, state["active"], state["images"][state["active"]], mutation)
    pending = state["pending"]
    if pending is None:
        return response(state, state["active"], "stable")
    candidate = copy.deepcopy(state)
    if state["attempted"]:
        candidate.update(pending=None, attempted=False)
        rolled = commit(root, state, candidate, "rollback", cut, mutation)
        return response(rolled, rolled["active"], "rollback")
    try:
        validate_image(root, pending, state["images"][pending], mutation)
    except (OSError, UpdateError):
        candidate.update(pending=None, attempted=False)
        rolled = commit(root, state, candidate, "rollback", cut, mutation)
        return response(rolled, rolled["active"], "invalid_pending")
    candidate["attempted"] = True
    trial = commit(root, state, candidate, "trial", cut, mutation)
    return response(trial, pending, "trial")  # trial 기록을 마친 뒤에만 새 슬롯을 선택합니다.


def confirm(root: Path, application_ok: bool, cut: str, mutation: str) -> dict:
    state = load_state(root)
    require(state["pending"] is not None and state["attempted"], "no running trial to confirm")
    require(application_ok, "application health checkpoint missing")
    validate_image(root, state["pending"], state["images"][state["pending"]], mutation)
    updated = copy.deepcopy(state)
    updated.update(active=state["pending"], pending=None, attempted=False)
    committed = commit(root, state, updated, "confirm", cut, mutation)
    return response(committed, committed["active"], "confirmed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--action", choices=("seed", "install", "boot", "confirm"), required=True)
    parser.add_argument("--cut", default="none")
    parser.add_argument("--mutation", choices=("none", "erase-active", "confirm-early", "skip-hash", "single-record"), default="none")
    parser.add_argument("--application-ok", action="store_true")
    args = parser.parse_args()
    try:
        allowed = {"seed": {"none"}, "install": {"none", "verified"}, "boot": {"none"}, "confirm": {"none"}}
        phases = {"install": ("pending",), "boot": ("trial", "rollback"), "confirm": ("confirm",), "seed": ()}
        for phase in phases[args.action]:
            allowed[args.action].update(phase + ":" + position for position in ("zero", "one", "half", "last", "full"))
        if args.action == "install":
            allowed[args.action].update(f"image:{count}" for count in range(33))
        require(args.cut in allowed[args.action], "unsupported cut for this action")
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        if args.action == "seed":
            result = seed(args.root, fixture)
        elif args.action == "install":
            result = install(args.root, fixture, args.cut, args.mutation)
        elif args.action == "boot":
            result = boot(args.root, args.cut, args.mutation)
        else:
            result = confirm(args.root, args.application_ok, args.cut, args.mutation)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "REJECTED", "error": f"{type(error).__name__}: {error}"}, ensure_ascii=False))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

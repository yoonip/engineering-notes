"""Bounded, single-writer backup restoration into a fresh host directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat


MUTATIONS = ("missing-file-allowed", "skip-content-check", "accept-old-generation",
             "publish-before-complete")


class Refused(ValueError):
    pass


def need(condition, code):
    if not condition:
        raise Refused(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def no_links(path):
    """Check all existing ancestors before resolve; controlled directories only."""
    for item in (path, *path.parents):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        reparse = getattr(info, "st_file_attributes", 0) & 0x400
        need(not stat.S_ISLNK(info.st_mode) and not reparse, "LINK_UNSUPPORTED")


def file_bytes(path, maximum):
    no_links(path)
    need(path.is_file(), "MISSING_FILE")
    need(path.stat().st_size <= maximum, "FILE_TOO_LARGE")
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    need(len(data) <= maximum, "FILE_TOO_LARGE")
    return data


def load_json(path):
    raw = file_bytes(path, 16384)
    try:
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise Refused("INVALID_JSON") from error
    need(type(obj) is dict, "OBJECT_REQUIRED")
    return raw, obj


def safe_name(value):
    need(type(value) is str and 1 <= len(value) <= 160, "BAD_PATH")
    parts = value.split("/")
    reserved = {"CON", "PRN", "AUX", "NUL"} | {
        f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)}
    for part in parts:
        need(1 <= len(part) <= 48 and re.fullmatch(
            r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", part) is not None, "BAD_PATH")
        need(part.split(".")[0].upper() not in reserved, "RESERVED_PATH")
    return value


def names(values):
    need(type(values) is list and 1 <= len(values) <= 16, "BAD_PATH_LIST")
    result = [safe_name(value) for value in values]
    folded = [value.casefold() for value in result]
    need(len(set(folded)) == len(result), "DUPLICATE_OR_CASE_COLLISION")
    for left in folded:
        need(not any(right.startswith(left + "/") for right in folded), "PATH_PREFIX_COLLISION")
    spelling = {}
    for value in result:
        parts = value.split("/")
        for count in range(1, len(parts) + 1):
            prefix = "/".join(parts[:count])
            need(spelling.setdefault(prefix.casefold(), prefix) == prefix, "DIRECTORY_CASE_COLLISION")
    return result


def tree_files(root):
    need(root.is_dir(), "MISSING_DIRECTORY")
    no_links(root)
    found, directories = set(), set()
    pending = [root]
    while pending:
        current = pending.pop()
        for child in current.iterdir():
            no_links(child)
            relative = child.relative_to(root).as_posix()
            if child.is_dir():
                directories.add(relative)
                pending.append(child)
            else:
                need(child.is_file(), "NON_REGULAR_FILE")
                found.add(relative)
            need(len(found) + len(directories) <= 64, "TREE_TOO_LARGE")
    return found, directories


def parent_names(paths):
    return {"/".join(value.split("/")[:count]) for value in paths
            for count in range(1, len(value.split("/")))}


def restore(backup, request_path, destination, mutation=None, cut_after=None):
    need(mutation is None or mutation in MUTATIONS, "BAD_MUTATION")
    need(cut_after is None or type(cut_after) is int and 1 <= cut_after <= 16, "BAD_CUT")
    for item in (backup, request_path, destination):
        no_links(item.absolute())
    backup, request_path, destination = (item.resolve() for item in
                                         (backup, request_path, destination))
    stage = destination.with_name(destination.name + ".staging")
    no_links(stage)
    need(destination.parent.is_dir(), "OUTPUT_PARENT_MISSING")
    need(not destination.exists() and not stage.exists(), "OUTPUT_EXISTS")
    backup_root = backup.resolve()
    for output in (destination, stage):
        need(not output.is_relative_to(backup_root) and not backup_root.is_relative_to(output),
             "OUTPUT_OVERLAPS_BACKUP")
        need(not request_path.is_relative_to(output), "OUTPUT_OVERLAPS_REQUEST")
    request_raw, request = load_json(request_path)
    need(set(request) == {"format", "generation", "manifest_sha256", "paths"}, "REQUEST_SCHEMA")
    need(request["format"] == "RESTORE-REQUEST1", "REQUEST_FORMAT")
    need(type(request["generation"]) is int and 0 <= request["generation"] <= 1000000,
         "BAD_GENERATION")
    need(type(request["manifest_sha256"]) is str and re.fullmatch(
        r"[0-9a-f]{64}", request["manifest_sha256"]) is not None, "BAD_MANIFEST_REFERENCE")
    expected = names(request["paths"])
    raw, manifest = load_json(backup / "manifest.json")
    need(sha(raw) == request["manifest_sha256"], "MANIFEST_REFERENCE_MISMATCH")
    need(set(manifest) == {"format", "generation", "files"}, "MANIFEST_SCHEMA")
    need(manifest["format"] == "BACKUP1", "MANIFEST_FORMAT")
    need(type(manifest["generation"]) is int and 0 <= manifest["generation"] <= 1000000,
         "BAD_GENERATION")
    if mutation != "accept-old-generation":
        need(manifest["generation"] == request["generation"], "OLD_GENERATION")
    records = manifest["files"]
    need(type(records) is list and 1 <= len(records) <= 16, "BAD_RECORD_LIST")
    for record in records:
        need(type(record) is dict and set(record) == {"path", "size", "sha256"}, "RECORD_SCHEMA")
        need(type(record["size"]) is int and 0 <= record["size"] <= 4096, "BAD_SIZE")
        need(type(record["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}",
             record["sha256"]) is not None, "BAD_DIGEST")
    actual_names = names([record["path"] for record in records])
    need(set(actual_names) == set(expected), "INVENTORY_MISMATCH")
    expected_files = {"manifest.json"} | {"payload/" + value for value in expected}
    backup_files, backup_dirs = tree_files(backup)
    allowed_dirs = {"payload"} | {"payload/" + name for name in parent_names(expected)}
    need(backup_dirs == allowed_dirs, "BACKUP_DIRECTORY_MISMATCH")
    if mutation == "missing-file-allowed":
        need(backup_files <= expected_files, "UNEXPECTED_BACKUP_FILE")
    else:
        need(backup_files == expected_files, "BACKUP_FILE_SET_MISMATCH")
    payloads = {}
    for record in records:
        source = backup / "payload" / record["path"]
        if mutation == "missing-file-allowed" and not source.exists():
            continue
        data = file_bytes(source, 4096)
        need(len(data) == record["size"], "PAYLOAD_LENGTH_MISMATCH")
        if mutation != "skip-content-check":
            need(sha(data) == record["sha256"], "PAYLOAD_DIGEST_MISMATCH")
        payloads[record["path"]] = data
    stage.mkdir()
    target = stage
    if mutation == "publish-before-complete":
        stage.rename(destination)
        target = destination
    for index, (name, data) in enumerate(sorted(payloads.items()), 1):
        output = target / name
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if cut_after == index:
            return {"status": "INTERRUPTED", "copied": index, "published": destination.exists()}
    found, directories = tree_files(target)
    required = set(payloads) if mutation == "missing-file-allowed" else set(expected)
    need(found == required and directories == parent_names(required), "RESTORE_INCOMPLETE")
    for record in records:
        if mutation == "missing-file-allowed" and record["path"] not in payloads:
            continue
        copied = file_bytes(target / record["path"], 4096)
        need(len(copied) == record["size"], "RESTORED_LENGTH_MISMATCH")
        if mutation != "skip-content-check":
            need(sha(copied) == record["sha256"], "RESTORED_DIGEST_MISMATCH")
    need(file_bytes(request_path, 16384) == request_raw and
         file_bytes(backup / "manifest.json", 16384) == raw, "INPUT_CHANGED")
    need(not destination.exists() or mutation == "publish-before-complete", "OUTPUT_EXISTS")
    if target == stage:
        stage.rename(destination)
    return {"status": "RESTORED", "backup_integrity": "VERIFIED",
            "restored_content": "VERIFIED", "generation": manifest["generation"],
            "files": sorted(found), "bytes": sum(len(value) for value in payloads.values()),
            "published": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--mutation", choices=MUTATIONS)
    parser.add_argument("--cut-after", type=int)
    args = parser.parse_args()
    try:
        result = restore(args.backup, args.request, args.destination, args.mutation, args.cut_after)
        code = 4 if result["status"] == "INTERRUPTED" else 0
    except (Refused, OSError) as error:
        result, code = {"status": "REFUSED", "reason": str(error)}, 3
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

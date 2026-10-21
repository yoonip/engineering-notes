"""Create fresh host files and compare restored bytes with independent literals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ORACLE = {"config.bin": b"\x01\x02\x03\x04",
          "models/model.bin": b"\x10\x20\x30\x40\x50",
          "notes/readme.txt": b"OK\n"}
MUTATIONS = ("missing-file-allowed", "skip-content-check", "accept-old-generation",
             "publish-before-complete")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def inventory(root):
    result = {}
    for path in sorted(root.rglob("*")):
        key = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[key] = "SYMLINK:" + os.readlink(path)
        elif path.is_file():
            result[key] = sha(path.read_bytes())
        elif path.is_dir():
            result[key] = "DIRECTORY"
        else:
            result[key] = "OTHER"
    return result


class Verification:
    def __init__(self, output, mutation):
        self.output, self.mutation = output, mutation
        self.report = {"status": "RUNNING", "mutation": mutation, "checks": 0,
                       "cases": [], "children": [], "capabilities": {},
                       "python": sys.version, "platform": platform.platform(),
                       "source_sha256": {name: sha((HERE / name).read_bytes())
                                         for name in ("model.py", "verify.py", "fixtures.json")}}

    def need(self, condition, label):
        self.report["checks"] += 1
        if not condition:
            raise RuntimeError(label)

    def setup(self, label):
        root = self.output / label
        root.mkdir()
        original, backup = root / "original", root / "backup"
        original.mkdir()
        backup.mkdir()
        for name, data in ORACLE.items():
            path = original / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        records = []
        for name in sorted(ORACLE):
            data = (original / name).read_bytes()
            target = backup / "payload" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            records.append({"path": name, "size": len(data), "sha256": sha(data)})
        dump(backup / "manifest.json", {"format": "BACKUP1", "generation": 7, "files": records})
        request = root / "request.json"
        dump(request, {"format": "RESTORE-REQUEST1", "generation": 7,
                       "manifest_sha256": sha((backup / "manifest.json").read_bytes()),
                       "paths": sorted(ORACLE)})
        return root, original, backup, request, root / "restored"

    def reseal(self, backup, request, modify):
        manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
        modify(manifest)
        dump(backup / "manifest.json", manifest)
        expected = json.loads(request.read_text(encoding="utf-8"))
        expected["manifest_sha256"] = sha((backup / "manifest.json").read_bytes())
        dump(request, expected)

    def run_child(self, original, backup, request, destination, extra=()):
        before = {"original": inventory(original), "backup": inventory(backup),
                  "request": sha(request.read_bytes())}
        command = [sys.executable, "-X", "utf8", "-B"]
        if sys.flags.optimize:
            command.append("-O")
        command += [str(HERE / "model.py"), "--backup", str(backup), "--request", str(request),
                    "--destination", str(destination)]
        if self.mutation:
            command += ["--mutation", self.mutation]
        command += list(extra)
        child = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=20)
        entry = {"command": command, "exit": child.returncode,
                 "stdout": child.stdout, "stderr": child.stderr}
        self.report["children"].append(entry)
        self.need(child.stderr == "", "unexpected child stderr")
        try:
            observed = json.loads(child.stdout)
        except json.JSONDecodeError as error:
            raise RuntimeError("missing child JSON") from error
        entry["observed"] = observed
        self.need(before == {"original": inventory(original), "backup": inventory(backup),
                            "request": sha(request.read_bytes())}, "input changed")
        entry["inputs_preserved"] = True
        return child.returncode, observed

    def refusal(self, label, change, reason, extra=()):
        root, original, backup, request, dest = self.setup(label)
        change(root, original, backup, request, dest)
        before = inventory(root)
        code, observed = self.run_child(original, backup, request, dest, extra)
        self.need(code == 3 and observed.get("status") == "REFUSED", label + ": refused")
        self.need(observed.get("reason") == reason, label + ": reason")
        self.need(before == inventory(root), label + ": no output/input changes")
        self.report["cases"].append({"name": label, "status": "PASS", "reason": reason})

    def execute(self):
        fixture = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
        self.need(fixture["expected_files_hex"] == {name: data.hex() for name, data in ORACLE.items()},
                  "fixture literal mismatch")
        self.need(fixture["generation"] == 7 and fixture["total_bytes"] == 12, "fixture constants")
        root, original, backup, request, dest = self.setup("restore_deleted_and_changed")
        (original / "models/model.bin").unlink()
        (original / "config.bin").write_bytes(b"\x09\x09\x09\x09")
        code, observed = self.run_child(original, backup, request, dest)
        self.need(code == 0 and observed.get("status") == "RESTORED", "restore status")
        self.need(observed.get("backup_integrity") == "VERIFIED" and
                  observed.get("restored_content") == "VERIFIED", "separate verification labels")
        files = {path.relative_to(dest).as_posix(): path.read_bytes()
                 for path in dest.rglob("*") if path.is_file()}
        self.need(files == ORACLE, "restored literal path set and payload")
        self.need(observed.get("files") == ["config.bin", "models/model.bin", "notes/readme.txt"] and
                  observed.get("bytes") == 12 and observed.get("generation") == 7, "restore summary")
        self.need(not dest.with_name(dest.name + ".staging").exists(), "stage published")
        self.report["cases"].append({"name": "restore_deleted_and_changed", "status": "PASS",
                                     "restored_hex": {name: value.hex() for name, value in files.items()}})

        self.refusal("missing_payload", lambda r, o, b, q, d: (b / "payload/models/model.bin").unlink(),
                     "BACKUP_FILE_SET_MISMATCH")
        self.refusal("changed_payload", lambda r, o, b, q, d:
                     (b / "payload/config.bin").write_bytes(b"\x01\x02\x03\x05"), "PAYLOAD_DIGEST_MISMATCH")
        self.refusal("short_payload", lambda r, o, b, q, d:
                     (b / "payload/config.bin").write_bytes(b"\x01\x02\x03"), "PAYLOAD_LENGTH_MISMATCH")
        self.refusal("wrong_declared_size", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"][0].update(size=5)), "PAYLOAD_LENGTH_MISMATCH")
        self.refusal("old_generation", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m.update(generation=6)), "OLD_GENERATION")
        self.refusal("manifest_replaced", lambda r, o, b, q, d:
                     (b / "manifest.json").write_bytes((b / "manifest.json").read_bytes() + b" "),
                     "MANIFEST_REFERENCE_MISMATCH")
        self.refusal("extra_backup_file", lambda r, o, b, q, d:
                     (b / "payload/extra.bin").write_bytes(b"x"), "BACKUP_FILE_SET_MISMATCH")
        self.refusal("extra_empty_directory", lambda r, o, b, q, d:
                     (b / "payload/extra").mkdir(), "BACKUP_DIRECTORY_MISMATCH")
        self.refusal("manifest_omits_file", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"].pop()), "INVENTORY_MISMATCH")
        for label, bad in (("parent_escape", "../escape.bin"), ("absolute_path", "/escape.bin"),
                           ("windows_absolute", "C:/escape.bin"), ("backslash_path", "a\\b.bin"),
                           ("dot_component", "a/./b.bin"), ("empty_component", "a//b.bin"),
                           ("reserved_windows_name", "NUL.txt")):
            self.refusal(label, lambda r, o, b, q, d, bad=bad:
                         self.reseal(b, q, lambda m: m["files"][0].update(path=bad)),
                         "RESERVED_PATH" if label == "reserved_windows_name" else "BAD_PATH")
        self.refusal("duplicate_path", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"].append(dict(m["files"][0]))),
                     "DUPLICATE_OR_CASE_COLLISION")
        self.refusal("case_collision", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"][1].update(path="CONFIG.bin")),
                     "DUPLICATE_OR_CASE_COLLISION")
        self.refusal("file_directory_prefix", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"][0].update(path="models")), "PATH_PREFIX_COLLISION")
        self.refusal("directory_case_collision", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"][0].update(path="Models/config.bin")),
                     "DIRECTORY_CASE_COLLISION")
        self.refusal("bool_generation", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m.update(generation=True)), "BAD_GENERATION")
        self.refusal("bool_size", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"][0].update(size=True)), "BAD_SIZE")
        self.refusal("oversize_record", lambda r, o, b, q, d:
                     self.reseal(b, q, lambda m: m["files"][0].update(size=4097)), "BAD_SIZE")
        self.refusal("request_duplicate_key", lambda r, o, b, q, d:
                     q.write_bytes(q.read_bytes().rstrip()[:-1] + b', "generation":7}'), "DUPLICATE_JSON_KEY")
        self.refusal("request_empty_inventory", lambda r, o, b, q, d:
                     dump(q, dict(json.loads(q.read_text(encoding="utf-8")), paths=[])), "BAD_PATH_LIST")
        self.refusal("request_inventory_omits_file", lambda r, o, b, q, d:
                     dump(q, dict(json.loads(q.read_text(encoding="utf-8")), paths=["config.bin"])),
                     "INVENTORY_MISMATCH")
        self.refusal("existing_destination", lambda r, o, b, q, d: d.mkdir(), "OUTPUT_EXISTS")
        self.refusal("existing_stage", lambda r, o, b, q, d:
                     d.with_name(d.name + ".staging").mkdir(), "OUTPUT_EXISTS")
        self.refusal("output_inside_backup", lambda r, o, b, q, d: None, "OUTPUT_OVERLAPS_BACKUP",
                     ("--destination", str(self.output / "output_inside_backup/backup/new")))

        root, original, backup, request, dest = self.setup("interrupted_after_one")
        code, observed = self.run_child(original, backup, request, dest, ("--cut-after", "1"))
        self.need(code == 4 and observed.get("status") == "INTERRUPTED", "interruption status")
        self.need(not dest.exists(), "partial output must not be published")
        stage = dest.with_name(dest.name + ".staging")
        partial = {p.relative_to(stage).as_posix(): p.read_bytes() for p in stage.rglob("*") if p.is_file()}
        self.need(partial == {"config.bin": b"\x01\x02\x03\x04"}, "partial stage bytes")
        saved = inventory(root)
        code, observed = self.run_child(original, backup, request, dest)
        self.need(code == 3 and observed.get("reason") == "OUTPUT_EXISTS", "no stale-stage reuse")
        self.need(saved == inventory(root), "preserve interrupted evidence")
        self.report["cases"].append({"name": "interrupted_after_one", "status": "PASS",
                                     "published": False, "stage_hex": {k: v.hex() for k, v in partial.items()}})

        root, original, backup, request, dest = self.setup("payload_symlink")
        outside = root / "outside.bin"
        outside.write_bytes(ORACLE["config.bin"])
        link = backup / "payload/link-probe.bin"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as error:
            self.report["capabilities"]["symlink"] = {"status": "NOT_EXECUTED", "reason": str(error)}
        else:
            self.report["capabilities"]["symlink"] = {"status": "EXECUTED"}
            before = inventory(root)
            code, observed = self.run_child(original, backup, request, dest)
            self.need(code == 3 and observed.get("reason") == "LINK_UNSUPPORTED", "symlink refused")
            self.need(before == inventory(root), "symlink source unchanged")
            self.report["cases"].append({"name": "payload_symlink", "status": "PASS"})
        self.report["status"] = "PASS"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    try:
        args.output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(json.dumps({"status": "REFUSED", "reason": "OUTPUT_EXISTS"}))
        return 2
    verify = Verification(args.output.resolve(), args.mutation)
    try:
        verify.execute()
        code = 0
    except Exception as error:
        verify.report.update(status="ERROR", error=str(error), error_type=type(error).__name__)
        code = 1
    dump(args.output / "results.json", verify.report)
    print(json.dumps({"status": verify.report["status"], "checks": verify.report["checks"],
                      "cases": len(verify.report["cases"]), "children": len(verify.report["children"]),
                      "error": verify.report.get("error")}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

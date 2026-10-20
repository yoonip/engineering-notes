"""C/C++ 교육 사례를 빌드하고 실행 기록을 새 출력 폴더에 저장합니다."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--zig", type=Path, help="zig cc / zig c++를 사용할 실행 파일입니다.")
    parser.add_argument("--cc", default="gcc")
    parser.add_argument("--cxx", default="g++")
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)  # 기존 기록을 덮어쓰지 않습니다.
    source_dir = Path(__file__).resolve().parent
    report = {"utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version, "platform": platform.platform(),
              "scope": "host execution; deliberate educational faults; no MCU/ISR/physical board",
              "runs": []}

    def invoke(command: list[str], label: str) -> dict:
        result = subprocess.run(command, text=True, encoding="utf-8", errors="replace",
                                capture_output=True, timeout=240, cwd=out)
        entry = {"label": label, "command": command, "exit_code": result.returncode,
                 "stdout": result.stdout, "stderr": result.stderr}
        (out / f"{label}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        report["runs"].append(entry)
        return entry

    try:
        if args.zig:
            zig = str(args.zig.resolve())
            c_compiler, cpp_compiler = [zig, "cc"], [zig, "c++"]
            version = invoke([zig, "version"], "compiler-version")
        else:
            c_compiler, cpp_compiler = [args.cc], [args.cxx]
            version = invoke([args.cc, "--version"], "c-compiler-version")
            invoke([args.cxx, "--version"], "cpp-compiler-version")
        if version["exit_code"]:
            raise RuntimeError("compiler version query failed")
        for name, standard, compiler in [
            ("frame_bounds.c", "c11", c_compiler),
            ("view_ownership.cpp", "c++17", cpp_compiler),
            ("ring_publish_model.c", "c11", c_compiler),
        ]:
            original = source_dir / name
            # 소스 복사본과 바이너리를 함께 남겨 실제 빌드 입력을 보존합니다.
            copied = out / name
            shutil.copyfile(original, copied)
            digest = hashlib.sha256(copied.read_bytes()).hexdigest()
            executable = out / (copied.stem + (".exe" if sys.platform == "win32" else ""))
            build = invoke(compiler + [f"-std={standard}", "-O2", "-UNDEBUG", "-Wall", "-Wextra", "-Werror",
                                       name, "-o", str(executable)], copied.stem + "-build")
            build["source_sha256"] = digest
            if build["exit_code"]:
                raise RuntimeError(f"{name}: build failed")
            run = invoke([str(executable)], copied.stem + "-run")
            if run["exit_code"]:
                raise RuntimeError(f"{name}: contract check failed")
        report["status"] = "passed"
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = str(exc)
    (out / "results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(out / "results.json")},
                     ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

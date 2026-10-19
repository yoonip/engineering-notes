"""VS Code file-input launcher; the solution file stays unchanged."""
from pathlib import Path
import io
import os
import runpy
import sys

def main():
    if len(sys.argv) < 2:
        print("[실행 안내] 실행할 Python(.py) 코드 탭을 먼저 선택한 뒤 F5를 누르세요.",
              file=sys.stderr, flush=True)
        return
    source = Path(sys.argv[1]).resolve()
    if source.suffix.lower() != ".py":
        language = "C++" if source.suffix.lower() in (".cpp", ".cc", ".cxx") else "C"
        print(f"[실행 안내] 현재 연 파일은 {source.name}인데 Python 실행 설정이 선택되어 있습니다.",
              file=sys.stderr, flush=True)
        if source.suffix.lower() in (".c", ".cpp", ".cc", ".cxx"):
            print(f"왼쪽 [실행 및 디버그]의 위쪽 설정 목록에서 '{language} 현재 파일 (input.txt 자동 입력)'을 선택하고 다시 F5를 누르세요.",
                  file=sys.stderr, flush=True)
        else:
            print("실행할 .py / .cpp / .c 코드 탭을 선택하세요. Python 코드는 .py 파일에서 실행합니다.",
                  file=sys.stderr, flush=True)
        return
    if not source.is_file():
        print(f"[실행 안내] {source.name} 파일을 찾지 못했습니다. 코드를 저장하고 그 탭을 선택한 뒤 다시 실행하세요.",
              file=sys.stderr, flush=True)
        return
    workspace = Path(__file__).resolve().parent.parent
    candidates = (source.parent / "input.txt", workspace / "input.txt")
    input_path = next((path for path in candidates if path.is_file()), None)
    if input_path is None:
        print("[실행 안내] 코드 파일과 같은 폴더에 input.txt를 만들고 문제의 예제 입력을 넣으세요. 프로젝트 루트의 input.txt도 사용할 수 있습니다.",
              file=sys.stderr, flush=True)
        return
    # Opening text stdin keeps input(), sys.stdin.read(), and stdin.buffer usable.
    # The file provides EOF automatically, including for read-to-end solutions.
    print(f"[input.txt] {input_path}", file=sys.stderr, flush=True)
    with input_path.open("rb") as raw_stream:
        # Skip only a leading UTF-8 BOM, including for sys.stdin.buffer readers.
        if raw_stream.read(3) != b"\xef\xbb\xbf":
            raw_stream.seek(0)
        input_stream = io.TextIOWrapper(raw_stream, encoding="utf-8", newline=None)
        old_stdin = sys.stdin
        old_argv = sys.argv
        old_cwd = Path.cwd()
        sys.stdin = input_stream
        sys.argv = [str(source)] + old_argv[2:]
        sys.path.insert(0, str(source.parent))
        os.chdir(source.parent)
        try:
            # run_path preserves the real source filename for VS Code breakpoints.
            runpy.run_path(str(source), run_name="__main__")
        finally:
            sys.stdin = old_stdin
            sys.argv = old_argv
            os.chdir(old_cwd)

if __name__ == "__main__":
    main()

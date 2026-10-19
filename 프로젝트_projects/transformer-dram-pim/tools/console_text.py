"""Windows 외부 도구의 UTF-8/CP949 출력을 읽는 공통 함수.

Transformer의 정수 수식이나 UART payload를 변환하는 모듈이 아니다.
Icarus/vvp 같은 프로그램이 stdout/stderr에 출력한 사람용 로그만 해석한다.
가령 한국어 Windows의 vvp는 경로를 CP949로 출력할 수 있으므로 처음부터
UTF-8 errors='replace'로 읽으면 원래 한글 바이트를 복원할 기회를 잃는다.
"""
from __future__ import annotations

import locale
import subprocess
from typing import Any


def decode_console_bytes(data: bytes) -> str:
    """원본 바이트를 보존한 채 UTF-8 → CP949 → OS 기본 encoding 순서로 읽는다.

    UTF-8은 새 Python 도구의 표준 로그이므로 먼저 검사한다. UTF-8 strict가
    실패하면 한국어 Windows 도구에서 실제 관찰한 CP949로 다시 검사한다.
    두 형식 모두 아니라면 OS의 기본 encoding을 strict로 시도하고, 그래도
    해석되지 않는 부분만 replacement 문자로 표시한다. 모든 바이트열의
    encoding을 자동으로 확정할 수 있다는 뜻은 아니며, 이 프로젝트의
    실제 도구 출력 두 종류를 손실 없이 읽는 것이 우선이다.
    """
    preferred = locale.getpreferredencoding(False) or "utf-8"
    # 같은 encoding을 반복 검사해도 해석이 달라지지 않으므로 중복을 뺀다.
    candidates = dict.fromkeys(("utf-8", "cp949", preferred))
    for encoding in candidates:
        try:
            return data.decode(encoding, errors="strict")
        except (UnicodeDecodeError, LookupError):
            continue
    # 알 수 없는 바이트가 있다는 이유만으로 실패 로그 전체를 읽지 못하면
    # 원래 도구의 오류를 찾기 어렵다. 마지막 단계에만 대체 문자를 허용한다.
    try:
        return data.decode(preferred, errors="replace")
    except LookupError:
        return data.decode("utf-8", errors="replace")


def _console_output(value: bytes | None) -> str | None:
    """capture하지 않은 stream의 None은 유지하고 text=True의 줄바꿈 규칙을 따른다."""
    if value is None:
        return None
    return decode_console_bytes(value).replace("\r\n", "\n").replace("\r", "\n")


def run_console(*popenargs: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """subprocess.run처럼 실행하되 콘솔 출력은 bytes로 받은 뒤 안전하게 읽는다.

    executable/argument list/cwd/env/timeout/returncode를 바꾸지 않는다.
    기존 호출부가 text=True, encoding='utf-8', errors='replace'를 넘겨도
    subprocess 내부에서 먼저 손실 변환하지 않도록 이 옵션만 제거한다.
    stdout/stderr는 문자열 또는 미수집 시 None으로 돌려주므로 기존의
    PASS 검사, 숫자 정규식, 로그 저장 코드를 그대로 사용할 수 있다.
    """
    options = dict(kwargs)
    # 이 프로젝트의 Icarus/vvp 호출은 input을 쓰지 않는다. 일반적인 도구에
    # str input을 전달하는 경우에는 명시한 encoding 또는 UTF-8로 바이트화한다.
    input_encoding = options.pop("encoding", None) or "utf-8"
    input_errors = options.pop("errors", None) or "strict"
    options.pop("text", None)
    options.pop("universal_newlines", None)
    options["text"] = False
    if isinstance(options.get("input"), str):
        options["input"] = options["input"].encode(input_encoding, errors=input_errors)
    try:
        result = subprocess.run(*popenargs, **options)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        # check=True 실패나 timeout에서도 원래 예외 종류·종료코드·timeout은
        # 그대로 전달하고, 수집한 partial 로그만 같은 규칙으로 해석한다.
        error.output = _console_output(error.output)
        error.stderr = _console_output(error.stderr)
        raise
    return subprocess.CompletedProcess(
        args=result.args,
        returncode=result.returncode,
        stdout=_console_output(result.stdout),
        stderr=_console_output(result.stderr),
    )

"""현재 Python ABI와 맞는 프로젝트 로컬 PyTorch만 import 경로에 넣는다.

cp313 wheel은 Python3.13용이고 cp312는 Python3.12용이다. 이름이 같은 torch
폴더라고 먼저 넣으면 DLL 로딩 오류가 난다. 이 함수는 설치·학습·가중치 변경을
하지 않으며 WHEEL의 실제 호환 tag를 확인해 선택한다.
"""
from pathlib import Path
import importlib.util
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def enable_local_torch() -> Path | None:
    """일반 설치를 우선하고 없으면 현재 cpXY와 같은 로컬 wheel을 선택한다."""
    if importlib.util.find_spec('torch') is not None:
        return None
    abi = f'cp{sys.version_info.major}{sys.version_info.minor}'
    candidates = [ROOT/'build'/f'python_packages_{abi}', ROOT/'build/python_packages']
    for candidate in candidates:
        for wheel in candidate.glob('torch-*.dist-info/WHEEL'):
            tags = re.findall(r'^Tag:\s*(\S+)\s*$',wheel.read_text(encoding='utf-8'),re.M)
            if any(tag.startswith(abi+'-'+abi+'-') for tag in tags):
                sys.path.insert(0,str(candidate))
                return candidate
    # 호환 wheel이 없으면 import torch 자체가 명확한 오류를 내도록 둔다.
    # 맞지 않는 이전 cp313 DLL을 강제 로딩하거나 바꾸지는 않는다.
    return None

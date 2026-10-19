"""재실행에 사용한 실제 OS·Python·도구 버전을 읽기 전용으로 기록한다."""
from pathlib import Path
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.console_text import decode_console_bytes
from model.torch_runtime import enable_local_torch


def main():
    local_torch = enable_local_torch()
    tools = {}
    for name, path, arguments in [
        ('Icarus','C:/iverilog/bin/iverilog.exe',['-V']),
        ('Vivado','C:/Xilinx/Vivado/2024.1/bin/vivado.bat',['-version']),
    ]:
        executable = Path(path)
        if executable.is_file():
            completed = subprocess.run([str(executable),*arguments],stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,timeout=60,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            text = decode_console_bytes(completed.stdout)
            tools[name] = {'path':str(executable),'returncode':completed.returncode,
                           'version_output':text.strip()}
        else:
            tools[name] = {'path':path,'available':False}
    libraries = {}
    for name in ('torch','numpy','reportlab','pypdf','pdfplumber','Pillow'):
        try:
            libraries[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            libraries[name] = None
    result = {'collected_local_time':datetime.now().isoformat(timespec='seconds'),
              'mode':'read_only_environment_inventory','os':platform.platform(),
              'machine':platform.machine(),'python_version':sys.version,
              'python_executable':sys.executable,'libraries':libraries,'tools':tools,
              'compatible_local_torch_path':str(local_torch) if local_torch else None,
              'physical_fpga_or_pim_measured':False,
              'note_ko':'설치된 도구의 버전 확인이며 새 회로 시험·장비 측정이 아니다. 다른 PC는 실제 설치 경로로 준비한다.'}
    output = ROOT/'build/reports/environment_manifest.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))


if __name__=='__main__':
    main()

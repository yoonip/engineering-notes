"""설치된 Icarus로 고정소수점과 순차회로 예제를 실제 실행한다."""
import argparse
from fractions import Fraction
import json
import locale
from pathlib import Path
import random
import shutil
import subprocess
import tempfile


def run(iverilog=None):
    root=Path(__file__).resolve().parent
    compiler=Path(iverilog or shutil.which('iverilog') or 'C:/iverilog/bin/iverilog.exe')
    simulator=compiler.with_name('vvp.exe' if compiler.suffix=='.exe' else 'vvp')
    if not compiler.is_file() or not simulator.is_file():
        raise FileNotFoundError('iverilog와 같은 폴더의 vvp를 찾을 수 없습니다')
    # Icarus의 Windows 진단은 시스템 코드페이지를 쓴다. Python UTF-8 모드와 구분한다.
    tool_encoding=locale.getencoding()
    rng=random.Random(551)
    edge=[-32768,-32767,-257,-256,-128,-1,0,1,128,256,32767]
    pairs=[(a,b) for a in edge for b in edge]
    pairs.extend((rng.randint(-32768,32767),rng.randint(-32768,32767)) for _ in range(10000))
    result={}
    with tempfile.TemporaryDirectory(prefix='hardware-rtl-') as temporary:
        work=Path(temporary)
        lines=[]
        for a,b in pairs:
            y=max(-32768,min(32767,round(Fraction(a*b,256))))
            lines.append(f'{a&65535:04x}{b&65535:04x}{y&65535:04x}')
        (work/'vectors.hex').write_text('\n'.join(lines)+'\n',encoding='ascii')
        cases=[('qmul16',['qmul16.sv','tb_qmul16.sv'],['-P',f'tb_qmul16.N={len(pairs)}']),
               ('counter_equiv',['counter_equiv.sv','tb_counter_equiv.sv'],[])]
        for name,sources,parameters in cases:
            output=work/(name+'.vvp')
            compile_result=subprocess.run([str(compiler),'-g2012','-s',
                'tb_qmul16' if name=='qmul16' else 'tb_counter_equiv',*parameters,
                '-o',str(output),*[str(root/source) for source in sources]],
                cwd=work,text=True,encoding=tool_encoding,capture_output=True,check=True)
            executed=subprocess.run([str(simulator),str(output)],cwd=work,
                                     text=True,encoding=tool_encoding,capture_output=True,check=True)
            result[name]={'stdout':executed.stdout.strip(),
                          'compile_warnings':compile_result.stderr.strip()}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--iverilog')
    print(json.dumps(run(parser.parse_args().iverilog),ensure_ascii=False,indent=2))

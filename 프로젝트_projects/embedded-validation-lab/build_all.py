"""ARM/STM32 compile + ARM emulator + RV32I RTL/reference comparison."""
from pathlib import Path
import os,sys,subprocess,json,struct,shutil
ROOT=Path(__file__).resolve().parent
WS=Path(os.environ.get('VALIDATION_WORKSPACE', str(ROOT)))
BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
TOOLS=WS/'post-silicon-virtual-lab/tools'
SIM=WS/'tmp/hw_ml_book/tools/sim/ucrt64'

def program(variable, command_name, fallback):
    value = os.environ.get(variable) or shutil.which(command_name)
    if value:
        path = Path(value)
        if path.is_file():
            return path.resolve()
    matches = list(WS.glob(fallback))
    if matches:
        return matches[0].resolve()
    raise FileNotFoundError(f'{command_name}: PATH 또는 {variable} 환경변수에 실행 파일을 지정하세요.')

ARM=program('ARM_GCC','arm-none-eabi-gcc','post-silicon-virtual-lab/tools/xpack-arm*/bin/arm-none-eabi-gcc.exe')
RV=program('RISCV_GCC','riscv-none-elf-gcc','post-silicon-virtual-lab/tools/riscv-gcc/*/bin/riscv-none-elf-gcc.exe')
QEMU=program('QEMU_ARM','qemu-system-arm','post-silicon-virtual-lab/tools/qemu/qemu-system-arm.exe')
IVERILOG=program('IVERILOG','iverilog','tmp/hw_ml_book/tools/sim/ucrt64/bin/iverilog.exe')
VVP=program('VVP','vvp','tmp/hw_ml_book/tools/sim/ucrt64/bin/vvp.exe')
sys.path.insert(0,str(ROOT/'rtl'))
from reference_model import run_reference

def signature():
    x=0x12345678
    for i in range(256):
        x ^= (i+0x9e3779b9)&0xffffffff
        x=((x<<5)|(x>>27))&0xffffffff
        x=(x+0x7f4a7c15)&0xffffffff
    return x

SIG=signature()
def command(args, log, timeout=120, env=None):
    # 인수 배열로 실행해 shell 확장과 공백 path의 인용 오류를 피한다.
    p=subprocess.run([str(a) for a in args],cwd=ROOT,capture_output=True,
                     text=True,errors='replace',timeout=timeout,env=env)
    (BUILD/log).write_text(p.stdout+p.stderr,encoding='utf-8')
    if p.returncode:raise RuntimeError(f'{log}: exit={p.returncode}\n{p.stdout}\n{p.stderr}')
    return p.stdout+p.stderr

flags=['-mcpu=cortex-m7','-mthumb','-mfloat-abi=soft','-Os','-g','-std=c11',
       '-ffreestanding','-fno-builtin','-ffunction-sections','-fdata-sections',
       '-Wall','-Wextra','-Werror','-nostdlib','-Wl,--gc-sections']
command([ARM,*flags,f'-DEXPECTED_SIGNATURE={SIG}u','arm/startup.S','arm/main.c',
         '-Tarm/linker.ld','-o',BUILD/'arm.elf'],'arm_compile.txt')
armrun=command([QEMU,'-M','mps2-an500',
                '-kernel','build/arm.elf','-semihosting-config','enable=on,target=native',
                '-nographic','-monitor','none','-serial','none'],'arm_run.txt')
if 'ARM memory PASS' not in armrun or 'ARM signature PASS' not in armrun:
    raise AssertionError('ARM emulator test failed')
cmsis=Path(os.environ.get('CMSIS_ROOT', str(WS/'STM32F767ZI_Practice')))
cmsis_core=Path(os.environ.get('CMSIS_CORE_INCLUDE', str(cmsis/'Core')))
cmsis_device=Path(os.environ.get('CMSIS_DEVICE_INCLUDE', str(cmsis/'Device')))
command([ARM,*flags,'-DSTM32F767xx',f'-I{cmsis_core}',f'-I{cmsis_device}',
         'arm/startup.S','stm32/main.c','common/runtime.c','-Tstm32/linker.ld','-o',BUILD/'stm32.elf'],
        'stm32_compile.txt')

rvflags=['-march=rv32i','-mabi=ilp32','-mno-relax','-msmall-data-limit=0',
         '-Os','-g','-std=c11','-ffreestanding','-fno-builtin','-Wall','-Wextra','-Werror',
         '-nostdlib','-Wl,--no-relax','-Triscv/linker.ld']
objcopy=Path(os.environ.get('RISCV_OBJCOPY', str(RV.with_name(RV.name.replace('gcc', 'objcopy')))))
images={}
for name,files in [('firmware',['riscv/startup.S','riscv/main.c','common/runtime.c']),
                   ('directed',['riscv/directed.S'])]:
    command([RV,*rvflags,*files,'-o',BUILD/(name+'.elf')],name+'_compile.txt')
    command([objcopy,'-O','binary',BUILD/(name+'.elf'),BUILD/(name+'.bin')],name+'_binary.txt')
    images[name]=(BUILD/(name+'.bin')).read_bytes()
# 의도적인 illegal/misaligned/access fault. 짧은 프로그램으로 원인을 분리한다.
pack=lambda *x:b''.join(struct.pack('<I',i) for i in x)
images.update(illegal=pack(0xffffffff),load_misaligned=pack(0x00102003),
              store_misaligned=pack(0x00002123),jump_misaligned=pack(0x0020006f),
              load_fault=pack(0x000100b7,0x0000a003),
              store_fault=pack(0x000200b7,0x0000a023),
              fetch_fault=pack(0x000100b7,0x00008067),ecall=pack(0x00000073))
env=os.environ.copy();env['PATH']=str(IVERILOG.parent)+os.pathsep+env.get('PATH','')
command([IVERILOG,'-g2012','-s','tb_cpu',
         f"-DEXPECTED_SIGNATURE=32'h{SIG:08x}",'-o',BUILD/'cpu.vvp',
         'rtl/rv32_cpu.sv','rtl/tb_cpu.sv'],'rtl_compile.txt',env=env)
results=[]
for name,binary in images.items():
    ref=run_reference(binary,BUILD/(name+'_golden.txt'))
    padded=binary+bytes(65536-len(binary))
    (BUILD/(name+'.hex')).write_text('\n'.join(
        f'{int.from_bytes(padded[i:i+4],"little"):08x}' for i in range(0,65536,4)),encoding='ascii')
    for seed in ([1,7,42] if name in ['firmware','directed'] else [1]):
        args=[VVP,BUILD/'cpu.vvp',f'+IMAGE=build/{name}.hex',
              f'+GOLDEN=build/{name}_golden.txt',f'+CAUSE={ref["trap_cause"]}',
              f'+TRAP_PC={ref["trap_pc"]:08x}',f'+SEED={seed}']
        if name=='firmware':args.append('+MAILBOX')
        out=command(args,f'{name}_seed{seed}.txt',timeout=120,env=env)
        if 'PASS' not in out:raise AssertionError(out)
        results.append({'name':name,'seed':seed,'reference':ref,'log':out.strip()})
report={'signature':SIG,'signature_hex':f'0x{SIG:08x}',
        'arm_emulator':armrun.strip(),'stm32_compile':'PASS','rtl':results,
        'physical_boards_executed':False}
(BUILD/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'signature':hex(SIG),'arm':armrun.strip(),'stm32':'compile PASS',
                  'rtl_runs':len(results)},indent=2))

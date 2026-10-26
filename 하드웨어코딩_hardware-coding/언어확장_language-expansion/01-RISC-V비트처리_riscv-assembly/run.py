import argparse  # 도구 경로와 새 결과 폴더의 명령행 해석
import hashlib  # 실행 원본과 작업 복사본의 SHA-256 기록
import json  # 실제 명령·출력·결과를 기계 판독 형식으로 저장
import os  # 자식 프로세스 환경 설정
from pathlib import Path  # 소스와 빌드 경로 처리
import re  # ELF 속성과 실제 출력 집계 추출
import shutil  # 원본 소스를 새 빌드 폴더로 복사
import subprocess  # RISC-V 컴파일러와 CPU 에뮬레이터 실행

def main():  # 컴파일·실행·증거 저장의 시작점
    parser = argparse.ArgumentParser()  # 예제 전용 실행 옵션
    parser.add_argument('--gcc', required=True, type=Path)  # RV32I를 지원하는 GNU 컴파일러
    parser.add_argument('--qemu', required=True, type=Path)  # qemu-system-riscv32 실행 파일
    parser.add_argument('--out', required=True, type=Path)  # 기존 결과를 덮지 않을 새 빌드 경로
    parser.add_argument('--negative-byte-sign', action='store_true')  # 복사본에서만 lbu를 lb로 바꾸는 음성 대조
    args = parser.parse_args()  # 실제 전달한 옵션 읽기
    source = Path(__file__).resolve().parent  # 저장소의 이 예제 위치
    work = args.out.resolve()  # 결과를 저장할 절대 경로
    work.mkdir(parents=True, exist_ok=False)  # 이미 있는 결과 폴더는 거절
    gcc, qemu = args.gcc.resolve(), args.qemu.resolve()  # 두 실제 도구의 절대 경로
    names = ['functions.S', 'abi_probe.S', 'startup.S', 'driver.c', 'linker.ld']  # ELF를 만드는 실제 입력 파일
    for name in names:  # 원본 대신 작업 폴더에서 컴파일
        shutil.copyfile(source / name, work / name)  # 소스 바이트를 그대로 복사
    source_hashes = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in names + ['run.py']}  # 검사한 원본 식별
    if args.negative_byte_sign:  # 정상 원본은 건드리지 않는 결함 주입
        text = (work / 'functions.S').read_text(encoding='utf-8')  # 작업 복사본의 함수 코드
        if text.count('lbu t1, 0(t0)') != 1:  # 정확한 한 명령에만 결함 적용
            raise ValueError('byte load mutation target count')  # 모호한 위치를 임의로 변경하지 않기
        (work / 'functions.S').write_text(text.replace('lbu t1, 0(t0)', 'lb t1, 0(t0)'), encoding='utf-8', newline='\n')  # 부호 확장 결함을 작업 복사본에만 저장
    report = {'commands': [], 'source_sha256': source_hashes, 'negative_byte_sign': args.negative_byte_sign}  # 실행 보고서의 기본 구조
    environment = dict(os.environ)  # 현재 실행 환경을 자식에게 전달
    environment.update(TEMP='.', TMP='.', TMPDIR='.')  # 임시 산출물도 지정한 빌드 폴더 안에 생성
    def command(label, argv):  # 실제 도구 명령 하나와 결과 기록
        completed = subprocess.run([str(value) for value in argv], cwd=work, env=environment, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)  # 셸 해석 없이30초 이내 실행
        item = {'name': label, 'command': [str(value) for value in argv], 'cwd': str(work), 'returncode': completed.returncode, 'stdout': completed.stdout, 'stderr': completed.stderr}  # 도구의 원래 종료·출력 보존
        report['commands'].append(item)  # 전체 실행 순서에 추가
        (work / (label + '.json')).write_text(json.dumps(item, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')  # 개별 결과도 저장
        return item  # 다음 검증 단계에서 결과 사용
    command('gcc_version', [gcc, '--version'])  # 설치된 컴파일러 판본 확인
    command('qemu_version', [qemu, '--version'])  # 설치된 CPU 에뮬레이터 판본 확인
    flags = ['-march=rv32i', '-mabi=ilp32', '-mcmodel=medany', '-mno-relax', '-msmall-data-limit=0', '-O2', '-g', '-std=c11', '-ffreestanding', '-fno-builtin', '-fno-pic', '-fno-pie', '-fno-stack-protector', '-Wall', '-Wextra', '-Werror', '-nostdlib', '-Wl,--no-relax', '-Tlinker.ld']  # 기본 정수 ISA와32비트 ABI로 제한
    built = command('compile', [gcc, *flags, 'startup.S', 'functions.S', 'abi_probe.S', 'driver.c', '-o', 'program.elf'])  # 실제 RISC-V ELF 생성
    if built['returncode'] != 0:  # 컴파일 실패를 CPU 기능 결과와 구분
        raise RuntimeError('compile failed; see compile.json')  # 원래 도구 로그를 근거로 중단
    readelf = gcc.with_name(gcc.name.replace('gcc', 'readelf'))  # 같은 도구 모음의 ELF 검사기
    attributes = command('elf_attributes', [readelf, '-h', '-A', 'program.elf'])  # ELF32·RISC-V·명령 확장 속성 확인
    if attributes['returncode'] or not re.search(r'Class:\s+ELF32', attributes['stdout']) or 'rv32i2p1' not in attributes['stdout']:  # 호스트 ELF나 다른 ISA 결과를 거절
        raise RuntimeError('unexpected ELF class or ISA')  # 실제 빌드 타깃의 증거가 없으면 실행 성공으로 쓰지 않기
    objdump = gcc.with_name(gcc.name.replace('gcc', 'objdump'))  # 실제 기계어를 읽을 역어셈블러
    disassembly = command('disassembly', [objdump, '-d', '-M', 'no-aliases', 'program.elf'])  # 의사 명령이 풀린 실제 ELF 코드 기록
    if disassembly['returncode'] != 0:  # 기계어 관측 실패 구분
        raise RuntimeError('objdump failed')  # 없는 역어셈블 결과를 만들지 않기
    (work / 'disassembly.txt').write_text(disassembly['stdout'], encoding='utf-8')  # 전체 명령 목록을 빌드 자료에 보관
    executed = command('qemu_cpu', [qemu, '-machine', 'virt', '-cpu', 'rv32i', '-m', '32M', '-bios', 'none', '-kernel', 'program.elf', '-display', 'none', '-serial', 'stdio', '-monitor', 'none', '-no-reboot', '-d', 'in_asm', '-D', 'qemu-instructions.log'])  # RV32I 가상 CPU에서 ELF를 실제 명령으로 실행
    marker = 'FAIL RV32I unsigned byte demo' if args.negative_byte_sign else 'PASS RV32I '  # 정상과 의도적 부호 오류의 기대 결과 분리
    expected_code = 1 if args.negative_byte_sign else 0  # finisher가 내보낼 실제 프로세스 종료 코드
    if executed['returncode'] != expected_code or marker not in executed['stdout']:  # 종료0만으로 기능 통과를 판단하지 않기
        raise RuntimeError('CPU result mismatch; see qemu_cpu.json')  # 실제 UART·종료 결과와 기대가 다른 경우
    report['result'] = 'EXPECTED_FUNCTIONAL_FAILURE' if args.negative_byte_sign else 'PASS'  # 음성 대조 실패를 정상 회로 성공과 구분
    report['checks'] = {key: int(value, 16) for key, value in re.findall(r'(field_checks|checksum_checks|abi_checks|total_checks)=([0-9a-f]{8})', executed['stdout'])}  # 실제 출력의16진수 집계를 정수로 변환
    report['built_source_sha256'] = {name: hashlib.sha256((work / name).read_bytes()).hexdigest() for name in names}  # 결함 복사본과 정상 원본의 해시 구분
    report['elf_sha256'] = hashlib.sha256((work / 'program.elf').read_bytes()).hexdigest()  # 실행한 실제 기계어 식별
    report['qemu_instruction_log_sha256'] = hashlib.sha256((work / 'qemu-instructions.log').read_bytes()).hexdigest()  # CPU 명령 블록 로그 식별
    report['environment_overrides'] = {'TEMP': '.', 'TMP': '.', 'TMPDIR': '.'}  # 빌드 위치 재현에 필요한 환경
    (work / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')  # 최종 실제 실행 기록 저장
    print(executed['stdout'], end='')  # RISC-V 펌웨어가 출력한 원래 결과 전달
    print('REPORT', work / 'report.json')  # 빌드 자료 위치 안내
    return 0  # 기대한 정상 또는 음성 대조가 확인된 러너의 성공

if __name__ == '__main__':  # 스크립트로 실행할 때만 도구 호출
    raise SystemExit(main())  # 러너 자체 종료 코드 전달

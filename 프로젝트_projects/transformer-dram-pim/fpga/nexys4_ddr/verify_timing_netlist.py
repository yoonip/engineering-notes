"""배선 지연 SDF를 포함한 실제 Nexys 회로의 R/RO timing xsim 검증.

--prepare-only는 export/xvlog/xelab까지만 실행하며 실제 UART 시험 PASS가 아니다.
그 뒤 같은 --stage와 corner/delay에서 --reuse-prepared로 xsim을 실행할 수 있다.
functional 도구·원본 routed.dcp·보드 가중치·bitstream은 수정하지 않는다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from fpga.nexys4_ddr.verify_netlist import sha256, testbench, verification_plan, validate_simulation_output
from model.gpt_q88 import load_checkpoint
from tools.console_text import decode_console_bytes
from fpga.nexys4_ddr.compare_timing_exports import compare_exports
from fpga.nexys4_ddr.lexical_timing_names import translate_exports, build_inventory_from_export

REFERENCES = [
    'https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/Generating-a-Timing-Netlist',
    'https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/Using-AMD-Simulation-Libraries',
    'https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/Running-Timing-Simulation',
    'https://docs.amd.com/r/2024.1-English/ug900-vivado-logic-simulation/xelab-xvhdl-and-xvlog-xsim-Command-Options',
    'https://docs.amd.com/r/2024.1-English/ug835-vivado-tcl-commands/write_verilog',
    'https://docs.amd.com/r/2024.1-English/ug835-vivado-tcl-commands/write_sdf',
    'https://docs.amd.com/r/2024.1-English/ug835-vivado-tcl-commands/rename_cell',
    'https://docs.amd.com/r/2024.1-English/ug835-vivado-tcl-commands/report_property',
    'https://adaptivesupport.amd.com/s/article/000036878?language=en_US',
]
PRIMITIVES = ('MMCME2_ADV', 'MMCME2_BASE', 'BUFG', 'IBUF', 'OBUF', 'DSP48E1',
              'FDRE', 'FDCE', 'LUT6', 'RAMD64E', 'RAMS64E', 'RAMD32', 'RAMS32', 'RAM64M', 'RAM32M')


def lexical_export_tcl(corner: str) -> str:
    """원본 export와 primitive 이름 inventory를 읽으며 CAD rename는 수행하지 않는다.

    Python이 원본 module graph에서 inventory를 만들므로 대규모 cell property
    query도 수행하지 않는다. 변경 없는 원본 설계의 전체 net NAME/ROUTE를
    전후 정확히 비교한다. 실제 변환은 Python의 허용 token span에만 수행한다.
    """
    return (f'write_verilog -force -mode timesim -sdf_anno true -sdf_file design_timing.sdf before_timesim.v\n'
            f'write_sdf -force -mode timesim -process_corner {corner} -multithread 1 before_timing.sdf\n')+r'''
set taskAllNets [get_nets -hier]
set taskNetNamesBefore [get_property NAME $taskAllNets]
set taskRoutesBefore [get_property ROUTE $taskAllNets]
set taskFile [open route_vector_before.txt w]
puts $taskFile $taskRoutesBefore
close $taskFile
if {[get_property NAME $taskAllNets] ne $taskNetNamesBefore} { error "Original net names changed" }
set taskRoutesAfter [get_property ROUTE $taskAllNets]
set taskFile [open route_vector_after.txt w]
puts $taskFile $taskRoutesAfter
close $taskFile
if {$taskRoutesBefore ne $taskRoutesAfter} { error "Original physical ROUTE changed" }
puts "TIMING_RENAME_COUNT: 0"
puts "TIMING_ROUTE_CHECK_COUNT: [llength $taskAllNets]"
puts "TIMING_EXPORT_INVARIANCE_MODE: lexical_original_export_token_inversion_and_all_net_routes"
'''


def bulk_safe_instance_tcl(corner: str, limit: int = 0) -> str:
    """전체 내보내기 내용 비교와 모든 net ROUTE 일괄 비교를 위한 이름 변환이다.

    개별 cell의 수백 개 파생 메타데이터를 질의하는 방식 대신, 변경 전 timing
    Verilog/SDF를 보존한다. Python 비교기가 변경 후 파일의 안전 이름을 복원해
    전체 primitive 속성·parameter·핀 연결·procedural body·모든 지연/check를
    비교한다. Tcl은 모든 net을 같은 collection 순서로 유지하여 이름/ROUTE도
    전후 정확히 비교한다. limit은 독립 소형 실험용이며 정상 내보내기는 0이다.
    실제 flatten 결과에는 p_0_out_inferred__25/x_vec[2][11]_i_11처럼 하나의
    escaped leaf 안에 slash가 들어간다. 따라서 NAME의 마지막 slash로 계층을
    자르지 않고 HIERARCHICALNAME의 최종 escaped identifier 전체를 사용한다.
    """
    if corner not in ('slow', 'fast') or limit < 0:
        raise ValueError('잘못된 corner 또는 rename limit입니다.')
    return (f'write_verilog -force -mode timesim -sdf_anno true -sdf_file design_timing.sdf before_timesim.v\n'
            f'write_sdf -force -mode timesim -process_corner {corner} -multithread 1 before_timing.sdf\n'
            f'set taskRenameLimit {limit}\n') + r'''
set taskAllNets [get_nets -hier]
set taskNetNamesBefore [get_property NAME $taskAllNets]
set taskRoutesBefore [get_property ROUTE $taskAllNets]
set taskFile [open route_vector_before.txt w]
puts $taskFile $taskRoutesBefore
close $taskFile
set taskRenameMap [open instance_name_map.tsv w]
puts $taskRenameMap "original_name\tsafe_name\toriginal_hierarchicalname\tsafe_hierarchicalname\tref_name\tloc\tbel\tproperties_checked\tpins_checked"
set taskCellNames [dict create]
foreach taskCell [get_cells -hier] { dict set taskCellNames [get_property NAME $taskCell] 1 }
set taskRenameCount 0
foreach taskCell [get_cells -hier -filter {IS_PRIMITIVE == 1}] {
    set taskOldName [get_property NAME $taskCell]
    if {[string first {[} $taskOldName] < 0 && [string first {]} $taskOldName] < 0} { continue }
    set taskOldHier [get_property HIERARCHICALNAME $taskCell]
    # NAME can contain / inside a flattened escaped leaf. Only the final
    # Verilog escaped identifier in HIERARCHICALNAME defines the true leaf.
    # A bracket in a parent does not require renaming a normal final leaf.
    if {[string index $taskOldHier end] ne " "} { continue }
    set taskHierSplit [string last "\\" $taskOldHier]
    if {$taskHierSplit < 0} {
        error "Unexpected original Verilog hierarchical name: $taskOldName $taskOldHier"
    }
    set taskLeaf [string range $taskOldHier [expr {$taskHierSplit+1}] end-1]
    if {[string first {[} $taskLeaf] < 0 && [string first {]} $taskLeaf] < 0} { continue }
    set taskLeafStart [expr {[string length $taskOldName]-[string length $taskLeaf]}]
    if {$taskLeafStart < 0 || [string range $taskOldName $taskLeafStart end] ne $taskLeaf} {
        error "NAME and Verilog escaped leaf disagree: $taskOldName $taskOldHier"
    }
    set taskSeparator [expr {$taskLeafStart-1}]
    binary scan [encoding convertto utf-8 $taskLeaf] H* taskLeafHex
    set taskSafeLeaf "timing_escaped_$taskLeafHex"
    set taskNewName "[string range $taskOldName 0 $taskSeparator]$taskSafeLeaf"
    if {[dict exists $taskCellNames $taskNewName]} { error "Safe cell name collision: $taskNewName" }
    set taskExpectedHier "[string range $taskOldHier 0 [expr {$taskHierSplit-1}]]$taskSafeLeaf"
    set taskRef [get_property REF_NAME $taskCell]
    set taskLoc [get_property LOC $taskCell]
    set taskBel [get_property BEL $taskCell]
    rename_cell -to $taskNewName $taskCell
    if {[get_property NAME $taskCell] ne $taskNewName ||
        [get_property HIERARCHICALNAME $taskCell] ne $taskExpectedHier ||
        [get_property REF_NAME $taskCell] ne $taskRef ||
        [get_property LOC $taskCell] ne $taskLoc || [get_property BEL $taskCell] ne $taskBel} {
        error "Cell name/type/physical location changed unexpectedly: $taskOldName"
    }
    dict set taskCellNames $taskNewName 1
    puts $taskRenameMap "$taskOldName\t$taskNewName\t$taskOldHier\t$taskExpectedHier\t$taskRef\t$taskLoc\t$taskBel\t0\t0"
    incr taskRenameCount
    if {$taskRenameCount % 1000 == 0} { puts "TIMING_RENAME_PROGRESS: $taskRenameCount" }
    if {$taskRenameLimit > 0 && $taskRenameCount >= $taskRenameLimit} { break }
}
close $taskRenameMap
if {[get_property NAME $taskAllNets] ne $taskNetNamesBefore} { error "A net name changed during cell rename" }
set taskRoutesAfter [get_property ROUTE $taskAllNets]
set taskFile [open route_vector_after.txt w]
puts $taskFile $taskRoutesAfter
close $taskFile
if {$taskRoutesBefore ne $taskRoutesAfter} { error "A physical net ROUTE changed during cell rename" }
puts "TIMING_RENAME_COUNT: $taskRenameCount"
puts "TIMING_ROUTE_CHECK_COUNT: [llength $taskAllNets]"
puts "TIMING_EXPORT_INVARIANCE_MODE: whole_export_and_all_net_routes"
'''


def safe_instance_tcl() -> str:
    """2024.1 escaped-name SDF 적용 문제를 이름만 바꾸어 우회하는 Tcl이다.

    원본 DCP에 저장하지 않는다. 현재 stage의 메모리상 design에서 []가 포함된
    primitive leaf 이름을 UTF-8 바이트의 hex로 일대일 변환한다. 같은 design에서
    netlist와 SDF를 함께 내보내야 두 파일이 같은 이름을 참조한다. 매 rename은
    NAME/HIERARCHICALNAME은 요청한 새 이름 및 Verilog 계층 표기와 같은지 별도로 검사한다. 이 두
    이름 메타데이터 이외의 모든 cell property와 pin→net 연결이 동일한지 검사하고,
    영향을 받은 net의 ROUTE도 모두 비교한다. 이름 collision/속성/배선 변화는 즉시 실패다.
    """
    return r'''
proc timing_pin_connections {taskCell} {
    set taskConnections [dict create]
    set taskCellName [get_property NAME $taskCell]
    foreach taskPin [get_pins -quiet -of_objects $taskCell] {
        set taskPinName [get_property NAME $taskPin]
        set taskPortName [string range $taskPinName [expr {[string length $taskCellName]+1}] end]
        set taskNets [get_nets -quiet -of_objects $taskPin]
        set taskNames [list]
        foreach taskNet $taskNets { lappend taskNames [get_property NAME $taskNet] }
        dict set taskConnections $taskPortName [lsort $taskNames]
    }
    return $taskConnections
}
proc timing_cell_properties {taskCell} {
    # report_property batches C++ database reads; per-property calls for 43k cells
    # would take hours. Its rows retain type/read-only/value. If any property is
    # absent from the report, query that property explicitly rather than omit it.
    set taskReported [dict create]
    foreach taskLine [split [report_property -all -return_string $taskCell] "\n"] {
        set taskValue ""
        if {[regexp {^[ \t]*(\S+)[ \t]+(\S+)[ \t]+(true|false|0|1)(?:[ \t]+(.*))?$} $taskLine -> taskProperty taskType taskReadOnly taskValue]} {
            if {[dict exists $taskReported $taskProperty]} { error "Duplicate cell property row: $taskProperty" }
            dict set taskReported $taskProperty [list $taskType $taskReadOnly $taskValue]
        }
    }
    set taskProperties [dict create]
    foreach taskProperty [list_property $taskCell] {
        if {$taskProperty in {NAME HIERARCHICALNAME}} { continue }
        if {[dict exists $taskReported $taskProperty]} {
            dict set taskProperties $taskProperty [dict get $taskReported $taskProperty]
        } else {
            dict set taskProperties $taskProperty [list explicit_get [get_property $taskProperty $taskCell]]
        }
    }
    return $taskProperties
}
set taskRenameMap [open instance_name_map.tsv w]
puts $taskRenameMap "original_name\tsafe_name\toriginal_hierarchicalname\tsafe_hierarchicalname\tref_name\tloc\tbel\tproperties_checked\tpins_checked"
set taskRenameCount 0
set taskRoutesBefore [dict create]
set taskCellNames [dict create]
foreach taskNamedCell [get_cells -hier] {
    dict set taskCellNames [get_property NAME $taskNamedCell] 1
}
foreach taskCell [get_cells -hier -filter {IS_PRIMITIVE == 1}] {
    set taskOldName [get_property NAME $taskCell]
    if {[string first {[} $taskOldName] < 0 && [string first {]} $taskOldName] < 0} { continue }
    set taskOldHier [get_property HIERARCHICALNAME $taskCell]
    # A flattened escaped leaf can include /: NAME's last slash is not
    # necessarily a hierarchy boundary. Preserve the actual Verilog parent.
    if {[string index $taskOldHier end] ne " "} { continue }
    set taskHierSplit [string last "\\" $taskOldHier]
    if {$taskHierSplit < 0} {
        error "Unexpected original Verilog hierarchical name: $taskOldName $taskOldHier"
    }
    set taskLeaf [string range $taskOldHier [expr {$taskHierSplit+1}] end-1]
    if {[string first {[} $taskLeaf] < 0 && [string first {]} $taskLeaf] < 0} { continue }
    set taskLeafStart [expr {[string length $taskOldName]-[string length $taskLeaf]}]
    if {$taskLeafStart < 0 || [string range $taskOldName $taskLeafStart end] ne $taskLeaf} {
        error "NAME and Verilog escaped leaf disagree: $taskOldName $taskOldHier"
    }
    set taskSeparator [expr {$taskLeafStart-1}]
    binary scan [encoding convertto utf-8 $taskLeaf] H* taskLeafHex
    set taskSafeLeaf "timing_escaped_$taskLeafHex"
    set taskNewName "[string range $taskOldName 0 $taskSeparator]$taskSafeLeaf"
    set taskExpectedHier "[string range $taskOldHier 0 [expr {$taskHierSplit-1}]]$taskSafeLeaf"
    if {[dict exists $taskCellNames $taskNewName]} { error "Safe cell name collision: $taskNewName" }
    set taskProperties [timing_cell_properties $taskCell]
    set taskConnections [timing_pin_connections $taskCell]
    foreach taskPin [get_pins -quiet -of_objects $taskCell] {
        foreach taskNet [get_nets -quiet -of_objects $taskPin] {
            set taskNetName [get_property NAME $taskNet]
            if {![dict exists $taskRoutesBefore $taskNetName]} {
                dict set taskRoutesBefore $taskNetName [get_property ROUTE $taskNet]
            }
        }
    }
    rename_cell -to $taskNewName $taskCell
    # The Vivado typed cell object remains the same object after rename. Avoid
    # tens of thousands of global wildcard name searches; verify its new NAME.
    set taskNewCell $taskCell
    dict set taskCellNames $taskNewName 1
    if {[get_property NAME $taskNewCell] ne $taskNewName ||
        [get_property HIERARCHICALNAME $taskNewCell] ne $taskExpectedHier} {
        error "Renamed cell does not have the exact requested name: $taskOldName"
    }
    set taskPropertiesAfter [timing_cell_properties $taskNewCell]
    if {[lsort [dict keys $taskPropertiesAfter]] ne [lsort [dict keys $taskProperties]]} {
        error "Available cell properties changed during name-only export: $taskOldName"
    }
    foreach taskProperty [dict keys $taskProperties] {
        if {[dict get $taskPropertiesAfter $taskProperty] ne [dict get $taskProperties $taskProperty]} {
            error "Cell property changed during name-only export: $taskOldName $taskProperty"
        }
    }
    set taskConnectionsAfter [timing_pin_connections $taskNewCell]
    if {[lsort [dict keys $taskConnectionsAfter]] ne [lsort [dict keys $taskConnections]]} {
        error "Cell pin set changed during name-only export: $taskOldName"
    }
    foreach taskPortName [dict keys $taskConnections] {
        if {[dict get $taskConnectionsAfter $taskPortName] ne [dict get $taskConnections $taskPortName]} {
            error "Pin/net connectivity changed during name-only export: $taskOldName $taskPortName"
        }
    }
    puts $taskRenameMap "$taskOldName\t$taskNewName\t$taskOldHier\t$taskExpectedHier\t[get_property REF_NAME $taskNewCell]\t[get_property LOC $taskNewCell]\t[get_property BEL $taskNewCell]\t[dict size $taskProperties]\t[dict size $taskConnections]"
    incr taskRenameCount
    if {$taskRenameCount % 1000 == 0} { puts "TIMING_RENAME_PROGRESS: $taskRenameCount" }
}
set taskRoutesChecked 0
foreach taskNet [get_nets -hier] {
    set taskNetName [get_property NAME $taskNet]
    if {[dict exists $taskRoutesBefore $taskNetName]} {
        if {[get_property ROUTE $taskNet] ne [dict get $taskRoutesBefore $taskNetName]} {
            error "Physical ROUTE changed during name-only export: $taskNetName"
        }
        incr taskRoutesChecked
    }
}
if {$taskRoutesChecked != [dict size $taskRoutesBefore]} { error "A connected net disappeared during rename" }
close $taskRenameMap
puts "TIMING_RENAME_COUNT: $taskRenameCount"
puts "TIMING_ROUTE_CHECK_COUNT: $taskRoutesChecked"
'''


def diagnostics(text: str) -> dict:
    """원문 경고를 보존하고 SDF 오류/경고와 timing violation을 별도로 센다.

    경고를 끄거나 ERROR를 WARNING으로 낮추는 simulator 옵션을 쓰지 않는다.
    JSON에는 최대100개 예시를 담고 원문 전체는 단계별 console.log에 남긴다.
    """
    lines = text.splitlines()
    warnings = [line for line in lines if re.search(r'\b(?:WARNING|CRITICAL WARNING)\b', line, re.I)]
    errors = [line for line in lines if re.search(r'^\s*(?:ERROR|FATAL)\s*:', line, re.I)]
    sdf_issues = [line for line in lines if re.search(r'sdf|annotat', line, re.I)
                  and re.search(r'warning|error|fail|cannot|unable|not found|unmatched|mismatch', line, re.I)]
    # xsim의 일반 Timing violation 문구뿐 아니라 compound $setuphold/$recrem,
    # clock period/pulse width check 진단도 놓치지 않는다. primitive 소스의 check
    # 선언만으로 실패하지 않고 violation/violated 등의 실제 진단 문맥을 확인한다.
    violations = [line for line in lines if re.search(
        r'timing\s+(?:check\s+)?violation|'
        r'(?:setuphold|setup|hold|recrem|recovery|removal|width|period|skew|timeskew|fullskew|nochange)\s+violation|'
        r'\$(?:setuphold|setup|hold|recrem|recovery|removal|width|period|skew|timeskew|fullskew|nochange)\b.*(?:violation|violated|failure|failed)',
        line, re.I)]
    return {'warning_count': len(warnings), 'error_count': len(errors),
            'sdf_issue_count': len(sdf_issues), 'timing_violation_count': len(violations),
            'warnings_sample': warnings[:100], 'errors_sample': errors[:100],
            'sdf_issues_sample': sdf_issues[:100], 'timing_violations_sample': violations[:100]}


def annotation_evidence(log_path: Path) -> dict:
    """xelab의 적용 시작·완료 두 메시지와 경고 0개를 함께 확인한다.

    2024.1에서는 수만 개의 cell 적용을 생략해도 'successful' INFO가 나온다.
    따라서 성공 INFO 하나만으로 SDF 적용을 인정하지 않는다. 실제 UART 시험
    전의 이 증거는 elaboration 증거이며 최종 sdf_annotated/PASS와 구분한다.
    """
    console = decode_console_bytes(log_path.read_bytes())
    diag = diagnostics(console)
    starts = re.findall(r'^INFO: \[XSIM 43-3451\].*$', console, re.M)
    successes = re.findall(r'^INFO: \[XSIM 43-3452\].*$', console, re.M)
    if (len(starts) != 1 or len(successes) != 1
            or any('"design_timing.sdf"' not in line or '"tb_nexys_netlist/dut"' not in line
                   for line in starts + successes)
            or diag['error_count'] or diag['sdf_issue_count'] or diag['timing_violation_count']):
        raise RuntimeError('xelab SDF 적용 시작/완료/경고 0개/정확한 DUT 범위의 결합 증거가 부족합니다.')
    return {'verified': True, 'stage': 'elaboration', 'simulation_performed': False,
            'log_sha256': sha256(log_path), 'start_message': starts[0],
            'success_message': successes[0], 'diagnostics': diag}


def inspect_sdf(path: Path) -> dict:
    """파일 존재만이 아니라 실제 cell·배선·경로·timing check 지연 레코드를 확인한다."""
    text = path.read_text(encoding='ascii')
    result = {'file': path.name, 'sha256': sha256(path), 'bytes': path.stat().st_size,
              'timescale': re.findall(r'\(TIMESCALE\s+([^\)]+)\)', text),
              'cell_records': len(re.findall(r'\(CELL\s', text)),
              'interconnect_records': len(re.findall(r'\(INTERCONNECT\s', text)),
              'iopath_records': len(re.findall(r'\(IOPATH\s', text)),
              'timingcheck_records': len(re.findall(r'\(TIMINGCHECK\s', text))}
    if min(result['cell_records'], result['interconnect_records'], result['iopath_records']) <= 0:
        raise RuntimeError('SDF에 실제 cell/interconnect/IOPATH 지연 레코드가 없습니다.')
    return result


def compile_policy(tokens: list[str]) -> dict:
    """실제 xelab 명령/Compile_Options에서 pulse 정책과 최적화 수준을 읽는다.

    kernel을 다른 정책으로 다시 해석하지 않는다. 명시한 reject 옵션은
    정확히 한 번 있어야 하고, error 옵션을 생략한 옛100% kernel은
    XSim2024.1의 문서상 기본100%로만 해석한다. O2/O3는 C++ simulator
    생성 최적화이며 netlist의 실제 FPGA 자원이나 클록을 바꾸지 않는다.
    """
    def value(flag: str, default: int | None = None) -> int:
        positions = [index for index, token in enumerate(tokens) if token == flag]
        if not positions and default is not None:
            return default
        if len(positions) != 1 or positions[0] + 1 >= len(tokens):
            raise RuntimeError(f'실제 compile 명령의 {flag} 증거가 유일하지 않습니다.')
        try:
            result = int(tokens[positions[0] + 1])
        except ValueError as error:
            raise RuntimeError(f'실제 compile 명령의 {flag} 값이 정수가 아닙니다.') from error
        if result not in (0, 50, 100):
            raise RuntimeError(f'실제 compile 명령의 {flag} 값이 지원 범위를 벗어납니다.')
        return result
    levels = [int(token[3:]) for token in tokens if re.fullmatch(r'--O[0-3]', token)]
    if len(levels) != 1 or levels[0] not in (2, 3):
        raise RuntimeError('실제 compile 명령에서 유일한 --O2/--O3 증거가 필요합니다.')
    policy = {'pulse_r_percent': value('--pulse_r'),
              'pulse_int_r_percent': value('--pulse_int_r'),
              'pulse_e_percent': value('--pulse_e', 100),
              'pulse_int_e_percent': value('--pulse_int_e', 100),
              'optimization_level': levels[0]}
    if (policy['pulse_r_percent'] > policy['pulse_e_percent']
            or policy['pulse_int_r_percent'] > policy['pulse_int_e_percent']):
        raise RuntimeError('실제 compile 명령에서 pulse reject limit은 error limit 이하여야 합니다.')
    return policy


def verify_prepared_identity(stored: dict, requested: dict, options_path: Path) -> dict:
    """보존 kernel의 정책을 실제 compile 옵션과 함께 확인한 뒤 재사용을 허용한다.

    새로 추가한 r/optimization 세 필드가 옛 manifest에 없을 수 있다. 이때
    원본 JSON을 수정하거나 임의의 새 값을 넣지 않는다. 요청이 기존0/0/O2이고
    실제 Compile_Options도 그 값일 때만 비교용 사본을 보완한다. e 필드가
    없는 과거 manifest, 또는50/100/O3 요청에는 이 예외를 적용하지 않는다.
    실제 옵션·원본 manifest SHA는 새 보고서에 연결되므로 재검토할 수 있다.
    """
    legacy = {'pulse_r_percent': 0, 'pulse_int_r_percent': 0, 'optimization_level': 2}
    fixed_keys = set(legacy)
    if ({key: val for key, val in stored.items() if key not in fixed_keys}
            != {key: val for key, val in requested.items() if key not in fixed_keys}):
        raise RuntimeError('준비한 DCP/model/corner/delay/baud/testbench 또는 pulse 정책이 현재 요청과 다릅니다.')
    normalized = dict(stored)
    missing = [key for key in legacy if key not in stored]
    for key in missing:
        if requested.get(key) != legacy[key]:
            raise RuntimeError('옛 kernel의 미기록 r/optimization은 검증된0/0/O2에서만 재사용합니다. 새 정책은 새 xelab이 필요합니다.')
        normalized[key] = legacy[key]
    if normalized != requested:
        raise RuntimeError('준비한 kernel의 pulse reject/최적화 정책이 현재 요청과 다릅니다.')
    if not options_path.is_file():
        raise RuntimeError('kernel의 실제 Compile_Options.txt가 없어 r/optimization을 검증할 수 없습니다.')
    actual = compile_policy(shlex.split(options_path.read_text(encoding='utf-8-sig')))
    if any(actual[key] != requested[key] for key in actual):
        raise RuntimeError('실제 Compile_Options.txt의 pulse/optimization이 요청 정체성과 다릅니다.')
    return {'verified': True, 'legacy_missing_fields': missing,
            'legacy_inferred_values': {key: legacy[key] for key in missing},
            'original_manifest_mutated': False,
            'compile_options_sha256': sha256(options_path), 'actual_compile_policy': actual}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, default=ROOT/'build/nexys4_ddr/board/routed.dcp')
    parser.add_argument('--model-checkpoint', type=Path,
                        default=ROOT/'output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json')
    parser.add_argument('--vivado-root', type=Path, default=Path('C:/Xilinx/Vivado/2024.1'))
    parser.add_argument('--stage', type=Path)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--corner', choices=('slow', 'fast'), default='slow')
    parser.add_argument('--delay-mode', choices=('min', 'typ', 'max'), default='max')
    parser.add_argument('--pulse-reject-limit', type=int, choices=(0,50,100), default=0,
                        help='path/interconnect pulse reject limit(%%); 0=UG900 권고, 50/100=별도 pulse 필터 실험')
    parser.add_argument('--pulse-error-limit', type=int, choices=(0,50,100), default=100,
                        help='path/interconnect pulse error limit(%%); reject limit 이상이어야 함; 100=vendor 기본')
    parser.add_argument('--interconnect-pulse-reject-limit', type=int, choices=(0,50,100),
                        help='배선 pulse reject 별도 지정; 생략하면 --pulse-reject-limit과 동일')
    parser.add_argument('--interconnect-pulse-error-limit', type=int, choices=(0,50,100),
                        help='배선 pulse error 별도 지정; 생략하면 --pulse-error-limit과 동일')
    parser.add_argument('--optimization', type=int, choices=(2,3), default=2,
                        help='xelab simulator 생성 최적화 --O2/--O3; 회로·SDF 지연·timing check는 유지')
    parser.add_argument('--host-baud', type=int, default=115200)
    parser.add_argument('--timeout', type=int, default=3600, help='각 tool 단계의 벽시계 초')
    parser.add_argument('--prepare-only', action='store_true', help='export/compile/elaboration만 실행; UART 시험 안 함')
    parser.add_argument('--reuse-prepared', action='store_true', help='같은 stage의 해시 검증된 snapshot을 재사용해 xsim')
    parser.add_argument('--preparation-source-result', type=Path,
                        help='재사용 snapshot을 준비한 보존 result.json; 원본 tool 명령과 해시를 연결')
    parser.add_argument('--resume-export', action='store_true',
                        help='기존 export 성공 자료를 해시/조건 검사하고 비교기·compile·xsim부터 계속')
    parser.add_argument('--prior-result', type=Path,
                        help='--resume-export 대상의 기존 실패/준비 result.json; export exit0 증거 보존')
    parser.add_argument('--safe-instance-names', action='store_true',
                        help='2024.1 SDF escaped-name 문제 우회; leaf 이름만 hex 변환, 전체 Verilog/SDF/ROUTE 전후 비교')
    parser.add_argument('--lexical-safe-instance-names', action='store_true',
                        help='CAD rename 없이 원본 export의 등록된 이름 token만 변환; inverse byte/hash 및 전체구조 검증')
    parser.add_argument('--per-cell-property-checks', action='store_true',
                        help='추가 진단용 느린 개별 cell 전체속성/핀 검사; 기본은 전체 내보내기/모든 net ROUTE 비교')
    args = parser.parse_args()
    if args.lexical_safe_instance_names:
        args.safe_instance_names = True
        if args.per_cell_property_checks:
            parser.error('lexical 변환에는 CAD per-cell rename 속성 검사를 함께 사용하지 않습니다.')
    if args.prepare_only and args.reuse_prepared:
        parser.error('--prepare-only와 --reuse-prepared를 함께 쓰지 마세요.')
    if args.resume_export and (args.reuse_prepared or args.prior_result is None):
        parser.error('--resume-export는 --prior-result가 필요하며 --reuse-prepared와 함께 쓰지 않습니다.')
    if args.per_cell_property_checks and not args.safe_instance_names:
        parser.error('--per-cell-property-checks는 --safe-instance-names와 함께 사용하세요.')
    if args.host_baud <= 0 or args.timeout <= 0:
        parser.error('baud와 timeout은 양수여야 합니다.')
    if args.pulse_reject_limit > args.pulse_error_limit:
        parser.error('--pulse-reject-limit은 --pulse-error-limit 이하여야 합니다.')
    # IOPATH와 INTERCONNECT는 다른 지연 범주다. 선택적으로 독립 정책을
    # 지정하되 생략 시 이전 인터페이스처럼 같은 수치를 두 범주에 전달한다.
    int_reject = (args.pulse_reject_limit if args.interconnect_pulse_reject_limit is None
                  else args.interconnect_pulse_reject_limit)
    int_error = (args.pulse_error_limit if args.interconnect_pulse_error_limit is None
                 else args.interconnect_pulse_error_limit)
    if int_reject > int_error:
        parser.error('interconnect pulse reject limit은 interconnect error limit 이하여야 합니다.')
    tag = f'{args.corner}_{args.delay_mode}'
    if args.safe_instance_names:
        tag += '_safenames'
    if (args.pulse_reject_limit != 0 or args.pulse_error_limit != 100 or args.optimization != 2
            or int_reject != args.pulse_reject_limit or int_error != args.pulse_error_limit):
        tag += f'_r{args.pulse_reject_limit}_e{args.pulse_error_limit}_ir{int_reject}_ie{int_error}_O{args.optimization}'
    stage = (args.stage or Path(tempfile.gettempdir())/f'nexys_timing_{tag}_20261004').resolve()
    output = (args.output_dir or ROOT/'build/nexys4_ddr'/f'timing_netlist_{tag}').resolve()
    if not str(stage).isascii():
        parser.error('stage는 영문/ASCII 경로여야 합니다.')
    if stage == output or stage == args.checkpoint.resolve().parent or output == args.checkpoint.resolve().parent:
        parser.error('stage/output은 서로 다르고 원본 보드 DCP 폴더와도 달라야 합니다.')
    for path in (args.checkpoint, args.model_checkpoint, args.vivado_root/'data/verilog/src/glbl.v'):
        if not path.is_file():
            parser.error(f'필요한 파일이 없습니다: {path}')
    board_path = args.checkpoint.resolve().parent/'result.json'
    if not board_path.is_file():
        parser.error('실제 DCP·가중치·context를 확인할 보드 구현 result.json이 필요합니다.')
    board = json.loads(board_path.read_text(encoding='utf-8-sig'))
    if (board.get('routed_checkpoint', {}).get('sha256') != sha256(args.checkpoint)
            or board.get('checkpoint_sha256') != sha256(args.model_checkpoint)):
        parser.error('보드 구현 보고서와 지정한 DCP/학습 checkpoint 해시가 다릅니다.')
    model = load_checkpoint(args.model_checkpoint)
    if len(model['vocab']) != 65 or model['vocab'][30] != 'R' or model['vocab'][27] != 'O':
        parser.error('현재 시험은 V65/R30/O27 어휘를 사용합니다.')
    if not isinstance(board.get('max_context'), int) or board['max_context'] < 2:
        parser.error('R/RO를 처리할 실제 context 크기가 보드 보고서에 없습니다.')
    plan = verification_plan(model, [30, 27], None)
    bench = testbench(args.host_baud).replace('post-route functional netlist', 'post-route timing netlist')
    # SV unsized integer 4,000,000,000은 signed32 범위를 넘는다. xsim에서 0시각
    # timeout으로 오해석한 사례를 막기 위해 real literal 표기를 반드시 확인한다.
    if '#4000000000.0;' not in bench or '#4000000000;' in bench:
        parser.error('공통 testbench의 가상4초 timeout은 #4000000000.0; real literal여야 합니다.')
    stage.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    # 생성 netlist에 $sdf_annotate를 넣고 --min/typ/maxdelay로 TOOL_CONTROL을 선택한다.
    # 별도 testbench/CLI annotation을 중복 적용하지 않는다. 원본 primitive를 유지한다.
    report = {'mode': 'post_route_sdf_timing_netlist_simulation', 'passed': False,
              'prepared': False, 'simulation_performed': False,
              'physical_board_measured': False, 'physical_programming_performed': False,
              'sdf_annotation_requested': True, 'sdf_annotated': False, 'routed_delays_simulated': False,
              'timing_corner': args.corner, 'delay_mode': args.delay_mode,
              'annotation_method': 'write_verilog generated $sdf_annotate with TOOL_CONTROL',
              'annotation_scope': 'tb_nexys_netlist.dut', 'timing_checks_enabled': True,
              'specify_paths_enabled': True, 'interconnect_delays_enabled': True,
              'transport_interconnect_delays': True,
              'pulse_r_percent': args.pulse_reject_limit, 'pulse_int_r_percent': int_reject,
              'pulse_e_percent': args.pulse_error_limit, 'pulse_int_e_percent': int_error,
              'pulse_error_policy': 'vendor_default_100' if args.pulse_error_limit == 100 else
                  'transport_all_pulses_0' if args.pulse_error_limit == 0 else 'custom_error_50',
              'pulse_reject_policy': 'ug900_recommended_zero' if args.pulse_reject_limit == 0 else
                  f'additional_inertial_filter_{args.pulse_reject_limit}',
              'pulse_reject_matches_ug900_recommendation': args.pulse_reject_limit == 0 and int_reject == 0,
              'interconnect_pulse_reject_policy': 'ug900_recommended_zero' if int_reject == 0 else
                  f'additional_inertial_filter_{int_reject}',
              'interconnect_pulse_error_policy': 'vendor_default_100' if int_error == 100 else
                  'transport_all_pulses_0' if int_error == 0 else 'custom_error_50',
              'optimization_level': args.optimization,
              'libraries': ['simprims_ver', 'secureip'],
              'routed_checkpoint': str(args.checkpoint.resolve()), 'routed_checkpoint_sha256': sha256(args.checkpoint),
              'model_checkpoint_sha256': sha256(args.model_checkpoint),
              'board_implementation_report_sha256': sha256(board_path),
              'core_context': board.get('max_context'), 'cache_storage': board.get('cache_storage', 'unspecified'),
              'board_clock_hz': board.get('clock_hz'), 'ascii_stage': str(stage),
              'safe_instance_names': args.safe_instance_names,
              'name_only_in_memory_export': args.safe_instance_names and not args.lexical_safe_instance_names,
              'lexical_safe_instance_names': args.lexical_safe_instance_names,
              'original_routed_dcp_mutated': False,
              'in_memory_cad_cells_renamed': args.safe_instance_names and not args.lexical_safe_instance_names,
              'name_invariance_mode': 'lexical_original_export_token_inversion_and_all_net_routes'
                  if args.lexical_safe_instance_names else ('per_cell_properties_and_connected_net_routes'
                  if args.per_cell_property_checks else 'whole_export_and_all_net_routes')
                  if args.safe_instance_names else 'no_rename',
              'input_ids': [30, 27], 'expected_logits_raw_q88': plan['rows'],
              'expected_reply_frames': 3, 'expected_exact_logit_comparisons': 130,
              'reply_frames': None, 'exact_logit_comparisons': None,
              'host_baud': args.host_baud, 'simulation_timeout_ns': 4000000000,
              'tool_stage_timeout_seconds': args.timeout, 'simulation_time_unit': '1ps',
              'steps': [], 'diagnostics_by_stage': {}, 'official_references': REFERENCES,
              'notes_ko': ['준비 완료는 실제 UART timing 시험 PASS와 다르다.',
                           'slow/max, fast/min 및 필요 시 다른 corner/delay 조합은 각각 실행한다.',
                           'SDF와 timing warning을 숨기거나 timing check를 끄는 옵션을 사용하지 않는다.',
                           '실제 보드 측정이 아니며 STA/실물 시험을 대체하지 않는다.']}
    manifest_path = stage/'prepared_manifest.json'
    identity = {'dcp_sha256': report['routed_checkpoint_sha256'],
                'model_sha256': report['model_checkpoint_sha256'], 'corner': args.corner,
                'delay_mode': args.delay_mode, 'host_baud': args.host_baud,
                'safe_instance_names': args.safe_instance_names,
                'name_invariance_mode': report['name_invariance_mode'],
                'testbench_sha256': hashlib.sha256(bench.encode('utf-8')).hexdigest()}
    if args.lexical_safe_instance_names:
        identity['lexical_safe_instance_names'] = True
    # Pulse 정책은 compile된 kernel의 동작 일부이다. 100에서 0으로 바꿀 때
    # old kernel을 실행하면 짧은 pulse가 X로 처리되는 동작이 그대로 남는다.
    # 따라서 명시한 두 error limit을 준비 정체성에 포함하고 불일치면 거부한다.
    # 이 정책은 모든 SDF 숫자·specify·setup/hold 등의 timing checker를 유지한다.
    identity['pulse_e_percent'] = args.pulse_error_limit
    identity['pulse_int_e_percent'] = int_error
    identity['pulse_r_percent'] = args.pulse_reject_limit
    identity['pulse_int_r_percent'] = int_reject
    identity['optimization_level'] = args.optimization
    env = os.environ.copy()
    env['XILINX_VIVADO'] = str(args.vivado_root.resolve())
    bin_dir = args.vivado_root/'bin'

    def run_step(name: str, arguments: list[str]) -> None:
        """원문 로그와 자기 PID를 보존하고 timeout 때 자기 프로세스 tree만 정리한다."""
        print(f'진행: timing {name}', flush=True)
        started = time.monotonic()
        logpath = stage/f'{name}.console.log'
        timed_out = False
        cleanup_info = None
        with logpath.open('wb') as log:
            process = subprocess.Popen(arguments, cwd=stage, env=env, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            try:
                code = process.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                code = None
                try:
                    if os.name == 'nt':
                        cleanup = subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                                                 stdout=log, stderr=subprocess.STDOUT, timeout=30)
                        cleanup_info = {'returncode': cleanup.returncode, 'cleaned': cleanup.returncode == 0}
                    else:
                        process.kill()
                        cleanup_info = {'cleaned': True}
                    if cleanup_info['cleaned']:
                        process.wait(timeout=30)
                except Exception as error:
                    cleanup_info = {'cleaned': False, 'error': str(error)}
        report['steps'].append({'stage': name, 'command': arguments, 'returncode': code,
                                'started_process_pid': process.pid, 'timed_out': timed_out,
                                'timeout_process_tree_cleanup': cleanup_info,
                                'wall_seconds': round(time.monotonic()-started, 3),
                                'log': str(output/logpath.name)})
        diag = diagnostics(decode_console_bytes(logpath.read_bytes()))
        report['diagnostics_by_stage'][name] = diag
        if code != 0:
            raise RuntimeError(f'{name} 실패(returncode={code}, timeout={timed_out}); 원문 로그를 확인하세요.')
        if diag['error_count'] or diag['sdf_issue_count'] or diag['timing_violation_count']:
            raise RuntimeError(f'{name}의 SDF 오류/경고 또는 timing violation이 있습니다. 원문을 보존했습니다.')
        print(f'완료: timing {name}', flush=True)

    try:
        if args.reuse_prepared:
            if not manifest_path.is_file():
                raise RuntimeError('같은 stage에 prepared_manifest.json이 없습니다. 먼저 --prepare-only를 실행하세요.')
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            report['prepared_identity_validation'] = verify_prepared_identity(
                manifest['identity'], identity, stage/'xsim.dir/nexys_timing/Compile_Options.txt')
            for filename, digest in manifest['files'].items():
                if not (stage/filename).is_file() or sha256(stage/filename) != digest:
                    raise RuntimeError(f'준비 산출물의 해시가 다릅니다: {filename}')
            # 이미 준비한 simulator를 재사용해도 그 simulator를 만든 실제 명령과
            # 로그의 출처가 필요하다. 결과를 덮어쓰는 canonical result를 출처로
            # 사용하면 해시의 대상이 사라지므로, 별도 보존한 이력 JSON을 요구한다.
            # 과거 준비를 현재 source로 새로 compile했다고 표시하지 않는다.
            if args.preparation_source_result is None:
                raise RuntimeError('--reuse-prepared에는 보존한 --preparation-source-result가 필요합니다.')
            source_path = args.preparation_source_result.resolve()
            if source_path == (output/'result.json').resolve():
                raise RuntimeError('준비 출처 result.json은 새 결과와 다른 보존 경로에 있어야 합니다.')
            source_report = json.loads(source_path.read_text(encoding='utf-8-sig'))
            for key in ('routed_checkpoint_sha256', 'model_checkpoint_sha256',
                        'timing_corner', 'delay_mode', 'ascii_stage', 'safe_instance_names',
                        'name_invariance_mode', 'board_implementation_report_sha256'):
                if source_report.get(key) != report.get(key):
                    raise RuntimeError(f'준비 출처 보고서와 현재 요청 조건이 다릅니다: {key}')
            if (source_report.get('prepared') is not True
                    or source_report.get('timing_netlist_sha256') != sha256(stage/'design_timesim.v')
                    or source_report.get('sdf', {}).get('sha256') != sha256(stage/'design_timing.sdf')):
                raise RuntimeError('준비 출처의 완료 상태/netlist/SDF 해시가 준비 snapshot과 다릅니다.')
            source_steps = [step for step in source_report.get('steps', [])
                            if step.get('stage') in ('export', 'export_reused', 'xvlog', 'xelab')]
            for required_stage in ('xvlog', 'xelab'):
                selected = [step for step in source_steps if step.get('stage') == required_stage]
                if (len(selected) != 1 or selected[0].get('returncode') != 0
                        or selected[0].get('timed_out')):
                    raise RuntimeError(f'준비 출처에 실제 {required_stage} 정상 종료 증거가 없습니다.')
            source_compile = next(step for step in source_steps if step['stage'] == 'xelab')
            actual_source_policy = compile_policy(source_compile['command'])
            if any(actual_source_policy[key] != identity[key] for key in actual_source_policy):
                raise RuntimeError('준비 출처의 실제 xelab 명령과 요청 pulse/optimization 정책이 다릅니다.')
            report['prepared_identity_validation']['source_command_policy_verified'] = True
            if not any(step.get('stage') in ('export', 'export_reused') for step in source_steps):
                raise RuntimeError('준비 출처에 export 또는 보존 export 재사용 증거가 없습니다.')
            source_annotation = source_report.get('elaboration_sdf_annotation_evidence')
            if (not isinstance(source_annotation, dict) or source_annotation.get('verified') is not True
                    or source_annotation.get('log_sha256') != sha256(stage/'xelab.console.log')):
                raise RuntimeError('준비 출처의 SDF annotation 로그 해시가 실제 준비 로그와 다릅니다.')
            try:
                relative_source = source_path.relative_to(ROOT).as_posix()
            except ValueError:
                relative_source = str(source_path)
            report.update({'preparation_source_result_path': relative_source,
                           'preparation_source_result_absolute_path': str(source_path),
                           'preparation_source_result_sha256': sha256(source_path),
                           'preparation_manifest_sha256': sha256(manifest_path),
                           'preparation_tool_steps': source_steps,
                           'preparation_source_elaboration_evidence': source_annotation})
            report['preparation_reused'] = True
            report['preparation_evidence'] = manifest['evidence']
            report.update(manifest['evidence'])
        else:
            if args.resume_export:
                # 비교기 보완 때문에 이미 끝난 수만 개 rename를 다시 실행하지
                # 않는다. 기존 성공 export의 조건·원문·해시를 먼저 검사하고
                # 이어지는 전후 전체 비교와 모든 ROUTE 검사를 다시 수행한다.
                prior = json.loads(args.prior_result.read_text(encoding='utf-8-sig'))
                for key in ('routed_checkpoint_sha256', 'model_checkpoint_sha256',
                            'timing_corner', 'delay_mode', 'ascii_stage', 'safe_instance_names',
                            'name_invariance_mode', 'board_implementation_report_sha256'):
                    if prior.get(key) != report.get(key):
                        raise RuntimeError(f'기존 export와 현재 요청 조건이 다릅니다: {key}')
                export_steps = [step for step in prior.get('steps', []) if step.get('stage') == 'export']
                if len(export_steps) != 1 or export_steps[0].get('returncode') != 0 or export_steps[0].get('timed_out'):
                    raise RuntimeError('기존 보고서에 export 정상 종료 증거가 없습니다.')
                expected_text = ''.join(f'{v&0xffff:04x}\n' for row in plan['rows'] for v in row)
                if ((stage/'expected.mem').read_text(encoding='ascii') != expected_text
                        or (stage/'tb_nexys_netlist.sv').read_text(encoding='utf-8') != bench
                        or sha256(stage/'routed.dcp') != report['routed_checkpoint_sha256']
                        or sha256(stage/'glbl.v') != sha256(args.vivado_root/'data/verilog/src/glbl.v')
                        or sha256(stage/'design_timesim.v') != prior.get('timing_netlist_sha256')
                        or sha256(stage/'design_timing.sdf') != prior.get('sdf', {}).get('sha256')):
                    raise RuntimeError('기존 export의 DUT/model/기준값/TB/glbl/netlist/SDF 해시가 다릅니다.')
                export_diag = diagnostics(decode_console_bytes((stage/'export.console.log').read_bytes()))
                if export_diag['error_count'] or export_diag['sdf_issue_count'] or export_diag['timing_violation_count']:
                    raise RuntimeError('기존 export 원문에 오류/SDF 문제/timing violation이 있습니다.')
                report['export_reused'] = True
                report['prior_result_sha256'] = sha256(args.prior_result)
                report['prior_result'] = str(args.prior_result.resolve())
                # 원래 실행 위치의 절대 경로를 남기면서, 전달 패키지를 다른 폴더에
                # 풀었을 때도 동일한 증거 JSON을 찾을 수 있게 저장소 상대 경로를
                # 함께 기록한다. 파일 내용과 SHA, 기존 export 명령은 바꾸지 않는다.
                try:
                    report['prior_result_path'] = args.prior_result.resolve().relative_to(ROOT).as_posix()
                except ValueError:
                    report['prior_result_path'] = str(args.prior_result.resolve())
                report['steps'].append({'stage': 'export_reused', 'returncode': 0, 'wall_seconds': 0,
                                        'prior_export_step': export_steps[0]})
                report['diagnostics_by_stage']['export'] = export_diag
                print('확인: 기존 export 조건/해시/정상 종료 재검사 완료', flush=True)
            else:
                (stage/'expected.mem').write_text(''.join(f'{v&0xffff:04x}\n' for row in plan['rows'] for v in row),encoding='ascii')
                (stage/'tb_nexys_netlist.sv').write_text(bench, encoding='utf-8')
                shutil.copy2(args.checkpoint, stage/'routed.dcp')
                shutil.copy2(args.vivado_root/'data/verilog/src/glbl.v', stage/'glbl.v')
                primitive_list = ' '.join(PRIMITIVES)
                (stage/'export_timing.tcl').write_text(
                    'set_param general.maxThreads 1\nhelp write_verilog\nhelp write_sdf\n'
                    'open_checkpoint routed.dcp\n'
                    + ((lexical_export_tcl(args.corner) if args.lexical_safe_instance_names else
                        safe_instance_tcl() if args.per_cell_property_checks else bulk_safe_instance_tcl(args.corner))
                       if args.safe_instance_names else '') +
                    ('' if args.lexical_safe_instance_names else
                     'write_verilog -force -mode timesim -sdf_anno true -sdf_file design_timing.sdf design_timesim.v\n'
                     f'write_sdf -force -mode timesim -process_corner {args.corner} -multithread 1 design_timing.sdf\n')+
                    f'foreach primitive {{{primitive_list}}} {{\n'
                    ' puts "TIMING_PRIMITIVE: $primitive [llength [get_cells -hier -filter REF_NAME==$primitive]]"\n'
                    '}\nexit\n', encoding='ascii')
                (stage/'run_sim.tcl').write_text('run all\nquit\n', encoding='ascii')
                run_step('export', [str(bin_dir/'vivado.bat'), '-mode', 'batch', '-source', 'export_timing.tcl',
                                    '-log', 'export.log', '-journal', 'export.jou'])
            if args.lexical_safe_instance_names:
                print('진행: 원본 export 이름 token 변환 및 byte 역변환 검증', flush=True)
                report['lexical_inventory'] = build_inventory_from_export(stage)
                report['lexical_translation'] = translate_exports(stage)
            report['sdf'] = inspect_sdf(stage/'design_timing.sdf')
            netlist_text = (stage/'design_timesim.v').read_text(encoding='ascii')
            annotation = re.findall(r'\$sdf_annotate\s*\([^;]+;', netlist_text)
            if len(annotation) != 1 or 'design_timing.sdf' not in annotation[0]:
                raise RuntimeError('time netlist의 유일한 $sdf_annotate가 지정 SDF를 가리키지 않습니다.')
            report['generated_sdf_annotate_statement'] = annotation[0]
            report['timing_netlist_sha256'] = sha256(stage/'design_timesim.v')
            report['timing_netlist_bytes'] = (stage/'design_timesim.v').stat().st_size
            export_text = decode_console_bytes((stage/'export.console.log').read_bytes())
            counts = {name: int(count) for name, count in re.findall(r'TIMING_PRIMITIVE: (\w+) (\d+)',export_text)}
            report['exported_primitive_counts'] = counts
            if args.safe_instance_names:
                table = (stage/'instance_name_map.tsv').read_text(encoding='utf-8').splitlines()
                keys = table[0].split('\t')
                entries = [dict(zip(keys, row.split('\t'))) for row in table[1:]]
                for row in entries:
                    row['properties_checked'] = int(row['properties_checked'])
                    row['pins_checked'] = int(row['pins_checked'])
                renamed = (report['lexical_inventory']['candidate_primitive_paths'] if args.lexical_safe_instance_names
                           else int(re.search(r'TIMING_RENAME_COUNT: (\d+)', export_text)[1]))
                routes_checked = int(re.search(r'TIMING_ROUTE_CHECK_COUNT: (\d+)', export_text)[1])
                if len(entries) != renamed or len({row['safe_name'] for row in entries}) != renamed:
                    raise RuntimeError('이름 변경 mapping 개수/고유성 증거가 일치하지 않습니다.')
                if not args.per_cell_property_checks:
                    proof = compare_exports(stage/'before_timesim.v', stage/'design_timesim.v',
                                            stage/'before_timing.sdf', stage/'design_timing.sdf',
                                            stage/'instance_name_map.tsv')
                    route_before, route_after = stage/'route_vector_before.txt', stage/'route_vector_after.txt'
                    if sha256(route_before) != sha256(route_after):
                        raise RuntimeError('모든 net ROUTE vector의 전후 SHA-256이 다릅니다.')
                    proof.update({'all_net_routes_unchanged': True, 'routes_compared': routes_checked,
                                  'route_vector_sha256': sha256(route_before),
                                  'route_vector_bytes': route_before.stat().st_size})
                    (stage/'export_invariance.json').write_text(
                        json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
                    report['export_invariance'] = proof
                name_metadata = (['original export module graph and SDF CELLTYPE', 'translated declaration/byte spans']
                                 if args.lexical_safe_instance_names else ['NAME','HIERARCHICALNAME'])
                (stage/'instance_name_map.json').write_text(
                    json.dumps({'mapping':entries,
                                'verification_method':report['name_invariance_mode'],
                                'exported_primitive_attributes_and_pin_connections_unchanged':True,
                                'per_cell_all_properties_checked':args.per_cell_property_checks,
                                'name_metadata_verified':name_metadata,
                                'connected_net_routes_unchanged':True,'routes_checked':routes_checked},
                               ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                report['instance_name_mapping'] = {'renamed_cells':0 if args.lexical_safe_instance_names else renamed,
                    'inventory_primitive_paths':renamed,'routes_checked':routes_checked,
                    'sha256':sha256(stage/'instance_name_map.json'),
                    'exported_primitive_attributes_and_pin_connections_unchanged':True,
                    'per_cell_all_properties_checked':args.per_cell_property_checks,
                    'verification_method':report['name_invariance_mode'],'physical_routes_unchanged':True,
                    'name_metadata_verified':name_metadata}
            if (counts.get('MMCME2_ADV',0)+counts.get('MMCME2_BASE',0)<1
                    or counts.get('BUFG',0)<2 or counts.get('IBUF',0)<3 or counts.get('OBUF',0)<5):
                raise RuntimeError('실제 MMCM/BUFG/핀 primitive가 유지되지 않았습니다.')
            run_step('xvlog', [str(bin_dir/'xvlog.bat'),'--sv','--work','xil_defaultlib',
                               'design_timesim.v','tb_nexys_netlist.sv','glbl.v'])
            # SIMPRIM은 specify/timing checker를 포함한다. 기능용 UNISIM을 먼저 검색해
            # delay/check가 없는 model이 선택되지 않도록 simprims_ver만 명시한다.
            run_step('xelab', [str(bin_dir/'xelab.bat'),'--mt','2',f'--O{args.optimization}','--debug','off',
                               '-L','simprims_ver','-L','secureip', f'--{args.delay_mode}delay',
                               '--transport_int_delays','--pulse_r',str(args.pulse_reject_limit),
                               '--pulse_int_r',str(int_reject),
                               '--pulse_e',str(args.pulse_error_limit),'--pulse_int_e',str(int_error),
                               'xil_defaultlib.tb_nexys_netlist','xil_defaultlib.glbl','-s','nexys_timing'])
            evidence_keys = ('sdf','generated_sdf_annotate_statement','timing_netlist_sha256',
                             'timing_netlist_bytes','exported_primitive_counts')
            if args.safe_instance_names:
                evidence_keys += ('instance_name_mapping',)
                if not args.per_cell_property_checks:
                    evidence_keys += ('export_invariance',)
            if args.lexical_safe_instance_names:
                evidence_keys += ('lexical_translation','lexical_inventory')
            files = ['design_timesim.v','design_timing.sdf','expected.mem','tb_nexys_netlist.sv',
                     'glbl.v','run_sim.tcl']
            if args.safe_instance_names:
                files += ['instance_name_map.json','instance_name_map.tsv']
                if not args.per_cell_property_checks:
                    files += ['before_timesim.v','before_timing.sdf','route_vector_before.txt',
                              'route_vector_after.txt','export_invariance.json']
            if args.lexical_safe_instance_names:
                files += ['lexical_translation_proof.json','lexical_inventory_proof.json',
                          'name_edits.verilog.jsonl.gz','name_edits.sdf.jsonl.gz']
            # exe뿐 아니라 kernel이 읽는 memory/relocation/type 데이터도 같은 snapshot이어야 한다.
            snapshot = stage/'xsim.dir/nexys_timing'
            files += [path.relative_to(stage).as_posix() for path in snapshot.iterdir()
                      if path.is_file() and path.suffix in ('.exe','.mem','.reloc','.rtti','.type',
                                                           '.svtype','.dbg','.xdbg')]
            if 'xsim.dir/nexys_timing/xsimk.exe' not in files:
                raise RuntimeError('xelab timing snapshot의 xsimk.exe가 없습니다.')
            # 명령 자체도 snapshot 해시에 연결한다. 옛 manifest에는 없으므로
            # 재사용 helper가 실제 명령과 보존 result의 명령을 별도로 대조한다.
            options_path = snapshot/'Compile_Options.txt'
            actual_policy = compile_policy(shlex.split(options_path.read_text(encoding='utf-8-sig')))
            if any(actual_policy[key] != identity[key] for key in actual_policy):
                raise RuntimeError('새 xelab의 실제 Compile_Options와 요청 pulse/optimization이 다릅니다.')
            files += ['xsim.dir/nexys_timing/Compile_Options.txt']
            manifest = {'identity':identity, 'files':{name:sha256(stage/name) for name in files},
                        'evidence':{key:report[key] for key in evidence_keys}}
            manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        report['elaboration_sdf_annotation_evidence'] = annotation_evidence(stage/'xelab.console.log')
        report['prepared'] = True
        if not args.prepare_only:
            report['simulation_performed'] = True
            report['simulation_completed'] = False
            run_step('xsim', [str(bin_dir/'xsim.bat'),'nexys_timing','-tclbatch','run_sim.tcl','-log','simulation.log'])
            report['simulation_completed'] = True
            simulation = decode_console_bytes((stage/'xsim.console.log').read_bytes())
            # 숫자/frame 규칙은 기존 검증기를 사용하고 PASS 종류 문자열만 대응시킨다.
            report.update(validate_simulation_output(simulation.replace('post-route timing netlist',
                                                                        'post-route functional netlist'),plan))
            report.update({'passed':True,'sdf_annotated':True,'routed_delays_simulated':True,
                           'numerical_comparison_passed':True,'timing_violation_free':True,
                           'sdf_diagnostics_free':True})
    except Exception as error:
        report['failure_ko'] = str(error)
        print(f'실패: {error}',flush=True)
    finally:
        for path in stage.iterdir():
            if path.is_file() and path.name != 'routed.dcp':
                shutil.copy2(path, output/path.name)
        (output/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'prepared':report['prepared'],
                      'simulation_performed':report['simulation_performed'],
                      'sdf_annotated':report['sdf_annotated'],'report':str(output/'result.json')},ensure_ascii=False),flush=True)
    return 0 if (report['prepared'] if args.prepare_only else report['passed']) else 1


if __name__ == '__main__':
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    raise SystemExit(main())

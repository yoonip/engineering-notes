"""이름 변환 전후의 전체 timing netlist/SDF를 구조적으로 비교한다.

단순히 모든 줄/숫자를 정렬하면 서로 다른 instance의 INIT나 입력/출력이 섞여
같다고 오판할 수 있다. 여기서는 각 module item 및 각 SDF record의 내부 순서를
보존한다. 독립 module item/지연 record의 나열 순서와 배너/DATE만 정규화한다.
SHA-256은 각 완전한 record에 적용하며 중복 record의 개수도 보존한다.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import re
from collections import Counter
from pathlib import Path


def digest(parts: list[str]) -> str:
    """토큰 경계까지 해시에 포함하여 ['ab','c']와 ['a','bc']가 합쳐지지 않게 한다."""
    payload = json.dumps(parts, ensure_ascii=True, separators=(',', ':')).encode('ascii')
    return hashlib.sha256(payload).hexdigest()


def name_map(table: Path) -> dict[str, str]:
    """hex leaf는 부모 계층과 무관하게 원래 leaf로 일대일 복원된다."""
    rows = table.read_text(encoding='utf-8').splitlines()
    columns = rows[0].split('\t')
    mapping: dict[str, str] = {}
    for row in rows[1:]:
        fields = dict(zip(columns, row.split('\t')))
        # Vivado가 flatten한 leaf 안에는 /도 들어갈 수 있다. NAME의 마지막
        # slash로 나누면 실제 식별자의 앞부분을 잃는다. Verilog 계층 표기의
        # 마지막 escaped identifier(백슬래시에서 종료 공백까지)를 기준으로
        # 원래 leaf를 구하고 NAME의 정확한 suffix와도 일치하는지 확인한다.
        hierarchical = fields['original_hierarchicalname']
        escape = hierarchical.rfind('\\')
        if escape < 0 or not hierarchical.endswith(' '):
            raise RuntimeError('mapping에 원래 Verilog escaped leaf가 없습니다.')
        original = hierarchical[escape+1:-1]
        if not fields['original_name'].endswith(original):
            raise RuntimeError('mapping의 NAME과 Verilog leaf가 일치하지 않습니다.')
        safe = fields['safe_name'].rsplit('/', 1)[-1]
        if safe in mapping and mapping[safe] != original:
            raise RuntimeError('서로 다른 leaf 이름이 같은 안전 이름으로 바뀌었습니다.')
        if safe != 'timing_escaped_' + original.encode('utf-8').hex():
            raise RuntimeError('mapping의 hex 이름 변환 규칙이 다릅니다.')
        mapping[safe] = original
    return mapping


GENERATED_UNUSED_WIRE = re.compile(r'^NLW_(timing_escaped_[0-9a-f]+)_([A-Za-z][A-Za-z0-9_]*)_UNCONNECTED$')


def restore_component(component: str, mapping: dict[str, str]) -> str:
    """검증된 primitive leaf와 그 leaf에서 파생한 Vivado unused wire만 복원한다.

    exporter가 연결하지 않은 출력에도 NLW_<instance>_<port>_UNCONNECTED
    dummy wire를 만든다. 이름을 바꾼 primitive에서 이를 다시 내보내면 해당
    wire 이름도 바뀐다. 정확한 형식과 mapping의 leaf 일치가 모두 있을 때만
    원래 이름을 구성하며, port·UNCONNECTED·bit slice는 변경하지 않는다.
    모든 wire 선언과 참조도 전체 item 비교에 남으므로 잘못된 출력 연결을
    지우거나 서로 다른 net을 합치는 정규화가 아니다.
    """
    if component in mapping:
        return mapping[component]
    derived = GENERATED_UNUSED_WIRE.fullmatch(component)
    if derived and derived[1] in mapping:
        return 'NLW_' + mapping[derived[1]] + '_' + derived[2] + '_UNCONNECTED'
    return component


def restore_identifier(value: str, mapping: dict[str, str]) -> str:
    return '/'.join(restore_component(component, mapping) for component in value.split('/'))


def has_forbidden_safe_component(value: str, forbidden: set[str]) -> bool:
    """원본에 새 leaf 또는 그 파생 unused wire와 같은 이름이 없음을 확인한다."""
    for component in value.split('/'):
        if component in forbidden:
            return True
        derived = GENERATED_UNUSED_WIRE.fullmatch(component)
        if derived and derived[1] in forbidden:
            return True
    return False


VERILOG_TOKEN = re.compile(
    r'(?P<space>\s+)|(?P<comment>//[^\n]*|/\*.*?\*/)|'
    r'(?P<directive>`[^\n]*)|(?P<string>"(?:\\.|[^"\\])*")|'
    r'(?P<escaped>\\[^\s]+)|(?P<identifier>[A-Za-z_$][A-Za-z0-9_$]*)|'
    r'(?P<number>(?:\d+)?\s*\'[sS]?[bBoOdDhH][0-9a-fA-F_xXzZ?]+|\d+(?:\.\d+)?)|'
    r'(?P<symbol>[^\s])', re.S)


def verilog_signature(path: Path, mapping: dict[str, str], forbidden_safe_names: set[str] | None = None,
                      item_evidence: dict[str, list[str] | None] | None = None) -> dict:
    """전체 module header와 module item을 비교한다. process 내부 순서는 보존한다.

    cell의 parameter/port/attribute는 하나의 item 안에 붙어 있다. initial begin
    블록의 세미콜론도 블록을 분리하지 않는다. 서로 동시에 존재하는 module
    item의 선언 순서만 정렬한다. generate/function/specify 등의 다른 문법을
    발견하면 임의로 해석하지 않고 실패한다(현재 Vivado 내보내기에는 없다).
    """
    modules: dict[str, dict] = {}
    prefix: list[str] = []
    header: list[str] | None = None
    items: list[str] = []
    item: list[str] = []
    nesting = 0
    parens = 0
    module_name = None
    waiting_name = False
    in_header = False
    token_count = 0
    replacement_count = 0
    for match in VERILOG_TOKEN.finditer(path.read_text(encoding='ascii')):
        kind, value = match.lastgroup, match.group()
        if kind in ('space', 'comment'):
            continue
        token_count += 1
        raw_value = value
        if kind == 'escaped':
            value = value[1:]
            if forbidden_safe_names and has_forbidden_safe_component(value, forbidden_safe_names):
                raise RuntimeError('원본 Verilog에 새 안전 이름과 같은 identifier가 이미 있습니다.')
            restored = restore_identifier(value, mapping)
            replacement_count += restored != value
            value = 'ID:' + restored
        elif kind == 'identifier':
            if forbidden_safe_names and has_forbidden_safe_component(value, forbidden_safe_names):
                raise RuntimeError('원본 Verilog에 새 안전 이름과 같은 identifier가 이미 있습니다.')
            restored = restore_identifier(value, mapping)
            replacement_count += restored != value
            value = 'ID:' + restored
        elif kind == 'number':
            value = re.sub(r'\s+', '', value)
        elif kind == 'directive':
            value = 'DIRECTIVE:' + re.sub(r'\s+', ' ', value.strip())
            if header is not None:
                raise RuntimeError('module 내부 preprocessor는 이 비교기에서 허용하지 않습니다.')
        if header is None:
            if raw_value == 'module' and kind == 'identifier':
                header = prefix + [value]
                prefix = []
                waiting_name, in_header = True, True
            else:
                prefix.append(value)
            continue
        if waiting_name:
            module_name = value
            waiting_name = False
        if in_header:
            header.append(value)
            if raw_value == '(':
                parens += 1
            elif raw_value == ')':
                parens -= 1
            elif raw_value == ';' and parens == 0:
                in_header = False
            continue
        if kind == 'identifier' and raw_value in ('generate', 'function', 'task', 'specify', 'fork'):
            raise RuntimeError(f'지원 범위 밖 module 문법입니다: {raw_value}')
        if raw_value == 'endmodule' and kind == 'identifier':
            if item or nesting or parens:
                raise RuntimeError('module 마지막에 완료되지 않은 item이 있습니다.')
            if module_name in modules:
                raise RuntimeError('중복 module definition이 있습니다.')
            modules[module_name] = {'header_sha256': digest(header),
                                    'items': sorted(Counter(items).items()), 'item_count': len(items)}
            header, module_name = None, None
            items = []
            continue
        item.append(value)
        if raw_value == '(':
            parens += 1
        elif raw_value == ')':
            parens -= 1
        elif raw_value == 'begin' and kind == 'identifier':
            nesting += 1
        elif raw_value == 'end' and kind == 'identifier':
            nesting -= 1
            if nesting < 0:
                raise RuntimeError('begin/end 깊이가 잘못되었습니다.')
            if nesting == 0 and parens == 0:
                item_digest = digest(item)
                if item_evidence is not None and item_digest in item_evidence:
                    item_evidence[item_digest] = item.copy()
                items.append(item_digest); item = []
        elif raw_value == ';' and nesting == 0 and parens == 0:
            item_digest = digest(item)
            if item_evidence is not None and item_digest in item_evidence:
                item_evidence[item_digest] = item.copy()
            items.append(item_digest); item = []
    if header is not None or not modules:
        raise RuntimeError('module 구문이 끝나지 않았거나 없습니다.')
    signature = {'modules': modules, 'suffix': prefix}
    return {'sha256': digest([json.dumps(signature, sort_keys=True, separators=(',', ':'))]),
            'module_count': len(modules), 'item_count': sum(row['item_count'] for row in modules.values()),
            'token_count': token_count, 'restored_identifier_occurrences': replacement_count,
            'module_signatures': modules}


SDF_TOKEN = re.compile(r'\s+|"(?:\\.|[^"\\])*"|[()]|(?:\\.|[^()"\s])+', re.S)


def sdf_atom(token: str, mapping: dict[str, str]) -> tuple[str, bool]:
    """SDF의 계층 slash와 식별자 안의 escaped slash를 구분하여 보존한다.

    ``a/b``는 두 계층 성분이고 ``a\\/b``는 slash 문자가 포함된 성분 한
    개이다. 먼저 이 경계를 읽고, 각 완전한 성분에만 안전 이름의 역변환을
    적용한다. 역변환으로 돌아온 leaf 안의 slash도 같은 성분 안에 남는다.
    JSON 배열로 성분 경계까지 canonical 값에 넣으므로 두 경우가 같아질
    수 없다. keyword/숫자와 같은 일반 atom은 그대로 두어 SDF 문법의 head
    이름을 유지하며, bracket·escape·경로·역변환 atom은 구조화한다.
    """
    components = ['']
    index = 0
    while index < len(token):
        char = token[index]
        if char == '\\':
            if index + 1 >= len(token):
                raise RuntimeError('SDF atom 끝에 해석할 수 없는 escape가 있습니다.')
            components[-1] += token[index+1]
            index += 2
        elif char == '/':
            components.append('')
            index += 1
        else:
            components[-1] += char
            index += 1
    restored = [mapping.get(component, component) for component in components]
    replaced = restored != components
    if replaced or any(char in token for char in '/\\[]'):
        return 'SDF_ATOM:' + json.dumps(restored, ensure_ascii=True, separators=(',', ':')), replaced
    return token, False


def sdf_signature(path: Path, mapping: dict[str, str]) -> dict:
    """SDF 전체를 작은 record 해시로 접어 메모리 사용을 줄인다.

    CELL 나열 순서, ABSOLUTE의 IOPATH/INTERCONNECT 나열 순서, TIMINGCHECK의
    check 나열 순서만 정규화한다. 각 path의 입력/출력과 min:typ:max 숫자 순서,
    조건 식과 모든 timing check 인수를 그대로 보존한다. 계층 slash와 leaf
    안의 escaped slash의 차이도 유지한다. DATE만 제외한다.
    """
    stack: list[list[tuple[str, str]]] = []
    roots: list[str] = []
    cells = paths = checks = replaced = 0
    for match in SDF_TOKEN.finditer(path.read_text(encoding='ascii')):
        token = match.group()
        if token.isspace():
            continue
        if token == '(':
            stack.append([])
        elif token == ')':
            if not stack or not stack[-1] or stack[-1][0][0] != 'atom':
                raise RuntimeError('잘못된 SDF expression입니다.')
            fields = stack.pop()
            head = fields[0][1]
            children = fields[1:]
            cells += head == 'CELL'
            paths += head in ('IOPATH', 'INTERCONNECT')
            checks += head == 'TIMINGCHECK'
            if head == 'DATE':
                children = [('atom', '<export_timestamp>')]
            elif head in ('ABSOLUTE', 'TIMINGCHECK'):
                if any(kind != 'expr' for kind, _ in children):
                    raise RuntimeError(f'{head}에 예상 밖 위치 인수가 있습니다.')
                children = sorted(children)
            elif head == 'DELAYFILE':
                # header의 위치는 보존하고 CELL들은 완전한 개별 record로 정렬한다.
                headers = [(kind, val) for kind, val in children if kind != 'cell']
                cell_records = sorted((kind, val) for kind, val in children if kind == 'cell')
                children = headers + cell_records
            normalized = digest([head] + [kind + ':' + val for kind, val in children])
            kind = 'cell' if head == 'CELL' else 'expr'
            if stack:
                stack[-1].append((kind, normalized))
            else:
                roots.append(normalized)
        else:
            if not stack:
                raise RuntimeError('SDF expression 밖 token이 있습니다.')
            if not token.startswith('"'):
                token, restored = sdf_atom(token, mapping)
                replaced += restored
            stack[-1].append(('atom', token))
    if stack or len(roots) != 1:
        raise RuntimeError('SDF 최상위 expression이 올바르지 않습니다.')
    return {'sha256': roots[0], 'cell_records': cells, 'path_records': paths,
            'timingcheck_records': checks, 'restored_identifier_occurrences': replaced}


def compare_exports(before_v: Path, after_v: Path, before_sdf: Path, after_sdf: Path, table: Path) -> dict:
    mapping = name_map(table)
    v_before = verilog_signature(before_v, {}, set(mapping))
    v_after = verilog_signature(after_v, mapping)
    s_before, s_after = sdf_signature(before_sdf, {}), sdf_signature(after_sdf, mapping)
    if v_before['sha256'] != v_after['sha256']:
        raise RuntimeError('이름 복원 후 전체 Verilog module/attribute/parameter/port/body가 다릅니다.')
    if s_before['sha256'] != s_after['sha256']:
        raise RuntimeError('이름 복원 후 전체 SDF cell/path/check 지연 내용이 다릅니다.')
    def compact_verilog(signature: dict) -> dict:
        compact = {key: value for key, value in signature.items() if key != 'module_signatures'}
        compact['module_signatures'] = {
            name: {'sha256': digest([json.dumps(row, sort_keys=True, separators=(',', ':'))]),
                   'header_sha256': row['header_sha256'], 'item_count': row['item_count']}
            for name, row in signature['module_signatures'].items()}
        return compact
    return {'passed': True, 'comparison_scope': 'whole_exported_verilog_and_sdf',
            'canonical_comparator_schema': 3, 'sdf_hierarchy_delimiters_preserved': True,
            'restored_name_rules': ['verified primitive leaf',
                                    'Vivado NLW_<verified leaf>_<port>_UNCONNECTED'],
            'ignored_fields': ['Verilog comments/banner', 'SDF DATE'],
            'normalized_order': ['concurrent module items', 'SDF CELL records',
                                 'SDF ABSOLUTE path records', 'SDF TIMINGCHECK records'],
            'parameter_and_port_order_preserved': True, 'process_internal_order_preserved': True,
            'timing_path_argument_and_min_typ_max_order_preserved': True,
            'unique_safe_leaf_names': len(mapping), 'verilog_before': compact_verilog(v_before),
            'verilog_after': compact_verilog(v_after), 'sdf_before': s_before, 'sdf_after': s_after}


def main() -> int:
    """이미 보존된 전후 export를 새 comparator로 재검증하는 독립 실행 입구다.

    Vivado/xsim을 다시 실행하거나 원본 DCP를 수정하지 않는다. 이 명령의
    PASS는 회로 이름 변환 불변성 검사의 성공이며 UART timing PASS와 다르다.
    따라서 실제 simulation과 보드 측정 여부를 명시적으로 false로 기록한다.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    proof = compare_exports(args.stage/'before_timesim.v', args.stage/'design_timesim.v',
                            args.stage/'before_timing.sdf', args.stage/'design_timing.sdf',
                            args.stage/'instance_name_map.tsv')
    def file_sha256(path: Path) -> str:
        checksum = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1 << 20), b''):
                checksum.update(chunk)
        return checksum.hexdigest()
    proof.update({'mode': 'export_invariance_recheck', 'actual_uart_simulation_performed': False,
                  'physical_board_measured': False, 'stage': str(args.stage.resolve()),
                  'comparator_sha256': file_sha256(Path(__file__)),
                  'export_file_sha256': {name: file_sha256(args.stage/name) for name in
                      ('before_timesim.v', 'design_timesim.v', 'before_timing.sdf',
                       'design_timing.sdf', 'instance_name_map.tsv')}})
    route_before, route_after = args.stage/'route_vector_before.txt', args.stage/'route_vector_after.txt'
    if route_before.is_file() and route_after.is_file():
        before_hash, after_hash = file_sha256(route_before), file_sha256(route_after)
        if before_hash != after_hash:
            raise RuntimeError('보존된 전체 net ROUTE vector의 전후 해시가 다릅니다.')
        proof.update({'all_net_routes_unchanged': True, 'route_vector_sha256': before_hash,
                      'route_vector_bytes': route_before.stat().st_size})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'scope': proof['mode'], 'schema': proof['canonical_comparator_schema'],
                      'sdf_hierarchy_delimiters_preserved': True, 'output': str(args.output)},
                     ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""원본 timing export에서 등록된 primitive 인스턴스 이름 token만 변환한다.

Vivado 객체·DCP·wire·port·NLW·INIT·연산식·지연 수치는 변경하지 않는다.
문법으로 확인한 선언과 SDF cell 경로의 byte span만 편집하고 역변환 파일이
원본 byte와 완전히 같은지 확인한다. 실제 SDF annotation/xsim은 별도 단계다.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import re
from pathlib import Path

from fpga.nexys4_ddr.compare_timing_exports import VERILOG_TOKEN, SDF_TOKEN, name_map


def token_id(token: tuple) -> str:
    return token[1][1:] if token[0] == 'escaped' else token[1]


def module_graph(text: str) -> dict:
    """Vivado structure netlist의 module별 실제 instance 선언과 범위를 읽는다.

    attribute와 #(...) parameter 목록을 먼저 건너뛴 뒤 TYPE INSTANCE (...)
    형태만 허용한다. named port 앞의 점과 hierarchical reference를 구분하고,
    후자·defparam·generate·복수 instance 선언 같은 지원 밖 문법은 실패시킨다.
    모든 identifier를 저장해 새 instance가 기존 wire/port 이름과 충돌하는지도
    검사할 수 있게 한다. 선언 token 위치가 byte 편집의 유일한 허용 근거이다.
    """
    modules, current, header, module_name, waiting_name = {}, None, False, None, False
    item, parens, blocks = [], 0, 0
    declarations = {'wire','reg','input','output','inout','assign','parameter','localparam',
                    'integer','real','time','tri','tri0','tri1','supply0','supply1','initial','always'}
    def finish_item(tokens: list[tuple]) -> None:
        if not tokens:
            return
        if any(t[1] in ('defparam','generate','function','task','fork','specify') and t[0] == 'identifier' for t in tokens):
            raise RuntimeError('lexical 변환에서 지원하지 않는 netlist 문법입니다.')
        # Vivado 자체가 ASYNC_REG에 넣은 기존 notifier 참조는 선언 이름과
        # 함께 바꿔야 한다. RHS 1'bx나 vendor 동작을 새로 추가/변경하지 않는다.
        notifier = (len(tokens)==8 and [t[1] for t in tokens[:2]]==['initial','assign']
                    and tokens[2][0] in ('identifier','escaped')
                    and [t[1] for t in tokens[3:]]==['.','notifier','=',"1'bx",';'])
        if notifier:
            current['notifier_references'].append(tokens[2])
            return
        for index, token in enumerate(tokens):
            if token[1] == '.' and index and tokens[index-1][0] in ('identifier','escaped'):
                if token_id(tokens[index-1]) != 'glbl':
                    raise RuntimeError('선언 이름 변경에 함께 처리할 수 없는 hierarchical reference가 있습니다: '
                                       +str(module_name)+': '+tokens[index-1][1]+'.'+tokens[index+1][1])
        pos = 0
        while pos+1 < len(tokens) and tokens[pos][1] == '(' and tokens[pos+1][1] == '*':
            pos += 2
            while pos+1 < len(tokens) and not (tokens[pos][1] == '*' and tokens[pos+1][1] == ')'):
                pos += 1
            if pos+1 >= len(tokens):
                raise RuntimeError('끝나지 않은 instance attribute입니다.')
            pos += 2
        if pos >= len(tokens) or token_id(tokens[pos]) in declarations:
            return
        if tokens[pos][0] not in ('identifier','escaped'):
            raise RuntimeError('예상 밖 module item입니다.')
        kind = token_id(tokens[pos]); pos += 1
        if pos < len(tokens) and tokens[pos][1] == '#':
            pos += 1
            if tokens[pos][1] != '(':
                raise RuntimeError('잘못된 instance parameter 문법입니다.')
            depth = 0
            while pos < len(tokens):
                depth += tokens[pos][1] == '('; depth -= tokens[pos][1] == ')'
                pos += 1
                if depth == 0:
                    break
        if (pos+1 >= len(tokens) or tokens[pos][0] not in ('identifier','escaped')
                or tokens[pos+1][1] != '(' or tokens[-1][1] != ';' or tokens[-2][1] != ')'):
            raise RuntimeError('단일 instance 선언으로 해석할 수 없는 module item입니다: '
                               +str(module_name)+': '+' '.join(t[1] for t in tokens[:12]))
        instance = token_id(tokens[pos])
        depth=0; closing=None
        for connection_index in range(pos+1,len(tokens)):
            depth += tokens[connection_index][1]=='('
            depth -= tokens[connection_index][1]==')'
            if depth==0:
                closing=connection_index; break
        if closing!=len(tokens)-2:
            raise RuntimeError('복수 instance 또는 지원 밖 연결 목록입니다.')
        if instance in current['instances']:
            raise RuntimeError('같은 module에 중복 instance 이름이 있습니다.')
        current['instances'][instance] = {'type': kind, 'token': tokens[pos]}
    for match in VERILOG_TOKEN.finditer(text):
        kind, raw = match.lastgroup, match.group()
        if kind in ('space','comment'):
            continue
        token = (kind, raw, match.start(), match.end())
        if current is None:
            if raw == 'module' and kind == 'identifier':
                current = {'instances':{}, 'identifiers':set(),'notifier_references':[]}
                header, waiting_name, parens = True, True, 0
            continue
        if kind in ('identifier','escaped'):
            current['identifiers'].add(token_id(token))
        if waiting_name:
            module_name = token_id(token); waiting_name = False
        if header:
            parens += raw == '('; parens -= raw == ')'
            if raw == ';' and parens == 0:
                header = False
            continue
        if raw == 'endmodule' and kind == 'identifier':
            if item or blocks or parens or module_name in modules:
                raise RuntimeError('module 종료 상태 또는 이름이 잘못됐습니다.')
            modules[module_name] = current; current = None
            continue
        item.append(token)
        parens += raw == '('; parens -= raw == ')'
        if kind == 'identifier' and raw == 'begin':
            blocks += 1
        elif kind == 'identifier' and raw == 'end':
            blocks -= 1
            if blocks == 0 and parens == 0:
                finish_item(item); item = []
        elif raw == ';' and blocks == 0 and parens == 0:
            finish_item(item); item = []
    if current is not None or not modules:
        raise RuntimeError('완료된 module을 찾지 못했습니다.')
    return modules


def hierarchy_components(value: str) -> list[str]:
    """Verilog HIERARCHICALNAME의 escaped leaf 안 점/slash를 보존한다."""
    result, index = [], 0
    while index < len(value):
        if value[index].isspace():
            index += 1; continue
        if value[index] == '.':
            index += 1; continue
        escaped = value[index] == '\\'
        start = index + escaped; index = start
        while index < len(value) and (not value[index].isspace() if escaped else value[index] != '.'):
            index += 1
        result.append(value[start:index])
    return result


def resolve(graph: dict, top: str, components: list[str]) -> tuple[str, dict]:
    """원래 module instance graph를 따라 전체 SDF cell 경로를 해석한다."""
    parent, node = top, {'type':top}
    for component in components:
        if parent not in graph or component not in graph[parent]['instances']:
            raise RuntimeError('원본 module graph에서 cell 경로를 찾을 수 없습니다: '+'/'.join(components))
        node = graph[parent]['instances'][component]
        previous = parent; parent = node['type']
    return (previous if components else top), node


def compatible_type(verilog_type: str, ref_type: str) -> bool:
    return verilog_type == ref_type or (ref_type in ('RAM32M','RAM64M') and verilog_type.startswith(ref_type+'_'))


def build_inventory_from_export(stage: Path, top: str = 'nexys4_ddr_gpt_top') -> dict:
    """원본 export graph에서 실제 vendor primitive 경로를 빠르게 전개한다.

    대규모 Vivado property query나 CAD rename는 호출하지 않는다. 실제 원본
    Verilog에서 terminal primitive 및 vendor RAM macro 선언을 찾고 top부터
    전체 경로를 만든다. LOC/BEL은 조회하지 않았으므로 빈 값이며 source를
    original_export_module_graph로 명시한다. 뒤 단계는 별도 원본 SDF의
    CELLTYPE·경로와 이 graph를 모두 대응시키고 byte 역변환을 검사한다.
    """
    text=(stage/'before_timesim.v').read_bytes().decode('ascii')
    graph=module_graph(text)
    rows=[]; terminal_paths=0
    identifier=re.compile(r'^[A-Za-z_$][A-Za-z0-9_$]*$')
    def spelling(name: str) -> str:
        return name if identifier.fullmatch(name) else '\\'+name+' '
    def walk(module: str, path: list[str], ancestry: tuple[str,...]) -> None:
        nonlocal terminal_paths
        if module in ancestry:
            raise RuntimeError('원본 module graph에 재귀 계층이 있습니다.')
        for leaf,node in graph[module]['instances'].items():
            components=path+[leaf]
            terminal=node['type'] not in graph
            macro=node['type'].startswith(('RAM32M_','RAM64M_'))
            if terminal: terminal_paths+=1
            # XSim의 SDF 경로 해석은 escaped leaf 안의 []뿐 아니라 점(.)도
            # HDL 계층 경계로 잘못 읽을 수 있다. 실제32-token RAM wrapper에는
            # g_flat_distributed_cache.key_memory_reg... 같은 점 포함 이름이
            # 있어 첫 방식에서765개 SDF 적용을 건너뛰었다. 실제 instance
            # 선언의 비단순 identifier 전부를 같은 일대일 hex 이름으로 맞춘다.
            # RAM macro 부모를 바꾸면 그 내부 RAMA 등 자식의 SDF 경로 성분도
            # translate_exports가 함께 바꾼다. wire/핀/숫자는 바꾸지 않는다.
            if not identifier.fullmatch(leaf):
                safe='timing_escaped_'+leaf.encode('utf-8').hex()
                rows.append({'original_name':'/'.join(components),'safe_name':'/'.join(path+[safe]),
                    'original_hierarchicalname':'.'.join(spelling(c) for c in [top]+components),
                    'safe_hierarchicalname':'.'.join(spelling(c) for c in [top]+path+[safe]),
                    'ref_name':node['type'],'loc':'','bel':'','properties_checked':'0','pins_checked':'0',
                    'inventory_source':'original_export_module_graph'})
            if not terminal:
                walk(node['type'],components,ancestry+(module,))
    walk(top,[],())
    columns=['original_name','safe_name','original_hierarchicalname','safe_hierarchicalname',
             'ref_name','loc','bel','properties_checked','pins_checked','inventory_source']
    (stage/'instance_name_map.tsv').write_text('\t'.join(columns)+'\n'+
        ''.join('\t'.join(row[c] for c in columns)+'\n' for row in rows),encoding='utf-8')
    result={'source':'original_export_module_graph','original_verilog_sha256':hashlib.sha256(text.encode('ascii')).hexdigest(),
            'candidate_primitive_paths':len(rows),'terminal_vendor_primitive_paths':terminal_paths,
            'cad_property_queries_performed':False,'cad_cells_renamed':0,'loc_bel_queried':False}
    (stage/'lexical_inventory_proof.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def sdf_components(token: str) -> list[tuple[str,int,int]]:
    r"""SDF atom의 decoded 성분과 원문 범위를 함께 보존한다. \/는 separator가 아니다."""
    result, chars, start, index = [], [], 0, 0
    while index < len(token):
        if token[index] == '\\':
            if index+1 >= len(token):
                raise RuntimeError('끝나지 않은 SDF escape입니다.')
            chars.append(token[index+1]); index += 2
        elif token[index] == '/':
            result.append((''.join(chars), start, index)); chars = []
            index += 1; start = index
        else:
            chars.append(token[index]); index += 1
    result.append((''.join(chars), start, index))
    return result


def apply_edits(text: str, edits: list[dict], destination: Path, evidence: Path) -> dict:
    """허용 token 범위 외 byte를 그대로 복사하고, 실제 변환 후 byte 역변환을 검사한다."""
    parts, cursor, shift = [], 0, 0
    for edit in sorted(edits, key=lambda e:e['start']):
        if edit['start'] < cursor or text[edit['start']:edit['end']] != edit['old']:
            raise RuntimeError('편집 범위가 겹치거나 원래 token과 다릅니다.')
        parts.extend((text[cursor:edit['start']], edit['new']))
        edit['new_start'] = edit['start']+shift
        edit['new_end'] = edit['new_start']+len(edit['new'])
        shift += len(edit['new'])-len(edit['old']); cursor = edit['end']
    parts.append(text[cursor:]); translated = ''.join(parts)
    reverse, cursor = [], 0
    for edit in sorted(edits, key=lambda e:e['new_start']):
        if translated[edit['new_start']:edit['new_end']] != edit['new']:
            raise RuntimeError('실제 변환 파일의 token이 편집 증거와 다릅니다.')
        reverse.extend((translated[cursor:edit['new_start']], edit['old'])); cursor=edit['new_end']
    reverse.append(translated[cursor:]); restored = ''.join(reverse)
    if restored.encode('ascii') != text.encode('ascii'):
        raise RuntimeError('이름 token 역변환 후 원본 byte와 다릅니다.')
    destination.write_bytes(translated.encode('ascii'))
    if destination.read_bytes()!=translated.encode('ascii'):
        raise RuntimeError('저장한 실제 변환 파일과 검증한 byte가 다릅니다.')
    with gzip.open(evidence, 'wt', encoding='utf-8', newline='\n') as stream:
        for edit in sorted(edits, key=lambda e:e['start']):
            stream.write(json.dumps(edit, ensure_ascii=True, separators=(',',':'))+'\n')
    return {'edits':len(edits), 'original_sha256':hashlib.sha256(text.encode('ascii')).hexdigest(),
            'translated_sha256':hashlib.sha256(translated.encode('ascii')).hexdigest(),
            'inverse_sha256':hashlib.sha256(restored.encode('ascii')).hexdigest(),
            'inverse_byte_identical':True, 'only_allowed_token_spans_changed':True,
            'written_file_bytes_verified':True,
            'edit_evidence_file':evidence.name}


def translate_exports(stage: Path, top: str = 'nexys4_ddr_gpt_top') -> dict:
    """등록 primitive 경로↔선언↔SDF CELLTYPE을 확인하고 lossless 이름 변환한다."""
    original_v = (stage/'before_timesim.v').read_bytes().decode('ascii')
    original_sdf = (stage/'before_timing.sdf').read_bytes().decode('ascii')
    graph = module_graph(original_v)
    table = (stage/'instance_name_map.tsv').read_text(encoding='utf-8').splitlines()
    headers = table[0].split('\t'); allowed = {}
    mapping = name_map(stage/'instance_name_map.tsv')
    for line in table[1:]:
        row = dict(zip(headers,line.split('\t')))
        components = hierarchy_components(row['original_hierarchicalname'])
        if not components or components[0] != top:
            raise RuntimeError('inventory와 원래 top의 이름이 다릅니다.')
        parent, node = resolve(graph,top,components[1:])
        if not compatible_type(node['type'],row['ref_name']):
            raise RuntimeError('등록 inventory 종류와 원본 Verilog instance 종류가 다릅니다.')
        leaf = components[-1]; safe = row['safe_name'].rsplit('/',1)[-1]
        if mapping.get(safe) != leaf or safe in graph[parent]['identifiers']:
            raise RuntimeError('lexical 안전 이름의 원본 leaf 또는 module 내 충돌 검사 실패')
        key = (parent,leaf)
        if key in allowed and allowed[key] != safe:
            raise RuntimeError('같은 선언의 변환 이름이 다릅니다.')
        allowed[key] = safe
    verilog_edits=[]
    for (parent,leaf),safe in allowed.items():
        token=graph[parent]['instances'][leaf]['token']
        if token[0] != 'escaped' or token[1] != '\\'+leaf:
            raise RuntimeError('등록된 leaf의 실제 Verilog escaped 선언과 다릅니다.')
        verilog_edits.append({'start':token[2],'end':token[3],'old':token[1],'new':safe,
                              'role':'primitive_instance_declaration','module':parent,
                              'type':graph[parent]['instances'][leaf]['type']})
    declarations_translated=len(verilog_edits)
    for parent,module in graph.items():
        for token in module['notifier_references']:
            leaf=token_id(token)
            if leaf not in module['instances']:
                raise RuntimeError('기존 notifier의 primitive instance를 찾지 못했습니다.')
            if (parent,leaf) in allowed:
                verilog_edits.append({'start':token[2],'end':token[3],'old':token[1],
                                      'new':allowed[(parent,leaf)],'module':parent,
                                      'role':'existing_vivado_notifier_instance_reference'})
    sdf_edits=[]; frames=[]; cells_checked=0; endpoints_checked=0
    for match in SDF_TOKEN.finditer(original_sdf):
        raw=match.group()
        if raw.isspace(): continue
        if raw=='(':
            if frames: frames[-1]['children']+=1
            frames.append({'head':None,'children':0,'cell_type':None,'scope':None}); continue
        if raw==')':
            if not frames: raise RuntimeError('SDF 괄호 상태 오류')
            if frames[-1]['head']=='INSTANCE' and frames[-1]['children']==0:
                if len(frames)<2 or frames[-2]['head']!='CELL' or frames[-2]['cell_type']!=top:
                    raise RuntimeError('빈 INSTANCE의 top CELL scope가 다릅니다.')
                frames[-2]['scope']=[]; cells_checked+=1
            frames.pop(); continue
        if not frames: raise RuntimeError('SDF expression 밖 atom')
        frame=frames[-1]
        if frame['head'] is None: frame['head']=raw; continue
        frame['children']+=1
        if frame['head']=='DIVIDER' and raw!='/':
            raise RuntimeError('현재 도구가 지원하는 SDF DIVIDER는 /입니다.')
        if frame['head']=='CELLTYPE' and frame['children']==1:
            if frames[-2]['head']!='CELL': raise RuntimeError('CELLTYPE scope 오류')
            frames[-2]['cell_type']=json.loads(raw); continue
        head=frame['head']
        if head not in ('INSTANCE','INTERCONNECT') or (head=='INTERCONNECT' and frame['children']>2):
            continue
        if raw.startswith('"'): raise RuntimeError('지원하지 않는 quoted SDF 경로')
        components=sdf_components(raw); values=[c[0] for c in components]
        cell_frame=next((f for f in reversed(frames[:-1]) if f['head']=='CELL'),None)
        if cell_frame is None: raise RuntimeError('SDF CELL 경로 밖 endpoint')
        if head=='INSTANCE':
            if frames[-2]['head']!='CELL': raise RuntimeError('INSTANCE 직접 부모가 CELL이 아닙니다.')
            if frame['children']!=1: raise RuntimeError('INSTANCE 인수 개수 오류')
            cell_frame['scope']=values
            parent,node=resolve(graph,top,values)
            if not compatible_type(node['type'],cell_frame['cell_type']):
                raise RuntimeError('원래 SDF CELLTYPE과 Verilog graph가 다릅니다: '+raw)
            cells_checked+=1; cell_values=values; base=[]
        else:
            if len(frames)<4 or [f['head'] for f in frames[-4:-1]]!=['CELL','DELAY','ABSOLUTE']:
                raise RuntimeError('지원 밖 INTERCONNECT 문맥입니다.')
            # INTERCONNECT 마지막 성분은 실제 pin이다. pin bit/escape는 그대로 둔다.
            if cell_frame['scope'] is None: raise RuntimeError('INTERCONNECT 이전 INSTANCE 없음')
            base=cell_frame['scope']; cell_values=values[:-1]
            resolve(graph,top,base+cell_values); endpoints_checked+=1
        parent=top
        for component in base:
            parent=graph[parent]['instances'][component]['type']
        for index,component in enumerate(cell_values):
            key=(parent,component)
            node=graph[parent]['instances'][component]
            if key in allowed:
                start,end=components[index][1:]
                sdf_edits.append({'start':match.start()+start,'end':match.start()+end,
                                  'old':raw[start:end],'new':allowed[key],
                                  'role':'sdf_'+head.lower()+'_cell_component','module':parent,'type':node['type']})
            parent=node['type']
    if frames: raise RuntimeError('끝나지 않은 SDF expression')
    vproof=apply_edits(original_v,verilog_edits,stage/'design_timesim.v',stage/'name_edits.verilog.jsonl.gz')
    sproof=apply_edits(original_sdf,sdf_edits,stage/'design_timing.sdf',stage/'name_edits.sdf.jsonl.gz')
    if not verilog_edits or not sdf_edits: raise RuntimeError('실제 이름 변환 token이 없습니다.')
    proof={'passed':True,'mode':'lexical_original_export_token_inversion',
           'original_dcp_or_cad_cells_mutated':False,'verilog':vproof,'sdf':sproof,
           'instance_declarations_translated':declarations_translated,
           'existing_vivado_notifier_references_translated':len(verilog_edits)-declarations_translated,
           'inventory_primitive_paths':len(table)-1,'sdf_cells_resolved':cells_checked,
           'sdf_interconnect_endpoints_resolved':endpoints_checked,
           'sdf_endpoint_cell_paths_resolved':True,'sdf_endpoint_pin_tokens_unchanged':True,
           'sdf_endpoint_pin_existence_independently_checked':False,
           'wire_port_nlw_init_and_logic_tokens_unchanged':True,
           'iopath_timingcheck_pin_edge_condition_and_delay_tokens_unchanged':True,
           'actual_uart_simulation_performed':False,'physical_board_measured':False}
    (stage/'lexical_translation_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return proof

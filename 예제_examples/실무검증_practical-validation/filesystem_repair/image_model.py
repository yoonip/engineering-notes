"""Bounded EDUFS1 JSON images; no disk device, mount or real fsck support."""

import argparse  # import는 표준 라이브러리의 명령행 처리 기능을 불러옵니다.
import copy  # copy는 원본과 분리한 중첩 자료 사본을 만듭니다.
import hashlib  # hashlib은 이미지와 파일 내용의 SHA-256을 계산합니다.
import json  # json은 자체 이미지의 객체와 UTF-8 바이트를 변환합니다.
import os  # os는 새 결과 파일에 동기화 요청을 보냅니다.
from pathlib import Path  # Path는 호스트 파일 경로를 다룹니다.
import re  # re는 제한한 이름과 16진수 표기를 검사합니다.

MUTATIONS = ('none', 'ignore-shared', 'guess-size', 'drop-orphan', 'skip-digest')
MAX_IMAGE = 65536
MAX_MANIFEST = 16384


class ImageError(ValueError):  # class는 이 이미지 형식의 거부 사유를 구분합니다.
    pass


def require(condition, reason):  # def는 조건이 거짓일 때 명시적으로 거부합니다.
    if not condition:  # not은 참과 거짓을 뒤집습니다.
        raise ImageError(reason)


def canonical(value):  # 정렬한 compact JSON을 동일한 UTF-8 bytes로 만듭니다.
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def object_pairs(pairs):  # JSON의 중복 키를 마지막 값으로 조용히 덮지 않습니다.
    result = {}
    for key, value in pairs:
        require(key not in result, 'DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def read_json(path, limit):
    require(path.is_file(), 'REGULAR_HOST_FILE_REQUIRED')
    with path.open('rb') as stream:  # with는 파일을 사용한 뒤 닫습니다.
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, 'INPUT_TOO_LARGE')
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=object_pairs)
    return raw, value


def keys(value, expected, reason):
    require(type(value) is dict and set(value) == set(expected), reason)


def integer(value, lower, upper):
    require(type(value) is int and lower <= value <= upper, 'INTEGER_RANGE_OR_TYPE')


def hash_text(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{64}', value), 'SHA256_FORMAT')


def load_image(path):
    raw, image = read_json(path, MAX_IMAGE)
    keys(image, ('format', 'super', 'inodes', 'dirs', 'blocks', 'bitmap', 'checksum'), 'IMAGE_SCHEMA')
    require(image['format'] == 'EDUFS1', 'UNSUPPORTED_FORMAT')
    header = image['super']
    keys(header, ('block_size', 'block_count', 'root', 'lost_found', 'features'), 'SUPER_SCHEMA')
    require(header == {'block_size': 8, 'block_count': 8, 'root': 1, 'lost_found': 2, 'features': []}, 'UNSUPPORTED_GEOMETRY_OR_FEATURE')
    require(all(type(header[k]) is int for k in ('block_size', 'block_count', 'root', 'lost_found')), 'SUPER_INTEGER_TYPE')
    hash_text(image['checksum'])
    body = {k: v for k, v in image.items() if k != 'checksum'}
    require(digest(canonical(body)) == image['checksum'], 'IMAGE_CHECKSUM')
    for collection, bound in (('inodes', 16), ('dirs', 16), ('blocks', 8), ('bitmap', 8)):
        require(type(image[collection]) is list and len(image[collection]) <= bound, 'COLLECTION_BOUND')
    inode_ids = set()
    for inode in image['inodes']:
        keys(inode, ('id', 'kind', 'size', 'blocks', 'nlink'), 'INODE_SCHEMA')
        integer(inode['id'], 1, 32)
        require(inode['id'] not in inode_ids, 'DUPLICATE_INODE')
        inode_ids.add(inode['id'])
        require(inode['kind'] in ('file', 'dir'), 'INODE_KIND')
        integer(inode['size'], 0, 64)
        integer(inode['nlink'], 0, 32)
        require(type(inode['blocks']) is list and len(inode['blocks']) <= 8, 'BLOCK_LIST_BOUND')
        for block in inode['blocks']:
            integer(block, 0, 7)
        if inode['kind'] == 'dir':
            require(inode['size'] == 0 and inode['blocks'] == [], 'DIRECTORY_STORAGE_CONTRACT')
    block_ids = set()
    for block in image['blocks']:
        keys(block, ('id', 'data', 'sha256'), 'BLOCK_SCHEMA')
        integer(block['id'], 0, 7)
        require(block['id'] not in block_ids, 'DUPLICATE_BLOCK_RECORD')
        block_ids.add(block['id'])
        require(type(block['data']) is str and re.fullmatch('[0-9a-f]{16}', block['data']), 'BLOCK_HEX')
        hash_text(block['sha256'])
        require(digest(bytes.fromhex(block['data'])) == block['sha256'], 'BLOCK_CHECKSUM')
    dir_ids = set()
    for directory in image['dirs']:
        keys(directory, ('inode', 'entries'), 'DIRECTORY_SCHEMA')
        integer(directory['inode'], 1, 32)
        require(directory['inode'] not in dir_ids, 'DUPLICATE_DIRECTORY_RECORD')
        dir_ids.add(directory['inode'])
        require(type(directory['entries']) is list and len(directory['entries']) <= 32, 'ENTRY_BOUND')
        for entry in directory['entries']:
            keys(entry, ('name', 'inode'), 'ENTRY_SCHEMA')
            require(type(entry['name']) is str and re.fullmatch('[A-Za-z0-9_.+-]{1,32}', entry['name']) and entry['name'] not in ('.', '..'), 'ENTRY_NAME')
            integer(entry['inode'], 1, 32)
    for block in image['bitmap']:
        integer(block, 0, 7)
    require(len(set(image['bitmap'])) == len(image['bitmap']), 'DUPLICATE_BITMAP_BIT')
    return raw, image


def load_manifest(path):
    if path is None:
        return None, None
    raw, manifest = read_json(path, MAX_MANIFEST)
    keys(manifest, ('format', 'files'), 'MANIFEST_SCHEMA')
    require(manifest['format'] == 'EDUFS-MANIFEST1' and type(manifest['files']) is list and len(manifest['files']) <= 16, 'MANIFEST_FORMAT')
    seen = set()
    for entry in manifest['files']:
        keys(entry, ('inode', 'size', 'sha256'), 'MANIFEST_FILE_SCHEMA')
        integer(entry['inode'], 1, 32)
        integer(entry['size'], 0, 64)
        hash_text(entry['sha256'])
        require(entry['inode'] not in seen, 'DUPLICATE_MANIFEST_INODE')
        seen.add(entry['inode'])
    return raw, manifest


def file_bytes(image, inode):
    blocks = {b['id']: bytes.fromhex(b['data']) for b in image['blocks']}
    return b''.join(blocks[b] for b in inode['blocks'])


def identity(image, manifest, mutation):
    files = {n['id']: n for n in image['inodes'] if n['kind'] == 'file'}
    expected = {} if manifest is None else {e['inode']: e for e in manifest['files']}
    records = []
    for number in sorted(set(files) | set(expected)):
        inode, reference = files.get(number), expected.get(number)
        if inode is None:
            status = 'MISSING_FILE'
        elif reference is None:
            status = 'NOT_ESTABLISHED'
        elif any(b not in {v['id'] for v in image['blocks']} for b in inode['blocks']):
            status = 'MISSING_BLOCK'
        elif inode['size'] != reference['size']:
            status = 'SIZE_MISMATCH'
        elif len(file_bytes(image, inode)[:inode['size']]) != inode['size']:
            status = 'MISSING_PAYLOAD_BYTES'
        elif mutation == 'skip-digest' or digest(file_bytes(image, inode)[:inode['size']]) == reference['sha256']:
            status = 'VERIFIED'
        else:
            status = 'DIGEST_MISMATCH'
        records.append({'inode': number, 'status': status})
    failures = any(r['status'] not in ('VERIFIED', 'NOT_ESTABLISHED') for r in records)
    overall = 'FAIL' if failures else 'VERIFIED' if records and all(r['status'] == 'VERIFIED' for r in records) else 'NOT_ESTABLISHED'
    return {'status': overall, 'files': records}


def inspect(image, manifest=None, mutation='none'):
    nodes = {n['id']: n for n in image['inodes']}
    directories = {d['inode']: d['entries'] for d in image['dirs']}
    blocks = {b['id']: b for b in image['blocks']}
    issues, owners, incoming = [], {}, {n: 0 for n in nodes}

    def issue(code, **details):
        issues.append({'code': code, **details})

    if 1 not in nodes or 2 not in nodes or nodes.get(1, {}).get('kind') != 'dir' or nodes.get(2, {}).get('kind') != 'dir':
        issue('ROOT_LAYOUT')
    if set(directories) != {n['id'] for n in nodes.values() if n['kind'] == 'dir'}:
        issue('DIRECTORY_RECORD_SET')
    if [e for e in directories.get(1, []) if e['name'] == 'lost+found'] != [{'name': 'lost+found', 'inode': 2}]:
        issue('ROOT_LAYOUT')
    for directory, entries in sorted(directories.items()):
        names = set()
        for entry in entries:
            if entry['name'] in names:
                issue('DUPLICATE_NAME', directory=directory, name=entry['name'])
            names.add(entry['name'])
            if entry['inode'] not in nodes:
                issue('DANGLING_ENTRY', directory=directory, name=entry['name'], target=entry['inode'])
            else:
                incoming[entry['inode']] += 1
    for number, inode in sorted(nodes.items()):
        if inode['kind'] == 'file':
            if len(set(inode['blocks'])) != len(inode['blocks']):
                issue('DUPLICATE_FILE_BLOCK', inode=number)
            if inode['size'] > 8 * len(inode['blocks']) or len(inode['blocks']) != (inode['size'] + 7) // 8:
                issue('SIZE_CAPACITY', inode=number)
            for block in inode['blocks']:
                if block not in blocks:
                    issue('MISSING_BLOCK', inode=number, block=block)
                owners.setdefault(block, set()).add(number)
        if inode['kind'] == 'dir' and incoming[number] > (0 if number == 1 else 1):
            issue('DIRECTORY_PARENT_COUNT', inode=number, incoming=incoming[number])
        target_links = 1 if number == 1 else incoming[number]
        if inode['nlink'] != target_links:
            issue('NLINK', inode=number, expected=target_links)
    for block, files in sorted(owners.items()):
        if len(files) > 1 and mutation != 'ignore-shared':
            issue('SHARED_BLOCK', block=block, owners=sorted(files))
    colors = {}

    def visit(number):
        if colors.get(number) == 1:
            issue('DIRECTORY_CYCLE', inode=number)
            return
        if colors.get(number) == 2:
            return
        colors[number] = 1
        for entry in directories.get(number, []):
            if nodes.get(entry['inode'], {}).get('kind') == 'dir':
                visit(entry['inode'])
        colors[number] = 2

    for number in sorted(directories):
        visit(number)
    reachable, pending = set(), [1]
    while pending:
        number = pending.pop()
        if number in reachable or number not in nodes:
            continue
        reachable.add(number)
        pending.extend(e['inode'] for e in directories.get(number, []))
    orphans = sorted(set(nodes) - reachable)
    for number in orphans:
        issue('ORPHAN_FILE' if nodes[number]['kind'] == 'file' else 'ORPHAN_DIRECTORY', inode=number)
    missing = sorted(set(owners) - set(image['bitmap']))
    extra = sorted(set(image['bitmap']) - set(owners))
    if missing:
        issue('BITMAP_MISSING', blocks=missing)
    if extra:
        issue('UNOWNED_ALLOCATED', blocks=extra)
    return {'structural': 'PASS' if not issues else 'FAIL', 'issues': issues,
            'reachable': sorted(reachable), 'orphans': orphans,
            'owners': {str(b): sorted(v) for b, v in sorted(owners.items())},
            'used_blocks': len(owners), 'free_blocks': 8 - len(owners),
            'identity': identity(image, manifest, mutation)}


def make_plan(raw, image, manifest_raw, manifest, mutation='none'):
    before = inspect(image, manifest, mutation)
    allowed = {'DANGLING_ENTRY', 'SIZE_CAPACITY', 'NLINK', 'BITMAP_MISSING', 'ORPHAN_FILE'}
    reasons = sorted({i['code'] for i in before['issues'] if i['code'] not in allowed})
    if reasons:
        return {'format': 'EDUFS-PLAN1', 'image_sha256': digest(raw),
                'manifest_sha256': None if manifest_raw is None else digest(manifest_raw),
                'status': 'REFUSED', 'reasons': reasons, 'actions': [], 'before': before}
    actions = []
    work = copy.deepcopy(image)
    nodes = {n['id']: n for n in work['inodes']}
    expected = {} if manifest is None else {e['inode']: e for e in manifest['files']}
    for finding in before['issues']:
        if finding['code'] == 'DANGLING_ENTRY':
            actions.append({'op': 'remove_entry', 'directory': finding['directory'], 'name': finding['name'], 'target': finding['target']})
    for number, inode in sorted(nodes.items()):
        if inode['kind'] != 'file':
            continue
        reference = expected.get(number)
        capacity_bad = any(i['code'] == 'SIZE_CAPACITY' and i['inode'] == number for i in before['issues'])
        if capacity_bad or (reference and reference['size'] != inode['size']):
            if reference and all(b in {v['id'] for v in work['blocks']} for b in inode['blocks']) and len(inode['blocks']) == (reference['size'] + 7) // 8 and digest(file_bytes(work, inode)[:reference['size']]) == reference['sha256']:
                actions.append({'op': 'set_size', 'inode': number, 'value': reference['size']})
            elif mutation == 'guess-size':
                actions.append({'op': 'set_size', 'inode': number, 'value': len(inode['blocks']) * 8})
            else:
                reasons.append('SIZE_WITHOUT_VALID_REFERENCE')
    for number in before['orphans']:
        if nodes[number]['kind'] == 'file':
            if mutation == 'drop-orphan':
                actions.append({'op': 'delete_inode', 'inode': number})
            else:
                name = 'inode_' + str(number)
                existing = next((d['entries'] for d in work['dirs'] if d['inode'] == 2), [])
                if any(e['name'] == name for e in existing):
                    reasons.append('RECOVERY_NAME_COLLISION')
                else:
                    actions.append({'op': 'add_entry', 'directory': 2, 'name': name, 'target': number})
    apply_actions(work, actions)
    interim = inspect(work, manifest, mutation)
    for finding in interim['issues']:
        if finding['code'] == 'NLINK':
            actions.append({'op': 'set_nlink', 'inode': finding['inode'], 'value': finding['expected']})
    if work['bitmap'] != sorted(int(b) for b in interim['owners']):
        actions.append({'op': 'set_bitmap', 'value': sorted(int(b) for b in interim['owners'])})
    # 같은 동작을 중복 적용하지 않고 원본에서 최종 후보를 만듭니다.
    candidate = copy.deepcopy(image)
    apply_actions(candidate, actions)
    after = inspect(candidate, manifest, mutation)
    if after['structural'] != 'PASS':
        reasons.extend(i['code'] for i in after['issues'])
    if after['identity']['status'] == 'FAIL':
        reasons.append('CONTENT_REFERENCE_MISMATCH')
    return {'format': 'EDUFS-PLAN1', 'image_sha256': digest(raw),
            'manifest_sha256': None if manifest_raw is None else digest(manifest_raw),
            'status': 'REFUSED' if reasons else 'READY', 'reasons': sorted(set(reasons)),
            'actions': [] if reasons else actions, 'before': before}


def apply_actions(image, actions):
    for action in actions:
        op = action['op']
        if op in ('remove_entry', 'add_entry'):
            directory = next(d for d in image['dirs'] if d['inode'] == action['directory'])
            if op == 'remove_entry':
                directory['entries'] = [e for e in directory['entries'] if not (e['name'] == action['name'] and e['inode'] == action['target'])]
            else:
                directory['entries'].append({'name': action['name'], 'inode': action['target']})
        elif op in ('set_size', 'set_nlink'):
            inode = next(n for n in image['inodes'] if n['id'] == action['inode'])
            inode['size' if op == 'set_size' else 'nlink'] = action['value']
        elif op == 'set_bitmap':
            image['bitmap'] = action['value']
        elif op == 'delete_inode':
            image['inodes'] = [n for n in image['inodes'] if n['id'] != action['inode']]
        else:
            raise ImageError('UNKNOWN_ACTION')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True, type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--action', required=True, choices=('check', 'plan', 'repair'))
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--mutation', choices=MUTATIONS, default='none')
    args = parser.parse_args()
    try:
        raw, image = load_image(args.image)
        manifest_raw, manifest = load_manifest(args.manifest)
        if args.action == 'check':
            result = {'status': 'CHECKED', 'image_sha256': digest(raw), **inspect(image, manifest, args.mutation)}
        else:
            plan = make_plan(raw, image, manifest_raw, manifest, args.mutation)
            if args.action == 'plan':
                result = plan
            else:
                require(args.plan is not None and args.output is not None, 'PLAN_AND_NEW_OUTPUT_REQUIRED')
                require(args.output.resolve() != args.image.resolve() and not args.output.exists(), 'OUTPUT_ALREADY_EXISTS_OR_SOURCE')
                _, supplied = read_json(args.plan, MAX_IMAGE)
                require(supplied == plan, 'STALE_OR_MODIFIED_PLAN')
                require(plan['status'] == 'READY', 'AMBIGUOUS_REPAIR_REFUSED')
                repaired = copy.deepcopy(image)
                apply_actions(repaired, plan['actions'])
                repaired['checksum'] = digest(canonical({k: v for k, v in repaired.items() if k != 'checksum'}))
                payload = canonical(repaired) + b'\n'
                require(len(payload) <= MAX_IMAGE, 'REPAIRED_IMAGE_TOO_LARGE')
                require(inspect(repaired, manifest, args.mutation)['structural'] == 'PASS', 'POSTCHECK_FAILED')
                require(args.image.read_bytes() == raw, 'SOURCE_CHANGED_DURING_REPAIR')
                with args.output.open('xb') as stream:  # xb는 기존 파일을 덮어쓰지 않습니다.
                    require(stream.write(payload) == len(payload), 'SHORT_WRITE')
                    stream.flush()
                    os.fsync(stream.fileno())
                result = {'status': 'REPAIRED_COPY', 'source_sha256': digest(raw), 'output_sha256': digest(payload),
                          'actions': plan['actions'], 'after': inspect(repaired, manifest, args.mutation)}
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 0
    except (ImageError, OSError, ValueError, TypeError, KeyError, StopIteration, RecursionError) as error:
        print(json.dumps({'status': 'REJECTED', 'reason': str(error)}, ensure_ascii=True))
        return 3


if __name__ == '__main__':
    raise SystemExit(main())

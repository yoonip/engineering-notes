"""Execute new EDUFS1 host-file cases and preserve commands/results."""

import argparse  # 명령행에서 새 출력 폴더와 의도한 결함을 받습니다.
import copy  # 중첩 fixture의 원본을 바꾸지 않고 손상을 주입합니다.
import datetime  # 실제 실행 시각을 기록합니다.
import hashlib  # 소스·입력·결과의 SHA-256을 계산합니다.
import json  # 이미지·계획·관측 보고서를 저장합니다.
from pathlib import Path  # 호스트 경로를 객체로 다룹니다.
import platform  # 실행한 운영체제를 기록합니다.
import subprocess  # 각 검사·계획·사본 복구를 새 Python에서 실행합니다.
import sys  # 현재 Python과 -O 설정을 자식에도 적용합니다.

HERE = Path(__file__).resolve().parent
MUTATIONS = ('none', 'ignore-shared', 'guess-size', 'drop-orphan', 'skip-digest')


class CheckFailed(RuntimeError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8') + b'\n'


def reseal(image):
    body = {k: v for k, v in image.items() if k != 'checksum'}
    image['checksum'] = sha(encoded(body)[:-1])
    return image


def dump(path, value):
    with path.open('xb') as stream:
        stream.write(encoded(value))


class Suite:
    def __init__(self, output, mutation):
        self.output, self.mutation = output, mutation
        self.fixture = json.loads((HERE / 'fixtures.json').read_text(encoding='utf-8'))
        self.checks, self.commands = [], []
        self.cases = []

    def eq(self, name, actual, expected):  # == 대조를 기록하고 다르면 즉시 멈춥니다.
        self.checks.append({'name': name, 'actual': actual, 'expected': expected, 'passed': actual == expected})
        if actual != expected:
            raise CheckFailed(name + ': ' + repr(actual) + ' != ' + repr(expected))

    def case(self, label, image=None, manifest=True):
        folder = self.output / label
        folder.mkdir()
        path = folder / 'image.json'
        image = copy.deepcopy(self.fixture['seed_image'] if image is None else image)
        dump(path, reseal(image))
        reference = None
        if manifest is not False:
            reference = folder / 'manifest.json'
            dump(reference, self.fixture['trusted_manifest'] if manifest is True else manifest)
        self.cases.append({'label': label, 'image': str(path), 'initial_sha256': sha(path.read_bytes()),
                           'manifest_sha256': None if reference is None else sha(reference.read_bytes())})
        return path, reference

    def call(self, image, manifest, action, expected_exit=0, plan=None, output=None):
        command = [sys.executable, '-X', 'utf8', '-B']
        if sys.flags.optimize:
            command.append('-O')
        command += [str(HERE / 'image_model.py'), '--image', str(image), '--action', action, '--mutation', self.mutation]
        if manifest is not None:
            command += ['--manifest', str(manifest)]
        if plan is not None:
            command += ['--plan', str(plan)]
        if output is not None:
            command += ['--output', str(output)]
        before = sha(image.read_bytes())
        record = {'command': command, 'image_sha256_before': before,
                  'manifest_sha256': None if manifest is None else sha(manifest.read_bytes()),
                  'plan_sha256': None if plan is None else sha(plan.read_bytes())}
        self.commands.append(record)
        try:
            completed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=15)
        except (OSError, subprocess.TimeoutExpired) as error:
            record['infrastructure_error'] = str(error)
            raise CheckFailed('CHILD_EXECUTION_FAILED') from error
        record.update({'exit': completed.returncode, 'stdout': completed.stdout, 'stderr': completed.stderr,
                       'image_sha256_after': sha(image.read_bytes())})
        self.eq(action + '.source_preserved.' + image.parent.name, record['image_sha256_after'], before)
        self.eq(action + '.exit.' + image.parent.name, completed.returncode, expected_exit)
        try:
            result = json.loads(completed.stdout)
        except ValueError as error:
            raise CheckFailed('CHILD_JSON_MISSING_OR_INVALID') from error
        record['result'] = result
        if expected_exit == 3:
            self.eq(action + '.rejected.' + image.parent.name, result.get('status'), 'REJECTED')
        return result

    def plan_file(self, image, manifest, filename='plan.json'):
        plan = self.call(image, manifest, 'plan')
        path = image.parent / filename
        dump(path, plan)
        return path, plan

    def payloads(self, path):  # 검증 대상 함수를 불러오지 않고 실제 결과 파일을 읽습니다.
        image = json.loads(path.read_text(encoding='utf-8'))
        blocks = {b['id']: bytes.fromhex(b['data']) for b in image['blocks']}
        return {str(n['id']): b''.join(blocks[b] for b in n['blocks'])[:n['size']].hex()
                for n in image['inodes'] if n['kind'] == 'file'}

    def correct_cases(self):
        image, manifest = self.case('clean')
        self.eq('fixed seed size', image.stat().st_size, self.fixture['seed_file_bytes'])
        self.eq('fixed seed SHA', sha(image.read_bytes()), self.fixture['seed_image_sha256'])
        checked = self.call(image, manifest, 'check')
        self.eq('clean structure and identity', [checked['structural'], checked['identity']['status'], checked['used_blocks'], checked['free_blocks']], ['PASS', 'VERIFIED', 4, 4])
        self.eq('literal owners', checked['owners'], {'0': [3], '1': [3], '2': [4], '3': [5]})
        plan_path, plan = self.plan_file(image, manifest)
        self.eq('clean empty plan', [plan['status'], plan['actions']], ['READY', []])
        output = image.parent / 'copy.json'
        repaired = self.call(image, manifest, 'repair', plan=plan_path, output=output)
        self.eq('clean copy literal SHA', repaired['output_sha256'], self.fixture['seed_image_sha256'])
        prior = sha(output.read_bytes())
        self.call(image, manifest, 'repair', expected_exit=3, plan=plan_path, output=output)
        self.eq('existing output preserved', sha(output.read_bytes()), prior)
        self.call(image, manifest, 'repair', expected_exit=3, plan=plan_path, output=image)

        damaged = copy.deepcopy(self.fixture['seed_image'])
        next(n for n in damaged['inodes'] if n['id'] == 3).update(size=19, nlink=7)
        damaged['dirs'][2]['entries'].append({'name': 'ghost.txt', 'inode': 31})
        damaged['bitmap'] = [0, 2, 3]
        image, manifest = self.case('metadata_damage', damaged)
        checked = self.call(image, manifest, 'check')
        self.eq('metadata four independent findings', sorted(i['code'] for i in checked['issues']), ['BITMAP_MISSING', 'DANGLING_ENTRY', 'NLINK', 'SIZE_CAPACITY'])
        plan_path, plan = self.plan_file(image, manifest)
        self.eq('metadata plan literal', [plan['status'], plan['actions']], ['READY', self.fixture['expected_repair_actions']])
        output = image.parent / 'repaired.json'
        self.call(image, manifest, 'repair', plan=plan_path, output=output)
        self.eq('metadata copy equals seed bytes', output.read_bytes().hex(), encoded(self.fixture['seed_image']).hex())
        expected = {str(e['inode']): e['hex'] for e in self.fixture['expected_files']}
        self.eq('independent three file byte literals', self.payloads(output), expected)
        checked = self.call(output, manifest, 'check')
        self.eq('post-repair structure and identity', [checked['structural'], checked['identity']['status']], ['PASS', 'VERIFIED'])
        again_path, again = self.plan_file(output, manifest, 'second-plan.json')
        self.eq('repair fixed point empty plan', again['actions'], [])
        second = image.parent / 'repaired-again.json'
        self.call(output, manifest, 'repair', plan=again_path, output=second)
        self.eq('repair idempotent bytes', second.read_bytes().hex(), output.read_bytes().hex())

        orphan = copy.deepcopy(self.fixture['seed_image'])
        orphan['dirs'][0]['entries'] = [e for e in orphan['dirs'][0]['entries'] if e['inode'] != 5]
        next(n for n in orphan['inodes'] if n['id'] == 5)['nlink'] = 0
        image, manifest = self.case('orphan_file', orphan, manifest=False)
        checked = self.call(image, manifest, 'check')
        self.eq('unreachable regular inode literal', checked['orphans'], [5])
        plan_path, plan = self.plan_file(image, manifest)
        self.eq('retain orphan instead of deleting', [plan['status'], plan['actions']], ['READY', self.fixture['expected_orphan_actions']])
        output = image.parent / 'recovered.json'
        self.call(image, manifest, 'repair', plan=plan_path, output=output)
        result = json.loads(output.read_text(encoding='utf-8'))
        self.eq('new salvage name literal', result['dirs'][1]['entries'], [{'inode': 5, 'name': 'inode_5'}])
        self.eq('lost original name remains unknown', 'archive.bin' in [e['name'] for e in result['dirs'][0]['entries']], False)
        self.eq('orphan original payload literal', self.payloads(output)['5'], '4f525048414e0a')
        self.eq('salvage preserves all physical block bytes', result['blocks'], self.fixture['seed_image']['blocks'])
        checked = self.call(output, None, 'check')
        self.eq('salvage alone cannot prove identity', [checked['structural'], checked['identity']['status']], ['PASS', 'NOT_ESTABLISHED'])
        ref = output.parent / 'trusted-manifest.json'
        dump(ref, self.fixture['trusted_manifest'])
        self.eq('salvage with independent digest', self.call(output, ref, 'check')['identity']['status'], 'VERIFIED')

        hardlink = copy.deepcopy(self.fixture['seed_image'])
        hardlink['dirs'][0]['entries'].append({'name': 'same-config.bin', 'inode': 3})
        next(n for n in hardlink['inodes'] if n['id'] == 3)['nlink'] = 2
        image, manifest = self.case('valid_hardlink', hardlink)
        checked = self.call(image, manifest, 'check')
        self.eq('two names one inode allowed', [checked['structural'], checked['owners']['0']], ['PASS', [3]])

    def ambiguous_cases(self):
        seed = self.fixture['seed_image']
        shared = copy.deepcopy(seed)
        next(n for n in shared['inodes'] if n['id'] == 4)['blocks'] = [0]
        shared['bitmap'] = [0, 1, 3]
        image, reference = self.case('shared_block', shared, manifest=False)
        checked = self.call(image, reference, 'check')
        self.eq('two distinct inode owners detected', [i for i in checked['issues'] if i['code'] == 'SHARED_BLOCK'], [{'code': 'SHARED_BLOCK', 'block': 0, 'owners': [3, 4]}])
        self.eq('shared ownership refuses automatic choice', self.call(image, reference, 'plan')['status'], 'REFUSED')
        for label, change, code in (
            ('directory_cycle', lambda i: i['dirs'][2]['entries'].append({'name': 'back', 'inode': 1}), 'DIRECTORY_CYCLE'),
            ('two_directory_parents', lambda i: i['dirs'][1]['entries'].append({'name': 'reports-too', 'inode': 6}), 'DIRECTORY_PARENT_COUNT'),
            ('orphan_directory', lambda i: i['dirs'][0].update(entries=[e for e in i['dirs'][0]['entries'] if e['inode'] != 6]), 'ORPHAN_DIRECTORY'),
            ('duplicate_name', lambda i: i['dirs'][0]['entries'].append({'name': 'config.bin', 'inode': 4}), 'DUPLICATE_NAME'),
            ('missing_payload_block', lambda i: i.update(blocks=[b for b in i['blocks'] if b['id'] != 0]), 'MISSING_BLOCK'),
            ('repeated_file_block', lambda i: next(n for n in i['inodes'] if n['id'] == 3).update(blocks=[0, 0]), 'DUPLICATE_FILE_BLOCK'),
        ):
            damaged = copy.deepcopy(seed)
            change(damaged)
            image, reference = self.case(label, damaged, manifest=False)
            checked = self.call(image, reference, 'check')
            self.eq(label + '.detected', code in [i['code'] for i in checked['issues']], True)
            plan_path, plan = self.plan_file(image, reference)
            self.eq(label + '.refused', plan['status'], 'REFUSED')
            output = image.parent / 'must-not-exist.json'
            self.call(image, reference, 'repair', expected_exit=3, plan=plan_path, output=output)
            self.eq(label + '.no output published', output.exists(), False)

        bad_size = copy.deepcopy(seed)
        next(n for n in bad_size['inodes'] if n['id'] == 3)['size'] = 19
        image, reference = self.case('size_without_reference', bad_size, manifest=False)
        self.eq('do not clamp unknown original length', self.call(image, reference, 'plan')['status'], 'REFUSED')

        leak = copy.deepcopy(seed)
        leak['bitmap'].append(6)
        leak['blocks'][6].update(data=b'LOSTDATA'.hex(), sha256=sha(b'LOSTDATA'))
        image, reference = self.case('unowned_allocated_block', leak)
        plan = self.call(image, reference, 'plan')
        self.eq('unowned allocation is not automatically freed', [plan['status'], plan['reasons']], ['REFUSED', ['UNOWNED_ALLOCATED']])
        self.eq('unowned bytes are not assigned to an invented file', len(json.loads(image.read_text(encoding='utf-8'))['inodes']), 6)

        altered = copy.deepcopy(seed)
        raw = b'NO\n' + bytes(5)
        altered['blocks'][2].update(data=raw.hex(), sha256=sha(raw))
        image, reference = self.case('resealed_changed_payload', altered)
        checked = self.call(image, None, 'check')
        self.eq('valid structure does not prove old bytes', [checked['structural'], checked['identity']['status']], ['PASS', 'NOT_ESTABLISHED'])
        checked = self.call(image, reference, 'check')
        self.eq('external digest detects changed bytes', [checked['structural'], checked['identity']['status']], ['PASS', 'FAIL'])
        self.eq('known wrong payload not repaired from hash alone', self.call(image, reference, 'plan')['status'], 'REFUSED')

        absent = copy.deepcopy(seed)
        absent['inodes'] = [n for n in absent['inodes'] if n['id'] != 5]
        absent['dirs'][0]['entries'] = [e for e in absent['dirs'][0]['entries'] if e['inode'] != 5]
        absent['bitmap'] = [0, 1, 2]
        absent['blocks'][3].update(data=bytes(8).hex(), sha256=sha(bytes(8)))
        image, reference = self.case('missing_inode_and_payload', absent)
        checked = self.call(image, None, 'check')
        self.eq('consistent deletion may hide historical loss', [checked['structural'], checked['identity']['status']], ['PASS', 'NOT_ESTABLISHED'])
        checked = self.call(image, reference, 'check')
        self.eq('external inventory detects missing file', [checked['identity']['status'], checked['identity']['files'][-1]], ['FAIL', {'inode': 5, 'status': 'MISSING_FILE'}])
        self.eq('missing payload not reconstructed from digest', self.call(image, reference, 'plan')['status'], 'REFUSED')

    def boundaries(self):
        seed = self.fixture['seed_image']
        empty = copy.deepcopy(seed)
        next(n for n in empty['inodes'] if n['id'] == 4).update(size=0, blocks=[])
        empty['bitmap'] = [0, 1, 3]
        manifest = copy.deepcopy(self.fixture['trusted_manifest'])
        next(f for f in manifest['files'] if f['inode'] == 4).update(size=0, sha256=sha(b''))
        image, reference = self.case('empty_file_boundary', empty, manifest=manifest)
        checked = self.call(image, reference, 'check')
        self.eq('zero length file has zero blocks', [checked['structural'], checked['identity']['status'], checked['used_blocks']], ['PASS', 'VERIFIED', 3])

        full = copy.deepcopy(seed)
        next(n for n in full['inodes'] if n['id'] == 3).update(size=64, blocks=list(range(8)))
        for inode in full['inodes']:
            if inode['id'] in (4, 5):
                inode.update(size=0, blocks=[])
        full['bitmap'] = list(range(8))
        image, reference = self.case('full_capacity_boundary', full, manifest=False)
        checked = self.call(image, reference, 'check')
        self.eq('all eight blocks fit 64 byte file', [checked['structural'], checked['used_blocks'], checked['free_blocks']], ['PASS', 8, 0])

        short = copy.deepcopy(seed)
        next(n for n in short['inodes'] if n['id'] == 3).update(size=64, blocks=[0])
        short['bitmap'] = [0, 2, 3]
        manifest = copy.deepcopy(self.fixture['trusted_manifest'])
        next(f for f in manifest['files'] if f['inode'] == 3).update(size=64, sha256=sha(b'GAIN=1.2'))
        image, reference = self.case('digest_of_shorter_than_declared_file', short, manifest=manifest)
        checked = self.call(image, reference, 'check')
        self.eq('short bytes cannot verify declared 64 byte file', [checked['structural'], checked['identity']['status'], checked['identity']['files'][0]],
                ['FAIL', 'FAIL', {'inode': 3, 'status': 'MISSING_PAYLOAD_BYTES'}])
        self.eq('short payload not synthesized from size and digest', self.call(image, reference, 'plan')['status'], 'REFUSED')

        for label, change, reason in (
            ('unsupported_features', lambda i: i['super'].update(features=['extents']), 'UNSUPPORTED_GEOMETRY_OR_FEATURE'),
            ('boolean_size', lambda i: next(n for n in i['inodes'] if n['id'] == 3).update(size=True), 'INTEGER_RANGE_OR_TYPE'),
            ('block_out_of_range', lambda i: next(n for n in i['inodes'] if n['id'] == 3).update(blocks=[8]), 'INTEGER_RANGE_OR_TYPE'),
            ('invalid_name', lambda i: i['dirs'][0]['entries'][0].update(name='../escape'), 'ENTRY_NAME'),
            ('duplicate_inode', lambda i: i['inodes'].append(copy.deepcopy(i['inodes'][0])), 'DUPLICATE_INODE'),
            ('bad_block_checksum', lambda i: i['blocks'][0].update(sha256='0' * 64), 'BLOCK_CHECKSUM'),
        ):
            malformed = copy.deepcopy(seed)
            change(malformed)
            image, reference = self.case(label, malformed, manifest=False)
            self.eq(label + '.reason', self.call(image, reference, 'check', expected_exit=3)['reason'], reason)

        for label, raw, reason in (
            ('bad_image_checksum', encoded({**seed, 'checksum': '0' * 64}), 'IMAGE_CHECKSUM'),
            ('duplicate_json_key', b'{"format":"EDUFS1","format":"EDUFS1"}\n', 'DUPLICATE_JSON_KEY'),
            ('oversized_input', b' ' * 65537, 'INPUT_TOO_LARGE'),
            ('truncated_json', b'{"format":', None),
        ):
            image, reference = self.case(label, manifest=False)
            image.write_bytes(raw)
            rejected = self.call(image, reference, 'check', expected_exit=3)
            if reason is not None:
                self.eq(label + '.reason', rejected['reason'], reason)

        image, reference = self.case('stale_plan')
        plan_path, plan = self.plan_file(image, reference)
        changed = copy.deepcopy(seed)
        changed['inodes'][2]['nlink'] = 7
        image.write_bytes(encoded(reseal(changed)))
        output = image.parent / 'must-not-exist.json'
        self.eq('stale plan input hash rejected', self.call(image, reference, 'repair', expected_exit=3, plan=plan_path, output=output)['reason'], 'STALE_OR_MODIFIED_PLAN')
        self.eq('stale plan no output', output.exists(), False)

        image, reference = self.case('tampered_plan')
        plan_path, plan = self.plan_file(image, reference)
        plan['actions'].append({'op': 'delete_inode', 'inode': 3})
        plan_path.write_bytes(encoded(plan))
        self.eq('modified action rejected', self.call(image, reference, 'repair', expected_exit=3, plan=plan_path, output=image.parent / 'must-not-exist.json')['reason'], 'STALE_OR_MODIFIED_PLAN')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--mutation', choices=MUTATIONS, default='none')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output already exists: ' + str(args.output))
    args.output.mkdir(parents=True, exist_ok=False)
    suite = Suite(args.output.resolve(), args.mutation)
    source_hashes = {n: sha((HERE / n).read_bytes()) for n in ('image_model.py', 'verify.py', 'fixtures.json')}
    report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'python': sys.version,
              'executable': sys.executable, 'platform': platform.platform(), 'optimize': sys.flags.optimize,
              'argv': sys.argv, 'mutation': args.mutation,
              'scope': 'New bounded EDUFS1 JSON host images and fresh Python children; no raw disk, mount, real fsck, ext4 execution or power-loss claim.',
              'source_and_input_sha256': source_hashes}
    try:
        suite.correct_cases()
        suite.ambiguous_cases()
        suite.boundaries()
        suite.eq('source unchanged throughout execution', {n: sha((HERE / n).read_bytes()) for n in source_hashes}, source_hashes)
        report['status'] = 'PASS'
    except (CheckFailed, OSError, ValueError, KeyError, TypeError) as error:
        report.update(status='ERROR', reason=str(error))
    report.update(checks=suite.checks, commands=suite.commands, cases=suite.cases,
                  counts={'checks': len(suite.checks), 'cases': len(suite.cases), 'subprocesses': len(suite.commands),
                          'failed_checks': sum(not c['passed'] for c in suite.checks)})
    dump(args.output / 'results.json', report)
    print(json.dumps({'status': report['status'], **report['counts']}, sort_keys=True))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

"""NAND의 free pool·마모·scrub·실패 보존을 리터럴 기대값과 대조합니다."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

from models import ContractError, Manager, Nand

BASE = Path(__file__).resolve().parent
MUTATIONS = ('none', 'nand-zero-to-one', 'reuse-bad', 'early-remap', 'publish-ue', 'skip-scrub')


def require(condition, message):
    if not condition:  # -O에서도 남는 명시적 검사입니다.
        raise AssertionError(message)


def rejected(function, reason):
    try:
        function()
    except ContractError as exc:
        require(str(exc) == reason, f'{exc} != {reason}')
        return {'reason': str(exc), 'exception': type(exc).__name__}
    raise AssertionError('invalid path accepted: ' + reason)


def validate_fixture(value):
    if not isinstance(value, dict) or set(value) != {'schema', 'wear', 'scrub'}:
        raise ContractError('FIXTURE_KEYS')
    if type(value['schema']) is not int or value['schema'] != 1:
        raise ContractError('FIXTURE_SCHEMA')
    wear, scrub = value['wear'], value['scrub']
    wear_keys = {'initial_erases', 'factory_bad', 'cold', 'initial_hot', 'hot_updates', 'dynamic_targets',
                 'static_move', 'static_targets', 'dynamic_expected', 'static_expected',
                 'expected_waf', 'expected_erase_spread'}
    scrub_keys = {'payload', 'count_reads_expected_due', 'count_move', 'post_move', 'ce_observation',
                  'ue_observation', 'faults'}
    if not isinstance(wear, dict) or set(wear) != wear_keys or not isinstance(scrub, dict) or set(scrub) != scrub_keys:
        raise ContractError('FIXTURE_SECTION')
    if not isinstance(wear['hot_updates'], list) or len(wear['hot_updates']) != 4:
        raise ContractError('FIXTURE_UPDATES')
    if not isinstance(scrub['faults'], list) or len(scrub['faults']) != 4:
        raise ContractError('FIXTURE_FAULTS')
    for row in scrub['faults']:
        if not isinstance(row, dict) or set(row) != {'fault', 'expected', 'mapping', 'bad', 'free', 'public_read'}:
            raise ContractError('FIXTURE_FAULT_ROW')


def checks(fixture, mutation):
    fresh = Manager(mutation=mutation)
    require(fresh.free_blocks() == [0, 1, 2, 3, 4], 'factory bad block entered free pool')
    fresh.nand.program(1, 0, '12345678', fail=True)
    require(fresh.free_blocks() == [0, 2, 3, 4] and fresh.nand.block(1).kind == 'GROWN_BAD',
            'grown bad block entered free pool')

    wear = fixture['wear']
    wear_results = {}
    for policy in ('dynamic', 'static'):
        manager = Manager(wear['factory_bad'], wear['initial_erases'], mutation=mutation)
        manager.seed(0, 0, wear['cold'])
        manager.seed(1, 1, wear['initial_hot'])
        manager.reset_metrics()  # 초기 자료·erase count는 측정 창 밖에서 준비합니다.
        relocation = manager.static_level() if policy == 'static' else None
        if policy == 'static':
            require(relocation == wear['static_move'], 'static move literal differs')
        rows = [manager.write(1, payload) for payload in wear['hot_updates']]
        require([row['target'] for row in rows] == wear[policy + '_targets'], policy + ' target literal differs')
        snapshot = manager.snapshot()
        require(snapshot == wear[policy + '_expected'], policy + ' wear/counter literal differs')
        observed_cold = [manager.read_page(0, page)['data_hex'] for page in range(2)]
        observed_hot = [manager.read_page(1, page)['data_hex'] for page in range(2)]
        require(observed_cold == wear['cold'] and observed_hot == ['44444444', 'dddddddd'],
                'wear policy changed payload')
        good_erases = [b.erases for b in manager.nand.blocks if b.kind == 'GOOD']
        spread = max(good_erases) - min(good_erases)
        waf = manager.nand.program_attempt_bytes / manager.host_bytes
        require(spread == wear['expected_erase_spread'][policy] and waf == wear['expected_waf'][policy],
                policy + ' independent arithmetic differs')
        wear_results[policy] = {'static_move': relocation, 'writes': rows, 'snapshot': snapshot,
                                'erase_spread': spread, 'program_bytes_per_host_byte': waf,
                                'cold_read': observed_cold, 'hot_read': observed_hot}

    scrub = fixture['scrub']
    def seeded():
        manager = Manager(mutation=mutation)
        manager.seed(0, 0, scrub['payload'])
        manager.reset_metrics()
        return manager

    counted = seeded()
    observations = [counted.read_page(0, 0) for _ in range(4)]
    require([row['scrub_due'] for row in observations] == scrub['count_reads_expected_due'],
            'read-count scrub threshold literal differs')
    moved = counted.scrub(0)
    require(moved == scrub['count_move'] and counted.snapshot() == scrub['post_move'], 'scrub move literal differs')
    require(counted.nand.block(1).reads == 2 and counted.nand.block(1).corrected_max == 0,
            'verification reads were not counted on target')
    require(not counted.due(0), 'new scrub target unexpectedly due before further reads')

    ce = seeded()
    ce_observation = ce.read_page(0, 0, corrected=2)
    require(ce_observation == scrub['ce_observation'], 'CE-triggered scrub literal differs')
    failures = []
    for row in scrub['faults']:
        manager = seeded()
        manager.read_page(0, 0, corrected=2)
        source_before = list(manager.nand.block(0).pages)
        result = manager.scrub(0, row['fault'])
        require(result == row['expected'], 'scrub ' + row['fault'] + ' outcome differs')
        require({str(l): p for l, p in manager.mapping.items()} == row['mapping'], 'failed move published mapping')
        require([i for i, b in enumerate(manager.nand.blocks) if b.kind == 'GROWN_BAD'] == row['bad'] and
                manager.free_blocks() == row['free'], 'failed move retirement/free pool differs')
        if row['fault'] != 'erase':
            require(manager.nand.block(0).pages == source_before and manager.nand.block(0).erases == 0,
                    'failed migration erased or changed source')
        published = [manager.read_page(0, page)['data_hex'] for page in range(2)]
        require(published == row['public_read'], 'unverified or UE data published')
        failures.append({'fault': row['fault'], 'result': result, 'snapshot': manager.snapshot(),
                         'published_hex': published, 'source_preserved_before_cleanup': row['fault'] != 'erase'})
    ue = seeded()
    ue_observation = ue.read_page(0, 0, ue=True)
    require(ue_observation == scrub['ue_observation'], 'UE data was published')
    require(ue.scrub(0) == {'result': 'SOURCE_UE', 'source': 0, 'mapped': 0}, 'UE source migrated')

    raw = Nand(mutation=mutation)
    raw.program(0, 0, 'f0f0f0f0')
    zero_to_one = rejected(lambda: raw.program(0, 0, 'ffffffff'), 'ERASE_REQUIRED')
    require(raw.blocks[0].pages[0].hex() == 'f0f0f0f0', 'rejected program changed bits')
    repeated = rejected(lambda: raw.program(0, 0, 'e0e0e0e0'), 'PAGE_ALREADY_PROGRAMMED')
    raw.erase(0)
    require([page.hex() for page in raw.blocks[0].pages] == ['ffffffff', 'ffffffff'], 'erase did not restore ones')
    raw.program(0, 0, 'aaaaaaaa')
    require(raw.blocks[0].pages[0].hex() == 'aaaaaaaa' and raw.blocks[0].erases == 1, 'erase/program literal differs')
    raw.erase(0, fail=True)
    require(raw.blocks[0].kind == 'GROWN_BAD' and raw.blocks[0].erases == 1, 'failed erase counted as successful')

    errors = [zero_to_one, repeated]
    def bad(function, reason):
        errors.append(rejected(function, reason))

    bad(lambda: raw.program(0, 0, '00000000'), 'BAD_BLOCK')
    bad(lambda: raw.erase(0), 'BAD_BLOCK')
    bad(lambda: raw.read(0, 0), 'BAD_BLOCK')
    bad(lambda: Nand(factory_bad=[1, 1]), 'DUPLICATE_BAD_BLOCK')
    bad(lambda: Nand(factory_bad=[True]), 'BLOCK_RANGE')
    bad(lambda: Nand(factory_bad=[6]), 'BLOCK_RANGE')
    bad(lambda: Nand(erase_counts=[0] * 5), 'ERASE_COUNT_LIST')
    bad(lambda: Nand(erase_counts=[-1] + [0] * 5), 'ERASE_COUNT_RANGE')
    bad(lambda: Manager(read_limit=0), 'READ_LIMIT_RANGE')
    bad(lambda: Manager(ce_limit=9), 'CE_LIMIT_RANGE')
    clean = Nand()
    bad(lambda: clean.program(0, 1, '00000000'), 'PAGE_ORDER')
    bad(lambda: clean.program(True, 0, '00000000'), 'BLOCK_RANGE')
    bad(lambda: clean.program(6, 0, '00000000'), 'BLOCK_RANGE')
    bad(lambda: clean.program(0, 2, '00000000'), 'PAGE_RANGE')
    bad(lambda: clean.program(0, 0, 'zzzzzzzz'), 'PAGE_HEX')
    bad(lambda: clean.program(0, 0, '11 22 33'), 'PAGE_HEX')
    bad(lambda: clean.program(0, 0, '00000000', fail=1), 'BOOL_REQUIRED')
    bad(lambda: clean.erase(0, fail=1), 'BOOL_REQUIRED')
    manager = seeded()
    before = manager.snapshot()
    bad(lambda: manager.read_page(0, 0, corrected=9), 'CORRECTED_RANGE')
    bad(lambda: manager.read_page(0, 0, ue=1), 'BOOL_REQUIRED')
    bad(lambda: manager.read_page(0, 0, corrected=1, ue=True), 'UE_COUNT_UNKNOWN')
    require(manager.nand.block(0).reads == 0 and manager.snapshot() == before, 'invalid telemetry changed state')
    bad(lambda: manager.write(3, scrub['payload']), 'LOGICAL_RANGE')
    bad(lambda: manager.read_page(1, 0), 'UNMAPPED_LOGICAL')
    bad(lambda: manager.write(0, []), 'TWO_PAGES_REQUIRED')
    bad(lambda: manager.write(0, scrub['payload'], fault='timeout'), 'FAULT_UNSUPPORTED')
    bad(lambda: manager.scrub(0, fault='other'), 'FAULT_UNSUPPORTED')
    bad(lambda: manager.static_level(gap=0), 'GAP_RANGE')
    bad(lambda: manager.seed(0, 1, scrub['payload']), 'SEED_CONFLICT')
    bad(lambda: manager.seed(1, 0, scrub['payload']), 'SEED_CONFLICT')
    bad(lambda: manager.seed(1, 5, scrub['payload']), 'BAD_BLOCK')
    require(manager.scrub(0) == {'result': 'NOT_DUE', 'source': 0}, 'unneeded scrub was not skipped')
    require(manager.static_level() == {'result': 'GAP_SMALL', 'source': 0, 'target': 1}, 'small wear gap moved')
    require(Manager().static_level() == {'result': 'NO_MAPPED_BLOCK'}, 'empty mapping static case differs')
    no_space = Manager(factory_bad=[3, 4, 5])
    for logical in range(3):
        no_space.seed(logical, logical, scrub['payload'])
    no_space.reset_metrics()
    bad(lambda: no_space.write(0, scrub['payload']), 'NO_FREE_BLOCK')
    require(no_space.snapshot()['mapping'] == {'0': 0, '1': 1, '2': 2} and
            no_space.nand.program_attempt_bytes == 0, 'out-of-space write changed mapping/data')

    for value in range(256):
        nand = Nand(factory_bad=[])
        text = f'{value:02x}' * 4
        nand.program(5, 0, text)
        nand.program(5, 1, text)
        require(nand.blocks[5].pages == [bytes([value]) * 4, bytes([value]) * 4], 'byte boundary program differs')
        nand.erase(5)
        require(nand.blocks[5].pages == [b'\xff' * 4, b'\xff' * 4], 'byte boundary erase differs')
    return {'wear': wear_results, 'count_observations': observations, 'count_move': moved,
            'post_count_move': counted.snapshot(), 'ce_observation': ce_observation,
            'ue_observation': ue_observation, 'migration_faults': failures,
            'input_rejections': errors, 'input_rejection_count': len(errors),
            'byte_boundary_cases': 256, 'boundary_physical_block': 5, 'boundary_pages': [0, 1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--fixture', type=Path, default=BASE / 'fixtures.json')
    parser.add_argument('--mutation', choices=MUTATIONS, default='none')
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output directory already exists; choose a new --out')
    try:
        fixture = json.loads(args.fixture.read_bytes())
        validate_fixture(fixture)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    args.out.mkdir(parents=True, exist_ok=False)
    sources = [BASE / 'models.py', BASE / 'runner.py', args.fixture.resolve()]
    report = {'scope': 'synthetic NAND policy; no raw commands, physical device, ECC decoder or power-cut test',
              'utc': datetime.now(timezone.utc).isoformat(), 'mutation': args.mutation,
              'environment': {'python': sys.version, 'executable': sys.executable,
                              'platform': platform.platform(), 'optimize': sys.flags.optimize},
              'argv': sys.argv, 'sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    try:
        report['observations'] = checks(fixture, args.mutation)
        report['status'], code = 'PASS', 0
    except (AssertionError, ContractError, TypeError, KeyError) as exc:
        report.update(status='ERROR', error_type=type(exc).__name__, error=str(exc))
        code = 1
    (args.out / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                         encoding='utf-8', newline='\n')
    print(json.dumps({'status': report['status'], 'mutation': args.mutation, 'exit_code': code,
                      'result': str(args.out / 'result.json')}, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())

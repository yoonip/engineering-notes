"""리터럴 기대값, 입력 경계, 의도적 오류 구현을 대조합니다."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

from models import Card, ContractError, Nvme, blocks_at

BASE = Path(__file__).resolve().parent
MUTATIONS = ('none', 'nvme-completion-is-durable', 'nvme-fua-flushes-all',
             'nvme-ignore-flush-error', 'card-ignore-status-error', 'card-busy-is-done')
METHODS = {
    'nvme': {'submit_write', 'submit_flush', 'complete', 'read', 'power_loss'},
    'card': {'enable_cache', 'submit_write', 'poll', 'timeout', 'flush', 'read', 'power_loss'},
}


def require(condition, message):
    if not condition:  # -O에서 삭제되는 assert 구문 대신 명시적 예외를 사용합니다.
        raise AssertionError(message)


def rejected(function, reason):
    try:
        function()
    except ContractError as exc:
        require(str(exc) == reason, f'{exc} != {reason}')
        return {'reason': str(exc), 'exception': type(exc).__name__}
    raise AssertionError('invalid path accepted: ' + reason)


def validate_fixture(fixture):
    if not isinstance(fixture, dict) or set(fixture) != {'schema', 'geometry', 'scenarios'}:
        raise ContractError('FIXTURE_KEYS')
    if type(fixture['schema']) is not int or fixture['schema'] != 1:
        raise ContractError('FIXTURE_SCHEMA')
    if fixture['geometry'] != {'blocks': 8, 'bytes_per_block': 4}:
        raise ContractError('FIXTURE_GEOMETRY')
    scenarios = fixture['scenarios']
    if not isinstance(scenarios, list) or not 1 <= len(scenarios) <= 100:
        raise ContractError('FIXTURE_SCENARIOS')
    names = set()
    for row in scenarios:
        if not isinstance(row, dict) or set(row) != {'name', 'model', 'config', 'steps'}:
            raise ContractError('FIXTURE_ROW')
        if not isinstance(row['name'], str) or not row['name'] or row['name'] in names:
            raise ContractError('FIXTURE_NAME')
        names.add(row['name'])
        if row['model'] not in METHODS or not isinstance(row['config'], dict):
            raise ContractError('FIXTURE_MODEL')
        keys = {'vwc'} if row['model'] == 'nvme' else {'family', 'cache_supported'}
        if set(row['config']) != keys:
            raise ContractError('FIXTURE_CONFIG')
        if not isinstance(row['steps'], list) or not 1 <= len(row['steps']) <= 100:
            raise ContractError('FIXTURE_STEPS')
        for step in row['steps']:
            if not isinstance(step, list) or len(step) != 3:
                raise ContractError('FIXTURE_STEP')
            if step[0] not in METHODS[row['model']] or not isinstance(step[1], list):
                raise ContractError('FIXTURE_METHOD')


def checks(fixture, mutation):
    observations = []
    for row in fixture['scenarios']:
        factory = Nvme if row['model'] == 'nvme' else Card
        model = factory(**row['config'], mutation=mutation)  # **는 사전의 값을 이름 인자로 펼칩니다.
        steps = []
        for index, (method, arguments, expected) in enumerate(row['steps']):
            result = getattr(model, method)(*arguments)  # 허용 목록 안의 메서드와 위치 인자를 호출합니다.
            require(result == expected, f"{row['name']} step {index}: {result!r} != {expected!r}")
            steps.append({'method': method, 'actual': result})
        observations.append({'name': row['name'], 'steps': steps,
                             'persistent_media': [model.media[i].hex() for i in range(8)]})

    errors = []
    def bad(function, reason):
        errors.append(rejected(function, reason))

    nvme = Nvme()
    bad(lambda: nvme.submit_write(True, 0, ['11111111']), 'CID_RANGE')
    bad(lambda: nvme.submit_write(-1, 0, ['11111111']), 'CID_RANGE')
    bad(lambda: nvme.submit_write(65536, 0, ['11111111']), 'CID_RANGE')
    bad(lambda: nvme.submit_write(1, 8, ['11111111']), 'LBA_RANGE')
    bad(lambda: nvme.submit_write(1, 7, ['11111111', '22222222']), 'BLOCK_RANGE')
    bad(lambda: nvme.submit_write(1, 0, []), 'BLOCK_RANGE')
    bad(lambda: nvme.submit_write(1, 0, ['gggggggg']), 'BLOCK_HEX')
    bad(lambda: nvme.submit_write(1, 0, ['11 22 33']), 'BLOCK_HEX')
    bad(lambda: nvme.submit_write(1, 0, ['11111111'], 1), 'FUA_BOOL')
    nvme.submit_write(1, 0, ['11111111'])
    bad(lambda: nvme.submit_write(1, 1, ['22222222']), 'CID_IN_USE')
    bad(lambda: nvme.submit_write(2, 0, ['22222222']), 'OVERLAPPING_INFLIGHT_WRITE')
    bad(lambda: nvme.submit_flush(2), 'PRIOR_COMMAND_PENDING')
    bad(lambda: nvme.complete(2, 'SUCCESS'), 'UNKNOWN_CID')
    bad(lambda: nvme.complete(1, 'UNKNOWN'), 'STATUS_UNSUPPORTED')
    bad(lambda: nvme.complete(1, 'MEDIA_ERROR', 2), 'FAULT_PREFIX_RANGE')
    bad(lambda: nvme.complete(1, 'SUCCESS', 1), 'FAULT_ON_SUCCESS')
    require(list(nvme.pending) == [1] and nvme.read(0) == '00000000',
            'invalid NVMe completion changed pending/media')
    nvme.complete(1, 'SUCCESS')
    nvme.submit_flush(2)
    bad(lambda: nvme.submit_write(3, 1, ['22222222']), 'FLUSH_BARRIER_ACTIVE')
    nvme.complete(2, 'SUCCESS')
    nvme.submit_write(1, 1, ['22222222'])
    require(nvme.complete(1, 'SUCCESS')['cid'] == 1, 'completed CID not reusable')
    bad(lambda: nvme.complete(1, 'SUCCESS'), 'UNKNOWN_CID')
    nvme.power_loss()
    bad(lambda: nvme.submit_flush(0), 'POWER_LOST_NEW_SESSION_REQUIRED')
    full = Nvme()
    for index in range(4):
        full.submit_write(index, index, ['11111111'])
    bad(lambda: full.submit_write(4, 4, ['11111111']), 'QUEUE_FULL')
    bad(lambda: Nvme(vwc=1), 'VWC_BOOL')

    card = Card('sd')
    bad(card.enable_cache, 'CACHE_UNSUPPORTED')
    bad(lambda: card.flush(True), 'CACHE_NOT_ENABLED')
    bad(lambda: card.poll(False, True, 'TRAN'), 'NO_ACTIVE_WRITE')
    bad(card.timeout, 'NO_ACTIVE_WRITE')
    bad(lambda: Card('sata'), 'CARD_FAMILY')
    bad(lambda: Card('emmc', cache_supported=1), 'CAPABILITY_BOOL')
    bad(lambda: card.submit_write(True, 0, ['11111111']), 'REQUEST_ID_RANGE')
    card.submit_write(7, 0, ['11111111'])
    bad(lambda: card.submit_write(8, 1, ['22222222']), 'CARD_NOT_IDLE')
    bad(card.enable_cache, 'CARD_NOT_IDLE')
    bad(lambda: card.flush(True), 'CARD_NOT_IDLE')
    bad(lambda: card.poll(0, True, 'TRAN'), 'BUSY_BOOL')
    bad(lambda: card.poll(False, 1, 'TRAN'), 'READY_BOOL')
    bad(lambda: card.poll(False, True, 'IDLE'), 'STATE_UNSUPPORTED')
    bad(lambda: card.poll(False, True, 'TRAN', 'CRC?'), 'CARD_ERROR_UNSUPPORTED')
    bad(lambda: card.poll(False, True, 'TRAN', None, 1), 'FAULT_WITHOUT_ERROR')
    bad(lambda: card.timeout(2), 'FAULT_PREFIX_RANGE')
    require(card.active[0] == 7 and card.read(0) == '00000000', 'invalid card input changed state')
    card.timeout()
    bad(lambda: card.submit_write(8, 1, ['22222222']), 'CARD_NOT_IDLE')
    card.power_loss()
    bad(card.enable_cache, 'POWER_LOST_NEW_SESSION_REQUIRED')
    flush_error = Card('emmc', True)
    flush_error.enable_cache()
    bad(lambda: flush_error.flush(1), 'FLUSH_SUCCESS_BOOL')
    flush_error.flush(False)
    bad(lambda: flush_error.submit_write(0, 0, ['11111111']), 'CARD_NOT_IDLE')
    wp = Card('sd')
    wp.submit_write(11, 0, ['11111111'])
    result_wp = wp.poll(False, True, 'TRAN', 'WP_VIOLATION')
    require(result_wp == {'request_id': 11, 'result': 'FAILED_UNCERTAIN', 'durable_ack': False,
                          'error': 'WP_VIOLATION'} and wp.read(0) == '00000000', 'write-protect literal differs')
    bad(lambda: wp.submit_write(12, 1, ['22222222']), 'CARD_NOT_IDLE')

    boundary = []
    for lba in range(8):
        device = Nvme(vwc=False)
        device.submit_write(0, lba, ['76543210'])
        require(device.complete(0, 'SUCCESS')['durable_ack'], 'no-cache boundary not durable')
        device.power_loss()
        require(device.read(lba) == '76543210', 'NVMe last block failed')
        boundary.append({'kind': 'nvme_lba', 'lba': lba, 'actual_hex': device.read(lba)})
        device_card = Card('sd')
        device_card.submit_write(0, lba, ['89abcdef'])
        device_card.poll(False, True, 'TRAN')
        device_card.power_loss()
        require(device_card.read(lba) == '89abcdef', 'card last block failed')
        boundary.append({'kind': 'card_lba', 'lba': lba, 'actual_hex': device_card.read(lba)})
    for count in range(1, 9):
        data = blocks_at(0, ['01010101'] * count)
        require(list(data) == list(range(count)) and list(data.values()) == [b'\x01' * 4] * count,
                'block-count boundary differs')
        boundary.append({'kind': 'block_count', 'count': count})
    overwrite = Nvme()
    overwrite.submit_write(0, 0, ['11111111'])
    overwrite.complete(0, 'SUCCESS')
    overwrite.submit_write(1, 0, ['22222222'], fua=True)
    overwrite.complete(1, 'SUCCESS')
    overwrite.power_loss()
    require(overwrite.read(0) == '22222222', 'FUA did not replace old cached block')
    return {'scenarios': observations, 'scenario_count': len(observations),
            'literal_step_count': sum(len(row['steps']) for row in observations),
            'input_rejections': errors, 'input_rejection_count': len(errors),
            'boundaries': boundary, 'boundary_count': len(boundary),
            'extra_literals': {'write_protect': result_wp, 'fua_replaces_cached_hex': overwrite.read(0)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--fixture', type=Path, default=BASE / 'fixtures.json')
    parser.add_argument('--mutation', choices=MUTATIONS, default='none')
    args = parser.parse_args()
    if args.out.exists():  # 결과 폴더가 이미 있으면 먼저 중단하여 과거 기록을 보존합니다.
        parser.error('output directory already exists; choose a new --out')
    try:
        raw = args.fixture.read_bytes()
        fixture = json.loads(raw)
        validate_fixture(fixture)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    args.out.mkdir(parents=True, exist_ok=False)
    files = [BASE / 'models.py', BASE / 'run_cases.py', args.fixture.resolve()]
    report = {'scope': 'decoded synthetic host contract; no storage commands or hardware',
              'utc': datetime.now(timezone.utc).isoformat(), 'mutation': args.mutation,
              'environment': {'python': sys.version, 'executable': sys.executable,
                              'platform': platform.platform(), 'optimize': sys.flags.optimize},
              'argv': sys.argv, 'sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                         for path in files}}
    try:
        report['observations'] = checks(fixture, args.mutation)
        report['status'] = 'PASS'
        code = 0
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

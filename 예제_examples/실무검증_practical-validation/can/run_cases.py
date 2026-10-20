"""합성 CAN 관측의 복구 정책과 자체 응용 계약을 검사합니다. 장비에 접속하지 않습니다."""

import argparse  # 명령행 인수를 해석하는 표준 모듈입니다.
from collections import Counter  # 같은 판정의 횟수를 세는 사전형을 가져옵니다.
from datetime import datetime, timezone  # 실행 시각을 시간대와 함께 남깁니다.
import hashlib  # 소스와 입력 파일의 SHA-256을 계산합니다.
import json  # 표준 JSON 파일을 읽고 씁니다.
from pathlib import Path  # 운영체제별 경로를 객체로 다룹니다.
import platform  # Python과 운영체제 정보를 기록합니다.
import sys  # 실행 파일 경로와 인수를 기록합니다.

BASE = Path(__file__).resolve().parent  # 이 코드가 있는 폴더를 기준으로 입력을 찾습니다.
MASK32 = (1 << 32) - 1  # <<는 비트 이동이며 32비트 순환 시계의 마스크입니다.
HALF32 = 1 << 31  # 반주기 이상 차이는 미래·역행·시계 불일치로 거부합니다.


class InputError(ValueError):  # class는 형을 정의하며 잘못된 입력을 구분합니다.
    pass  # 별도 동작 없이 ValueError의 기능을 상속합니다.


def integer(value, minimum, maximum, label):  # def는 이름 있는 함수를 정의합니다.
    if type(value) is not int or not minimum <= value <= maximum:
        raise InputError(f"{label}: integer in [{minimum}, {maximum}] required")
    return value  # bool은 int의 하위 형이므로 type 비교로 제외합니다.


def require(condition, message):
    if not condition:  # not은 참·거짓을 뒤집으며 실행 모드와 무관하게 검사합니다.
        raise AssertionError(message)  # assert 문을 사용하지 않아 -O에서도 남습니다.


class RecoveryPolicy:
    """관측된 bus-off 뒤의 호스트 정책입니다. CAN error confinement 구현이 아닙니다."""

    def __init__(self, cooldown_ms, window_ms, max_requests):
        self.cooldown = integer(cooldown_ms, 1, 1000000, 'cooldown_ms')
        self.window = integer(window_ms, 1, 1000000, 'window_ms')
        self.maximum = integer(max_requests, 1, 1000, 'max_requests')
        self.phase = 'READY'  # 아직 bus-off 관측이 없는 초기 정책 상태입니다.
        self.bus_off_at = None  # None은 기준 시각이 아직 없음을 뜻합니다.
        self.request_times = []  # []는 순서를 유지하는 가변 목록입니다.
        self.last_time = -1

    def step(self, event):
        if not isinstance(event, dict):
            raise InputError('controller event must be an object')
        when = integer(event.get('time_ms'), 0, 10**12, 'time_ms')
        if when < self.last_time:
            raise InputError('controller time must not go backwards')
        kind = event.get('kind')
        allowed = {'tx_queued', 'ack_error', 'tx_complete', 'bus_off',
                   'app_send', 'tick', 'controller_active'}  # {}는 집합 표기입니다.
        if not isinstance(kind, str) or kind not in allowed:  # not in은 허용 집합에 없는지 검사합니다.
            raise InputError('unknown controller event')
        self.last_time = when
        if kind == 'bus_off':
            if self.phase == 'READY':
                self.bus_off_at = when  # 같은 bus-off 반복 알림은 기준을 미루지 않습니다.
                self.phase = 'BUS_OFF'
            action = 'WAIT_ACTIVE' if self.phase == 'WAIT_ACTIVE' else 'BLOCK_TX'
        elif kind == 'app_send':
            action = 'ALLOW_TX' if self.phase == 'READY' else 'DENY_TX'
        elif kind == 'controller_active':
            if self.phase == 'WAIT_ACTIVE':
                self.phase = 'READY'  # 요청 반환이 아니라 활성 관측으로 송신 허용을 바꿉니다.
                action = 'RESUME_TX'
            else:
                action = 'LOG_ACTIVE' if self.phase == 'READY' else 'HOLD_UNREQUESTED_ACTIVE'
        elif kind == 'tick':
            if self.phase == 'READY':
                action = 'NO_ACTION'
            elif self.phase == 'WAIT_ACTIVE':
                action = 'WAIT_ACTIVE'  # 요청 뒤 확인이 없으면 계속 차단합니다.
            elif when - self.bus_off_at < self.cooldown:
                action = 'WAIT_COOLDOWN'
            else:
                self.request_times = [t for t in self.request_times if when - t < self.window]
                if len(self.request_times) >= self.maximum:
                    action = 'HOLD_RATE_LIMIT'
                else:
                    self.request_times.append(when)  # append는 목록 끝에 요청 시각을 추가합니다.
                    self.phase = 'WAIT_ACTIVE'
                    action = 'REQUEST_RESTART'  # 실제 제어 호출 없이 결정만 돌려줍니다.
        else:
            action = {'tx_queued': 'LOG_QUEUED', 'ack_error': 'LOG_ACK_ERROR',
                      'tx_complete': 'LOG_TX_COMPLETE'}[kind]  # 사전에서 이벤트별 이름을 찾습니다.
        return {'time_ms': when, 'kind': kind, 'action': action, 'phase': self.phase}


def faulty_recovery(events):
    """의도적 오류: cooldown·횟수 제한 없이 요청 즉시 READY로 간주합니다."""
    phase, rows = 'READY', []
    for event in events:  # for는 입력 순서대로 반복합니다.
        if event['kind'] == 'bus_off':
            phase = 'BUS_OFF'
        elif event['kind'] == 'tick' and phase == 'BUS_OFF':
            phase = 'READY'  # 잘못된 상태 변경을 의도적으로 남깁니다.
            rows.append({'time_ms': event['time_ms'], 'action': 'REQUEST_RESTART'})
        elif event['kind'] == 'app_send':
            rows.append({'time_ms': event['time_ms'],
                         'action': 'ALLOW_TX' if phase == 'READY' else 'DENY_TX'})
    return rows


def age32(now, then):
    age = (now - then) & MASK32  # &는 비트 AND이며 32비트 순환 차이를 구합니다.
    return None if age >= HALF32 else age


def validate_frame(frame, state):
    """자체 8바이트 형식이며 상태는 모든 검사를 통과한 뒤에만 변경합니다."""
    if not isinstance(frame, dict):
        raise InputError('application frame must be an object')
    can_id = integer(frame.get('can_id'), 0, (1 << 29) - 1, 'can_id')
    for flag in ('is_extended', 'is_remote', 'is_fd', 'is_error'):
        if type(frame.get(flag)) is not bool:
            raise InputError(f'{flag}: boolean required')
    rx = integer(frame.get('rx_ms'), 0, MASK32, 'rx_ms')
    now = integer(frame.get('now_ms'), 0, MASK32, 'now_ms')
    session = frame.get('session')
    if not isinstance(session, str) or not session:
        raise InputError('nonempty session required')
    text = frame.get('data_hex')
    if not isinstance(text, str) or len(text) % 2 or any(c not in '0123456789abcdefABCDEF' for c in text):
        raise InputError('data_hex must contain complete hexadecimal bytes')
    data = bytes.fromhex(text)  # 16진수 문자열을 실제 바이트열로 바꿉니다.
    row = {'name': frame.get('name'), 'accepted': False, 'reason': None}

    def reject(reason):  # 안쪽 함수는 공통 거부 결과를 돌려줍니다.
        return dict(row, reason=reason)  # dict는 기존 사전에 새 항목을 합쳐 복사합니다.

    if frame['is_extended']:
        return reject('ID_FORMAT')
    if can_id != 0x321:  # 0x는 16진수 정수 표기입니다.
        return reject('ID')
    if frame['is_remote'] or frame['is_fd'] or frame['is_error']:
        return reject('FRAME_TYPE')
    if len(data) != 8:
        return reject('LENGTH')
    if data[0] != 1:  # []는 위치 접근이며 첫 바이트는 자체 형식 버전입니다.
        return reject('VERSION')
    sequence = data[1]
    millivolts = int.from_bytes(data[2:4], 'little')  # [2:4]는 끝 위치를 제외한 슬라이스입니다.
    sample_ms = int.from_bytes(data[4:8], 'little')
    if not 0 <= millivolts <= 5000:
        return reject('VALUE_RANGE')
    queue_age = age32(now, rx)
    sample_age = age32(now, sample_ms)
    if queue_age is None:
        return reject('CAPTURE_CLOCK')
    if sample_age is None:
        return reject('SAMPLE_CLOCK')
    if sample_age < queue_age:  # 같은 시계에서는 생성 시각이 수신 시각 뒤일 수 없습니다.
        return reject('SAMPLE_AFTER_CAPTURE')
    if sample_age > 100:  # 100 ms는 이 예제의 응용 정책이며 CAN 표준 상한이 아닙니다.
        return reject('STALE')
    previous = state.get(session)  # get은 첫 수신처럼 키가 없는 경우 None을 돌려줍니다.
    if previous is not None:
        delta = (sequence - previous) & 0xFF  # 8비트 순번의 순환 차이를 계산합니다.
        if delta == 0:
            return reject('DUPLICATE')
        if delta != 1:
            return reject('SEQUENCE')
    state[session] = sequence  # 전부 통과한 프레임만 마지막 채택 순번을 갱신합니다.
    return dict(row, accepted=True, reason='ACCEPT', millivolts=millivolts,
                sequence=sequence, sample_age_ms=sample_age, queue_age_ms=queue_age)


def faulty_advance_before_age(frame, state):
    """의도적 오류: 오래된 입력인지 보기 전에 순번을 채택합니다."""
    data = bytes.fromhex(frame['data_hex'])
    sequence, key = data[1], frame['session']
    previous = state.get(key)
    if previous == sequence:
        return 'DUPLICATE'
    state[key] = sequence  # 이 갱신 뒤 STALE을 반환해도 상태를 되돌리지 않습니다.
    sample = int.from_bytes(data[4:8], 'little')
    age = age32(frame['now_ms'], sample)
    return 'STALE' if age is None or age > 100 else 'ACCEPT'


def expect_input_error(label, function):
    try:  # try는 예외가 생길 수 있는 검사를 실행합니다.
        function()
    except InputError as exc:  # except는 예상한 입력 오류만 처리합니다.
        return {'case': label, 'exception': type(exc).__name__, 'message': str(exc)}
    raise AssertionError(f'{label}: malformed input unexpectedly accepted')


def run_checks(controller, application):
    policy = RecoveryPolicy(controller['cooldown_ms'], controller['window_ms'],
                            controller['max_requests_per_window'])
    controller_rows = []
    for event in controller['events']:
        row = policy.step(event)
        require(row['action'] == event['expected'], f'controller mismatch: {row}')
        controller_rows.append(row)
    restart_times = [r['time_ms'] for r in controller_rows if r['action'] == 'REQUEST_RESTART']
    require(restart_times == [140, 300, 1140], 'independent restart timestamps differ')
    faulty_rows = faulty_recovery(controller['events'])
    require(any(r == {'time_ms': 50, 'action': 'REQUEST_RESTART'} for r in faulty_rows),
            'faulty immediate restart was not exposed')
    require(any(r == {'time_ms': 141, 'action': 'ALLOW_TX'} for r in faulty_rows),
            'faulty unconfirmed transmission was not exposed')

    state, frame_rows = {}, []  # {}는 여기서 키/값 사전이며 세션별 채택 순번을 저장합니다.
    for frame in application['frames']:
        before = dict(state)
        row = validate_frame(frame, state)
        require(row['reason'] == frame['expected'], f'application mismatch: {row}')
        if row['accepted']:
            require(row['millivolts'] == frame['expected_mv'], 'independent millivolt value differs')
        else:
            require(state == before, 'rejected frame changed accepted sequence')
        frame_rows.append(row)
    first = bytes.fromhex(application['frames'][0]['data_hex'])
    wrong_endian_mv = int.from_bytes(first[2:4], 'big')
    require(wrong_endian_mv == 13330 and frame_rows[0]['millivolts'] == 4660,
            'known 34 12 byte pattern did not separate endian choices')
    lookup = {f['name']: f for f in application['frames']}
    premature_state = {'main': 254}
    premature = [faulty_advance_before_age(lookup[name], premature_state)
                 for name in ('stale_sample', 'next_sequence_255')]
    require(premature == ['STALE', 'DUPLICATE'], 'premature-state fault was not exposed')

    malformed = []
    bad_events = [('negative_time', {'time_ms': -1, 'kind': 'tick'}),
                  ('unknown_event', {'time_ms': 0, 'kind': 'invented'}),
                  ('array_event_kind', {'time_ms': 0, 'kind': []}),
                  ('boolean_time', {'time_ms': True, 'kind': 'tick'})]
    for label, event in bad_events:
        malformed.append(expect_input_error(label, lambda e=event: RecoveryPolicy(100, 1000, 2).step(e)))
    reverse = RecoveryPolicy(100, 1000, 2)
    reverse.step({'time_ms': 10, 'kind': 'tick'})
    malformed.append(expect_input_error('reverse_time', lambda: reverse.step({'time_ms': 9, 'kind': 'tick'})))
    for label, change in [('bad_hex', {'data_hex': 'GG'}), ('odd_hex', {'data_hex': '1'}),
                          ('integer_flag', {'is_fd': 0}), ('oversize_id', {'can_id': 1 << 29}),
                          ('negative_clock', {'rx_ms': -1}), ('empty_session', {'session': ''})]:
        candidate = dict(application['frames'][0], **change)
        malformed.append(expect_input_error(label, lambda f=candidate: validate_frame(f, {})))
    malformed.append(expect_input_error('zero_cooldown', lambda: RecoveryPolicy(0, 1000, 2)))

    event_counts = Counter(row['kind'] for row in controller_rows)
    return {'status': 'PASS', 'scope': 'Deterministic software fixtures; no hardware or SocketCAN execution',
            'controller': {'checked_events': len(controller_rows), 'rows': controller_rows,
                           'restart_request_ms': restart_times, 'faulty_rows': faulty_rows,
                           'ack_error_observations': event_counts['ack_error'],
                           'link_tx_complete_observations': event_counts['tx_complete'],
                           'application_completions_confirmed': 0,
                           'faulty_completions_from_queueing': event_counts['tx_queued']},
            'application': {'checked_records': len(frame_rows), 'rows': frame_rows,
                            'reason_counts': dict(Counter(r['reason'] for r in frame_rows)),
                            'wrong_endian_mv': wrong_endian_mv,
                            'faulty_state_order_results': premature,
                            'unchecked_path_would_accept_records': len(frame_rows)},
            'malformed_inputs': malformed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='new output folder; existing paths are rejected')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    try:
        output.mkdir(parents=True, exist_ok=False)  # 기존 결과를 덮어쓰지 않습니다.
    except FileExistsError:
        parser.error(f'output already exists: {output}')
    inputs = ['controller_trace.json', 'application_frames.json']
    manifest = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
                for name in ['run_cases.py', *inputs]}  # *는 목록 원소를 펼칩니다.
    environment = {'python': sys.version, 'executable': sys.executable,
                   'platform': platform.platform(), 'machine': platform.machine(),
                   'utc': datetime.now(timezone.utc).isoformat(),
                   'argv': sys.argv, 'source_and_input_sha256': manifest}
    try:
        controller, application = [json.loads((BASE / name).read_text(encoding='utf-8')) for name in inputs]
        result = run_checks(controller, application)
    except Exception as exc:
        result = {'status': 'ERROR', 'exception': type(exc).__name__, 'message': str(exc)}
        exit_code = 1
    else:
        exit_code = 0
    result['environment'] = environment
    (output / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'output': str(output)}, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':  # 직접 실행할 때만 main을 호출합니다.
    raise SystemExit(main())  # 반환값을 운영체제 종료 코드로 전달합니다.

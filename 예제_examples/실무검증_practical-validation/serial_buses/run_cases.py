"""SPI 읽기 경계와 I2C 묶음 읽기를 합성합니다. 실제 장치·드라이버를 실행하지 않습니다."""

import argparse  # 명령행 인수 해석을 위한 표준 모듈입니다.
from datetime import datetime, timezone  # 시간대가 있는 실행 시각을 기록합니다.
import hashlib  # 소스와 입력의 SHA-256을 계산합니다.
import json  # JSON을 읽고 기록합니다.
from pathlib import Path  # 파일 경로를 객체로 다룹니다.
import platform  # 실행 환경의 정보를 얻습니다.
import sys  # Python 버전·실행 경로·인수를 기록합니다.

BASE = Path(__file__).resolve().parent  # 실행 위치와 별개로 입력 폴더를 찾습니다.


class InputError(ValueError):  # class는 잘못된 입력을 구분하는 예외 형을 만듭니다.
    pass  # ValueError의 기능을 그대로 사용합니다.


def check(condition, message):
    if not condition:  # not은 조건을 뒤집으며 -O에서도 검사를 유지합니다.
        raise AssertionError(message)


def uint(value, maximum, label):
    if type(value) is not int or not 0 <= value <= maximum:
        raise InputError(f'{label}: integer in [0,{maximum}] required')
    return value  # bool을 숫자로 오인하지 않도록 정확한 형을 비교합니다.


def decode_hex(text):
    if not isinstance(text, str) or len(text) % 2 or any(c not in '0123456789abcdefABCDEF' for c in text):
        raise InputError('complete hexadecimal bytes required')
    return bytes.fromhex(text)  # 16진수 문자열을 바이트열로 바꿉니다.


def memory_from_json(raw, maximum):
    if not isinstance(raw, dict):
        raise InputError('memory must be an object')
    memory = {}
    for address, text in raw.items():
        try:
            number = int(address)  # 문자열 주소를 정수로 변환합니다.
        except (ValueError, TypeError) as exc:
            raise InputError('memory address must be decimal integer text') from exc
        uint(number, maximum, 'memory address')
        data = decode_hex(text)
        if len(data) != 1:
            raise InputError('one byte required at each memory address')
        memory[number] = data[0]
    return memory


def sample_edge(cpol, cpha):
    uint(cpol, 1, 'CPOL')
    uint(cpha, 1, 'CPHA')
    return 'rising' if cpol == cpha else 'falling'


def spi_wave(tx, memory, break_after_bytes=None, dummy_clocks=8):
    """Mode0의 이상적 논리 파형입니다. 출력 지연 5ns·clock 주기1000ns는 자체 가정입니다."""
    if not isinstance(tx, bytes) or not 1 <= len(tx) <= 64:
        raise InputError('SPI requires 1..64 bytes')
    if break_after_bytes is not None:
        uint(break_after_bytes, len(tx) - 1, 'CS break')
        if break_after_bytes == 0:
            raise InputError('CS break must follow a complete byte')
    uint(dummy_clocks, 32, 'dummy clocks')
    bits = [(byte >> shift) & 1 for byte in tx for shift in range(7, -1, -1)]
    prefix, local, address, opcode = [], 0, None, None
    samples, waveform, intervals = [], [{'time_ns': 0, 'event': 'CS', 'level': 0}], 1

    def output_for(position):
        if opcode != 0x0B or address is None or position < 32 + dummy_clocks:
            return None  # None은 이 모델에서 유효 데이터가 아닌 high-Z/don't-care 구간입니다.
        offset = position - 32 - dummy_clocks
        value = memory.get(address + offset // 8, 0xFF)
        return (value >> (7 - offset % 8)) & 1

    for index, mosi in enumerate(bits):
        if break_after_bytes is not None and index == break_after_bytes * 8:
            waveform += [{'time_ns': index * 1000 + 10, 'event': 'CS', 'level': 1},
                         {'time_ns': index * 1000 + 100, 'event': 'CS', 'level': 0}]
            prefix, local, address, opcode = [], 0, None, None
            intervals += 1
        waveform.append({'time_ns': index * 1000 + 100, 'event': 'mosi_update', 'mosi': mosi})
        stable = output_for(local)
        rising = index * 1000 + 500
        waveform.append({'time_ns': rising, 'event': 'rising', 'mosi': mosi,
                         'miso': 1 if stable is None else stable, 'valid': stable is not None})
        samples.append(1 if stable is None else stable)  # 유효하지 않은 입력의 판독1은 자체 pull-up 가정입니다.
        if local < 32:
            prefix.append(mosi)
            if local == 31:
                opcode = sum(prefix[i] << (7 - i) for i in range(8))
                address = sum(prefix[i] << (31 - i) for i in range(8, 32))
        local += 1
        following = output_for(local)
        falling = (index + 1) * 1000
        waveform += [{'time_ns': falling, 'event': 'falling'},
                     {'time_ns': falling + 5, 'event': 'miso_update',
                      'miso': 1 if following is None else following}]
    waveform.append({'time_ns': len(bits) * 1000 + 100, 'event': 'CS', 'level': 1})
    rx = bytes(sum(samples[start + i] << (7 - i) for i in range(8))
               for start in range(0, len(samples), 8))
    # 잘못된 fall+10ns 표본은 가정한 fall+5ns 출력 변화 뒤이므로 다음 비트를 읽습니다.
    late = [event['miso'] for event in waveform if event['event'] == 'miso_update']
    late_rx = bytes(sum(late[start + i] << (7 - i) for i in range(8))
                    for start in range(0, len(late), 8))
    return {'rx_hex': rx.hex(), 'late_falling_rx_hex': late_rx.hex(), 'clocks': len(bits),
            'cs_intervals': intervals, 'waveform': waveform,
            'valid_data_samples': sum(e.get('valid', False) for e in waveform)}


def open_drain(controller_release, target_release, stuck_low=False):
    for value in (controller_release, target_release, stuck_low):
        if type(value) is not bool:
            raise InputError('open-drain states must be boolean')
    return int(controller_release and target_release and not stuck_low)


def i2c_read(memory, address7=0x50, pointer=0x12, combined=True,
             interloper_pointer=None, nack_at=None, final_ack=False,
             sda_stuck=False, scl_stuck=False):
    """24LC256의 주소 지정·읽기 일부만 합성하며 EEPROM 쓰기/전기적 타이밍은 구현하지 않습니다."""
    uint(address7, 0x7F, 'I2C seven-bit address')
    uint(pointer, 0x7FFF, 'I2C pointer')
    allowed = {None, 'address_write', 'pointer_high', 'pointer_low', 'address_read'}
    if not isinstance(nack_at, (str, type(None))) or nack_at not in allowed:
        raise InputError('unknown NACK phase')
    if interloper_pointer is not None:
        uint(interloper_pointer, 0x7FFE, 'interloper pointer')
    for value in (combined, final_ack, sda_stuck, scl_stuck):
        if type(value) is not bool:
            raise InputError('I2C option must be boolean')
    trace, clocks, data = [], 0, []
    if not open_drain(True, True, scl_stuck):
        return {'status': 'SCL_STUCK', 'trace': ['SCL:LOW_BEFORE_START'], 'clocks': 0, 'data_hex': ''}
    if not open_drain(True, True, sda_stuck):
        return {'status': 'SDA_STUCK', 'trace': ['SDA:LOW_BEFORE_START'], 'clocks': 0, 'data_hex': ''}

    def send(actor, value, stage=None):
        nonlocal clocks  # nonlocal은 바깥 함수의 clock 변수를 갱신하게 합니다.
        trace.append(f'{actor}:TX:{value:02X}')
        clocks += 9  # 바이트8비트와 ACK/NACK1비트를 함께 셉니다.
        acknowledged = stage != nack_at or stage is None
        trace.append('TARGET:ACK' if acknowledged else 'TARGET:NACK')
        return acknowledged

    trace.append('C1:START')
    for value, stage in [((address7 << 1), 'address_write'),
                         (pointer >> 8, 'pointer_high'), (pointer & 0xFF, 'pointer_low')]:
        if not send('C1', value, stage):
            trace.append('C1:STOP')
            return {'status': 'TARGET_NACK:' + stage, 'trace': trace, 'clocks': clocks, 'data_hex': ''}
    current = pointer
    if combined:
        trace.append('C1:RESTART')
    else:
        trace.append('C1:STOP')  # bus를 놓은 경계에서만 다른 요청을 끼워 넣습니다.
        if interloper_pointer is not None:
            trace.append('C2:START')
            send('C2', address7 << 1)
            send('C2', interloper_pointer >> 8)
            send('C2', interloper_pointer & 0xFF)
            trace.append('C2:STOP')
            current = interloper_pointer
        trace.append('C1:START')
    if not send('C1', (address7 << 1) | 1, 'address_read'):
        trace.append('C1:STOP')
        return {'status': 'TARGET_NACK:address_read', 'trace': trace, 'clocks': clocks, 'data_hex': ''}
    for index in range(2):
        value = memory.get((current + index) & 0x7FFF, 0xFF)  # 이 EEPROM의 순차 주소 순환을 적용합니다.
        data.append(value)
        trace.append(f'TARGET:TX:{value:02X}')
        trace.append('C1:ACK' if index == 0 or final_ack else 'C1:NACK')
        clocks += 9
    trace.append('C1:STOP')
    return {'status': 'READ', 'trace': trace, 'clocks': clocks, 'data_hex': bytes(data).hex()}


def faulty_any_nack_is_failure(trace):
    return any(token.endswith(':NACK') for token in trace)  # 잘못된 경로: NACK의 주체를 무시합니다.


def faulty_cache_fallback(result, cached_hex):
    return result['data_hex'] if result['status'] == 'READ' else cached_hex


def expect_input_error(label, function):
    try:
        function()
    except InputError as exc:
        return {'case': label, 'exception': type(exc).__name__, 'message': str(exc)}
    raise AssertionError(label + ': input unexpectedly accepted')


def run(inputs, mutation):
    spi, i2c = inputs['spi'], inputs['i2c']
    flash = memory_from_json(spi['memory_hex'], 0xFFFFFF)
    eeprom = memory_from_json(i2c['memory_hex'], 0x7FFF)
    normal = spi_wave(decode_hex(spi['normal_tx_hex']), flash,
                      dummy_clocks=0 if mutation == 'spi-no-dummy' else 8)
    check(normal['rx_hex'] == spi['expected_normal_rx_hex'], 'SPI literal receive oracle failed')
    check(normal['clocks'] == spi['expected_clocks'] == 56, 'SPI clocks differ')
    check(normal['valid_data_samples'] == 16 and normal['cs_intervals'] == 1, 'SPI phase/CS differ')
    times = [event['time_ns'] for event in normal['waveform']]
    check(times == sorted(times), 'SPI waveform event time went backwards')
    edges = [sample_edge(mode >> 1, mode & 1) for mode in range(4)]
    check(edges == spi['expected_sample_edges'], 'CPOL/CPHA literal edges differ')
    payload = normal['rx_hex'][10:14]  # 5바이트의 명령·주소·dummy 수신을 건너뜁니다.
    check(payload == spi['expected_payload_hex'], 'SPI payload differs')
    bad_offset = normal['rx_hex'][8:12]
    check(bad_offset == spi['expected_skipped_dummy_hex'] and bad_offset != payload, 'dummy offset fault missing')
    short = spi_wave(decode_hex(spi['short_tx_hex']), flash)
    check(short['rx_hex'][-4:] == 'ffa5' and short['valid_data_samples'] == 8, 'missing clocks fault missing')
    split = spi_wave(decode_hex(spi['normal_tx_hex']), flash, break_after_bytes=4)
    check(split['rx_hex'][-4:] == spi['expected_split_payload_hex'] and split['valid_data_samples'] == 0,
          'CS split fault missing')
    late_payload = normal['late_falling_rx_hex'][10:14]
    check(late_payload == spi['expected_late_falling_hex'] and late_payload != payload, 'late-edge fault missing')

    normal_i2c = i2c_read(eeprom, i2c['address7'], i2c['pointer'],
                          final_ack=mutation == 'i2c-final-ack')
    check(normal_i2c['trace'] == i2c['expected_trace'], 'I2C literal trace oracle failed')
    check(normal_i2c['data_hex'] == i2c['expected_payload_hex'], 'I2C data differs')
    check(normal_i2c['clocks'] == i2c['expected_clocks_combined'] == 54, 'I2C clocks differ')
    separated = i2c_read(eeprom, combined=False, interloper_pointer=i2c['interloper_pointer'])
    check(separated['data_hex'] == i2c['expected_split_payload_hex'], 'I2C interleaving fault missing')
    check(separated['clocks'] == i2c['expected_clocks_split_with_interloper'] == 81, 'I2C interloper clocks differ')
    no_interleaving = i2c_read(eeprom, combined=False)
    check(no_interleaving['data_hex'] == 'a55a', 'STOP alone must not reset this model pointer')
    nacks = {}
    for phase, expected_clocks in i2c['expected_nack_clocks'].items():
        observed = i2c_read(eeprom, nack_at=phase)
        check(observed['status'] == 'TARGET_NACK:' + phase and observed['data_hex'] == '', 'NACK used as data')
        check(observed['clocks'] == expected_clocks, 'NACK abort clock boundary differs')
        nacks[phase] = observed
    last_ack = i2c_read(eeprom, final_ack=True)
    check(last_ack['data_hex'] == 'a55a' and last_ack['trace'][-2] == 'C1:ACK', 'last-ACK control differs')
    check(last_ack['trace'] != i2c['expected_trace'], 'payload-only check would miss final ACK')
    faulty_nack_error = faulty_any_nack_is_failure(normal_i2c['trace'])
    check(faulty_nack_error, 'NACK-role fault missing')
    stale_fallback = faulty_cache_fallback(nacks['address_read'], 'a55a')
    check(stale_fallback == 'a55a' and nacks['address_read']['data_hex'] == '', 'cached-data fault missing')
    wrap = i2c_read(eeprom, pointer=0x7FFF)
    check(wrap['data_hex'] == i2c['expected_wrap_payload_hex'], 'EEPROM pointer wrap differs')
    levels = [open_drain(c, t) for c, t in [(True, True), (True, False), (False, True), (False, False)]]
    check(levels == i2c['expected_open_drain_levels'], 'open-drain truth table differs')
    stuck = {line: i2c_read(eeprom, **{line + '_stuck': True}) for line in ('sda', 'scl')}
    check(stuck['sda']['status'] == 'SDA_STUCK' and stuck['scl']['status'] == 'SCL_STUCK', 'stuck line missing')

    exceptions = []
    for label, function in [
        ('odd_hex', lambda: decode_hex('0')),
        ('non_hex', lambda: decode_hex('GG')),
        ('empty_spi', lambda: spi_wave(b'', flash)),
        ('bad_mode', lambda: sample_edge(0, 2)),
        ('zero_cs_break', lambda: spi_wave(b'\x0b\x00', flash, break_after_bytes=0)),
        ('eight_bit_address', lambda: i2c_read(eeprom, address7=0xA0)),
        ('negative_pointer', lambda: i2c_read(eeprom, pointer=-1)),
        ('bad_nack_phase', lambda: i2c_read(eeprom, nack_at='invented')),
        ('numeric_open_drain', lambda: open_drain(1, True)),
    ]:
        exceptions.append(expect_input_error(label, function))
    return {'status': 'PASS', 'scope': 'Synthetic logical models only; no hardware or kernel API calls',
            'spi': {'normal': normal, 'payload_hex': payload, 'wrong_offset_hex': bad_offset,
                    'missing_dummy_clocks': short, 'split_cs': split, 'late_falling_payload_hex': late_payload,
                    'mode_sample_edges': edges},
            'i2c': {'normal': normal_i2c, 'split_with_interloper': separated,
                    'split_without_interloper': no_interleaving, 'target_nacks': nacks,
                    'wrong_final_ack': last_ack, 'open_drain_levels': levels, 'stuck_lines': stuck,
                    'pointer_wrap': wrap, 'faulty_final_nack_is_error': faulty_nack_error,
                    'faulty_cached_data_after_target_nack_hex': stale_fallback},
            'input_exceptions': exceptions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mutation', choices=['none', 'spi-no-dummy', 'i2c-final-ack'], default='none')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    try:
        output.mkdir(parents=True, exist_ok=False)  # 기존 결과를 덮어쓰지 않습니다.
    except FileExistsError:
        parser.error(f'output already exists: {output}')
    hashes = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
              for name in ('run_cases.py', 'bus_inputs.json')}
    try:
        result = run(json.loads((BASE / 'bus_inputs.json').read_text(encoding='utf-8')), args.mutation)
    except Exception as exc:
        result = {'status': 'ERROR', 'exception': type(exc).__name__, 'message': str(exc)}
        exit_code = 1
    else:
        exit_code = 0
    result['environment'] = {'python': sys.version, 'executable': sys.executable,
                             'platform': platform.platform(), 'machine': platform.machine(),
                             'utc': datetime.now(timezone.utc).isoformat(), 'argv': sys.argv,
                             'source_and_input_sha256': hashes, 'mutation': args.mutation}
    (output / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'output': str(output)}, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':  # 직접 실행할 때만 명령행 진입 함수를 호출합니다.
    raise SystemExit(main())

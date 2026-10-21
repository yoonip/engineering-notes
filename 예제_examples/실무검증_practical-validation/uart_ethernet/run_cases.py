"""UART 호스트 모델·합성 Ethernet 캡처·실제 localhost UDP 경계를 검사합니다."""

import argparse  # 명령행 인수를 해석하는 표준 모듈입니다.
from datetime import datetime, timezone
import hashlib  # 파일 지문인 SHA-256을 기록합니다.
import json  # JSON 입력과 결과를 다룹니다.
from pathlib import Path
import platform
import socket  # 실제 loopback UDP 소켓에만 사용합니다.
import sys

from models import InputError, PacketError, StreamParser, internet_checksum, parse_udp_capture

BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:  # 명시적인 예외이므로 Python -O에서도 검사가 남습니다.
        raise AssertionError(message)


def from_hex(text):
    if not isinstance(text, str) or len(text) % 2 or any(c not in '0123456789abcdefABCDEF' for c in text):
        raise InputError('complete hex bytes required')
    return bytes.fromhex(text)


def feed_chunks(chunks, ignore_checksum=False):
    parser, frames = StreamParser(ignore_checksum), []
    for chunk in chunks:
        frames.extend(parser.feed(chunk))  # 같은 parser의 상태를 다음 조각에 이어 사용합니다.
    return frames, parser


def faulty_each_read_is_one_frame(chunks):
    frames = []
    for chunk in chunks:
        found = StreamParser().feed(chunk)  # 잘못된 경로는 수신 호출마다 상태를 버립니다.
        if found:
            frames.append(found[0])  # 한 호출에서 여러 프레임이 나와도 첫것만 채택합니다.
    return frames


def packet_outcome(frame, **options):
    try:
        return {'reason': 'ACCEPT', 'data': parse_udp_capture(frame, **options)}
    except PacketError as exc:
        return {'reason': str(exc)}  # 지원하지 않는 기능과 잘못된 길이를 각각 남깁니다.


def loopback_udp(payloads):
    rows = []
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as receiver:
        receiver.bind(('127.0.0.1', 0))  # 포트0은 운영체제에 빈 로컬 포트를 요청합니다.
        receiver.settimeout(2.0)  # 수신이 오지 않으면 성공으로 대신하지 않고 실패합니다.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
            for text in payloads:
                data = from_hex(text)
                sent = sender.sendto(data, receiver.getsockname())
                observed, peer = receiver.recvfrom(65535)
                require(sent == len(data) and observed == data, 'localhost UDP payload boundary mismatch')
                require(peer[0] == '127.0.0.1', 'unexpected non-loopback peer')
                rows.append({'sent_bytes': sent, 'received_bytes': len(observed),
                             'received_hex': observed.hex(), 'peer': list(peer)})
            endpoint = list(receiver.getsockname())
    return {'executed': True, 'transport': 'IPv4 UDP localhost', 'receiver': endpoint,
            'datagrams': rows, 'raw_ethernet_fixture_transmitted': False}


def checks(fixture, mutation):
    uart = fixture['uart']
    one, two, empty = [from_hex(uart[name]) for name in ('frame_one_hex', 'frame_two_hex', 'empty_frame_hex')]
    stream = one + two + empty
    partitions = [[stream], [bytes([byte]) for byte in stream]]
    partitions += [[stream[:cut], stream[cut:]] for cut in range(1, len(stream))]
    peaks = []
    for chunks in partitions:
        actual, parser = feed_chunks(chunks)
        require(actual == uart['expected_frames'], 'UART chunk-independent literal frames differ')
        require(not parser.buffer, 'UART completed stream retained input')
        peaks.append(parser.peak)
    bad_partial = faulty_each_read_is_one_frame([one[:2], one[2:]])
    bad_merged = faulty_each_read_is_one_frame([stream])
    require(bad_partial == [] and bad_merged == uart['expected_frames'][:1], 'UART per-read fault missing')
    bad_checksum = from_hex(uart['bad_checksum_hex']) + two
    recovered, corrupt = feed_chunks([bad_checksum], mutation == 'uart-ignore-checksum')
    require(recovered == [uart['expected_frames'][1]] and corrupt.checksum_errors == 1,
            'UART checksum rejection/recovery literal failed')
    recovered_length, oversize = feed_chunks([from_hex(uart['bad_length_prefix_hex']) + one])
    require(recovered_length == [uart['expected_frames'][0]] and oversize.length_errors == 1,
            'UART oversized length recovery failed')
    timeout = StreamParser()
    pending = timeout.feed(from_hex(uart['partial_prefix_hex']) + one)
    require(pending == [] and len(timeout.buffer) == 10, 'UART partial candidate did not wait')
    after_expiry = timeout.expire_partial()
    require(after_expiry == [uart['expected_frames'][0]] and timeout.expirations == 1,
            'UART explicit partial expiry did not recover')
    maximum = StreamParser()
    max_frame = from_hex('a55a080400000000000000000c')
    long_noise = maximum.feed(b'x' * 100000 + max_frame)
    require(long_noise == [{'sequence': 4, 'payload_hex': '00' * 8}] and maximum.peak == 13,
            'UART bounded staging buffer differs')
    collision, _ = feed_chunks([from_hex(uart['collision_frame_hex'])])
    require(collision == [{'sequence': 1, 'payload_hex': uart['expected_collision_payload_hex']}],
            'UART additive-checksum collision control differs')

    packets = []
    for entry in fixture['ethernet']['cases']:
        outcome = packet_outcome(from_hex(entry['capture_hex']),
                                 ignore_udp_checksum=mutation == 'udp-ignore-checksum')
        require(outcome['reason'] == entry['expected'], f"Ethernet/UDP literal mismatch: {entry['name']} {outcome}")
        if entry['expected'] == 'ACCEPT':
            require(outcome['data']['payload_hex'] == entry['payload_hex'], 'UDP literal payload differs')
            if mutation != 'udp-ignore-checksum':
                require(outcome['data']['udp_checksum'] == entry['checksum'], 'UDP checksum status differs')
        packets.append(dict(name=entry['name'], **outcome))
    base = from_hex(fixture['ethernet']['cases'][0]['capture_hex'])
    boundary_checks = []
    for length in range(len(base) + 1):
        outcome = packet_outcome(base[:length])
        require((outcome['reason'] == 'ACCEPT') == (length >= 46), 'capture boundary acceptance differs')
        boundary_checks.append({'captured_bytes': length, 'reason': outcome['reason']})
    accepted = packets[0]['data']
    expected = fixture['ethernet']
    require([accepted['source_port'], accepted['destination_port']] == expected['expected_ports'], 'network byte order differs')
    require(int.from_bytes(base[34:36], 'little') == 13330, 'little-endian fault control differs')
    require(accepted['ip_total_length'] == 32 and accepted['udp_length'] == 12 and
            accepted['ethernet_padding_bytes'] == 14, 'layer/padding lengths differ')
    faulty_payload = base[42:]
    require(faulty_payload.hex() == '41424344' + '00' * 14 and len(faulty_payload) == 18,
            'Ethernet padding-as-payload fault control differs')
    zero = from_hex(next(case['capture_hex'] for case in expected['cases'] if case['name'] == 'checksum_omitted_ipv4'))
    require(packet_outcome(zero, allow_zero_udp=False)['reason'] == 'UDP_CHECKSUM_REQUIRED', 'strict checksum policy failed')
    for vector in fixture['checksum_vectors']:
        require(internet_checksum(from_hex(vector['hex'])) == vector['expected'], 'independent checksum literal failed')
    input_errors = []
    for label, function in [('uart_text', lambda: StreamParser().feed('abc')),
                            ('packet_text', lambda: parse_udp_capture('abc')),
                            ('checksum_text', lambda: internet_checksum('abc')),
                            ('odd_hex', lambda: from_hex('a')),
                            ('bad_hex', lambda: from_hex('GG'))]:
        try:
            function()
        except InputError as exc:
            input_errors.append({'case': label, 'exception': type(exc).__name__, 'message': str(exc)})
        else:
            raise AssertionError(label + ': invalid input accepted')
    actual_socket = loopback_udp(fixture['loopback']['payloads_hex'])
    return {'status': 'PASS', 'uart': {'partition_patterns': len(partitions), 'expected_frames': uart['expected_frames'],
             'normal_max_buffer': max(peaks), 'faulty_partial_frames': bad_partial, 'faulty_merged_frames': bad_merged,
             'checksum_recovered': recovered, 'length_recovered': recovered_length,
             'partial_expiry_recovered': after_expiry, 'noise_bytes': 100000, 'maximum_buffer': maximum.peak,
             'checksum_collision_accepted': collision},
             'ethernet': {'cases': packets, 'capture_boundary_checks': boundary_checks,
                          'faulty_payload_including_padding_hex': faulty_payload.hex(),
                          'little_endian_source_port_control': int.from_bytes(base[34:36], 'little')},
             'input_errors': input_errors, 'localhost_udp': actual_socket}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mutation', choices=['none', 'uart-ignore-checksum', 'udp-ignore-checksum'], default='none')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error(f'output already exists: {output}')
    report = {'scope': 'UART byte model and synthetic capture parser; separate real localhost UDP payload test',
              'environment': {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
                 'machine': platform.machine(), 'utc': datetime.now(timezone.utc).isoformat(), 'argv': sys.argv,
                 'source_and_input_sha256': {name: hashlib.sha256((BASE/name).read_bytes()).hexdigest()
                    for name in ('models.py', 'run_cases.py', 'fixtures.json')}, 'mutation': args.mutation}}
    try:
        report.update(checks(json.loads((BASE/'fixtures.json').read_text(encoding='utf-8')), args.mutation))
    except Exception as exc:
        report.update(status='ERROR', exception=type(exc).__name__, message=str(exc))
    (output/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'], 'output':str(output)},ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

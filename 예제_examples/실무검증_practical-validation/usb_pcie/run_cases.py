"""USB·PCIe 합성 전송의 literal·소유권·입력 오류·변이 검사를 실행합니다."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

from models import (BulkRecords, CompletionTracker, ContractError, IdempotentDevice, InputError,
                    UsbEndpoint, bulk_result, octets, retry_after_stall)

BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:  # 일반 assert와 달리 -O에서도 이 예외 검사는 남습니다.
        raise AssertionError(message)


def rejected(function, reason, kind=ContractError):
    try:
        function()
    except kind as exc:
        require(str(exc) == reason, f'wrong rejection: {exc}, expected {reason}')
        return {'exception': type(exc).__name__, 'reason': str(exc)}
    raise AssertionError('invalid path accepted: ' + reason)


def checks(fixture, mutation):
    collector = BulkRecords(drop_timeout=mutation == 'usb-drop-timeout')
    reads = [collector.receive(event) for event in fixture['usb_reads']]
    frames = [frame for row in reads for frame in row['records']]
    require(frames == fixture['usb_expected_records'] and not collector.buffer, 'USB partial-record literal failed')
    require([row['bulk']['actual_length'] for row in reads] == [3, 2, 1, 0], 'USB actual-length literal failed')
    wrong = octets(fixture['usb_reads'][0]['data_hex']).ljust(8, b'\x00')[:6].hex()
    require(wrong == 'aabbcc000000' and reads[0]['records'] == [], 'USB requested-length fault differs')
    retry = retry_after_stall(new_id=mutation == 'usb-new-command-id')
    require(retry['device_value'] == 17 and retry['application_count'] == 1 and
            retry['retry'] == {'result': 17, 'applied_now': False}, 'USB retry applied command twice')
    faulty_retry = retry_after_stall(new_id=True)
    require([faulty_retry['device_value'], faulty_retry['application_count']] == [24, 2], 'USB duplicate control differs')
    device = IdempotentDevice()
    device.execute(41, 7)
    id_conflict = rejected(lambda: device.execute(41, 8), 'COMMAND_ID_CONFLICT')

    endpoint = UsbEndpoint()
    stalled, inflight = endpoint.submit(0), endpoint.submit(1)
    endpoint.callback(stalled, 'STALL')
    pending_clear = rejected(endpoint.clear_halt, 'PENDING_ACTIVE')
    endpoint.cancel(inflight)
    after_cancel_count = len(endpoint.pending)
    require(after_cancel_count == 1, 'USB cancel returned ownership early')
    cancelled = endpoint.callback(inflight, 'CANCELLED', 'aabb')
    require(cancelled['published'] is False and cancelled['actual_length'] == 2, 'USB cancel-prefix policy differs')
    endpoint.clear_halt()
    usable_again = endpoint.submit(1)
    endpoint.callback(usable_again, 'COMPLETED')

    connection = UsbEndpoint()
    old = connection.submit(0)
    connection.cancel(old)
    owned = rejected(lambda: connection.submit(0), 'BUFFER_OWNED')
    connection.disconnect()
    disconnected = rejected(lambda: connection.submit(1), 'DISCONNECTED')
    connection.reconnect()
    fresh = connection.submit(1)
    old_result = connection.callback(old, 'COMPLETED', 'eeee')
    require(old_result['stale'] is True and old_result['published'] is False, 'old USB generation published bytes')
    require(fresh in connection.pending, 'old USB callback removed fresh transfer')
    new_result = connection.callback(fresh, 'COMPLETED', '1122')
    require(new_result['published_hex'] == '1122' and new_result['stale'] is False, 'fresh USB callback missing')
    duplicate_callback = rejected(lambda: connection.callback(old, 'COMPLETED'), 'UNKNOWN_TRANSFER')
    race = UsbEndpoint()
    race_token = race.submit(0)
    race.cancel(race_token)
    cancel_race = race.callback(race_token, 'COMPLETED', 'aa')
    require(cancel_race['stale'] is False and cancel_race['published'] is False and cancel_race['actual_length'] == 1,
            'USB cancellation race policy differs')
    late = UsbEndpoint()
    old_late = late.submit(0)
    late.disconnect()
    late.reconnect()
    new_late = late.submit(1)
    old_no_device = late.callback(old_late, 'NO_DEVICE')
    require(late.connected and new_late in late.pending and old_no_device['stale'],
            'old NO_DEVICE callback disconnected new session')
    late.callback(new_late, 'COMPLETED')
    no_device = UsbEndpoint()
    gone = no_device.submit(0)
    disconnect_callback = no_device.callback(gone, 'NO_DEVICE', 'aa')
    require(not no_device.connected and disconnect_callback['stale'], 'NO_DEVICE did not end session')
    require(bulk_result(0,'COMPLETED','')['actual_length'] == 0, 'zero bulk size boundary differs')

    tracker = CompletionTracker(finish_first=mutation == 'pcie-finish-first')
    for request in fixture['pcie_requests']:
        tracker.issue(**request)
    busy = rejected(lambda: tracker.issue(5, 0x3000, 4), 'TAG_BUSY')
    states = []
    for index, completion in enumerate(fixture['pcie_completions']):
        states.append(tracker.receive(**completion))
        require(states[-1] == fixture['pcie_expected_states'][index], 'PCIe per-completion state literal failed')
        if index == 0:
            before_done = rejected(lambda: tracker.cpu_read(5), 'DEVICE_OWNED')
    payloads = {str(tag): tracker.cpu_read(tag) for tag in (5, 9)}
    require(payloads == fixture['pcie_expected_payloads'], 'PCIe assembled payload literal failed')
    duplicate = rejected(lambda: tracker.receive(**fixture['pcie_completions'][2]), 'NOT_ACTIVE')
    tracker.retire(5)
    retired = rejected(lambda: tracker.receive(**fixture['pcie_completions'][2]), 'UNKNOWN_TAG')
    tracker.issue(5, 0x3000, 4)
    tracker.receive(5, 0, 4, '55667788')
    require(tracker.cpu_read(5) == '55667788', 'retired tag reuse failed')

    bads = []
    first, last = fixture['pcie_completions'][0], fixture['pcie_completions'][2]
    alterations = [('BYTE_COUNT', dict(last, byte_count=32)),
                   ('LOWER_ADDRESS', dict(last, lower_address=16)),
                   ('BYTE_COUNT', first),  # 먼저 받은 첫 조각을 다시 보내는 중복입니다.
                   ('COMPLETION_STATUS', dict(last, status='UR')),
                   ('PAYLOAD_LENGTH', dict(last, data_hex='')),
                   ('PAYLOAD_LENGTH', dict(last, data_hex='101112')),
                   ('PAYLOAD_LENGTH', dict(last, data_hex='00'*20))]
    for label, bad in alterations:
        item = CompletionTracker(ignore_byte_count=mutation == 'pcie-ignore-byte-count')
        item.issue(5, 0x1070, 32)
        item.receive(**first)
        try:
            item.receive(**bad)
        except ContractError as exc:
            require(str(exc) == label, 'PCIe wrong bad-completion reason')
            bads.append({'expected': label, 'actual': str(exc)})
        else:
            raise AssertionError('PCIe malformed completion accepted: '+label)
        require(len(item.requests[5]['data']) == 16, 'rejected PCIe completion changed buffer')
    rcb = CompletionTracker()
    rcb.issue(5, 0x1070, 32)
    rcb_split = rejected(lambda: rcb.receive(5,112,32,'00010203'), 'RCB_SPLIT')
    single = CompletionTracker()
    single.issue(5, 0x1070, 32)
    single.receive(5,112,32,fixture['pcie_expected_payloads']['5'])
    require(single.cpu_read(5) == payloads['5'], 'single completion across RCB differs')
    legal = CompletionTracker()
    legal.issue(31,0x1F00,256)
    legal.receive(31,0,256,'11'*128)
    legal.receive(31,0,128,'22'*128)
    require(legal.cpu_read(31) == '11'*128+'22'*128, 'maximum request literal failed')
    maximum_payload = CompletionTracker()
    maximum_payload.issue(0,0x1000,256)
    mps = rejected(lambda: maximum_payload.receive(0,0,256,'00'*132),'PAYLOAD_LENGTH')
    ending = CompletionTracker()
    ending.issue(0,0x1FFC,4)
    ending.receive(0,124,4,'aabbccdd')
    require(ending.cpu_read(0) == 'aabbccdd', '4KB ending boundary differs')

    invalid = []
    for label, function in [
        ('boolean_requested', lambda: bulk_result(True,'COMPLETED','')),
        ('oversized_actual', lambda: bulk_result(1,'COMPLETED','aabb')),
        ('unsupported_bulk_status', lambda: bulk_result(8,'OVERFLOW','')),
        ('odd_hex', lambda: octets('f')), ('nonhex', lambda: octets('zz')),
        ('tag32', lambda: CompletionTracker().issue(32,0,4)),
        ('unaligned_address', lambda: CompletionTracker().issue(0,1,4)),
        ('unaligned_length', lambda: CompletionTracker().issue(0,0,5)),
        ('cross_4KB', lambda: CompletionTracker().issue(0,0x1FFC,8)),
        ('zero_length', lambda: CompletionTracker().issue(0,0,0)),
        ('too_long', lambda: CompletionTracker().issue(0,0,260))]:
        try:
            function()
        except InputError as exc:
            invalid.append({'case':label,'exception':type(exc).__name__,'message':str(exc)})
        else:
            raise AssertionError('invalid input accepted: '+label)
    return {'usb':{'reads':reads,'requested_as_length_fault':wrong,'retry':retry,'faulty_retry':faulty_retry,
                   'id_conflict':id_conflict,'pending_clear':pending_clear,'pending_after_cancel':after_cancel_count,
                   'cancelled_callback':cancelled,'buffer_owned':owned,'disconnected_submit':disconnected,
                   'old_callback':old_result,'new_callback':new_result,'duplicate_callback':duplicate_callback,
                   'cancel_race':cancel_race,'old_no_device':old_no_device,'disconnect_callback':disconnect_callback},
            'pcie':{'completion_states':states,'payloads':payloads,'busy_tag':busy,'partial_cpu_read':before_done,
                    'duplicate_done':duplicate,'retired_completion':retired,'rejected_completions':bads,
                    'rcb_split':rcb_split,'single_crossing_completion_accepted':True,
                    'request256_payload128_test':True,'mps_exceeded':mps,'end_4KB_request_accepted':True},
            'input_errors':invalid}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mutation',choices=['usb-drop-timeout','usb-new-command-id','pcie-ignore-byte-count','pcie-finish-first'])
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        output.mkdir(parents=True,exist_ok=False)
    except FileExistsError:
        parser.error('output already exists: '+str(output))
    report = {'scope':'synthetic decoded USB/PCIe transactions; no device, libusb, driver, root port or physical-link execution',
              'python':sys.version,'executable':sys.executable,'platform':platform.platform(),
              'utc':datetime.now(timezone.utc).isoformat(),'argv':sys.argv,'optimize':sys.flags.optimize,
              'mutation':args.mutation,'source_and_input_sha256':{
                  name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in ('models.py','run_cases.py','fixtures.json')}}
    try:
        report['checks'] = checks(json.loads((BASE/'fixtures.json').read_text(encoding='utf-8')),args.mutation)
        report['status'] = 'PASS'
    except Exception as exc:
        report.update(status='ERROR',exception=type(exc).__name__,message=str(exc))
    (output/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'output':str(output)},ensure_ascii=False))
    return 0 if report['status']=='PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

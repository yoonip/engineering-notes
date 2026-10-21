"""USB API 결과와 제한된 PCIe Completion의 합성 호스트 계약입니다."""


class InputError(ValueError):
    pass


class ContractError(ValueError):
    pass


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:  # bool을 정수 입력으로 받지 않습니다.
        raise InputError(f'integer in [{low}, {high}] required')
    return value


def octets(value):
    if type(value) is not str or len(value) % 2 or any(c not in '0123456789abcdefABCDEF' for c in value):
        raise InputError('complete hex bytes required')
    return bytes.fromhex(value)


STATUSES = {'COMPLETED', 'TIMED_OUT', 'STALL', 'CANCELLED', 'NO_DEVICE', 'ERROR'}


def bulk_result(requested, status, data_hex):
    integer(requested, 0, 4096)  # 4096은 이 예제의 입력 상한이며 USB 공통 한계가 아닙니다.
    if type(status) is not str or status not in STATUSES:
        raise InputError('unsupported synthetic bulk status')
    data = octets(data_hex)
    if len(data) > requested:
        raise InputError('actual bytes exceed requested capacity')
    return {'status': status, 'requested': requested, 'actual_length': len(data),
            'short': len(data) < requested, 'data_hex': data.hex()}


class BulkRecords:
    """순서가 정해진 IN 결과에서 6바이트 자체 레코드를 조립합니다."""

    def __init__(self, drop_timeout=False):
        self.buffer = bytearray()  # bytearray는 내용을 바꿀 수 있는 바이트 저장소입니다.
        self.drop_timeout = drop_timeout

    def receive(self, event):
        result = bulk_result(**event)
        usable = result['status'] in {'COMPLETED', 'TIMED_OUT'}
        if self.drop_timeout and result['status'] == 'TIMED_OUT':
            usable = False  # 의도적 오류: timeout에 이미 전송된 바이트도 버립니다.
        frames = []
        if usable:
            self.buffer.extend(octets(result['data_hex']))
            while len(self.buffer) >= 6:
                frames.append(self.buffer[:6].hex())
                del self.buffer[:6]  # 슬라이스의 끝은 포함하지 않으며 소비한 레코드를 지웁니다.
        return {'bulk': result, 'records': frames, 'pending_hex': self.buffer.hex(), 'prefix_used': usable}


class IdempotentDevice:
    """같은 command ID·같은 인수의 재요청을 한 번만 적용하는 자체 장치 규칙입니다."""

    def __init__(self):
        self.value, self.applied = 10, 0
        self.saved = {}

    def execute(self, command_id, delta):
        integer(command_id, 1, 1000000)
        integer(delta, -100, 100)
        if command_id in self.saved:
            old_delta, result = self.saved[command_id]
            if old_delta != delta:
                raise ContractError('COMMAND_ID_CONFLICT')
            return {'result': result, 'applied_now': False}
        self.value += delta
        self.applied += 1
        self.saved[command_id] = (delta, self.value)
        return {'result': self.value, 'applied_now': True}


class UsbEndpoint:
    """단일 bulk endpoint의 callback·buffer 소유권·연결 세대를 모델링합니다."""

    def __init__(self):
        self.generation, self.serial = 0, 0
        self.connected, self.halted = True, False
        self.pending = {}  # {}는 token별 제출 상태를 보관하는 딕셔너리입니다.

    def submit(self, slot):
        integer(slot, 0, 3)
        if not self.connected:
            raise ContractError('DISCONNECTED')
        if self.halted:
            raise ContractError('HALTED')
        if any(item['slot'] == slot for item in self.pending.values()):
            raise ContractError('BUFFER_OWNED')
        self.serial += 1
        token = (self.generation, self.serial)  # tuple은 변경하지 않는 식별자 묶음입니다.
        self.pending[token] = {'slot': slot, 'cancel_requested': False}
        return token

    def cancel(self, token):
        if token not in self.pending:
            raise ContractError('UNKNOWN_TRANSFER')
        self.pending[token]['cancel_requested'] = True  # 취소 요청만으로 버퍼를 반환하지 않습니다.

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.generation += 1
            for item in self.pending.values():
                item['cancel_requested'] = True

    def reconnect(self):
        if self.connected:
            raise ContractError('ALREADY_CONNECTED')
        self.connected, self.halted = True, False

    def callback(self, token, status, data_hex=''):
        if token not in self.pending:
            raise ContractError('UNKNOWN_TRANSFER')
        if type(status) is not str or status not in STATUSES:
            raise InputError('unsupported synthetic bulk status')
        data = octets(data_hex)
        if status == 'NO_DEVICE' and token[0] == self.generation:
            self.disconnect()
        item = self.pending.pop(token)  # pop은 해당 제출의 소유권을 여기서 반환합니다.
        stale = token[0] != self.generation or not self.connected
        if status == 'STALL' and not stale:
            self.halted = True
        accepted = not stale and not item['cancel_requested'] and status in {'COMPLETED', 'TIMED_OUT'}
        return {'slot_freed': item['slot'], 'stale': stale, 'cancel_requested': item['cancel_requested'],
                'actual_length': len(data), 'published_hex': data.hex() if accepted else '', 'published': accepted}

    def clear_halt(self):
        if not self.connected:
            raise ContractError('DISCONNECTED')
        if self.pending:
            raise ContractError('PENDING_ACTIVE')  # pending callback을 모두 받은 뒤 clear하는 자체 순서입니다.
        self.halted = False


def retry_after_stall(new_id=False):
    device, endpoint = IdempotentDevice(), UsbEndpoint()
    first = device.execute(41, 7)  # OUT 명령이 적용된 뒤 ACK를 읽는 IN 전송이 STALL한 일정입니다.
    token = endpoint.submit(0)
    ack = endpoint.callback(token, 'STALL')
    endpoint.clear_halt()  # endpoint 복구 자체는 이미 적용한 응용 명령을 취소하지 않습니다.
    retried = device.execute(42 if new_id else 41, 7)
    return {'first': first, 'ack': ack, 'retry': retried,
            'device_value': device.value, 'application_count': device.applied}


class CompletionTracker:
    """한 Requester의 DW 정렬·전체 byte-enable·SC read만 받는 제한 모델입니다."""

    def __init__(self, ignore_byte_count=False, finish_first=False):
        self.requests = {}
        self.ignore_byte_count, self.finish_first = ignore_byte_count, finish_first

    def issue(self, tag, address, length):
        integer(tag, 0, 31)
        integer(address, 0, (1 << 32) - 1)
        integer(length, 4, 256)
        if address % 4 or length % 4:
            raise InputError('DWORD-aligned full-byte requests only')
        if (address & 4095) + length > 4096:
            raise InputError('request crosses 4KB boundary')
        if tag in self.requests:
            raise ContractError('TAG_BUSY')
        self.requests[tag] = {'address': address, 'length': length, 'data': bytearray(), 'state': 'ACTIVE'}

    def receive(self, tag, lower_address, byte_count, data_hex, status='SC'):
        integer(tag, 0, 31)
        integer(lower_address, 0, 127)
        integer(byte_count, 1, 256)  # raw wire field의 0=4096 인코딩은 이 모델에 없습니다.
        data = octets(data_hex)
        if tag not in self.requests:
            raise ContractError('UNKNOWN_TAG')
        request = self.requests[tag]
        if request['state'] != 'ACTIVE':
            raise ContractError('NOT_ACTIVE')
        if status != 'SC':
            raise ContractError('COMPLETION_STATUS')
        received = len(request['data'])
        remaining = request['length'] - received
        next_address = request['address'] + received
        if not self.ignore_byte_count and byte_count != remaining:
            raise ContractError('BYTE_COUNT')
        if lower_address != next_address & 127:
            raise ContractError('LOWER_ADDRESS')
        if not data or len(data) % 4 or len(data) > remaining or len(data) > 128:
            raise ContractError('PAYLOAD_LENGTH')
        if len(data) < remaining and (next_address + len(data)) % 128:
            raise ContractError('RCB_SPLIT')  # RCB는 크기 상한이 아니라 중간 분할 위치의 경계입니다.
        request['data'].extend(data)  # 모든 검사를 통과한 뒤에만 요청별 저장소를 바꿉니다.
        done = len(request['data']) == request['length'] or self.finish_first
        if done:
            request['state'] = 'DONE'
        return {'tag': tag, 'received': len(request['data']), 'remaining': request['length']-len(request['data']),
                'state': request['state']}

    def cpu_read(self, tag):
        if tag not in self.requests:
            raise ContractError('UNKNOWN_TAG')
        if self.requests[tag]['state'] != 'DONE':
            raise ContractError('DEVICE_OWNED')
        return self.requests[tag]['data'].hex()

    def retire(self, tag):
        self.cpu_read(tag)  # 완료를 확인하기 전 tag를 재사용하지 않습니다.
        del self.requests[tag]

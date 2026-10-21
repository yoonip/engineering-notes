"""NVMe·카드의 완료와 영속성을 구분하는 decoded 합성 호스트 모델입니다."""
from dataclasses import dataclass


class ContractError(ValueError):
    """지원 범위 밖 입력과 잘못된 상태 전이를 거부합니다."""


def integer(value, low, high, reason):
    if type(value) is not int or not low <= value <= high:  # bool은 정수 입력에서 제외합니다.
        raise ContractError(reason)
    return value


def boolean(value, reason):
    if type(value) is not bool:
        raise ContractError(reason)
    return value


def blocks_at(lba, payload):
    integer(lba, 0, 7, 'LBA_RANGE')
    if not isinstance(payload, list) or not payload or lba + len(payload) > 8:
        raise ContractError('BLOCK_RANGE')
    decoded = []
    for item in payload:  # for는 각 블록을 순서대로 검사합니다.
        if not isinstance(item, str) or len(item) != 8:
            raise ContractError('BLOCK_HEX')
        try:
            data = bytes.fromhex(item)
        except ValueError as exc:
            raise ContractError('BLOCK_HEX') from exc
        if len(data) != 4:
            raise ContractError('BLOCK_HEX')
        decoded.append(data)
    return {lba + offset: data for offset, data in enumerate(decoded)}


@dataclass(frozen=True)
class Command:
    kind: str
    data: dict
    fua: bool = False


class Nvme:
    """단일 SQ·namespace, 8개 4바이트 블록과 직렬 flush 정책입니다."""

    def __init__(self, vwc=True, mutation='none'):
        self.vwc = boolean(vwc, 'VWC_BOOL')
        self.mutation = mutation
        self.media = {index: bytes(4) for index in range(8)}
        self.cache = {}
        self.pending = {}
        self.powered = True

    def _live(self):
        if not self.powered:
            raise ContractError('POWER_LOST_NEW_SESSION_REQUIRED')

    def _cid(self, cid):
        self._live()
        integer(cid, 0, 65535, 'CID_RANGE')
        if cid in self.pending:
            raise ContractError('CID_IN_USE')
        if len(self.pending) >= 4:
            raise ContractError('QUEUE_FULL')

    def submit_write(self, cid, lba, payload, fua=False):
        self._cid(cid)
        data = blocks_at(lba, payload)
        boolean(fua, 'FUA_BOOL')
        if any(cmd.kind == 'FLUSH' for cmd in self.pending.values()):
            raise ContractError('FLUSH_BARRIER_ACTIVE')
        if any(set(data) & set(cmd.data) for cmd in self.pending.values()):
            raise ContractError('OVERLAPPING_INFLIGHT_WRITE')
        self.pending[cid] = Command('WRITE', data, fua)

    def submit_flush(self, cid):
        self._cid(cid)
        if self.pending:  # 자체 정책: 앞선 쓰기의 완료를 모두 관측한 뒤 flush합니다.
            raise ContractError('PRIOR_COMMAND_PENDING')
        self.pending[cid] = Command('FLUSH', {})

    def complete(self, cid, status, fault_prefix=0):
        self._live()
        integer(cid, 0, 65535, 'CID_RANGE')
        if cid not in self.pending:
            raise ContractError('UNKNOWN_CID')
        if status not in ('SUCCESS', 'MEDIA_ERROR', 'ABORTED'):
            raise ContractError('STATUS_UNSUPPORTED')
        command = self.pending[cid]
        integer(fault_prefix, 0, len(command.data), 'FAULT_PREFIX_RANGE')
        if status == 'SUCCESS' and fault_prefix:
            raise ContractError('FAULT_ON_SUCCESS')
        # 검증 입력을 모두 확인한 뒤에만 명령을 제거합니다.
        del self.pending[cid]
        if status != 'SUCCESS':
            for lba, data in list(command.data.items())[:fault_prefix]:
                self.media[lba] = data  # 실패 장치의 주입된 내부 효과이며 CQE 정보가 아닙니다.
                self.cache.pop(lba, None)
            if command.kind == 'FLUSH' and self.mutation == 'nvme-ignore-flush-error':
                self.media.update(self.cache)
                self.cache.clear()
                return {'cid': cid, 'kind': command.kind, 'status': status,
                        'result': 'SUCCESS', 'durable_ack': True}
            return {'cid': cid, 'kind': command.kind, 'status': status,
                    'result': 'FAILED_UNCERTAIN', 'durable_ack': False}
        if command.kind == 'FLUSH':
            self.media.update(self.cache)
            self.cache.clear()
            durable = True
        elif command.fua or not self.vwc:
            if command.fua and self.mutation == 'nvme-fua-flushes-all':
                self.media.update(self.cache)
                self.cache.clear()
            self.media.update(command.data)
            for lba in command.data:
                self.cache.pop(lba, None)
            durable = True
        else:
            self.cache.update(command.data)
            durable = self.mutation == 'nvme-completion-is-durable'
        return {'cid': cid, 'kind': command.kind, 'status': status,
                'result': 'SUCCESS', 'durable_ack': durable}

    def read(self, lba):
        """합성 가시 데이터 조회이며 power_loss 뒤에는 내부 media만 검사합니다."""
        integer(lba, 0, 7, 'LBA_RANGE')
        return self.cache.get(lba, self.media[lba]).hex()

    def power_loss(self):
        self._live()
        self.cache.clear()
        self.pending.clear()
        self.powered = False  # 재연결·오래된 완료는 별도 새 세션이 필요합니다.


class Card:
    """eMMC/SD의 wire 명령 대신 이미 해석한 상태·캐시 기능을 입력받습니다."""

    def __init__(self, family, cache_supported=False, mutation='none'):
        if family not in ('emmc', 'sd'):
            raise ContractError('CARD_FAMILY')
        self.family = family
        self.cache_supported = boolean(cache_supported, 'CAPABILITY_BOOL')
        self.cache_enabled = False
        self.mutation = mutation
        self.media = {index: bytes(4) for index in range(8)}
        self.cache = {}
        self.active = None
        self.recovery_required = False
        self.powered = True

    def _live(self):
        if not self.powered:
            raise ContractError('POWER_LOST_NEW_SESSION_REQUIRED')

    def enable_cache(self):
        self._live()
        if self.active or self.recovery_required:
            raise ContractError('CARD_NOT_IDLE')
        if not self.cache_supported:
            raise ContractError('CACHE_UNSUPPORTED')
        self.cache_enabled = True

    def submit_write(self, request_id, lba, payload):
        self._live()
        integer(request_id, 0, 65535, 'REQUEST_ID_RANGE')
        if self.active or self.recovery_required:
            raise ContractError('CARD_NOT_IDLE')
        self.active = (request_id, blocks_at(lba, payload))

    def poll(self, busy, ready, state, error=None, fault_prefix=0):
        self._live()
        if self.active is None:
            raise ContractError('NO_ACTIVE_WRITE')
        boolean(busy, 'BUSY_BOOL')
        boolean(ready, 'READY_BOOL')
        if state not in ('TRAN', 'PRG', 'RCV'):
            raise ContractError('STATE_UNSUPPORTED')
        if error not in (None, 'WRITE_ERROR', 'WP_VIOLATION'):
            raise ContractError('CARD_ERROR_UNSUPPORTED')
        request_id, data = self.active
        integer(fault_prefix, 0, len(data), 'FAULT_PREFIX_RANGE')
        if error is None and fault_prefix:
            raise ContractError('FAULT_WITHOUT_ERROR')
        if error is not None and self.mutation != 'card-ignore-status-error':
            for lba, item in list(data.items())[:fault_prefix]:
                self.media[lba] = item
                self.cache.pop(lba, None)
            self.active = None
            self.recovery_required = True
            return {'request_id': request_id, 'result': 'FAILED_UNCERTAIN',
                    'durable_ack': False, 'error': error}
        if busy:
            return {'request_id': request_id, 'result': 'WAIT_BUSY', 'durable_ack': False}
        if self.mutation != 'card-busy-is-done' and (not ready or state != 'TRAN'):
            return {'request_id': request_id, 'result': 'WAIT_STATUS', 'durable_ack': False}
        if self.cache_enabled:
            self.cache.update(data)
        else:
            self.media.update(data)
        self.active = None
        return {'request_id': request_id, 'result': 'SUCCESS',
                'durable_ack': not self.cache_enabled}

    def timeout(self, fault_prefix=0):
        self._live()
        if self.active is None:
            raise ContractError('NO_ACTIVE_WRITE')
        request_id, data = self.active
        integer(fault_prefix, 0, len(data), 'FAULT_PREFIX_RANGE')
        for lba, item in list(data.items())[:fault_prefix]:
            self.media[lba] = item
            self.cache.pop(lba, None)
        self.active = None
        self.recovery_required = True  # 자체 정책: 불명확한 결과 뒤 새 쓰기를 막습니다.
        return {'request_id': request_id, 'result': 'TIMED_OUT_UNKNOWN', 'durable_ack': False}

    def flush(self, success):
        self._live()
        boolean(success, 'FLUSH_SUCCESS_BOOL')
        if self.active or self.recovery_required:
            raise ContractError('CARD_NOT_IDLE')
        if not self.cache_supported or not self.cache_enabled:
            raise ContractError('CACHE_NOT_ENABLED')
        if not success:
            self.recovery_required = True
            return {'result': 'FAILED_UNCERTAIN', 'durable_ack': False}
        self.media.update(self.cache)
        self.cache.clear()
        return {'result': 'SUCCESS', 'durable_ack': True}

    def read(self, lba):
        """합성 가시 데이터 조회이며 꺼진 실물 카드에 read를 보내지 않습니다."""
        integer(lba, 0, 7, 'LBA_RANGE')
        return self.cache.get(lba, self.media[lba]).hex()

    def power_loss(self):
        self._live()
        self.active = None
        self.cache.clear()
        self.powered = False

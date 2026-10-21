"""NAND의 블록 상태·전체 블록 매핑·읽기 telemetry를 다루는 합성 모델입니다."""
from dataclasses import dataclass, field


class ContractError(ValueError):
    """모델 범위 밖 입력이나 허용하지 않는 상태 전이입니다."""


def number(value, low, high, reason):
    if type(value) is not int or not low <= value <= high:  # bool을 정수로 받지 않습니다.
        raise ContractError(reason)
    return value


def flag(value):
    if type(value) is not bool:
        raise ContractError('BOOL_REQUIRED')
    return value


def page_bytes(text):
    if not isinstance(text, str) or len(text) != 8:
        raise ContractError('PAGE_HEX')
    try:
        data = bytes.fromhex(text)
    except ValueError as exc:
        raise ContractError('PAGE_HEX') from exc
    if len(data) != 4:
        raise ContractError('PAGE_HEX')
    return data


def payload_pages(payload):
    if not isinstance(payload, list) or len(payload) != 2:
        raise ContractError('TWO_PAGES_REQUIRED')
    return [page_bytes(item) for item in payload]


@dataclass
class Block:
    kind: str = 'GOOD'
    erases: int = 0
    pages: list = field(default_factory=lambda: [b'\xff' * 4, b'\xff' * 4])
    programmed: set = field(default_factory=set)
    reads: int = 0
    corrected_max: int = 0
    unreadable: bool = False


class Nand:
    """6블록·2페이지·4바이트이며 한 erase 주기에 페이지당 program은 1회입니다."""

    def __init__(self, factory_bad=(5,), erase_counts=None, mutation='none'):
        if not isinstance(factory_bad, (tuple, list)):
            raise ContractError('BAD_BLOCK_LIST')
        for block in factory_bad:
            number(block, 0, 5, 'BLOCK_RANGE')
        if len(set(factory_bad)) != len(factory_bad):
            raise ContractError('DUPLICATE_BAD_BLOCK')
        counts = [0] * 6 if erase_counts is None else erase_counts
        if not isinstance(counts, list) or len(counts) != 6:
            raise ContractError('ERASE_COUNT_LIST')
        for count in counts:
            number(count, 0, 1000000, 'ERASE_COUNT_RANGE')
        self.blocks = [Block(kind='FACTORY_BAD' if i in factory_bad else 'GOOD', erases=counts[i])
                       for i in range(6)]
        self.mutation = mutation
        self.program_attempt_bytes = 0
        self.erase_attempts = 0

    def block(self, index):
        return self.blocks[number(index, 0, 5, 'BLOCK_RANGE')]

    def _good(self, index):
        block = self.block(index)
        if block.kind != 'GOOD':
            raise ContractError('BAD_BLOCK')
        return block

    def program(self, index, page, text, fail=False):
        block = self._good(index)
        number(page, 0, 1, 'PAGE_RANGE')
        data = page_bytes(text)
        flag(fail)
        zero_to_one = any((old & new) != new for old, new in zip(block.pages[page], data))
        broken = self.mutation == 'nand-zero-to-one' and zero_to_one
        if zero_to_one and not broken:
            raise ContractError('ERASE_REQUIRED')
        if page in block.programmed and not broken:
            raise ContractError('PAGE_ALREADY_PROGRAMMED')
        if page == 1 and 0 not in block.programmed:
            raise ContractError('PAGE_ORDER')
        self.program_attempt_bytes += 4
        if fail:
            block.kind = 'GROWN_BAD'  # 실패한 후보를 격리하며 부분 bit 효과는 모델 밖입니다.
            return False
        block.pages[page] = data
        block.programmed.add(page)
        return True

    def erase(self, index, fail=False):
        block = self._good(index)
        flag(fail)
        self.erase_attempts += 1
        if fail:
            block.kind = 'GROWN_BAD'
            return False
        block.pages = [b'\xff' * 4, b'\xff' * 4]
        block.programmed.clear()
        block.erases += 1
        block.reads = block.corrected_max = 0
        block.unreadable = False
        return True

    def read(self, index, page, corrected=0, ue=False):
        block = self._good(index)
        number(page, 0, 1, 'PAGE_RANGE')
        number(corrected, 0, 8, 'CORRECTED_RANGE')
        flag(ue)
        if ue and corrected:
            raise ContractError('UE_COUNT_UNKNOWN')
        block.reads += 1
        block.corrected_max = max(block.corrected_max, corrected)
        block.unreadable = block.unreadable or ue
        if block.unreadable:
            data = block.pages[page].hex() if self.mutation == 'publish-ue' else None
            return {'status': 'UE', 'data_hex': data}
        return {'status': 'CE' if corrected else 'OK', 'data_hex': block.pages[page].hex()}


class Manager:
    """논리 블록당 물리 블록 하나를 사용하며 복사·검증 후 매핑을 바꿉니다."""

    def __init__(self, factory_bad=(5,), erase_counts=None, read_limit=4, ce_limit=2, mutation='none'):
        number(read_limit, 1, 1000000, 'READ_LIMIT_RANGE')
        number(ce_limit, 1, 8, 'CE_LIMIT_RANGE')
        self.nand = Nand(factory_bad, erase_counts, mutation)
        self.mapping = {}
        self.host_bytes = 0
        self.move_bytes = 0
        self.read_limit, self.ce_limit = read_limit, ce_limit
        self.mutation = mutation

    def seed(self, logical, physical, payload):
        number(logical, 0, 2, 'LOGICAL_RANGE')
        data = payload_pages(payload)
        block = self.nand._good(physical)
        if logical in self.mapping or physical in self.mapping.values() or block.programmed:
            raise ContractError('SEED_CONFLICT')
        for page, item in enumerate(data):
            self.nand.program(physical, page, item.hex())
        self.mapping[logical] = physical

    def reset_metrics(self):
        self.host_bytes = self.move_bytes = 0
        self.nand.program_attempt_bytes = self.nand.erase_attempts = 0

    def free_blocks(self):
        return [i for i, block in enumerate(self.nand.blocks)
                if i not in self.mapping.values() and not block.programmed and
                (block.kind == 'GOOD' or self.mutation == 'reuse-bad')]

    def _choose(self, static=False):
        free = self.free_blocks()
        if not free:
            raise ContractError('NO_FREE_BLOCK')
        if static:
            return max(free, key=lambda i: (self.nand.blocks[i].erases, -i))
        return min(free, key=lambda i: (self.nand.blocks[i].erases, i))

    def _logical(self, logical):
        number(logical, 0, 2, 'LOGICAL_RANGE')
        if logical not in self.mapping:
            raise ContractError('UNMAPPED_LOGICAL')
        return self.mapping[logical]

    def due(self, logical):
        block = self.nand.block(self._logical(logical))
        if block.unreadable:
            return True
        if self.mutation == 'skip-scrub':
            return False
        return block.reads >= self.read_limit or block.corrected_max >= self.ce_limit

    def read_page(self, logical, page, corrected=0, ue=False):
        physical = self._logical(logical)
        result = self.nand.read(physical, page, corrected, ue)
        block = self.nand.block(physical)
        return dict(result, block=physical, reads=block.reads,
                    corrected_max=block.corrected_max, scrub_due=self.due(logical))

    def _install(self, logical, data, reason, fault='none', static=False):
        target = self._choose(static)
        source = self.mapping.get(logical)
        if self.mutation == 'early-remap':
            self.mapping[logical] = target  # 의도적 오류: 쓰기·검증 전에 새 위치를 공개합니다.
        for page, item in enumerate(data):
            if not self.nand.program(target, page, item.hex(), fail=fault == 'program' and page == 1):
                return {'result': 'DEST_PROGRAM_FAILED', 'source': source, 'target': target,
                        'mapped': self.mapping.get(logical)}
        # 비교 read의 ECC 결과는 OK로 고정한 자체 검증이며 물리 ECC 동작이 아닙니다.
        copied = [self.nand.read(target, page)['data_hex'] for page in range(2)]
        if fault == 'verify' or copied != [item.hex() for item in data]:
            self.nand.block(target).kind = 'GROWN_BAD'
            return {'result': 'DEST_VERIFY_FAILED', 'source': source, 'target': target,
                    'mapped': self.mapping.get(logical)}
        self.mapping[logical] = target
        if reason == 'host':
            self.host_bytes += 8
        else:
            self.move_bytes += 8
        cleanup = 'NONE'
        if source is not None:
            cleanup = 'ERASED' if self.nand.erase(source, fail=fault == 'erase') else 'ERASE_FAILED_RETIRED'
        return {'result': 'MAPPED', 'source': source, 'target': target, 'cleanup': cleanup}

    def write(self, logical, payload, fault='none'):
        number(logical, 0, 2, 'LOGICAL_RANGE')
        data = payload_pages(payload)
        if fault not in ('none', 'program', 'verify', 'erase'):
            raise ContractError('FAULT_UNSUPPORTED')
        return self._install(logical, data, 'host', fault)

    def scrub(self, logical, fault='none'):
        source = self._logical(logical)
        if fault not in ('none', 'read-ue', 'program', 'verify', 'erase'):
            raise ContractError('FAULT_UNSUPPORTED')
        if not self.due(logical):
            return {'result': 'NOT_DUE', 'source': source}
        data = []
        for page in range(2):
            row = self.nand.read(source, page, ue=fault == 'read-ue' and page == 1)
            if row['status'] == 'UE':
                return {'result': 'SOURCE_UE', 'source': source, 'mapped': self.mapping[logical]}
            data.append(bytes.fromhex(row['data_hex']))
        return self._install(logical, data, 'scrub', fault)

    def static_level(self, gap=3, fault='none'):
        number(gap, 1, 1000000, 'GAP_RANGE')
        if fault not in ('none', 'read-ue', 'program', 'verify', 'erase'):
            raise ContractError('FAULT_UNSUPPORTED')
        if not self.mapping:
            return {'result': 'NO_MAPPED_BLOCK'}
        logical = min(self.mapping, key=lambda l: (self.nand.block(self.mapping[l]).erases, l))
        source = self.mapping[logical]
        target = self._choose(static=True)
        if self.nand.block(target).erases - self.nand.block(source).erases < gap:
            return {'result': 'GAP_SMALL', 'source': source, 'target': target}
        data = []
        for page in range(2):
            row = self.nand.read(source, page, ue=fault == 'read-ue' and page == 1)
            if row['status'] == 'UE':
                return {'result': 'SOURCE_UE', 'source': source, 'mapped': source}
            data.append(bytes.fromhex(row['data_hex']))
        return self._install(logical, data, 'static', fault, static=True)

    def snapshot(self):
        return {'mapping': {str(l): p for l, p in sorted(self.mapping.items())},
                'kinds': [b.kind for b in self.nand.blocks],
                'erases': [b.erases for b in self.nand.blocks], 'free': self.free_blocks(),
                'host_bytes': self.host_bytes, 'move_bytes': self.move_bytes,
                'program_attempt_bytes': self.nand.program_attempt_bytes,
                'erase_attempts': self.nand.erase_attempts}

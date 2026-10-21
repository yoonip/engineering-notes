"""바이트 프레이밍과 제한된 Ethernet/IPv4/UDP 캡처의 호스트 모델입니다."""

MARKER = b'\xa5\x5a'  # bytes는 바이트열이며 자체 프레임의 시작 표식입니다.
MAX_PAYLOAD = 8


class InputError(ValueError):  # class는 입력 형식 오류를 구분하는 예외 형을 정의합니다.
    pass


class PacketError(ValueError):
    pass


class StreamParser:
    """A5 5A LEN SEQ DATA SUM8 형식입니다. 기존 저장소의 CRC 프레임과 다릅니다."""

    def __init__(self, ignore_checksum=False):
        self.buffer = bytearray()  # bytearray는 바꿀 수 있는 바이트 저장 공간입니다.
        self.ignore_checksum = ignore_checksum
        self.length_errors = self.checksum_errors = self.expirations = self.peak = 0

    def _drain(self):
        frames = []  # []는 이번 호출에서 완성한 프레임의 목록입니다.
        while self.buffer:
            index = self.buffer.find(MARKER)
            if index < 0:
                self.buffer[:] = b'\xa5' if self.buffer[-1] == 0xA5 else b''
                break  # 시작 표식의 첫 바이트만 있을 때 다음 조각까지 보존합니다.
            if index:
                del self.buffer[:index]  # del은 표식 앞의 잡음 바이트를 제거합니다.
            if len(self.buffer) < 3:
                break
            length = self.buffer[2]  # []는 바이트 위치 접근이며 LEN은 payload 수입니다.
            if length > MAX_PAYLOAD:
                self.length_errors += 1
                del self.buffer[0]  # 후보 한 바이트를 버리고 안쪽의 다음 표식을 찾습니다.
                continue
            needed = 5 + length
            if len(self.buffer) < needed:
                break
            candidate = self.buffer[:needed]
            if not self.ignore_checksum and sum(candidate[2:-1]) & 0xFF != candidate[-1]:
                self.checksum_errors += 1
                del self.buffer[0]
                continue
            frames.append({'sequence': candidate[3], 'payload_hex': candidate[4:-1].hex()})
            del self.buffer[:needed]
        return frames

    def feed(self, chunk):
        if not isinstance(chunk, bytes):
            raise InputError('UART chunk must be bytes')
        frames = []
        for byte in chunk:  # 입력 조각 전체를 먼저 쌓지 않고 한 바이트씩 처리합니다.
            self.buffer.append(byte)
            self.peak = max(self.peak, len(self.buffer))
            frames.extend(self._drain())  # extend는 완성된 목록의 원소를 이어 붙입니다.
        return frames

    def expire_partial(self):
        """호출자가 정한 timeout 사건입니다. 실제 UART/벽시계 timer는 실행하지 않습니다."""
        if self.buffer:
            self.expirations += 1
            del self.buffer[0]
            return self._drain()
        return []


def internet_checksum(data):
    if not isinstance(data, bytes):
        raise InputError('checksum input must be bytes')
    padded = data + (b'\x00' if len(data) % 2 else b'')
    total = sum((padded[i] << 8) | padded[i + 1] for i in range(0, len(padded), 2))
    while total >> 16:  # 상위 carry를 하위16비트에 반복해서 더합니다.
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF  # ~는 비트 반전이며 16비트 one's complement입니다.


def parse_udp_capture(frame, allow_zero_udp=True, ignore_udp_checksum=False):
    """FCS 없는 untagged EthernetII·IHL5 IPv4·비단편 UDP 일부만 지원합니다."""
    if not isinstance(frame, bytes):
        raise InputError('capture must be bytes')
    if len(frame) < 14:
        raise PacketError('ETHERNET_TRUNCATED')
    if frame[12:14] != b'\x08\x00':
        raise PacketError('UNSUPPORTED_ETHERTYPE')
    packet = frame[14:]
    if len(packet) < 20:
        raise PacketError('IP_TRUNCATED')
    version, ihl = packet[0] >> 4, packet[0] & 15
    if version != 4:
        raise PacketError('IP_VERSION')
    if ihl < 5:
        raise PacketError('IP_IHL')
    if ihl != 5:
        raise PacketError('UNSUPPORTED_IP_OPTIONS')
    total = int.from_bytes(packet[2:4], 'big')  # 네트워크 바이트 순서는 상위 바이트부터 읽습니다.
    if total < 28:
        raise PacketError('IP_LENGTH')
    if total > len(packet):
        raise PacketError('IP_TRUNCATED')
    if internet_checksum(packet[:20]) != 0:
        raise PacketError('IP_CHECKSUM')
    flags_offset = int.from_bytes(packet[6:8], 'big')
    if flags_offset & 0x8000:
        raise PacketError('IP_RESERVED_FLAG')
    if flags_offset & 0x3FFF:  # MF나 offset이 있으면 재조립 없이 UDP로 읽지 않습니다.
        raise PacketError('UNSUPPORTED_FRAGMENT')
    if packet[9] != 17:
        raise PacketError('UNSUPPORTED_PROTOCOL')
    udp = packet[20:total]  # IP total 뒤 Ethernet padding을 UDP 데이터에 넣지 않습니다.
    udp_length = int.from_bytes(udp[4:6], 'big')
    if udp_length < 8:
        raise PacketError('UDP_LENGTH')
    if udp_length > len(udp):
        raise PacketError('UDP_TRUNCATED')
    if udp_length < len(udp):
        raise PacketError('UNSUPPORTED_UDP_SURPLUS')  # UDP Options 영역의 지원 여부와 잘못된 길이를 구분합니다.
    wire_checksum = int.from_bytes(udp[6:8], 'big')
    if wire_checksum == 0:
        if not allow_zero_udp:
            raise PacketError('UDP_CHECKSUM_REQUIRED')
        checksum_state = 'omitted_ipv4'
    else:
        pseudo = packet[12:20] + bytes([0, 17]) + udp[4:6]
        if not ignore_udp_checksum and internet_checksum(pseudo + udp) != 0:
            raise PacketError('UDP_CHECKSUM')
        checksum_state = 'checked' if not ignore_udp_checksum else 'bypassed_mutation'
    return {'payload_hex': udp[8:].hex(), 'source_port': int.from_bytes(udp[:2], 'big'),
            'destination_port': int.from_bytes(udp[2:4], 'big'), 'ip_total_length': total,
            'udp_length': udp_length, 'ethernet_padding_bytes': len(packet) - total,
            'udp_checksum': checksum_state}

from dataclasses import dataclass  # 검증한 읽기 전용 샘플 표현
import math  # 비유한 센서값 거절
from google.protobuf.message import DecodeError  # 실제 wire 파서의 실패 구분
import telemetry_pb2  # telemetry.proto에서 실제 생성한 메시지 클래스
@dataclass(frozen=True)  # 검사 뒤 샘플 내용을 바꾸지 않기
class Sample:  # 애플리케이션에 전달할 값
    sequence: int  # 성공적으로 읽은 순번
    sampled_ms: int  # 벤치의 공통 단조 시각
    bus_v: float  # 볼트 단위 전원 관측값
    temperature_c: float  # 섭씨 단위 온도 관측값
def decode(payload):  # wire 해석과 이 벤치의 데이터 계약 확인
    if not isinstance(payload, bytes) or len(payload) > 256: raise ValueError('payload_size_or_type')  # 파서 앞에서 입력 크기 제한
    message = telemetry_pb2.Sample()  # 생성된 클래스의 빈 메시지
    try: message.ParseFromString(payload)  # 실제 Protobuf 런타임으로 역직렬화
    except DecodeError as error: raise ValueError('wire') from error  # 구문 실패를 값 검증과 구분
    for name in ('sequence', 'sampled_ms'):  # 기본값 0이 누락을 숨기지 않게 확인
        if not message.HasField(name): raise ValueError('missing_' + name)  # optional의 명시적 존재 검사
    values = {}  # 같은 채널을 두 번 받아 덮어쓰지 않기
    for reading in message.readings:  # 파서가 읽은 각 채널 검사
        if reading.channel in values or reading.channel not in ('bus_v', 'temperature_c'): raise ValueError('channel')  # 중복과 모르는 이름 거절
        if not reading.HasField('value') or not math.isfinite(reading.value): raise ValueError('value')  # 누락과 NaN·무한대 거절
        values[reading.channel] = reading.value  # 검사한 채널만 보관
    if set(values) != {'bus_v', 'temperature_c'}: raise ValueError('missing_channel')  # 일부 채널만으로 새 상태를 만들지 않기
    if not 0 <= values['bus_v'] <= 30 or not -20 <= values['temperature_c'] <= 80: raise ValueError('bench_range')  # 설명용 벤치 입력 범위
    return Sample(message.sequence, message.sampled_ms, values['bus_v'], values['temperature_c'])  # wire 객체와 분리된 검증 결과
class Monitor:  # 공유 단조 시계와 단일 생산자를 가정한 수신 상태
    def __init__(self, max_age_ms=100):  # 예제의 데이터 신선도 계약
        if type(max_age_ms) is not int or max_age_ms < 0: raise ValueError('max_age')  # 음수나 부동소수 임계값 거절
        self.max_age_ms, self.sample, self.last_now = max_age_ms, None, None  # 값 없음과 0인 값을 분리
    def observe(self, now_ms):  # 수신기에서 관측한 단조 시각 검사
        if type(now_ms) is not int or now_ms < 0: raise ValueError('clock')  # bool·음수·소수는 벤치 시각으로 쓰지 않기
        if self.last_now is not None and now_ms < self.last_now: raise ValueError('clock_rewind')  # 시계가 뒤로 가면 별도 재초기화 필요
        self.last_now = now_ms  # 잘못된 패킷을 받았어도 수신기 시간 관측은 보존
    def accept(self, payload, received_ms):  # 검증한 새 샘플만 상태로 반영
        self.observe(received_ms)  # 외부 메시지의 시각과 수신기 시각을 구분
        candidate = decode(payload)  # 잘못된 wire나 값은 현재 샘플을 바꾸지 않기
        if candidate.sampled_ms > received_ms or received_ms - candidate.sampled_ms > self.max_age_ms: raise ValueError('sample_age')  # 미래 또는 이미 오래된 샘플 거절
        if self.sample is not None and candidate.sequence <= self.sample.sequence: raise ValueError('sequence')  # 중복·역순이 신선도를 갱신하지 않게 처리
        if self.sample is not None and candidate.sampled_ms < self.sample.sampled_ms: raise ValueError('sample_rewind')  # 순번이 커도 측정 시각이 뒤로 가면 거절
        self.sample = candidate  # 모든 검사를 통과한 뒤에만 교체
    def status(self, now_ms):  # 관측값의 신선도만 표시하며 장치를 제어하지 않기
        self.observe(now_ms)  # 화면 조회도 같은 단조 시각 계약 사용
        if self.sample is None: return 'NO_DATA'  # 수신 전 상태
        return 'FRESH' if now_ms - self.sample.sampled_ms <= self.max_age_ms else 'STALE'  # 도착이 아니라 측정 시각에서 나이 계산

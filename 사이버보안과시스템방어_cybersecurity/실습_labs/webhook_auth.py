"""직접 작성한 교육 예제: HMAC 인증과 별도의 재전송 방지 상태를 대조합니다."""
import hashlib  # hashlib는 SHA-256 해시 함수를 제공합니다.
import hmac  # hmac는 비밀키 기반 메시지 인증과 태그 비교를 제공합니다.

def make_tag(key, timestamp, event_id, body):  # 송신자와 수신자가 공유할 정규 메시지를 만듭니다.
    if type(timestamp) is not int or timestamp < 0:  # type 검사는 bool 등 다른 자료형을 제외합니다.
        raise ValueError("invalid timestamp")  # 음수·비정수 시각을 거부합니다.
    if not isinstance(event_id, str) or not event_id.isascii() or not event_id.isalnum() or len(event_id) > 64:  # ID의 문자와 길이를 제한합니다.
        raise ValueError("invalid event id")  # 구분자를 포함한 ID를 인증 형식에 넣지 않습니다.
    message = b"event-v1\x00" + str(timestamp).encode("ascii") + b"\x00" + event_id.encode("ascii") + b"\x00" + body  # bytes와 구분자로 인증 범위를 고정합니다.
    return hmac.digest(key, message, hashlib.sha256)  # SHA-256 기반 HMAC 태그를 반환합니다.

def verify_once(key, timestamp, event_id, body, tag, now, seen):  # seen은 단일 프로세스 예제의 처리 완료 ID 집합입니다.
    if abs(now - timestamp) > 300:  # abs는 차이의 절댓값이며 ±300초의 예제 정책을 적용합니다.
        return False  # 허용 시간 밖의 메시지를 거부합니다.
    expected = make_tag(key, timestamp, event_id, body)  # 받은 헤더와 원시 본문으로 태그를 다시 계산합니다.
    if not hmac.compare_digest(expected, tag):  # 외부 태그는 전용 비교 함수로 대조합니다.
        return False  # 태그가 다르면 ID 상태를 바꾸지 않습니다.
    if event_id in seen:  # in은 이미 처리한 ID인지 확인합니다.
        return False  # 유효한 태그라도 재전송이면 거부합니다.
    seen.add(event_id)  # 인증된 새 ID만 처리 상태에 추가합니다.
    return True  # 이 예제에서 한 번의 수신을 승인합니다.

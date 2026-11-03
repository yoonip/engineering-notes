"""직접 작성한 교육 예제: 신뢰한 기준 해시와 받은 바이트의 일치 여부를 검사합니다."""
import hashlib  # hashlib는 표준 해시 알고리즘을 제공합니다.
import hmac  # compare_digest로 동일 자료형의 digest를 비교합니다.

def matches_pinned_digest(data, expected_hex):  # expected_hex는 별도 신뢰 경로에서 받은 64자리 SHA-256입니다.
    if not isinstance(expected_hex, str) or len(expected_hex) != 64:  # 기준 해시의 자료형과 길이를 확인합니다.
        return False  # 형식이 잘못됐으면 검사에 실패합니다.
    try:  # 잘못된 16진수 문자열 변환의 예외를 처리합니다.
        expected = bytes.fromhex(expected_hex)  # 클래스 메서드로 16진수 문자열을 바이트로 바꿉니다.
    except ValueError:  # 변환할 수 없는 문자가 있으면 이 분기를 실행합니다.
        return False  # 잘못된 기준을 정상 값으로 취급하지 않습니다.
    return len(expected) == 32 and hmac.compare_digest(hashlib.sha256(data).digest(), expected)  # and는 두 조건이 모두 맞아야 True를 반환합니다.

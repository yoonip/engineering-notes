# 암호와 키의 신뢰 | Cryptography and keys

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 비슷해 보이는 도구의 목적을 나눕니다

| 도구 | 무엇을 확인하거나 보호하나요 | 필요한 전제 |
| --- | --- | --- |
| SHA-256 해시 | 같은 바이트인지 비교합니다. | 기준 해시를 신뢰하는 경로가 필요합니다. |
| HMAC | 공유 비밀키를 가진 쪽이 인증한 메시지인지 확인합니다. | 양쪽이 키를 보호해야 하며 검증자도 태그를 만들 수 있습니다. |
| 전자서명 | 공개키에 대응하는 개인키로 서명했는지 검사합니다. | 공개키·인증서의 신뢰와 키 폐기 정책이 필요합니다. |
| 인증 암호, AEAD | 암호문 내용의 기밀성과 인증을 함께 제공합니다. | 선택한 알고리즘의 nonce·키 사용 규칙을 지켜야 합니다. |
| 비밀번호 해싱 | 유출된 검증값에서 비밀번호 추측의 비용을 높입니다. | salt·작업 비용·접근 제한·복구 경로도 관리합니다. |

nonce는 보통 한 키 아래에서 정해진 재사용 제한을 지켜야 하는 값입니다. AES-GCM의 nonce를 같은 키로 재사용하면 보안 전제가 깨집니다. 무작위 문자열을 아무 길이로나 붙이는 자체 암호 대신 검토된 라이브러리와 프로토콜을 사용합니다. [OWASP Cryptographic Storage의 알고리즘·키 관리 절](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

SHA-256은 빠르게 계산하도록 만든 해시이므로 비밀번호를 한 번 해싱하는 용도로는 적합하지 않습니다. salt는 사용자마다 다르게 저장하는 공개 난수로 같은 비밀번호의 검증값이 같아지는 것을 줄입니다. pepper는 DB와 분리해서 관리하는 비밀값입니다. Argon2id 같은 비밀번호 해싱은 메모리·계산 비용을 조절합니다. 비용값은 서버 용량과 로그인 부하를 재어 정하며 재해싱 정책도 필요합니다. [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## 태그가 맞아도 새 요청이라는 뜻은 아닙니다

은행 송신자가 인증한 ‘10원 지급’ 메시지를 두 번 처리하면 두 번째도 HMAC이 맞습니다. 메시지 인증과 재전송 방지는 별개입니다. 실습은 시각·이벤트 ID·원시 본문을 함께 인증하고 이미 처리한 ID를 따로 검사합니다. 실제 서비스에서는 ID의 유일성과 업무 처리를 DB 트랜잭션으로 연결해야 합니다.

이 예제의 `seen` 집합은 단일 프로세스 메모리입니다. 재시작하면 사라지고 여러 worker 사이에 공유되지 않습니다. ‘조회 후 추가’도 동시 요청에 대한 원자적 저장이 아닙니다. 따라서 분산 webhook 서버의 완성 구현으로 사용하지 않습니다. 허용 시간 ±300초는 이 실습의 가정이며 어떤 표준의 공통 권고값도 아닙니다. 비교 함수의 의미는 [Python hmac](https://docs.python.org/3.12/library/hmac.html)에 있습니다.

## 키의 생명주기

생성→배포→사용→교체→폐기를 설계합니다. 키 ID는 공개 식별자이고 키 자체가 아닙니다. 키를 바꿀 때는 전환 기간, 옛 키로 서명한 자료의 검증 기간, 유출 시 취소 범위를 정합니다. 개발·시험·운영 키와 서명·암호화 키의 용도도 분리합니다. KMS·HSM은 키 접근과 사용을 통제하는 수단이며 애플리케이션 권한 검사를 대신하지 않습니다.

읽기 과제는 ‘공격자가 파일과 해시를 함께 바꾸면 왜 검사가 통과하는가’입니다. [해시 실습](실습_labs/artifact_digest.py)의 통과 결과는 기준 자체를 신뢰하지 못할 때의 한계를 보여 줍니다. 암호 알고리즘의 충돌을 찾아 통과한 것이 아닙니다.

## 코드와 줄별 설명

공식 API·설계 원칙을 참고해 직접 작성한 교육 예제입니다. 기업의 내부 코드나 원문 발췌가 아닙니다. [실행 파일](실습_labs/webhook_auth.py) · [검사 방법과 결과](실습_labs/검증기록_validation.md)

```python
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
```

## 원문에서 이어 읽기

- [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html): 암호 선택·키 관리·인증 암호 절입니다.
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): 비밀번호 해싱·salt·Argon2id 절입니다.
- [Python hmac](https://docs.python.org/3.12/library/hmac.html): digest·compare_digest API입니다.
- [IETF RFC 4231](https://www.rfc-editor.org/rfc/rfc4231.html): §4.2 HMAC-SHA-256 시험 벡터1입니다.

## English

Hashes, MACs, signatures, encryption and password hashing serve different purposes. Authentication does not establish freshness or replay protection.

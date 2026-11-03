# 인증과 권한 검사 | Identity and access control

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 로그인과 자료 접근은 다른 검사입니다

인증(authentication)은 누구인지 확인하는 과정입니다. 인가·권한 검사(authorization)는 그 주체가 이 자료에 이 작업을 할 수 있는지 정하는 과정입니다. 로그인한 사용자가 URL의 ID를 바꿔 다른 고객의 문서를 읽는 문제는 인증 성공 이후의 권한 결함입니다.

세션·토큰을 검증한 서버 계층에서 사용자와 조직을 정해야 합니다. 클라이언트나 AI가 보낸 `user`, `tenant`, `role` 값을 그대로 주체로 쓰면 스스로 권한을 정하는 셈입니다. RBAC는 역할에 권한을 묶고, ABAC는 조직·기기·자원·작업 같은 속성을 검사하며, 관계 기반 정책은 소유자·공유 관계를 봅니다. 어떤 방식이든 객체별·요청별로 적용해야 합니다. [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

## 계정 탈취 경로를 나눕니다

| 경로 | 방어에서 확인할 사항 |
| --- | --- |
| 유출 비밀번호 재사용 | 재사용을 줄이고 속도 제한·이상 로그인 탐지·추가 인증을 적용합니다. |
| 가짜 로그인 페이지 | 서비스와 결합된 피싱 저항성 인증을 검토합니다. |
| 세션 쿠키·토큰 유출 | 저장·로그·전송·수명·철회와 민감 작업의 재인증을 다룹니다. |
| 계정 복구 악용 | 복구 경로가 주 인증보다 훨씬 약하지 않은지 확인합니다. |
| 과도한 서비스 계정 | 작업·대상·수명별로 권한을 줄이고 사용 기록을 남깁니다. |

패스키는 공개키 기반 인증을 사용하며, 올바른 구현에서는 서비스 식별자와 결합하여 가짜 사이트로의 자격증명 전달을 줄입니다. 모든 MFA가 피싱 저항성을 갖는 것은 아닙니다. OTP를 사용자가 가짜 사이트에 입력할 수 있는 방식과 서비스 결합형 인증은 구분해야 합니다. [NIST SP 800-63B-4의 피싱 저항성·인증기 관리 절](https://pages.nist.gov/800-63-4/sp800-63b.html)

## 실습의 권한 규칙

서버가 만든 `Principal`은 사용자·조직·scope를 가집니다. `scope`는 작업 권한의 범위이며 여기서는 `documents:read`입니다. 이 권한만 있어도 임의 문서를 읽을 수 있는 것은 아닙니다. 자료의 조직과 소유자를 추가로 확인합니다. 다른 고객·같은 조직의 다른 사용자·scope 없음·인증 없음·없는 ID를 각각 시험합니다.

`frozen=True`는 Python 객체 필드의 재대입을 막는 편의 기능입니다. 신뢰하지 않는 코드와 같은 프로세스에서 완전한 보안 경계를 만드는 장치는 아닙니다. 실습은 인증 프로토콜·세션 저장소·사용자 관리 기능을 구현하지 않았으며, 주체를 서버가 이미 검증했다는 가정 아래 객체 접근 검사만 다룹니다.

실무에서는 관리자를 단순 예외 처리로 뚫어 두지 말고 관리 작업을 따로 정의합니다. 권한을 회수했을 때 캐시와 장기 토큰에 언제 반영되는지, 백그라운드 작업이 어느 주체로 실행되는지도 검사해야 합니다.

## 코드와 줄별 설명

공식 API·설계 원칙을 참고해 직접 작성한 교육 예제입니다. 기업의 내부 코드나 원문 발췌가 아닙니다. [실행 파일](실습_labs/access_control.py) · [검사 방법과 결과](실습_labs/검증기록_validation.md)

```python
"""직접 작성한 교육 예제: 인증된 주체와 자료의 소속을 서버 측에서 대조합니다."""
from dataclasses import dataclass  # dataclass는 필드 중심의 클래스를 간단히 정의합니다.

@dataclass(frozen=True)  # 데코레이터가 생성 후 필드 재대입을 막는 자료형을 만듭니다.
class Principal:  # class는 인증 계층에서 전달할 주체 자료형을 정의합니다.
    user: str  # : str은 사용자 식별자의 타입 힌트입니다.
    tenant: str  # tenant는 조직·고객 사이의 자료 경계입니다.
    scopes: frozenset[str]  # frozenset은 변경할 수 없는 허용 작업 집합입니다.

def read_document(principal, document_id, documents):  # 서버가 보유한 자료에서 하나를 읽는 함수입니다.
    if not isinstance(principal, Principal):  # isinstance는 정해진 주체 자료형인지 검사합니다.
        raise PermissionError("authentication required")  # raise는 인증 실패 예외를 발생시킵니다.
    if "documents:read" not in principal.scopes:  # not in은 읽기 권한이 집합에 없는지 확인합니다.
        raise PermissionError("scope denied")  # 기본 거부 정책을 적용합니다.
    item = documents.get(document_id)  # dict.get은 ID가 없으면 None을 반환합니다.
    if item is None or item["tenant"] != principal.tenant or item["owner"] != principal.user:  # or는 존재·조직·소유자 중 하나라도 어긋나는지 검사합니다.
        raise PermissionError("document unavailable")  # 다른 고객의 자료와 없는 자료를 같은 예외로 처리합니다.
    return item["body"]  # 모든 조건이 맞은 자료 내용만 반환합니다.
```

## 원문에서 이어 읽기

- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): 최소권한·기본 거부·매 요청 검사 절입니다.
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html): 인증 보증·피싱 저항성·비밀번호·복구 관련 절입니다.

## English

Authentication establishes a principal; authorization checks that principal against the requested object and action. The example assumes an already authenticated server-side principal.

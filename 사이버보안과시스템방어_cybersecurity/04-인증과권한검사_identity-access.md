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

## 로그인 방어는 한 계정의 실패 횟수만 세지 않습니다

계정 공격은 관측되는 모양이 서로 다릅니다. 한 계정에 많은 후보를 넣는 시도는 계정별 제한에 드러나기 쉽지만, 같은 후보를 여러 계정에 나누어 넣는 password spraying은 계정별 기준을 피할 수 있습니다. 유출된 조합을 재사용하는 credential stuffing은 정상 사용자의 비밀번호 재사용이 원인에 포함됩니다. 따라서 탐지와 방어를 계정 하나의 실패 횟수에만 의존하지 않습니다. [MITRE ATT&CK의 비밀번호 공격 분류](https://attack.mitre.org/techniques/T1110/index.html)

속도 제한은 계정 잠금만으로 구현하면 공격자가 다른 사람의 계정을 잠가 서비스 거부를 만들 수 있습니다. 계정·출발 네트워크·기기·세션의 위험 신호를 결합하고, 도전 과제·추가 인증·알림·유출 비밀번호 검사 같은 대응을 위험에 맞게 선택합니다. 비정상 위치 하나만으로 탈취를 확정하지 말고 사용자 확인과 후속 조사 경로를 둡니다.

## 인증 수단과 계정 복구를 같은 생명주기로 관리합니다

| 단계 | 서버가 확인할 내용 | 남는 위험 |
| --- | --- | --- |
| 등록 | 신원 확인, 인증기 공개키 또는 비밀번호 검증값을 안전하게 저장합니다. | 최초 계정 탈취나 약한 본인 확인입니다. |
| 로그인 | 프로토콜·서비스 식별자·도전값·만료를 검증합니다. | 구현 오류, 피싱, 탈취된 세션입니다. |
| 세션 발급 | 목적·대상·수명·권한을 제한합니다. | 브라우저 저장소·로그·기기 탈취입니다. |
| 권한 변경 | 서버 정책으로 독립 승인하고 감사 기록을 남깁니다. | 관리 계정 오용·대리 권한입니다. |
| 복구·폐기 | 기존 세션 철회, 인증기 교체, 알림을 연결합니다. | 복구 절차가 주 인증보다 약한 경우입니다. |

패스키는 서비스 도메인과 결합된 공개키 인증이라 피싱 저항성에 도움을 주지만, 계정 복구·기기 동기화·세션 탈취·인가 결함까지 자동 해결하지는 않습니다. MFA도 방법마다 피싱 저항성이 다릅니다. 사용자의 입력을 가짜 사이트에 전달할 수 있는 코드와 서비스에 묶인 암호학적 인증을 구분합니다. [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)

## 원문에서 이어 읽기

- [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): 최소권한·기본 거부·매 요청 검사 절입니다.
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html): 인증 보증·피싱 저항성·비밀번호·복구 관련 절입니다.

## English

Authentication establishes a principal; authorization checks that principal against the requested object and action. The example assumes an already authenticated server-side principal.

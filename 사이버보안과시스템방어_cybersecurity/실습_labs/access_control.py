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

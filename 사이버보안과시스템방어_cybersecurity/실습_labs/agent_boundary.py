"""직접 작성한 교육 예제: 모델의 제안과 서버의 접근 통제를 분리하며 모델은 호출하지 않습니다."""
from access_control import read_document  # 같은 실습 폴더의 서버 측 권한 검사 함수를 가져옵니다.

def dispatch(principal, proposal, documents):  # principal은 서버 인증 계층이 정하며 proposal에서 읽지 않습니다.
    if type(proposal) is not dict or set(proposal) != {"tool", "arguments"}:  # set은 키 집합이며 알 수 없는 추가 필드를 거부합니다.
        raise ValueError("invalid proposal shape")  # 구조가 맞지 않는 제안은 실행하지 않습니다.
    if proposal["tool"] != "read_document":  # !=는 유일하게 허용한 도구 이름과 다른지 검사합니다.
        raise PermissionError("tool denied")  # shell·파일 쓰기·네트워크 전송 도구를 허용하지 않습니다.
    args = proposal["arguments"]  # []는 사전에서 해당 키의 값을 가져옵니다.
    if type(args) is not dict or set(args) != {"document_id"}:  # 인수도 정확히 한 필드만 허용합니다.
        raise ValueError("invalid argument shape")  # user·tenant 같은 권한 위조 필드를 받지 않습니다.
    document_id = args["document_id"]  # 모델이 제안한 ID를 별도 변수로 읽습니다.
    if type(document_id) is not str or not 1 <= len(document_id) <= 64:  # 연쇄 비교로 ID 길이를 제한합니다.
        raise ValueError("invalid document id")  # 잘못된 자료형이나 과도한 길이를 거부합니다.
    return read_document(principal, document_id, documents)  # 최종 허용 여부는 실제 서버의 권한 검사로 정합니다.

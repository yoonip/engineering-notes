"""합성 자료의 독립 기대값으로 방어 경계와 잘못된 대조군을 검사합니다."""
import hashlib  # 표준 SHA-256 구현을 시험 자료 준비에 사용합니다.
import hmac  # RFC 4231의 공개 HMAC 시험 벡터를 계산합니다.
import unittest  # 표준 단위검사와 assertion을 사용합니다.
from access_control import Principal, read_document  # 검사할 주체 자료형과 권한 함수를 가져옵니다.
from agent_boundary import dispatch  # 모델 제안 처리 경계를 가져옵니다.
from artifact_digest import matches_pinned_digest  # 기준 해시 대조 함수를 가져옵니다.
from login_detection import failure_alerts  # 합성 로그의 시간창 검사를 가져옵니다.
from output_encoding import render_message  # HTML 본문 출력을 가져옵니다.
from sql_boundary import fixture, unsafe_lookup, bound_lookup  # SQL의 정상·오류 대조군을 가져옵니다.
from webhook_auth import make_tag, verify_once  # 인증 태그와 재전송 방지를 가져옵니다.

DOCS = {"d1": {"tenant": "org1", "owner": "alice", "body": "A"}, "d2": {"tenant": "org2", "owner": "bob", "body": "B"}}  # 합성 자료이며 실제 개인정보가 없습니다.
ALICE = Principal("alice", "org1", frozenset({"documents:read"}))  # 서버가 인증했다고 가정한 읽기 주체입니다.

class SqlTests(unittest.TestCase):  # TestCase를 상속해 SQL 경계를 검사합니다.
    def setUp(self):  # 각 검사 전에 새 메모리 DB를 만듭니다.
        self.db = fixture()  # 객체의 db 속성에 연결을 보관합니다.
        self.addCleanup(self.db.close)  # 검사 실패 시에도 DB 연결을 닫습니다.

    def test_normal(self):  # 정상 소유자 검색의 독립 기대값입니다.
        self.assertEqual(bound_lookup(self.db, "alice"), [("A",)])  # alice의 A만 반환해야 합니다.

    def test_bad_query_reproduces_extra_rows(self):  # 오류 대조군의 실제 결과를 확인합니다.
        self.assertEqual(unsafe_lookup(self.db, "' OR 1=1 --"), [("A",), ("B",)])  # 구문으로 해석되면 두 행이 나옵니다.

    def test_same_input_remains_data(self):  # 같은 입력을 수정된 함수에 넣습니다.
        self.assertEqual(bound_lookup(self.db, "' OR 1=1 --"), [])  # 입력과 같은 이름의 사용자는 없습니다.

    def test_quote_is_valid_data(self):  # 아포스트로피가 있는 정상 입력을 거부하지 않아야 합니다.
        self.db.execute("INSERT INTO notes VALUES (?, ?)", ("O'Neil", "C"))  # 바인딩으로 정상 이름을 넣습니다.
        self.assertEqual(bound_lookup(self.db, "O'Neil"), [("C",)])  # 따옴표를 삭제하지 않고 정확히 검색합니다.

class AccessTests(unittest.TestCase):  # 권한별 기대 결과를 검사합니다.
    def test_owner(self):  # 조직·소유자·scope가 모두 맞는 경우입니다.
        self.assertEqual(read_document(ALICE, "d1", DOCS), "A")  # 허용 결과는 A입니다.

    def test_other_tenant(self):  # 타 조직 ID를 추측한 경우입니다.
        with self.assertRaises(PermissionError):  # 지정 예외가 발생해야 통과합니다.
            read_document(ALICE, "d2", DOCS)  # bob 자료는 반환하면 안 됩니다.

    def test_same_tenant_other_owner(self):  # 같은 조직이어도 소유자가 다른 경우입니다.
        with self.assertRaises(PermissionError):  # 조직 일치만으로 허용하지 않습니다.
            read_document(Principal("eve", "org1", ALICE.scopes), "d1", DOCS)  # eve는 소유자가 아닙니다.

    def test_scope_missing(self):  # 읽기 scope가 없는 경우입니다.
        with self.assertRaises(PermissionError):  # 권한 실패가 기대 결과입니다.
            read_document(Principal("alice", "org1", frozenset()), "d1", DOCS)  # 빈 집합에는 읽기 권한이 없습니다.

    def test_no_authentication(self):  # 인증되지 않은 요청입니다.
        with self.assertRaises(PermissionError):  # 문자열 user 파라미터를 인증으로 취급하지 않습니다.
            read_document(None, "d1", DOCS)  # None에는 인증된 주체가 없습니다.

    def test_missing_id(self):  # 존재하지 않는 ID를 읽는 경우입니다.
        with self.assertRaises(PermissionError):  # 자료가 없더라도 동일한 거부가 나옵니다.
            read_document(ALICE, "absent", DOCS)  # 임의의 ID를 입력합니다.

class WebhookTests(unittest.TestCase):  # 태그와 최신성의 독립 조건을 검사합니다.
    def setUp(self):  # 검사마다 공개된 예제 키·시각·본문을 준비합니다.
        self.key, self.now, self.body = b"not-a-secret-test-key", 1000, b"amount=10"  # 운영 비밀이 아닌 시험 자료입니다.
        self.tag = make_tag(self.key, self.now, "event1", self.body)  # 정해진 형식의 태그를 계산합니다.

    def test_rfc4231_vector(self):  # 공식 RFC의 독립 정답과 HMAC 구현을 대조합니다.
        actual = hmac.digest(bytes.fromhex("0b" * 20), b"Hi There", "sha256").hex()  # RFC 4231 시험 1의 키와 메시지입니다.
        self.assertEqual(actual, "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")  # 공개 시험 벡터의 32바이트 결과입니다.

    def test_first_then_replay(self):  # 같은 유효 메시지를 두 번 보냅니다.
        seen = set()  # 아직 처리한 ID가 없습니다.
        self.assertTrue(verify_once(self.key, 1000, "event1", self.body, self.tag, 1000, seen))  # 첫 수신은 허용합니다.
        self.assertFalse(verify_once(self.key, 1000, "event1", self.body, self.tag, 1000, seen))  # 재수신은 거부합니다.

    def test_body_tamper(self):  # 본문을 바꾼 입력입니다.
        self.assertFalse(verify_once(self.key, 1000, "event1", b"amount=99", self.tag, 1000, set()))  # 태그 검사가 실패합니다.

    def test_identity_tamper(self):  # 이벤트 ID를 바꾼 입력입니다.
        self.assertFalse(verify_once(self.key, 1000, "event2", self.body, self.tag, 1000, set()))  # 본문이 같아도 거부합니다.

    def test_time_tamper(self):  # 인증에 포함된 시각을 바꿉니다.
        self.assertFalse(verify_once(self.key, 1001, "event1", self.body, self.tag, 1001, set()))  # 시간창 안이어도 태그가 다릅니다.

    def test_wrong_key(self):  # 수신 키가 잘못된 경우입니다.
        self.assertFalse(verify_once(b"other", 1000, "event1", self.body, self.tag, 1000, set()))  # 키가 다르면 인증할 수 없습니다.

    def test_time_boundaries(self):  # 허용 시간창의 양끝과 바로 바깥을 검사합니다.
        for now, expected in [(700, True), (1300, True), (699, False), (1301, False)]:  # 표의 값이 독립 기대값입니다.
            with self.subTest(now=now):  # 각 입력의 실패를 구별합니다.
                self.assertEqual(verify_once(self.key, 1000, "event1", self.body, self.tag, now, set()), expected)  # 상태는 입력마다 새로 만듭니다.

    def test_rejected_tag_does_not_poison_seen(self):  # 거부된 메시지는 ID를 소비하지 않아야 합니다.
        seen = set()  # 비어 있는 상태를 준비합니다.
        self.assertFalse(verify_once(self.key, 1000, "event1", self.body, b"x" * 32, 1000, seen))  # 거짓 태그를 먼저 넣습니다.
        self.assertEqual(seen, set())  # 처리 상태는 그대로여야 합니다.

    def test_delimiter_id_rejected(self):  # 메시지 경계를 흐리는 ID를 검사합니다.
        with self.assertRaises(ValueError):  # 형식 검사의 예외가 기대값입니다.
            make_tag(self.key, 1000, "bad\x00id", self.body)  # NUL을 ID에 넣을 수 없습니다.

class OutputDigestTests(unittest.TestCase):  # 출력 문맥과 신뢰 기준을 검사합니다.
    def test_html_text(self):  # HTML 태그로 해석될 입력입니다.
        self.assertEqual(render_message('<img src=x>'), '<p>&lt;img src=x&gt;</p>')  # 실제 태그 대신 문자 표현을 출력합니다.

    def test_plain_text(self):  # 정상 한국어와 & 기호를 검사합니다.
        self.assertEqual(render_message('안녕 & hello'), '<p>안녕 &amp; hello</p>')  # 텍스트는 유지하고 &만 변환합니다.

    def test_known_sha256(self):  # abc의 널리 알려진 독립 SHA-256 값입니다.
        self.assertTrue(matches_pinned_digest(b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"))  # 기준과 내용이 같습니다.

    def test_tampered_data(self):  # 기준을 유지하고 자료만 바꿉니다.
        self.assertFalse(matches_pinned_digest(b"abd", hashlib.sha256(b"abc").hexdigest()))  # 변조를 탐지합니다.

    def test_untrusted_reference_also_changes(self):  # 기준까지 바뀌면 단순 해시 검사가 통과함을 보입니다.
        self.assertTrue(matches_pinned_digest(b"replacement", hashlib.sha256(b"replacement").hexdigest()))  # 이것은 배포자 인증의 증거가 아닙니다.

    def test_invalid_digest(self):  # 비정상 기준값을 거부합니다.
        for value in [None, "", "g" * 64, "ab" * 31, " " * 64]:  # 형식별 독립 입력입니다.
            with self.subTest(value=value):  # 각 경계 사례를 따로 식별합니다.
                self.assertFalse(matches_pinned_digest(b"abc", value))  # 모두 False여야 합니다.

class AgentTests(unittest.TestCase):  # 제안은 권한이 아니라는 조건을 검사합니다.
    def proposal(self, doc="d1"):  # 기본 허용 제안을 만드는 검사 도우미입니다.
        return {"tool": "read_document", "arguments": {"document_id": doc}}  # 실행할 코드를 보내지 않습니다.

    def test_allowed(self):  # 인증 주체의 문서 읽기입니다.
        self.assertEqual(dispatch(ALICE, self.proposal(), DOCS), "A")  # A만 읽습니다.

    def test_cross_tenant(self):  # 모델이 다른 고객의 ID를 제안한 경우입니다.
        with self.assertRaises(PermissionError):  # 서버가 거부해야 합니다.
            dispatch(ALICE, self.proposal("d2"), DOCS)  # 모델의 설득 문구와 무관하게 거부합니다.

    def test_unknown_tool(self):  # 허용 목록에 없는 도구입니다.
        with self.assertRaises(PermissionError):  # 모르는 도구는 기본 거부합니다.
            dispatch(ALICE, {"tool": "shell", "arguments": {}}, DOCS)  # 어떤 shell도 실행되지 않습니다.

    def test_forged_identity(self):  # 모델이 주체를 바꾸려는 필드를 넣습니다.
        p = self.proposal()  # 정상 제안을 복사해 만듭니다.
        p["arguments"]["tenant"] = "org2"  # 인수에 허용되지 않은 필드를 추가합니다.
        with self.assertRaises(ValueError):  # 추가 필드가 있으면 스키마 검사를 실패해야 합니다.
            dispatch(ALICE, p, DOCS)  # 인증 주체는 ALICE 그대로입니다.

    def test_extra_top_key(self):  # 최상위에서도 임의 필드를 거부합니다.
        p = dict(self.proposal(), approved=True)  # 모델의 자체 승인 표기를 추가합니다.
        with self.assertRaises(ValueError):  # 자체 승인을 허용하지 않습니다.
            dispatch(ALICE, p, DOCS)  # 서버 정책만 사용합니다.

    def test_bad_id_type(self):  # 배열을 ID로 보내는 입력입니다.
        with self.assertRaises(ValueError):  # 자료형 오류를 명시적으로 거부합니다.
            dispatch(ALICE, self.proposal(["d1"]), DOCS)  # 잘못된 ID를 DB 조회까지 보내지 않습니다.

    def test_large_id(self):  # ID 길이 상한을 넘는 경우입니다.
        with self.assertRaises(ValueError):  # 길이 제한을 확인합니다.
            dispatch(ALICE, self.proposal("x" * 65), DOCS)  # 64자를 넘습니다.

class DetectionTests(unittest.TestCase):  # 합성 정수 시각으로 시간창을 검사합니다.
    def event(self, time, account="alice", result="failure"):  # 합성 로그 한 건을 만드는 함수입니다.
        return {"time": time, "account": account, "result": result}  # 실제 IP나 개인정보가 없습니다.

    def test_threshold(self):  # 60초 안의 실패 세 번입니다.
        self.assertEqual(failure_alerts([self.event(t) for t in [0, 10, 20]]), [("alice", 20, 3)])  # 20초에 처음 경보가 납니다.

    def test_exact_window_expires(self):  # 왼쪽 경계의 오래된 사건은 빠집니다.
        self.assertEqual(failure_alerts([self.event(t) for t in [0, 30, 60]]), [])  # 60초 시점에 0초는 시간창 밖입니다.

    def test_accounts_do_not_mix(self):  # 서로 다른 계정의 실패를 섞지 않습니다.
        self.assertEqual(failure_alerts([self.event(0), self.event(1, "bob"), self.event(2)]), [])  # alice 2회·bob 1회입니다.

    def test_success_is_not_failure(self):  # 성공은 실패 횟수에 더하지 않습니다.
        self.assertEqual(failure_alerts([self.event(0), self.event(1, result="success"), self.event(2)]), [])  # 실패는 두 번입니다.

    def test_out_of_order(self):  # 정렬 계약을 어긴 로그입니다.
        with self.assertRaises(ValueError):  # 순서 오류가 나야 합니다.
            failure_alerts([self.event(2), self.event(1)])  # 시각이 뒤로 갑니다.

    def test_invalid_settings(self):  # 임계값이 0이면 검사 자체가 무의미합니다.
        with self.assertRaises(ValueError):  # 설정 오류를 반환합니다.
            failure_alerts([], threshold=0)  # 빈 로그라도 잘못된 설정을 거부합니다.

if __name__ == "__main__":  # 직접 실행할 때 검사 모음을 실행합니다.
    unittest.main()  # 실패는 0이 아닌 종료 코드로 보고합니다.

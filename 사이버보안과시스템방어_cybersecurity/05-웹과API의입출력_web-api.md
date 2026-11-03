# 웹과 API의 입출력 | Web and API security

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 입력 검사는 실행 문맥과 함께 봅니다

SQL injection은 입력값이 DB 명령의 문법으로 해석되는 문제입니다. 따옴표를 지우는 임시 처리보다 매개변수 바인딩으로 구문과 값을 분리합니다. 테이블명·정렬 열처럼 값 바인딩을 할 수 없는 위치는 서버가 정한 허용 목록에서 고릅니다. [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

메모리 DB 실습에서 정상 입력 `alice`는 A를 반환합니다. 잘못된 문자열 결합 검색은 특수 입력을 조건식으로 받아 A·B를 반환합니다. 수정한 검색은 같은 문자열을 사용자 이름 하나로 취급해 빈 결과를 반환합니다. 정상 이름 `O'Neil`도 유지하므로 단순 문자 삭제와 다릅니다. 단, 입력 바인딩만으로 인증·권한 결함까지 해결되지는 않습니다.

## 브라우저에 출력하는 위치가 중요합니다

XSS는 공격자가 제어한 내용이 브라우저의 실행 문맥으로 넘어가는 문제입니다. HTML 본문, 속성값, URL, JavaScript는 필요한 처리가 다릅니다. 실습의 `html.escape`는 일반 문자열을 `<p>`의 텍스트로 출력하는 경우만 다룹니다. script 내용·위험한 URL 스킴·허용 HTML 편집기의 정화 문제를 이 함수 하나로 처리하지 않습니다. [OWASP XSS Prevention의 문맥별 인코딩 절](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html), [Python html.escape](https://docs.python.org/3.12/library/html.html)

| 결함 | 왜 성립하나요 | 설계·검사 지점 |
| --- | --- | --- |
| 객체 권한 누락 | ID를 알면 자료를 반환합니다. | 모든 API에서 주체·객체·행위·조직을 대조합니다. |
| CSRF | 브라우저가 자동 첨부하는 인증으로 원치 않는 변경을 요청합니다. | CSRF 토큰·Origin 검사·쿠키 정책을 서비스 흐름에 맞게 적용합니다. |
| SSRF | 서버의 URL 요청 권한을 외부 입력이 이용합니다. | 목적지·주소·리디렉션·네트워크 출구를 함께 제한합니다. |
| 경로 이탈 | 파일 이름 입력이 허용 디렉터리 밖을 가리킵니다. | 파일 ID 매핑·권한·원자적 파일 열기를 설계합니다. |
| 업로드 오용 | 확장자·내용·실행 위치의 의미가 다릅니다. | 크기 제한·내용 판정·실행 불가 저장소·검사 흐름을 둡니다. |
| 자원 고갈 | 작은 요청도 큰 쿼리·압축 해제·생성 비용을 유발합니다. | 시간·메모리·응답량·사용자별 비용에 상한을 둡니다. |

## 목록을 제품 검사로 바꾸는 방법

OWASP Top 10:2025는 위험 인식을 위한 대표 범주이며 모든 검증 요구사항의 대체물은 아닙니다. 인증·입력·출력·세션·오류·암호·API의 구체 요구는 ASVS와 실제 설계에서 정합니다. [Top 10:2025](https://top10.owasp.org/2025/), [ASVS](https://owasp.org/www-project-application-security-verification-standard/)

예약 API의 동시 중복 요청처럼 문법적으로 올바른 요청도 사업 규칙을 깰 수 있습니다. 수정 후에는 정상 흐름, 경계값, 동시 요청, 다른 계정·조직, 수정 전 재현 입력을 함께 검사합니다. 오류 응답에는 내부 쿼리·토큰·개인정보가 섞이지 않게 하고 서버의 조사 로그와 사용자 메시지를 구분합니다.

## 코드와 줄별 설명

공식 API·설계 원칙을 참고해 직접 작성한 교육 예제입니다. 기업의 내부 코드나 원문 발췌가 아닙니다. [실행 파일](실습_labs/sql_boundary.py) · [검사 방법과 결과](실습_labs/검증기록_validation.md)

```python
"""직접 작성한 교육 예제: 메모리 DB에서 SQL 구문과 입력값의 경계를 비교합니다."""
import sqlite3  # import는 SQLite 메모리 DB를 다루는 표준 모듈을 불러옵니다.

def fixture():  # def는 매번 같은 합성 자료를 준비하는 함수를 정의합니다.
    db = sqlite3.connect(":memory:")  # :memory:는 디스크 파일 없이 DB를 만듭니다.
    db.execute("CREATE TABLE notes (owner TEXT, body TEXT)")  # 고정된 SQL로 두 열을 정의합니다.
    db.executemany("INSERT INTO notes VALUES (?, ?)", [("alice", "A"), ("bob", "B")])  # ?에 각 튜플의 값을 바인딩합니다.
    return db  # return은 준비된 DB 연결을 돌려줍니다.

def unsafe_lookup(db, owner):  # 이 함수는 입력을 SQL 구문에 합치는 잘못된 대조군입니다.
    return db.execute(f"SELECT body FROM notes WHERE owner = '{owner}'").fetchall()  # f 문자열이 입력을 쿼리 문법으로 해석하게 만듭니다.

def bound_lookup(db, owner):  # 이 함수는 같은 검색을 매개변수 바인딩으로 수행합니다.
    return db.execute("SELECT body FROM notes WHERE owner = ?", (owner,)).fetchall()  # (owner,)는 한 원소 튜플이며 입력은 값으로 전달됩니다.

if __name__ == "__main__":  # 파일을 직접 실행한 경우에만 예제를 출력합니다.
    connection = fixture()  # 합성 사용자 둘의 메모리 DB를 만듭니다.
    try:  # finally와 짝을 이뤄 예외가 나도 연결을 닫습니다.
        value = "' OR 1=1 --"  # 외부 시스템에 보내지 않는 로컬 오류 재현 문자열입니다.
        print("unsafe", unsafe_lookup(connection, value))  # 잘못된 검색은 A·B 두 행을 반환합니다.
        print("bound", bound_lookup(connection, value))  # 바인딩 검색은 일치하는 소유자가 없어 빈 목록을 반환합니다.
    finally:  # 성공 여부와 관계없이 정리합니다.
        connection.close()  # 메모리 DB 연결을 닫습니다.
```

## 원문에서 이어 읽기

- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html): 매개변수 쿼리·허용 목록 절입니다.
- [Python sqlite3](https://docs.python.org/3.12/library/sqlite3.html): 매개변수 바인딩·메모리 DB API입니다.
- [OWASP Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html): 출력 문맥·인코딩·safe sinks 절입니다.
- [Python html](https://docs.python.org/3.12/library/html.html): escape의 동작과 quote 인수입니다.
- [OWASP Top 10:2025](https://top10.owasp.org/2025/): 정식 목록·각 위험 범주의 명칭입니다.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 검증 요구사항·판본·프로젝트 목적입니다.

## English

Separate SQL structure from values and encode output for its actual context. The local examples cover query binding and plain HTML text, not every web risk.

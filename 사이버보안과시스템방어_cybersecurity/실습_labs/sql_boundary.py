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

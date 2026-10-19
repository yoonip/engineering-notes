# SQLite WAL의 동시 접근 | Reviewing SQLite WAL behavior

SQLite는 프로그램 안에서 사용하는 관계형 데이터베이스 엔진입니다. 별도 DB 서버 없이 파일을 사용할 수 있어 로컬 분석 도구와 장치 기록에 적합한 경우가 있습니다. 여기서는 제품의 동시 접근 동작을 두 연결로 확인합니다. Python 3.12.14에 연결된 SQLite 3.53.1을 2026-10-19에 실행했습니다.

## 비교할 동작

공식 [WAL 안내](https://www.sqlite.org/wal.html#concurrency)는 읽기와 쓰기가 겹쳐 진행될 수 있다고 설명합니다. 동시에 진행할 수 있는 쓰기 트랜잭션은 하나입니다. WAL은 수정 내용을 로그에 추가하므로 독자는 자신이 읽기 시작한 시점의 내용을 계속 볼 수 있습니다. [격리 설명](https://www.sqlite.org/isolation.html)은 이러한 snapshot과 새 트랜잭션의 차이를 설명합니다.

직접 만든 실험에서는 값 10을 저장하고 A 연결이 읽기 트랜잭션을 시작합니다. 이어 B 연결에서 값을 20으로 바꿔 commit을 시도합니다. A는 같은 트랜잭션에서 다시 읽고, 이를 끝낸 뒤 새로 읽습니다. 대기 시간을 0으로 두어 잠금 충돌을 즉시 관찰합니다.

| 관찰 | DELETE journal | WAL |
| --- | --- | --- |
| A의 첫 읽기 | 10 | 10 |
| A가 읽는 동안 B의 commit | `SQLITE_BUSY`, B를 rollback합니다. | 성공합니다. |
| A의 같은 트랜잭션 읽기 | 10 | 10 |
| A가 끝낸 뒤 새로 읽기 | 10 | 20 |

DELETE 모드의 마지막 값이 10인 이유는 실패한 B의 변경을 실험에서 rollback했기 때문입니다. WAL에서 같은 읽기가 계속 10인 것은 갱신 실패가 아니라 snapshot 유지입니다. A가 트랜잭션을 끝내고 다시 읽으면 B가 commit한 20을 확인합니다.

## 사용 판단

읽기와 쓰기를 겹치게 해야 하는 로컬 도구라면 WAL을 검토할 이유가 있습니다. 다만 동시 작성자 수를 무제한으로 늘려 주지는 않습니다. 긴 읽기 트랜잭션은 checkpoint 진행을 지연시킬 수 있으므로 처리 후 트랜잭션을 오래 열어 두지 않는 것이 중요합니다. WAL의 공유 메모리 조건 때문에 네트워크 파일시스템을 여러 호스트가 공유하는 구성에도 맞지 않습니다. 이 조건들은 [공식 WAL 문서](https://www.sqlite.org/wal.html)에 명시되어 있습니다.

단순히 journal 모드를 바꾸는 일과 애플리케이션의 오류 처리는 별도입니다. `SQLITE_BUSY`를 만났을 때 재시도할지, 사용자에게 알릴지, 작업을 취소할지는 트랜잭션의 의미에 맞춰 정해야 합니다. 한 건을 두 번 기록해도 되는지 같은 질문은 DB 설정만으로 해결되지 않습니다.

## 재실행과 범위

저장소 루트에서 `python 제품리뷰_reviews/sqlite_concurrency.py`를 실행합니다. [코드](sqlite_concurrency.py)는 임시 파일을 만들고 두 모드의 관찰값을 검사한 뒤 파일을 정리합니다. [원시 결과](sqlite_result.json)에는 실제 Python·SQLite 버전과 설정이 있습니다. Python API의 동작은 해당 실행 버전의 [sqlite3 문서](https://docs.python.org/3.12/library/sqlite3.html)를 함께 확인하실 수 있습니다.

이 실험은 연결 두 개의 동작 확인입니다. 처리량, 전원 차단 내구성, 여러 프로세스의 장시간 부하는 측정하지 않았으므로 그 성능을 비교하는 자료로 사용하지 않습니다. 더 자세한 상태 분석은 [WAL snapshot 해설](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md)에 있습니다.

## English

Two connections observe a single stored value. A reader holds a transaction while a writer changes 10 to 20. With a zero timeout, DELETE mode returns SQLITE_BUSY and the writer is rolled back. WAL commits successfully, while the existing reader still sees 10 and a new read transaction sees 20. This is a behavioral check on SQLite 3.53.1, not a throughput or crash-durability benchmark. WAL allows reader/writer overlap but retains a single writer and checkpoint considerations.

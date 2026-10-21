# 데이터베이스와 데이터 공학 | Databases & Data Engineering

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

데이터베이스는 데이터를 저장하는 기능과 함께 질의·동시 접근·무결성·복구를 제공합니다. 데이터 엔지니어링은 수집부터 변환·검증·저장·전달까지 이어지는 흐름을 만듭니다.

## SQL과 실행 계획

관계형 모델은 표와 관계를 사용합니다. Index는 조회를 빠르게 할 수 있지만 저장 공간과 쓰기 비용이 추가됩니다. Transaction은 여러 연산을 하나의 논리 작업으로 다루며 isolation 수준에 따라 동시 실행에서 관찰되는 현상이 달라집니다. Query plan은 데이터 접근과 join이 어떤 순서와 방식으로 실행되는지 보여줍니다.

SQLite는 파일 기반의 내장형 데이터베이스, PostgreSQL·MySQL은 서버형 관계형 데이터베이스, DuckDB는 분석 질의, Redis는 메모리 기반 데이터 구조에 자주 쓰입니다. CSV는 단순 교환, Parquet는 columnar 저장, Arrow는 메모리 내 데이터 교환과 관련됩니다.

## 파이프라인과 검색

Batch는 모인 데이터를 묶어 처리하고 streaming은 계속 들어오는 이벤트를 다룹니다. Spark·Kafka는 대규모 데이터 처리와 이벤트 전달에 쓰입니다. 결측·중복·단위·시간대·schema 변화가 분석 결과에 영향을 줍니다. FAISS·pgvector는 벡터 유사도 검색에 쓰이며 유사도 점수 자체가 내용의 사실성을 보장하지는 않습니다.

## 관련 기술

SQLite, PostgreSQL, MySQL, DuckDB, Redis, Parquet, Arrow, Spark, Kafka, FAISS, pgvector

## 참고 자료

- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html)

## 기초 해설

- [DB의 인덱스, 트랜잭션, SQL 집계](해설_notes/DB의인덱스트랜잭션SQL집계_indexes-transactions-and-aggregation.md)

## 한 문장의 실패와 업무 전체의 취소

창고 A와 B의 재고가 각각 50개이며, 이 학습 예에서는 창고별 상한을 60개로 정합니다. A에서 30개를 빼고 B에 30개를 더하려 하면 B의 80개가 상한을 위반합니다. 두 UPDATE를 별도로 확정하면 첫 차감만 남아 총재고가 100에서 70으로 줄어듭니다. 트랜잭션으로 묶고 오류 때 전체를 되돌리면 50·50을 유지합니다.

아래 코드는 Python 표준 라이브러리의 실제 SQLite 엔진을 사용합니다. `:memory:`는 이 연결 안의 메모리 DB이며 파일이나 전원 차단 복구 시험이 아닙니다. `isolation_level=None`에서는 암묵적으로 트랜잭션을 시작하지 않으므로 BEGIN·COMMIT·ROLLBACK을 직접 실행합니다. [Python 3.12의 트랜잭션 제어](https://docs.python.org/3.12/library/sqlite3.html#transaction-control-via-the-isolation-level-attribute)

```python
import sqlite3  # import는 표준 라이브러리의 SQLite 연결 기능을 불러옵니다.
def transfer(atomic):  # def는 두 UPDATE를 묶을지 인수로 받는 함수를 정의합니다.
    db = sqlite3.connect(":memory:", isolation_level=None)  # 메모리 DB를 열고 암묵적 BEGIN을 끕니다.
    db.execute("CREATE TABLE stock(id INTEGER PRIMARY KEY, qty INTEGER CHECK(qty BETWEEN 0 AND 60))")  # CHECK는 재고 범위를 제한합니다.
    db.executemany("INSERT INTO stock VALUES(?, ?)", [(1, 50), (2, 50)])  # ? 자리에 tuple의 값을 바인딩합니다.
    if atomic:  # if는 업무 전체를 하나로 묶는 경로만 선택합니다.
        db.execute("BEGIN")  # BEGIN은 명시적인 트랜잭션을 시작합니다.
    try:  # try는 제약 위반이 날 수 있는 두 변경을 실행합니다.
        db.execute("UPDATE stock SET qty = qty - 30 WHERE id = 1")  # A를 50에서 20으로 줄입니다.
        db.execute("UPDATE stock SET qty = qty + 30 WHERE id = 2")  # B의 80이 CHECK를 위반합니다.
        if atomic:  # 두 변경이 성공했을 때만 확정할 경로입니다.
            db.execute("COMMIT")  # COMMIT은 묶인 변경을 확정합니다.
    except sqlite3.IntegrityError:  # except는 범위 등 무결성 제약 위반을 처리합니다.
        if db.in_transaction:  # 속성은 되돌릴 열린 트랜잭션이 있는지 나타냅니다.
            db.execute("ROLLBACK")  # 앞서 성공한 차감까지 함께 취소합니다.
    rows = db.execute("SELECT id, qty FROM stock ORDER BY id").fetchall()  # 순서를 정해 모든 결과 행을 가져옵니다.
    db.close()  # close는 연결을 닫습니다.
    return rows  # return은 행의 리스트를 호출한 곳에 돌려줍니다.
print(transfer(False))  # [(1, 20), (2, 50)]로 앞의 차감이 남습니다.
print(transfer(True))  # [(1, 50), (2, 50)]로 업무 전체가 취소됩니다.
```

SQLite의 기본 ABORT 처리는 실패한 문장의 변경을 취소하지만 앞 문장의 변경까지 자동 취소하는 처리는 아닙니다. 이 예에서는 CHECK 오류를 잡은 뒤 명시적으로 ROLLBACK하므로 첫 차감도 취소됩니다. 오류를 잡고 무조건 COMMIT하면 같은 보호가 사라집니다. [SQLite의 충돌 처리](https://www.sqlite.org/lang_conflict.html)

## 트랜잭션 경계와 복구 근거

원자성은 여러 변경을 전부 반영하거나 전부 취소하는 성질입니다. 영속성은 확정된 변경을 장애 뒤에도 보존하는 성질입니다. 위 메모리 DB에서 전체 취소를 확인한 사실만으로 저장장치 전원 오류에서의 영속성을 확인한 것은 아닙니다. 파일의 동기화·장치 캐시·기록 순서와 실제 복구 경로가 추가로 필요합니다.

SQLite의 [원자적 commit 설명](https://www.sqlite.org/atomiccommit.html)은 rollback journal을 만드는 방식이며, [WAL](https://www.sqlite.org/wal.html)은 다른 기록·확정·checkpoint 절차를 사용합니다. 두 형식을 섞어 설명하지 않습니다. [중단된 저널의 트랜잭션 복구](../../설계와검증사례_engineering-cases/중단된저널의트랜잭션복구_storage-journal-recovery.md)는 직접 정의한 별도 형식의 파일·프로세스 실험입니다. SQLite 파일 형식을 구현한 것으로 취급하지 않습니다.

## English

### Databases and data engineering

Databases provide queries, concurrent access, integrity, and recovery alongside data storage. Data engineering connects collection, transformation, validation, storage, and delivery into a pipeline.

### SQL and query plans

The relational model represents data through tables and relationships. An index can speed up reads at the cost of storage and additional work on writes. A transaction groups operations into a logical unit; its isolation level affects what concurrent transactions can observe. A query plan shows how data access and joins will execute.

SQLite is an embedded, file-based database. PostgreSQL and MySQL are server-based relational databases, DuckDB supports analytical queries, and Redis provides in-memory data structures. CSV is used for simple data exchange, Parquet for columnar storage, and Arrow for in-memory data interchange.

### Pipelines and search

Batch processing works on accumulated data, while streaming handles incoming events continuously. Spark and Kafka support large-scale processing and event delivery. Missing values, duplicates, units, time zones, and schema changes affect analysis. FAISS and pgvector support vector-similarity search, but a similarity score does not establish whether the retrieved content is factually correct.

### Foundation article

- [DB의 인덱스, 트랜잭션, SQL 집계](해설_notes/DB의인덱스트랜잭션SQL집계_indexes-transactions-and-aggregation.md#english)


### Statement failure and transaction rollback

The runnable SQLite example gives two warehouses 50 items each and an assumed capacity of 60. Removing 30 from one and adding 30 to the other fails the destination CHECK. Separate statement commits leave 20 and 50; explicit BEGIN and rollback on error preserve 50 and 50. SQLite's default ABORT cancels the failed statement rather than every earlier statement. The connection uses explicit SQL transaction control.

This real SQLite in-memory execution demonstrates an application transaction boundary, not file recovery or power-loss durability. SQLite rollback journals, SQLite WAL and the separately defined file-journal example have different formats and commit rules. Atomicity and persistence require distinct evidence.


## 심화 해설 | Advanced article

- [SQLite WAL에서 snapshot과 낙관적 갱신을 관찰하기](해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md) · [English](해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md#english)

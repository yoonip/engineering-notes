# SQLite WAL에서 snapshot과 낙관적 갱신을 관찰하기

[실제 DB 실행 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 트랜잭션 두 개가 같은 값을 읽었을 때

한 요청이 값을 읽고 계산하는 사이에 다른 요청이 먼저 변경할 수 있다. 읽은 값을 그대로 덮어쓰면 앞선 변경을 잃을 수 있다. 이 문제는 “SQL 한 문장이 실행됐다”만으로 설명되지 않는다. 어느 snapshot을 읽었고 어떤 조건으로 변경을 허용했는지 살펴야 한다.

이 예제는 임시 디렉터리의 실제 SQLite 파일과 서로 다른 연결 두 개를 사용한다. `:memory:` 데이터베이스 두 개를 같은 저장소처럼 취급하지 않는다. `PRAGMA journal_mode=WAL`의 실제 반환이 wal인지 확인하고, 공유 cache·read_uncommitted는 사용하지 않는다. WAL은 읽기가 기존 snapshot을 유지하며 writer와 함께 진행할 수 있지만 writer는 한 번에 하나다. [SQLite WAL](https://www.sqlite.org/wal.html)

## WAL의 기록과 읽기 경계

Write-ahead logging은 변경한 page를 먼저 WAL에 기록하고 이후 checkpoint로 본 파일에 반영하는 구조다. 읽기 transaction은 시작한 snapshot의 경계에 맞는 page를 읽는다. WAL이 이후에 더 길어져도 현재 읽기 transaction의 관점이 자동으로 최신으로 바뀌지 않는다. 긴 reader는 checkpoint 진행을 제한할 수 있다. Reader와 writer가 함께 진행된다는 설명을 “모든 작업에 잠금도 대기도 없다”로 해석하지 않는다.

SQLite의 WAL snapshot 설명을 일반적인 tuple-version MVCC 구현 전체와 동일시하지 않는다. 구현은 page와 WAL을 이용하지만, 이 예제에서 확인하는 성질은 별도 연결 사이의 snapshot 유지와 오래된 읽기의 쓰기 승격 제한이다. [SQLite isolation](https://www.sqlite.org/isolation.html)

## 사건 순서를 고정한 실행

`counter(id,value,version)` 한 행을 (1,0,0)으로 만든다. 순서는 다음과 같다.

| 순서 | Reader 연결 | Writer 연결 |
|---|---|---|
| 1 | BEGIN 뒤 (0,0) 읽기 | |
| 2 | snapshot 유지 | BEGIN IMMEDIATE 뒤 value·version을 각각 +1, COMMIT |
| 3 | 다시 읽어도 (0,0) | |
| 4 | UPDATE 시도 후 snapshot 오류, ROLLBACK | |
| 5 | 새 읽기에서 (1,1) | version=0 조건의 변경은 0행 |

Thread sleep에 기대지 않고 호출 순서로 관계를 만든다. Reader의 첫 SELECT가 snapshot을 확정한 뒤 writer가 commit한다. Reader의 후속 읽기는 같은 (0,0)이고, transaction을 끝낸 새 읽기는 (1,1)이다.

오래된 reader가 그대로 UPDATE로 승격하려 하면 `SQLITE_BUSY_SNAPSHOT`이 발생한다. 이전 snapshot에서 갈라진 쓰기 이력을 만들 수 없기 때문이다. 이 상황에서는 같은 transaction 안의 UPDATE만 반복할 것이 아니라 읽기 transaction을 끝내고 입력과 판단을 새로 구성해야 한다. 실제 업무의 재시도는 부작용·최대 횟수·충돌 정책을 함께 정한다. [SQLite의 승격 예](https://www.sqlite.org/isolation.html)

## Version 조건으로 변경을 보호한다

업무 행의 version을 명시적으로 두는 낙관적 방식은 “내가 읽은 버전이 아직 현재라면 변경한다”는 계약이다.

```sql
UPDATE counter
SET value = value + 1, version = version + 1
WHERE id = 1 AND version = :expected_version;
```

성공은 rowcount 1, 같은 expected_version을 재사용한 요청은 0이다. 0행은 syntax 오류가 아니라 예상한 상태가 더 이상 맞지 않는다는 결과다. 해당 행이 없는 경우와 버전 충돌이 같은 0으로 나타날 수 있으므로 서비스가 둘을 구분할지 별도로 정한다. 업무 version과 SQLite 내부 snapshot은 역할이 다르다.

수학적으로 version v에서 두 요청이 모두 시작해도, 원자적 조건 변경 하나가 먼저 $`v\to v+1`$로 바꾸면 뒤 요청의 $`version=v`$ 조건은 거짓이다. “읽기 후 애플리케이션에서 비교, 조건 없는 UPDATE”는 같은 보호가 아니다. DB가 조건 확인과 변경을 한 연산으로 처리해야 한다.

## 실행과 독립 관찰

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" database
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

Python 3.12.14·SQLite 3.53.1 실행에서 first와 same_snapshot은 [0,0], current는 [1,1], changed_rows는 1, stale_changed_rows는 0이었다. Snapshot 승격의 확장 오류 코드는 517이었다. 이 값은 SQLite의 `SQLITE_BUSY_SNAPSHOT` 상수와 비교한다. Exception 문자열만 맞추는 테스트는 언어·버전에 따라 취약할 수 있다.

이 코드는 실제 DB engine의 상태를 관찰한다. 독립 검증은 서로 다른 연결의 읽기, 조건부 변경 행 수와 공식 오류 상수이며 애플리케이션 dict로 DB를 흉내 낸 결과가 아니다. 함수는 모든 연결을 닫고 임시 파일을 정리한다. WAL을 지원하는 로컬 파일시스템을 전제로 하며 네트워크 filesystem의 적합성은 주장하지 않는다. 전원 차단 뒤 내구성, 여러 process의 성능이나 production retry 처리를 검증한 결과도 아니다. [SQLite transaction modes](https://www.sqlite.org/lang_transaction.html)

## English

### A read can become stale

Two requests can read one value before either writes. An unconditional replacement based on an old read can lose an earlier update. Correctness depends on the snapshot read and the condition under which a change is accepted, not merely successful SQL syntax.

The example creates one real temporary SQLite file and two distinct connections, verifies that WAL mode was enabled, and excludes shared-cache/read-uncommitted modes. Two independent in-memory databases would not be the same experiment. WAL allows readers and a writer to make concurrent progress, but still permits only one writer at a time. [WAL](https://www.sqlite.org/wal.html)

### Snapshot and event sequence

WAL records changed pages before checkpointing them into the main file. A read transaction keeps its snapshot boundary even as later commits extend WAL. Long-lived readers can constrain checkpoint progress. Concurrent progress is not the absence of locks or waiting.

This page/WAL mechanism should not be equated with every tuple-version MVCC design. The observed properties are snapshot retention between separate connections and restrictions on promoting an obsolete read to a write. [Isolation](https://www.sqlite.org/isolation.html)

The table fixes an explicit schedule: reader begins and reads (0,0); writer begins an immediate transaction, increments value and version and commits; reader still sees (0,0). Its attempted update raises `SQLITE_BUSY_SNAPSHOT`, after which it rolls back. A fresh read sees (1,1). Calls, rather than sleep timing, establish these relations.

Retrying only the update inside the same old transaction does not refresh its snapshot. Application retries must restart the relevant reads and decisions with a bounded, side-effect-aware policy. [SQLite's promotion example](https://www.sqlite.org/isolation.html)

### Optimistic row versions

The shown UPDATE changes value and version only when the current version matches the expected one. A successful update changes one row; repeating the old expected version changes zero rows. Zero is a state-conflict outcome, not malformed SQL. Missing rows can also produce zero, so distinguishing absence from conflict is a separate service policy.

If two requests expect v, the first atomic transition to $`v+1`$ makes the second predicate false. Comparing in application code and then performing an unconditional UPDATE does not provide the same atomic check-and-change. The business version and SQLite snapshot are different concepts.

### Executed results and scope

Run the commands above. Python 3.12.14 with SQLite 3.53.1 produced first/same_snapshot [0,0], current [1,1], one successful row and zero stale rows. Promotion error 517 is checked against SQLite's named extended error constant rather than a localized exception string.

The test observes a real database engine using separate reads, affected-row counts and the official error code. Connections close and temporary storage is removed. A WAL-capable local filesystem is assumed; network-filesystem suitability, power-loss durability, multi-process throughput and production retry behavior are not established. [Transaction modes](https://www.sqlite.org/lang_transaction.html)

## 출처 / Sources

- [SQLite, Write-Ahead Logging](https://www.sqlite.org/wal.html): pages, reader boundaries, single writer and checkpoint constraints.
- [SQLite, Isolation](https://www.sqlite.org/isolation.html): snapshot behavior and obsolete read-to-write promotion.
- [SQLite, Transactions](https://www.sqlite.org/lang_transaction.html): explicit transaction modes and completion. 확인 / checked: 2026-10-19.

# 동시 갱신과 SQLite의 충돌 처리 | Concurrent updates and SQLite conflict handling

설비 시험 결과를 여러 작업자가 갱신하거나 서버의 요청 두 개가 같은 수량을 변경할 때, SQL 실행이 성공했다는 사실만으로 업무 결과가 맞지는 않습니다. 이 사례는 같은 값을 읽은 두 요청이 한 번의 갱신을 덮어쓰는 문제, 읽기 트랜잭션의 스냅샷, 업무용 버전 검사를 구분합니다. 실제 로컬 SQLite 파일과 두 연결을 사용했으며, 호출 순서를 정한 재현 실험입니다. 병렬 부하 시험이나 운영 서비스의 장애 기록은 아닙니다.

## 문제와 판정 조건

자체 구성한 예제 테이블은 `counter(id, value, version)`입니다. 시작 상태는 `(1, 0, 0)`입니다. 두 요청 A와 B가 각각 `value=0`을 읽은 뒤 1을 더하려고 합니다. 성공을 반환한 두 요청이 모두 반영되어야 하는 단순 누적이라면 최종 값은 2여야 합니다. 반면 사용자가 읽은 상태를 근거로 승인하는 업무라면, 그 상태가 바뀌었을 때 두 번째 요청을 거절하고 다시 판단하게 할 수 있습니다. 두 요구사항은 같은 갱신 정책이 아닙니다.

`transaction`은 여러 DB 작업을 하나의 확정·취소 단위로 묶는 트랜잭션입니다. `snapshot`은 읽기 작업이 기준으로 삼는 DB 상태입니다. `version`은 여기서 직접 만든 정수 열로, 업무 데이터가 읽은 뒤 바뀌었는지를 판단합니다. SQLite의 내부 버전 번호나 WAL 위치를 읽는 열이 아닙니다.

## 세 가지 갱신을 비교한 결과

A와 B가 각각 읽기를 끝낸 다음 A의 쓰기, B의 쓰기 순서로 실행했습니다. 각 방식마다 새 DB 파일을 사용했습니다. 아래 수치는 2026-10-21의 실제 로컬 실행 결과입니다.

| 방식 | 핵심 SQL | A·B의 변경 행 수 | 최종 `(value, version)` | 해석 |
| --- | --- | --- | --- | --- |
| 읽은 값으로 덮어쓰기 | `SET value=?`에 각각 1 전달 | 1, 1 | `(1, 0)` | 두 쓰기는 성공했지만 한 증가분이 사라집니다. |
| DB 안에서 증가 | `SET value=value+1` | 1, 1 | `(2, 0)` | 현재 값을 기준으로 각 증가를 반영합니다. |
| 버전 조건 검사 | `SET value=value+1, version=version+1 WHERE version=?` | 1, 0 | `(1, 1)` | 오래된 버전 0을 가진 B의 요청을 거절합니다. |

앞의 두 방식에는 의도적으로 버전을 올리는 SQL을 넣지 않았습니다. 따라서 `version=0`이라는 결과는 그 두 실험에서 버전 관리를 하지 않았다는 뜻입니다. 세 번째 방식도 두 요청을 자동으로 모두 처리하지 않습니다. 충돌을 드러낸 뒤 B의 재조회·업무 재판정을 요구합니다.

이 표에서 얻는 설계 판단은 단순합니다. 누적 카운터는 DB 내부 증가 연산이 적합합니다. 재고를 음수로 만들면 안 되는 경우에는 `WHERE stock >= ?`와 영향받은 행 수를 같은 SQL에 결합할 수 있습니다. 여러 값을 읽어 승인 여부를 판단하는 업무에서는 버전 검사나 적절한 쓰기 트랜잭션이 필요합니다. 재고 예시는 이 글에서 든 적용 예이며, 이번 실행에서 별도 시험한 서비스는 아닙니다.

## WAL과 스냅샷을 확인한 순서

기존 구현인 [`sqlite_wal_snapshot()`](../예제_examples/심화_advanced/ai_data/advanced_ai_models.py)은 임시 폴더에 실제 파일을 만들고 서로 다른 두 `sqlite3.Connection`을 엽니다. `PRAGMA journal_mode=WAL`의 반환값이 `wal`인지 확인합니다. WAL은 변경 내용을 먼저 로그에 기록하는 방식이며, 이 구성에서 읽기와 쓰기가 겹칠 수 있습니다. 동시에 여러 쓰기가 진행된다는 뜻은 아닙니다.

| 순서 | 연결 R | 연결 W | 실제 관측 |
| --- | --- | --- | --- |
| 1 | `BEGIN` 후 조회 | 대기 | R은 `(0, 0)`을 읽습니다. |
| 2 | 읽기 트랜잭션 유지 | `BEGIN IMMEDIATE`, 버전 0의 행을 갱신하고 `COMMIT` | W의 변경 행 수는 1입니다. |
| 3 | 다시 조회 | 쓰기 종료 | R은 여전히 `(0, 0)`을 읽습니다. |
| 4 | 같은 트랜잭션에서 갱신 시도 | — | 확장 오류 코드 517을 확인합니다. |
| 5 | `ROLLBACK` 후 새 조회 | — | R은 `(1, 1)`을 읽습니다. |
| 6 | 오래된 버전 0으로 조건부 갱신 | — | 변경 행 수는 0입니다. |

517은 `SQLITE_BUSY_SNAPSHOT`입니다. 읽기 기준이 오래된 상태에서 그 트랜잭션을 쓰기로 바꾸려 했습니다. 이 경우 같은 `UPDATE`를 무한 반복하는 것으로 해결하지 않습니다. 트랜잭션을 끝내고 최신 데이터를 읽은 뒤 판단을 다시 해야 합니다. 실제 관측은 SQLite의 [격리 설명](https://www.sqlite.org/isolation.html)과 [확장 오류 코드 설명](https://www.sqlite.org/rescode.html#busy_snapshot)에 대응합니다.

## 코드에서 검토할 부분

아래는 기존 코드의 설계 의도를 읽기 위한 짧은 예입니다. 전체 실행 코드와 동일한 독립 프로그램은 아닙니다.

```python
sql = "UPDATE counter SET value=value+1, version=version+1 WHERE id=1 AND version=?"
changed = connection.execute(sql, (expected_version,)).rowcount
if changed == 0:
    raise RuntimeError("읽은 이후 상태가 바뀌었습니다.")
```

`?`는 값이 들어갈 자리표시자입니다. `(expected_version,)`은 원소가 하나인 튜플이며, 쉼표가 있어야 함수 인자용 값 묶음이 됩니다. `execute()`는 SQL을 실행하고 커서를 돌려줍니다. `rowcount`는 이 갱신에서 영향을 받은 행 수입니다. 이 테이블의 기본키 조건에서 0이면 예상 버전의 행을 갱신하지 못했고, 1이면 갱신했습니다. “예외가 없었다”와 “업무 변경이 적용되었다”를 나누어 보는 부분입니다.

`BEGIN IMMEDIATE`로 쓰기 권한을 먼저 확보하면 다른 쓰기와의 경쟁 시점이 앞당겨집니다. 그러나 오래 걸리는 계산이나 사용자 응답을 기다리는 동안 쓰기 트랜잭션을 붙잡으면 다른 요청이 기다립니다. 이 사례는 두 선택의 처리량 우열을 측정하지 않았습니다. 실제 업무에서는 트랜잭션 길이, 충돌률, 재시도 가능성, 중복 요청의 식별 방법을 함께 정해야 합니다.

## 재현 방법과 확인 범위

저장소 루트에서 실행하는 첫 명령은 DB 예제입니다. 출력 경로의 상위 폴더는 먼저 준비합니다. 두 번째 명령은 예제 폴더에서 실행하는 해당 테스트 하나입니다.

```text
python 예제_examples/심화_advanced/ai_data/demo.py database --output /existing/folder/sqlite-review.json
python -m unittest -v test_advanced_ai.TilingDecodeAndData.test_real_sqlite_wal_and_optimistic_conflict
```

이번 환경은 Windows AMD64, CPython 3.12.14, SQLite 3.53.1입니다. 기존 대상 테스트 1개가 통과했고, 추가로 앞의 세 갱신 대조를 실행했습니다. 자세한 순서·결과·파일 해시는 [2026-10-21 검증 기록](검증기록_evidence/SQLite갱신검증_20261021.md)에 있습니다. 기존 소스와 과거 결과 파일은 바꾸지 않았습니다.

메모리 변수로 흉내 낸 잠금 시험이 아니라 실제 DB 엔진을 사용했다는 점이 이 검사의 근거입니다. 다만 프로세스 강제 종료, 전원 중단, 네트워크 파일시스템, 백업 복구, 장시간 체크포인트 지연, TPS와 응답 지연은 시험하지 않았습니다. 이 결과로 운영 DB의 내구성이나 대규모 동시 사용자 성능을 결론 내리지 않습니다.

## 확인 문제

1. 두 `UPDATE`의 `rowcount`가 모두 1인데 증가분이 하나 사라질 수 있습니까?
2. 버전 조건 갱신에서 변경 행 수가 0이면 똑같은 값을 즉시 다시 보내면 됩니까?
3. WAL이면 두 연결이 동시에 DB 파일을 쓰는 것입니까?

답: 1번은 그렇습니다. 둘 다 이전 값 0을 근거로 1을 덮어쓰면 최종 값이 1입니다. 2번은 최신 상태를 읽고 업무 판단을 다시 해야 합니다. 3번은 아닙니다. 이 사례의 WAL은 읽기와 쓰기의 공존을 확인하며, SQLite의 쓰기는 한 번에 하나입니다.

## 출처와 관련 글

- SQLite, [Isolation In SQLite](https://www.sqlite.org/isolation.html), “Isolation And Concurrency”. 읽기 스냅샷과 쓰기 승격의 설명을 확인했습니다.
- SQLite, [Write-Ahead Logging](https://www.sqlite.org/wal.html), WAL의 동작과 제약. 2026-10-21 열람했습니다.
- SQLite, [Result and Error Codes](https://www.sqlite.org/rescode.html#busy_snapshot), `SQLITE_BUSY_SNAPSHOT` 항목.
- [기존 WAL·버전 충돌 학습 본문](../전자컴퓨터공학_ece/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md), [기존 대상 테스트](../예제_examples/심화_advanced/ai_data/test_advanced_ai.py).

## English

This case uses real local SQLite files and two separately opened connections with explicitly ordered calls. An unconditional replacement loses an increment, an in-database increment applies both, and a version predicate rejects the stale writer. The existing WAL example preserves the reader's old snapshot, observes extended error 517 when promoting that reader, then sees the committed value after rollback. One targeted existing test and three additional comparison scenarios were run on CPython 3.12.14 / SQLite 3.53.1. These are correctness checks, not parallel-load, power-loss or durability benchmarks.

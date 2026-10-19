# DB의 인덱스, 트랜잭션, SQL 집계

## 저장된 값보다 중요한 것은 데이터의 관계다

측정값이나 판매 기록을 파일에 한 줄씩 적을 수 있다. 하지만 “장비별 유효 측정 평균”, “지역별 총액”, “중복 없는 샘플 ID”처럼 관계와 규칙이 생기면 데이터베이스의 역할이 커진다. 관계형 DB는 행과 열로 데이터를 표현하고, SQL은 원하는 결과를 선언한다. 실행 순서를 직접 지정하기보다 query planner가 접근 경로를 선택한다. [SQLite query planning](https://www.sqlite.org/queryplanner.html)

키는 행을 구분하고, 제약은 잘못된 상태를 막는다. 예제의 계좌 ID는 primary key이며 잔액은 `CHECK(balance>=0)`를 따른다. 금액은 최소 화폐 단위의 정수로 저장해 이진 부동소수점의 소수 표현 문제를 피한다. 모든 수치가 정수에 적합한 것은 아니다. 측정값의 정밀도, 단위, 허용 범위는 데이터의 의미에 맞춰 별도로 정한다.

## 인덱스는 별도의 탐색 구조다

책의 찾아보기처럼 인덱스는 조건에 맞는 행의 위치를 찾는 데 도움을 준다. 균형 잡힌 B-tree 인덱스에서 단일 키 탐색은 대략 $O(\log N)$, 결과 $K$개를 읽는 비용은 그 뒤에 더해진다. 실제 비용에는 페이지 I/O, 캐시, 중복도, 테이블 접근이 포함된다. 인덱스가 없는 전체 scan은 (O(N))이며 대부분의 행이 필요한 경우 오히려 합리적일 수 있다. [SQLite 탐색·covering index 설명](https://www.sqlite.org/queryplanner.html)

`(region, time)` 복합 인덱스는 region이 먼저, 같은 region 안에서는 time 순으로 정렬한 사전과 비슷하다. 실제 사용 가능 여부는 조건, 정렬, planner와 DB 버전에 따른다. 인덱스는 저장 공간과 쓰기 유지 비용이 필요하므로 개수가 많다고 항상 좋은 것은 아니다. `EXPLAIN QUERY PLAN` 같은 계획 확인과 실제 데이터 크기에서의 측정을 구분한다. 실행 계획이 달라도 결과가 같아야 한다는 점이 첫 번째 검증 기준이다.

## 트랜잭션은 여러 변경을 한 묶음으로 만든다

계좌 A에서 30을 빼고 B에 30을 더하는 작업을 생각하자. 두 문장 사이에 실패하면 총액이 줄어들 수 있다. 트랜잭션은 묶음 전체를 commit하거나 rollback한다. PostgreSQL 문서는 이를 all-or-nothing 연산으로 설명하며 `BEGIN`, `COMMIT`, `ROLLBACK`을 구분한다. 격리 수준은 동시 트랜잭션이 어떤 상태를 볼 수 있는지 정한다. 트랜잭션이 있다는 사실만으로 모든 업무 규칙과 모든 동시성 문제가 해결되는 것은 아니다. [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)

잔액 $A,B$, 양의 이체액 $d\le A$라면

$$A'=A-d,\qquad B'=B+d,\qquad A'+B'=A+B.$$

이 보존식이 성공 경로의 독립 검증 기준이다. 실패 경로에서는 두 잔액이 모두 원래 값이어야 한다. [구현의 `transfer`](../../../예제_examples/확장기초_extended/ai_data/models.py)는 SQL `BEGIN`으로 자체 트랜잭션을 열고, 잔액 조건을 포함한 `UPDATE`의 결과를 확인한다. 성공하면 SQL `COMMIT`, 수신 계좌 누락 등 실패에는 SQL `ROLLBACK`을 실행한다. Python의 `with connection`은 새 트랜잭션을 열어 주지 않으므로 자동 시작에 의존하지 않는다. [Python sqlite3 트랜잭션 제어](https://docs.python.org/3.12/library/sqlite3.html#transaction-control)

함수 시작 시 `in_transaction=False`여야 하며, 이미 열린 호출자 트랜잭션은 변경하지 않고 거부한다. `isolation_level=None`이나 `autocommit=True`에서도 명시적 SQL로 이체를 한 묶음으로 처리한다. 반면 Python의 `autocommit=False`처럼 트랜잭션을 항상 열어 두는 방식은 이 함수의 호출 조건과 맞지 않는다. 실서비스의 다중 연결 격리·경합·장애 복구까지 재현하는 예제는 아니다.

## 집계에서 행의 의미와 NULL을 구분한다

그룹 $g$의 총액은 $S_g=\sum_{i:\,region_i=g}a_i$다.

```sql
SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region;
```

`WHERE`는 집계 전 행을 거르고 `HAVING`은 집계 후 그룹을 거른다. `COUNT(*)`는 행 수, `COUNT(column)`은 해당 열이 NULL이 아닌 행 수다. `AVG`와 `SUM`도 보통 NULL 입력을 제외한다. PostgreSQL에서 빈 입력의 `SUM`은 0이 아니라 NULL이다. 0이 업무상 맞는 경우 `COALESCE`로 그 정책을 표현한다. NULL은 자동으로 0이나 “측정값 0”이 되지 않는다. [PostgreSQL aggregates](https://www.postgresql.org/docs/current/functions-aggregate.html)

행별 평균을 다시 단순 평균하면 그룹 크기가 다를 때 틀린다. 그룹 평균 $m_g$, 표본 수 $n_g$라면 전체 평균은 $\sum_gn_gm_g/\sum_gn_g$다. Join 후에 행이 복제되면 합계가 부풀 수 있으므로 집계 단위가 주문인지, 품목인지, 센서 측정인지 먼저 정의한다.

## 실행과 검증

[예제](../../../예제_examples/확장기초_extended/ai_data/models.py)의 `sales_totals`는 매개변수 바인딩으로 행을 넣고 SQL로 집계한다. 문자열로 SQL에 값을 이어 붙이지 않는다. [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 양수·환불을 섞은 직접 계산 합계, 빈 입력, 이체 성공의 총액 보존, 수신 계좌 누락 시 rollback, 잔액 부족을 확인한다. 자동 시작을 끈 두 연결 방식에서도 실패한 출금이 남지 않는지, 기존 호출자 트랜잭션을 거부할 때 그 변경이 보존되는지도 검사한다. 인덱스의 존재를 속도 향상의 증거로 삼지 않고, 정확성과 계획·성능의 검증을 나눈다.

## English

### Relations and constraints

Plain files can store measurements or sales, but questions such as per-device averages, regional totals and unique sample IDs introduce relationships and rules. A relational database represents data as rows and columns. SQL declares the desired result while the query planner selects an access strategy. [SQLite planning](https://www.sqlite.org/queryplanner.html)

Keys identify rows and constraints reject invalid states. The account example uses a primary key and nonnegative balance check. Monetary amounts use integer minor units to avoid binary floating-point representation of decimal fractions. This does not make integers suitable for every measurement; precision, units and valid ranges depend on the data's meaning.

### Index costs

An index resembles a book's index. A balanced B-tree lookup is approximately $O(\log N)$, followed by the cost of reading $K$ matches. Real costs include pages, caching, duplicates and table lookups. Scanning all $N$ rows can be reasonable when most rows are needed. A composite `(region, time)` index orders by region, then time within a region. Eligibility depends on predicates, ordering, planner and version. Indexes consume space and add write maintenance, so more indexes do not automatically improve performance. A plan inspection and a representative timing measurement answer different questions. [SQLite indexes](https://www.sqlite.org/queryplanner.html)

### Atomic changes

A transfer subtracts $d$ from one balance and adds it to another. The equations above independently establish total conservation. A failure between separate updates could violate that property. A transaction groups the changes for commit or rollback. Isolation specifies visibility between concurrent transactions; transactions alone do not establish every business invariant or eliminate every concurrency issue. [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)

The linked `transfer` explicitly starts its own SQL `BEGIN`, performs a conditional debit and checks affected rows. It executes SQL `COMMIT` on success and SQL `ROLLBACK` after failures such as a missing recipient. Python's connection context manager does not open a new transaction, so the implementation does not depend on implicit transaction startup. [Python sqlite3 transaction control](https://docs.python.org/3.12/library/sqlite3.html#transaction-control)

The function requires `in_transaction=False` on entry and rejects an existing caller transaction without changing it. Explicit SQL also makes the transfer atomic with `isolation_level=None` or `autocommit=True`. Python's `autocommit=False`, which keeps a transaction open, does not meet this function's entry contract. This is not a multi-connection isolation, contention or crash-recovery experiment.

### Aggregation semantics

The SQL query implements $S_g=\sum_{i:region_i=g}a_i$. `WHERE` filters input rows; `HAVING` filters aggregate groups. `COUNT(*)` counts rows, whereas `COUNT(column)` counts non-NULL values. `SUM` and `AVG` generally exclude NULL input. PostgreSQL returns NULL for `SUM` over no rows; `COALESCE` can express a deliberate zero policy. A missing measurement is not automatically a measured zero. [PostgreSQL aggregates](https://www.postgresql.org/docs/current/functions-aggregate.html)

When groups have different sizes, the overall mean is $\sum_gn_gm_g/\sum_gn_g$, not the unweighted mean of group means. A join can duplicate input rows and inflate totals. Define whether the aggregation unit is an order, line item or sensor observation before interpreting results.

### Implementation and checks

`sales_totals` inserts data with bound parameters and groups it in SQL. Tests compare positive amounts and refunds against hand-calculated totals, check an empty input, total conservation after a successful transfer, rollback after a missing recipient and rejection of insufficient funds. They also verify rollback in both connection modes without implicit transaction startup, and preservation of the caller's existing changes when its transaction is rejected. They separate result correctness from plan and performance assessment; creating an index is not evidence of a measured speedup.

## Sources

- [SQLite, Query Planning](https://www.sqlite.org/queryplanner.html): indexed lookup, scan, compound and covering indexes.
- [PostgreSQL, Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html): atomic transaction blocks and rollback.
- [Python 3.12, sqlite3 transaction control](https://docs.python.org/3.12/library/sqlite3.html#transaction-control): connection modes, explicit SQL and context-manager behavior.
- [PostgreSQL, Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html): COUNT, NULL and empty-input semantics. Reference date: 2026-10-19.

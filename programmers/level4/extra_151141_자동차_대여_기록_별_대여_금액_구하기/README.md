# 자동차 대여 기록 별 대여 금액 구하기

Level 4 · [151141 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/151141)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

트럭의 각 대여 기록별 요금을 구합니다. 시작·종료일을 모두 포함하고 7·30·90일 이상에 해당하는 가장 긴 할인 구간을 적용합니다. 요금·기록 ID 내림차순입니다.

## 풀이

DATEDIFF+1로 포함 일수를 구하고 90→30→7 순서로 할인 종류를 고릅니다. 할인 미해당은 0%로 처리하며 마지막에 FLOOR합니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

각 기록에 적용 가능한 할인율을 상관 하위쿼리로 조회합니다. 할인 조인 대신 독립 조회를 써 조건을 분리합니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Return each truck rental’s fee, including both endpoint dates and applying its longest qualifying 7-, 30-, or 90-day discount tier. Order by fee and history ID descending.

### Method and correctness

Use DATEDIFF+1 for inclusive days, choose the tier in 90→30→7 order, treat missing discounts as zero, and FLOOR the final amount.



### Alternative and trade-offs

Look up the appropriate discount through a correlated subquery rather than an outer join.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 자동차 대여 기록 별 대여 금액 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151141) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

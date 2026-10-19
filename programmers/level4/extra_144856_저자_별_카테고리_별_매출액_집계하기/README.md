# 저자 별 카테고리 별 매출액 집계하기

Level 4 · [144856 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/144856)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022년 1월 매출을 저자·카테고리별로 합산합니다. 매출은 판매량×책 가격이고 저자 ID 오름차순·카테고리 내림차순입니다.

## 풀이

도서·저자·판매를 키로 조인하고 기간을 제한한 뒤 같은 저자·카테고리의 금액을 합칩니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

판매를 도서별로 먼저 합산해 같은 책의 여러 날짜 기록을 줄인 후 조인합니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Sum January 2022 revenue by author and category as quantity×book price, ordered by author ID ascending and category descending.

### Method and correctness

Join books, authors and sales by their keys, filter the period, and aggregate revenue by author and category.



### Alternative and trade-offs

Preaggregate sales per book to reduce multiple daily records before joining.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 저자 별 카테고리 별 매출액 집계하기](https://school.programmers.co.kr/learn/courses/30/lessons/144856) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

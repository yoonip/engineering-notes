# 식품분류별 가장 비싼 식품의 정보 조회하기

Level 4 · [131116 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131116)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

과자·국·김치·식용유 분류의 최고가 상품을 구하고 가격 내림차순으로 출력합니다.

## 풀이

각 상품의 가격을 같은 분류의 MAX 가격과 비교합니다. 가격 동률이 있다면 최댓값과 같은 행을 모두 보존합니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

DENSE_RANK에서 NULL만 있는 분류도 1위를 받으므로 PRICE IS NOT NULL을 함께 검사합니다. NULL은 가격 비교 대상에서 제외하며, 숫자 가격이 전혀 없는 분류는 출력하지 않습니다.

분류별 가격 순위를 DENSE_RANK로 붙여 1위만 남깁니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Return highest-priced products in the snack, soup, kimchi and cooking-oil categories, ordered by price descending.

### Method and correctness

Compare each product price with its category MAX. Preserve every tied maximum if a tie exists.



### Alternative and trade-offs

DENSE_RANK also assigns rank one to an all-NULL group, so PRICE IS NOT NULL is required. NULL is not a price candidate; omit a category with no numeric price.

Use DENSE_RANK within each category and retain rank one.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [MySQL 8.4 집계 함수](https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html) — MAX의 NULL 제외 규칙 / NULL handling in MAX. 확인 / checked: 2026-11-02.
- [프로그래머스 공식 문제: 식품분류별 가장 비싼 식품의 정보 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/131116) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 8회 SQLite 호환 검사를 통과했습니다. NULL만 있는 분류와 숫자·NULL 혼합 분류를 별도 경계 입력으로 포함합니다.

Both SQL implementations passed eight SQLite compatibility checks, including an additional fixture with an all-NULL group and a mixed numeric/NULL group.

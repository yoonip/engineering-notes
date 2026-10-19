# 오프라인/온라인 판매 데이터 통합하기

Level 4 · [131537 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131537)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022년 3월 온라인·오프라인 판매를 통합합니다. 오프라인 USER_ID는 NULL이고 날짜·상품 ID·사용자 ID 오름차순입니다.

## 풀이

열 순서를 맞춰 UNION ALL로 합칩니다. 같은 날짜·상품·수량이라도 다른 실제 판매라면 모두 남아야 합니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

전체 판매를 먼저 하나의 CTE로 통합한 뒤 바깥에서 기간 조건과 날짜 형식을 적용합니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Combine online and offline sales from March 2022, using NULL user IDs for offline rows and ordering by date, product ID, then user ID.

### Method and correctness

Align output columns and use UNION ALL. Equal-looking rows can represent distinct real sales and must be retained.



### Alternative and trade-offs

Combine all sales in one CTE, then apply the period filter and date formatting outside it.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 오프라인/온라인 판매 데이터 통합하기](https://school.programmers.co.kr/learn/courses/30/lessons/131537) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

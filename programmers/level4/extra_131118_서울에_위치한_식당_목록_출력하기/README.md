# 서울에 위치한 식당 목록 출력하기

Level 4 · [131118 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131118)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

주소가 서울로 시작하고 리뷰가 있는 식당의 평균 리뷰점수를 소수 둘째 자리까지 반올림합니다. 점수·즐겨찾기 내림차순입니다.

## 풀이

식당별 리뷰 평균을 구하려면 식당 ID로 묶습니다. ROUND는 평균을 계산한 뒤 적용하고 리뷰 없는 식당은 내부 조인으로 제외합니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

리뷰 평균을 별도 CTE에서 계산하고 서울 식당에 조인합니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Return reviewed restaurants whose addresses start with Seoul, rounding average ratings to two decimals and sorting by score and favorites descending.

### Method and correctness

Group reviews by restaurant ID. Apply ROUND after averaging, and use an inner join to omit restaurants without reviews.



### Alternative and trade-offs

Preaggregate review averages in a CTE, then join Seoul restaurants.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 서울에 위치한 식당 목록 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131118) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

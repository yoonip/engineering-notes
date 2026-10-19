# 그룹별 조건에 맞는 식당 목록 출력하기

Level 4 · [131124 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131124)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

리뷰 수가 가장 많은 회원들의 모든 리뷰를 구합니다. 공동 최다인 회원도 포함하고 리뷰 날짜·리뷰 내용 오름차순입니다.

## 풀이

회원별 리뷰 수를 먼저 세고 그 최댓값과 같은 회원을 모두 선택합니다. LIMIT 1은 공동 최다 회원을 빠뜨릴 수 있으므로 사용하지 않습니다.


기존 제출본은 최다 회원 한 명을 선택했습니다. 현재 풀이는 공동 최다 회원의 리뷰도 포함하도록 정리했습니다.


[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

DENSE_RANK로 회원별 리뷰 수 순위를 매긴 뒤 1위 회원들의 리뷰를 조인합니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Return every review from members tied for the largest review count, ordered by review date and review text.

### Method and correctness

Count reviews per member and select every member whose count equals the maximum. LIMIT 1 would omit tied leaders.


The saved submission selected one top member. The current solution also includes reviews by tied top members.


### Alternative and trade-offs

Use DENSE_RANK on per-member review counts, then join every first-ranked member’s reviews.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 그룹별 조건에 맞는 식당 목록 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131124) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

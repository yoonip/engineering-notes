# 특정 세대의 대장균 찾기

Level 4 · [301650 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/301650)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

루트의 자식을 두 단계 연결해 정확히 3세대인 개체 ID를 오름차순으로 구합니다.

## 풀이

자기 조인으로 자식→부모→조부모를 연결하고 조부모의 PARENT_ID가 NULL인 행만 남깁니다. 세 번의 별도 테이블이 아니라 같은 테이블의 세 역할입니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

재귀 CTE로 루트부터 세대 번호를 붙입니다. 깊이를 3으로 제한해 불필요한 후손 확장을 막습니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Return IDs of exactly third-generation organisms, ordered ascending. A root is generation one.

### Method and correctness

Join child to parent to grandparent and retain rows whose grandparent has NULL PARENT_ID. These are three roles of one table, not three distinct tables.



### Alternative and trade-offs

A recursive CTE assigns generations from the roots and stops after generation three.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 특정 세대의 대장균 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/301650) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

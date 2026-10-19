# 언어별 개발자 분류하기

Level 4 · [276036 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/276036)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

A는 Front End 기술과 Python을 모두 보유, B는 A가 아니면서 C# 보유, C는 앞 두 등급이 아니면서 Front End 보유입니다. 해당 개발자만 등급·ID·이메일을 등급과 ID 오름차순으로 구합니다.

## 풀이

기술 코드는 서로 다른 비트이므로 비트 AND로 보유 여부를 확인합니다. CASE를 A→B→C 순서로 평가해 등급 우선순위를 지킵니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

통합 비트마스크 대신 EXISTS로 각 기술 조건을 직접 확인합니다. 기술 행이 여러 개 있어도 개발자 행이 늘어나지 않습니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

A requires both a Front End skill and Python; otherwise B requires C#, otherwise C requires a Front End skill. Return qualifying developers by grade and ID ascending.

### Method and correctness

Skill codes occupy distinct bits, so bitwise AND tests possession. Evaluate CASE in A→B→C order to enforce grade precedence.



### Alternative and trade-offs

Use EXISTS for each skill requirement instead of a combined bitmask. Multiple matching skills cannot duplicate developer rows.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 언어별 개발자 분류하기](https://school.programmers.co.kr/learn/courses/30/lessons/276036) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

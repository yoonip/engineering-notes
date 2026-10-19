# 특정 기간동안 대여 가능한 자동차들의 대여비용 구하기

Level 4 · [157339 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/157339)

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건

2022년 11월 내내 비어 있는 세단·SUV의 30일 할인 요금을 구합니다. 500,000 이상 2,000,000 미만만 남기고 요금 내림차순·차종 오름차순·ID 내림차순입니다.

## 풀이

대여 구간이 11월과 겹치는 조건은 시작일≤11월30일 AND 종료일≥11월1일입니다. 이런 기록이 없는 차량만 고르고 30일 이상 할인율을 적용해 소수점을 버립니다.



[기본 SQL](solution.sql) · [다른 SQL](alternative.sql) · [제출 원본](submitted_original.sql)

## 다른 방법과 비교

겹치는 기록만 LEFT JOIN한 뒤 NULL인 행을 남기는 반조인을 사용합니다.

조인·상관 하위쿼리·CTE·윈도 함수의 실행 비용은 행 수, 인덱스, MySQL 실행계획에 따라 달라집니다. 같은 결과를 낸다고 같은 속도인 것은 아닙니다. 정렬이 필요한 R개 결과의 비교 정렬 비용은 O(R log R)이고, 해시 집계·인덱스 접근 여부에 따라 그 앞 단계의 비용이 달라집니다.

## 검증

공식 예제와 별도 경계 입력의 결과를 확인합니다. 중복 판매, NULL, 기준 날짜 양 끝, 공동 최다·최고가 등 해당 쿼리의 중요한 조건을 포함합니다. SQLite 호환 실행은 MySQL 신규 채점과 구분하며 [test_queries.py](test_queries.py)에서 두 SQL을 같은 입력에 실행합니다.

## English

### Task and constraints

Return discounted 30-day fees for sedans/SUVs available throughout November 2022. Keep fees from 500,000 inclusive to 2,000,000 exclusive; order fee descending, type ascending, ID descending.

### Method and correctness

A rental overlaps November when start≤November 30 and end≥November 1. Keep cars without such rentals, apply the 30-day discount, and floor the fee.



### Alternative and trade-offs

Use a LEFT anti-join against overlapping rentals and retain NULL matches.

Runtime depends on row counts, indexes and the MySQL execution plan. Equivalent queries need not run at equal speed. Comparison sorting of R result rows costs O(R log R); the preceding join and aggregation costs depend on hash/index access and the chosen plan.

### Verification

Official examples and additional edge fixtures cover relevant duplicates, NULLs, inclusive date boundaries and tied maxima. [test_queries.py](test_queries.py) runs both queries on identical fixtures using a SQLite compatibility adapter; this is distinct from a new MySQL website submission. The original saved submission received 100 points.

## 출처 / Sources

- [프로그래머스 공식 문제: 특정 기간동안 대여 가능한 자동차들의 대여비용 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/157339) — 조건·스키마·예제 / task rules, schema and examples. 확인 / checked: 2026-10-19.

## 예제 표기 확인 / Example consistency

공식 예제 입력으로 다시 계산하면 ID 1은 25,000×30×0.92=690,000원, ID 5는 22,000×30×0.90=594,000원입니다. 원문 설명의 621,000원과 결과표의 ID·금액 배치는 이 입력과 맞지 않습니다. 검증 자료는 입력과 할인식으로 독립 계산한 값을 사용합니다.

Recomputing the official inputs gives 690,000 for car 1 (25,000×30×0.92) and 594,000 for car 5 (22,000×30×0.90). The stated 621,000 and the displayed ID–fee associations are inconsistent with these inputs. Fixtures use independently recomputed amounts.

## 실행 / Run

```bash
python test_queries.py
```

[입력 테이블과 기대 결과 / Input tables and expected rows](query_fixtures.json) — 공식 입력·빈 테이블·독립 경계 입력에 두 SQL을 실행한 6회 SQLite 호환 검사를 통과했습니다.

Both SQL implementations passed six SQLite compatibility checks across the official-input, empty-table and independent boundary fixtures.

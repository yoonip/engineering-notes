# 성분으로 구분한 아이스크림 총 주문량

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/133026) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

성분 유형별 아이스크림 상반기 총 주문량을 구한다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 성분 유형별 아이스크림 상반기 총 주문량을 구한다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `FIRST_HALF`: `SHIPMENT_ID`, `FLAVOR`, `TOTAL_ORDER`
- `ICECREAM_INFO`: `FLAVOR`, `INGREDIENT_TYPE`

## 풀이를 따라가기

맛을 키로 주문 테이블과 성분 테이블을 연결한다. 성분 유형별 TOTAL_ORDER를 합하고 총 주문량 오름차순으로 정렬한다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 맛을 키로 주문 테이블과 성분 테이블을 연결한다. 성분 유형별 TOTAL_ORDER를 합하고 총 주문량 오름차순으로 정렬한다.
SELECT i.INGREDIENT_TYPE, SUM(h.TOTAL_ORDER) AS TOTAL_ORDER
FROM FIRST_HALF AS h
JOIN ICECREAM_INFO AS i ON i.FLAVOR = h.FLAVOR
GROUP BY i.INGREDIENT_TYPE
ORDER BY TOTAL_ORDER
```

## 왜 맞는가

맛 키로 주문과 성분 유형을 연결하면 각 주문량이 해당 성분 그룹에 배정된다. 성분별 SUM은 그 성분을 쓰는 맛들의 주문량 합이다.

주문 N개와 성분 정보 M개의 조인 뒤 G개 성분 합계를 정렬한다. 조인 방식·키 인덱스가 비용을 좌우하며 결과 비교 정렬은 O(G log G)이다.

주의할 점: 맛별 행 수를 세는 문제가 아니라 주문량 합을 구한다. 두 테이블의 연결 키는 FLAVOR다.

## 다른 방법: 맛별 주문 선집계 후 성분별 합산

```sql
WITH flavor_totals AS (
    SELECT FLAVOR,SUM(TOTAL_ORDER) AS N FROM FIRST_HALF GROUP BY FLAVOR
)
SELECT i.INGREDIENT_TYPE,SUM(f.N) AS TOTAL_ORDER
FROM flavor_totals f JOIN ICECREAM_INFO i ON i.FLAVOR=f.FLAVOR
GROUP BY i.INGREDIENT_TYPE ORDER BY TOTAL_ORDER;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 맛을 키로 주문 테이블과 성분 테이블을 연결한다. 성분 유형별 TOTAL_ORDER를 합하고 총 주문량 오름차순으로 정렬한다. | 맛별 주문 선집계 후 성분별 합산 |
| 비용 | 주문 N개와 성분 정보 M개의 조인 뒤 G개 성분 합계를 정렬한다. 조인 방식·키 인덱스가 비용을 좌우하며 결과 비교 정렬은 O(G log G)이다. | 맛별 주문량을 먼저 합친 뒤 성분별로 다시 합친다. 맛이 고유한 입력에서는 앞선 집계가 행 수를 줄이지 않는다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Return first-half ice-cream order totals grouped by ingredient type.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return first-half ice-cream order totals grouped by ingredient type.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `FIRST_HALF`: `SHIPMENT_ID`, `FLAVOR`, `TOTAL_ORDER`
- `ICECREAM_INFO`: `FLAVOR`, `INGREDIENT_TYPE`

### Approach

Join orders and ingredient information by flavor, sum TOTAL_ORDER per ingredient type, and order totals ascending.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Joining on flavor assigns each order total to its ingredient type. SUM by ingredient combines the totals of its associated flavors.

Join N order rows with M ingredient rows and sort G ingredient totals. Join strategy and key indexes affect cost; result comparison sorting is O(G log G).

Boundary cases: Sum order quantities rather than counting flavors. FLAVOR is the join key.

### Alternative: Preaggregate orders by flavor before ingredient grouping

Aggregate by flavor before ingredient. With unique flavor rows, the first aggregation does not reduce row count.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 성분으로 구분한 아이스크림 총 주문량](https://school.programmers.co.kr/learn/courses/30/lessons/133026) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

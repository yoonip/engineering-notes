# ROOT 아이템 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/273710) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

부모가 없는 ROOT 아이템의 ID와 이름을 찾는다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 부모가 없는 ROOT 아이템의 ID와 이름을 찾는다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `ITEM_INFO`: `ITEM_ID`, `ITEM_NAME`, `RARITY`, `PRICE`
- `ITEM_TREE`: `ITEM_ID`, `PARENT_ITEM_ID`

## 풀이를 따라가기

관계 테이블의 PARENT_ITEM_ID가 NULL인지 검사한 뒤 정보 테이블에서 이름을 가져온다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 관계 테이블의 PARENT_ITEM_ID가 NULL인지 검사한 뒤 정보 테이블에서 이름을 가져온다.
SELECT i.ITEM_ID, i.ITEM_NAME
FROM ITEM_INFO AS i
JOIN ITEM_TREE AS tree ON tree.ITEM_ID = i.ITEM_ID
WHERE tree.PARENT_ITEM_ID IS NULL
ORDER BY i.ITEM_ID
```

## 왜 맞는가

부모 ID가 NULL인 관계 행이 ROOT를 뜻한다. 아이템 ID로 이름을 연결하므로 부모가 없는 아이템의 번호와 이름만 출력한다.

정보 N개와 관계 M개의 조인·필터 뒤 R개 ROOT를 정렬한다. 키 인덱스와 조인 계획에 따라 비용이 달라지며 결과 비교 정렬은 O(R log R)이다.

주의할 점: NULL은 = NULL이 아니라 IS NULL로 검사한다. ROOT는 업그레이드할 수 없는 마지막 아이템과 다르다.

공식 스키마 표의 RARITY 자료형 표기와 달리 예제·조회 조건은 `COMMON`, `RARE`, `LEGEND` 문자열을 사용한다. 쿼리에서도 이 문자열 값으로 비교한다.

## 다른 방법: EXISTS로 ROOT 관계 확인

```sql
SELECT i.ITEM_ID,i.ITEM_NAME FROM ITEM_INFO i
WHERE EXISTS (SELECT 1 FROM ITEM_TREE t WHERE t.ITEM_ID=i.ITEM_ID AND t.PARENT_ITEM_ID IS NULL)
ORDER BY i.ITEM_ID;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 관계 테이블의 PARENT_ITEM_ID가 NULL인지 검사한 뒤 정보 테이블에서 이름을 가져온다. | EXISTS로 ROOT 관계 확인 |
| 비용 | 정보 N개와 관계 M개의 조인·필터 뒤 R개 ROOT를 정렬한다. 키 인덱스와 조인 계획에 따라 비용이 달라지며 결과 비교 정렬은 O(R log R)이다. | 각 아이템에 부모 없는 관계 행이 있는지 EXISTS로 확인한다. ITEM_ID 인덱스와 세미조인 변환이 비용에 영향을 준다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find IDs and names of ROOT items without a parent.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Find IDs and names of ROOT items without a parent.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `ITEM_INFO`: `ITEM_ID`, `ITEM_NAME`, `RARITY`, `PRICE`
- `ITEM_TREE`: `ITEM_ID`, `PARENT_ITEM_ID`

### Approach

Filter relationship rows with NULL PARENT_ITEM_ID and obtain names from the item table.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A relation with a NULL parent ID identifies a root. Joining by item ID retrieves exactly those root items and their names.

Join/filter N item records and M relations, then sort R roots. Key indexes and join strategy affect cost; result comparison sorting is O(R log R).

Boundary cases: Use IS NULL, not = NULL. A ROOT item is distinct from a terminal upgrade item.

Although the official schema’s RARITY type label is inconsistent, its examples and predicates use string values `COMMON`, `RARE` and `LEGEND`. The queries compare those string values.

### Alternative: EXISTS over root relationship rows

Check root relations with EXISTS per item; ITEM_ID indexes and semijoin transformations affect cost.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: ROOT 아이템 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/273710) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

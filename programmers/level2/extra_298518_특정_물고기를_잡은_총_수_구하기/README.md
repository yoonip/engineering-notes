# 특정 물고기를 잡은 총 수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/298518) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

BASS와 SNAPPER에 해당하는 포획 기록 수를 합해 한 행으로 출력한다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. BASS와 SNAPPER에 해당하는 포획 기록 수를 합해 한 행으로 출력한다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `FISH_INFO`: `ID`, `FISH_TYPE`, `LENGTH`, `TIME`
- `FISH_NAME_INFO`: `FISH_TYPE`, `FISH_NAME`

## 풀이를 따라가기

물고기 종류 번호로 이름을 조인하고 두 이름을 고른 뒤 COUNT(*)로 행을 센다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 물고기 종류 번호로 이름을 조인하고 두 이름을 고른 뒤 COUNT(*)로 행을 센다.
SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO AS f
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
WHERE names.FISH_NAME IN ('BASS', 'SNAPPER')
```

## 왜 맞는가

종류 키로 이름을 확인해 BASS 또는 SNAPPER인 포획 행만 센다. COUNT(*)이므로 길이가 NULL인 행도 포함된다. EXISTS 대안은 각 포획 행의 해당 종류 존재 여부를 검사한다.

물고기 N개와 종류 M개의 조인 또는 존재 검사 비용이 필요하다. 종류 키 인덱스로 조회를 줄일 수 있으며 출력은 합계 한 행이라 정렬하지 않는다.

주의할 점: 종류별 두 행이 아니라 전체 합계 한 행이다. 길이가 NULL인 포획도 센다.

## 다른 방법: EXISTS 세미 조인

```sql
SELECT COUNT(*) AS FISH_COUNT
FROM FISH_INFO f
WHERE EXISTS (
    SELECT 1 FROM FISH_NAME_INFO n
    WHERE n.FISH_TYPE=f.FISH_TYPE AND n.FISH_NAME IN ('BASS','SNAPPER')
);
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 물고기 종류 번호로 이름을 조인하고 두 이름을 고른 뒤 COUNT(*)로 행을 센다. | EXISTS 세미 조인 |
| 비용 | 물고기 N개와 종류 M개의 조인 또는 존재 검사 비용이 필요하다. 종류 키 인덱스로 조회를 줄일 수 있으며 출력은 합계 한 행이라 정렬하지 않는다. | 각 물고기의 종류가 대상 이름인지 EXISTS로 검사한다. 결과는 한 행이며 종류 키 접근 방식에 따라 비용이 달라진다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Return one total count of catches whose species is BASS or SNAPPER.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return one total count of catches whose species is BASS or SNAPPER.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `FISH_INFO`: `ID`, `FISH_TYPE`, `LENGTH`, `TIME`
- `FISH_NAME_INFO`: `FISH_TYPE`, `FISH_NAME`

### Approach

Join species IDs to names, filter the two requested names and count rows with COUNT(*).

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Resolve species names and count catches of BASS or SNAPPER. COUNT(*) includes NULL lengths. The EXISTS alternative tests the matching species for each catch.

Cost comes from joining or existence-checking N catches against M species. A species-key index can reduce lookups. The single aggregate row requires no sorting.

Boundary cases: Return one combined total, not one row per species. Include catches with NULL length.

### Alternative: EXISTS semijoin

Use EXISTS to check each catch's species name. The result is one row; species-key access determines lookup cost.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 특정 물고기를 잡은 총 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/298518) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

# 부모의 형질을 모두 가지는 대장균 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/301647) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

부모가 가진 모든 비트 형질을 포함한 자식의 ID와 두 형질 값을 찾는다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 부모가 가진 모든 비트 형질을 포함한 자식의 ID와 두 형질 값을 찾는다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `ECOLI_DATA`: `ID`, `PARENT_ID`, `SIZE_OF_COLONY`, `DIFFERENTIATION_DATE`, `GENOTYPE`

## 풀이를 따라가기

같은 테이블을 부모·자식 역할로 조인한다. 자식 AND 부모가 부모와 같으면 부모의 모든 켜진 비트를 보존한 것이다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 같은 테이블을 부모·자식 역할로 조인한다. 자식 AND 부모가 부모와 같으면 부모의 모든 켜진 비트를 보존한 것이다.
SELECT child.ID, child.GENOTYPE, parent.GENOTYPE AS PARENT_GENOTYPE
FROM ECOLI_DATA AS child
JOIN ECOLI_DATA AS parent ON parent.ID = child.PARENT_ID
WHERE (child.GENOTYPE & parent.GENOTYPE) = parent.GENOTYPE
ORDER BY child.ID
```

## 왜 맞는가

자식과 부모를 ID로 연결하면 비교 대상 부모가 정해진다. child AND parent가 parent와 같다는 것은 부모의 모든 1비트가 자식에도 있다는 뜻이다. 자식의 추가 형질은 허용한다.

N개 자식에서 부모 키를 조회하고 비트를 비교한 뒤 R개 결과를 정렬한다. 부모 키 인덱스와 조인 계획이 조회 비용을 정하며 결과 비교 정렬은 O(R log R)이다.

주의할 점: 정수 크기가 크다고 형질을 포함하는 것은 아니다. 부모가 없는 행은 제외한다.

## 다른 방법: 상관 서브쿼리와 비트 OR

```sql
SELECT c.ID, c.GENOTYPE,
       (SELECT p.GENOTYPE FROM ECOLI_DATA p WHERE p.ID=c.PARENT_ID) AS PARENT_GENOTYPE
FROM ECOLI_DATA c
WHERE EXISTS (
    SELECT 1 FROM ECOLI_DATA p
    WHERE p.ID=c.PARENT_ID AND (c.GENOTYPE | p.GENOTYPE)=c.GENOTYPE
)
ORDER BY c.ID;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 같은 테이블을 부모·자식 역할로 조인한다. 자식 AND 부모가 부모와 같으면 부모의 모든 켜진 비트를 보존한 것이다. | 상관 서브쿼리와 비트 OR |
| 비용 | N개 자식에서 부모 키를 조회하고 비트를 비교한 뒤 R개 결과를 정렬한다. 부모 키 인덱스와 조인 계획이 조회 비용을 정하며 결과 비교 정렬은 O(R log R)이다. | 부모 정보를 상관 하위쿼리로 읽고 OR의 포함 관계를 검사한다. 부모 키 조회가 반복될 수 있어 실제 계획을 비교해야 한다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Return children containing every trait bit present in their parent, with both genotype values.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return children containing every trait bit present in their parent, with both genotype values.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `ECOLI_DATA`: `ID`, `PARENT_ID`, `SIZE_OF_COLONY`, `DIFFERENTIATION_DATE`, `GENOTYPE`

### Approach

Self-join parent and child. child AND parent equals parent exactly when all parent bits are present in the child.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The ID join identifies each child's parent. child AND parent equals parent exactly when every parent bit is present in the child; additional child traits are allowed.

Look up parents for N children, test bits and sort R matches. Parent-key indexes and join plans determine lookup cost; result comparison sorting is O(R log R).

Boundary cases: Numerical magnitude does not imply bit containment. Exclude rows without a parent.

### Alternative: Correlated parent lookup with bitwise OR

Use correlated parent lookups and the equivalent OR subset test. Repeated key lookups require plan inspection.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 부모의 형질을 모두 가지는 대장균 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/301647) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

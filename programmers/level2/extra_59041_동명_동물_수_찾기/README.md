# 동명 동물 수 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59041) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

이름 NULL은 제외하며 2마리 이상이 같은 이름인 그룹의 NAME·COUNT를 이름순으로 출력합니다.

Exclude NULL names and output NAME and COUNT for names shared by at least two animals, ordered by name.

## 풀이 흐름 / Approach

NULL 이름을 제외한 뒤 이름별 동물 수를 셉니다. 두 마리 이상인 그룹만 HAVING으로 남기고 이름순으로 출력합니다.

Exclude NULL names, count animals per name, keep groups of at least two with HAVING, and order by name.

## 왜 맞는가 / Why it works

WHERE는 이름 없는 행을 집계 전에 제거합니다. GROUP BY와 COUNT(*)가 이름별 마릿수를 만들고 HAVING이 그 집계값에 조건을 적용합니다.

WHERE removes unnamed rows before aggregation. GROUP BY and COUNT(*) form per-name counts, then HAVING applies the threshold to those aggregated values.

## 비용 / Complexity

일반 스캔·해시 집계 O(n), 정렬 그룹 수 g에 O(g log g) / Typical O(n) scan/hash aggregation plus O(g log g) group sort

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- COUNT(*)는 그룹 안 행 수, AS는 별칭.
SELECT NAME, COUNT(*) AS COUNT
FROM ANIMAL_INS
-- IS NOT NULL로 이름 없는 동물 제외.
WHERE NAME IS NOT NULL
GROUP BY NAME
-- 두 번 이상 등장한 이름만 선택.
HAVING COUNT(*) >= 2
ORDER BY NAME
```

## 다른 방법: 상관 서브쿼리의 같은 이름 수 / Correlated count per distinct name

각 행의 이름과 같은 행 수를 서브쿼리로 세고 DISTINCT로 한 번만 출력합니다. 인덱스·최적화가 없으면 O(n²) 조회가 되어 그룹 집계보다 불리할 수 있습니다.

Count matching names in a correlated subquery and use DISTINCT to emit each name once. Without indexing or decorrelation it can require O(n²) work and be worse than grouped aggregation.

[alternative.sql](alternative.sql)

```sql
SELECT DISTINCT a.NAME,
       (SELECT COUNT(*) FROM ANIMAL_INS AS b WHERE b.NAME = a.NAME) AS COUNT
FROM ANIMAL_INS AS a
WHERE a.NAME IS NOT NULL
  AND (SELECT COUNT(*) FROM ANIMAL_INS AS b WHERE b.NAME = a.NAME) >= 2
ORDER BY a.NAME;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "Lucy",
      3
    ],
    [
      "Raven",
      2
    ]
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 21개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 21 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

로컬 검증은 SQLite에서 공통 SQL과 필요한 함수의 호환 구현을 실행합니다. MySQL 서버의 실행 계획·collation 성능 측정은 포함하지 않습니다.

Local verification executes common SQL in SQLite with compatibility functions where needed. It does not measure a MySQL server’s query plan or collation performance.

원본 채점 기록: 100점. [submitted_original.sql](submitted_original.sql)는 당시 원본 파일을 그대로 보존하며, `solution.sql`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.sql](submitted_original.sql) preserves the original file bytes; `solution.sql` contains the documented implementation.

출처: [프로그래머스 문제 59041](https://school.programmers.co.kr/learn/courses/30/lessons/59041), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59041](https://school.programmers.co.kr/learn/courses/30/lessons/59041), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

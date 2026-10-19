# 대장균들의 자식의 수 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/299305) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

부모가 없는 PARENT_ID는 NULL입니다. 각 ID와 직접 자식 수를 출력하며 자식이 없으면 0, ID 오름차순입니다.

Root PARENT_ID values are NULL. Output each ID and its number of direct children, including zero, in ascending ID order.

## 풀이 흐름 / Approach

대장균 테이블을 부모와 자식 역할로 자기 조인합니다. 자식이 없는 부모도 남도록 LEFT JOIN을 사용하고 자식 ID만 셉니다.

Self-join the bacteria table in parent and child roles. LEFT JOIN retains individuals without children, and COUNT(child.ID) counts only actual children.

## 왜 맞는가 / Why it works

자식이 없으면 LEFT JOIN이 만든 확장 행에서 자식 ID는 NULL입니다. COUNT(c.ID)는 이를 0으로 세지만 COUNT(*)는 1로 세므로 바꾸면 안 됩니다.

For a childless parent, LEFT JOIN produces a null-extended child row. COUNT(c.ID) yields zero, while COUNT(*) would incorrectly count one.

## 비용 / Complexity

인덱스 없는 중첩 조인 최악 O(n²), PARENT_ID 인덱스·집계 계획이면 개선 / Unindexed nested-loop worst case O(n²); parent indexes and aggregation plans improve it

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- 부모 번호와 실제 자식 수 출력.
SELECT p.ID, COUNT(c.ID) AS CHILD_COUNT
FROM ECOLI_DATA AS p
-- 같은 테이블을 자식 c로 다시 조회해 부모 번호가 같은 행을 연결.
LEFT JOIN ECOLI_DATA AS c ON c.PARENT_ID = p.ID
GROUP BY p.ID
-- ORDER BY는 ID 오름차순 정렬.
ORDER BY p.ID
```

## 다른 방법: 부모별 자식 수를 먼저 집계 / Pre-aggregate child counts

PARENT_ID별 개수를 먼저 구해 부모 정보와 왼쪽 조인합니다. 자식 그룹이 없는 개체는 COALESCE로 0을 넣습니다.

Aggregate counts by PARENT_ID before left-joining them to all individuals. COALESCE supplies zero for missing child-count groups.

[alternative.sql](alternative.sql)

```sql
SELECT p.ID, COALESCE(c.CHILD_COUNT, 0) AS CHILD_COUNT
FROM ECOLI_DATA AS p
LEFT JOIN (
    SELECT PARENT_ID, COUNT(*) AS CHILD_COUNT
    FROM ECOLI_DATA
    WHERE PARENT_ID IS NOT NULL
    GROUP BY PARENT_ID
) AS c ON c.PARENT_ID = p.ID
ORDER BY p.ID;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      1,
      1
    ],
    [
      2,
      2
    ],
    [
      3,
      0
    ],
    [
      4,
      1
    ],
    [
      5,
      0
    ],
    [
      6,
      0
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

출처: [프로그래머스 문제 299305](https://school.programmers.co.kr/learn/courses/30/lessons/299305), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 299305](https://school.programmers.co.kr/learn/courses/30/lessons/299305), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

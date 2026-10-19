# 중복 제거하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59408) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

NAME은 NULL 가능하며 중복도 있습니다. NULL을 제외한 서로 다른 이름 수 한 값을 반환합니다.

NAME may be NULL and duplicated. Return one count of distinct non-NULL names.

## 풀이 흐름 / Approach

이름이 실제로 있는 동물들의 서로 다른 이름 수를 셉니다. COUNT(DISTINCT NAME)은 NULL을 제외하고 같은 이름을 한 번만 셉니다.

Count distinct present names. COUNT(DISTINCT NAME) ignores NULL and counts each repeated name once.

## 왜 맞는가 / Why it works

DISTINCT가 중복 이름을 하나로 묶고 COUNT(열)이 NULL을 제외하므로 두 요구 조건을 함께 만족합니다.

DISTINCT merges equal names and COUNT(column) excludes NULL, satisfying both requirements together.

## 비용 / Complexity

일반 계획 O(n) 스캔+고유값 집계; 정렬 방식이면 O(n log n) / Scan plus distinct aggregation; sort-based plans may take O(n log n)

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- AS는 별칭.
SELECT COUNT(DISTINCT NAME) AS count
FROM ANIMAL_INS
```

## 다른 방법: 중복 제거 후 행 수 계산 / Count rows after explicit deduplication

이름 NULL을 먼저 제외하고 DISTINCT 결과 행 수를 셉니다. 하나의 집계와 파생 관계로 나누어 표현한 차이가 있으며 같은 결과입니다.

Remove NULL names, build a DISTINCT derived relation, then count its rows. This splits the same logic into two explicit relational stages.

[alternative.sql](alternative.sql)

```sql
SELECT COUNT(*) AS count
FROM (SELECT DISTINCT NAME FROM ANIMAL_INS WHERE NAME IS NOT NULL) AS names;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
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

출처: [프로그래머스 문제 59408](https://school.programmers.co.kr/learn/courses/30/lessons/59408), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59408](https://school.programmers.co.kr/learn/courses/30/lessons/59408), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

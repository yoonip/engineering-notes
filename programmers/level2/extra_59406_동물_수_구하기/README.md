# 동물 수 구하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59406) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

ANIMAL_ID는 NULL이 아니고 이름은 NULL일 수 있습니다. 전체 동물 수 한 값을 반환합니다.

ANIMAL_ID is non-nullable while NAME may be NULL. Return a single count of all animals.

## 풀이 흐름 / Approach

한 행이 한 동물이므로 전체 행 수를 셉니다. 이름이 없는 동물도 포함해야 하므로 COUNT(NAME)이 아니라 COUNT(*)를 사용합니다.

Each row represents one animal, so count all rows. Missing names must not exclude animals; use COUNT(*) rather than COUNT(NAME).

## 정답이 되는 이유 / Why it works

COUNT(*)는 열 값의 NULL 여부와 관계없이 행 하나마다 1을 더하므로 전체 동물 수와 같습니다.

COUNT(*) adds one per row regardless of NULL column values, exactly matching the total number of animals.

## 비용 / Complexity

일반 집계 스캔 O(n); 스토리지 엔진·인덱스에 따라 달라짐 / Typical O(n) aggregate scan; engine and indexes affect the actual plan

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- 입소 동물 한 행이 한 마리.
SELECT COUNT(*) AS count
FROM ANIMAL_INS
```

## 다른 방법: NULL 불가 ID의 개수 / Count a non-nullable ID

공식 스키마에서 ANIMAL_ID가 NULL이 아니므로 COUNT(ANIMAL_ID)도 같은 값입니다. 이름 열처럼 NULL 가능한 열로 바꾸면 같은 결과를 보장할 수 없습니다.

ANIMAL_ID is non-nullable in the official schema, so COUNT(ANIMAL_ID) is equivalent. Substituting a nullable column such as NAME would not preserve the result.

[alternative.sql](alternative.sql)

```sql
SELECT COUNT(ANIMAL_ID) AS count
FROM ANIMAL_INS;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      4
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

출처: [프로그래머스 문제 59406](https://school.programmers.co.kr/learn/courses/30/lessons/59406), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59406](https://school.programmers.co.kr/learn/courses/30/lessons/59406), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

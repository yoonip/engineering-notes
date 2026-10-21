# 고양이와 개는 몇 마리 있을까

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59040) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

종류별 마릿수를 Cat 다음 Dog 순으로 출력합니다. 이름 없는 동물도 마릿수에 포함합니다.

Output counts by type, Cat before Dog, including animals without names.

## 풀이 흐름 / Approach

Cat과 Dog인 행을 종류별로 묶어 마릿수를 셉니다. 종류 이름 오름차순은 Cat 다음 Dog 순서이므로 고양이가 먼저 나옵니다.

Group Cat and Dog rows by animal type and count them. Alphabetic type ordering places Cat before Dog, as required.

## 정답이 되는 이유 / Why it works

동물 한 행은 한 종류 그룹에만 속합니다. COUNT(*)는 이름 유무와 관계없이 그 종류의 모든 동물을 셉니다.

Each animal belongs to one type group. COUNT(*) includes every animal of that type regardless of missing names.

## 비용 / Complexity

일반 스캔 O(n), 최대 2개 그룹 / Typical O(n) scan with at most two groups

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- COUNT(*)는 각 종의 동물 행 수, AS는 결과 별칭.
SELECT ANIMAL_TYPE, COUNT(*) AS count
FROM ANIMAL_INS
-- 고양이·개만 선택.
WHERE ANIMAL_TYPE IN ('Cat', 'Dog')
GROUP BY ANIMAL_TYPE
-- 문자열 오름차순에서 Cat이 Dog보다 앞서므로 고양이 먼저 출력.
ORDER BY ANIMAL_TYPE
```

## 다른 방법: 종별 집계의 UNION ALL / UNION ALL of separate per-type aggregates

고양이와 개를 따로 센 뒤 합칩니다. 해당 종류가 없는 경우 행을 만들지 않도록 HAVING을 두어 GROUP BY와 같은 결과를 유지합니다. 보통 두 번 스캔해 더 무겁습니다.

Count cats and dogs separately and union the results. HAVING suppresses absent types to match GROUP BY semantics. This typically scans twice and is heavier.

[alternative.sql](alternative.sql)

```sql
SELECT 'Cat' AS ANIMAL_TYPE, COUNT(*) AS count
FROM ANIMAL_INS WHERE ANIMAL_TYPE = 'Cat' HAVING COUNT(*) > 0
UNION ALL
SELECT 'Dog' AS ANIMAL_TYPE, COUNT(*) AS count
FROM ANIMAL_INS WHERE ANIMAL_TYPE = 'Dog' HAVING COUNT(*) > 0
ORDER BY ANIMAL_TYPE;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "Cat",
      2
    ],
    [
      "Dog",
      1
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

출처: [프로그래머스 문제 59040](https://school.programmers.co.kr/learn/courses/30/lessons/59040), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59040](https://school.programmers.co.kr/learn/courses/30/lessons/59040), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

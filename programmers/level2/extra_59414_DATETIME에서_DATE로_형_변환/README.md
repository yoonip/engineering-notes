# DATETIME에서 DATE로 형 변환

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59414) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

ANIMAL_INS의 ANIMAL_ID·NAME·DATETIME을 출력하며 시각은 YYYY-MM-DD입니다. ID 오름차순입니다.

Output ANIMAL_ID, NAME and DATETIME from ANIMAL_INS, formatting the timestamp as YYYY-MM-DD and ordering by ID.

## 풀이 흐름 / Approach

입소 시각에서 연·월·일만 YYYY-MM-DD 형식으로 출력합니다. 동물 ID와 이름은 그대로 유지하고 ID 오름차순으로 정렬합니다.

Display only year, month and day from the intake timestamp in YYYY-MM-DD format. Retain the ID and name and order rows by animal ID.

## 왜 맞는가 / Why it works

DATE_FORMAT은 행을 합치거나 제거하지 않고 각 시각을 요구한 표시 문자열로 바꿉니다. ORDER BY가 출력 순서를 확정합니다.

DATE_FORMAT transforms each timestamp into the requested string without removing or grouping rows. ORDER BY establishes the required output order.

## 비용 / Complexity

인덱스 없는 일반 계획: 스캔 O(n), 정렬 O(n log n); 실제 계획은 EXPLAIN으로 확인 / Typical unindexed scan O(n) plus O(n log n) sort; inspect EXPLAIN for the actual plan

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- AS는 결과 열 이름.
SELECT ANIMAL_ID, NAME, DATE_FORMAT(DATETIME, '%Y-%m-%d') AS DATETIME
FROM ANIMAL_INS
-- 동물 ID 오름차순 정렬.
ORDER BY ANIMAL_ID
```

## 다른 방법: DATE형 추출 / Extract a DATE value

DATE는 날짜 값을 반환하고 DATE_FORMAT은 형식화한 문자열을 반환합니다. 이 문제의 출력은 같지만 결과 자료형은 다릅니다. 어느 쪽이 항상 더 빠르다고 볼 수는 없습니다.

DATE returns a date value whereas DATE_FORMAT returns formatted text. The displayed result matches here, but result types differ; neither is universally faster.

[alternative.sql](alternative.sql)

```sql
SELECT ANIMAL_ID, NAME, DATE(DATETIME) AS DATETIME
FROM ANIMAL_INS
ORDER BY ANIMAL_ID;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "A349996",
      "Sugar",
      "2018-01-22"
    ],
    [
      "A350276",
      "Jewel",
      "2017-08-13"
    ],
    [
      "A350375",
      "Meo",
      "2017-03-06"
    ],
    [
      "A352555",
      "Harley",
      "2014-08-08"
    ],
    [
      "A352713",
      "Gia",
      "2017-04-13"
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

출처: [프로그래머스 문제 59414](https://school.programmers.co.kr/learn/courses/30/lessons/59414), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59414](https://school.programmers.co.kr/learn/courses/30/lessons/59414), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

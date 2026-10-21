# NULL 처리하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59410) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

ANIMAL_TYPE·이름·SEX_UPON_INTAKE를 ID순으로 출력합니다. 이름 NULL만 No name으로 바꾸고 빈 문자열은 유지합니다.

Output type, name and intake sex status in ID order, replacing only NULL names by No name and preserving empty strings.

## 풀이 흐름 / Approach

이름이 NULL인 경우에만 No name을 출력합니다. 빈 문자열과 NULL은 다르므로 빈 문자열을 바꾸지 않습니다. 출력 열에 ID가 없어도 ID로 정렬할 수 있습니다.

Replace only NULL names with No name. An empty string is different from NULL and is preserved. Ordering by ID is valid even when ID is not displayed.

## 정답이 되는 이유 / Why it works

COALESCE는 앞에서 처음 NULL이 아닌 값을 반환하므로 이름이 있으면 그대로, 없으면 대체 문자열이 됩니다.

COALESCE returns the first non-NULL argument, preserving present names and substituting only missing ones.

## 비용 / Complexity

인덱스 없는 일반 계획: O(n) 스캔+O(n log n) 정렬 / Typical unindexed O(n) scan plus O(n log n) sort

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- 이름이 NULL이면 대체 문자열 사용, AS는 열 이름 유지.
SELECT ANIMAL_TYPE, COALESCE(NAME, 'No name') AS NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
-- 출력에 ID 열이 없어도 ID 오름차순으로 정렬 가능.
ORDER BY ANIMAL_ID
```

## 다른 방법: CASE의 명시적 NULL 분기 / Explicit NULL branch with CASE

CASE WHEN NAME IS NULL로 두 경우를 직접 나눕니다. COALESCE보다 길지만 NULL 조건과 반환값이 그대로 드러나는 동등한 표현입니다.

Use CASE WHEN NAME IS NULL to spell out the two cases. It is longer than COALESCE but makes the condition and return value explicit.

[alternative.sql](alternative.sql)

```sql
SELECT ANIMAL_TYPE,
       CASE WHEN NAME IS NULL THEN 'No name' ELSE NAME END AS NAME,
       SEX_UPON_INTAKE
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
      "Cat",
      "Jewel",
      "Spayed Female"
    ],
    [
      "Cat",
      "Meo",
      "Neutered Male"
    ],
    [
      "Dog",
      "No name",
      "Spayed Female"
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

출처: [프로그래머스 문제 59410](https://school.programmers.co.kr/learn/courses/30/lessons/59410), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59410](https://school.programmers.co.kr/learn/courses/30/lessons/59410), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

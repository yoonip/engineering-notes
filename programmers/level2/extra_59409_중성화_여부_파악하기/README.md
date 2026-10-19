# 중성화 여부 파악하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59409) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

ID·이름·중성화 표시를 ID순으로 출력합니다. Neutered 또는 Spayed가 포함되면 O, 나머지는 X입니다.

Output ID, name and neutering indicator in ID order. Neutered or Spayed yields O, otherwise X.

## 풀이 흐름 / Approach

중성화 정보에 Neutered 또는 Spayed가 포함되면 O, 그렇지 않으면 X를 계산 열로 출력합니다. 중성화하지 않은 동물도 보여야 하므로 WHERE로 걸러내지 않습니다.

Produce O when the status contains Neutered or Spayed and X otherwise. Do not filter out unneutered animals, since both categories must remain in the output.

## 왜 맞는가 / Why it works

CASE의 조건은 요구한 두 표시 문자열의 포함 여부와 같으며, 각 입력 행에서 O 또는 X 하나를 만들어 전체 행을 보존합니다.

The CASE predicate matches either required status marker, producing one O/X value for every input row without dropping animals.

## 비용 / Complexity

문자 길이 d에 일반 스캔 O(nd), 정렬 O(n log n) / Typical O(nd) string scan plus O(n log n) sorting

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- SELECT는 동물 ID·이름과 이어지는 계산 열 출력.
SELECT ANIMAL_ID, NAME,
       CASE WHEN SEX_UPON_INTAKE LIKE '%Neutered%' OR SEX_UPON_INTAKE LIKE '%Spayed%'
            -- END는 CASE 종료, AS는 한글 열 별칭.
            THEN 'O' ELSE 'X' END AS `중성화`
FROM ANIMAL_INS
-- 동물 ID 오름차순 정렬.
ORDER BY ANIMAL_ID
```

## 다른 방법: IF와 부분 문자열 위치 / IF with substring positions

LOCATE의 양수 여부와 IF를 사용합니다. CASE보다 MySQL에 특화된 표현이며 이 조건에서는 동일한 결과를 냅니다.

Use positive LOCATE results with IF. This is more MySQL-specific than CASE and produces the same result for this predicate.

[alternative.sql](alternative.sql)

```sql
SELECT ANIMAL_ID, NAME,
       IF(LOCATE('Neutered', SEX_UPON_INTAKE) > 0
          OR LOCATE('Spayed', SEX_UPON_INTAKE) > 0, 'O', 'X') AS `중성화`
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
      "A355753",
      "Elijah",
      "O"
    ],
    [
      "A373219",
      "Ella",
      "O"
    ],
    [
      "A382192",
      "Maxwell 2",
      "X"
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

출처: [프로그래머스 문제 59409](https://school.programmers.co.kr/learn/courses/30/lessons/59409), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59409](https://school.programmers.co.kr/learn/courses/30/lessons/59409), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

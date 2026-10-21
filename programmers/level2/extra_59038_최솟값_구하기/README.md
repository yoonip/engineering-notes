# 최솟값 구하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59038) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

ANIMAL_INS에서 가장 이른 DATETIME 하나를 시간 열로 출력합니다.

Output the earliest DATETIME from ANIMAL_INS in the 시간 column.

## 풀이 흐름 / Approach

입소 시각 중 가장 작은 값을 구합니다. 시각의 순서는 연·월·일·시·분·초 순서이므로 최솟값이 가장 먼저 들어온 시각입니다.

Find the minimum intake timestamp. Chronological timestamp order makes the minimum the earliest intake time.

## 정답이 되는 이유 / Why it works

다른 열의 정보를 요구하지 않으므로 행 전체를 찾을 필요가 없습니다. MIN(DATETIME)은 필요한 시각 하나를 직접 반환합니다.

No other columns are requested, so the entire animal row is unnecessary. MIN(DATETIME) directly returns the required timestamp.

## 비용 / Complexity

일반 스캔 O(n); 시각 인덱스로 최솟값 접근 가능 / Typical O(n) scan; a timestamp index may support direct minimum access

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- AS는 출력 이름, 백틱은 한글 식별자 표시.
SELECT MIN(DATETIME) AS `시간`
FROM ANIMAL_INS
```

## 다른 방법: 정렬한 첫 값을 스칼라 조회 / Scalar query of the first sorted value

시각을 정렬해 첫 값을 고릅니다. 바깥 스칼라 조회를 두어 빈 테이블에서도 MIN처럼 NULL 한 행을 반환합니다. 일반 정렬은 MIN보다 많은 작업입니다.

Select the first sorted timestamp. A scalar outer query preserves MIN’s one-NULL-row result on an empty table. A general sort does more work than MIN.

[alternative.sql](alternative.sql)

```sql
SELECT (SELECT DATETIME FROM ANIMAL_INS ORDER BY DATETIME LIMIT 1) AS `시간`;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "2013-10-14 15:38:00"
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

출처: [프로그래머스 문제 59038](https://school.programmers.co.kr/learn/courses/30/lessons/59038), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59038](https://school.programmers.co.kr/learn/courses/30/lessons/59038), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

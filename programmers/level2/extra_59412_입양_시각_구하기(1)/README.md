# 입양 시각 구하기(1)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59412) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

ANIMAL_OUTS에서 시각 9~19시(양끝 포함)의 건수를 시간별로 출력합니다. HOUR·COUNT 열, HOUR 오름차순입니다.

Count ANIMAL_OUTS adoptions for hours 9–19 inclusive. Output HOUR and COUNT ordered by HOUR.

## 풀이 흐름 / Approach

입양 시각의 시(hour)가 9 이상 19 이하인 행만 남깁니다. 같은 시각대끼리 묶어 입양 건수를 세고 시각 순으로 출력합니다. 19시 59분도 포함됩니다.

Keep adoption rows whose hour is between 9 and 19 inclusive. Group by hour, count rows and order by hour. An adoption at 19:59 is included.

## 왜 맞는가 / Why it works

필터는 요청 시간대와 같고 각 행은 하나의 시간 그룹에만 속합니다. COUNT(*)는 이름 NULL 여부와 무관하게 모든 입양을 셉니다.

The filter matches the requested hour range, and each row belongs to exactly one hourly group. COUNT(*) counts every adoption regardless of nullable names.

## 비용 / Complexity

인덱스 없는 일반 계획: O(n) 스캔, 최대 11개 그룹 / Typical unindexed O(n) scan with at most 11 groups

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- SELECT는 출력 열, HOUR는 시각의 시간 0~23 추출, COUNT(*)는 입양 건수, AS는 결과 별칭.
SELECT HOUR(DATETIME) AS HOUR, COUNT(*) AS COUNT
FROM ANIMAL_OUTS
-- 9시부터 19시 59분 59초까지 선택.
WHERE HOUR(DATETIME) BETWEEN 9 AND 19
GROUP BY HOUR(DATETIME)
-- 시간 숫자 오름차순 정렬.
ORDER BY HOUR
```

## 다른 방법: 시간 추출 파생 테이블 / Derived table for extracted hours

시각 추출을 파생 테이블에 분리합니다. 의미가 단계적으로 보이지만 MySQL 옵티마이저가 합칠 수 있으므로 실행 계획의 성능 차이를 단정하지 않습니다.

Separate hour extraction into a derived table. This exposes the logical stages, though MySQL may merge them, so a different runtime plan is not guaranteed.

[alternative.sql](alternative.sql)

```sql
SELECT extracted.hour_value AS HOUR, COUNT(*) AS COUNT
FROM (SELECT HOUR(DATETIME) AS hour_value FROM ANIMAL_OUTS) AS extracted
WHERE extracted.hour_value >= 9 AND extracted.hour_value < 20
GROUP BY extracted.hour_value
ORDER BY extracted.hour_value;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      10,
      1
    ],
    [
      13,
      1
    ],
    [
      14,
      1
    ],
    [
      15,
      1
    ]
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 20개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 20 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

로컬 검증은 SQLite에서 공통 SQL과 필요한 함수의 호환 구현을 실행합니다. MySQL 서버의 실행 계획·collation 성능 측정은 포함하지 않습니다.

Local verification executes common SQL in SQLite with compatibility functions where needed. It does not measure a MySQL server’s query plan or collation performance.

원본 채점 기록: 100점. [submitted_original.sql](submitted_original.sql)는 당시 원본 파일을 그대로 보존하며, `solution.sql`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.sql](submitted_original.sql) preserves the original file bytes; `solution.sql` contains the documented implementation.

출처: [프로그래머스 문제 59412](https://school.programmers.co.kr/learn/courses/30/lessons/59412), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59412](https://school.programmers.co.kr/learn/courses/30/lessons/59412), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

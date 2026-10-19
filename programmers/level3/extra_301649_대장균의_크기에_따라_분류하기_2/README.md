# 대장균의 크기에 따라 분류하기 2

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/301649) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

전체 행 수는 4의 배수이고 같은 크기가 분류 경계를 가로지르지 않습니다. 큰 순서부터 4등분해 CRITICAL,HIGH,MEDIUM,LOW를 붙이고 ID순으로 출력합니다.

The row count is divisible by four and equal sizes never cross group boundaries. Divide descending sizes into four equal-count groups labeled CRITICAL,HIGH,MEDIUM,LOW, then order by ID.

## 풀이 흐름 / Approach

크기 내림차순으로 정렬한 개체를 NTILE(4)로 같은 수의 네 그룹에 나눕니다. 그룹 번호 1~4를 CRITICAL·HIGH·MEDIUM·LOW에 대응시키고 ID순으로 출력합니다.

Use NTILE(4) over descending colony sizes to divide individuals into four equally sized groups. Map groups 1–4 to CRITICAL, HIGH, MEDIUM and LOW, then order by ID.

## 왜 맞는가 / Why it works

총 행 수가 4의 배수이고 같은 크기가 분류 경계를 가로지르지 않는다는 조건 덕분에 네 그룹이 정확한 사분위 분류입니다. NTILE을 크기 값의 사분위수와 혼동하지 않습니다.

The row count is divisible by four and equal sizes never cross classification boundaries, so four equal-count buckets exactly implement the categories. NTILE is a row bucket operation, not a numerical-size quantile calculation.

## 비용 / Complexity

일반 윈도 정렬 O(n log n), 공간 O(n) / Typical O(n log n) window sort and O(n) workspace

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
SELECT ID,
       -- NTILE(4)는 행을 네 균등 그룹으로 나누는 윈도 함수, OVER는 적용 순서, DESC는 크기 내림차순.
       CASE NTILE(4) OVER (ORDER BY SIZE_OF_COLONY DESC)
           WHEN 1 THEN 'CRITICAL'
           -- 두 번째 25% 그룹의 이름.
           WHEN 2 THEN 'HIGH'
           WHEN 3 THEN 'MEDIUM'
           ELSE 'LOW'
       -- AS는 출력 열에 별칭 부여.
       END AS COLONY_NAME
FROM ECOLI_DATA
ORDER BY ID
```

## 다른 방법: 행 번호와 전체 행 수 / Row numbers and total row count

ROW_NUMBER와 COUNT OVER로 각 행의 순번을 전체 개수의 1/4·1/2·3/4와 비교합니다. NTILE 대신 분류 경계를 식으로 드러냅니다.

Compare ROW_NUMBER with one quarter, one half and three quarters of COUNT OVER. This exposes bucket boundaries explicitly instead of using NTILE.

[alternative.sql](alternative.sql)

```sql
WITH ranked AS (
    SELECT ID, ROW_NUMBER() OVER (ORDER BY SIZE_OF_COLONY DESC) AS rn,
           COUNT(*) OVER () AS total
    FROM ECOLI_DATA
)
SELECT ID,
       CASE WHEN 4 * rn <= total THEN 'CRITICAL'
            WHEN 2 * rn <= total THEN 'HIGH'
            WHEN 4 * rn <= 3 * total THEN 'MEDIUM'
            ELSE 'LOW' END AS COLONY_NAME
FROM ranked
ORDER BY ID;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      1,
      "MEDIUM"
    ],
    [
      2,
      "LOW"
    ],
    [
      3,
      "HIGH"
    ],
    [
      4,
      "MEDIUM"
    ],
    [
      5,
      "HIGH"
    ],
    [
      6,
      "CRITICAL"
    ],
    [
      7,
      "CRITICAL"
    ],
    [
      8,
      "LOW"
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

출처: [프로그래머스 문제 301649](https://school.programmers.co.kr/learn/courses/30/lessons/301649), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 301649](https://school.programmers.co.kr/learn/courses/30/lessons/301649), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

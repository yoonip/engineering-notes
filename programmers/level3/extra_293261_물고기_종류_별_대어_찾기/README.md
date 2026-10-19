# 물고기 종류 별 대어 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/293261) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

종류별 최대 물고기는 유일하며 그 길이는 10cm를 넘습니다. 종류 이름을 조인해 ID·FISH_NAME·LENGTH를 ID순으로 출력합니다.

Each species has a unique largest fish longer than 10cm. Join its species name and output ID,FISH_NAME,LENGTH ordered by ID.

## 풀이 흐름 / Approach

각 물고기의 길이를 같은 종류의 최대 길이와 비교합니다. 최대인 행에 종류 이름을 조인하고 ID순으로 출력합니다. NULL 길이는 최대 길이와의 비교가 참이 되지 않습니다.

Compare each fish’s length with the maximum within its species. Join the species name for matching rows and sort by ID. NULL lengths cannot satisfy that equality.

## 왜 맞는가 / Why it works

상관 서브쿼리는 현재 행과 같은 종류만 보므로 종류별 최댓값을 정확히 구합니다. 공식 조건에서 종류별 최대 물고기는 유일하므로 종류당 한 행이 남습니다.

The correlated subquery restricts itself to the current species, giving its exact maximum. The official uniqueness condition leaves one largest fish per species.

## 비용 / Complexity

상관 조회의 비최적화 최악 O(n²); 인덱스·옵티마이저에 의존 / Unoptimized correlated-query worst case O(n²); indexes and decorrelation affect cost

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- 점(.)은 테이블 별칭의 열을 지정.
SELECT f.ID, names.FISH_NAME, f.LENGTH
FROM FISH_INFO AS f
-- JOIN·ON은 같은 종류 번호를 가진 이름 정보를 연결.
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
WHERE f.LENGTH = (
    -- 같은 종류의 최대 길이 계산.
    SELECT MAX(other.LENGTH)
    FROM FISH_INFO AS other
    -- 바깥 행 f의 종류만 검사하는 상관 하위 쿼리.
    WHERE other.FISH_TYPE = f.FISH_TYPE
)
ORDER BY f.ID
```

## 다른 방법: 종류별 MAX 집계 후 조인 / Join a pre-aggregated maximum table

종류별 최대 길이를 한 번 집계한 결과에 물고기 정보를 조인합니다. 반복 상관 조회를 명시적 그룹·조인으로 바꾼 방식이며 실제 차이는 실행 계획으로 봅니다.

Aggregate the maximum once per species, then join fish and names to it. This expresses repeated correlation as grouping plus joins; actual gains depend on the execution plan.

[alternative.sql](alternative.sql)

```sql
SELECT f.ID, names.FISH_NAME, f.LENGTH
FROM FISH_INFO AS f
JOIN (SELECT FISH_TYPE, MAX(LENGTH) AS maximum FROM FISH_INFO GROUP BY FISH_TYPE) AS maxima
  ON maxima.FISH_TYPE = f.FISH_TYPE AND maxima.maximum = f.LENGTH
JOIN FISH_NAME_INFO AS names ON names.FISH_TYPE = f.FISH_TYPE
ORDER BY f.ID;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      6,
      "BASS",
      60
    ],
    [
      8,
      "ANCHOVY",
      73
    ],
    [
      9,
      "SNAPPER",
      73
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

출처: [프로그래머스 문제 293261](https://school.programmers.co.kr/learn/courses/30/lessons/293261), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 293261](https://school.programmers.co.kr/learn/courses/30/lessons/293261), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

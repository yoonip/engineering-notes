# 특정 조건을 만족하는 물고기별 수와 최대 길이 구하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/298519) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

10cm 이하 길이는 NULL이며 평균에서 10으로 취급합니다. 평균≥33cm 종류의 전체 마릿수·최대 길이·종류를 출력하고 종류 오름차순입니다.

Lengths at most 10cm are NULL and count as ten in the average. Output total fish count, maximum length and type for species averaging at least 33cm, ordered by type.

## 풀이 흐름 / Approach

종류별로 전체 마릿수와 최대 길이를 구합니다. 평균에만 NULL 길이를 10cm로 바꿔 33cm 이상인 그룹을 남깁니다. 짧은 물고기도 마릿수의 분모에 포함해야 합니다.

Group by species to count all fish and obtain maximum length. Replace NULL lengths by 10cm only for the average and keep groups averaging at least 33cm. Short fish still belong in the denominator.

## 정답이 되는 이유 / Why it works

AVG는 원래 NULL을 무시하므로 먼저 10으로 바꿔야 문제의 평균입니다. MAX는 실제 측정 최대 길이이고 qualifying 그룹에는 33 이상 값이 반드시 있어 NULL 보정이 최대값을 바꾸지 않습니다.

AVG normally ignores NULL, so replacing it with ten is essential. MAX uses measured lengths; a qualifying group must include a value at least 33, so the NULL substitution cannot alter its maximum.

## 비용 / Complexity

일반 O(n) 스캔·집계+종류 g 정렬 O(g log g) / Typical O(n) scan/aggregation plus O(g log g) group sort

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- COUNT(*)는 행 수, MAX는 최댓값, AS는 출력 열 별칭.
SELECT COUNT(*) AS FISH_COUNT, MAX(LENGTH) AS MAX_LENGTH, FISH_TYPE
FROM FISH_INFO
-- 종류가 같은 물고기끼리 묶어 집계.
GROUP BY FISH_TYPE
HAVING AVG(COALESCE(LENGTH, 10)) >= 33
-- 종류 번호 오름차순 정렬.
ORDER BY FISH_TYPE
```

## 다른 방법: 합과 개수로 평균 조건 작성 / Express the average threshold through sum and count

AVG 대신 SUM(COALESCE(...))≥33×COUNT(*)로 판정합니다. 같은 수학적 조건이며 NULL을 분모에서 빼지 않도록 전체 행 수를 씁니다.

Replace AVG with SUM(COALESCE(...))≥33×COUNT(*). It is the same mathematical threshold and explicitly keeps all rows in the denominator.

[alternative.sql](alternative.sql)

```sql
SELECT COUNT(*) AS FISH_COUNT, MAX(LENGTH) AS MAX_LENGTH, FISH_TYPE
FROM FISH_INFO
GROUP BY FISH_TYPE
HAVING SUM(COALESCE(LENGTH, 10)) >= 33 * COUNT(*)
ORDER BY FISH_TYPE;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      3,
      50,
      0
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

출처: [프로그래머스 문제 298519](https://school.programmers.co.kr/learn/courses/30/lessons/298519), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 298519](https://school.programmers.co.kr/learn/courses/30/lessons/298519), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

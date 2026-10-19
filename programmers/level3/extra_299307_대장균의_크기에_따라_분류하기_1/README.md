# 대장균의 크기에 따라 분류하기 1

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/299307) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

크기≤100은 LOW,100<크기≤1000은 MEDIUM,1000 초과는 HIGH입니다. ID·SIZE를 ID순으로 출력합니다.

Size≤100 is LOW, 100<size≤1000 is MEDIUM, and size>1000 is HIGH. Output ID and SIZE ordered by ID.

## 풀이 흐름 / Approach

크기가 100 이하인지 먼저 확인하고, 아니면 1000 이하인지 확인합니다. 앞 조건을 이미 통과하지 않았으므로 두 번째 조건에 100 초과를 다시 쓰지 않아도 됩니다.

First check whether size is at most 100, then whether it is at most 1000. Failing the first branch already implies greater than 100.

## 정답이 되는 이유 / Why it works

CASE는 처음 참인 조건의 결과를 반환합니다. 따라서 ≤100, 100~1000, >1000 세 구간이 겹치지 않고 모든 크기를 포함합니다.

CASE returns the first matching branch. The three resulting intervals are disjoint and exhaust all non-null sizes.

## 비용 / Complexity

일반 스캔 O(n), ID 정렬 O(n log n) / Typical O(n) scan plus O(n log n) ID sort

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
SELECT ID,
       CASE
           -- 작은따옴표는 문자열.
           WHEN SIZE_OF_COLONY <= 100 THEN 'LOW'
           WHEN SIZE_OF_COLONY <= 1000 THEN 'MEDIUM'
           ELSE 'HIGH'
       END AS SIZE
-- FROM은 조회할 테이블 지정.
FROM ECOLI_DATA
ORDER BY ID
```

## 다른 방법: 구간별 UNION ALL / UNION ALL of disjoint ranges

세 구간을 각각 필터하고 합칩니다. 조건을 빠뜨리지 않도록 100·1000 경계를 명시합니다. 일반적으로 여러 번 읽어 CASE 한 번보다 유리하지 않습니다.

Filter each of the three disjoint ranges and combine them. The 100 and 1000 boundaries are explicit, but multiple scans are generally no advantage over one CASE.

[alternative.sql](alternative.sql)

```sql
SELECT ID, 'LOW' AS SIZE FROM ECOLI_DATA WHERE SIZE_OF_COLONY <= 100
UNION ALL
SELECT ID, 'MEDIUM' AS SIZE FROM ECOLI_DATA WHERE SIZE_OF_COLONY > 100 AND SIZE_OF_COLONY <= 1000
UNION ALL
SELECT ID, 'HIGH' AS SIZE FROM ECOLI_DATA WHERE SIZE_OF_COLONY > 1000
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
      "LOW"
    ],
    [
      2,
      "MEDIUM"
    ],
    [
      3,
      "HIGH"
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

출처: [프로그래머스 문제 299307](https://school.programmers.co.kr/learn/courses/30/lessons/299307), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 299307](https://school.programmers.co.kr/learn/courses/30/lessons/299307), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

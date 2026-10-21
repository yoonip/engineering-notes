# 업그레이드 할 수 없는 아이템 구하기

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/273712) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

루트의 PARENT_ITEM_ID는 NULL이며 각 아이템의 부모는 최대 하나입니다. 더 업그레이드할 자식이 없는 아이템의 ID·이름·희귀도를 ID 내림차순으로 출력합니다.

Root parent IDs are NULL and each item has at most one parent. Output ID,name,rarity for childless terminal items in descending ID order.

## 풀이 흐름 / Approach

현재 아이템을 부모로 가지는 다음 아이템이 있는지 확인합니다. LEFT JOIN에서 자식 행이 연결되지 않은 아이템만 남기면 더 업그레이드할 수 없는 끝 아이템입니다.

Check whether any next item has the current item as its parent. Keep only items with no matching child in the LEFT JOIN; these are terminal upgrades.

## 정답이 되는 이유 / Why it works

더 업그레이드할 수 없다는 것은 자신의 ID가 다른 아이템의 부모 ID로 등장하지 않는다는 뜻입니다. 자식 ITEM_ID의 NULL 여부는 바로 이 부재 조건을 나타냅니다.

A terminal item is one whose ID never appears as another item’s parent. A null child ITEM_ID in the left join represents exactly that absence.

## 비용 / Complexity

인덱스 없는 중첩 검사 최악 O(it), 부모 인덱스·안티조인 계획이면 개선 / Unindexed nested-check worst case O(it); parent indexes and antijoin plans improve it

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- i.는 아이템 정보 테이블의 열 지정.
SELECT i.ITEM_ID, i.ITEM_NAME, i.RARITY
FROM ITEM_INFO AS i
-- 자식이 없어도 현재 행 유지.
LEFT JOIN ITEM_TREE AS child ON child.PARENT_ITEM_ID = i.ITEM_ID
WHERE child.ITEM_ID IS NULL
-- DESC는 큰 값부터.
ORDER BY i.ITEM_ID DESC
```

## 다른 방법: NOT EXISTS 안티조인 / NOT EXISTS antijoin

자식이 존재하지 않는 조건을 직접 적습니다. NULL 부모가 있는 NOT IN과 달리 NULL 때문에 모든 행이 사라지는 문제가 없습니다.

State the absence of a child directly with NOT EXISTS. Unlike a naive NOT IN over nullable parents, NULL does not invalidate every comparison.

[alternative.sql](alternative.sql)

```sql
SELECT i.ITEM_ID, i.ITEM_NAME, i.RARITY
FROM ITEM_INFO AS i
WHERE NOT EXISTS (
    SELECT 1 FROM ITEM_TREE AS child WHERE child.PARENT_ITEM_ID = i.ITEM_ID
)
ORDER BY i.ITEM_ID DESC;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      4,
      "ITEM_E",
      "RARE"
    ],
    [
      3,
      "ITEM_D",
      "RARE"
    ],
    [
      2,
      "ITEM_C",
      "LEGEND"
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

출처: [프로그래머스 문제 273712](https://school.programmers.co.kr/learn/courses/30/lessons/273712), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 273712](https://school.programmers.co.kr/learn/courses/30/lessons/273712), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

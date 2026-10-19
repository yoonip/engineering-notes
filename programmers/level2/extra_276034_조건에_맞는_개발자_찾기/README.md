# 조건에 맞는 개발자 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/276034) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

Python 또는 C# 기술 비트를 가진 개발자 정보를 찾습니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. Python 또는 C# 기술 비트를 가진 개발자 정보를 찾습니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `SKILLCODES`: `NAME`, `CATEGORY`, `CODE`
- `DEVELOPERS`: `ID`, `FIRST_NAME`, `LAST_NAME`, `EMAIL`, `SKILL_CODE`

## 풀이를 따라가기

기술 코드 표에서 두 언어에 해당하는 행을 찾습니다. 개발자 코드와 비트 AND한 값이 0이 아닌 행이 있는지 EXISTS로 확인합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 기술 코드 표에서 두 언어에 해당하는 행을 찾는다. 개발자 코드와 비트 AND한 값이 0이 아닌 행이 있는지 EXISTS로 확인한다.
SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME
FROM DEVELOPERS AS d
WHERE EXISTS (
    SELECT 1
    FROM SKILLCODES AS s
    WHERE s.NAME IN ('Python', 'C#')
      AND (d.SKILL_CODE & s.CODE) <> 0
)
ORDER BY d.ID
```

## 정답이 되는 이유

기술 코드의 각 비트는 보유 기술을 나타냅니다. Python 또는 C# 코드와 AND가 0이 아니면 둘 중 하나를 가진 것입니다. EXISTS는 두 기술을 모두 가져도 개발자를 한 번만 남깁니다.

개발자 D명과 기술 S개를 단순 중첩 검사하면 O(DS), 대안은 기술 마스크 집계 O(S) 뒤 D명을 검사합니다. R명 결과 비교 정렬 O(R log R)은 별도입니다.

주의할 점: 두 언어를 모두 아는 개발자도 한 번만 출력합니다. 기술 코드를 일반 숫자 대소 비교로 검사하지 않습니다.

## 다른 방법: 목표 비트 합집합 후 한 번 검사

```sql
SELECT d.ID,d.EMAIL,d.FIRST_NAME,d.LAST_NAME
FROM DEVELOPERS d
CROSS JOIN (SELECT BIT_OR(CODE) AS MASK FROM SKILLCODES WHERE NAME IN ('Python','C#')) s
WHERE (d.SKILL_CODE & s.MASK)<>0 ORDER BY d.ID;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 기술 코드 표에서 두 언어에 해당하는 행을 찾습니다. 개발자 코드와 비트 AND한 값이 0이 아닌 행이 있는지 EXISTS로 확인합니다. | 목표 비트 합집합 후 한 번 검사 |
| 비용 | 개발자 D명과 기술 S개를 단순 중첩 검사하면 O(DS), 대안은 기술 마스크 집계 O(S) 뒤 D명을 검사합니다. R명 결과 비교 정렬 O(R log R)은 별도입니다. | 기술 코드들을 BIT_OR로 한 번 합친 뒤 개발자마다 한 번 AND합니다. 단순 중첩 EXISTS 검사와 연산 횟수가 다릅니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find developers having the Python or C# skill bit.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Find developers having the Python or C# skill bit.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `SKILLCODES`: `NAME`, `CATEGORY`, `CODE`
- `DEVELOPERS`: `ID`, `FIRST_NAME`, `LAST_NAME`, `EMAIL`, `SKILL_CODE`

### Approach

Look up the two language codes and use EXISTS to test whether any target bit intersects a developer’s skill code.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Skill bits encode membership. A nonzero AND with Python or C# indicates at least one requested skill. EXISTS retains each developer once even when both match.

A simple nested check costs O(DS) for D developers and S skills. The alternative builds one mask in O(S) then checks D developers. Sorting R results adds O(R log R) comparisons.

Boundary cases: A developer knowing both languages appears once. Do not compare skill codes by numeric magnitude.

### Alternative: Aggregate the target skill mask before filtering

Combine requested codes once with BIT_OR, then apply one AND per developer instead of a simple nested check.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 조건에 맞는 개발자 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/276034) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

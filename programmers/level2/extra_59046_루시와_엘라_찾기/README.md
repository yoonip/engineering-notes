# 루시와 엘라 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59046) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

대상 이름은 Lucy,Ella,Pickle,Rogan,Sabrina,Mitty입니다. ID·이름·성별 상태를 ID순으로 출력합니다.

Target names are Lucy,Ella,Pickle,Rogan,Sabrina,Mitty. Output ID, name and sex status ordered by ID.

## 풀이 흐름 / Approach

이름이 제시된 여섯 문자열 중 하나와 같은 동물을 고릅니다. 일부만 포함하는 검색이 아니라 전체 이름의 동등 비교입니다. ID 오름차순으로 출력합니다.

Select animals whose complete name equals one of the six listed names. This is exact-name membership, not substring matching. Order by animal ID.

## 왜 맞는가 / Why it works

IN은 나열된 값과의 동등 비교를 OR로 연결한 조건과 같습니다. 정확히 대상 이름인 행만 남습니다.

IN is equivalent to OR-combining equalities against the listed values, retaining exactly the requested names.

## 비용 / Complexity

일반 스캔 O(n), 정렬 O(k log k); 이름 인덱스 사용 여부는 계획 의존 / Typical O(n) scan and O(k log k) sort; name-index use is plan-dependent

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- SELECT는 동물 ID·이름·성별과 중성화 정보를 출력.
SELECT ANIMAL_ID, NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
-- IN은 이름이 제시된 여섯 문자열 중 하나와 같은지 검사.
WHERE NAME IN ('Lucy', 'Ella', 'Pickle', 'Rogan', 'Sabrina', 'Mitty')
ORDER BY ANIMAL_ID
```

## 다른 방법: 개별 동등 조건의 OR / Explicit OR of equalities

각 이름을 =로 비교해 OR로 묶습니다. 동일한 관계 조건의 다른 표현이며 IN보다 길어 성능 개선을 기대할 이유는 없습니다.

Spell out each equality joined by OR. This is the same relational predicate in a longer form, with no inherent performance advantage over IN.

[alternative.sql](alternative.sql)

```sql
SELECT ANIMAL_ID, NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
WHERE NAME = 'Lucy' OR NAME = 'Ella' OR NAME = 'Pickle'
   OR NAME = 'Rogan' OR NAME = 'Sabrina' OR NAME = 'Mitty'
ORDER BY ANIMAL_ID;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "A373219",
      "Ella",
      "Spayed Female"
    ],
    [
      "A377750",
      "Lucy",
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

출처: [프로그래머스 문제 59046](https://school.programmers.co.kr/learn/courses/30/lessons/59046), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59046](https://school.programmers.co.kr/learn/courses/30/lessons/59046), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

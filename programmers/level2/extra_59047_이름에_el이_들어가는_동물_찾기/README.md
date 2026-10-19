# 이름에 el이 들어가는 동물 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/59047) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

개 중 이름에 대소문자 없이 el이 포함된 동물의 ID·이름을 이름순으로 출력합니다.

Output IDs and names of dogs containing el case-insensitively, ordered by name.

## 풀이 흐름 / Approach

종류가 Dog이고 이름에 대소문자 구분 없이 el이 포함된 행을 찾습니다. 검색용 이름만 소문자로 바꾸고 출력 이름은 원래대로 유지합니다.

Find dogs whose names contain el without regard to case. Lowercase only the search expression and preserve the original displayed name.

## 왜 맞는가 / Why it works

두 WHERE 조건의 AND가 개이면서 이름 조건을 만족하는 교집합을 고릅니다. NULL 이름은 포함 비교가 참이 아니어서 자동으로 제외됩니다.

The AND of the predicates selects exactly dogs satisfying the name condition. A NULL name cannot make the substring predicate true and is excluded.

## 비용 / Complexity

이름 길이 d에 O(nd) 스캔, 출력 k행 정렬 O(k log k) / O(nd) scan and O(k log k) output sorting

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- SELECT는 동물 ID·이름 출력.
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
-- 개만 선택.
WHERE ANIMAL_TYPE = 'Dog'
  AND LOWER(NAME) LIKE '%el%'
-- 이름 오름차순, 이름 동점이면 ID 오름차순.
ORDER BY NAME, ANIMAL_ID
```

## 다른 방법: LOCATE로 부분 문자열 찾기 / Substring search with LOCATE

LIKE 패턴 대신 LOCATE 위치가 0보다 큰지 확인합니다. 앞뒤 %를 쓰는 의미와 같고, 인덱스를 자동으로 더 잘 쓰는 변경은 아닙니다.

Check whether LOCATE returns a positive position instead of using a LIKE pattern. It has the same containment meaning and does not automatically improve index use.

[alternative.sql](alternative.sql)

```sql
SELECT ANIMAL_ID, NAME
FROM ANIMAL_INS
WHERE ANIMAL_TYPE = 'Dog' AND LOCATE('el', LOWER(NAME)) > 0
ORDER BY NAME, ANIMAL_ID;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "A355753",
      "Elijah"
    ],
    [
      "A382192",
      "Maxwell 2"
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

출처: [프로그래머스 문제 59047](https://school.programmers.co.kr/learn/courses/30/lessons/59047), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 59047](https://school.programmers.co.kr/learn/courses/30/lessons/59047), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

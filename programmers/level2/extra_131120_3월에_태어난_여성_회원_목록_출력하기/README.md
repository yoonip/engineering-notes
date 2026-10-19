# 3월에 태어난 여성 회원 목록 출력하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131120) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

전화번호가 있는 3월생 여성 회원 정보를 조회한다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 전화번호가 있는 3월생 여성 회원 정보를 조회한다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `MEMBER_PROFILE`: `MEMBER_ID`, `MEMBER_NAME`, `TLNO`, `GENDER`, `DATE_OF_BIRTH`

## 풀이를 따라가기

성별·생일 월·전화번호 NOT NULL 조건을 동시에 적용한다. 생일을 YYYY-MM-DD로 표시하고 회원 ID순으로 정렬한다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 성별·생일 월·전화번호 NOT NULL 조건을 동시에 적용한다. 생일을 YYYY-MM-DD로 표시하고 회원 ID순으로 정렬한다.
SELECT MEMBER_ID, MEMBER_NAME, GENDER, DATE_FORMAT(DATE_OF_BIRTH, '%Y-%m-%d') AS DATE_OF_BIRTH
FROM MEMBER_PROFILE
WHERE GENDER = 'W'
  AND MONTH(DATE_OF_BIRTH) = 3
  AND TLNO IS NOT NULL
ORDER BY MEMBER_ID
```

## 왜 맞는가

AND로 연결한 세 조건을 모두 만족하는 회원만 남긴다. 날짜 형식 변경은 표시만 바꾸며, 출력 순서는 MEMBER_ID로 결정한다.

N명 검사와 R명 결과 정렬이 필요하다. 비교 정렬은 O(R log R)이며 날짜 함수와 인덱스 사용 여부에 따라 검색 비용이 달라진다.

주의할 점: NULL은 빈 문자열과 다르다. 생년이 아니라 생일 월이 3인지 검사한다.

## 다른 방법: 조건 ID 집합 INTERSECT 대신 EXISTS 세미 조인

```sql
WITH eligible AS (
    SELECT MEMBER_ID FROM MEMBER_PROFILE
    WHERE GENDER='W' AND MONTH(DATE_OF_BIRTH)=3 AND TLNO IS NOT NULL
)
SELECT m.MEMBER_ID,m.MEMBER_NAME,m.GENDER,
       DATE_FORMAT(m.DATE_OF_BIRTH,'%Y-%m-%d') AS DATE_OF_BIRTH
FROM MEMBER_PROFILE m
WHERE EXISTS (SELECT 1 FROM eligible e WHERE e.MEMBER_ID=m.MEMBER_ID)
ORDER BY m.MEMBER_ID;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 성별·생일 월·전화번호 NOT NULL 조건을 동시에 적용한다. 생일을 YYYY-MM-DD로 표시하고 회원 ID순으로 정렬한다. | 조건 ID 집합 INTERSECT 대신 EXISTS 세미 조인 |
| 비용 | N명 검사와 R명 결과 정렬이 필요하다. 비교 정렬은 O(R log R)이며 날짜 함수와 인덱스 사용 여부에 따라 검색 비용이 달라진다. | 같은 조건으로 고른 회원을 EXISTS로 다시 확인한다. 더 빠른 풀이로 간주하지 않으며 단순 WHERE와 실행계획을 비교한다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Return female members born in March who have a phone number.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Return female members born in March who have a phone number.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `MEMBER_PROFILE`: `MEMBER_ID`, `MEMBER_NAME`, `TLNO`, `GENDER`, `DATE_OF_BIRTH`

### Approach

Apply gender, birth month and non-NULL phone predicates together. Format birth dates as YYYY-MM-DD and sort by member ID.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

All three AND-connected predicates must hold. Date formatting changes presentation only; MEMBER_ID determines output order.

Inspect N members and order R results. Comparison sorting costs O(R log R); date expressions and index access affect filtering.

Boundary cases: NULL and an empty string are different. Test the birth month, not the birth year.

### Alternative: EXISTS semijoin over the qualifying member-ID set

EXISTS rechecks the eligible member set. It is not assumed faster than the direct WHERE filter.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 3월에 태어난 여성 회원 목록 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131120) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

# 조건에 맞는 도서와 저자 리스트 출력하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/144854) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

경제 분야 도서에 저자 이름과 지정 형식의 출판일을 붙입니다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합입니다. 경제 분야 도서에 저자 이름과 지정 형식의 출판일을 붙입니다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용합니다.

- `BOOK`: `BOOK_ID`, `CATEGORY`, `AUTHOR_ID`, `PRICE`, `PUBLISHED_DATE`
- `AUTHOR`: `AUTHOR_ID`, `AUTHOR_NAME`

## 풀이를 따라가기

도서의 AUTHOR_ID로 저자 테이블을 조인합니다. CATEGORY가 경제인 행만 남기고 출판일 오름차순으로 출력합니다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 도서의 AUTHOR_ID로 저자 테이블을 조인한다. CATEGORY가 경제인 행만 남기고 출판일 오름차순으로 출력한다.
SELECT b.BOOK_ID, a.AUTHOR_NAME, DATE_FORMAT(b.PUBLISHED_DATE, '%Y-%m-%d') AS PUBLISHED_DATE
FROM BOOK AS b
JOIN AUTHOR AS a ON a.AUTHOR_ID = b.AUTHOR_ID
WHERE b.CATEGORY = '경제'
ORDER BY b.PUBLISHED_DATE
```

## 정답이 되는 이유

경제 분류의 도서만 고른 뒤 AUTHOR_ID로 저자 이름을 붙입니다. 저자 키가 고유하므로 같은 책의 행이 조인으로 늘어나지 않습니다.

도서 N개를 필터하고 저자 M개와 연결한 뒤 R권을 출판일순으로 정렬합니다. 저자 키 인덱스와 조인 계획에 따라 비용이 달라지며 결과 비교 정렬은 O(R log R)입니다.

주의할 점: 출력 날짜는 YYYY-MM-DD입니다. 도서 ID와 저자 ID를 서로 연결하면 안 됩니다.

## 다른 방법: 상관 서브쿼리로 저자 이름 조회

```sql
SELECT b.BOOK_ID,
       (SELECT a.AUTHOR_NAME FROM AUTHOR a WHERE a.AUTHOR_ID=b.AUTHOR_ID) AS AUTHOR_NAME,
       DATE_FORMAT(b.PUBLISHED_DATE,'%Y-%m-%d') AS PUBLISHED_DATE
FROM BOOK b WHERE b.CATEGORY='경제'
  AND EXISTS (SELECT 1 FROM AUTHOR a WHERE a.AUTHOR_ID=b.AUTHOR_ID)
ORDER BY b.PUBLISHED_DATE;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 도서의 AUTHOR_ID로 저자 테이블을 조인합니다. CATEGORY가 경제인 행만 남기고 출판일 오름차순으로 출력합니다. | 상관 서브쿼리로 저자 이름 조회 |
| 비용 | 도서 N개를 필터하고 저자 M개와 연결한 뒤 R권을 출판일순으로 정렬합니다. 저자 키 인덱스와 조인 계획에 따라 비용이 달라지며 결과 비교 정렬은 O(R log R)입니다. | 책마다 상관 하위쿼리로 저자 이름과 존재 여부를 확인합니다. 저자 키 인덱스와 하위쿼리 변환 여부에 따라 비용이 달라집니다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했습니다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했습니다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않습니다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

List economics books with author names and formatted publication dates.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. List economics books with author names and formatted publication dates.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `BOOK`: `BOOK_ID`, `CATEGORY`, `AUTHOR_ID`, `PRICE`, `PUBLISHED_DATE`
- `AUTHOR`: `AUTHOR_ID`, `AUTHOR_NAME`

### Approach

Join authors by AUTHOR_ID, keep CATEGORY 경제, and order by publication date.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Select economics books and attach author names through AUTHOR_ID. A unique author key prevents the join from multiplying a book row.

Filter N books, look up authors among M rows, then order R books by publication date. Author-key indexes and join plans affect lookup cost; result sorting is O(R log R).

Boundary cases: Format dates as YYYY-MM-DD. Do not join book IDs directly to author IDs.

### Alternative: Correlated scalar lookup of author names

Use correlated author lookups per book; key indexes and subquery transformations determine cost.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 조건에 맞는 도서와 저자 리스트 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/144854) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

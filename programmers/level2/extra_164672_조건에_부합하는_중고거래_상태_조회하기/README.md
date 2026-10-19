# 조건에 부합하는 중고거래 상태 조회하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/164672) · Level 2 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

2022년 10월 5일 작성된 중고거래 글의 상태를 한국어로 표시한다.

## 조건과 입출력

입력은 아래 테이블이고 출력은 쿼리 결과 집합이다. 2022년 10월 5일 작성된 중고거래 글의 상태를 한국어로 표시한다.

수치 배열 제한 대신 테이블 스키마와 조회 조건을 사용한다.

- `USED_GOODS_BOARD`: `BOARD_ID`, `WRITER_ID`, `TITLE`, `CONTENTS`, `PRICE`, `CREATED_DATE`, `STATUS`, `VIEWS`

## 풀이를 따라가기

해당 날짜의 반열린 시각 구간을 필터한다. CASE로 SALE·RESERVED·DONE을 표시용 이름으로 바꾸고 게시글 ID를 내림차순 정렬한다.

[기본 풀이 / Main](solution.sql) · [다른 풀이 / Alternative](alternative.sql) · [제출 원본 / Archived submission](submitted_original.sql)

```sql
-- 해당 날짜의 반열린 시각 구간을 필터한다. CASE로 SALE·RESERVED·DONE을 표시용 이름으로 바꾸고 게시글 ID를 내림차순 정렬한다.
SELECT BOARD_ID, WRITER_ID, TITLE, PRICE,
       CASE STATUS
           WHEN 'SALE' THEN '판매중'
           WHEN 'RESERVED' THEN '예약중'
           WHEN 'DONE' THEN '거래완료'
       END AS STATUS
FROM USED_GOODS_BOARD
WHERE CREATED_DATE >= '2022-10-05' AND CREATED_DATE < '2022-10-06'
ORDER BY BOARD_ID DESC
```

## 왜 맞는가

생성 시각이 10월 5일 하루에 속하는 행만 고르고 CASE로 상태 코드를 표시 문자열에 대응시킨다. 다음 날 0시는 제외해 날짜 경계를 지킨다.

N개 게시글을 검사하고 R개 결과를 ID 역순으로 정렬한다. 결과 비교 정렬은 O(R log R); 날짜 인덱스와 ID 순서 접근이 계획에 영향을 준다.

주의할 점: 날짜·시간 열에서도 해당 날짜 전체를 포함한다. 원래 상태 코드와 표시 이름을 혼동하지 않는다.

## 다른 방법: 상태 코드 매핑 CTE 조인

```sql
WITH labels AS (
    SELECT 'SALE' AS CODE,'판매중' AS LABEL
    UNION ALL SELECT 'RESERVED','예약중'
    UNION ALL SELECT 'DONE','거래완료'
)
SELECT b.BOARD_ID,b.WRITER_ID,b.TITLE,b.PRICE,l.LABEL AS STATUS
FROM USED_GOODS_BOARD b JOIN labels l ON l.CODE=b.STATUS
WHERE b.CREATED_DATE>='2022-10-05' AND b.CREATED_DATE<'2022-10-06'
ORDER BY b.BOARD_ID DESC;
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 해당 날짜의 반열린 시각 구간을 필터한다. CASE로 SALE·RESERVED·DONE을 표시용 이름으로 바꾸고 게시글 ID를 내림차순 정렬한다. | 상태 코드 매핑 CTE 조인 |
| 비용 | N개 게시글을 검사하고 R개 결과를 ID 역순으로 정렬한다. 결과 비교 정렬은 O(R log R); 날짜 인덱스와 ID 순서 접근이 계획에 영향을 준다. | 상태 코드 세 개의 대응표를 만들고 조인한다. CASE 분기 대신 작은 대응표 조회를 사용한다. |

## 검증

공식 예제 테이블을 로컬 SQLite에서 실행하고 두 쿼리의 결과를 비교했다. YEAR·MONTH·DATE_FORMAT 등은 호환 함수를 사용했다. 이는 MySQL 서버의 실행·성능 검증이나 새 사이트 제출을 뜻하지 않는다.

문제 폴더에서 `python test_query.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Show used-goods posts created on 5 October 2022 with Korean status labels.

### Conditions and input/output

The input consists of the tables below; the output is a query result set. Show used-goods posts created on 5 October 2022 with Korean status labels.

This SQL task is defined by table schemas and query predicates rather than array-size limits.

- `USED_GOODS_BOARD`: `BOARD_ID`, `WRITER_ID`, `TITLE`, `CONTENTS`, `PRICE`, `CREATED_DATE`, `STATUS`, `VIEWS`

### Approach

Filter the half-open interval for the date. Map SALE, RESERVED and DONE to display labels with CASE, then order by descending board ID.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Retain rows created on October 5 and map status codes to display labels with CASE. Excluding midnight of the following day preserves the date boundary.

Inspect N posts and order R results by descending ID. Comparison sorting is O(R log R); date indexes and ordered ID access affect the plan.

Boundary cases: Include the entire date even for timestamp columns. Distinguish stored status codes from display labels.

### Alternative: Join a status-label mapping CTE

Join a three-row status-label table instead of evaluating CASE branches.

### Verification

Official example tables were checked locally with SQLite and the two query results were compared. Compatibility functions supplied YEAR, MONTH, DATE_FORMAT and similar MySQL functions. This does not constitute MySQL-server execution/performance testing or a new site submission.

Run `python test_query.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 조건에 부합하는 중고거래 상태 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/164672) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

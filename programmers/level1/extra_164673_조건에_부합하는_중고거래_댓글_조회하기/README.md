# 조건에 부합하는 중고거래 댓글 조회하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/164673) · Level 1 · MySQL

## 풀이

10월에 작성된 게시글을 고르고 그 게시글의 댓글을 연결합니다. 날짜 조건은 게시글에, 출력·정렬 날짜는 댓글에 적용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT B.TITLE, B.BOARD_ID, R.REPLY_ID, R.WRITER_ID, R.CONTENTS,
       DATE_FORMAT(R.CREATED_DATE, '%Y-%m-%d') AS CREATED_DATE
FROM USED_GOODS_BOARD AS B
JOIN USED_GOODS_REPLY AS R ON B.BOARD_ID = R.BOARD_ID
WHERE B.CREATED_DATE >= '2022-10-01' AND B.CREATED_DATE < '2022-11-01'
ORDER BY R.CREATED_DATE, B.TITLE

-- 전체 코드 줄별 설명
-- SELECT B.TITLE, B.BOARD_ID, R.REPLY_ID, R.WRITER_ID, R.CONTENTS,  -- SELECT는 출력 열 선택. 점은 테이블 별칭의 열 접근. 게시글·댓글 정보를 지정 순서로 조회.
--        DATE_FORMAT(R.CREATED_DATE, '%Y-%m-%d') AS CREATED_DATE  -- DATE_FORMAT은 날짜 형식 지정. %Y·%m·%d는 연·월·일, AS는 결과 열 별칭.
-- FROM USED_GOODS_BOARD AS B  -- FROM은 원본 게시글 테이블, AS B는 짧은 별칭 지정.
-- JOIN USED_GOODS_REPLY AS R ON B.BOARD_ID = R.BOARD_ID  -- JOIN·ON은 같은 게시글 ID를 가진 댓글 연결.
-- WHERE B.CREATED_DATE >= '2022-10-01' AND B.CREATED_DATE < '2022-11-01'  -- WHERE는 조건 필터, AND는 모두 만족. 댓글이 아닌 게시글의 작성일이 2022년 10월인지 검사.
-- ORDER BY R.CREATED_DATE, B.TITLE  -- ORDER BY는 정렬. 댓글 작성일 오름차순, 같으면 게시글 제목 오름차순.

-- 풀이 요약
-- 10월에 작성된 게시글을 고르고 그 게시글의 댓글을 연결합니다. 날짜 조건은 게시글에, 출력·정렬 날짜는 댓글에 적용합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.

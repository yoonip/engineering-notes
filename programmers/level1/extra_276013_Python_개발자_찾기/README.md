# Python 개발자 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/276013) · Level 1 · MySQL

## 풀이

세 스킬 열 중 하나라도 Python인 개발자를 조회하고 ID 순으로 정렬합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT ID, EMAIL, FIRST_NAME, LAST_NAME
FROM DEVELOPER_INFOS
WHERE 'Python' IN (SKILL_1, SKILL_2, SKILL_3)
ORDER BY ID

-- 전체 코드 줄별 설명
-- SELECT ID, EMAIL, FIRST_NAME, LAST_NAME  -- SELECT는 출력 열 선택. 쉼표로 ID·이메일·이름·성 구분.
-- FROM DEVELOPER_INFOS  -- FROM은 개발자 정보 테이블 지정.
-- WHERE 'Python' IN (SKILL_1, SKILL_2, SKILL_3)  -- WHERE는 필터, IN은 괄호 안 값 중 하나와 같은지 검사. 세 스킬 중 Python 보유자 선택.
-- ORDER BY ID  -- ORDER BY는 정렬. 기본 ASC로 ID 오름차순 정렬.

-- 풀이 요약
-- 세 스킬 열 중 하나라도 Python인 개발자를 조회하고 ID 순으로 정렬합니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.

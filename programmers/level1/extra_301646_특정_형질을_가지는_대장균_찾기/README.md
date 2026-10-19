# 특정 형질을 가지는 대장균 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/301646) · Level 1 · MySQL

## 풀이

형질 번호 j는 2의 (j-1)제곱 비트입니다. 2번은 없고 1번 또는 3번이 있는 개체만 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.sql) · [채점 기록 / Grade](grading.json)

```sql
SELECT COUNT(*) AS COUNT
FROM ECOLI_DATA
WHERE (GENOTYPE & 2) = 0
  AND (GENOTYPE & 5) <> 0

-- 전체 코드 줄별 설명
-- SELECT COUNT(*) AS COUNT  -- SELECT는 조회, COUNT(*)는 행 개수, AS는 출력 열의 별칭.
-- FROM ECOLI_DATA  -- FROM은 대장균 정보 테이블 지정.
-- WHERE (GENOTYPE & 2) = 0  -- WHERE는 조건 필터, &는 비트 AND. 2번 형질의 비트 2가 없는 개체 선택.
--   AND (GENOTYPE & 5) <> 0  -- AND는 두 조건 모두 만족, <>는 다름. 1번·3번 형질 비트 1과 4의 합 5 중 하나 이상 존재.

-- 풀이 요약
-- 형질 번호 j는 2의 (j-1)제곱 비트입니다. 2번은 없고 1번 또는 3번이 있는 개체만 셉니다.
--
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.

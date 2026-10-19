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
SELECT child.ID, child.GENOTYPE, parent.GENOTYPE AS PARENT_GENOTYPE
FROM ECOLI_DATA AS child
JOIN ECOLI_DATA AS parent ON parent.ID = child.PARENT_ID
WHERE (child.GENOTYPE & parent.GENOTYPE) = parent.GENOTYPE
ORDER BY child.ID

-- 전체 코드 줄별 설명
-- SELECT child.ID, child.GENOTYPE, parent.GENOTYPE AS PARENT_GENOTYPE  -- SELECT는 출력 열 선택. AS는 부모 형질 열의 별칭. 점(.)은 부모·자식 역할별 열 구분.
-- FROM ECOLI_DATA AS child  -- 같은 테이블을 자식 역할로 조회.
-- JOIN ECOLI_DATA AS parent ON parent.ID = child.PARENT_ID  -- JOIN·ON으로 자식의 부모 번호와 부모 개체 ID를 연결하는 자기 조인.
-- WHERE (child.GENOTYPE & parent.GENOTYPE) = parent.GENOTYPE  -- &는 비트 AND. 부모의 켜진 비트가 자식에게 전부 있으면 AND 결과가 부모 형질과 같음. 괄호는 계산 우선순위 지정.
-- ORDER BY child.ID  -- 자식 ID 오름차순 정렬.

-- 풀이 요약
-- 형질 정수는 각 비트가 형질 존재 여부를 뜻한다. 자식&부모가 부모와 같으면 부모의 모든 형질을 포함한 것이다.
-- 부모가 없는 최초 개체는 내부 JOIN에서 제외된다. 단순 크기 비교가 아니라 비트 포함 여부를 검사한다.
-- 
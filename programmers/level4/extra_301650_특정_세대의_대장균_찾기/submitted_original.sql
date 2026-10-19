SELECT child.ID
FROM ECOLI_DATA AS child
JOIN ECOLI_DATA AS parent ON child.PARENT_ID = parent.ID
JOIN ECOLI_DATA AS grandparent ON parent.PARENT_ID = grandparent.ID
WHERE grandparent.PARENT_ID IS NULL
ORDER BY child.ID

-- 전체 코드 줄별 설명
-- SELECT child.ID  -- SELECT는 결과로 출력할 열 선택. child.ID는 자식 개체의 식별자.
-- FROM ECOLI_DATA AS child  -- FROM은 조회 테이블 지정, AS는 별명 지정. 자식 역할로 child 사용.
-- JOIN ECOLI_DATA AS parent ON child.PARENT_ID = parent.ID  -- JOIN은 행 연결, ON은 연결 조건. 자식의 부모 행을 연결.
-- JOIN ECOLI_DATA AS grandparent ON parent.PARENT_ID = grandparent.ID  -- 동일 테이블을 다시 연결하여 조부모를 찾는 셀프 조인.
-- WHERE grandparent.PARENT_ID IS NULL  -- WHERE는 조건 필터. IS NULL은 값이 없음을 검사하여 조부모가 1세대인지 확인.
-- ORDER BY child.ID  -- ORDER BY는 정렬. 기본값 ASC이므로 ID 오름차순.

-- 풀이 요약
-- 자식→부모→조부모를 연결하고 조부모의 부모가 없는 행만 선택하면 정확히 3세대입니다.
-- 예: 1→3→7이면 7을 출력하고, 1→3→7→8의 8은 제외합니다.
-- 
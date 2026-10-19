-- 루트의 자식을 두 단계 연결해 정확히 3세대인 개체 ID를 오름차순으로 구합니다.
-- 자기 조인으로 자식→부모→조부모를 연결하고 조부모의 PARENT_ID가 NULL인 행만 남깁니다. 세 번의 별도 테이블이 아니라 같은 테이블의 세 역할입니다.
SELECT child.ID
FROM ECOLI_DATA AS child
JOIN ECOLI_DATA AS parent ON child.PARENT_ID = parent.ID
JOIN ECOLI_DATA AS grandparent ON parent.PARENT_ID = grandparent.ID
WHERE grandparent.PARENT_ID IS NULL
ORDER BY child.ID

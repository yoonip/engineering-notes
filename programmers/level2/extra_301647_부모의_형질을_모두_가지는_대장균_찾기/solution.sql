-- 같은 테이블을 부모·자식 역할로 조인한다. 자식 AND 부모가 부모와 같으면 부모의 모든 켜진 비트를 보존한 것이다.
SELECT child.ID, child.GENOTYPE, parent.GENOTYPE AS PARENT_GENOTYPE
FROM ECOLI_DATA AS child
JOIN ECOLI_DATA AS parent ON parent.ID = child.PARENT_ID
WHERE (child.GENOTYPE & parent.GENOTYPE) = parent.GENOTYPE
ORDER BY child.ID

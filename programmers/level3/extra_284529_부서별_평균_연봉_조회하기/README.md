# 부서별 평균 연봉 조회하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/284529) · Level 3 · MySQL

[입력 테이블과 자료형 / Input schema](SCHEMA.md)

## 문제와 조건 / Task and conditions

부서 ID로 두 테이블을 연결합니다. 부서 ID·영문 이름·평균 연봉을 출력하고 소수점 첫째 자리 반올림, 평균 연봉 내림차순입니다.

Join by department ID. Output ID, English name and average salary rounded to an integer, ordered by descending average salary.

## 풀이 흐름 / Approach

부서와 사원을 부서 ID로 연결한 뒤 부서별 연봉 평균을 구합니다. 평균을 정수로 반올림하고 평균 연봉이 큰 부서부터 출력합니다.

Join departments and employees by department ID, compute each department’s average salary, round it to an integer and order departments by descending average salary.

## 정답이 되는 이유 / Why it works

부서 ID 조인은 각 사원의 연봉을 소속 부서에 대응시킵니다. 부서 ID·이름별 집계로 부서 평균을 만들고 ROUND(...,0)이 소수점 첫째 자리 반올림을 수행합니다.

The department-ID join associates each salary with its department. Grouping by department ID and name computes the mean, and ROUND(...,0) rounds at the first decimal place.

## 비용 / Complexity

일반 조인·그룹 계획은 인덱스 의존; 중첩 조인 최악 O(de), 그룹 정렬 O(d log d) / Plan-dependent join/grouping; unindexed nested-loop O(de), group sort O(d log d)

## 구현 / Implementation

[solution.sql](solution.sql)

```sql
-- AVG는 평균, ROUND(값,0)는 소수 첫째 자리에서 반올림한 정수, AS는 별칭.
SELECT d.DEPT_ID, d.DEPT_NAME_EN, ROUND(AVG(e.SAL), 0) AS AVG_SAL
FROM HR_DEPARTMENT AS d
-- JOIN·ON으로 부서 ID가 같은 사원을 연결.
JOIN HR_EMPLOYEES AS e ON e.DEPT_ID = d.DEPT_ID
GROUP BY d.DEPT_ID, d.DEPT_NAME_EN
-- 평균 연봉이 높은 부서부터 출력.
ORDER BY AVG_SAL DESC
```

## 다른 방법: 사원 연봉 선집계 / Aggregate employee salaries before joining

사원 테이블을 부서별로 먼저 집계하고 부서명을 붙입니다. 부서 이름 같은 넓은 열을 집계 단계에 전달하지 않아도 되며, 사원이 없는 부서는 주 풀이와 같이 제외됩니다.

Aggregate employees by department before attaching department names. Wider descriptive columns need not participate in aggregation; employee-less departments are excluded just as in the main inner join.

[alternative.sql](alternative.sql)

```sql
SELECT d.DEPT_ID, d.DEPT_NAME_EN, ROUND(s.mean_salary, 0) AS AVG_SAL
FROM HR_DEPARTMENT AS d
JOIN (SELECT DEPT_ID, AVG(SAL) AS mean_salary FROM HR_EMPLOYEES GROUP BY DEPT_ID) AS s
  ON s.DEPT_ID = d.DEPT_ID
ORDER BY AVG_SAL DESC;
```

## 검증 데이터 / Verification data

입력 테이블과 예상 결과는 [cases.json](cases.json)에 있습니다. 첫 검증의 결과 일부는 다음과 같습니다.

Input tables and expected rows are in [cases.json](cases.json). The first case starts with these expected rows.

```json
{
  "expected_rows": [
    [
      "D0007",
      "Marketing",
      54666667
    ],
    [
      "D0006",
      "Purchasing",
      54250000
    ],
    [
      "D0005",
      "Finance",
      52000000
    ]
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 21개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 21 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

로컬 검증은 SQLite에서 공통 SQL과 필요한 함수의 호환 구현을 실행합니다. MySQL 서버의 실행 계획·collation 성능 측정은 포함하지 않습니다.

Local verification executes common SQL in SQLite with compatibility functions where needed. It does not measure a MySQL server’s query plan or collation performance.

원본 채점 기록: 100점. [submitted_original.sql](submitted_original.sql)는 당시 원본 파일을 그대로 보존하며, `solution.sql`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.sql](submitted_original.sql) preserves the original file bytes; `solution.sql` contains the documented implementation.

출처: [프로그래머스 문제 284529](https://school.programmers.co.kr/learn/courses/30/lessons/284529), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 284529](https://school.programmers.co.kr/learn/courses/30/lessons/284529), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

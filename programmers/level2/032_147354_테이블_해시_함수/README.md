# 테이블 해시 함수

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/147354) · Level 2 · Python3

지정 정렬 뒤 각 행의 나머지 합을 계산해 주어진 구간을 XOR한다.

## 조건과 입출력

입력 매개변수: `data, col, row_begin, row_end`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ data의 길이 ≤ 2,500
- 1 ≤ data의 원소의 길이 ≤ 500
- 1 ≤ data[i][j] ≤ 1,000,000
- 1 ≤ col ≤ data의 원소의 길이
- 1 ≤ row_begin ≤ row_end ≤ data의 길이

## 풀이를 따라가기

col열 오름차순·첫 열 내림차순으로 정렬한다. 정렬 후 i행의 모든 값을 i로 나눈 나머지 합 S_i를 구한다. row_begin부터 row_end까지 XOR한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(data, col, row_begin, row_end):
    # 지정 열은 오름차순, 같으면 첫 열은 내림차순이다.
    data.sort(key=lambda row: (row[col - 1], -row[0]))
    answer = 0
    for index in range(row_begin, row_end + 1):
        # 정렬 후 1부터 시작하는 행 번호로 나머지를 구한다.
        value = sum(number % index for number in data[index - 1])
        answer ^= value
    return answer
```

## 왜 맞는가

복합 정렬 키가 두 우선순위를 그대로 구현한다. 각 행의 나머지 합을 정의대로 계산한 뒤 XOR의 결합법칙으로 누적하면 요구한 해시다.

시간 O(N log N+NM), 공간 O(N) 이하 / Time O(N log N+NM), auxiliary space at most O(N)

주의할 점: 나머지의 분모는 정렬 후 1부터 시작하는 행 번호다. 원본 풀이는 data를 정렬해 입력을 바꾼다.

## 다른 방법: 안정 정렬 두 번 + XOR 누적합

```python
def solution(data,col,row_begin,row_end):
    rows=sorted(data,key=lambda row:row[0],reverse=True)
    rows.sort(key=lambda row:row[col-1])
    prefix=[0]
    for index,row in enumerate(rows,1):
        prefix.append(prefix[-1]^sum(value%index for value in row))
    return prefix[row_end]^prefix[row_begin-1]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | col열 오름차순·첫 열 내림차순으로 정렬한다. 정렬 후 i행의 모든 값을 i로 나눈 나머지 합 S_i를 구한다. row_begin부터 row_end까지 XOR한다. | 안정 정렬 두 번 + XOR 누적합 |
| 비용 | 시간 O(N log N+NM), 공간 O(N) 이하 / Time O(N log N+NM), auxiliary space at most O(N) | 시간 O(N log N+NM), 공간 O(NM) / Time O(N log N+NM), space O(NM) with copied rows |

## 검증

공식 예제 1개와 생성 입력 50개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Sort the table as specified, sum each selected row’s remainders and XOR those sums.

### Conditions and input/output

Input arguments: `data, col, row_begin, row_end`. The return value is an integer satisfying the task described below.

- 1 ≤ rows ≤ 2500; 1 ≤ columns ≤ 500; 1 ≤ data[i][j] ≤ 1000000
- 1 ≤ col ≤ columns; 1 ≤ row_begin ≤ row_end ≤ rows

### Approach

Sort by column col ascending and the first column descending. Compute S_i as the sum of row i’s values modulo i, then XOR the requested row interval.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The compound key enforces both sort priorities. Each row sum follows its definition, and associative XOR accumulation yields the required hash.

시간 O(N log N+NM), 공간 O(N) 이하 / Time O(N log N+NM), auxiliary space at most O(N)

Boundary cases: The modulus uses the sorted one-based row number. The main implementation sorts data in place.

### Alternative: Two stable sorts with prefix XOR

시간 O(N log N+NM), 공간 O(NM) / Time O(N log N+NM), space O(NM) with copied rows

### Verification

Local checks covered 1 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 테이블 해시 함수](https://school.programmers.co.kr/learn/courses/30/lessons/147354) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

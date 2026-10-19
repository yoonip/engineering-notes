# 유사 칸토어 비트열

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/148652) · Level 2 · Python3

재귀적으로 늘어나는 유사 칸토어 비트열의 구간에서 1의 개수를 센다.

## 조건과 입출력

입력 매개변수: `n, l, r`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ n ≤ 20
- 1 ≤ l, r ≤ 5^n
- l ≤ r < l + 10,000,000

## 풀이를 따라가기

길이 5의 묶음에서 가운데는 모두 0이고 나머지 넷은 이전 단계와 같다. prefix(level,length)로 앞 length개의 1 개수를 구한다. 완전한 묶음은 4의 거듭제곱으로 더하고 남은 한 묶음만 재귀한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(n, l, r):
    def prefix(level, length):
        if level == 0:
            return length
        block = 5 ** (level - 1)
        groups, rest = divmod(length, block)
        # 가운데 세 번째 묶음은 모두 0이라 완전 묶음 수에서 뺀다.
        full = groups - int(groups > 2)
        total = full * 4 ** (level - 1)
        # 남은 위치가 가운데 묶음이면 1이 추가되지 않는다.
        if groups == 2:
            return total
        return total + prefix(level - 1, rest)
    return prefix(n, r) - prefix(n, l - 1)
```

## 왜 맞는가

다섯 부분은 서로 겹치지 않으며 가운데만 기여가 0이다. 완전한 부분의 개수와 나머지 재귀를 더하면 정확한 누적 개수이고 두 누적값의 차이가 구간 답이다.

시간 O(n), 공간 O(n) / Time and space O(n)

주의할 점: 입력 구간은 1부터 세는 폐구간이다. prefix의 length는 개수여서 [l,r]은 prefix(r)−prefix(l−1)이다.

## 다른 방법: 5진수 자릿수로 각 비트 판정

```python
def solution(n,l,r):
    answer=0
    for position in range(l-1,r):
        value=position
        for _ in range(n):
            value,digit=divmod(value,5)
            if digit==2: break
        else:
            answer+=1
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 길이 5의 묶음에서 가운데는 모두 0이고 나머지 넷은 이전 단계와 같다. prefix(level,length)로 앞 length개의 1 개수를 구한다. 완전한 묶음은 4의 거듭제곱으로 더하고 남은 한 묶음만 재귀한다. | 5진수 자릿수로 각 비트 판정 |
| 비용 | 시간 O(n), 공간 O(n) / Time and space O(n) | 시간 O((r−l+1)n), 공간 O(1) / Time O((r−l+1)n), space O(1) |

## 검증

공식 예제 1개와 생성 입력 60개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count ones in a range of the recursively expanded Cantor-like bit sequence.

### Conditions and input/output

Input arguments: `n, l, r`. The return value is an integer satisfying the task described below.

- 1 ≤ n ≤ 20; 1 ≤ l ≤ r ≤ 5^n; r < l+10000000
- one-based inclusive interval [l,r]

### Approach

Among five blocks, the middle is all zero and the other four repeat the preceding level. A prefix function adds complete blocks using powers of four and recurses into one remaining block.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The five blocks are disjoint, with zero contribution from the middle. Adding complete blocks and the remaining prefix yields an exact count; subtract two prefixes for the interval.

시간 O(n), 공간 O(n) / Time and space O(n)

Boundary cases: The input is a one-based inclusive range. Prefix arguments are lengths, so use prefix(r)−prefix(l−1).

### Alternative: Test each position through base-five digits

시간 O((r−l+1)n), 공간 O(1) / Time O((r−l+1)n), space O(1)

### Verification

Local checks covered 1 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 유사 칸토어 비트열](https://school.programmers.co.kr/learn/courses/30/lessons/148652) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

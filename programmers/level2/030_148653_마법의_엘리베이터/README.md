# 마법의 엘리베이터

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/148653) · Level 2 · Python3

10의 거듭제곱만큼 위아래로 이동해 0층으로 가는 최소 버튼 수를 구한다.

## 조건과 입출력

입력 매개변수: `storey`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ storey ≤ 100,000,000

## 풀이를 따라가기

일의 자리를 없앨 때 0으로 내릴지 10으로 올릴지 정한다. 5보다 크면 올리고 작으면 내린다. 정확히 5이면 다음 자리가 5 이상인지 보고 올림을 결정한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(storey):
    answer = 0
    while storey:
        storey, digit = divmod(storey, 10)
        # 5에서 동률이면 다음 자리의 올림 이득까지 확인한다.
        if digit > 5 or (digit == 5 and storey % 10 >= 5):
            answer += 10 - digit
            storey += 1
        else:
            answer += digit
    return answer
```

## 왜 맞는가

현재 자리는 결국 10의 배수로 맞춰야 한다. 내림은 digit번, 올림은 10−digit번이며 차이가 나면 싼 쪽이 우세하다. 5 동률에서는 다음 자리에 전달되는 올림이 유리한지 비교하면 된다.

시간 O(log storey), 공간 O(1) / Time O(log storey), space O(1)

주의할 점: 일의 자리가 5인 경우를 무조건 내리면 55 같은 수에서 손해다. 올림으로 자리 수가 늘어날 수 있다.

## 다른 방법: 올림·내림을 모두 비교하는 메모이제이션

```python
from functools import lru_cache

def solution(storey):
    @lru_cache(None)
    def best(value):
        if value<10: return min(value,11-value)
        high,digit=divmod(value,10)
        return min(digit+best(high),10-digit+best(high+1))
    return best(storey)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 일의 자리를 없앨 때 0으로 내릴지 10으로 올릴지 정한다. 5보다 크면 올리고 작으면 내린다. 정확히 5이면 다음 자리가 5 이상인지 보고 올림을 결정한다. | 올림·내림을 모두 비교하는 메모이제이션 |
| 비용 | 시간 O(log storey), 공간 O(1) / Time O(log storey), space O(1) | 시간·공간 O(log storey) 상태 / O(log storey) time and space states |

## 검증

공식 예제 2개와 생성 입력 202개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Minimize button presses to reach floor zero using positive or negative powers of ten.

### Conditions and input/output

Input arguments: `storey`. The return value is an integer satisfying the task described below.

- 1 ≤ storey ≤ 100000000

### Approach

Remove the last digit by rounding down to zero or up to ten. Round up above five and down below five; at five, inspect whether the next digit is at least five.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The current digit must eventually become a multiple of ten. The two costs are digit and 10−digit; choose the cheaper, using the next digit to resolve the equal-cost carry case.

시간 O(log storey), 공간 O(1) / Time O(log storey), space O(1)

Boundary cases: Always rounding five down fails for values such as 55. Carrying may create another digit.

### Alternative: Memoized recursion comparing both rounding directions

시간·공간 O(log storey) 상태 / O(log storey) time and space states

### Verification

Local checks covered 2 official examples and 202 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 마법의 엘리베이터](https://school.programmers.co.kr/learn/courses/30/lessons/148653) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

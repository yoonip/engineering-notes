# 이진 변환 반복하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/70129) · Level 2 · Python3

0 제거와 남은 길이의 이진수 변환을 반복해 변환 횟수와 제거한 0 수를 구한다.

## 조건과 입출력

입력 매개변수: `s`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- s의 길이는 1 이상 150,000 이하입니다.
- s에는 '1'이 최소 하나 이상 포함되어 있습니다.

## 풀이를 따라가기

현재 문자열의 1 개수를 센다. 길이−1 개수를 제거한 0 수에 더한다. 1의 개수를 이진수 문자열로 바꾸고 1이 될 때까지 반복한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(s):
    conversions = removed = 0
    while s != '1':
        # 0을 지우고 남는 것은 1의 개수뿐이다.
        ones = s.count('1')
        # 이번 변환에서 제거한 0 수를 누적한다.
        removed += len(s) - ones
        s = bin(ones)[2:]
        conversions += 1
    return [conversions, removed]
```

## 왜 맞는가

0을 지운 뒤 남는 문자열은 모두 1이므로 필요한 정보는 그 길이뿐이다. 이 길이를 정확히 이진 변환하면 정의된 다음 상태와 같다.

시간 O(N), 공간 O(N) / Time and space O(N); 이후 길이가 로그 규모로 감소 / subsequent lengths shrink logarithmically

주의할 점: 처음부터 1이면 [0,0]이다. 입력에 1이 적어도 하나 있어 길이 0 변환을 고려할 필요가 없다.

## 다른 방법: 정수의 bit_count로 1 수 추적

```python
def solution(s):
    value=int(s,2)
    length=len(s)
    turns=zeros=0
    while length!=1 or value!=1:
        ones=value.bit_count()
        zeros+=length-ones
        value=ones
        length=value.bit_length()
        turns+=1
    return [turns,zeros]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 현재 문자열의 1 개수를 센다. 길이−1 개수를 제거한 0 수에 더한다. 1의 개수를 이진수 문자열로 바꾸고 1이 될 때까지 반복한다. | 정수의 bit_count로 1 수 추적 |
| 비용 | 시간 O(N), 공간 O(N) / Time and space O(N); 이후 길이가 로그 규모로 감소 / subsequent lengths shrink logarithmically | 시간 O(N), 공간 O(N)비트 / Time O(N), space O(N) bits |

## 검증

공식 예제 3개와 생성 입력 71개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Repeat zero removal and binary length conversion, returning the number of conversions and removed zeros.

### Conditions and input/output

Input arguments: `s`. The return value is a numeric list satisfying the task described below.

- 1 ≤ len(s) ≤ 150000; binary string with at least one '1'

### Approach

Count ones, add length minus that count to removed zeros, and replace the string with the binary representation of the count until it becomes one.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

After deleting zeros, only the number of ones matters. Converting that count to binary gives exactly the next state.

시간 O(N), 공간 O(N) / Time and space O(N); 이후 길이가 로그 규모로 감소 / subsequent lengths shrink logarithmically

Boundary cases: An initial one returns [0,0]. The input contains a one, so a zero-length conversion cannot occur.

### Alternative: Track one counts using integer bit_count

시간 O(N), 공간 O(N)비트 / Time O(N), space O(N) bits

### Verification

Local checks covered 3 official examples and 71 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 이진 변환 반복하기](https://school.programmers.co.kr/learn/courses/30/lessons/70129) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

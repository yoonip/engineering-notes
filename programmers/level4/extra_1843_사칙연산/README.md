# 사칙연산

Level 4 · `1843` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1843)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

숫자와 +·− 순서를 유지하면서 괄호를 배치해 최종값을 최대화한다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`3≤len(arr)≤201, odd; 2..101 numbers in1..1000; alternating numbers and +/−; preserve token order.`

## 풀이를 따라가기

연속 구간마다 최댓값과 최솟값을 함께 저장한다. 마지막 계산 위치를 모두 고른다. 덧셈은 최대+최대·최소+최소, 뺄셈은 최대−최소·최소−최대가 경계다.

어떤 괄호 배치도 마지막 연산에서 왼쪽·오른쪽 연속 구간으로 갈라진다. 그 분할을 모두 조사하고 두 경계를 유지하면 모든 최적·최악 조합을 포함한다.

## 다른 방법과 비교

대안은 구간에서 실제로 가능한 결과 값 전체를 집합으로 저장한다. 경계 두 개만 보관하는 압축이 맞는지 확인할 수 있지만 숫자 12개 이하 비교용으로 제한한다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(N³), N=숫자 수/numbers` | `O(N²)` |
| 대안 풀이 | `가능한 구간 값 집합에 비례 / proportional to attainable interval-value sets` | 코드의 상태·탐색 구조 참조 |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Maximize an expression containing ordered numbers and plus/minus operators by choosing parentheses.

Input limits and constants, using the parameter names in the code:

`3≤len(arr)≤201, odd; 2..101 numbers in1..1000; alternating numbers and +/−; preserve token order.`

### Following the solution

Store both minimum and maximum for every contiguous interval. Enumerate its final split: addition combines matching extrema, while subtraction combines opposite extrema.

Every parenthesization splits into two contiguous subexpressions at its final operator. Considering every split and both extrema therefore covers all optimal and worst combinations.

### Alternative and comparison

The alternative stores every attainable interval value in a set, independently checking the extrema compression. It is limited to twelve numbers.

The primary solution takes `O(N³), N=숫자 수/numbers` time and `O(N²)` additional space. The alternative takes `가능한 구간 값 집합에 비례 / proportional to attainable interval-value sets` time. Its code shows the states and storage it uses.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 사칙연산](https://school.programmers.co.kr/learn/courses/30/lessons/1843): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.

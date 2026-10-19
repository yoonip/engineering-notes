# 4단 고음

Level 4 · `1831` · C++ · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1831)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py) · [C++ 제출 코드](solution.cpp)

## 문제와 조건

3을 곱한 뒤 1을 두 번 더하는 고음 과정을 중첩하거나 이어 붙여 최종 음높이 n을 만드는 서로 다른 올바른 문자열 수를 센다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`5≤n≤2^31−1; start pitch=1; *=multiply by3, +=add1; each * must have two matching later + operations.`

## 풀이를 따라가기

뒤에서 보면 +는 값에서 1을 빼고 아직 대응할 + 개수를 늘린다. 값이 3의 배수이고 대기 +가 두 개 이상일 때만 역방향 *로 3을 나눈다. 같은 값·대기 수는 메모한다.

올바른 문자열의 모든 접두사는 사용한 +가 *의 두 배를 넘지 않는다. 남은 +를 대응시키는 데 필요한 최소 곱셈 수와 3의 거듭제곱 하한으로 불가능한 상태를 자른다. C++ map 비용을 포함해 방문 상태 수로 복잡도를 표현한다.

## 다른 방법과 비교

대안은 1에서 시작해 *·+를 정방향으로 붙인다. 남은 + 의무를 상태로 기억하며 목표 음높이 10000 이하에서 역방향 가지치기를 검산한다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(S log S) C++ map; O(S) Python cache 평균/expected` | `O(S), S=방문 상태/visited states` |
| 대안 풀이 | `정방향 상태 수에 비례 / proportional to forward states` | 코드의 상태·탐색 구조 참조 |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.cpp](submitted_original.cpp)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Count valid nested or concatenated high-note strings reaching n from pitch one, where each multiplication by three is paired with two later increments.

Input limits and constants, using the parameter names in the code:

`5≤n≤2^31−1; start pitch=1; *=multiply by3, +=add1; each * must have two matching later + operations.`

### Following the solution

Reverse an increment by subtracting one and increasing pending increments. Reverse a multiplication only at a multiple of three with at least two pending increments. Memoize pitch/pending pairs.

Every valid prefix has at most twice as many increments as multiplications. The minimum multiplication count needed to match pending increments gives a power-of-three lower-bound prune. Complexity is stated in visited states, including C++ map lookup costs.

### Alternative and comparison

The alternative grows strings forward while tracking outstanding increment obligations, checking the reverse search independently for target pitch at most 10000.

The primary solution takes `O(S log S) C++ map; O(S) Python cache 평균/expected` time and `O(S), S=방문 상태/visited states` additional space. The alternative takes `정방향 상태 수에 비례 / proportional to forward states` time. Its code shows the states and storage it uses.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.cpp](submitted_original.cpp).

## 출처 / Source

- [Programmers — 4단 고음](https://school.programmers.co.kr/learn/courses/30/lessons/1831): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)

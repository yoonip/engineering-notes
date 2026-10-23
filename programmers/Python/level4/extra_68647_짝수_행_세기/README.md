# 짝수 행 세기

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 4 · `68647` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68647)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

각 열의 1 개수는 유지하면서 모든 행의 합이 짝수인 이진 행렬의 개수를 셉니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤rows,cols≤300; binary matrix; preserve each column sum, require every row sum even; modulus 10000019.`

## 풀이를 따라가기

처리한 열까지 짝수인 행 개수만 상태로 둡니다. 짝수 행 e개 중 x개와 홀수 행 R−e개 중 c−x개에 1을 넣으면 새 짝수 행 수는 e+c−2x입니다.

같은 홀짝 그룹 안의 행은 앞으로의 경우의 수에 대칭적입니다. 선택 방법 수 C(e,x)C(R−e,c−x)를 곱해 상태를 합치고, 마지막에 짝수 행이 R개인 경우만 택합니다.

## 다른 방법과 비교

대안은 모든 행의 홀짝을 비트마스크로 저장합니다. 1을 놓을 행 조합을 직접 만들고 XOR로 갱신합니다. 행 8개 이하에서는 압축 상태의 조합 계수를 확인하기 좋습니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(cols·rows²)` | `O(rows²)` |
| 대안 풀이 | `O(cols·2^rows·max binomial(rows,column_ones))` | `O(2^rows + max binomial(rows,column_ones))` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Count binary matrices preserving every column sum while making every row sum even.

Input limits and constants, using the parameter names in the code:

`1≤rows,cols≤300; binary matrix; preserve each column sum, require every row sum even; modulus 10000019.`

### Following the solution

Track only the number e of even rows. Selecting x even rows and c−x odd rows for a column containing c ones produces e+c−2x even rows.

Rows within a parity group are symmetric for future counts. Multiply by C(e,x)C(R−e,c−x), aggregate transitions and finish at R even rows.

### Alternative and comparison

The alternative retains the entire row-parity bitmask and enumerates row subsets for each column. At most eight rows independently check the compressed combinatorial transitions.

The primary solution takes `O(cols·rows²)` time and `O(rows²)` additional space. The alternative takes `O(cols·2^rows·max binomial(rows,column_ones))` time. Its additional space is `O(2^rows + max binomial(rows,column_ones))`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 짝수 행 세기](https://school.programmers.co.kr/learn/courses/30/lessons/68647): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.

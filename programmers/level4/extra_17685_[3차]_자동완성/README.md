# [3차] 자동완성

Level 4 · `17685` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17685)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

입력 중인 접두사로 단어가 하나로 정해지는 즉시 자동완성합니다. 모든 단어를 찾는 데 필요한 입력 글자 수의 합을 구합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`2≤word count≤100000; 2≤total characters≤1000000; lowercase words, no duplicate entries.`

## 풀이를 따라가기

정렬하면 어떤 단어와 가장 긴 접두사를 공유하는 단어는 바로 앞이나 뒤에 있습니다. 인접 쌍의 공통 길이보다 한 글자를 더 필요 길이에 반영합니다.

그보다 먼 단어가 더 긴 접두사를 공유한다면 그 사이의 단어도 같은 접두사를 가져야 하므로 인접 비교만으로 충분합니다. 단어 자체가 다른 단어의 접두사이면 자기 전체 길이까지만 입력합니다.

## 다른 방법과 비교

대안은 trie의 각 접두사에 몇 단어가 지나가는지 셉니다. 등장 수가 1인 첫 지점에서 멈춥니다. 문자 수에 비례하지만 노드 메모리가 늘어납니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(L log N), 비교 문자 포함 / including character comparisons` | `O(N)` |
| 대안 풀이 | `O(L) 시간·공간 / time and space` | `O(L)` |

L은 모든 단어의 총 글자 수, N은 단어 수입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Autocomplete once the typed prefix identifies a word uniquely. Sum the required keystrokes for all words.

Input limits and constants, using the parameter names in the code:

`2≤word count≤100000; 2≤total characters≤1000000; lowercase words, no duplicate entries.`

### Following the solution

In sorted order, a word has its longest competing common prefix with an immediate neighbor. Update each pair with one more character than their common-prefix length.

A farther word sharing a longer prefix would force intervening words to share it too. Neighbor checks therefore suffice. Cap required input at the word length when it prefixes another word.

### Alternative and comparison

The trie alternative counts words traversing every prefix and stops at the first count of one. It is linear in total characters but uses explicit prefix nodes.

L is the total character count and N is the number of words.

The primary solution takes `O(L log N), including character comparisons` time and `O(N)` additional space. The alternative takes `O(L) time and space` time. Its additional space is `O(L)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — [3차] 자동완성](https://school.programmers.co.kr/learn/courses/30/lessons/17685): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.

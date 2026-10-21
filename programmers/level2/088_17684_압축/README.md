# [3차] 압축

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17684) · Level 2 · Python3

## 문제와 조건 / Task and conditions

msg는 대문자 1~1000자입니다. A~Z가 1~26번인 초기 사전에서 시작해 최장 일치와 새 문자열 등록을 반복하고 출력 번호 배열을 반환합니다.

msg has 1–1000 uppercase letters. Start with A–Z at indices 1–26, repeatedly use the longest match and register the next extension, returning the emitted indices.

## 풀이 흐름 / Approach

기본 A~Z 사전에서 시작합니다. 현재 문자열에 다음 문자를 붙인 것이 사전에 있으면 계속 늘립니다. 없으면 현재 문자열의 번호를 출력하고 확장 문자열을 새 번호로 등록합니다.

Start with dictionary entries A–Z. Extend the current word while the next character keeps it in the dictionary. On a missing extension, output the current index and register the extension.

## 정답이 되는 이유 / Why it works

처리 중인 word는 항상 사전에 있는 가장 긴 현재 접두부입니다. 확장이 처음 실패한 시점에 출력하므로 LZW 규칙의 최장 일치 문자열을 정확히 선택합니다.

The current word is always a dictionary entry and the longest current prefix. Outputting at the first failed extension implements the LZW longest-match rule.

## 비용 / Complexity

Python 문자열 복사·해시 포함 시간 O(n²), 공간 O(n²) 보수적 상한 / Conservative O(n²) time and space with string copying/hashing

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(msg):
    # A~Z를 색인 1~26으로 초기화.
    dictionary = {chr(65 + index): index + 1 for index in range(26)}
    answer = []
    word = ''
    for character in msg:
        # 한 글자 더 붙인 단어가 사전에 있는지 확인.
        if word + character in dictionary:
            word += character
        else:
            # 마지막 일치 단어의 색인도 출력.
            answer.append(dictionary[word])
            dictionary[word + character] = len(dictionary) + 1
            # =로 다음 입력 단어를 현재 문자부터 새로 시작.
            word = character
    if word:
        answer.append(dictionary[word])
    return answer
```

## 다른 방법: 문자별 트라이 사전 / Character trie dictionary

문자열 전체를 키로 복사하는 대신 노드의 다음 문자 간선을 따라갑니다. 각 입력 문자의 이동과 새 노드 추가로 처리하므로 시간·공간 O(n)입니다.

Follow per-character trie edges rather than copying whole string keys. Input traversal and node insertion take O(n) time and space.

[alternative.py](alternative.py)

```python
def solution(msg):
    edges = [{} for _ in range(27)]
    root = {chr(65 + i): i + 1 for i in range(26)}
    output, start = [], 0
    while start < len(msg):
        node = root[msg[start]]
        end = start + 1
        while end < len(msg) and msg[end] in edges[node]:
            node = edges[node][msg[end]]
            end += 1
        output.append(node)
        if end < len(msg):
            edges[node][msg[end]] = len(edges)
            edges.append({})
        start = end
    return output
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "KAKAO"
  ],
  "output": [
    11,
    1,
    27,
    15
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 31개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 31 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 31개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 31 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 17684](https://school.programmers.co.kr/learn/courses/30/lessons/17684), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17684](https://school.programmers.co.kr/learn/courses/30/lessons/17684), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

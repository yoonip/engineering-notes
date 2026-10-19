# [3차] n진수 게임

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17687) · Level 2 · Python3

## 문제와 조건 / Task and conditions

진법 n=2~16, t=1~1000, 사람 m=2~100, 순서 p=1~m입니다. 0부터 말하며 10~15는 A~F를 쓰고 해당 사람이 말할 t자를 반환합니다.

Base n is 2–16, t is 1–1000, players m is 2–100, and p is 1–m. Start at zero, use A–F for digits 10–15 and return that player’s t spoken digits.

## 풀이 흐름 / Approach

0부터 수를 차례대로 n진법으로 바꿔 한 줄로 이어 붙입니다. p번째 사람은 p−1, p−1+m, …번째 문자를 말하므로 그 위치만 골라 t개를 반환합니다.

Convert consecutive integers starting at zero to base n and concatenate their digits. Player p speaks at indices p−1, p−1+m, and so on; return the first t of these.

## 왜 맞는가 / Why it works

전체 발화 순서는 각 자연수의 n진수 표현을 순서대로 나열한 것과 같습니다. 인덱스를 m으로 나눈 나머지가 p−1인 자리만 선택하면 정확히 그 사람의 차례입니다.

The complete speaking order is the concatenation of consecutive base-n representations. Indices congruent to p−1 modulo m select exactly the requested player’s turns.

## 비용 / Complexity

생성한 문자 수 L에 시간 O(L), 공간 O(L) / O(L) time and space for L generated digits

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n, t, m, p):
    # 진법의 각 자릿수를 대문자까지 표현할 문자열.
    digits = '0123456789ABCDEF'
    stream = []
    number = 0
    while len(stream) < t * m:
        # 나눗셈 중에도 원래 정수를 보존하도록 작업용 변수 복사.
        value = number
        converted = '0' if value == 0 else ''
        while value:
            # 두 값 언패킹.
            value, remainder = divmod(value, n)
            converted = digits[remainder] + converted
        # extend는 문자열의 문자들을 리스트 끝에 각각 추가.
        stream.extend(converted)
        number += 1
    return ''.join(stream[p - 1:t * m:m])
```

## 다른 방법: 발화 스트림에서 필요한 문자만 수집 / Stream only the requested turns

전체 스트림을 저장하지 않고 현재 전체 발화 위치만 셉니다. 변환된 숫자 한 개와 정답 t자만 보관해 공간을 줄입니다.

Track the global digit position without retaining the complete stream. Store only one converted number and the t requested output digits.

[alternative.py](alternative.py)

```python
def solution(n, t, m, p):
    alphabet = '0123456789ABCDEF'
    output, position, number = [], 0, 0
    while len(output) < t:
        value, digits = number, []
        if value == 0:
            digits.append('0')
        while value:
            value, remainder = divmod(value, n)
            digits.append(alphabet[remainder])
        for digit in reversed(digits):
            if position % m == p - 1 and len(output) < t:
                output.append(digit)
            position += 1
        number += 1
    return ''.join(output)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    2,
    4,
    2,
    1
  ],
  "output": "0111"
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

출처: [프로그래머스 문제 17687](https://school.programmers.co.kr/learn/courses/30/lessons/17687), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17687](https://school.programmers.co.kr/learn/courses/30/lessons/17687), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

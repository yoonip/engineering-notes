# 오픈채팅방

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42888) · Level 2 · Python3

## 문제와 조건 / Task and conditions

기록은 1~100000개이고 ID·닉네임은 1~10자이며 대소문자를 구별합니다. Enter·Leave만 출력하고 Change는 이름만 갱신합니다. 모든 메시지는 최종 닉네임을 씁니다.

There are 1–100000 valid records with case-sensitive IDs/names of length 1–10. Emit Enter/Leave messages, use Change only to update names, and display each user’s final nickname.

## 풀이 흐름 / Approach

메시지 문장을 바로 만들지 않고 사용자 ID와 입장·퇴장 종류만 기록합니다. 모든 닉네임 변경을 처리한 뒤 최종 닉네임으로 문장을 만듭니다.

Store user IDs and enter/leave events rather than immediately formatting messages. Apply every nickname update, then render all events with the final nickname.

## 정답이 되는 이유 / Why it works

출력의 닉네임은 해당 사용자의 마지막 닉네임으로 결정됩니다. 이벤트 순서와 최종 닉네임을 분리하면 변경으로 과거 메시지를 직접 수정할 필요 없이 같은 결과를 얻습니다.

Each displayed nickname is the final nickname of that user. Separating event order from the name map reproduces the required history without rewriting earlier strings.

## 비용 / Complexity

입력·출력 문자 합 L에 시간 O(L), 공간 O(L) / O(L) time and space including output

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(record):
    names = {}
    events = []
    # 기록 순회.
    for entry in record:
        parts = entry.split()
        # [인덱스]로 동작·ID를 읽어 각각 대입.
        action, user = parts[0], parts[1]
        if action != 'Leave':
            # [키]의 닉네임을 최신 값으로 덮어씀.
            names[user] = parts[2]
        if action != 'Change':
            # 아직 닉네임은 넣지 않음.
            events.append((user, action))
    messages = {'Enter': '님이 들어왔습니다.', 'Leave': '님이 나갔습니다.'}
    return [names[user] + messages[action] for user, action in events]
```

## 다른 방법: 역순으로 최종 닉네임 확정 / Resolve names in reverse order

기록을 뒤에서 읽으면 처음 만난 닉네임이 그 사용자의 최종 이름입니다. 그다음 정방향으로 입퇴장 기록을 출력합니다.

In a reverse scan, the first encountered nickname is the final one. A second forward pass emits enter/leave events.

[alternative.py](alternative.py)

```python
def solution(record):
    parsed = [entry.split() for entry in record]
    final = {}
    for parts in reversed(parsed):
        if parts[0] != 'Leave':
            final.setdefault(parts[1], parts[2])
    suffix = {'Enter': '님이 들어왔습니다.', 'Leave': '님이 나갔습니다.'}
    return [final[p[1]] + suffix[p[0]] for p in parsed if p[0] in suffix]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      "Enter uid1234 Muzi",
      "Enter uid4567 Prodo",
      "Leave uid1234",
      "Enter uid1234 Prodo",
      "Change uid4567 Ryan"
    ]
  ],
  "output": [
    "Prodo님이 들어왔습니다.",
    "Ryan님이 들어왔습니다.",
    "Prodo님이 나갔습니다.",
    "Prodo님이 들어왔습니다."
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42888](https://school.programmers.co.kr/learn/courses/30/lessons/42888), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42888](https://school.programmers.co.kr/learn/courses/30/lessons/42888), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

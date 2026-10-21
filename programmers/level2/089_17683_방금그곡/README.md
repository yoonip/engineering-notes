# [3차] 방금그곡

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17683) · Level 2 · Python3

## 문제와 조건 / Task and conditions

기억한 멜로디·악보는 각각 1~1439개 음, 곡은 최대 100개입니다. 음은 C,C#,D,D#,E,F,F#,G,G#,A,A#,B이며 분당 한 음입니다. 자정을 넘지 않습니다. 긴 재생·입력 순으로 고르고 없으면 (None)입니다.

The remembered melody and each score contain 1–1439 notes, with at most 100 songs. Allowed notes are C,C#,D,D#,E,F,F#,G,G#,A,A#,B at one note per minute, without crossing midnight. Prefer longer playback, then earlier input; return (None) if absent.

## 풀이 흐름 / Approach

C와 C#을 다른 한 글자로 바꿔 한 음을 한 문자로 맞춥니다. 시작·종료 시각에서 재생 시간을 구하고 악보를 그 길이만큼 반복합니다. 일치 곡 중 재생 시간이 긴 곡을 고르며 동률은 먼저 나온 곡입니다.

Normalize sharp notes to distinct single characters so one note occupies one character. Repeat each score for its playback duration, then choose the longest matching song, preserving the first on ties.

## 정답이 되는 이유 / Why it works

정규화는 음과 문자 사이의 일대일 대응이므로 C와 C#의 부분 일치를 막습니다. 실제 재생 구간에서 연속 부분 문자열을 찾고 엄격히 더 긴 곡만 갱신하면 동률 규칙도 유지됩니다.

Normalization gives a one-to-one note encoding and prevents a C from matching C#. Searching the actual repeated playback and updating only for strictly longer songs preserves the tie rule.

## 비용 / Complexity

단순 부분 문자열 탐색의 보수적 상한 O(Σ(duration·|m|)), 공간 O(최대 duration) / Conservative O(Σ(duration·|m|)) time, O(max duration) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(m, musicinfos):
    def normalize(text):
        # 기본 음 문자 순회.
        for note in 'ABCDEFG':
            text = text.replace(note + '#', note.lower())
        return text
    # 기억한 멜로디를 정규화 함수로 변환.
    target = normalize(m)
    answer, longest = '(None)', -1
    # 방송 정보가 들어온 순서대로 순회.
    for info in musicinfos:
        start, end, title, score = info.split(',')
        # 시작·종료 차이를 분으로 계산.
        duration = (int(end[:2]) - int(start[:2])) * 60 + int(end[3:]) - int(start[3:])
        melody = normalize(score)
        # 실제 재생 시간만큼 반복 후 슬라이스로 자름.
        played = (melody * (duration // len(melody) + 1))[:duration]
        if target in played and duration > longest:
            # 같은 시간은 갱신하지 않아 먼저 입력된 곡 유지.
            answer, longest = title, duration
    return answer
```

## 다른 방법: 순환 악보 KMP 검색 / KMP over a cyclic score

재생 문자열을 만들지 않고 악보의 순환 인덱스에서 KMP로 찾습니다. 시간 O(|m|+전체 재생 분수), 보조 공간 O(|m|)로 긴 재생에서도 반복 문자열이 필요 없습니다.

Run KMP on cyclic score indices without materializing the playback. It uses O(|m|+total playback minutes) time and O(|m|) auxiliary space.

[alternative.py](alternative.py)

```python
def solution(m, musicinfos):
    def notes(text):
        result = []
        for ch in text:
            if ch == '#':
                result[-1] += '#'
            else:
                result.append(ch)
        return result
    pattern = notes(m)
    failure = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j and pattern[i] != pattern[j]:
            j = failure[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        failure[i] = j
    answer, longest = '(None)', -1
    for record in musicinfos:
        start, end, title, score = record.split(',')
        minutes = lambda text: int(text[:2]) * 60 + int(text[3:])
        duration = minutes(end) - minutes(start)
        melody, j = notes(score), 0
        for i in range(duration):
            note = melody[i % len(melody)]
            while j and note != pattern[j]:
                j = failure[j - 1]
            if note == pattern[j]:
                j += 1
            if j == len(pattern):
                if duration > longest:
                    answer, longest = title, duration
                break
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "ABCDEFG",
    [
      "12:00,12:14,HELLO,CDEFGAB",
      "13:00,13:05,WORLD,ABCDEF"
    ]
  ],
  "output": "HELLO"
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

출처: [프로그래머스 문제 17683](https://school.programmers.co.kr/learn/courses/30/lessons/17683), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17683](https://school.programmers.co.kr/learn/courses/30/lessons/17683), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

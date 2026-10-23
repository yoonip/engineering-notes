# 기능개발

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42586) · Level 2 · Python3

## 문제와 조건 / Task and conditions

작업 수는 최대 100개, 진행도는 1~99, 속도는 1~100입니다. 하루 끝에만 배포하며 앞 기능보다 먼저 끝난 뒤 기능도 기다려야 합니다. 배포별 기능 수를 반환합니다.

There are at most 100 jobs, progress values 1–99 and speeds 1–100. Releases occur at day end in original feature order. Return the number of features in each release.

## 풀이 흐름 / Approach

각 기능이 100에 도달하는 날을 올림 나눗셈으로 구합니다. 맨 앞 기능의 배포일보다 일찍 끝난 뒤 기능은 같은 묶음에 넣습니다. 더 늦게 끝나는 기능이 나오면 새 배포일이 됩니다.

Compute completion days with ceiling division. A later feature finishing no later than the front feature joins its release batch; a later completion starts a new batch.

## 정답이 되는 이유 / Why it works

앞 기능이 배포될 때까지 뒤 기능은 기다려야 합니다. 따라서 현재 묶음의 배포일은 그 묶음에서 가장 늦은 앞쪽 완료일이며, 그 날까지 끝난 연속 기능들이 정확히 함께 배포됩니다.

Later features must wait for the front feature. The current release day groups exactly the consecutive following features completed by that day, proving the greedy batching.

## 비용 / Complexity

시간 O(n), 출력 포함 공간 O(n) / O(n) time and output space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(progresses, speeds):
    answer = []
    # 현재 배포 묶음의 배포일 초기화.
    release_day = 0
    for progress, speed in zip(progresses, speeds):
        # 남은 작업량을 속도로 올림 나눠 완료까지의 일수 계산.
        days = (100 - progress + speed - 1) // speed
        if days > release_day:
            # 현재 기능 한 개 포함.
            answer.append(1)
            release_day = days
        else:
            # 앞 기능과 함께 배포.
            answer[-1] += 1
    return answer
```

## 다른 방법: 날짜별 진행 시뮬레이션 / Day-by-day simulation

하루씩 진행도를 올리고 맨 앞의 완료 기능들을 꺼냅니다. 완료일 수 D에 시간 O(nD)라 큰 입력보다 작은 입력 대조에 알맞습니다.

Advance progress one day at a time and remove consecutive completed front features. It costs O(nD) for D days and is intended for small-input comparison.

[alternative_reference.py](alternative_reference.py)

```python
def solution(progresses, speeds):
    progresses = progresses[:]
    front, answer = 0, []
    while front < len(progresses):
        for i in range(front, len(progresses)):
            progresses[i] += speeds[i]
        count = 0
        while front < len(progresses) and progresses[front] >= 100:
            front += 1
            count += 1
        if count:
            answer.append(count)
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      93,
      30,
      55
    ],
    [
      1,
      30,
      5
    ]
  ],
  "output": [
    2,
    1
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 30개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 30 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 30개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 30 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42586](https://school.programmers.co.kr/learn/courses/30/lessons/42586), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42586](https://school.programmers.co.kr/learn/courses/30/lessons/42586), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

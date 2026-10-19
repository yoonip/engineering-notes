# 카카오 앱 정리하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468374) · Level 3 · Python3

## 문제와 조건 / Task and conditions

판은 각 변 2~10이고 앱 ID는 1부터 연속합니다. 앱은 정사각형이며 0은 빈칸입니다. 명령은 1~1000개, 방향 1·2·3·4는 오른쪽·아래·왼쪽·위입니다. 밀기·반대편 재진입 후 최종 판을 반환합니다.

Both board dimensions are 2–10, with consecutive app IDs from one and square apps; zero is empty. There are 1–1000 commands, with 1/2/3/4 meaning right/down/left/up. Return the board after pushing and wraparound.

## 풀이 흐름 / Approach

앱을 정사각형의 왼쪽 위 좌표와 크기로 관리합니다. 이동 방향으로 좌표를 통일하고, 서로 밀 수 있는 앱 사이의 최소 간격 조건을 만듭니다. 격자 밖으로 일부가 나가면 다음 바퀴 시작점으로 넘기고 필요한 이동을 큐로 전파합니다.

Represent apps by top-left coordinate and square size. Normalize the movement direction and build minimum-spacing constraints between apps that can push each other. Crossing a boundary jumps to the next cycle start; propagate the necessary movements with a queue.

## 정답이 되는 이유 / Why it works

이동축에 수직인 구간이 겹치는 앱의 앞뒤 순서는 원형 격자에서도 유지됩니다. 간격 제약을 위반한 앱만 앞으로 밀며 최소 필요 좌표로 갱신하므로 충돌을 해소하는 최소 밀림 상태를 얻습니다.

Apps overlapping on the perpendicular axis preserve their cyclic front-to-back order. Increasing only coordinates violating spacing constraints to the least required position computes the minimal collision-free pushed configuration.

## 비용 / Complexity

명령 c, 앱 a, 전파 갱신 횟수 R에 O(ca²+R·a), 공간 O(a²+nm) / O(ca²+Ra) time for R propagation updates, O(a²+nm) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import deque

def solution(board, commands):
    # 행·열 수를 두 변수로 나눠 받음.
    n, m = len(board), len(board[0])
    apps = {}
    for r, row in enumerate(board):
        # 각 칸의 열 번호와 앱 ID 순회.
        for c, number in enumerate(row):
            if number:
                if number not in apps:
                    # [] 리스트로 위치와 초기 크기 저장.
                    apps[number] = [r, c, 1]
                else:
                    apps[number][2] = max(apps[number][2], r - apps[number][0] + 1, c - apps[number][1] + 1)
    # 앱 번호 -1이 인덱스.
    apps = [apps[number] for number in range(1, len(apps) + 1)]
    count = len(apps)
    # 한 명령의 두 값을 언패킹.
    for number, direction in commands:
        axis = direction % 2
        # 움직이지 않는 수직 축의 인덱스.
        side = 1 - axis
        length = (n, m)[axis]
        # 왼쪽·위쪽이면 좌표를 반전해 모두 증가 방향으로 계산.
        reverse = direction >= 3
        positions = [length - app[2] - app[axis] if reverse else app[axis] for app in apps]
        # 앱마다 밀림을 전달할 이웃과 최소 간격을 저장하는 인접 리스트 생성.
        graph = [[] for _ in apps]
        for i in range(count):
            # 이전 앱들과만 비교해 중복 쌍을 만들지 않음.
            for j in range(i):
                if apps[i][side] >= apps[j][side] + apps[j][2] or apps[j][side] >= apps[i][side] + apps[i][2]:
                    continue
                # 증가 방향에서 뒤쪽·앞쪽 앱 순서로 번호 배치.
                first, second = (i, j) if positions[i] < positions[j] else (j, i)
                graph[first].append((second, apps[first][2]))
                # 한 바퀴 length를 빼서 같은 좌표계로 표현.
                graph[second].append((first, apps[second][2] - length))

        def normalize(value, size):
            remainder = value % length
            # 앱 전체가 들어가지 않는 시작 위치인지 검사.
            if remainder > length - size:
                value += length - remainder
            return value

        number -= 1
        # 명령 대상 앱을 한 칸 전진시키고 필요하면 반대편으로 넘김.
        positions[number] = normalize(positions[number] + 1, apps[number][2])
        queue = deque([number])
        # 같은 앱을 큐에 중복 저장하지 않기 위한 표시.
        queued = [False] * count
        queued[number] = True
        while queue:
            current = queue.popleft()
            queued[current] = False
            for other, gap in graph[current]:
                needed = normalize(positions[current] + gap, apps[other][2])
                if needed > positions[other]:
                    positions[other] = needed
                    if not queued[other]:
                        queued[other] = True
                        queue.append(other)
        for i, app in enumerate(apps):
            coordinate = positions[i] % length
            app[axis] = length - app[2] - coordinate if reverse else coordinate
    answer = [[0] * m for _ in range(n)]
    for number, (r, c, size) in enumerate(apps, 1):
        for x in range(r, r + size):
            for y in range(c, c + size):
                answer[x][y] = number
    return answer
```

## 다른 방법: 모든 간격 제약을 반복 완화 / Repeated full relaxation of spacing constraints

큐 대신 모든 제약을 반복해서 훑고 더 밀릴 앱이 없을 때 멈춥니다. 같은 좌표 모델을 전역 고정점 반복으로 풀며, 관련 앱만 처리하는 주 풀이보다 불필요한 검사가 많습니다.

Repeatedly scan all spacing constraints until no app needs to move. This solves the same coordinate model with global fixed-point iteration, doing more unnecessary checks than the work-queue method.

[alternative.py](alternative.py)

```python
def solution(board, commands):
    rows, cols = len(board), len(board[0])
    locations = {}
    for r, row in enumerate(board):
        for c, app in enumerate(row):
            if app:
                if app not in locations:
                    locations[app] = [r, c, 1]
                else:
                    locations[app][2] = max(locations[app][2], r - locations[app][0] + 1, c - locations[app][1] + 1)
    apps = [locations[i] for i in range(1, len(locations) + 1)]
    for selected, direction in commands:
        axis, reverse = direction % 2, direction >= 3
        side, length = 1 - axis, (rows, cols)[axis]
        pos = [length - a[2] - a[axis] if reverse else a[axis] for a in apps]
        constraints = []
        for i in range(len(apps)):
            for j in range(i):
                if max(apps[i][side], apps[j][side]) < min(apps[i][side] + apps[i][2], apps[j][side] + apps[j][2]):
                    first, second = (i, j) if pos[i] < pos[j] else (j, i)
                    constraints += [(first, second, apps[first][2]), (second, first, apps[second][2] - length)]
        def normalize(value, size):
            remainder = value % length
            return value + length - remainder if remainder > length - size else value
        i = selected - 1
        pos[i] = normalize(pos[i] + 1, apps[i][2])
        changed = True
        while changed:
            changed = False
            for source, target, gap in constraints:
                required = normalize(pos[source] + gap, apps[target][2])
                if required > pos[target]:
                    pos[target], changed = required, True
        for i, app in enumerate(apps):
            coordinate = pos[i] % length
            app[axis] = length - app[2] - coordinate if reverse else coordinate
    output = [[0] * cols for _ in range(rows)]
    for number, (r, c, size) in enumerate(apps, 1):
        for x in range(r, r + size):
            for y in range(c, c + size):
                output[x][y] = number
    return output
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      [
        0,
        2,
        2,
        0,
        0,
        0,
        0,
        0
      ],
      [
        0,
        2,
        2,
        0,
        0,
        4,
        4,
        0
      ],
      [
        0,
        3,
        3,
        3,
        1,
        4,
        4,
        0
      ],
      [
        0,
        3,
        3,
        3,
        0,
        0,
        0,
        0
      ],
      [
        0,
        3,
        3,
        3,
        5,
        5,
        6,
        0
      ],
      [
        0,
        0,
        0,
        0,
        5,
        5,
        0,
        0
      ]
    ],
    [
      [
        3,
        1
      ],
      [
        3,
        1
      ]
    ]
  ],
  "output": [
    [
      0,
      0,
      2,
      2,
      0,
      0,
      0,
      0
    ],
    [
      4,
      4,
      2,
      2,
      0,
      0,
      0,
      0
    ],
    [
      4,
      4,
      0,
      3,
      3,
      3,
      1,
      0
    ],
    [
      0,
      0,
      0,
      3,
      3,
      3,
      0,
      0
    ],
    [
      6,
      0,
      0,
      3,
      3,
      3,
      5,
      5
    ],
    [
      0,
      0,
      0,
      0,
      0,
      0,
      5,
      5
    ]
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 331개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 331 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 331개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 331 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 468374](https://school.programmers.co.kr/learn/courses/30/lessons/468374), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 468374](https://school.programmers.co.kr/learn/courses/30/lessons/468374), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

1×1 앱은 격자에서 연쇄로 밀릴 앱 집합을 먼저 구한 뒤 동시에 한 칸 옮기는 별도 기준과도 300개 무작위 입력을 대조했습니다. 큰 정사각형 앱의 순환 밀림은 공식 예제와 두 제약 완화 구현으로 확인했습니다.

For 1×1 apps, 300 randomized inputs were also checked against an independent grid model that first finds the push chain and then shifts all affected apps simultaneously. Wraparound of larger square apps was checked through official examples and the two constraint-relaxation implementations.

# 방문 길이

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/49994) · Level 2 · Python3

## 문제와 조건 / Task and conditions

U,D,R,L 명령 1~500개입니다. 시작은 (0,0), 허용 좌표는 두 축 모두 −5~5이며 경계 밖 명령은 무시합니다. 처음 지난 무방향 길 수를 반환합니다.

There are 1–500 U/D/R/L commands. Start at (0,0), remain in [−5,5] on both axes and ignore out-of-bounds moves. Return distinct undirected edges traversed.

## 풀이 흐름 / Approach

좌표가 아니라 두 좌표 사이의 길을 기록합니다. 양끝 좌표를 정렬해 오른쪽으로 간 길과 왼쪽으로 돌아온 길을 같은 키로 만듭니다. 격자를 벗어나는 명령은 무시합니다.

Record edges rather than visited points. Sorting the two endpoints gives the same key for a move and its reverse. Ignore commands that would leave the grid.

## 왜 맞는가 / Why it works

각 유효한 이동은 정확히 하나의 무방향 길에 대응합니다. 같은 길을 왕복해도 정렬된 키가 같으므로 집합의 크기는 처음 방문한 길의 수와 같습니다.

Each valid move corresponds to one undirected edge. Reversed traversal has the same canonical key, so the set cardinality counts exactly the distinct paths.

## 비용 / Complexity

시간 O(n), 공간 O(1): 고정 격자 최대 220개 길 / Time O(n), O(1) space on the fixed 220-edge grid

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(dirs):
    # {} 딕셔너리에 명령별 이동량 () 튜플 저장.
    moves = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
    x = y = 0
    edges = set()
    # 명령 순회.
    for command in dirs:
        dx, dy = moves[command]
        # +로 다음 좌표 계산.
        nx, ny = x + dx, y + dy
        if -5 <= nx <= 5 and -5 <= ny <= 5:
            # 반대 방향 이동도 같은 길로 표현.
            edge = tuple(sorted(((x, y), (nx, ny))))
            edges.add(edge)
            # 유효한 이동에서만 현재 좌표 갱신.
            x, y = nx, ny
    return len(edges)
```

## 다른 방법: 양방향 이동 기록 / Store both directed orientations

각 길의 정방향과 역방향을 함께 저장하고 원소 수를 2로 나눕니다. 정렬이 필요 없는 대신 기록 수가 두 배입니다.

Store both orientations and divide the size by two. This removes endpoint sorting at the cost of twice as many set entries.

[alternative.py](alternative.py)

```python
def solution(dirs):
    x = y = 0
    visited = set()
    moves = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
    for command in dirs:
        dx, dy = moves[command]
        nx, ny = x + dx, y + dy
        if -5 <= nx <= 5 and -5 <= ny <= 5:
            visited.add((x, y, nx, ny))
            visited.add((nx, ny, x, y))
            x, y = nx, ny
    return len(visited) // 2
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "ULURRDLLU"
  ],
  "output": 7
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

출처: [프로그래머스 문제 49994](https://school.programmers.co.kr/learn/courses/30/lessons/49994), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 49994](https://school.programmers.co.kr/learn/courses/30/lessons/49994), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

# 카카오프렌즈 컬러링북

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1829) · Level 2 · C++

## 문제와 조건 / Task and conditions

행·열은 1~100이고 색 값은 0~2³¹−1입니다. 0은 빈칸이며 같은 색 상하좌우 연결만 한 영역입니다. [영역 수,최대 넓이]를 반환합니다.

Both dimensions are 1–100 and colors are in [0,2³¹−1]. Zero is empty; only orthogonally connected equal colors form a region. Return [region count,largest area].

## 풀이 흐름 / Approach

아직 방문하지 않은 0이 아닌 칸을 찾으면 새 영역을 시작합니다. 같은 색의 상하좌우 칸을 DFS로 전부 방문하며 넓이를 셉니다. 대각선으로만 닿은 칸은 연결하지 않습니다.

Start a new region at every unvisited nonzero cell. Traverse equal-colored orthogonal neighbors with DFS and count the area. Diagonal-only contact is not connected.

## 정답이 되는 이유 / Why it works

DFS는 시작점에서 같은 색으로 연결된 칸을 모두, 그리고 그 칸만 방문합니다. 방문 시 표시하므로 영역을 중복 세지 않으며 각 영역의 크기 중 최댓값을 얻습니다.

DFS visits exactly the same-colored component reachable from the start. Marking on discovery prevents duplicate regions and gives each region’s exact size.

## 비용 / Complexity

시간·공간 O(mn), 그림 복사 포함 / O(mn) time and space including the picture copy

## 구현 / Implementation

[solution.cpp](solution.cpp)

```cpp
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

// picture는 값으로 전달되어 함수 안에서 지워도 호출자의 그림은 보존됨.
vector<int> solution(int m, int n, vector<vector<int>> picture) {
    int areas = 0, largest = 0;
    // 네 방향의 행 변화량.
    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    // ++는 1 증가.
    for (int row = 0; row < m; ++row) {
        for (int col = 0; col < n; ++col) {
            // 최대 색 값도 int 범위에 포함.
            int color = picture[row][col];
            if (color == 0) continue;
            ++areas;
            // 시작 칸 방문 표시.
            picture[row][col] = 0;
            vector<pair<int, int>> stack{{row, col}};
            // 현재 영역 넓이.
            int size = 0;
            while (!stack.empty()) {
                // back은 마지막 좌표 조회.
                auto point = stack.back();
                stack.pop_back();
                ++size;
                // 네 방향 이웃 검사.
                for (int direction = 0; direction < 4; ++direction) {
                    int nr = point.first + dr[direction];
                    // 다음 열 계산.
                    int nc = point.second + dc[direction];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && picture[nr][nc] == color) {
                        // 넣을 때 방문 표시해 같은 칸 중복 탐색 방지.
                        picture[nr][nc] = 0;
                        stack.push_back({nr, nc});
                    }
                }
            }
            // 현재 영역 넓이와 최대값 비교.
            largest = max(largest, size);
        }
    }
    return {areas, largest};
}
```

## 다른 방법: 서로소 집합 / Disjoint-set union

같은 색으로 맞닿은 칸을 합친 뒤 루트별 크기를 셉니다. DFS와 달리 재귀·탐색 스택이 없고 연결 관계를 합치는 방식으로 영역을 구합니다.

Union adjacent equal-colored cells and count component sizes by representative. This obtains regions through connectivity merges rather than a traversal stack.

[alternative.py](alternative.py)

```python
def solution(m, n, picture):
    parent = list(range(m * n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for r in range(m):
        for c in range(n):
            if not picture[r][c]:
                continue
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < m and nc < n and picture[nr][nc] == picture[r][c]:
                    parent[find(nr * n + nc)] = find(r * n + c)
    sizes = {}
    for r in range(m):
        for c in range(n):
            if picture[r][c]:
                root = find(r * n + c)
                sizes[root] = sizes.get(root, 0) + 1
    return [len(sizes), max(sizes.values(), default=0)]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    6,
    4,
    [
      [
        1,
        1,
        1,
        0
      ],
      [
        1,
        2,
        2,
        0
      ],
      [
        1,
        0,
        0,
        1
      ],
      [
        0,
        0,
        0,
        1
      ],
      [
        0,
        0,
        0,
        3
      ],
      [
        0,
        0,
        0,
        3
      ]
    ]
  ],
  "output": [
    4,
    5
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

[Python 비교 구현](solution.py)도 함께 제공합니다. 로컬 검증 대상은 Python 비교 구현이며 C++ 원본 채점 기록은 별도입니다.

A [Python counterpart](solution.py) is included. Local Python checks are separate from the original C++ grading record.

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.cpp](submitted_original.cpp)는 당시 원본 파일을 그대로 보존하며, `solution.cpp`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.cpp](submitted_original.cpp) preserves the original file bytes; `solution.cpp` contains the documented implementation.

출처: [프로그래머스 문제 1829](https://school.programmers.co.kr/learn/courses/30/lessons/1829), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 1829](https://school.programmers.co.kr/learn/courses/30/lessons/1829), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)

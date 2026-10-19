# [PCCP 기출문제] 2번 / 석유 시추

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/250136) · Level 2 · Python3

세로 시추관 하나가 만나는 석유 덩어리의 전체 면적 합을 최대화합니다.

## 조건과 입출력

입력 매개변수: `land`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ land의 길이 = 땅의 세로길이 = n ≤ 500
- 1 ≤ land[i]의 길이 = 땅의 가로길이 = m ≤ 500
- 1 ≤ land의 길이 = 땅의 세로길이 = n ≤ 100
- 1 ≤ land[i]의 길이 = 땅의 가로길이 = m ≤ 100

## 풀이를 따라가기

석유 연결 요소마다 DFS로 크기와 지나가는 열의 집합을 구합니다. 해당 열 각각에 덩어리 크기를 한 번씩 더합니다. 열별 합계의 최댓값이 답입니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(land):
    rows, cols = len(land), len(land[0])
    totals = [0] * cols
    for r in range(rows):
        for c in range(cols):
            if land[r][c] == 0:
                continue
            stack = [(r, c)]
            # 발견 즉시 방문 표시해 같은 칸을 중복으로 넣지 않는다.
            land[r][c] = 0
            columns = set()
            size = 0
            while stack:
                x, y = stack.pop()
                size += 1
                # 시추관이 같은 덩어리를 여러 칸에서 만나도 한 번만 센다.
                columns.add(y)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and land[nx][ny] == 1:
                        land[nx][ny] = 0
                        stack.append((nx, ny))
            # 덩어리 크기 전체를 닿는 열마다 한 번씩 더한다.
            for column in columns:
                totals[column] += size
    return max(totals)
```

## 정답이 되는 이유

한 열이 같은 덩어리를 여러 칸에서 만나도 회수하는 양은 그 덩어리 전체 한 번입니다. 열 집합으로 중복을 없애면 각 시추관의 회수량을 정확히 더합니다.

시간 O(RC), 공간 O(RC) / Time and space O(RC)

주의할 점: 원본 풀이는 방문한 석유를 0으로 바꿉니다. 같은 지도로 다시 호출하려면 복사본을 전달합니다.

## 다른 방법: 분리 집합으로 덩어리 연결

```python
def solution(land):
    rows, cols = len(land), len(land[0])
    parent = list(range(rows*cols))
    size = [1]*(rows*cols)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        a,b = find(a),find(b)
        if a==b:
            return
        if size[a] < size[b]:
            a,b=b,a
        parent[b]=a
        size[a]+=size[b]
    for r in range(rows):
        for c in range(cols):
            if land[r][c]:
                if r and land[r-1][c]: union(r*cols+c,(r-1)*cols+c)
                if c and land[r][c-1]: union(r*cols+c,r*cols+c-1)
    return max(sum(size[root] for root in {find(r*cols+c) for r in range(rows) if land[r][c]}) for c in range(cols))
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 석유 연결 요소마다 DFS로 크기와 지나가는 열의 집합을 구합니다. 해당 열 각각에 덩어리 크기를 한 번씩 더합니다. 열별 합계의 최댓값이 답입니다. | 분리 집합으로 덩어리 연결 |
| 비용 | 시간 O(RC), 공간 O(RC) / Time and space O(RC) | 시간 O(RC α(RC)), 공간 O(RC) / Time O(RC α(RC)), space O(RC) |

## 검증

공식 예제 2개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Maximize the total area of oil components touched by one vertical drilling column.

### Conditions and input/output

Input arguments: `land`. The return value is an integer satisfying the task described below.

- 1 ≤ rows,columns ≤ 500; land[i][j] ∈ {0,1}
- accuracy-only subtests: rows,columns ≤ 100; efficiency subtests use the full bounds

### Approach

DFS each oil component, collecting its size and set of columns. Add its size once to every touched column, then take the maximum column total.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Touching one component at multiple cells still extracts it only once. The set of columns removes exactly those duplicates.

시간 O(RC), 공간 O(RC) / Time and space O(RC)

Boundary cases: The main implementation marks visited oil as zero. Pass a copy when reusing the same grid.

### Alternative: Disjoint-set union for component labeling

시간 O(RC α(RC)), 공간 O(RC) / Time O(RC α(RC)), space O(RC)

### Verification

Local checks covered 2 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: [PCCP 기출문제] 2번 / 석유 시추](https://school.programmers.co.kr/learn/courses/30/lessons/250136) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.

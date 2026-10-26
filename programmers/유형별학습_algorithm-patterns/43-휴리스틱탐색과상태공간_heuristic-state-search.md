# 휴리스틱 탐색과 상태 공간, A*와 탐색 한계

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 탐색 순서에 정보를 더하기

BFS나 Dijkstra는 목표가 어느 방향인지 모른 채 순서를 정합니다. 휴리스틱 h(s)는 상태 s에서 목표까지 남은 비용의 추정값입니다. A*는 이미 쓴 비용 g(s)와 추정값을 더한 f(s)=g(s)+h(s)가 작은 후보부터 확인합니다.

목표에 가까워 보인다는 이유만으로 h만 최소화하면, 이미 크게 돌아온 경로를 선호할 수 있습니다. Greedy best-first는 탐색 순서를 빠르게 유도하지만 같은 최적성 보장을 갖지 않습니다. [CMU Search의 Informed Search 절](https://www.cs.cmu.edu/~15281/coursenotes/search/index.html)은 두 우선순위와 허용성·일관성을 구분합니다.

## 허용성과 일관성의 차이

이 문서에서 허용적(admissible) 휴리스틱은 실제 남은 최소 비용 h*(s)에 대해 0≤h(s)≤h*(s)를 만족합니다. 따라서 목표에서는 h=0입니다. 일관적(consistent) 휴리스틱은 모든 간선 u→v에서 h(u)≤w(u,v)+h(v)를 만족하고 목표에서 0입니다. 비음수 비용의 유한 그래프를 기준으로, 일관성은 닫힌 상태를 다시 열지 않는 일반적인 A* 그래프 탐색의 안전한 확정 근거를 제공합니다.

허용적이지만 일관적이지 않은 경우에는 더 좋은 g를 찾았을 때 이미 처리한 상태도 다시 열어야 할 수 있습니다. 단순히 visited를 영구 표시한 구현에 허용성만 주장하면 충분하지 않습니다. h=0이면 Dijkstra가 됩니다.

## 직접 구성한 격자 예제

상하좌우 이동 비용이 1인 격자에서 현재 칸 (x,y), 목표 (a,b)에 h=|x-a|+|y-b|를 사용합니다. 장애물을 무시한 최소 이동 수이므로 장애물 있는 실제 경로를 과대평가하지 않습니다. 한 번 이동하면 h가 최대 1만 바뀌므로 일관성도 만족합니다.

S=(0,0), G=(2,2)이면 h(S)=4입니다. (1,0)에 도착한 후보는 g=1,h=3,f=4입니다. 벽 때문에 돌아가는 후보는 g가 늘어나면서 f도 커집니다. 목표를 처음 생성했을 때가 아니라 유효한 최소 f 후보로 꺼낼 때 종료합니다.

대각선 이동을 비용 1에 허용하면 Manhattan 거리는 실제보다 커질 수 있습니다. 이 경우 해당 이동 모형의 하한인 Chebyshev 거리 등을 검토합니다. 포탈이 멀리 이동시켜 준다면 좌표 거리 자체가 하한이 아닐 수 있습니다.

## 실행 절차와 비용

1. 상태의 최선 g와 부모를 저장합니다.
2. 우선순위 큐에 (g+h, g, 상태)를 넣습니다.
3. 최선 g와 다른 낡은 후보는 버립니다.
4. 더 좋은 경로가 나오면 g와 부모를 갱신합니다.
5. 일관성 여부에 맞춰 재확장 정책을 정합니다.

좋은 h가 탐색량을 줄일 수 있지만 항상 적은 상태만 보는 것은 아닙니다. 최악에는 상태 수가 분기 수 b와 해 깊이 d에 대해 지수적으로 늘 수 있고, 저장한 후보가 메모리 병목이 됩니다. 고정된 유한 상태 그래프의 힙 비용과 문제 크기에 따른 상태 수 증가를 따로 계산합니다.

정확한 남은 비용을 h로 쓰면 유용하지만, 그 값을 계산하는 일이 원래 문제만큼 비쌀 수 있습니다. 추정값 한 번의 계산 비용과 줄어드는 확장 수를 함께 비교합니다. 장애물을 제거한 완화 문제, 패턴 데이터베이스처럼 더 쉬운 하위 문제의 정확한 비용이 하한을 만드는 방법이 됩니다.

## IDA*, branch and bound와 빔 탐색

IDA*는 f의 임계값을 두고 DFS를 반복하며, 현재 임계값을 넘긴 f 중 최솟값을 다음 임계값으로 선택합니다. 경로 중심으로 저장해 메모리를 줄이지만 같은 상태를 반복 계산할 수 있습니다. 양의 최소 간선 비용 또는 유한한 상태·사이클 처리 같은 종료 조건을 확인합니다.

최소화 branch and bound는 현재 최선의 실행 가능한 답을 상한 U로 두고, 부분 선택에서 가능한 최선의 하한 L이 U 이상이면 가지를 버립니다. 모든 동점 해도 필요하면 L=U인 가지를 버리는 정책을 다시 정합니다. 하한이 틀리면 최적해를 잘라내는 오답이 됩니다.

빔 탐색은 층마다 후보 일부만 남깁니다. 메모리·시간을 제한하기 쉽지만 정답 경로가 잘릴 수 있어 완전성과 최적성이 일반적으로 없습니다. A*와 동일한 정답 보장이라고 표시하지 않습니다. 탐욕 탐색, 가지치기, DP의 지배 상태 제거도 각각 안전성의 조건이 다릅니다.

## 응답에 따라 후보를 줄이는 질문 선택

정답 후보 집합이 있고 질문의 응답마다 남는 후보가 달라지면, 다음 질문이 만드는 가장 큰 그룹을 작게 하는 방법을 검토합니다. 직접 만든 후보 네 개에서 질문 A의 응답 그룹 크기가 3·1이고 질문 B가 2·2라면, 이번 한 번의 질문 뒤 최악의 후보 수는 B가 더 작습니다.

이 선택은 한 단계의 최대 잔여 수를 비교하는 minimax 기준입니다. 이후의 모든 질문 수까지 전역 최적으로 만드는지는 별도 분석이 필요합니다. 후보의 확률이 다르면 기대 정보량이나 평균 비용을 목표로 삼을 수도 있으며, 최악 그룹 최소화와 같은 목적이 아닙니다. 보관한 숫자 야구 풀이의 다음 질문 선택은 이 관점으로 읽을 수 있습니다.

## 실제 연결과 언어별 주의

정적인 격자 경로 계획, 퍼즐, 계획 문제의 축소 모형에 사용합니다. 실제 로봇은 위치 오차·동적 장애물·차량 운동학을 추가로 다루므로 격자 A* 통과만으로 운행 안전성을 주장할 수 없습니다. 이 연결은 특정 제품의 적용 사례가 아닌 모델의 예입니다.

C/C++은 상태 키·힙·부모 정보의 메모리를 계산합니다. Python은 큰 튜플이나 경로 전체를 후보마다 복제하지 않도록 상태를 작게 표현합니다. 비교 불가능한 사용자 객체가 동점 키 뒤에 놓이면 힙 비교가 실패할 수 있으므로 안정적인 번호를 함께 두는 방법을 사용합니다.

## 복습

복습: 장애물이 없는 거리의 두 배를 h로 사용하면 더 빨라 보이는데 항상 최적해인지 설명합니다. 답은 과대 추정으로 허용성이 깨져 일반 A* 최적성 보장을 사용할 수 없다는 점입니다. 근사 탐색을 선택했다면 그 변경과 허용하는 오차를 별도로 설명해야 합니다.

[CMU Andrew Moore의 A*·IDA* 튜토리얼](https://www.cs.cmu.edu/afs/cs/Web/People/awm/tutorials/astar.html)은 비용 추정과 메모리 절충을 더 읽는 자료입니다. 본문은 원문 슬라이드의 재배포가 아닌 자체 예제와 설명입니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

작은 장애물 격자에서 g+h가 최소인 열린 칸을 직접 골라 A*를 실행합니다. 상하좌우 비용은 1이며 Manhattan 하한이 일관적이므로 닫은 칸을 다시 열지 않습니다. 힙·IDA*·빔 탐색·경로 복원은 구현하지 않습니다.

이 예제에서 직접 구현하는 기법은 A* · 허용적·일관적인 Manhattan 하한 · 최선 g 완화 · 최소 f 목표 종료입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

R C 뒤에 R개의 격자 문자열이 주어집니다. 1≤R,C≤5, .은 통로이고 #은 벽입니다. 출발점은 (0,0), 목표는 (R-1,C-1)이며 두 끝점이 벽일 수도 있습니다.

```text
3 4
....
.##.
....
```

최소 이동 횟수를 출력합니다. 끝점이 벽이거나 경로가 없으면 -1입니다.

```text
5
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 출발 칸 0: g=0, h=5, f=5 | 장애물을 무시한 Manhattan 거리를 하한으로 사용합니다. |
| 2 | 칸 (0,1): g=1, h=4, f=5 | 통로를 한 칸 이동하면 g는 1 늘고 h는 1 줄어듭니다. |
| 3 | 벽 (1,1),(1,2)는 이웃 후보에서 제외 | 격자 범위와 벽을 확인한 뒤에만 거리 배열을 갱신합니다. |
| 4 | 목표 (2,3)를 꺼낼 때 g=5, h=0, f=5 | 일관적인 하한 아래에서 목표를 최소 f로 꺼낸 시점에 답을 확정합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/43-휴리스틱탐색과상태공간_heuristic-state-search/example.c>)

```c
#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    scanf("%32s", text);  // 종료 문자까지 들어갈 33칸 버퍼 사용
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 최소 f 스캔 방식의 실제 A* 탐색
    int rows = read_int(), cols = read_int(), distance[25], closed[25] = {0};  // 격자 크기·최선 g·닫힌 상태
    char grid[5][33];  // 토큰 입력 함수의 최대 폭을 담는 행 버퍼
    for (int r = 0; r < rows; ++r) read_word(grid[r]);  // 격자의 벽과 통로 읽기
    if (grid[0][0] == '#' || grid[rows - 1][cols - 1] == '#') { write_text("-1\n"); return 0; }  // 막힌 끝점은 즉시 제외
    int vertices = rows * cols, answer = -1;  // 상태 수와 아직 없는 도착 답
    const int inf = 1000000;  // 가능한 격자 경로보다 큰 미도달 값
    int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1};  // 상·우·하·좌 이동
    for (int v = 0; v < vertices; ++v) distance[v] = inf;  // 모든 칸의 g 초기화
    distance[0] = 0;  // 출발점의 실제 비용
    for (int step = 0; step < vertices; ++step) {  // 각 칸은 최대 한 번 확장
        int u = -1, best = inf;  // 다음 최소 f 후보
        for (int v = 0; v < vertices; ++v) {  // 열린 후보의 f를 직접 비교
            if (closed[v] || distance[v] == inf) continue;  // 닫혔거나 아직 미발견인 칸 제외
            int h = rows - 1 - v / cols + cols - 1 - v % cols;  // 목표까지의 Manhattan 하한
            int score = distance[v] + h;  // A* 우선순위 g+h
            if (score < best) { best = score; u = v; }  // 동률은 작은 칸 번호 유지
        }  // 최소 f 선택 끝
        if (u == -1) break;  // 더 갈 열린 상태가 없음
        if (u == vertices - 1) { answer = distance[u]; break; }  // 목표를 최소 f로 꺼냈을 때만 종료
        closed[u] = 1;  // 일관성으로 현재 g 확정
        int row = u / cols, col = u % cols;  // 번호를 행·열로 복원
        for (int direction = 0; direction < 4; ++direction) {  // 네 방향 전이
            int nr = row + dr[direction], nc = col + dc[direction];  // 이웃 좌표
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == '#') continue;  // 경계와 벽 확인
            int v = nr * cols + nc;  // 이웃의 상태 번호
            if (!closed[v] && distance[u] + 1 < distance[v]) distance[v] = distance[u] + 1;  // 더 좋은 열린 상태의 g 갱신
        }  // 이웃 완화 끝
    }  // 목표 확정 또는 탐색 실패
    write_number(answer); write_text("\n"); return 0;  // 최소 이동 또는 -1 출력
}  // A* 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/43-휴리스틱탐색과상태공간_heuristic-state-search/example.cpp>)

```cpp
#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    cin.width(33);  // 종료 문자를 포함한 버퍼 크기로 읽기 제한
    cin >> text;  // 공백 전까지의 토큰 읽기
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    cout << value;  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 최소 f 스캔 방식의 실제 A* 탐색
    int rows = read_int(), cols = read_int(), distance[25], closed[25] = {};  // 격자 크기·최선 g·닫힌 상태
    char grid[5][33];  // 토큰 입력 함수의 최대 폭을 담는 행 버퍼
    for (int r = 0; r < rows; ++r) read_word(grid[r]);  // 격자의 벽과 통로 읽기
    if (grid[0][0] == '#' || grid[rows - 1][cols - 1] == '#') { write_text("-1\n"); return 0; }  // 막힌 끝점은 즉시 제외
    int vertices = rows * cols, answer = -1;  // 상태 수와 아직 없는 도착 답
    const int inf = 1000000;  // 가능한 격자 경로보다 큰 미도달 값
    int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1};  // 상·우·하·좌 이동
    for (int v = 0; v < vertices; ++v) distance[v] = inf;  // 모든 칸의 g 초기화
    distance[0] = 0;  // 출발점의 실제 비용
    for (int step = 0; step < vertices; ++step) {  // 각 칸은 최대 한 번 확장
        int u = -1, best = inf;  // 다음 최소 f 후보
        for (int v = 0; v < vertices; ++v) {  // 열린 후보의 f를 직접 비교
            if (closed[v] || distance[v] == inf) continue;  // 닫혔거나 아직 미발견인 칸 제외
            int h = rows - 1 - v / cols + cols - 1 - v % cols;  // 목표까지의 Manhattan 하한
            int score = distance[v] + h;  // A* 우선순위 g+h
            if (score < best) { best = score; u = v; }  // 동률은 작은 칸 번호 유지
        }  // 최소 f 선택 끝
        if (u == -1) break;  // 더 갈 열린 상태가 없음
        if (u == vertices - 1) { answer = distance[u]; break; }  // 목표를 최소 f로 꺼냈을 때만 종료
        closed[u] = 1;  // 일관성으로 현재 g 확정
        int row = u / cols, col = u % cols;  // 번호를 행·열로 복원
        for (int direction = 0; direction < 4; ++direction) {  // 네 방향 전이
            int nr = row + dr[direction], nc = col + dc[direction];  // 이웃 좌표
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == '#') continue;  // 경계와 벽 확인
            int v = nr * cols + nc;  // 이웃의 상태 번호
            if (!closed[v] && distance[u] + 1 < distance[v]) distance[v] = distance[u] + 1;  // 더 좋은 열린 상태의 g 갱신
        }  // 이웃 완화 끝
    }  // 목표 확정 또는 탐색 실패
    write_number(answer); write_text("\n"); return 0;  // 최소 이동 또는 -1 출력
}  // A* 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/43-휴리스틱탐색과상태공간_heuristic-state-search/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    rows, cols = int(next(tokens)), int(next(tokens))  # 격자 크기
    grid = [next(tokens) for _ in range(rows)]  # 벽과 통로 문자열
    if grid[0][0] == "#" or grid[-1][-1] == "#":  # 출발점이나 목표가 벽이면
        print(-1)  # 경로 없음 표시
        return  # 탐색을 시작하지 않기
    vertices = rows * cols  # 격자 칸을 일차원 상태로 표현
    inf = 10 ** 6  # 가능한 이동 수보다 큰 미도달 값
    distance = [inf] * vertices  # 상태별 최선 g
    closed = [False] * vertices  # 확정한 상태 표시
    distance[0] = 0  # 출발점 실제 비용
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상·우·하·좌 순서
    answer = -1  # 아직 경로를 찾지 못한 상태
    for _ in range(vertices):  # 상태별 최대 한 번 확장
        u, best = -1, inf  # 다음 최소 f 후보
        for v in range(vertices):  # 열린 상태의 우선순위 직접 비교
            if closed[v] or distance[v] == inf:  # 닫혔거나 미발견인 칸
                continue  # 후보에서 제외
            h = rows - 1 - v // cols + cols - 1 - v % cols  # Manhattan 거리 하한
            score = distance[v] + h  # A*의 g+h
            if score < best:  # 작은 f를 우선하며 동률은 먼저 본 번호 유지
                best, u = score, v  # 이번 확장 후보 갱신
        if u == -1:  # 열린 후보가 더 없으면
            break  # 경로 탐색 실패
        if u == vertices - 1:  # 목표를 유효한 최소 f로 꺼낸 경우
            answer = distance[u]  # 최단 이동 수 확정
            break  # 생성 시점보다 늦게 종료
        closed[u] = True  # 일관성에 따라 재확장 없이 확정
        row, col = divmod(u, cols)  # 현재 칸의 행·열
        for dr, dc in directions:  # 네 방향 이웃 확인
            nr, nc = row + dr, col + dc  # 이웃 좌표
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":  # 범위와 벽 먼저 검사
                continue  # 이동할 수 없는 칸 제외
            v = nr * cols + nc  # 이웃의 상태 번호
            if not closed[v] and distance[u] + 1 < distance[v]:  # 더 짧은 열린 경로 확인
                distance[v] = distance[u] + 1  # 최선 실제 비용 갱신
    print(answer)  # 최단 거리 또는 미도달 -1

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 입력과 출력 | scanf와 fputs를 감싼 함수를 사용합니다. | cin과 cout을 감싼 함수를 사용합니다. | 입력을 split으로 나누고 print로 출력합니다. |
| 작업 배열 | 입력 형식에 명시한 작은 상한의 고정 배열을 사용합니다. | 절차 비교를 위해 C와 같은 고정 배열을 사용합니다. 가변 길이 배열이나 bits 헤더는 사용하지 않습니다. | 입력 크기에 맞춘 리스트를 생성합니다. |
| 정수와 상태 | 예제의 값 범위가 int 안에 들어가도록 상한을 제한합니다. | 같은 정수 범위와 상태 전이를 사용합니다. | int는 가변 정밀도이지만 이 예제는 작은 정수만 사용합니다. |

### 예제의 비용과 실행 파일

- 시간: O(V²), V=R×C
- 보조 공간: O(V)

열린 상태에서 최소 f를 전체 스캔하므로 O(V²)입니다. 일관적인 Manhattan 휴리스틱 때문에 상태당 한 번 확장하며 이웃은 최대 4개입니다.

[예제 입력](<예제_examples/43-휴리스틱탐색과상태공간_heuristic-state-search/input.txt>) · [예상 출력](<예제_examples/43-휴리스틱탐색과상태공간_heuristic-state-search/output.txt>) · [예제 실행 방법](<예제_examples/43-휴리스틱탐색과상태공간_heuristic-state-search/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 3 | 451808 숫자 야구 | [C](<../C/level3/007_451808_숫자_야구/README.md>) | [C++](<../C++/level3/007_451808_숫자_야구/README.md>) | [Python](<../Python/level3/007_451808_숫자_야구/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/heuristic-search.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.

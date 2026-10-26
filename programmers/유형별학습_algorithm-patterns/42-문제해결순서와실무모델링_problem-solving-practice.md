# 문제 해결 순서와 학습 경로, 실무 모델링

[학습 목차](README.md) · [유형별 연습문제](연습문제_problem-index.md)

## 유형을 외우는 목적

유형은 정답 코드를 기억하는 표지가 아니라, 새로운 조건을 이미 이해한 구조에 연결하는 도구입니다. 같은 BFS라도 상태가 다르고, 같은 DP라도 독립적으로 합칠 수 있는 정보가 다릅니다. 한 문제에 정렬·그리디·투포인터가 함께 쓰이는 것도 자연스럽습니다.

문제 제목이나 특정 단어만 보고 유형을 결정하지 않습니다. 최단이라는 말이 있어도 간선 비용이 다르면 BFS가 아닐 수 있고, 최댓값이라는 말이 있어도 그리디가 성립하지 않을 수 있습니다. 필요한 연산, 상태의 재사용, 단조성, 미래 선택에 미치는 영향을 확인합니다.

## 풀이를 만드는 순서

1. 입력, 출력, 가능한 선택, 불가능한 경우를 자신의 말로 다시 적습니다.
2. 정답을 직접 정의대로 계산하는 작은 완전 탐색을 생각합니다.
3. 입력 크기로 후보의 시간·공간 비용을 추산합니다.
4. 반복되는 하위 문제, 정렬 후 구조, 경계의 단조성, 연결 관계를 찾습니다.
5. 상태·전이·불변식 또는 안전한 선택의 근거를 적습니다.
6. 작은 예제를 손으로 추적하고 반례를 시도합니다.
7. 언어별 자료형과 컨테이너를 정한 뒤 구현합니다.
8. 정답과 성능을 별도로 확인하고 남은 불확실성을 기록합니다.

이 순서는 고정 시간표가 아닙니다. 문제의 규칙을 잘못 이해했다면 빠른 자료구조 선택보다 명세 확인으로 돌아가는 것이 필요합니다.

## 조건에서 시작하는 비교표

| 관찰한 구조 | 먼저 검토할 도구 | 꼭 확인할 조건 |
| --- | --- | --- |
| 같은 값을 자주 세거나 찾음 | 해시·빈도 배열 | 값 범위·중복 의미입니다. |
| 구간의 합을 반복 질의 | 누적합·Fenwick·세그먼트 트리 | 수정 여부·결합 연산입니다. |
| 정렬 후 양끝을 줄일 수 있음 | 투포인터 | 버린 후보가 다시 답이 되지 않는 근거입니다. |
| 답 후보의 가능 여부가 한 방향으로 바뀜 | 매개변수 탐색 | 판정의 단조성과 판정 자체의 정당성입니다. |
| 같은 상태에서 미래가 같음 | DP·메모이제이션 | 미래 결정에 필요한 정보를 상태가 모두 포함하는지입니다. |
| 한 번의 행동으로 다른 상태 이동 | 그래프 탐색 | 비용·상태 수·방향입니다. |
| 지금 고른 것을 최적해와 교환 가능 | 그리디 | 교환 뒤 남은 제약을 계속 만족하는지입니다. |
| 대부분의 후보를 일찍 버릴 수 있음 | 백트래킹·branch and bound | 가지치기가 최적해를 지우지 않는지입니다. |

## 기초에서 심화로 잇는 경로

기초 문법과 배열·문자열을 구현한 뒤, 정렬·해시·스택·큐·힙의 연산 비용을 익힙니다. 누적합·투포인터·이진 탐색으로 반복 계산과 후보 범위를 줄이고, 완전 탐색·백트래킹으로 상태 공간의 크기를 체감합니다.

그 다음 BFS·DFS의 방문 의미를 구별하고, 그리디의 교환 논증과 DP의 상태·전이를 비교합니다. 최단 경로·DSU·MST·위상 순서·트리 DP를 연결하면 그래프 문제의 목적 함수가 보입니다. 구간 자료구조·오프라인 질의·문자열 구조·정수론·유량·DP 최적화는 실제 필요 조건을 만났을 때 심화합니다.

처음부터 모든 고급 구조를 구현할 필요는 없습니다. 이미 아는 방법이 어느 입력에서 왜 부족한지 설명할 수 있을 때 다음 도구의 목적을 이해하기 쉽습니다. 학습 순서는 선행 개념에 따른 안내이며 난이도 레벨과 일대일 대응하지 않습니다.

## 한 문제를 비교하며 복습하기

처음에는 대표 풀이를 읽기 전에 작은 기준 풀이를 만듭니다. 이후 그리디·DP처럼 다른 방법이 가능한지, 입력을 바꾸면 어느 방법이 깨지는지 비교합니다. 마지막으로 C·C++·Python에서 같은 상태를 어떻게 저장하는지 읽습니다.

복습 기록에는 조건, 핵심 상태, 정당성 한 문장, 놓친 반례, 비용, 다른 문제로 옮길 수 있는 원리를 적습니다. 코드 길이나 통과 횟수 자체보다 어떤 가정을 놓쳤는지가 다음 문제에 도움이 됩니다. 공개 풀이와 자기 풀이의 차이도 정답 여부와 별도로 비교합니다.

## 코딩 테스트에서 실제 시스템으로

자체 모형으로 배송 거점을 가장 싸게 연결한다면 MST를 검토할 수 있습니다. 실제 배송은 트럭 용량·운행 순서·시간대·여러 차량의 상호작용이 있어 전체 연결 비용만으로 해결되지 않습니다. 작은 알고리즘 모형은 큰 문제의 한 부분을 정확히 해결하는 도구입니다.

업무 스케줄의 선후 관계는 DAG로 표현할 수 있습니다. 인력 한 명만 작업할 수 있다면 DAG의 임계 경로가 최소 완료 시간의 하한일 수는 있어도 실행 일정 전체를 정하지는 않습니다. 자원 제약을 추가한 다른 최적화 문제가 됩니다.

실무에 옮길 때는 데이터 크기와 품질, 갱신 빈도, 최악 지연, 장애 복구, 동시성, 설명 가능성과 유지보수 비용을 함께 봅니다. 정확한 최적해가 필요한지, 실행 가능한 근사해와 오차 설명이 더 유용한지도 목적에 따라 정합니다.

## 답을 읽을 때 확인할 사항

같은 문제의 C와 Python 구현이 같은 알고리즘이라는 보장은 없습니다. 이 카테고리는 대표 보관 풀이를 기준으로 유형을 연결하고, 다른 언어의 세부 구현은 각 풀이 문서로 연결합니다. 비교용 코드와 미완료 시도는 통과 코드와 구별합니다. 사이트의 미래 신규 문제까지 포함한다는 뜻도 아닙니다.

문제 해결을 상태·전이·비용으로 표현하는 관점은 [CMU Search의 Search Problem 절](https://www.cs.cmu.edu/~15281/coursenotes/search/index.html)과 연결됩니다. 이 문서의 배송·스케줄 사례는 특정 회사의 도입 사례가 아닌 자체 구성 모형입니다.

복습: 유형이 두 개 이상 보이면 무엇을 주유형으로 정할지 설명합니다. 답은 정답을 결정하는 핵심 구조와 비용을 줄인 주된 기법을 우선하고, 보조 기법도 함께 기록하는 것입니다. 분류명 자체보다 풀이 선택의 근거가 우선입니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

모든 도로 비용이 1인 무방향 배송 모형에서 0번 출발→필수 중간 지점→목적지를 두 BFS로 나눕니다. 정점 재방문을 허용하며 차량 용량·시간창·혼잡은 다루지 않습니다.

이 예제에서 직접 구현하는 기법은 상태·전이·비용 모델링 · 필수 지점 분해 · BFS · 불가능한 구간 판정입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

V E C T 뒤에 E개의 무방향 간선 u v가 주어집니다. 1≤V≤8, 0≤E≤28, 0≤C,T<V이며 출발점은 0입니다. 자기 간선·평행 간선은 없습니다.

```text
5 5 2 4
0 1
1 2
0 3
3 2
2 4
```

필수 중간 지점 C를 거쳐 T에 가는 최소 간선 수를 출력합니다. 불가능하면 -1입니다.

```text
3
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 상태=현재 위치, 전이 비용=도로당 1 | 동일 비용이고 추가 자원이 없으므로 BFS를 선택합니다. |
| 2 | 0에서의 distance=[0,1,2,1,3] | 출발점에서 필수 지점 2까지 최소 거리는 2입니다. |
| 3 | 2에서의 distance=[2,1,0,1,1] | 필수 지점 이후 목적지 4까지 거리는 1입니다. |
| 4 | first=2, second=1, 결과=3 | 각 구간의 하한을 동시에 달성하는 경로를 이어 붙입니다. 정점 재방문은 허용합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/42-문제해결순서와실무모델링_problem-solving-practice/example.c>)

```c
#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int n, adj[8][8];  // 위치만 상태로 삼는 작은 도로망
static int bfs_distance(int start, int goal) {  // 동일 비용 도로의 최소 이동 횟수
    int distance[8], queue[8], head = 0, tail = 0;  // 거리와 FIFO 큐
    for (int i = 0; i < n; ++i) distance[i] = -1;  // 아직 도달하지 않은 위치
    distance[start] = 0; queue[tail++] = start;  // 출발 위치 발견
    while (head < tail) {  // 가까운 위치부터 이웃 확인
        int u = queue[head++];  // 다음 위치
        for (int v = 0; v < n; ++v) {  // 도로로 이어진 이웃 후보
            if (adj[u][v] && distance[v] == -1) {  // 아직 발견하지 않은 연결 위치
                distance[v] = distance[u] + 1; queue[tail++] = v;  // 한 도로를 더 간 거리 기록
            }  // 새 위치 처리 끝
        }  // u의 도로 확인 끝
    }  // 도달 가능한 위치 탐색 끝
    return distance[goal];  // 불가능하면 초기값 -1
}  // 거리 계산 함수 끝
int main(void) {  // 단순 배송 명세를 두 거리 문제로 해결
    n = read_int(); int m = read_int(), checkpoint = read_int(), target = read_int();  // 도로망과 두 도착 조건
    for (int i = 0; i < m; ++i) {  // 도로 입력
        int a = read_int(), b = read_int();  // 양끝 위치
        adj[a][b] = adj[b][a] = 1;  // 왕복 가능한 도로
    }  // 도로망 구성 끝
    int first = bfs_distance(0, checkpoint), second = bfs_distance(checkpoint, target);  // 필수 지점 전후를 독립 계산
    write_number(first < 0 || second < 0 ? -1 : first + second);  // 두 구간이 모두 가능할 때만 합산
    write_text("\n"); return 0;  // 결과 줄을 마치고 종료
}  // 모델링 예제 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/42-문제해결순서와실무모델링_problem-solving-practice/example.cpp>)

```cpp
#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    cout << value;  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int n, adj[8][8];  // 위치만 상태로 삼는 작은 도로망
static int bfs_distance(int start, int goal) {  // 동일 비용 도로의 최소 이동 횟수
    int distance[8], queue[8], head = 0, tail = 0;  // 거리와 FIFO 큐
    for (int i = 0; i < n; ++i) distance[i] = -1;  // 아직 도달하지 않은 위치
    distance[start] = 0; queue[tail++] = start;  // 출발 위치 발견
    while (head < tail) {  // 가까운 위치부터 이웃 확인
        int u = queue[head++];  // 다음 위치
        for (int v = 0; v < n; ++v) {  // 도로로 이어진 이웃 후보
            if (adj[u][v] && distance[v] == -1) {  // 아직 발견하지 않은 연결 위치
                distance[v] = distance[u] + 1; queue[tail++] = v;  // 한 도로를 더 간 거리 기록
            }  // 새 위치 처리 끝
        }  // u의 도로 확인 끝
    }  // 도달 가능한 위치 탐색 끝
    return distance[goal];  // 불가능하면 초기값 -1
}  // 거리 계산 함수 끝
int main(void) {  // 단순 배송 명세를 두 거리 문제로 해결
    n = read_int(); int m = read_int(), checkpoint = read_int(), target = read_int();  // 도로망과 두 도착 조건
    for (int i = 0; i < m; ++i) {  // 도로 입력
        int a = read_int(), b = read_int();  // 양끝 위치
        adj[a][b] = adj[b][a] = 1;  // 왕복 가능한 도로
    }  // 도로망 구성 끝
    int first = bfs_distance(0, checkpoint), second = bfs_distance(checkpoint, target);  // 필수 지점 전후를 독립 계산
    write_number(first < 0 || second < 0 ? -1 : first + second);  // 두 구간이 모두 가능할 때만 합산
    write_text("\n"); return 0;  // 결과 줄을 마치고 종료
}  // 모델링 예제 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/42-문제해결순서와실무모델링_problem-solving-practice/example.py>)

```python
import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n, m, checkpoint, target = (int(next(tokens)) for _ in range(4))  # 위치 수·도로 수·필수 지점·목표
    adj = [[0] * n for _ in range(n)]  # 단위 비용 도로의 인접 행렬
    for _ in range(m):  # 양방향 도로 입력
        a, b = int(next(tokens)), int(next(tokens))  # 도로 양끝
        adj[a][b] = adj[b][a] = 1  # 두 방향 이동 허용
    def bfs_distance(start, goal):  # 위치만으로 충분한 최소 이동 계산
        distance = [-1] * n  # 아직 도달하지 않은 위치
        queue = [start]  # FIFO 탐색 목록
        distance[start] = 0  # 출발점을 거리 0으로 발견
        head = 0  # 다음에 읽을 큐 인덱스
        while head < len(queue):  # 가까운 위치부터 확인
            u = queue[head]  # 현재 위치
            head += 1  # 읽는 위치 전진
            for v in range(n):  # 이어진 도로 후보
                if adj[u][v] and distance[v] == -1:  # 새로 도달하는 위치
                    distance[v] = distance[u] + 1  # 한 도로 더 이동한 거리
                    queue.append(v)  # 다음 탐색 대상 추가
        return distance[goal]  # 미도달이면 -1
    first = bfs_distance(0, checkpoint)  # 필수 지점까지의 최소 이동
    second = bfs_distance(checkpoint, target)  # 필수 지점 이후의 최소 이동
    print(-1 if first < 0 or second < 0 else first + second)  # 두 구간의 도달 여부를 먼저 확인

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

- 시간: O(V²+E)
- 보조 공간: O(V²)

인접 행렬 BFS를 두 번 실행하며 상수 2는 점근식에서 제외합니다. 두 최단 구간의 연결은 재방문 허용 조건에서 유효합니다.

[예제 입력](<예제_examples/42-문제해결순서와실무모델링_problem-solving-practice/input.txt>) · [예상 출력](<예제_examples/42-문제해결순서와실무모델링_problem-solving-practice/output.txt>) · [예제 실행 방법](<예제_examples/42-문제해결순서와실무모델링_problem-solving-practice/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

[유형별 연습문제](<연습문제_problem-index.md>)에서 문제를 고르고 상태·정당성·구현 비용을 함께 비교할 수 있습니다.

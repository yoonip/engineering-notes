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

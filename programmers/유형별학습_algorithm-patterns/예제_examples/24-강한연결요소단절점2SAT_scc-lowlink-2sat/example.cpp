#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int vertices, adj[8][8], seen[8], order[8], order_size, component[8];  // 최대 8개 리터럴 정점의 SCC 상태
static int literal_node(int literal) {  // 부호 있는 리터럴을 정점 번호로 변환
    return 2 * (abs(literal) - 1) + (literal < 0);  // 양수는 짝수, 부정은 바로 다음 홀수
}  // 리터럴 변환 함수 끝
static void dfs_order(int u) {  // 원래 그래프의 종료 순서 기록
    seen[u] = 1;  // 재귀로 다시 방문하지 않게 표시
    for (int v = 0; v < vertices; ++v) if (adj[u][v] && !seen[v]) dfs_order(v);  // 미방문 후속 리터럴부터 처리
    order[order_size++] = u;  // 자식 탐색을 마친 뒤 종료 순서에 추가
}  // 종료 순서 DFS 끝
static void dfs_component(int u, int label) {  // 역그래프의 연결 탐색으로 SCC 배정
    component[u] = label;  // 현재 SCC 번호 기록
    for (int v = 0; v < vertices; ++v) if (adj[v][u] && component[v] == -1) dfs_component(v, label);  // 반대 간선으로 같은 SCC 확장
}  // 역그래프 DFS 끝
int main(void) {  // 2-SAT 만족 가능성 판정
    int variables = read_int(), clauses = read_int();  // 변수 수와 OR 절 수
    vertices = 2 * variables;  // 각 변수의 참·거짓 리터럴 정점
    for (int i = 0; i < clauses; ++i) {  // 두 리터럴 절 입력
        int a = literal_node(read_int()), b = literal_node(read_int());  // 두 리터럴의 정점 번호
        adj[a ^ 1][b] = 1; adj[b ^ 1][a] = 1;  // 부정 a에서 b, 부정 b에서 a로 함의 추가
    }  // 함의 그래프 구성 끝
    for (int u = 0; u < vertices; ++u) if (!seen[u]) dfs_order(u);  // 모든 정점의 DFS 종료 순서
    for (int u = 0; u < vertices; ++u) component[u] = -1;  // 아직 SCC가 없는 정점 표시
    int count = 0;  // 다음 SCC 번호
    for (int i = order_size - 1; i >= 0; --i) {  // 종료 순서 역순으로 두 번째 탐색
        int u = order[i];  // 이번 역그래프 출발 후보
        if (component[u] == -1) dfs_component(u, count++);  // 아직 소속이 없는 SCC를 하나 분리
    }  // SCC 분해 끝
    for (int x = 0; x < variables; ++x) {  // 각 변수와 그 부정의 소속 비교
        if (component[2 * x] == component[2 * x + 1]) { write_text("UNSAT\n"); return 0; }  // 같은 SCC면 양쪽 함의가 모순
    }  // 모든 변수의 모순 검사 끝
    write_text("SAT\n"); return 0;  // 모순 없는 배정의 존재 표시
}  // SCC 기반 2-SAT 예제 끝

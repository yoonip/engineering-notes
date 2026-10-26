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


typedef struct { int u, v, weight; } Edge;  // 양끝과 비용을 묶은 간선 자료형
static int parent[8], sizes[8];  // DSU 대표 연결과 집합 크기
static int find_root(int node) {  // 경로를 줄이며 현재 대표 찾기
    while (parent[node] != node) {  // 자기 자신이 대표가 될 때까지 이동
        parent[node] = parent[parent[node]];  // 한 단계 위 조상으로 경로 압축
        node = parent[node];  // 짧아진 부모 방향으로 이동
    }  // 대표 탐색 끝
    return node;  // 집합을 식별하는 대표
}  // find 함수 끝
static int compare_edges(const void *first, const void *second) {  // qsort용 비용 비교
    const Edge *a = (const Edge *)first, *b = (const Edge *)second;  // 전달받은 원소를 간선으로 해석
    return (a->weight > b->weight) - (a->weight < b->weight);  // 뺄셈 오버플로 없이 비교 부호 반환
}  // 간선 비교 함수 끝
int main(void) {  // Kruskal 최소 신장 트리 계산
    int n = read_int(), m = read_int();  // 정점 수와 간선 수
    Edge edges[32];  // 입력 상한만큼 간선 보관
    for (int i = 0; i < m; ++i) {  // 간선 목록 입력
        edges[i].u = read_int(); edges[i].v = read_int(); edges[i].weight = read_int();  // 양끝과 비용 저장
    }  // 간선 입력 끝
    qsort(edges, m, sizeof(Edge), compare_edges);  // 작은 비용부터 간선 검사
    for (int i = 0; i < n; ++i) { parent[i] = i; sizes[i] = 1; }  // 정점마다 독립 집합 생성
    int selected = 0, total = 0;  // 선택 간선 수와 누적 비용
    for (int i = 0; i < m; ++i) {  // 정렬한 간선을 한 번씩 확인
        int a = find_root(edges[i].u), b = find_root(edges[i].v);  // 두 끝의 현재 소속
        if (a == b) continue;  // 사이클을 만드는 간선 제외
        if (sizes[a] < sizes[b]) { int swap = a; a = b; b = swap; }  // 작은 집합을 큰 집합에 붙이기
        parent[b] = a; sizes[a] += sizes[b];  // 두 연결 요소 병합
        total += edges[i].weight; ++selected;  // 선택한 간선 비용과 개수 반영
    }  // 간선 선택 끝
    if (selected == n - 1) { write_number(total); write_text("\n"); }  // 전체 연결이면 MST 비용
    else write_text("DISCONNECTED\n");  // 전체 신장 트리가 없는 상태
    return 0;  // 정상 종료
}  // Kruskal 예제 끝

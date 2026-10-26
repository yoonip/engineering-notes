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


static int n, adj[8][8], depth[8], subtree[8], up[4][8];  // 작은 트리와 2의 거듭제곱 조상 표
static void prepare(int u, int parent) {  // 깊이·부모·서브트리 크기 계산
    up[0][u] = parent; subtree[u] = 1;  // 직계 부모와 자기 자신 한 개
    for (int v = 0; v < n; ++v) {  // 트리의 이웃 후보 확인
        if (!adj[u][v] || v == parent) continue;  // 없는 간선과 부모로 돌아가는 간선 제외
        depth[v] = depth[u] + 1;  // 자식 깊이는 한 단계 아래
        prepare(v, u);  // 자식 결과부터 계산
        subtree[u] += subtree[v];  // 완성한 자식 크기를 부모에 합산
    }  // 현재 서브트리 집계 끝
}  // 초기 DFS 끝
static int lca(int u, int v) {  // 두 정점의 최소 공통 조상
    if (depth[u] < depth[v]) { int swap = u; u = v; v = swap; }  // 더 깊은 정점을 u로 통일
    int difference = depth[u] - depth[v];  // 먼저 맞출 깊이 차이
    for (int k = 0; k < 4; ++k) if ((difference >> k) & 1) u = up[k][u];  // 차이의 비트만큼 조상 이동
    if (u == v) return u;  // 같은 정점이나 조상 관계면 여기서 바로 반환
    for (int k = 3; k >= 0; --k) {  // 큰 점프부터 LCA 바로 아래까지 함께 이동
        if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }  // 공통 조상보다 아래인 점프만 허용
    }  // 두 정점의 부모가 같아진 상태
    return up[0][u];  // 한 단계 위의 LCA
}  // LCA 질의 함수 끝
int main(void) {  // 서브트리와 조상 질의 실행
    n = read_int(); int queries = read_int();  // 정점 수와 질의 수
    for (int i = 1; i < n; ++i) {  // 트리 간선 n-1개 입력
        int a = read_int(), b = read_int();  // 간선 양끝
        adj[a][b] = adj[b][a] = 1;  // 무방향 연결
    }  // 트리 입력 끝
    prepare(0, 0);  // 루트의 부모를 자신으로 두어 범위 밖 조상 방지
    for (int k = 1; k < 4; ++k) {  // 2의 거듭제곱 조상 표 채우기
        for (int u = 0; u < n; ++u) up[k][u] = up[k - 1][up[k - 1][u]];  // 두 번의 절반 점프로 조상 계산
    }  // 이진 리프팅 표 완성
    for (int u = 0; u < n; ++u) {  // 서브트리 크기 출력
        if (u) write_text(" ");  // 숫자 사이 공백
        write_number(subtree[u]);  // 자기 자신을 포함한 정점 수
    }  // 크기 배열 출력 끝
    write_text("\n");  // 크기 배열의 줄바꿈
    for (int i = 0; i < queries; ++i) {  // 입력 순서대로 LCA 질의
        int u = read_int(), v = read_int();  // 이번 두 정점
        write_number(lca(u, v)); write_text("\n");  // LCA 하나를 한 줄에 출력
    }  // 모든 질의 출력 끝
    return 0;  // 정상 종료
}  // 트리 예제 끝

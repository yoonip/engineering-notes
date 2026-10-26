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


int main(void) {  // 정점 최소 스캔 방식의 Dijkstra
    int n = read_int(), m = read_int(), start = read_int();  // 그래프 크기와 출발점
    int weight[8][8], distance[8], used[8] = {0};  // 최소 간선·거리·확정 여부
    const int inf = 1000000000;  // 최대 단순 경로 비용보다 큰 미도달 값
    for (int i = 0; i < n; ++i) {  // 모든 정점과 간선 후보 초기화
        distance[i] = inf;  // 출발점을 제외한 미도달 상태
        for (int j = 0; j < n; ++j) weight[i][j] = inf;  // 아직 없는 방향 간선
    }  // 초기화 끝
    for (int i = 0; i < m; ++i) {  // 비음수 방향 간선 입력
        int a = read_int(), b = read_int(), cost = read_int();  // 간선의 출발·도착·비용
        if (cost < weight[a][b]) weight[a][b] = cost;  // 평행 간선의 최소 비용 유지
    }  // 간선 입력 끝
    distance[start] = 0;  // 출발 비용은 0
    for (int step = 0; step < n; ++step) {  // 최대 n개 정점을 확정
        int u = -1;  // 이번에 고를 미확정 정점
        for (int v = 0; v < n; ++v) {  // 현재 거리가 가장 작은 후보 찾기
            if (!used[v] && (u == -1 || distance[v] < distance[u])) u = v;  // 최소 거리 후보 갱신
        }  // 최소 후보 선택 끝
        if (u == -1 || distance[u] == inf) break;  // 남은 정점이 전부 미도달이면 종료
        used[u] = 1;  // 비음수 조건으로 현재 최단 거리 확정
        for (int v = 0; v < n; ++v) {  // u를 지나가는 방향 간선 완화
            if (weight[u][v] != inf && distance[u] + weight[u][v] < distance[v]) {  // 실제 간선의 더 짧은 경로
                distance[v] = distance[u] + weight[u][v];  // 새 최단 거리 저장
            }  // 현재 간선 완화 끝
        }  // u의 이웃 갱신 끝
    }  // 모든 도달 거리 계산 끝
    for (int i = 0; i < n; ++i) {  // 번호순 결과 출력
        if (i) write_text(" ");  // 숫자 사이 공백
        write_number(distance[i] == inf ? -1 : distance[i]);  // 미도달만 -1로 변환
    }  // 결과 배열 출력 끝
    write_text("\n"); return 0;  // 줄바꿈 후 정상 종료
}  // Dijkstra 예제 끝

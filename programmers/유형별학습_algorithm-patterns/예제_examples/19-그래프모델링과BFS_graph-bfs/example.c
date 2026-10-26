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


int main(void) {  // 작은 그래프의 BFS 거리 계산
    int n = read_int(), m = read_int(), start = read_int();  // 정점 수·간선 수·출발점
    int adj[8][8] = {0}, distance[8], queue[8];  // 연결 여부·거리·FIFO 저장 공간
    for (int i = 0; i < m; ++i) {  // 무방향 간선 입력
        int a = read_int(), b = read_int();  // 간선의 양끝
        adj[a][b] = adj[b][a] = 1;  // 양방향 이동 표시
    }  // 그래프 입력 끝
    for (int i = 0; i < n; ++i) distance[i] = -1;  // 미발견 정점의 거리
    int head = 0, tail = 0;  // 큐의 읽을 위치와 다음 저장 위치
    queue[tail++] = start; distance[start] = 0;  // 넣는 순간 출발점 발견
    while (head < tail) {  // 먼저 발견한 정점부터 처리
        int u = queue[head++];  // FIFO 순서의 다음 정점
        for (int v = 0; v < n; ++v) {  // 현재 행의 이웃 후보 순회
            if (adj[u][v] && distance[v] == -1) {  // 연결된 미발견 이웃만 선택
                distance[v] = distance[u] + 1;  // 한 간선 더 이동한 거리
                queue[tail++] = v;  // 다음 층 후보를 큐 뒤에 추가
            }  // 새 이웃의 발견 처리 끝
        }  // 현재 정점 이웃 확인 끝
    }  // 도달 가능한 정점 탐색 끝
    for (int i = 0; i < n; ++i) {  // 정점 번호순 출력
        if (i) write_text(" ");  // 숫자 사이의 공백
        write_number(distance[i]);  // 미도달 -1도 그대로 출력
    }  // 거리 배열 출력 끝
    write_text("\n");  // 결과 줄 마침
    return 0;  // 정상 종료
}  // BFS 예제 끝

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


int main(void) {  // Kahn 순서와 완료 시각 DP
    int n = read_int(), m = read_int();  // 작업 수와 선행 관계 수
    int duration[8], finish[8], degree[8] = {0}, adj[8][8] = {0}, queue[8];  // 시간·진입 차수·연결·큐
    for (int i = 0; i < n; ++i) { duration[i] = read_int(); finish[i] = duration[i]; }  // 선행 작업 없는 기본 완료 시각
    for (int i = 0; i < m; ++i) {  // 선행 관계 입력
        int u = read_int(), v = read_int();  // u 완료 후 v 시작
        if (!adj[u][v]) { adj[u][v] = 1; ++degree[v]; }  // 중복을 한 번만 진입 차수에 반영
    }  // 선행 관계 입력 끝
    int head = 0, tail = 0, processed = 0;  // 큐 위치와 처리한 작업 수
    for (int u = 0; u < n; ++u) if (!degree[u]) queue[tail++] = u;  // 바로 시작할 수 있는 작업 등록
    while (head < tail) {  // 준비된 작업을 차례로 완료 처리
        int u = queue[head++]; ++processed;  // 선행 조건이 모두 끝난 작업
        for (int v = 0; v < n; ++v) {  // 이 작업을 기다리는 후속 작업
            if (!adj[u][v]) continue;  // 실제 선행 관계만 처리
            if (finish[u] + duration[v] > finish[v]) finish[v] = finish[u] + duration[v];  // 가장 늦은 선행 완료 시각 반영
            if (--degree[v] == 0) queue[tail++] = v;  // 모든 선행 작업이 끝나면 큐에 추가
        }  // 후속 작업 갱신 끝
    }  // 가능한 작업 처리 끝
    if (processed != n) { write_text("CYCLE\n"); return 0; }  // 남은 작업은 순환 의존의 영향
    for (int i = 0; i < n; ++i) {  // 작업 번호순 완료 시각 출력
        if (i) write_text(" ");  // 출력 숫자 사이 공백
        write_number(finish[i]);  // 현재 작업의 최소 완료 시각
    }  // 완료 시각 배열 출력 끝
    write_text("\n"); return 0;  // 결과 줄을 마치고 종료
}  // 위상 DP 예제 끝

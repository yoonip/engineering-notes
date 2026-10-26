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


int main(void) {  // DFS로 연결 요소 번호 계산
    int n = read_int(), m = read_int();  // 그래프의 정점 수와 간선 수
    int adj[8][8] = {0}, label[8], stack[8];  // 인접 행렬·소속·탐색 스택
    for (int i = 0; i < m; ++i) {  // 간선 입력
        int a = read_int(), b = read_int();  // 간선 양끝
        adj[a][b] = adj[b][a] = 1;  // 두 방향의 연결 저장
    }  // 간선 입력 끝
    for (int i = 0; i < n; ++i) label[i] = -1;  // 아직 소속이 없는 정점 표시
    int count = 0;  // 지금까지 발견한 연결 요소 수
    for (int start = 0; start < n; ++start) {  // 고립 정점까지 새 출발 후보 확인
        if (label[start] != -1) continue;  // 이미 끝낸 요소는 다시 탐색하지 않기
        int top = 0; stack[top++] = start; label[start] = count;  // 새 요소의 시작점 등록
        while (top) {  // 현재 요소의 미처리 정점이 남으면 반복
            int u = stack[--top];  // 마지막에 넣은 정점부터 확인
            for (int v = 0; v < n; ++v) {  // 연결된 이웃 후보 확인
                if (adj[u][v] && label[v] == -1) {  // 새로 발견한 이웃만 스택에 넣기
                    label[v] = count; stack[top++] = v;  // 중복 삽입 전에 소속 확정
                }  // 새 이웃 등록 끝
            }  // 현재 정점의 이웃 확인 끝
        }  // 한 연결 요소 탐색 끝
        ++count;  // 다음 요소에 사용할 번호
    }  // 모든 연결 요소 탐색 끝
    write_number(count); write_text("\n");  // 요소 수 출력
    for (int i = 0; i < n; ++i) {  // 번호순 소속 출력
        if (i) write_text(" ");  // 소속 번호 사이 공백
        write_number(label[i]);  // 현재 정점의 요소 번호
    }  // 소속 배열 출력 끝
    write_text("\n"); return 0;  // 결과 줄을 끝내고 종료
}  // 연결 요소 예제 끝

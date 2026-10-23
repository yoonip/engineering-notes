#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

long long solution(int n, int m, int x, int y, int** queries, size_t queries_rows, size_t queries_cols) {
    (void)queries_cols;
    long long low[2] = {y,x}, high[2] = {y,x}, length[2] = {m,n};
    for (size_t i = queries_rows; i-- > 0;) {
        int command = queries[i][0], axis = command / 2; long long distance = queries[i][1];
        if (command % 2 == 0) { if (low[axis]) low[axis] += distance; high[axis] += distance; if (high[axis] >= length[axis]) high[axis] = length[axis] - 1; }
        else { if (high[axis] != length[axis] - 1) high[axis] -= distance; low[axis] -= distance; if (low[axis] < 0) low[axis] = 0; }
        if (low[axis] > high[axis]) return 0;
    }
    return (high[0] - low[0] + 1) * (high[1] - low[1] + 1);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// long long solution(int n, int m, int x, int y, int** queries, size_t queries_rows, size_t queries_cols) {  // 10억×10억 격자를 직접 돌리지 않고 목표 한 점에서 명령을 역순으로 적용해 가능한 시작 구간을 확장·이동하기
//     (void)queries_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     long long low[2] = {y,x}, high[2] = {y,x}, length[2] = {m,n};  // 역추적 가능한 열과 행의 최솟값 / 역추적 가능한 열과 행의 최댓값 / 열과 행의 격자 길이 저장
//     for (size_t i = queries_rows; i-- > 0;) {  // 뒤에서 읽을 이동 명령 순서대로 확인
//         int command = queries[i][0], axis = command / 2; long long distance = queries[i][1];  // 되돌릴 이동 방향 / 가로 또는 세로 범위 / 되돌릴 이동 거리 저장
//         if (command % 2 == 0) { if (low[axis]) low[axis] += distance; high[axis] += distance; if (high[axis] >= length[axis]) high[axis] = length[axis] - 1; }  // 왼쪽·위 이동을 역산해서 가능한 시작 구간을 늘리되 격자 끝에 맞추기
//         else { if (high[axis] != length[axis] - 1) high[axis] -= distance; low[axis] -= distance; if (low[axis] < 0) low[axis] = 0; }  // 앞 조건이 아니면 역추적 가능한 열과 행의 최댓값 / 가로 또는 세로 범위 / 열과 행의 격자 길이에서 이번 사용량 빼기
//         if (low[axis] > high[axis]) return 0;  // 가능한 좌표 구간이 비었으면 시작점은 0개
//     }  // 이 범위 끝
//     return (high[0] - low[0] + 1) * (high[1] - low[1] + 1);  // 역추적 가능한 열과 행의 최댓값 / 역추적 가능한 열과 행의 최솟값로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 10억×10억 격자를 직접 돌리지 않고 목표 한 점에서 명령을 역순으로 적용해 가능한 시작 구간을 확장·이동하기
// 벽에 막혀 같은 좌표에 모일 수 있으므로 후보 구간이 0 또는 마지막 경계를 포함할 때 해당 끝을 그대로 두기; 빈 구간이면 0; 시간 O(Q), 추가 공간 O(1)
// 예: 마지막 열이 0이고 직전에 왼쪽으로 3칸 이동했다면 이전 열은 0~3 모두 가능하므로 역산 구간이 넓어짐

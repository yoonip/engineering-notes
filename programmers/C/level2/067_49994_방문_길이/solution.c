#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(const char* dirs) {
    bool edges[121][121] = {{false}};
    int x = 5, y = 5, answer = 0;
    for (size_t i = 0; dirs[i]; ++i) {
        int nx = x, ny = y;
        if (dirs[i] == 'U') ++ny;
        else if (dirs[i] == 'D') --ny;
        else if (dirs[i] == 'R') ++nx;
        else --nx;
        if (nx < 0 || nx > 10 || ny < 0 || ny > 10) continue;
        int a = y * 11 + x, b = ny * 11 + nx;
        if (!edges[a][b]) { ++answer; edges[a][b] = edges[b][a] = true; }
        x = nx; y = ny;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// int solution(const char* dirs) {  // 두 칸 사이의 길을 양방향 bool 표에 함께 기록; 같은 길을 반대로 걸어도 처음 한 번만 세기
//     bool edges[121][121] = {{false}};  // 이미 지난 두 칸 사이의 길 저장
//     int x = 5, y = 5, answer = 0;  // 현재 가로 위치 / 현재 세로 위치 / 처음 지나간 길 수 저장
//     for (size_t i = 0; dirs[i]; ++i) {  // 이동 명령 위치 순서대로 확인
//         int nx = x, ny = y;  // 다음 가로 위치 / 다음 세로 위치 저장
//         if (dirs[i] == 'U') ++ny;  // U 명령이면 세로 좌표를 한 칸 올리기
//         else if (dirs[i] == 'D') --ny;  // D 명령이면 세로 좌표를 한 칸 내리기
//         else if (dirs[i] == 'R') ++nx;  // R 명령이면 가로 좌표를 한 칸 오른쪽으로 이동
//         else --nx;  // 앞 조건이 아니면 다음 가로 위치 갱신
//         if (nx < 0 || nx > 10 || ny < 0 || ny > 10) continue;  // 격자 밖이거나 막혔거나 이미 처리한 칸이면 다음 후보로 넘어가기
//         int a = y * 11 + x, b = ny * 11 + nx;  // 현재 칸의 일차원 번호 / 다음 칸의 일차원 번호 저장
//         if (!edges[a][b]) { ++answer; edges[a][b] = edges[b][a] = true; }  // 처음 지나는 길일 때만 세고 양방향을 함께 방문 표시
//         x = nx; y = ny;  // 현재 가로 위치 / 현재 세로 위치 갱신
//     }  // 이 범위 끝
//     return answer;  // 처음 지나간 길 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 칸 사이의 길을 양방향 bool 표에 함께 기록; 같은 길을 반대로 걸어도 처음 한 번만 세기
// 예: 'ULURRDLLU'의 9번 이동 중 새 길은 7개.; 명령 N개에 시간 O(N), 길 집합은 고정 격자 안에서 최대 220개

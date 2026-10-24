#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int* solution(int n) {
    int* answer = calloc((size_t)n * (n + 1) / 2, sizeof(*answer));
    const int dr[3] = {1,0,-1}, dc[3] = {0,1,-1};
    int r = -1, c = 0, value = 1;
    for (int side = 0; side < n; ++side)
        for (int step = 0; step < n - side; ++step) {
            r += dr[side % 3]; c += dc[side % 3];
            answer[r * (r + 1) / 2 + c] = value++;
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
// int* solution(int n) {  // 아래→오른쪽→왼쪽 위 순서로 이동하며, 채울 길이를 n,n-1,...,1로 줄이기; 마지막에 행 순서로 펼치기
//     int* answer = calloc((size_t)n * (n + 1) / 2, sizeof(*answer));  // 행 순서로 펼친 삼각형 공간 확보하고 0으로 시작
//     const int dr[3] = {1,0,-1}, dc[3] = {0,1,-1};  // 방향별 행 변화 / 방향별 열 변화 저장
//     int r = -1, c = 0, value = 1;  // 채우는 행 / 채우는 열 / 다음에 쓸 숫자 저장
//     for (int side = 0; side < n; ++side)  // 달팽이 방향과 남은 변 길이 순서대로 확인
//         for (int step = 0; step < n - side; ++step) {  // 현재 변에서 이동한 칸 수 순서대로 확인
//             r += dr[side % 3]; c += dc[side % 3];  // 채우는 행 / 방향별 행 변화 / 달팽이 방향과 남은 변 길이 더해 누적
//             answer[r * (r + 1) / 2 + c] = value++;  // 행 순서로 펼친 삼각형 갱신
//         }  // 이 범위 끝
//     return answer;  // 행 순서로 펼친 삼각형 반환
// }  // 이 범위 끝

// 풀이 요약
// 아래→오른쪽→왼쪽 위 순서로 이동하며, 채울 길이를 n,n-1,...,1로 줄이기; 마지막에 행 순서로 펼치기
// 예: n=4는 [1,2,9,3,10,8,4,5,6,7]; 시간·공간 O(n²)

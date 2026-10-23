#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int** dots, size_t dots_rows, size_t dots_cols) {
    (void)dots_cols;
    int min_x = dots[0][0], max_x = min_x, min_y = dots[0][1], max_y = min_y;
    for (size_t i = 1; i < dots_rows; ++i) {
        if (dots[i][0] < min_x) min_x = dots[i][0];
        if (dots[i][0] > max_x) max_x = dots[i][0];
        if (dots[i][1] < min_y) min_y = dots[i][1];
        if (dots[i][1] > max_y) max_y = dots[i][1];
    }
    return (max_x - min_x) * (max_y - min_y);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int** dots, size_t dots_rows, size_t dots_cols) {  // 직사각형 넓이 구하기 풀이 시작
//     (void)dots_cols;  // 각 행에 x와 y가 있다는 조건을 사용하므로 열 수 dots_cols는 계산에 쓰지 않으며, void 변환으로 이를 표시
//     int min_x = dots[0][0], max_x = min_x, min_y = dots[0][1], max_y = min_y;  // 첫 꼭짓점의 x와 y를 각각 min_x·max_x와 min_y·max_y의 초기 경곗값으로 저장
//     for (size_t i = 1; i < dots_rows; ++i) {  // 첫 꼭짓점은 이미 반영했으므로 size_t 인덱스 i를 1부터 늘려 나머지 꼭짓점을 확인
//         if (dots[i][0] < min_x) min_x = dots[i][0];  // 현재 꼭짓점의 x가 min_x보다 작으면 왼쪽 경계 min_x를 이 x로 바꾸기
//         if (dots[i][0] > max_x) max_x = dots[i][0];  // 현재 꼭짓점의 x가 max_x보다 크면 오른쪽 경계 max_x를 이 x로 바꾸기
//         if (dots[i][1] < min_y) min_y = dots[i][1];  // 현재 꼭짓점의 y가 min_y보다 작으면 아래쪽 경계 min_y를 이 y로 바꾸기
//         if (dots[i][1] > max_y) max_y = dots[i][1];  // 현재 꼭짓점의 y가 max_y보다 크면 위쪽 경계 max_y를 이 y로 바꾸기
//     }  // 블록 끝
//     return (max_x - min_x) * (max_y - min_y);  // 가로 길이 max_x - min_x와 세로 길이 max_y - min_y를 곱해 넓이를 반환
// }  // 블록 끝

// 풀이 요약
// 모든 꼭짓점에서 x와 y의 최솟값·최댓값을 찾기. x 좌표 차이를 가로 길이로, y 좌표 차이를 세로 길이로 사용하여 곱하기

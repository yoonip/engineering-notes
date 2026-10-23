#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

typedef struct { long long x, y; } Point;
char** solution(int** line, size_t line_rows, size_t line_cols) {
    (void)line_cols;
    Point* points = malloc(line_rows * line_rows * sizeof(*points));
    size_t count = 0; long long min_x = LLONG_MAX, min_y = LLONG_MAX, max_x = LLONG_MIN, max_y = LLONG_MIN;
    for (size_t i = 0; i < line_rows; ++i) for (size_t j = i + 1; j < line_rows; ++j) {
        long long a = line[i][0], b = line[i][1], e = line[i][2], c = line[j][0], d = line[j][1], f = line[j][2];
        long long denominator = a * d - b * c, nx = b * f - e * d, ny = e * c - a * f;
        if (!denominator || nx % denominator || ny % denominator) continue;
        long long x = nx / denominator, y = ny / denominator;
        points[count++] = (Point){x,y};
        if (x < min_x) min_x = x; if (x > max_x) max_x = x;
        if (y < min_y) min_y = y; if (y > max_y) max_y = y;
    }
    size_t rows = (size_t)(max_y - min_y + 1), cols = (size_t)(max_x - min_x + 1);
    char** answer = malloc(rows * sizeof(*answer));
    for (size_t i = 0; i < rows; ++i) { answer[i] = malloc(cols + 1); memset(answer[i], '.', cols); answer[i][cols] = '\0'; }
    for (size_t i = 0; i < count; ++i) answer[max_y - points[i].y][points[i].x - min_x] = '*';
    free(points);
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
// typedef struct { long long x, y; } Point;  // 정수 교점 x / 정수 교점 y를 한 상태로 묶기
// char** solution(int** line, size_t line_rows, size_t line_cols) {  // 두 직선의 교점을 정수 나눗셈으로 판정해 모으고, 모든 점의 최소 사각형에 별을 찍기; 화면의 행 방향은 y축과 반대
//     (void)line_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     Point* points = malloc(line_rows * line_rows * sizeof(*points));  // 정수 좌표 교점 목록 공간 확보
//     size_t count = 0; long long min_x = LLONG_MAX, min_y = LLONG_MAX, max_x = LLONG_MIN, max_y = LLONG_MIN;  // 모은 정수 교점 수 / 교점의 최소 x / 교점의 최소 y / 교점의 최대 x / 교점의 최대 y 저장
//     for (size_t i = 0; i < line_rows; ++i) for (size_t j = i + 1; j < line_rows; ++j) {  // 첫 직선 또는 교점 위치 순서대로 확인; 두 번째 직선 위치 갱신
//         long long a = line[i][0], b = line[i][1], e = line[i][2], c = line[j][0], d = line[j][1], f = line[j][2];  // 첫 직선 또는 교점 위치 / 두 번째 직선 위치 확인
//         long long denominator = a * d - b * c, nx = b * f - e * d, ny = e * c - a * f;  // 두 직선 교점 식의 공통 분모 / x좌표의 분자 / y좌표의 분자 저장
//         if (!denominator || nx % denominator || ny % denominator) continue;  // 평행한 두 직선이나 정수가 아닌 교점은 제외
//         long long x = nx / denominator, y = ny / denominator;  // 정수 교점 x / 정수 교점 y 저장
//         points[count++] = (Point){x,y};  // 정수 좌표 교점 목록 갱신
//         if (x < min_x) min_x = x; if (x > max_x) max_x = x;  // 정수 교점의 가로 최솟값과 최댓값 갱신
//         if (y < min_y) min_y = y; if (y > max_y) max_y = y;  // 정수 교점의 세로 최솟값과 최댓값 갱신
//     }  // 이 범위 끝
//     size_t rows = (size_t)(max_y - min_y + 1), cols = (size_t)(max_x - min_x + 1);  // 별 지도 행 수 / 별 지도 열 수 저장
//     char** answer = malloc(rows * sizeof(*answer));  // 교점을 별로 찍은 문자열 지도 공간 확보
//     for (size_t i = 0; i < rows; ++i) { answer[i] = malloc(cols + 1); memset(answer[i], '.', cols); answer[i][cols] = '\0'; }  // 첫 직선 또는 교점 위치 순서대로 확인; 교점을 별로 찍은 문자열 지도 공간 확보
//     for (size_t i = 0; i < count; ++i) answer[max_y - points[i].y][points[i].x - min_x] = '*';  // 첫 직선 또는 교점 위치 순서대로 확인; 교점을 별로 찍은 문자열 지도 / 교점의 최대 y / 정수 좌표 교점 목록 / 첫 직선 또는 교점 위치 확인
//     free(points);  // 정수 좌표 교점 목록 임시 공간 정리
//     return answer;  // 교점을 별로 찍은 문자열 지도 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 직선의 교점을 정수 나눗셈으로 판정해 모으고, 모든 점의 최소 사각형에 별을 찍기; 화면의 행 방향은 y축과 반대
// 예: y=1의 교점 x=-1,1이면 '*.*'.; 직선 N개·출력 넓이 A일 때 시간 O(N²+A), 공간 O(교점 수+A)

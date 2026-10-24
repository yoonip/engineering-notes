#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int* solution(int n, long long left, long long right) {
    int* answer = malloc((size_t)(right - left + 1) * sizeof(*answer));
    for (long long index = left; index <= right; ++index) {
        long long row = index / n, col = index % n;
        answer[index - left] = (int)(row > col ? row : col) + 1;
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
// int* solution(int n, long long left, long long right) {  // 0부터인 (행,열)의 값은 max(행,열)+1; 전체 n² 배열을 만들지 않고 필요한 인덱스만 행·열로 바꾸기
//     int* answer = malloc((size_t)(right - left + 1) * sizeof(*answer));  // 요청한 일차원 구간의 값 공간 확보
//     for (long long index = left; index <= right; ++index) {  // 전체 배열을 펼친 위치 순서대로 확인
//         long long row = index / n, col = index % n;  // 원래 배열의 행 / 원래 배열의 열 저장
//         answer[index - left] = (int)(row > col ? row : col) + 1;  // 요청한 일차원 구간의 값 갱신
//     }  // 이 범위 끝
//     return answer;  // 요청한 일차원 구간의 값 반환
// }  // 이 범위 끝

// 풀이 요약
// 0부터인 (행,열)의 값은 max(행,열)+1; 전체 n² 배열을 만들지 않고 필요한 인덱스만 행·열로 바꾸기
// 예: n=3의 인덱스 2~5는 [3,2,2,3]; 구간 길이 L일 때 시간·결과 공간 O(L)

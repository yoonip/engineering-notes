#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int sides[], size_t sides_len) {
    (void)sides_len;
    int shorter = sides[0] < sides[1] ? sides[0] : sides[1];
    return 2 * shorter - 1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int sides[], size_t sides_len) {  // 삼각형의 완성조건 (2) 풀이 시작
//     (void)sides_len;  // 배열 크기처럼 함수 형식에 포함되지만 본문에서 사용하지 않는 매개변수임을 표시
//     int shorter = sides[0] < sides[1] ? sides[0] : sides[1];  // 주어진 두 변 중 짧은 쪽. 가능한 나머지 변의 범위를 정할 기준
//     return 2 * shorter - 1;  // 가능한 세 번째 변의 정수 개수인 2 × 짧은 변 - 1 반환
// }  // 블록 끝
// 풀이 요약
// 세 번째 변은 두 변의 차보다 크고 합보다 작은 정수. 양 끝을 제외한 정수 개수는 2 × 짧은 변 - 1.

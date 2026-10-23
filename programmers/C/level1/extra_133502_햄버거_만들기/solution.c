#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int ingredient[], size_t ingredient_len) {
    int* stack = malloc(ingredient_len * sizeof(int)); size_t length = 0; int answer = 0;
    for (size_t i = 0; i < ingredient_len; ++i) {
        stack[length++] = ingredient[i];
        if (length >= 4 && stack[length - 4] == 1 && stack[length - 3] == 2 && stack[length - 2] == 3 && stack[length - 1] == 1) { length -= 4; ++answer; }
    }
    free(stack);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int solution(int ingredient[], size_t ingredient_len) {  // 재료를 스택에 쌓기; 끝의 네 재료가 1·2·3·1이면 제거하고 완성한 햄버거 수를 늘리기
//     int* stack = malloc(ingredient_len * sizeof(int)); size_t length = 0; int answer = 0;  // 아직 햄버거로 빼지 않은 재료 / 쌓인 재료 수 / 완성해서 뺀 햄버거 수 공간 확보
//     for (size_t i = 0; i < ingredient_len; ++i) {  // 다음 재료 위치 순서대로 확인
//         stack[length++] = ingredient[i];  // 아직 햄버거로 빼지 않은 재료 갱신
//         if (length >= 4 && stack[length - 4] == 1 && stack[length - 3] == 2 && stack[length - 2] == 3 && stack[length - 1] == 1) { length -= 4; ++answer; }  // 스택 끝이 빵·야채·고기·빵이면 네 재료를 빼고 햄버거 수 늘리기
//     }  // 이 범위 끝
//     free(stack);  // 아직 햄버거로 빼지 않은 재료 임시 공간 정리
//     return answer;  // 완성해서 뺀 햄버거 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 재료를 스택에 쌓기; 끝의 네 재료가 1·2·3·1이면 제거하고 완성한 햄버거 수를 늘리기

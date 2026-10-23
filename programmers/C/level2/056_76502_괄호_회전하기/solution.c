#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(const char* s) {
    size_t len = strlen(s); char* stack = malloc(len);
    int answer = 0;
    for (size_t offset = 0; offset < len; ++offset) {
        size_t top = 0; bool valid = true;
        for (size_t j = 0; j < len; ++j) {
            char c = s[(offset + j) % len];
            if (c == '(' || c == '[' || c == '{') stack[top++] = c;
            else {
                char expected = c == ')' ? '(' : c == ']' ? '[' : '{';
                if (!top || stack[--top] != expected) { valid = false; break; }
            }
        }
        answer += valid && top == 0;
    }
    free(stack);
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
// int solution(const char* s) {  // 각 회전을 스택으로 확인; 닫는 괄호는 가장 최근 여는 괄호와 종류가 맞아야 하며 끝에 스택이 비어야 하기
//     size_t len = strlen(s); char* stack = malloc(len);  // 괄호 문자열 길이 / 아직 닫히지 않은 괄호 공간 확보
//     int answer = 0;  // 올바른 회전 수 저장
//     for (size_t offset = 0; offset < len; ++offset) {  // 회전 시작 위치 순서대로 확인
//         size_t top = 0; bool valid = true;  // 미완성 열린 괄호 수 / 현재 회전의 유효 여부 저장
//         for (size_t j = 0; j < len; ++j) {  // 회전 후 읽을 위치 순서대로 확인
//             char c = s[(offset + j) % len];  // 현재 괄호 저장
//             if (c == '(' || c == '[' || c == '{') stack[top++] = c;  // 여는 괄호는 아직 닫히지 않은 괄호 스택에 추가
//             else {  // 닫는 괄호이면 스택 위 열린 괄호와 짝 검사
//                 char expected = c == ')' ? '(' : c == ']' ? '[' : '{';  // 닫힌 괄호와 짝이 되는 열린 괄호 저장
//                 if (!top || stack[--top] != expected) { valid = false; break; }  // 열린 괄호가 없거나 짝이 다르면 현재 회전은 실패
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         answer += valid && top == 0;  // 올바른 회전 수 / 현재 회전의 유효 여부 / 미완성 열린 괄호 수 더해 누적
//     }  // 이 범위 끝
//     free(stack);  // 아직 닫히지 않은 괄호 임시 공간 정리
//     return answer;  // 올바른 회전 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 회전을 스택으로 확인; 닫는 괄호는 가장 최근 여는 괄호와 종류가 맞아야 하며 끝에 스택이 비어야 하기
// 예: '[](){}'는 0·2·4칸 회전이 유효해 3.; 길이 N일 때 시간 O(N²), 공간 O(N)

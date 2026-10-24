#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

char** solution(const char* s[], size_t s_len) {
    char** answer = malloc(s_len * sizeof(*answer));
    for (size_t i = 0; i < s_len; ++i) {
        size_t len = strlen(s[i]), top = 0, count = 0; char* stack = malloc(len + 1);
        for (size_t j = 0; j < len; ++j) {
            stack[top++] = s[i][j];
            if (top >= 3 && stack[top - 3] == '1' && stack[top - 2] == '1' && stack[top - 1] == '0') { top -= 3; ++count; }
        }
        size_t position = top; while (position && stack[position - 1] != '0') --position;
        answer[i] = malloc(len + 1); memcpy(answer[i], stack, position);
        for (size_t j = 0; j < count; ++j) memcpy(answer[i] + position + 3 * j, "110", 3);
        memcpy(answer[i] + position + 3 * count, stack + position, top - position); answer[i][len] = '\0'; free(stack);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// char** solution(const char* s[], size_t s_len) {  // 스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤, 즉 끝에 연속한 1들 앞에 몰아넣기
//     char** answer = malloc(s_len * sizeof(*answer));  // 110을 옮긴 문자열 목록 공간 확보
//     for (size_t i = 0; i < s_len; ++i) {  // 문자열 번호 순서대로 확인
//         size_t len = strlen(s[i]), top = 0, count = 0; char* stack = malloc(len + 1);  // 현재 문자열 길이 / 110을 빼고 남은 글자 수 / 꺼낸 110 묶음 수 / 110을 제거하는 문자 스택 공간 확보
//         for (size_t j = 0; j < len; ++j) {  // 현재 문자 또는 110 묶음 위치 순서대로 확인
//             stack[top++] = s[i][j];  // 110을 제거하는 문자 스택 갱신
//             if (top >= 3 && stack[top - 3] == '1' && stack[top - 2] == '1' && stack[top - 1] == '0') { top -= 3; ++count; }  // 스택 끝의 110을 제거해 따로 세기
//         }  // 이 범위 끝
//         size_t position = top; while (position && stack[position - 1] != '0') --position;  // 마지막 0 바로 뒤의 삽입 위치 저장
//         answer[i] = malloc(len + 1); memcpy(answer[i], stack, position);  // 110을 옮긴 문자열 목록 공간 확보
//         for (size_t j = 0; j < count; ++j) memcpy(answer[i] + position + 3 * j, "110", 3);  // 현재 문자 또는 110 묶음 위치 순서대로 확인; 110을 옮긴 문자열 목록 / 문자열 번호 / 마지막 0 바로 뒤의 삽입 위치 복사
//         memcpy(answer[i] + position + 3 * count, stack + position, top - position); answer[i][len] = '\0'; free(stack);  // 110을 옮긴 문자열 목록 복사
//     }  // 이 범위 끝
//     return answer;  // 110을 옮긴 문자열 목록 반환
// }  // 이 범위 끝

// 풀이 요약
// 스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤, 즉 끝에 연속한 1들 앞에 몰아넣기
// 예: 1110에서 110을 빼면 1; 남은 0이 없으므로 맨 앞에 110을 넣어 1101이 됨
// 남은 0은 앞에 유지하고 110은 끝의 1보다 앞에 둬야 사전순으로 작아진다; 시간·공간 O(전체 글자 수)

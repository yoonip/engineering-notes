#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

typedef struct { int start, duration; const char* name; } Task;
static int compare(const void* p, const void* q) { return ((const Task*)p)->start - ((const Task*)q)->start; }
static char* copy_name(const char* name) { char* result = malloc(strlen(name) + 1); strcpy(result, name); return result; }
char** solution(const char*** plans, size_t plans_rows, size_t plans_cols) {
    (void)plans_cols;
    Task* tasks = malloc(plans_rows * sizeof(*tasks)); Task* stack = malloc(plans_rows * sizeof(*stack)); char** answer = malloc(plans_rows * sizeof(*answer));
    for (size_t i = 0; i < plans_rows; ++i) {
        int hour, minute; sscanf(plans[i][1], "%d:%d", &hour, &minute);
        tasks[i] = (Task){hour * 60 + minute,atoi(plans[i][2]),plans[i][0]};
    }
    qsort(tasks, plans_rows, sizeof(*tasks), compare); size_t top = 0, count = 0; int previous = 0;
    for (size_t i = 0; i < plans_rows; ++i) {
        int available = tasks[i].start - previous;
        while (available > 0 && top) {
            Task* old = &stack[top - 1];
            if (old->duration <= available) { available -= old->duration; answer[count++] = copy_name(old->name); --top; }
            else { old->duration -= available; available = 0; }
        }
        stack[top++] = tasks[i]; previous = tasks[i].start;
    }
    while (top) answer[count++] = copy_name(stack[--top].name);
    free(tasks); free(stack);
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
// typedef struct { int start, duration; const char* name; } Task;  // 과제의 시작 시각·남은 시간·이름을 한 항목으로 묶기
// static int compare(const void* p, const void* q) { return ((const Task*)p)->start - ((const Task*)q)->start; }  // 시작 시각이 빠른 과제부터 정렬
// static char* copy_name(const char* name) { char* result = malloc(strlen(name) + 1); strcpy(result, name); return result; }  // 과제 이름 사본 계산용 함수
// char** solution(const char*** plans, size_t plans_rows, size_t plans_cols) {  // 시작 시각 순으로 정렬하고, 다음 시작까지의 시간에 스택 위 과제를 처리; 새 과제는 스택 위에 올리기
//     (void)plans_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     Task* tasks = malloc(plans_rows * sizeof(*tasks)); Task* stack = malloc(plans_rows * sizeof(*stack)); char** answer = malloc(plans_rows * sizeof(*answer));  // 시작 시각순 과제 / 중단된 과제의 LIFO 목록 / 끝낸 순서의 과제 이름 공간 확보
//     for (size_t i = 0; i < plans_rows; ++i) {  // 다음 시작 과제 번호 순서대로 확인
//         int hour, minute; sscanf(plans[i][1], "%d:%d", &hour, &minute);  // sscanf로 시각·차량번호·입출차 상태 등의 입력 항목을 형식에 맞게 읽기
//         tasks[i] = (Task){hour * 60 + minute,atoi(plans[i][2]),plans[i][0]};  // 시작 시각순 과제 갱신
//     }  // 이 범위 끝
//     qsort(tasks, plans_rows, sizeof(*tasks), compare); size_t top = 0, count = 0; int previous = 0;  // 시작 시각순 과제 / 중단된 과제 수 정렬 순서 맞추기
//     for (size_t i = 0; i < plans_rows; ++i) {  // 다음 시작 과제 번호 순서대로 확인
//         int available = tasks[i].start - previous;  // 새 과제 전까지 남은 시간 저장
//         while (available > 0 && top) {  // 다음 과제 전 여유 시간과 중단한 과제가 모두 남아 있는 동안 재개
//             Task* old = &stack[top - 1];  // 가장 최근에 중단한 과제 저장
//             if (old->duration <= available) { available -= old->duration; answer[count++] = copy_name(old->name); --top; }  // 최근 중단 과제를 끝낼 시간이 있으면 결과에 넣고 남은 여유 시간 차감
//             else { old->duration -= available; available = 0; }  // 앞 조건이 아니면 가장 최근에 중단한 과제 / 새 과제 전까지 남은 시간에서 이번 사용량 빼기
//         }  // 이 범위 끝
//         stack[top++] = tasks[i]; previous = tasks[i].start;  // 새 과제를 중단 과제 스택 위에 올리고 기준 시각 갱신
//     }  // 이 범위 끝
//     while (top) answer[count++] = copy_name(stack[--top].name);  // 중단된 과제 수가 남아 있으면 반복; 끝낸 순서의 과제 이름 갱신
//     free(tasks); free(stack);  // 시작 시각순 과제 / 중단된 과제의 LIFO 목록 임시 공간 정리
//     return answer;  // 끝낸 순서의 과제 이름 반환
// }  // 이 범위 끝

// 풀이 요약
// 시작 시각 순으로 정렬하고, 다음 시작까지의 시간에 스택 위 과제를 처리; 새 과제는 스택 위에 올리기
// 예: aaa를 멈추고 bbb를 끝낸 뒤 ccc, aaa 순으로 완료하기; 시간 O(N log N), 공간 O(N)

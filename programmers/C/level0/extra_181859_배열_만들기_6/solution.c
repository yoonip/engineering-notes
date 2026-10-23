#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    int* stack = malloc(arr_len * sizeof(int));
    size_t length = 0;
    for (size_t i = 0; i < arr_len; ++i) {
        if (length && stack[length - 1] == arr[i]) --length;
        else stack[length++] = arr[i];
    }
    if (!length) stack[length++] = -1;
    int* answer = malloc(length * sizeof(int));
    memcpy(answer, stack, length * sizeof(int));
    free(stack);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 배열 만들기 6 풀이 시작
//     int* stack = malloc(arr_len * sizeof(int));  // stack를 저장할 메모리 확보
//     size_t length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < arr_len; ++i) {  // 입력 원소를 순서대로 스택 규칙에 적용
//         if (length && stack[length - 1] == arr[i]) --length;  // 스택이 비어 있지 않고 맨 위가 현재 값과 같으면 맨 위 제거
//         else stack[length++] = arr[i];  // 스택이 비었거나 끝값이 다르면 현재 원소를 새 끝에 추가
//     }  // 블록 끝
//     if (!length) stack[length++] = -1;  // 최종 스택이 비었으면 문제의 빈 결과 표시인 -1 추가
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, stack, length * sizeof(int));  // 스택에서 최종적으로 남은 원소들을 결과 배열에 복사
//     free(stack);  // free로 반환 결과에 사용하지 않는 임시 메모리를 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 새 값과 마지막 값이 같으면 마지막 값을 제거하고, 다르면 추가. 각 입력을 한 번씩 처리

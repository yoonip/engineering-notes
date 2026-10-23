#include <stdlib.h>
#include <stddef.h>

int* solution(int arr[], size_t arr_len) {
    int* answer = malloc((arr_len ? arr_len : 1) * sizeof(int));
    size_t used = 0;
    for (size_t i = 0; i < arr_len; ++i) {
        while (used && answer[used - 1] >= arr[i]) --used;
        answer[used++] = arr[i];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int* solution(int arr[], size_t arr_len) {  // 배열 만들기 4 풀이 시작
//     int* answer = malloc((arr_len ? arr_len : 1) * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     size_t used = 0;  // 스택에 남아 있는 원소 수를 0으로 시작
//     for (size_t i = 0; i < arr_len; ++i) {  // size_t형 인덱스를 for로 증가시키며 입력 배열의 모든 원소를 순회
//         while (used && answer[used - 1] >= arr[i]) --used;  // 스택이 비지 않고 끝값이 현재 값 이상인 동안 --로 원소 개수를 줄이기
//         answer[used++] = arr[i];  // 스택 끝에 현재 원소를 넣고 후위 ++로 저장 개수를 늘림
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝// 풀이 요약
// 현재 값 이상인 스택 끝 원소를 제거한 뒤 현재 값을 넣기

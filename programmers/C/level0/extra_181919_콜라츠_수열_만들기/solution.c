#include <stdlib.h>
#include <stddef.h>

int* solution(int n) {
    size_t capacity = 32, used = 0;
    int* answer = malloc(capacity * sizeof(int));
    for (;;) {
        if (used == capacity) {
            capacity *= 2;
            answer = realloc(answer, capacity * sizeof(int));
        }
        answer[used++] = n;
        if (n == 1) break;
        n = n % 2 == 0 ? n / 2 : 3 * n + 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int* solution(int n) {  // 콜라츠 수열 만들기 풀이 시작
//     size_t capacity = 32, used = 0;  // size_t형으로 초기 할당 용량과 저장한 원소 개수를 설정
//     int* answer = malloc(capacity * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     for (;;) {  // 종료 조건을 생략한 for를 실행하고 내부의 break로 수열 생성을 끝
//         if (used == capacity) {  // 현재 저장 개수가 할당 용량과 같은지 if로 확인해 공간을 확장
//             capacity *= 2;  // 복합 대입 *=로 동적 배열의 할당 용량을 두 배로 늘림
//             answer = realloc(answer, capacity * sizeof(int));  // realloc으로 기존 내용을 유지하며 늘어난 용량만큼 저장 공간을 다시 할당
//         }  // 블록 끝
//         answer[used++] = n;  // 콜라츠 수열의 현재 값을 저장하고 저장 개수를 늘림
//         if (n == 1) break;  // if로 마지막 값 1에 도달했는지 확인하고 break로 반복을 끝
//         n = n % 2 == 0 ? n / 2 : 3 * n + 1;  // 삼항 연산자 ?:로 짝수이면 절반, 홀수이면 3배에 1을 더한 값으로 바꾸기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 시작값을 저장하고 짝수이면 절반, 홀수이면 3배에 1을 더하며 1까지 기록

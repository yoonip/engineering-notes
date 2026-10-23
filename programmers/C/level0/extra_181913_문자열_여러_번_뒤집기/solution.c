#include <stdlib.h>
#include <string.h>
#include <stddef.h>

char* solution(const char* my_string, int** queries, size_t queries_rows, size_t queries_cols) {
    (void)queries_cols;
    char* answer = malloc(strlen(my_string) + 1);
    strcpy(answer, my_string);
    for (size_t i = 0; i < queries_rows; ++i) {
        int left = queries[i][0], right = queries[i][1];
        while (left < right) {
            char temp = answer[left];
            answer[left++] = answer[right];
            answer[right--] = temp;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(const char* my_string, int** queries, size_t queries_rows, size_t queries_cols) {  // 문자열 여러 번 뒤집기 풀이 시작
//     (void)queries_cols;  // 사용하지 않는 배열 크기 매개변수를 명시적으로 무시
//     char* answer = malloc(strlen(my_string) + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     strcpy(answer, my_string);  // strcpy로 종료 문자를 포함한 원본 문자열을 복사
//     for (size_t i = 0; i < queries_rows; ++i) {  // for로 2차원 쿼리 배열의 각 행을 주어진 순서대로 처리
//         int left = queries[i][0], right = queries[i][1];  // 이중 []로 현재 뒤집기 쿼리의 양 끝 인덱스를 읽기
//         while (left < right) {  // while로 양 끝 인덱스가 만날 때까지 문자 교환을 반복
//             char temp = answer[left];  // 두 문자를 교환할 때 덮어쓰지 않도록 왼쪽 문자를 임시 변수에 저장
//             answer[left++] = answer[right];  // 오른쪽 문자를 왼쪽에 대입한 뒤 후위 ++로 왼쪽 인덱스를 늘림
//             answer[right--] = temp;  // 임시 문자를 오른쪽에 대입한 뒤 후위 --로 오른쪽 인덱스를 줄이기
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 쿼리 순서대로 각 구간의 양 끝 문자를 교환하며 뒤집기

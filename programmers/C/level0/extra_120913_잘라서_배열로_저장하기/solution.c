#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char** solution(const char* my_str, int n) {
    size_t len = strlen(my_str), rows = (len + n - 1) / n;
    char** answer = malloc(rows * sizeof(*answer));
    for (size_t i = 0; i < rows; ++i) {
        size_t count = len - i * n;
        if (count > (size_t)n) count = n;
        answer[i] = malloc(count + 1);
        memcpy(answer[i], my_str + i * n, count);
        answer[i][count] = '\0';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// char** solution(const char* my_str, int n) {  // 잘라서 배열로 저장하기 풀이 시작
//     size_t len = strlen(my_str), rows = (len + n - 1) / n;  // 전체 길이 len을 구하고 (len + n - 1) / n으로 필요한 조각 수 rows를 올림 계산
//     char** answer = malloc(rows * sizeof(*answer));  // 각 조각 문자열의 시작 주소를 저장할 rows개의 포인터 공간을 할당
//     for (size_t i = 0; i < rows; ++i) {  // 만들 조각의 번호 i를 0부터 rows - 1까지 순회
//         size_t count = len - i * n;  // 현재 조각의 시작 위치 i * n부터 남아 있는 전체 문자 수를 count에 저장
//         if (count > (size_t)n) count = n;  // 남은 문자가 n보다 많으면 이번 조각의 복사 길이 count를 n으로 제한
//         answer[i] = malloc(count + 1);  // 이번 조각의 문자 count개와 널 문자 한 칸을 담을 공간을 할당
//         memcpy(answer[i], my_str + i * n, count);  // 원본의 i * n 위치부터 count개의 문자를 현재 조각에 복사
//         answer[i][count] = '\0';  // 복사한 문자 뒤에 널 문자를 넣어 각 조각을 독립된 C 문자열로 만들기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열 길이를 n으로 나눈 올림으로 조각 수를 구하기. 각 시작 위치 i * n에서 최대 n글자씩 복사하고, 마지막 조각은 남은 길이만큼만 복사한 뒤 널 문자를 붙이기

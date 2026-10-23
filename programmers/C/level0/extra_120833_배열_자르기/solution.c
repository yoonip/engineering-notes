#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int numbers[], size_t numbers_len, int num1, int num2) {
    (void)numbers_len;
    int* answer = malloc((num2 - num1 + 1) * sizeof(*answer));
    for (int i = num1; i <= num2; ++i) answer[i - num1] = numbers[i];
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
// int* solution(int numbers[], size_t numbers_len, int num1, int num2) {  // 배열 자르기 풀이 시작
//     (void)numbers_len;  // 배열 크기처럼 함수 형식에 포함되지만 본문에서 사용하지 않는 매개변수임을 표시
//     int* answer = malloc((num2 - num1 + 1) * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (int i = num1; i <= num2; ++i) answer[i - num1] = numbers[i];  // num1부터 num2까지 양 끝을 포함해 결과로 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 원본의 num1부터 num2까지 양 끝을 포함해 새 배열에 복사.

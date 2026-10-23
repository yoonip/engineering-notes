#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* my_string) {
    int sum = 0;
    for (size_t i = 0; my_string[i]; ++i)
        if (isdigit((unsigned char)my_string[i])) sum += my_string[i] - '0';
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* my_string) {  // 숨어있는 숫자의 덧셈 (1) 풀이 시작
//     int sum = 0;  // 합은 0부터 누적
//     for (size_t i = 0; my_string[i]; ++i)  // 문자열의 각 문자를 왼쪽부터 검사
//         if (isdigit((unsigned char)my_string[i])) sum += my_string[i] - '0';  // 숫자 문자이면 0을 빼 자릿값으로 바꾼 뒤 합산
//     return sum;  // 문자열에서 찾은 모든 숫자 자릿값의 합 반환
// }  // 블록 끝
// 풀이 요약
// 이 문제는 연속된 숫자도 자릿수 하나씩 따로 더하기

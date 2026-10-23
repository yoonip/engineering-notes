#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int num, int k) {
    char digits[16];
    snprintf(digits, sizeof(digits), "%d", num);
    for (int i = 0; digits[i]; ++i) if (digits[i] - '0' == k) return i + 1;
    return -1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int num, int k) {  // 숫자 찾기 풀이 시작
//     char digits[16];  // char 배열 digits에 num의 십진수 표현과 문자열 종료 문자를 저장할 공간을 준비
//     snprintf(digits, sizeof(digits), "%d", num);  // snprintf로 num을 십진수 문자열로 바꾸기. sizeof(digits)는 쓸 수 있는 버퍼 크기를 제한
//     for (int i = 0; digits[i]; ++i) if (digits[i] - '0' == k) return i + 1;  // for로 문자열을 왼쪽부터 널 문자 전까지 읽기. digits[i]에서 문자 0을 빼 숫자로 바꾸고, k와 같으면 0부터 시작하는 인덱스에 1을 더해 첫 위치를 반환
//     return -1;  // 끝까지 k를 찾지 못하면 문제에서 정한 -1을 반환
// }  // 블록 끝

// 풀이 요약
// num을 십진수 문자열로 바꾸어 왼쪽부터 숫자 k를 찾기. 처음 일치한 인덱스에 1을 더해 반환하며, 없으면 -1을 반환

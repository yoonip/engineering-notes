#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* bin1, const char* bin2) {
    int i = (int)strlen(bin1) - 1, j = (int)strlen(bin2) - 1;
    size_t capacity = strlen(bin1) + strlen(bin2) + 2, len = 0;
    char* answer = malloc(capacity);
    int carry = 0;
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += bin1[i--] - '0';
        if (j >= 0) sum += bin2[j--] - '0';
        answer[len++] = '0' + sum % 2;
        carry = sum / 2;
    }
    for (size_t k = 0; k < len / 2; ++k) {
        char temp = answer[k]; answer[k] = answer[len - 1 - k]; answer[len - 1 - k] = temp;
    }
    answer[len] = '\0';
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
// char* solution(const char* bin1, const char* bin2) {  // 이진수 더하기 풀이 시작
//     int i = (int)strlen(bin1) - 1, j = (int)strlen(bin2) - 1;  // i와 j를 각 문자열의 마지막 문자 인덱스로 두어 낮은 자리부터 읽기. int로 변환한 뒤 1을 빼 읽기를 마친 인덱스를 -1로 표시에 사용
//     size_t capacity = strlen(bin1) + strlen(bin2) + 2, len = 0;  // capacity는 결과를 담기에 충분한 공간 크기이며 두 입력 길이의 합에 올림수와 널 문자를 위한 여유를 더하기. len은 지금까지 쓴 결과 비트 수임
//     char* answer = malloc(capacity);  // malloc으로 capacity바이트를 확보하여 결과 비트들과 마지막 널 문자를 저장
//     int carry = 0;  // int 변수 carry를 0으로 초기화하여 이전 자리에서 올라온 올림수를 관리
//     while (i >= 0 || j >= 0 || carry) {  // 둘 중 한 문자열에 읽을 비트가 남아 있거나 마지막 올림수가 남아 있는 동안 자리별 덧셈을 반복
//         int sum = carry;  // 현재 자리의 합 sum을 이전 자리의 올림수 carry로 초기화
//         if (i >= 0) sum += bin1[i--] - '0';  // bin1에 비트가 남아 있으면 문자 0을 빼 숫자 비트로 바꾸어 sum에 더하고, i--로 다음 높은 자리로 이동
//         if (j >= 0) sum += bin2[j--] - '0';  // bin2에 비트가 남아 있으면 같은 방법으로 sum에 더하고, j--로 다음 높은 자리로 이동
//         answer[len++] = '0' + sum % 2;  // sum % 2로 현재 자리의 결과 비트를 얻어 문자 0 또는 1로 저장. len++로 저장 뒤 다음 결과 위치로 이동
//         carry = sum / 2;  // 정수 나눗셈 sum / 2로 다음 높은 자리에 넘길 올림수를 계산
//     }  // 블록 끝
//     for (size_t k = 0; k < len / 2; ++k) {  // 결과 비트는 낮은 자리부터 저장되어 있으므로 앞쪽 절반의 인덱스 k를 순회하며 문자열을 뒤집기
//         char temp = answer[k]; answer[k] = answer[len - 1 - k]; answer[len - 1 - k] = temp;  // 임시 문자 temp로 앞 문자를 보관하고, 대칭 위치 len - 1 - k의 문자와 서로 교환
//     }  // 블록 끝
//     answer[len] = '\0';  // len 위치에 널 문자를 넣어 높은 자리부터 읽는 결과 문자열을 완성
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 낮은 자리부터 두 입력 비트와 올림수를 더하기. 합을 2로 나눈 나머지는 결과 비트, 몫은 다음 올림수로 사용하고 마지막에 결과 비트 순서를 뒤집기

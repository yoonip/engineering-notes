#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* my_string) {
    int sum = 0, number = 0;
    for (size_t i = 0;; ++i) {
        unsigned char c = (unsigned char)my_string[i];
        if (isdigit(c)) number = number * 10 + c - '0';
        else { sum += number; number = 0; }
        if (!c) break;
    }
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
// int solution(const char* my_string) {  // 숨어있는 숫자의 덧셈 (2) 풀이 시작
//     int sum = 0, number = 0;  // int 변수 sum에는 완성된 수의 합을, number에는 현재 읽는 연속된 숫자의 값을 저장하고 둘 다 0으로 시작
//     for (size_t i = 0;; ++i) {  // size_t 인덱스 i를 0부터 하나씩 늘리며 문자열 끝 문자까지 검사. 종료 여부는 반복문 안의 break로 판단
//         unsigned char c = (unsigned char)my_string[i];  // 현재 문자를 unsigned char로 변환해 c에 저장하여 isdigit에 전달할 수 있는 값의 범위를 지킴
//         if (isdigit(c)) number = number * 10 + c - '0';  // isdigit이 숫자 문자라고 판단하면, 기존 값에 10을 곱하고 c - '0'으로 얻은 새 자릿수를 더하기
//         else { sum += number; number = 0; }  // 숫자가 아닌 문자를 만나면 number를 sum에 더하고, 다음 숫자 묶음을 읽도록 number를 0으로 초기화
//         if (!c) break;  // c가 문자열 종료 문자이면 break로 반복을 끝. 앞의 else에서 마지막 숫자 묶음도 이미 합산됨
//     }  // 블록 끝
//     return sum;  // return으로 문자열에서 찾은 모든 자연수의 합 sum을 반환
// }  // 블록 끝
// 풀이 요약
// 문자를 왼쪽부터 읽으며 연속된 숫자를 하나의 정수로 만들기. 숫자가 아닌 문자 또는 문자열 끝을 만나면 완성한 정수를 합에 더하기

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int sides[], size_t sides_len) {
    int total = 0, largest = 0;
    for (size_t i = 0; i < sides_len; ++i) {
        total += sides[i];
        if (sides[i] > largest) largest = sides[i];
    }
    return total - largest > largest ? 1 : 2;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int sides[], size_t sides_len) {  // 삼각형의 완성조건 (1) 풀이 시작
//     int total = 0, largest = 0;  // 세 변의 합과 가장 긴 변을 구할 누적값
//     for (size_t i = 0; i < sides_len; ++i) {  // 세 변의 길이를 읽으며 전체 합과 가장 긴 변 계산
//         total += sides[i];  // 현재 변 길이를 세 변의 합에 추가
//         if (sides[i] > largest) largest = sides[i];  // sides[i] > largest이면 largest에 sides[i] 저장
//     }  // 블록 끝
//     return total - largest > largest ? 1 : 2;  // 가장 긴 변이 나머지 두 변의 합보다 작으면 1, 아니면 2 반환
// }  // 블록 끝// 풀이 요약
// 전체 합에서 가장 긴 변을 뺀 값이 가장 긴 변보다 큰지 확인

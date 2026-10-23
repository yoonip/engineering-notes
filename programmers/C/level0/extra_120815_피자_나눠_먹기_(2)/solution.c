#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int a = n, b = 6;
    while (b) { int r = a % b; a = b; b = r; }
    return n / a;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) {  // 피자 나눠 먹기 (2) 풀이 시작
//     int a = n, b = 6;  // 최대공약수를 구할 두 정수 a와 b를 사람 수 n과 한 판의 조각 수 6으로 초기화
//     while (b) { int r = a % b; a = b; b = r; }  // b가 0이 아닌 동안 나머지 r = a % b를 구하고, a를 이전 b로, b를 r로 바꾸기. 반복이 끝나면 a가 n과 6의 최대공약수임
//     return n / a;  // 최소공배수 n * 6 / a를 한 판의 조각 수 6으로 나눈 값인 n / a를 반환
// }  // 블록 끝

// 풀이 요약
// 사람 수 n과 한 판의 조각 수 6의 최대공약수를 유클리드 호제법으로 구하기. 총 조각 수가 n과 6의 최소공배수여야 하므로 필요한 피자 수는 n / 최대공약수임

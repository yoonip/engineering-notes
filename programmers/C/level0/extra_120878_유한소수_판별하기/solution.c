#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int a, int b) {
    int x = a, y = b;
    while (y) { int r = x % y; x = y; y = r; }
    b /= x;
    while (b % 2 == 0) b /= 2;
    while (b % 5 == 0) b /= 5;
    return b == 1 ? 1 : 2;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int a, int b) {  // 유한소수 판별하기 풀이 시작
//     int x = a, y = b;  // 최대공약수를 구하는 동안 원래 분수 값을 보존할 복사본
//     while (y) { int r = x % y; x = y; y = r; }  // 유클리드 호제법으로 나머지를 반복 계산해 최대공약수 x 구하기
//     b /= x;  // 분모를 최대공약수로 나누어 기약분수의 분모로 약분
//     while (b % 2 == 0) b /= 2;  // while은 분모가 해당 소인수로 나누어지는 동안 반복하여 그 소인수를 제거
//     while (b % 5 == 0) b /= 5;  // while은 분모가 해당 소인수로 나누어지는 동안 반복하여 그 소인수를 제거
//     return b == 1 ? 1 : 2;  // 약분한 분모에서 2와 5를 모두 없앤 뒤 1이면 유한소수 1, 아니면 2 반환
// }  // 블록 끝
// 풀이 요약
// 약분한 분모에서 2와 5를 모두 제거했을 때 1이 남으면 유한소수임

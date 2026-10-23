#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    for (int r = 1; r <= n / r; ++r) if (r * r == n) return 1;
    return 2;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) {  // 제곱수 판별하기 풀이 시작
//     for (int r = 1; r <= n / r; ++r) if (r * r == n) return 1;  // for로 후보 r을 1부터 제곱근 이하까지 늘림. r <= n / r은 r의 제곱이 n 이하라는 뜻이며, r * r이 n과 같으면 제곱수이므로 즉시 1을 반환
//     return 2;  // 제곱근 이하의 모든 정수 후보에서 일치하는 값이 없으면 제곱수가 아니므로 2를 반환
// }  // 블록 끝
// 풀이 요약
// 정수 후보를 1부터 n의 제곱근 이하까지 검사. 제곱이 n과 같은 후보가 있으면 1, 없으면 2를 반환

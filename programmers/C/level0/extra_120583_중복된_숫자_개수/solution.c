#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len, int n) {
    int count = 0;
    for (size_t i = 0; i < array_len; ++i) count += array[i] == n;
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int array[], size_t array_len, int n) {  // 중복된 숫자 개수 풀이 시작
//     int count = 0;  // 찾을 값 n의 등장 횟수를 0으로 시작
//     for (size_t i = 0; i < array_len; ++i) count += array[i] == n;  // 배열을 모두 읽으며 원소가 n과 같을 때마다 개수 증가
//     return count;  // 중복 등장을 각각 포함한 n의 총 출현 횟수 반환
// }  // 블록 끝
// 풀이 요약
// 배열의 모든 원소를 순회하며 n과 같을 때마다 개수 증가. 중복된 원소도 등장한 횟수만큼 모두 셈.

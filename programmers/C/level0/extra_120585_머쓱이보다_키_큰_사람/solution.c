#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len, int height) {
    int count = 0;
    for (size_t i = 0; i < array_len; ++i) count += array[i] > height;
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
// int solution(int array[], size_t array_len, int height) {  // 머쓱이보다 키 큰 사람 풀이 시작
//     int count = 0;  // 기준보다 키가 큰 사람 수를 0으로 시작
//     for (size_t i = 0; i < array_len; ++i) count += array[i] > height;  // 기준 키 height보다 큰 원소마다 참의 값 1을 더함
//     return count;  // 기준보다 키가 큰 사람 수 반환
// }  // 블록 끝
// 풀이 요약
// 같은 키는 제외하고 기준 키보다 큰 사람만 세기

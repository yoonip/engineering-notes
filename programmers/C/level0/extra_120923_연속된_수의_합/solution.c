#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int num, int total) {
    int* answer = malloc(num * sizeof(*answer));
    int first = (2 * total / num - num + 1) / 2;
    for (int i = 0; i < num; ++i) answer[i] = first + i;
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
// int* solution(int num, int total) {  // 연속된 수의 합 풀이 시작
//     int* answer = malloc(num * sizeof(*answer));  // answer를 저장할 메모리 확보
//     int first = (2 * total / num - num + 1) / 2;  // 연속수열의 합 식을 정리해 첫 번째 수 계산
//     for (int i = 0; i < num; ++i) answer[i] = first + i;  // 구한 첫 수부터 1씩 증가시켜 num개의 연속 정수 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 연속된 수를 시작값+x로 표현하고 0부터 num-1까지의 합을 빼 시작값을 역산

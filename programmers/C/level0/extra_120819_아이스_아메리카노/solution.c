#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int money) {
    int* answer = malloc(2 * sizeof(*answer));
    answer[0] = money / 5500; answer[1] = money % 5500;
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
// int* solution(int money) {  // 아이스 아메리카노 풀이 시작
//     int* answer = malloc(2 * sizeof(*answer));  // answer를 저장할 메모리 확보
//     answer[0] = money / 5500; answer[1] = money % 5500;  // 살 수 있는 커피 잔 수는 몫, 남은 돈은 나머지
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 가격 5500원으로 나눈 몫과 나머지를 사용

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int n) {
    int* answer = malloc(((n + 1) / 2) * sizeof(*answer));
    for (int i = 0; 2 * i + 1 <= n; ++i) answer[i] = 2 * i + 1;
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
// int* solution(int n) {  // 짝수는 싫어요 풀이 시작
//     int* answer = malloc(((n + 1) / 2) * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (int i = 0; 2 * i + 1 <= n; ++i) answer[i] = 2 * i + 1;  // 1, 3, 5, …를 생성해 n 이하인 홀수만 순서대로 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 1부터 두 칸 간격으로 증가하면 홀수만 선택됨

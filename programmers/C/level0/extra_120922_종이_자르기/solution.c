#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int M, int N) { return M * N - 1; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int M, int N) { return M * N - 1; }  // 종이 자르기 풀이 시작
// 풀이 요약
// 한 조각에서 시작해 한 번 자를 때마다 조각 수가 1 증가. M × N조각까지 늘리는 데 필요한 횟수는 M × N - 1.

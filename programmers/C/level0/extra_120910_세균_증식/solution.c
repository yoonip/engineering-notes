#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n, int t) { return n * (1 << t); }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n, int t) { return n * (1 << t); }  // 세균 증식 풀이 시작

// 풀이 요약
// 세균은 한 시간마다 두 배가 되므로 t시간 후 개수는 n × 2의 t제곱임. 1 << t로 배수를 구해 처음 개수 n에 곱하기

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int slice, int n) { return (n + slice - 1) / slice; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int slice, int n) { return (n + slice - 1) / slice; }  // 피자 나눠 먹기 (3) 풀이 시작

// 풀이 요약
// 한 판의 조각 수 slice로 사람 수 n을 나눈 값을 올림하여 필요한 피자 판 수를 구하기

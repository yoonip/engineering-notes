#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int num1, int num2) { return num1 * 1000 / num2; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int num1, int num2) { return num1 * 1000 / num2; }  // num1에 먼저 1000을 곱한 뒤 정수 나눗셈으로 비율의 1000배 정수 부분 계산
// 풀이 요약
// num1에 먼저 1000을 곱한 뒤 정수 나눗셈으로 비율의 1000배 정수 부분 계산

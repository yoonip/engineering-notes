#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int n) { int answer = 0; while (n) { answer += n % 10; n /= 10; } return answer; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int solution(int n) { int answer = 0; while (n) { answer += n % 10; n /= 10; } return answer; }  // n을 10으로 나눈 나머지로 끝자리를 얻어 더하고, n을 10으로 나누어 그 자리를 제거합니다. 남은 자릿수가 없을 때까지 반복합니다.

// 풀이 요약
// n을 10으로 나눈 나머지로 끝자리를 얻어 더하고, n을 10으로 나누어 그 자리를 제거합니다. 남은 자릿수가 없을 때까지 반복합니다.

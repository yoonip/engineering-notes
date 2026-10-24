#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) { return (n + 6) / 7; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) { return (n + 6) / 7; }  // 7로 나눠떨어지지 않는 인원도 한 판이 필요하므로 (n+6)/7로 올림 계산

// 풀이 요약
// 7로 나눠떨어지지 않는 인원도 한 판이 필요하므로 (n+6)/7로 올림 계산

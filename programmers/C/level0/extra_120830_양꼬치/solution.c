#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n, int k) { return n * 12000 + (k - n / 10) * 2000; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n, int k) { return n * 12000 + (k - n / 10) * 2000; }  // 양꼬치 풀이 시작

// 풀이 요약
// 양꼬치 n인분의 금액과 유료 음료의 금액을 더하기. 정수 나눗셈 n / 10으로 무료 음료 수를 구해 주문한 음료 k개에서 빼기

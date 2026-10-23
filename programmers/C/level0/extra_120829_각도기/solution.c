#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int angle) { return angle < 90 ? 1 : angle == 90 ? 2 : angle < 180 ? 3 : 4; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int angle) { return angle < 90 ? 1 : angle == 90 ? 2 : angle < 180 ? 3 : 4; }  // 각도기 풀이 시작

// 풀이 요약
// 각도를 90도 미만, 90도, 180도 미만, 180도의 순서로 분류하여 문제에서 지정한 번호를 반환

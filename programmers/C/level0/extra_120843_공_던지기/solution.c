#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int numbers[], size_t numbers_len, int k) {
    return numbers[(2 * (k - 1)) % numbers_len];
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int numbers[], size_t numbers_len, int k) {  // 공 던지기 풀이 시작
//     return numbers[(2 * (k - 1)) % numbers_len];  // 첫 번째 던지기 전 이동은 0회이므로 2 * (k - 1)을 계산. 나머지 연산으로 원형 배열의 인덱스로 바꾼 뒤 그 위치의 사람 번호를 반환
// }  // 블록 끝

// 풀이 요약
// 첫 번째 사람의 인덱스를 0으로 두면 한 번 던질 때마다 인덱스가 2씩 증가. k번째로 던지는 사람은 2 × (k - 1)을 사람 수로 나눈 나머지 위치에 있음

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int a, int b, int n) {
    int answer = 0;
    while (n >= a) { int exchanged = n / a * b; n = n % a + exchanged; answer += exchanged; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int solution(int a, int b, int n) {  // 빈 병으로 바꿀 수 있는 새 병 수를 더하기; 교환 후 남은 빈 병과 새 병을 합쳐 더 교환할 수 없을 때까지 반복하기
//     int answer = 0;  // 교환으로 받은 콜라 총개수 저장
//     while (n >= a) { int exchanged = n / a * b; n = n % a + exchanged; answer += exchanged; }  // 교환할 빈 병이 남아 있는 동안 받은 콜라 수를 더하고 빈 병 수 갱신
//     return answer;  // 교환으로 받은 콜라 총개수 반환
// }  // 이 범위 끝

// 풀이 요약
// 빈 병으로 바꿀 수 있는 새 병 수를 더하기; 교환 후 남은 빈 병과 새 병을 합쳐 더 교환할 수 없을 때까지 반복하기

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* binomial) {
    int a, b;
    char op;
    sscanf(binomial, "%d %c %d", &a, &op, &b);
    return op == '+' ? a + b : op == '-' ? a - b : a * b;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* binomial) {  // 간단한 식 계산하기 풀이 시작
//     int a, b;  // 식의 왼쪽·오른쪽 정수 a와 b 준비
//     char op;  // 적용할 연산자 한 글자 저장
//     sscanf(binomial, "%d %c %d", &a, &op, &b);  // sscanf의 %d·%c 형식으로 피연산자와 연산자를 읽기
//     return op == '+' ? a + b : op == '-' ? a - b : a * b;  // 연산자가 +면 합, -면 차, 그 외 *면 곱 반환
// }  // 블록 끝
// 풀이 요약
// 문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용

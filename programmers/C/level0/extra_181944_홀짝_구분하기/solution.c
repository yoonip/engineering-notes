#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%d is %s\n", n, n % 2 == 0 ? "even" : "odd");
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int n;  // 짝홀을 판단할 입력 정수 n 준비
//     if (scanf("%d", &n) != 1) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     printf("%d is %s\n", n, n % 2 == 0 ? "even" : "odd");  // printf의 형식 지정자와 이스케이프 문자로 요구된 형식의 결과를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝
// 풀이 요약
// 2로 나눈 나머지에 따라 짝수와 홀수 출력 형식을 선택

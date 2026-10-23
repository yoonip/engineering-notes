#include <stdio.h>

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    printf("%d + %d = %d\n", a, b, a + b);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 입력 정수 두 개를 저장할 int형 변수를 선언
//     if (scanf("%d %d", &a, &b) != 2) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     printf("%d + %d = %d\n", a, b, a + b);  // printf의 형식 지정자와 이스케이프 문자로 요구된 형식의 결과를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 덧셈을 계산하고 요구된 공백과 기호를 포함해 출력

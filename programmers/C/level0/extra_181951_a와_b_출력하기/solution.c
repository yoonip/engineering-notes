#include <stdio.h>

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    printf("a = %d\nb = %d\n", a, b);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 두 입력 정수를 담을 int형 변수를 선언
//     if (scanf("%d %d", &a, &b) != 2) return 0;  // &로 변수 주소를 전달해 정수를 읽고 입력 개수를 확인
//     printf("a = %d\nb = %d\n", a, b);  // %d에 정수를 넣고 \n으로 줄을 바꿔 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 두 정수를 변수 이름과 함께 각각 출력

#include <stdio.h>

int main(void) {
    char text[1000001];
    if (scanf("%1000000s", text) != 1) return 0;
    puts(text);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[1000001];  // 문자열과 종료 문자를 담을 문자 배열을 선언
//     if (scanf("%1000000s", text) != 1) return 0;  // 배열 크기에 맞게 문자열을 읽고 입력 성공 여부를 확인
//     puts(text);  // puts로 입력 문자열과 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 문자열을 바꾸지 않고 그대로 출력

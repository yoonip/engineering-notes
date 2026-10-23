#include <stdio.h>

int main(void) {
    puts("!@#$%^&*(\\'\"<>?:;");
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     puts("!@#$%^&*(\\'\"<>?:;");  // puts로 지정된 문자열과 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 역슬래시와 큰따옴표를 이스케이프해 지정된 특수문자를 출력

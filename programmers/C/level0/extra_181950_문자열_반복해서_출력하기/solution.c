#include <stdio.h>

int main(void) {
    char text[100001];
    int n;
    if (scanf("%100000s %d", text, &n) != 2) return 0;
    for (int i = 0; i < n; ++i) fputs(text, stdout);
    putchar('\n');
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[100001];  // 입력 문자열을 저장할 문자 배열임
//     int n;  // 반복 횟수를 저장
//     if (scanf("%100000s %d", text, &n) != 2) return 0;  // 문자열과 반복 횟수를 읽고 입력 실패 시 종료
//     for (int i = 0; i < n; ++i) fputs(text, stdout);  // for문으로 문자열을 n번 출력
//     putchar('\n');  // 출력 끝에서 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열을 읽은 뒤 반복 횟수만큼 이어서 출력

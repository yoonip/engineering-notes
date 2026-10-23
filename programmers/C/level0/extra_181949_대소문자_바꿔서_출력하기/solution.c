#include <stdio.h>
#include <ctype.h>

int main(void) {
    char text[100001];
    if (scanf("%100000s", text) != 1) return 0;
    for (int i = 0; text[i]; ++i) {
        unsigned char c = (unsigned char)text[i];
        putchar(islower(c) ? toupper(c) : tolower(c));
    }
    putchar('\n');
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[100001];  // 입력 문자열과 종료 문자를 담을 char형 배열을 선언
//     if (scanf("%100000s", text) != 1) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     for (int i = 0; text[i]; ++i) {  // for로 널 문자 직전까지 각 문자의 인덱스를 순회
//         unsigned char c = (unsigned char)text[i];  // 문자 분류 함수에 안전하게 전달하도록 문자를 unsigned char로 변환
//         putchar(islower(c) ? toupper(c) : tolower(c));  // islower와 삼항 연산자로 대소문자 변환을 선택하고 putchar로 출력
//     }  // 블록 끝
//     putchar('\n');  // putchar로 줄바꿈 문자 하나를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 각 문자가 소문자이면 대문자로, 대문자이면 소문자로 바꾸기

#include <stdio.h>

int main(void) {
    char first[100001], second[100001];
    if (scanf("%100000s %100000s", first, second) != 2) return 0;
    printf("%s%s\n", first, second);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char first[100001], second[100001];  // 입력 문자열 두 개를 각각 저장할 char형 배열을 선언
//     if (scanf("%100000s %100000s", first, second) != 2) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     printf("%s%s\n", first, second);  // printf의 형식 지정자와 이스케이프 문자로 요구된 형식의 결과를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 공백으로 구분한 두 문자열을 붙여 출력

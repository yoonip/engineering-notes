#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    scanf("%32s", text);  // 종료 문자까지 들어갈 33칸 버퍼 사용
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


static int digit_value(char ch) {  // 숫자 문자 한 개를 자릿값으로 해석
    if (ch >= '0' && ch <= '9') return ch - '0';  // 십진 숫자의 자릿값
    return ch - 'A' + 10;  // 대문자 A~F를 10~15로 변환
}  // 자릿값 변환 함수 끝
int main(void) {  // 자리값의 나머지 누적
    int base = read_int(), modulus = read_int();  // 진법의 밑과 양의 나누는 수
    char text[33]; read_word(text);  // 최대 32자리와 종료 문자
    int remainder = 0;  // 빈 접두사의 나머지
    for (int i = 0; text[i] != '\0'; ++i) {  // 높은 자리부터 차례로 읽기
        int digit = digit_value(text[i]);  // 현재 숫자의 자릿값
        remainder = (remainder * base + digit) % modulus;  // 다음 자리를 붙인 값의 나머지만 유지
    }  // 모든 자릿값 누적 끝
    write_number(remainder); write_text("\n");  // 전체 수의 나머지 출력
    return 0;  // 정상 종료
}  // 진법·나머지 예제 끝

#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 양의 분모에 대한 floor 나눗셈 비교
    int a = read_int(), b = read_int();  // 나눌 정수와 양의 나누는 수
    int quotient = a / b, remainder = a % b;  // C·C++의 0 방향 몫과 그 나머지
    if (remainder < 0) {  // 음수 나머지이면 아직 내림 규칙과 다름
        --quotient;  // 몫을 한 단계 더 낮추기
        remainder += b;  // 같은 등식을 유지하며 나머지를 비음수로 조정
    }  // 내림 몫 보정 끝
    write_number(quotient); write_text(" "); write_number(remainder); write_text("\n");  // 두 값을 같은 형식으로 출력
    return 0;  // 정상 종료
}  // 음수 나눗셈 예제 끝

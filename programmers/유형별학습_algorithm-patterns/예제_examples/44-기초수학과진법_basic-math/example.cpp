#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    cin.width(33);  // 종료 문자를 포함한 버퍼 크기로 읽기 제한
    cin >> text;  // 공백 전까지의 토큰 읽기
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    cout << value;  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
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

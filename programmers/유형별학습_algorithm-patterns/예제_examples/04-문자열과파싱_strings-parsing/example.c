#include <stdio.h> // 한 줄 입력과 결과 출력
int main(void) { // 실행 시작점
    char text[102]; // 최대 100문자와 줄바꿈·끝 표시 공간
    fgets(text, sizeof(text), stdin); // 콤마가 포함된 입력 줄 읽기
    int position = 0, count = 0; long long total = 0; // 스캔 위치·정수 수·합 초기화
    while (1) { // 정수 토큰 하나씩 해석
        while (text[position] == ' ') ++position; // 토큰 앞의 ASCII 공백 건너뛰기
        int sign = 1, number = 0; // 기본 양수 부호와 현재 정수 초기화
        if (text[position] == '+' || text[position] == '-') { // 선택적 부호 검사
            if (text[position] == '-') sign = -1; // 음수 부호 반영
            ++position; // 부호 다음 숫자로 이동
        } // 부호 처리 끝
        while ('0' <= text[position] && text[position] <= '9') { // 연속된 십진수 숫자 읽기
            number = number * 10 + text[position] - '0'; ++position; // 자리값을 누적하고 다음 문자로 이동
        } // 정수 한 개 해석 끝
        total += sign * number; ++count; // 정수의 합과 개수 갱신
        while (text[position] == ' ') ++position; // 정수 뒤 공백 건너뛰기
        if (text[position] != ',') break; // 콤마가 없으면 마지막 토큰 처리 완료
        ++position; // 구분자 다음 토큰으로 이동
    } // 전체 줄 파싱 끝
    printf("%d %lld\n", count, total); // 읽은 정수 수와 합 출력
    return 0; // 정상 종료
} // 제한된 콤마 문법 파싱 끝

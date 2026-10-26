#include <stdio.h>  // 문자열 입력과 결과 출력
#include <string.h>  // 입력 문자열 길이

int minimum(int a, int b) { return a < b ? a : b; }  // 거울 반지름과 경계의 작은 값
int main(void) {  // 회문 반지름 계산 시작
    char text[101]; int odd[100], even[100];  // 문자열과 두 종류의 중심
    scanf("%100s", text);  // 빈 문자열은 입력 범위에서 제외
    int n = (int)strlen(text), left = 0, right = -1, best = 0, total = 0;  // 현재 경계와 결과
    for (int i = 0; i < n; ++i) {  // 문자 위의 홀수 중심
        int radius = i > right ? 1 : minimum(odd[left + right - i], right - i + 1);  // 검증된 거울 범위
        while (i - radius >= 0 && i + radius < n && text[i - radius] == text[i + radius]) ++radius;  // 경계 밖 일치 확장
        odd[i] = radius; total += radius;  // 중심별 회문 수 누적
        if (2 * radius - 1 > best) best = 2 * radius - 1;  // 홀수 최장 길이
        if (i + radius - 1 > right) { left = i - radius + 1; right = i + radius - 1; }  // 가장 먼 경계 갱신
    }  // 홀수 중심 처리 끝
    left = 0; right = -1;  // 짝수 중심의 독립 경계
    for (int i = 0; i < n; ++i) {  // i의 바로 앞을 짝수 중심으로 사용
        int radius = i > right ? 0 : minimum(even[left + right - i + 1], right - i + 1);  // 짝수 거울 중심
        while (i - radius - 1 >= 0 && i + radius < n && text[i - radius - 1] == text[i + radius]) ++radius;  // 두 문자씩 확장
        even[i] = radius; total += radius;  // 짝수 회문 발생 수 누적
        if (2 * radius > best) best = 2 * radius;  // 짝수 최장 길이
        if (i + radius - 1 > right) { left = i - radius; right = i + radius - 1; }  // 짝수 회문의 먼 경계
    }  // 짝수 중심 처리 끝
    printf("MAX %d\nCOUNT %d\n", best, total);  // 길이와 위치별 발생 수
    return 0;  // 정상 종료
}  // 프로그램 끝

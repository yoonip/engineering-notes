#include <stdio.h>  // 표준 입력과 출력 함수

long long gcd_value(long long a, long long b) {  // 음이 아닌 두 수의 최대공약수
    while (b != 0) {  // 나머지가 없어질 때까지 반복
        long long remainder = a % b;  // 공약수를 보존하는 나머지
        a = b; b = remainder;  // 다음 유클리드 상태
    }  // 최대공약수 확정
    return a;  // gcd(0,0)은 이 예제에서 0
}  // 최대공약수 함수 끝
long long power_mod(long long base, long long exponent, long long modulus) {  // 나머지를 유지하는 거듭제곱
    long long result = 1 % modulus;  // 빈 곱과 모듈러1 처리
    base %= modulus;  // 제곱할 현재 인수의 나머지
    while (exponent > 0) {  // 남은 지수의 비트 처리
        if (exponent & 1LL) result = result * base % modulus;  // 필요한 거듭제곱만 선택
        base = base * base % modulus;  // 다음 비트의 제곱
        exponent >>= 1;  // 처리한 비트 제거
    }  // 모든 지수 처리 끝
    return result;  // 최종 나머지
}  // 거듭제곱 함수 끝
int main(void) {  // 두 정수론 예제 실행
    long long a, b, exponent, modulus;  // 중간 곱까지 담는 정수
    scanf("%lld %lld %lld %lld", &a, &b, &exponent, &modulus);  // 입력 조건 읽기
    printf("GCD %lld\n", gcd_value(a, b));  // 최대공약수 출력
    printf("POWER %lld\n", power_mod(a, exponent, modulus));  // 모듈러 거듭제곱 출력
    return 0;  // 정상 종료
}  // 프로그램 끝

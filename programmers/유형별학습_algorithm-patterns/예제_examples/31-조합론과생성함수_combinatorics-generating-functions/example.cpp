#include <iostream>  // C++ 스트림 입력과 출력

int gcd_value(int a, int b) {  // 공배수 계산에 사용할 최대공약수
    while (b) { int remainder = a % b; a = b; b = remainder; }  // 유클리드 나머지 반복
    return a;  // 양의 최대공약수
}  // 최대공약수 계산 끝
int main() {  // 계수 곱과 포함 배제 실행
    int n, m, a[8], b[8], product[15] = {0};  // 작은 다항식의 고정 저장
    std::cin >> n >> m;  // 두 계수 배열 길이
    for (int i = 0; i < n; ++i) std::cin >> a[i];  // 첫 다항식의 낮은 차수부터 입력
    for (int j = 0; j < m; ++j) std::cin >> b[j];  // 둘째 다항식 입력
    for (int i = 0; i < n; ++i) {  // 첫 선택의 크기
        for (int j = 0; j < m; ++j) product[i + j] += a[i] * b[j];  // 합쳐진 크기의 계수 누적
    }  // 모든 계수 기여 처리 끝
    int limit, p, q;  // 포함 배제의 정수 범위와 배수 조건
    std::cin >> limit >> p >> q;  // 1부터 limit까지의 조건
    int lcm = p / gcd_value(p, q) * q;  // 중복으로 센 공배수 주기
    int union_count = limit / p + limit / q - limit / lcm;  // 교집합을 한 번 제외
    for (int i = 0; i < n + m - 1; ++i) {  // 곱의 모든 차수 출력
        std::cout << (i ? " " : "") << product[i];  // 앞 공백으로 후행 공백 방지
    }  // 계수 출력 끝
    std::cout << "\n" << union_count << "\n";  // 계수 줄 종료와 합집합 개수
    return 0;  // 정상 종료
}  // 프로그램 끝

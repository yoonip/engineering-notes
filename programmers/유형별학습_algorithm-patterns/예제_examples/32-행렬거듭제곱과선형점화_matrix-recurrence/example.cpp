#include <iostream>  // C++ 스트림 입력과 출력

typedef struct { long long cell[2][2]; } Matrix;  // 두 항의 선형 전이 저장
long long modulus;  // 모든 행렬 연산의 같은 모듈러
Matrix multiply(Matrix left, Matrix right) {  // 입력과 분리한 행렬 곱
    Matrix result = {{{0, 0}, {0, 0}}};  // 새 결과는 영행렬
    for (int i = 0; i < 2; ++i) {  // 결과의 행
        for (int j = 0; j < 2; ++j) {  // 결과의 열
            for (int k = 0; k < 2; ++k) result.cell[i][j] = (result.cell[i][j] + left.cell[i][k] * right.cell[k][j]) % modulus;  // 행과 열의 내적
        }  // 한 행의 열 계산 끝
    }  // 행렬 곱 계산 끝
    return result;  // 독립적인 결과 행렬
}  // 곱셈 함수 끝
int main() {  // 피보나치 전이의 거듭제곱
    long long exponent;  // 계산할 단계 수
    std::cin >> exponent >> modulus;  // 지수와 모듈러 입력
    Matrix answer = {{{1, 0}, {0, 1}}};  // 0단계의 단위행렬
    Matrix base = {{{1, 1}, {1, 0}}};  // 한 단계 피보나치 전이
    while (exponent > 0) {  // 필요한 거듭제곱을 비트별로 선택
        if (exponent & 1LL) answer = multiply(answer, base);  // 현재 자리의 전이 누적
        base = multiply(base, base);  // 두 배 이동 길이로 제곱
        exponent >>= 1;  // 처리한 지수 비트 제거
    }  // 모든 단계 합성 끝
    std::cout << answer.cell[1][0] % modulus << "\n";  // F_N의 나머지
    return 0;  // 정상 종료
}  // 프로그램 끝

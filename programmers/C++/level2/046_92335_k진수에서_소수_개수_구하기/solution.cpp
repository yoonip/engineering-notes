#include <algorithm>
#include <string>
using namespace std;

int solution(int n, int k) {
    string digits;
    while (n > 0) { digits.push_back(char('0' + n % k)); n /= k; }
    reverse(digits.begin(), digits.end());
    auto prime = [](long long value) {
        if (value < 2) return false;
        if (value % 2 == 0) return value == 2;
        for (long long d = 3; d <= value / d; d += 2) if (value % d == 0) return false;
        return true;
    };
    int answer = 0; long long value = 0;
    for (char digit : digits + '0') {
        if (digit == '0') { answer += prime(value); value = 0; }
        else value = value * 10 + digit - '0';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(int n, int k) {  // k진수의 0 사이 조각을 십진수로 읽어 소수 판정
// string digits;  // k진수의 자릿수를 문자열로 저장
// while (n > 0) { digits.push_back(char('0' + n % k)); n /= k; }  // 나머지 연산으로 낮은 자릿수부터 구하기
// reverse(digits.begin(), digits.end());  // 높은 자릿수가 앞으로 오도록 뒤집기
// auto prime = [](long long value) {  // 분리한 십진 정수가 소수인지 검사
// if (value < 2) return false;  // 0과 1은 소수가 아님
// if (value % 2 == 0) return value == 2;  // 짝수는 2만 소수
// for (long long d = 3; d <= value / d; d += 2) if (value % d == 0) return false;  // 제곱근까지 홀수 약수가 있는지 검사
// return true;  // 약수가 없으면 소수
// };  // 블록 끝
// int answer = 0; long long value = 0;  // 소수 개수와 현재 숫자 조각 초기화
// for (char digit : digits + '0') {  // 마지막 조각도 처리하도록 끝에 구분자 0 붙이기
// if (digit == '0') { answer += prime(value); value = 0; }  // 구분자에서 조각의 소수 여부를 세고 초기화
// else value = value * 10 + digit - '0';  // 0이 아닌 자릿수를 십진 정수로 이어 붙이기
// }  // 블록 끝
// return answer;  // 조건을 만족하는 소수 조각 수 반환
// }  // 블록 끝

// 풀이 요약
// n을 k진수 문자열로 바꾸고 0으로 구분한 조각을 십진 정수로 읽어 소수 여부 검사

#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

int solution(int a, int b) {
    int x = a, y = b;
    while (y) { int r = x % y; x = y; y = r; }
    b /= x;
    while (b % 2 == 0) b /= 2;
    while (b % 5 == 0) b /= 5;
    return b == 1 ? 1 : 2;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b) {  // 유한소수 판별하기 풀이 시작
//     int x = a, y = b;  // 분자와 분모의 최대공약수를 구할 복사본
//     while (y) { int r = x % y; x = y; y = r; }  // 유클리드 호제법으로 최대공약수를 x에 남기기
//     b /= x;  // 최대공약수로 분모를 나눠 기약분수로 약분
//     while (b % 2 == 0) b /= 2;  // while은 분모가 해당 소인수로 나누어지는 동안 반복하여 그 소인수를 제거
//     while (b % 5 == 0) b /= 5;  // while은 분모가 해당 소인수로 나누어지는 동안 반복하여 그 소인수를 제거
//     return b == 1 ? 1 : 2;  // 2와 5를 제거한 분모가 1이면 유한소수, 아니면 무한소수
// }  // 블록 끝

// 풀이 요약
// 약분한 분모에서 2와 5를 모두 제거했을 때 1이 남으면 유한소수임

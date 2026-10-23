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

int solution(string my_string) {
    int sum = 0;
    for (unsigned char c : my_string) if (isdigit(c)) sum += c - '0';
    return sum;
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
// int solution(string my_string) {  // 숨어있는 숫자의 덧셈 (1) 풀이 시작
//     int sum = 0;  // 문자열에서 발견한 한 자리 숫자의 합
//     for (unsigned char c : my_string) if (isdigit(c)) sum += c - '0';  // 숫자 문자만 자릿값으로 바꿔 더하기
//     return sum;  // 숨어 있는 한 자리 숫자의 총합
// }  // 블록 끝

// 풀이 요약
// 이 문제는 연속된 숫자도 자릿수 하나씩 따로 더하기

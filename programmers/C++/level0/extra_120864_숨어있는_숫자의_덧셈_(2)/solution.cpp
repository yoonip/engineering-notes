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
    int sum = 0, number = 0;
    for (unsigned char c : my_string) {
        if (isdigit(c)) number = number * 10 + c - '0';
        else { sum += number; number = 0; }
    }
    return sum + number;
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
// int solution(string my_string) {  // 숨어있는 숫자의 덧셈 (2) 풀이 시작
//     int sum = 0, number = 0;  // 완성된 수의 합과 지금 읽는 연속 숫자의 값
//     for (unsigned char c : my_string) {  // 숫자는 이어 읽고 문자를 만나면 한 수를 마무리
//         if (isdigit(c)) number = number * 10 + c - '0';  // isdigit으로 숫자 문자인지 검사하고 참일 때 해당 숫자를 계산에 반영
//         else { sum += number; number = 0; }  // else는 앞선 if 조건이 거짓인 경우의 계산을 실행
//     }  // 블록 끝
//     return sum + number;  // 문자 없이 끝난 마지막 숫자도 합에 포함
// }  // 블록 끝

// 풀이 요약
// 숫자를 만나면 현재 수에 자릿수를 이어 붙이고, 문자를 만나면 완성된 수를 합에 더해 초기화. 문자열 끝의 마지막 수까지 더하기

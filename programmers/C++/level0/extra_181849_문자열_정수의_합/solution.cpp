#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(string num_str) {
    int sum = 0;
    for (char digit : num_str) sum += digit - '0';
    return sum;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string num_str) {  // 문자열 정수의 합 풀이 시작
//     int sum = 0;  // 문자열에 적힌 각 자릿수의 합
//     for (char digit : num_str) sum += digit - '0';  // 숫자 문자에서 '0'을 빼 자릿값으로 바꿔 더하기
//     return sum;  // 누적 합계 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 전체를 하나의 정수로 바꾸지 않고 각 자릿수를 더하기

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

string solution(string my_string) {
    for (char& c : my_string) c = isupper(static_cast<unsigned char>(c)) ? tolower(c) : toupper(c);
    return my_string;
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
// string solution(string my_string) {  // 대문자와 소문자 풀이 시작
//     for (char& c : my_string) c = isupper(static_cast<unsigned char>(c)) ? tolower(c) : toupper(c);  // 범위 기반 for의 char& c는 원본 문자열의 각 문자를 직접 참조. isupper로 대문자인지 검사하여 대문자는 tolower로, 소문자는 toupper로 바꿔 같은 위치에 저장. 검사할 때 unsigned char로 변환
//     return my_string;  // return으로 모든 영문자의 대소문자를 교환한 my_string을 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자를 참조로 읽으며 대문자는 소문자로, 소문자는 대문자로 바꾸기. 변환한 문자를 원래 문자열의 같은 위치에 저장

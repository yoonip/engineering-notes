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
    for (char& c : my_string) c = tolower(static_cast<unsigned char>(c));
    sort(my_string.begin(), my_string.end());
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
// string solution(string my_string) {  // 문자열 정렬하기 (2) 풀이 시작
//     for (char& c : my_string) c = tolower(static_cast<unsigned char>(c));  // 모든 영문자를 소문자로 통일
//     sort(my_string.begin(), my_string.end());  // my_string를 오름차순 정렬
//     return my_string;  // 소문자로 바꿔 정렬한 문자열
// }  // 블록 끝

// 풀이 요약
// 소문자로 통일한 후 각 문자를 정렬해 다시 연결

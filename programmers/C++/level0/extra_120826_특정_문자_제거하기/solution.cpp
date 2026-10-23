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

string solution(string my_string, string letter) {
    my_string.erase(remove(my_string.begin(), my_string.end(), letter[0]), my_string.end());
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
// string solution(string my_string, string letter) {  // 특정 문자 제거하기 풀이 시작
//     my_string.erase(remove(my_string.begin(), my_string.end(), letter[0]), my_string.end());  // remove로 남길 문자를 앞으로 모은 뒤 erase로 제거 대상 구간을 지우기
//     return my_string;  // 지정한 문자를 모두 지운 문자열
// }  // 블록 끝

// 풀이 요약
// 대소문자를 구분하여 지정 문자만 모두 제거

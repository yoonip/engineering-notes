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

string solution(string rsp) {
    for (char& c : rsp) c = c == '2' ? '0' : c == '0' ? '5' : '2';
    return rsp;
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
// string solution(string rsp) {  // 가위 바위 보 풀이 시작
//     for (char& c : rsp) c = c == '2' ? '0' : c == '0' ? '5' : '2';  // 가위 2에는 바위 0, 바위 0에는 보 5, 보 5에는 가위 2
//     return rsp;  // 각 손에 이기는 손으로 바꾼 문자열
// }  // 블록 끝

// 풀이 요약
// 상대의 각 손에 이기는 가위·바위·보 기호로 바꾸기

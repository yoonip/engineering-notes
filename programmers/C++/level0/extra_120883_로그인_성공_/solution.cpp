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

string solution(vector<string> id_pw, vector<vector<string>> db) {
    for (const auto& member : db)
        if (member[0] == id_pw[0]) return member[1] == id_pw[1] ? "login" : "wrong pw";
    return "fail";
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
// string solution(vector<string> id_pw, vector<vector<string>> db) {  // 로그인 성공? 풀이 시작
//     for (const auto& member : db)  // 기록된 회원 중 같은 아이디 찾기
//         if (member[0] == id_pw[0]) return member[1] == id_pw[1] ? "login" : "wrong pw";  // 아이디가 같은 회원은 비밀번호도 같으면 login, 다르면 wrong pw 반환
//     return "fail";  // 일치하는 아이디가 없어서 로그인 실패
// }  // 블록 끝

// 풀이 요약
// 코딩 문제의 입력 데이터에서 아이디 존재 여부를 먼저 확인하고 비밀번호를 비교

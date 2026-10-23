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

string solution(string polynomial) {
    istringstream input(polynomial);
    string term;
    int coefficient = 0, constant = 0;
    while (input >> term) {
        if (term == "+") continue;
        if (term.back() == 'x') coefficient += term == "x" ? 1 : stoi(term.substr(0, term.size() - 1));
        else constant += stoi(term);
    }
    string answer;
    if (coefficient) answer = (coefficient == 1 ? string("") : to_string(coefficient)) + "x";
    if (constant) answer += (answer.empty() ? "" : " + ") + to_string(constant);
    return answer.empty() ? "0" : answer;
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
// string solution(string polynomial) {  // 다항식 더하기 풀이 시작
//     istringstream input(polynomial);  // polynomial를 공백 단위로 읽을 스트림 input
//     string term;  // string 변수 term에 매번 읽은 항 또는 더하기 기호를 저장
//     int coefficient = 0, constant = 0;  // int 변수 coefficient에는 x의 계수 합을, constant에는 상수항의 합을 저장하며 둘 다 0에서 시작
//     while (input >> term) {  // 스트림 추출 연산자 >>로 term을 읽을 수 있는 동안 모든 항과 기호를 순서대로 처리
//         if (term == "+") continue;  // term이 더하기 기호이면 continue로 계산을 건너뛰고 다음 항을 읽기
//         if (term.back() == 'x') coefficient += term == "x" ? 1 : stoi(term.substr(0, term.size() - 1));  // 마지막 문자가 x이면 x항임. x만 있으면 계수 1을, 그 외에는 substr로 x를 뗀 뒤 stoi로 변환한 계수를 coefficient에 더하기
//         else constant += stoi(term);  // x로 끝나지 않는 항은 stoi로 정수로 바꾸어 상수의 합 constant에 더하기
//     }  // 블록 끝
//     string answer;  // 동류항을 합친 다항식을 조립할 빈 문자열 answer를 준비
//     if (coefficient) answer = (coefficient == 1 ? string("") : to_string(coefficient)) + "x";  // coefficient가 0이 아니면 x항을 만들기. 삼항 연산자로 계수 1은 생략하고 다른 계수만 문자열로 붙이기
//     if (constant) answer += (answer.empty() ? "" : " + ") + to_string(constant);  // constant가 0이 아니면 상수항을 붙이기. answer가 비어 있지 않을 때만 앞에 더하기 기호와 공백을 넣기
//     return answer.empty() ? "0" : answer;  // 삼항 연산자로 answer가 비어 있으면 0을 나타내는 문자열을, 아니면 조립한 다항식을 반환
// }  // 블록 끝

// 풀이 요약
// 공백으로 구분된 항을 읽어 x의 계수와 상수를 각각 합. x항을 먼저 만들고 상수항을 이어 붙이며, 계수 1과 불필요한 더하기 기호는 생략

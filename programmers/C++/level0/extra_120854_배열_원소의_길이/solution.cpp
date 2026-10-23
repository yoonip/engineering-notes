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

vector<int> solution(vector<string> strlist) {
    vector<int> answer;
    for (const string& s : strlist) answer.push_back(s.size());
    return answer;
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
// vector<int> solution(vector<string> strlist) {  // 배열 원소의 길이 풀이 시작
//     vector<int> answer;  // 입력 순서에 맞춘 문자열 길이
//     for (const string& s : strlist) answer.push_back(s.size());  // 각 문자열의 길이를 같은 순서로 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자열의 길이를 입력 순서대로 반환

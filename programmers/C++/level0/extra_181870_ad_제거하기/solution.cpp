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

vector<string> solution(vector<string> strArr) {
    vector<string> answer;
    for (const string& text : strArr) if (text.find("ad") == string::npos) answer.push_back(text);
    return answer;
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
// vector<string> solution(vector<string> strArr) {  // ad 제거하기 풀이 시작
//     vector<string> answer;  // ad가 없는 문자열만 남길 배열
//     for (const string& text : strArr) if (text.find("ad") == string::npos) answer.push_back(text);  // ad를 찾지 못한 문자열만 원래 순서대로 남기기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// ad가 포함되지 않은 문자열만 순서를 유지해 남기기

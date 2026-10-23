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

string solution(string myString) {
    for (char& c : myString) { c = tolower((unsigned char)c); if (c == 'a') c = 'A'; }
    return myString;
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
// string solution(string myString) {  // A 강조하기 풀이 시작
//     for (char& c : myString) { c = tolower((unsigned char)c); if (c == 'a') c = 'A'; }  // 먼저 소문자로 통일한 뒤 a만 A로 강조
//     return myString;  // A를 제외한 영문자가 소문자인 결과
// }  // 블록 끝

// 풀이 요약
// 모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됨

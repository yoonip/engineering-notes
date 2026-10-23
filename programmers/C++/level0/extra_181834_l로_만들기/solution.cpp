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
    for (char& c : myString) c = max(c, 'l');
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
// string solution(string myString) {  // l로 만들기 풀이 시작
//     for (char& c : myString) c = max(c, 'l');  // l보다 앞선 알파벳만 l로 바꾸고 나머지는 유지
//     return myString;  // 모든 문자가 l 이상인 문자열
// }  // 블록 끝

// 풀이 요약
// 각 문자를 l과 비교해 더 큰 쪽을 선택

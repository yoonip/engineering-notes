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

string solution(string myString, string pat) {
    return myString.substr(0, myString.rfind(pat) + pat.size());
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
// string solution(string myString, string pat) {  // 특정 문자열로 끝나는 가장 긴 부분 문자열 찾기 풀이 시작
//     return myString.substr(0, myString.rfind(pat) + pat.size());  // 검색 결과가 존재하는지 비교해 참이면 1, 거짓이면 0을 반환
// }  // 블록 끝

// 풀이 요약
// 가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열임

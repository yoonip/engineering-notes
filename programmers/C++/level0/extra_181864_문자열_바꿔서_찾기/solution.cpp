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

int solution(string myString, string pat) {
    for (char& c : myString) c = c == 'A' ? 'B' : 'A';
    return myString.find(pat) != string::npos;
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
// int solution(string myString, string pat) {  // 문자열 바꿔서 찾기 풀이 시작
//     for (char& c : myString) c = c == 'A' ? 'B' : 'A';  // 각 위치에서 A와 B를 한 번씩 서로 교환
//     return myString.find(pat) != string::npos;  // 검색 결과가 존재하는지 비교해 참이면 1, 거짓이면 0을 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자를 한 번만 읽고 A↔B로 바꾸면 이미 치환한 문자를 다시 바꾸는 일이 없음

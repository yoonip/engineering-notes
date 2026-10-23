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
    int count = 0;
    for (size_t pos = myString.find(pat); pos != string::npos; pos = myString.find(pat, pos + 1)) ++count;
    return count;
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
// int solution(string myString, string pat) {  // 문자열이 몇 번 등장하는지 세기 풀이 시작
//     int count = 0;  // 패턴이 등장한 시작 위치의 수
//     for (size_t pos = myString.find(pat); pos != string::npos; pos = myString.find(pat, pos + 1)) ++count;  // 발견 위치의 한 칸 뒤부터 다시 찾아 겹치는 등장도 포함
//     return count;  // 조건을 만족한 횟수 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 세기

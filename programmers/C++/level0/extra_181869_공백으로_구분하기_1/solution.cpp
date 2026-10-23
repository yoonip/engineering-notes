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

vector<string> solution(string my_string) {
    istringstream stream(my_string);
    vector<string> answer;
    string word;
    while (stream >> word) answer.push_back(word);
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
// vector<string> solution(string my_string) {  // 공백으로 구분하기 1 풀이 시작
//     istringstream stream(my_string);  // my_string를 공백 단위로 읽을 스트림 stream
//     vector<string> answer;  // 공백으로 나눈 단어 목록
//     string word;  // 스트림에서 방금 읽은 단어
//     while (stream >> word) answer.push_back(word);  // 공백을 건너뛰며 단어를 읽어 순서대로 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 공백을 기준으로 단어들을 나누기

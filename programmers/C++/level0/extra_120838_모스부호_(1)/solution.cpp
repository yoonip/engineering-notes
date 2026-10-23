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

string solution(string letter) {
    vector<string> morse = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};
    istringstream input(letter);
    string token, answer;
    while (input >> token) answer += char('a' + (find(morse.begin(), morse.end(), token) - morse.begin()));
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
// string solution(string letter) {  // 모스부호 (1) 풀이 시작
//     vector<string> morse = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};  // vector<string> morse에 a부터 z까지의 부호를 순서대로 저장하여 배열 인덱스가 알파벳 순서가 되게 저장
//     istringstream input(letter);  // letter를 공백 단위로 읽을 스트림 input
//     string token, answer;  // string 변수 token에는 현재 부호를, 빈 문자열 answer에는 해독한 문자들을 저장
//     while (input >> token) answer += char('a' + (find(morse.begin(), morse.end(), token) - morse.begin()));  // 부호를 읽을 때마다 find로 표에서 위치를 찾기. begin과의 차이인 인덱스를 문자 a에 더하고 char로 변환해 answer 뒤에 붙이기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 알파벳 a부터 z까지의 모스부호를 순서대로 저장. 공백으로 분리한 부호를 표에서 찾아 그 인덱스에 해당하는 소문자를 결과에 붙이기

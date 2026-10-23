#include <string>
#include <vector>
using namespace std;

string solution(vector<string> arr) {
    string answer;
    for (const string& text : arr) answer += text;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<string> arr) {  // 문자 리스트를 문자열로 변환하기 풀이 시작
//     string answer;  // 입력 원소들을 순서대로 이어 붙일 문자열
//     for (const string& text : arr) answer += text;  // 범위 for에서 각 문자열을 const 참조로 읽고 +=로 순서대로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열 배열의 원소를 입력 순서대로 연결

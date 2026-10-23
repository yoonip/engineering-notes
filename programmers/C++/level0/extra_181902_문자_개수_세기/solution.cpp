#include <string>
#include <vector>
using namespace std;

vector<int> solution(string my_string) {
    vector<int> answer(52, 0);
    for (char c : my_string) ++answer[c >= 'A' && c <= 'Z' ? c - 'A' : c - 'a' + 26];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(string my_string) {  // 문자 개수 세기 풀이 시작
//     vector<int> answer(52, 0);  // 대문자와 소문자 각각 26개의 개수를 저장할 vector를 0으로 초기화
//     for (char c : my_string) ++answer[c >= 'A' && c <= 'Z' ? c - 'A' : c - 'a' + 26];  // 범위 for와 삼항 연산자로 각 문자를 대소문자 인덱스로 바꾸고 ++로 개수를 늘립니다
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 대문자 26개와 소문자 26개에 서로 다른 인덱스를 배정해 개수를 세기

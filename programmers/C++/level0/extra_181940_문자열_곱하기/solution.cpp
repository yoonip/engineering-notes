#include <string>
using namespace std;

string solution(string my_string, int k) {
    string answer;
    for (int i = 0; i < k; ++i) answer += my_string;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int k) {  // 문자열 곱하기 풀이 시작
//     string answer;  // 원본을 k번 이어 붙일 문자열
//     for (int i = 0; i < k; ++i) answer += my_string;  // for로 k번 반복하고 +=로 원본 문자열을 결과 뒤에 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 문자열을 k번 순서대로 이어 붙이기

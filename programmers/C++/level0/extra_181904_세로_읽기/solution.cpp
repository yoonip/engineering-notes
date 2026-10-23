#include <string>
using namespace std;

string solution(string my_string, int m, int c) {
    string answer;
    for (size_t i = c - 1; i < my_string.size(); i += m) answer += my_string[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int m, int c) {  // 세로 읽기 풀이 시작
//     string answer;  // 지정된 열의 문자를 위에서 아래로 모을 결과
//     for (size_t i = c - 1; i < my_string.size(); i += m) answer += my_string[i];  // 열을 0부터 시작하는 위치로 바꾸고 for에서 m씩 이동하며 같은 열의 문자를 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 열 번호를 0부터 시작하는 인덱스로 바꾸고 m칸 간격의 문자를 읽기

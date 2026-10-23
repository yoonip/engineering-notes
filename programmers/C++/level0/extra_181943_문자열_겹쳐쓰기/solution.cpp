#include <string>
using namespace std;

string solution(string my_string, string overwrite_string, int s) {
    my_string.replace(s, overwrite_string.size(), overwrite_string);
    return my_string;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, string overwrite_string, int s) {  // 문자열 겹쳐쓰기 풀이 시작
//     my_string.replace(s, overwrite_string.size(), overwrite_string);  // replace로 위치 s부터 새 문자열 길이만큼 덮어씁니다
//     return my_string;  // return으로 교체를 마친 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 시작 위치 s부터 덮어쓸 문자열 길이만큼 교체

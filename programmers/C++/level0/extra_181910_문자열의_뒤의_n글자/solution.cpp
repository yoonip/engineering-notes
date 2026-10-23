#include <string>
using namespace std;

string solution(string my_string, int n) {
    return my_string.substr(my_string.size() - n);
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int n) {  // 문자열의 뒤의 n글자 풀이 시작
//     return my_string.substr(my_string.size() - n);  // size에서 n을 뺀 위치부터 끝까지 substr로 추출해 반환
// }  // 블록 끝

// 풀이 요약
// 뒤에서 n번째 위치부터 끝까지 반환

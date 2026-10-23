#include <string>
using namespace std;

string solution(string my_string, int n) {
    return my_string.substr(0, n);
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int n) {  // 문자열의 앞의 n글자 풀이 시작
//     return my_string.substr(0, n);  // substr의 시작 위치와 길이 인자로 앞 n글자를 추출해 반환
// }  // 블록 끝

// 풀이 요약
// 문자열의 앞 n글자를 복사해 반환

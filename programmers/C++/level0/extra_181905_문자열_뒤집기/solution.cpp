#include <algorithm>
#include <string>
using namespace std;

string solution(string my_string, int s, int e) {
    reverse(my_string.begin() + s, my_string.begin() + e + 1);
    return my_string;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int s, int e) {  // 문자열 뒤집기 풀이 시작
//     reverse(my_string.begin() + s, my_string.begin() + e + 1);  // 반복자로 반열린 구간 [s, e+1)을 지정하여 인덱스 s부터 e까지의 문자를 reverse로 뒤집습니다.
//     return my_string;  // return으로 구간 변경을 마친 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 양 끝을 포함한 s부터 e 구간만 뒤집기

#include <string>
using namespace std;

int solution(string my_string, string is_prefix) {
    return my_string.compare(0, is_prefix.size(), is_prefix) == 0;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string my_string, string is_prefix) {  // 접두사인지 확인하기 풀이 시작
//     return my_string.compare(0, is_prefix.size(), is_prefix) == 0;  // compare로 원본 앞부분과 접두사 후보를 비교해 같으면 1을 반환
// }  // 블록 끝

// 풀이 요약
// 원본의 시작 부분과 접두사 후보를 비교

#include <string>
using namespace std;

int solution(string my_string, string is_suffix) {
    return my_string.size() >= is_suffix.size() && my_string.compare(my_string.size() - is_suffix.size(), is_suffix.size(), is_suffix) == 0;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string my_string, string is_suffix) {  // 접미사인지 확인하기 풀이 시작
//     return my_string.size() >= is_suffix.size() && my_string.compare(my_string.size() - is_suffix.size(), is_suffix.size(), is_suffix) == 0;  // &&로 길이를 먼저 확인한 뒤 compare로 끝부분이 접미사 후보와 같은지 비교
// }  // 블록 끝

// 풀이 요약
// 후보가 원본보다 길지 않은지 확인하고 끝부분을 비교

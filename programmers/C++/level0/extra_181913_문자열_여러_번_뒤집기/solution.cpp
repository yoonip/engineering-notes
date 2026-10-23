#include <algorithm>
#include <string>
#include <vector>
using namespace std;

string solution(string my_string, vector<vector<int>> queries) {
    for (const auto& query : queries) reverse(my_string.begin() + query[0], my_string.begin() + query[1] + 1);
    return my_string;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, vector<vector<int>> queries) {  // 문자열 여러 번 뒤집기 풀이 시작
//     for (const auto& query : queries) reverse(my_string.begin() + query[0], my_string.begin() + query[1] + 1);  // 범위 for로 쿼리를 const 참조로 읽고 reverse로 양 끝을 포함하는 범위를 뒤집기
//     return my_string;  // return으로 구간 변경을 마친 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 쿼리 순서대로 각 구간의 양 끝 문자를 교환하며 뒤집기

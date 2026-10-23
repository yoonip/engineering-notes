#include <algorithm>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(string my_string) {
    vector<string> answer;
    for (size_t i = 0; i < my_string.size(); ++i) answer.push_back(my_string.substr(i));
    sort(answer.begin(), answer.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<string> solution(string my_string) {  // 접미사 배열 풀이 시작
//     vector<string> answer;  // 접미사 문자열을 담을 빈 vector를 선언
//     for (size_t i = 0; i < my_string.size(); ++i) answer.push_back(my_string.substr(i));  // for로 모든 시작 인덱스를 순회하고 substr로 만든 접미사를 push_back으로 저장
//     sort(answer.begin(), answer.end());  // begin과 end로 전체 범위를 지정하고 sort로 접미사를 사전순 정렬
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 위치에서 시작하는 접미사를 모두 만들고 사전순으로 정렬

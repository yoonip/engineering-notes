#include <string>
#include <vector>
using namespace std;

string solution(vector<string> my_strings, vector<vector<int>> parts) {
    string answer;
    for (size_t i = 0; i < my_strings.size(); ++i) answer += my_strings[i].substr(parts[i][0], parts[i][1] - parts[i][0] + 1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<string> my_strings, vector<vector<int>> parts) {  // 부분 문자열 이어 붙여 문자열 만들기 풀이 시작
//     string answer;  // 각 부분 구간을 이어 붙일 결과
//     for (size_t i = 0; i < my_strings.size(); ++i) answer += my_strings[i].substr(parts[i][0], parts[i][1] - parts[i][0] + 1);  // for로 문자열을 순회하며 substr에 시작 위치와 포함 길이를 전달해 부분 문자열을 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자열에서 양 끝을 포함하는 부분 구간을 추출해 이어 붙이기

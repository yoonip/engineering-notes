#include <string>
#include <vector>
using namespace std;

string solution(string my_string, vector<int> indices) {
    vector<bool> removed(my_string.size(), false);
    for (int index : indices) removed[index] = true;
    string answer;
    for (size_t i = 0; i < my_string.size(); ++i) if (!removed[i]) answer += my_string[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, vector<int> indices) {  // 글자 지우기 풀이 시작
//     vector<bool> removed(my_string.size(), false);  // 문자열 길이만큼의 삭제 표시를 false로 초기화
//     for (int index : indices) removed[index] = true;  // 범위 for로 삭제할 인덱스를 읽고 해당 표시를 true로 바꾸기
//     string answer;  // 삭제 표시가 없는 문자만 모을 결과
//     for (size_t i = 0; i < my_string.size(); ++i) if (!removed[i]) answer += my_string[i];  // for로 문자를 순회하고 !로 삭제 표시가 없는 문자만 골라 +=로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 지울 인덱스를 표시한 뒤 남은 문자를 원래 순서대로 연결

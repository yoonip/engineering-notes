#include <string>
#include <vector>
using namespace std;

string solution(string my_string, vector<int> index_list) {
    string answer;
    for (int index : index_list) answer += my_string[index];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, vector<int> index_list) {  // 글자 이어 붙여 문자열 만들기 풀이 시작
//     string answer;  // 주어진 인덱스 순서대로 선택한 문자
//     for (int index : index_list) answer += my_string[index];  // 범위 for로 인덱스를 읽고 []로 선택한 문자를 +=로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 주어진 인덱스 순서대로 원본 문자를 연결

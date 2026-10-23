#include <string>
#include <vector>
using namespace std;

vector<int> solution(vector<string> intStrs, int k, int s, int l) {
    vector<int> answer;
    for (const string& text : intStrs) {
        int value = stoi(text.substr(s, l));
        if (value > k) answer.push_back(value);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<string> intStrs, int k, int s, int l) {  // 배열 만들기 5 풀이 시작
//     vector<int> answer;  // 부분 문자열을 정수로 바꾼 뒤 k보다 큰 값
//     for (const string& text : intStrs) {  // 범위 for에서 각 숫자 문자열을 const 참조로 읽기
//         int value = stoi(text.substr(s, l));  // substr로 s부터 l글자를 추출하고 stoi로 정수로 변환
//         if (value > k) answer.push_back(value);  // >로 기준을 초과하는지 검사하고 push_back으로 결과에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작 위치 s에서 l글자를 정수로 읽고 k보다 큰 값만 저장

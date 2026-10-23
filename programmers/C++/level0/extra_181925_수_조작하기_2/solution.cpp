#include <string>
#include <vector>
using namespace std;

string solution(vector<int> numLog) {
    string answer;
    for (size_t i = 1; i < numLog.size(); ++i) {
        int delta = numLog[i] - numLog[i - 1];
        answer += delta == 1 ? 'w' : delta == -1 ? 's' : delta == 10 ? 'd' : 'a';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<int> numLog) {  // 수 조작하기 2 풀이 시작
//     string answer;  // 기록 차이에 맞는 조작 문자를 모을 결과
//     for (size_t i = 1; i < numLog.size(); ++i) {  // for를 두 번째 원소부터 시작해 직전 기록과의 차이를 계산
//         int delta = numLog[i] - numLog[i - 1];  // []로 인접 기록을 읽어 두 값의 변화량을 구하기
//         answer += delta == 1 ? 'w' : delta == -1 ? 's' : delta == 10 ? 'd' : 'a';  // 중첩 삼항 연산자로 변화량에 맞는 문자를 고르고 +=로 결과에 붙이기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 인접한 기록의 차이를 조작 문자 w, s, d, a로 바꾸어 연결

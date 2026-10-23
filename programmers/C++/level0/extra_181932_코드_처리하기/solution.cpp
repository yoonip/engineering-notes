#include <string>
using namespace std;

string solution(string code) {
    string answer;
    int mode = 0;
    for (size_t i = 0; i < code.size(); ++i) {
        if (code[i] == '1') mode = 1 - mode;
        else if ((int)(i % 2) == mode) answer += code[i];
    }
    return answer.empty() ? "EMPTY" : answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string code) {  // 코드 처리하기 풀이 시작
//     string answer;  // 현재 모드와 홀짝이 맞는 문자만 모을 결과
//     int mode = 0;  // 문자 선택 규칙을 나타내는 모드를 0으로 초기화
//     for (size_t i = 0; i < code.size(); ++i) {  // size_t형 인덱스를 for로 증가시키며 각 위치를 차례로 처리
//         if (code[i] == '1') mode = 1 - mode;  // if로 모드 변경 문자를 검사하고 1에서 현재 값을 빼 0과 1을 전환
//         else if ((int)(i % 2) == mode) answer += code[i];  // %로 인덱스의 홀짝을 구해 모드와 같으면 +=로 문자를 연결
//     }  // 블록 끝
//     return answer.empty() ? "EMPTY" : answer;  // empty와 삼항 연산자 ?:로 결과가 비었으면 EMPTY 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 문자 1은 모드를 바꾸고, 나머지는 모드와 인덱스 홀짝이 같을 때만 연결

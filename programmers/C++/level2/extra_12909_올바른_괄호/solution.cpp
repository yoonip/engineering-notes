#include <string>
using namespace std;

bool solution(string s) {
    int balance = 0;
    for (char c : s) {
        balance += c == '(' ? 1 : -1;
        if (balance < 0) return false;
    }
    return balance == 0;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// bool solution(string s) {  // 괄호 균형이 음수가 되지 않고 0으로 끝나는지 확인
// int balance = 0;  // 아직 닫히지 않은 여는 괄호 수 저장
// for (char c : s) {  // 괄호를 왼쪽부터 검사
// balance += c == '(' ? 1 : -1;  // 괄호 종류에 따라 잔여 수를 늘리거나 줄이기
// if (balance < 0) return false;  // 여는 괄호 없이 닫히면 올바르지 않음
// }  // 블록 끝
// return balance == 0;  // 모든 여는 괄호가 닫혔는지 확인
// }  // 블록 끝

// 풀이 요약
// 여는 괄호 수에서 닫는 괄호 수를 뺀 값이 중간에 음수가 되지 않고 마지막에 0인지 확인

#include <string>
using namespace std;

string solution(string number, int k) {
    string stack;
    for (char digit : number) {
        while (k > 0 && !stack.empty() && stack.back() < digit) { stack.pop_back(); --k; }
        stack.push_back(digit);
    }
    if (k > 0) stack.resize(stack.size() - k);
    return stack;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(string number, int k) {  // 작은 앞자리를 지워 남는 수 최대화
// string stack;  // 큰 자릿수부터 유지할 숫자를 스택처럼 저장
// for (char digit : number) {  // 숫자를 왼쪽부터 읽기
// while (k > 0 && !stack.empty() && stack.back() < digit) { stack.pop_back(); --k; }  // 더 큰 숫자를 앞으로 보내도록 작은 끝 숫자 제거
// stack.push_back(digit);  // 현재 숫자를 뒤에 넣기
// }  // 블록 끝
// if (k > 0) stack.resize(stack.size() - k);  // 제거 횟수가 남으면 작은 뒤쪽 자릿수 지우기
// return stack;  // 만들 수 있는 가장 큰 수 반환
// }  // 블록 끝

// 풀이 요약
// 새 자릿수보다 작은 스택 끝 숫자를 제거해 큰 자릿수가 앞에 오게 만들고 남은 제거 횟수는 뒤에서 사용

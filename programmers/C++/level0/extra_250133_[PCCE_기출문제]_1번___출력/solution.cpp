#include <iostream>

using namespace std;

int main(void) {
    string msg = "Spring is beginning";
    int val1 = 3;
    string val2 = "3";

    cout << msg << endl;
    cout << val1 + 10 << endl;
    cout << val2 + "10" << endl;

    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     string msg = "Spring is beginning";  // 첫 줄에 출력할 문장
//     int val1 = 3;  // 덧셈할 정수 3
//     string val2 = "3";  // 다른 문자열과 이어 붙일 문자 3
//
//     cout << msg << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     cout << val1 + 10 << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     cout << val2 + "10" << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열은 이어 붙이고 정수는 덧셈. 첫 줄 문장, 정수 13, 문자열 310을 차례대로 출력

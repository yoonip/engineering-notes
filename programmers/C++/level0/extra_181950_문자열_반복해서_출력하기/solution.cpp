#include <iostream>
#include <string>
using namespace std;
int main() {
    string text;
    int n;
    cin >> text >> n;
    for (int i = 0; i < n; ++i) cout << text;
    cout << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     string text;  // 입력 문자열을 저장할 변수를 선언
//     int n;  // 반복 횟수를 저장할 int형 변수를 선언
//     cin >> text >> n;  // 입력 연산자 >>로 문자열과 정수를 읽기
//     for (int i = 0; i < n; ++i) cout << text;  // for로 n번 반복하며 <<로 문자열을 이어 출력
//     cout << '\n';  // 마지막에 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열을 n번 출력하고 마지막에 줄을 바꾸기

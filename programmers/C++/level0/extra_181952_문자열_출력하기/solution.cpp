#include <iostream>
#include <string>
using namespace std;
int main() {
    string text;
    cin >> text;
    cout << text << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     string text;  // 입력 문자열을 저장할 string형 변수를 선언
//     cin >> text;  // 입력 연산자 >>로 문자열을 읽기
//     cout << text << '\n';  // 출력 연산자 <<로 입력 문자열과 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 문자열을 그대로 출력

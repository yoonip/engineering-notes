#include <iostream>
#include <string>
using namespace std;
int main() {
    string first, second;
    cin >> first >> second;
    cout << first << second << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     string first, second;  // 입력 문자열 두 개를 저장할 변수를 선언
//     cin >> first >> second;  // 공백으로 구분된 문자열 두 개를 >>로 읽기
//     cout << first << second << '\n';  // 출력 연산자 <<로 두 문자열을 공백 없이 붙이고 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 공백으로 구분한 두 문자열을 붙여 출력

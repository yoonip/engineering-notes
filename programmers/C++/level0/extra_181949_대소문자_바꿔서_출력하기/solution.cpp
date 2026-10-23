#include <cctype>
#include <iostream>
#include <string>
using namespace std;
int main() {
    string text;
    cin >> text;
    for (unsigned char c : text) {
        cout << static_cast<char>(islower(c) ? toupper(c) : tolower(c));
    }
    cout << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     string text;  // 입력 문자열을 저장할 변수를 선언
//     cin >> text;  // 입력 연산자 >>로 문자열을 읽기
//     for (unsigned char c : text) {  // 범위 for에서 문자 분류 함수에 안전한 unsigned char형으로 각 문자를 읽기
//         cout << static_cast<char>(islower(c) ? toupper(c) : tolower(c));  // 삼항 연산자로 대소문자 변환을 고르고 static_cast로 문자형으로 바꾸어 출력
//     }  // 블록 끝
//     cout << '\n';  // 문자열 출력 뒤 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 각 문자가 소문자이면 대문자로, 대문자이면 소문자로 바꾸기

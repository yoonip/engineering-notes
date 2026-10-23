#include <iostream>
#include <string>
using namespace std;
int main(void) {
    string message = "Let's go!";
    cout << "3\n2\n1" << endl;
    cout << message << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     string message = "Let's go!";  // 큰따옴표 문자열 안에 작은따옴표를 포함한 출력 문장을 저장
//     cout << "3\n2\n1" << endl;  // <<로 숫자를 출력하며 문자열의 \n마다 줄을 바꾸기
//     cout << message << endl;  // 저장한 문장을 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 줄바꿈 문자를 넣어 숫자를 각각 한 줄씩 출력한 뒤 저장한 문장을 출력

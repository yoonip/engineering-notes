#include <iostream>
using namespace std;
int main() {
    cout << "!@#$%^&*(\\'\"<>?:;" << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     cout << "!@#$%^&*(\\'\"<>?:;" << '\n';  // 역슬래시와 큰따옴표를 이스케이프한 문자열을 <<로 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 역슬래시와 큰따옴표를 이스케이프해 지정된 특수문자를 출력

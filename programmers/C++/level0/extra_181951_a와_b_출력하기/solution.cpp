#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << "a = " << a << '\n';
    cout << "b = " << b << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 입력 정수 두 개를 담을 변수를 선언
//     cin >> a >> b;  // 입력 연산자 >>로 정수 두 개를 읽기
//     cout << "a = " << a << '\n';  // <<로 첫 변수의 이름과 값을 출력하고 줄을 바꾸기
//     cout << "b = " << b << '\n';  // <<로 두 번째 변수의 이름과 값을 출력하고 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 두 정수를 변수 이름과 함께 각각 출력

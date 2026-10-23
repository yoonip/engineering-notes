#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a << " + " << b << " = " << a + b << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 입력 정수 두 개를 담을 변수를 선언
//     cin >> a >> b;  // 입력 연산자 >>로 정수 두 개를 읽기
//     cout << a << " + " << b << " = " << a + b << '\n';  // <<로 두 정수와 합계를 공백 및 기호와 함께 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 덧셈을 계산하고 요구된 공백과 기호를 포함해 출력

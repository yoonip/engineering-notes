#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    cout << n << " is " << (n % 2 == 0 ? "even" : "odd") << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     int n;  // 입력받을 정수를 저장할 int형 변수를 선언
//     cin >> n;  // 입력 연산자 >>로 정수 n을 읽기
//     cout << n << " is " << (n % 2 == 0 ? "even" : "odd") << '\n';  // 나머지 연산자 %와 삼항 연산자 ?:로 홀짝을 구분하고 <<로 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 2로 나눈 나머지에 따라 짝수와 홀수 출력 형식을 선택

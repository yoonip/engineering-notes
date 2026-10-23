#include <iostream>

using namespace std;

int main(void) {
    int a;
    int c;
    cin >> a >> c;
    
    int b_square = c * c - a * a;
    cout << b_square << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int a;  // 직각을 끼는 주어진 변의 길이
//     int c;  // 주어진 빗변의 길이
//     cin >> a >> c;  // cin과 >>로 표준 입력의 값을 순서대로 읽기
//
//     int b_square = c * c - a * a;  // 빗변 제곱에서 알려진 변의 제곱을 빼 나머지 변의 제곱 구하기
//     cout << b_square << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 피타고라스 정리의 b² = c² - a²를 계산

#include <iostream>

using namespace std;

int main(void) {
    int angle1;
    int angle2;
    cin >> angle1 >> angle2;
    
    int sum_angle = (angle1 + angle2) % 360;
    cout << sum_angle << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int angle1;  // 입력 각도를 저장할 int 변수를 선언
//     int angle2;  // 입력 각도를 저장할 int 변수를 선언
//     cin >> angle1 >> angle2;  // 입력 연산자 >>로 표준 입력의 값을 변수에 저장
//
//     int sum_angle = (angle1 + angle2) % 360;  // 두 각도의 합을 360으로 나눈 나머지로 0 이상 360 미만의 각도를 구하기
//     cout << sum_angle << endl;  // 계산한 각도를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 각도 합을 360으로 나눈 나머지는 0 이상 360 미만이며 원래 각도와 같은 방향을 나타냅니다

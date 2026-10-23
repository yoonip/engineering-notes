#include <iostream>

using namespace std;

int main(void) {
    int start;
    int before;
    int after;
    cin >> start >> before >> after;

    int money = start;
    int month = 1;

    while (money < 70) {
        money += before;
        month++;
    }
    while (money < 100) {
        money += after;
        month++;
    }
    cout << month << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int start;  // 첫 달에 모은 금액
//     int before;  // 70만 원에 도달하기 전 매달 저축할 금액
//     int after;  // 70만 원부터 매달 저축할 금액
//     cin >> start >> before >> after;  // cin과 >>로 표준 입력의 값을 순서대로 읽기
//
//     int money = start;  // 첫 달의 저축액을 현재 잔액으로 설정
//     int month = 1;  // 첫 달 저축이 이미 반영되어 있으니 1개월
//
//     while (money < 70) {  // 잔액이 70만 원보다 작을 때의 저축
//         money += before;  // 초기 월 저축액을 잔액에 추가
//         month++;  // 저축한 달 하나 추가
//     }  // 블록 끝
//     while (money < 100) {  // 월 저축액을 바꾼 뒤 100만 원까지 모으기
//         money += after;  // 변경된 월 저축액을 잔액에 추가
//         month++;  // 저축한 달 하나 추가
//     }  // 블록 끝
//     cout << month << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 첫 달의 금액으로 시작. 70만 원 미만일 때 before를 더하고 그 이후에는 after를 더해 100만 원에 도달한 개월 수를 세기

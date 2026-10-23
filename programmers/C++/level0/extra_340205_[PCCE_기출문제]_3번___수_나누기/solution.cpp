#include <iostream>

using namespace std;

int main(void) {
    int number;
    cin >> number;
    
    int answer = 0;
    
    while(number > 0){
        answer += number % 100;
        number /= 100;
    }
    cout << answer << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int number;  // 두 자리씩 나눌 입력 정수를 저장할 변수를 선언
//     cin >> number;  // 입력 연산자 >>로 표준 입력의 값을 변수에 저장
//
//     int answer = 0;  // 잘라낸 수들의 합계를 0으로 초기화
//
//     while(number > 0){  // while문으로 처리할 자릿수가 남아 있는 동안 반복
//         answer += number % 100;  // %로 얻은 마지막 두 자리 값을 +=로 합계에 더하기
//         number /= 100;  // 정수 나눗셈으로 이미 더한 마지막 두 자리를 제거
//     }  // 블록 끝
//     cout << answer << endl;  // 두 자리씩 잘라 더한 합계와 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 100으로 나눈 나머지로 마지막 두 자리를 얻어 더하고, 100으로 나누어 자릿수를 줄이는 작업을 반복

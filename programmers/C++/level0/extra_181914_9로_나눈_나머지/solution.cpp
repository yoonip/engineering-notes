#include <string>
using namespace std;

int solution(string number) {
    int answer = 0;
    for (char c : number) answer = (answer + c - '0') % 9;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string number) {  // 9로 나눈 나머지 풀이 시작
//     int answer = 0;  // 정수형 결과 누적값을 0으로 초기화
//     for (char c : number) answer = (answer + c - '0') % 9;  // 범위 for로 각 숫자 문자를 정수로 바꾸어 더하고 % 9로 나머지를 유지
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 자리 숫자를 더하고 9로 나눈 나머지를 유지

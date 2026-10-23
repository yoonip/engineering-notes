#include <algorithm>
#include <string>
using namespace std;

string solution(int n) {
    string digits = "124", answer;
    while (n > 0) {
        --n; answer += digits[n % 3]; n /= 3;
    }
    reverse(answer.begin(), answer.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(int n) {  // 0 없는 세 자리 기호로 자릿수 변환
// string digits = "124", answer;  // 세 진법 자릿수 문자와 결과 저장
// while (n > 0) {  // 0이 없는 세 자리 체계의 낮은 자릿수부터 구하기
// --n; answer += digits[n % 3]; n /= 3;  // 1을 빼 0부터 시작하는 나머지로 자릿수 선택
// }  // 블록 끝
// reverse(answer.begin(), answer.end());  // 높은 자릿수가 앞에 오도록 뒤집기
// return answer;  // 124 나라의 숫자 반환
// }  // 블록 끝

// 풀이 요약
// 현재 수에서 1을 뺀 나머지를 1, 2, 4 중 하나로 바꾸고 몫을 반복해 자릿수 만들기

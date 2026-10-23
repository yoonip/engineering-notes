#include <vector>
using namespace std;

int solution(vector<int> num_list) {
    int odd = 0, even = 0;
    for (int value : num_list) {
        if (value % 2) odd = odd * 10 + value;
        else even = even * 10 + value;
    }
    return odd + even;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> num_list) {  // 이어 붙인 수 풀이 시작
//     int odd = 0, even = 0;  // 홀수와 짝수를 이어 붙인 결과를 각각 0으로 초기화
//     for (int value : num_list) {  // 범위 for로 정수 목록의 각 원소를 읽기
//         if (value % 2) odd = odd * 10 + value;  // 나머지 연산자 %로 홀수를 골라 기존 수를 10배 한 뒤 마지막 자릿수로 붙이기
//         else even = even * 10 + value;  // else에서 짝수를 골라 기존 수를 10배 한 뒤 마지막 자릿수로 붙이기
//     }  // 블록 끝
//     return odd + even;  // 홀수끼리 연결한 수와 짝수끼리 연결한 수의 합을 반환
// }  // 블록 끝

// 풀이 요약
// 홀수와 짝수를 각각 원래 순서대로 이어 붙인 정수 두 개를 더하기

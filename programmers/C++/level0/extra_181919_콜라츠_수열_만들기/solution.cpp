#include <vector>
using namespace std;

vector<int> solution(int n) {
    vector<int> answer{n};
    while (n != 1) {
        n = n % 2 == 0 ? n / 2 : 3 * n + 1;
        answer.push_back(n);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int n) {  // 콜라츠 수열 만들기 풀이 시작
//     vector<int> answer{n};  // 중괄호 초기화로 시작값 n을 첫 원소로 저장
//     while (n != 1) {  // while과 !=로 현재 값이 1이 아닐 동안 다음 수열 값을 계산
//         n = n % 2 == 0 ? n / 2 : 3 * n + 1;  // 삼항 연산자 ?:로 짝수이면 절반, 홀수이면 3배에 1을 더한 값으로 바꾸기
//         answer.push_back(n);  // push_back으로 다음 콜라츠 수열 값을 vector 끝에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작값을 저장하고 짝수이면 절반, 홀수이면 3배에 1을 더하며 1까지 기록

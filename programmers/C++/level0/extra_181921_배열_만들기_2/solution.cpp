#include <vector>
using namespace std;

vector<int> solution(int l, int r) {
    vector<int> answer;
    for (int value = l; value <= r; ++value) {
        int rest = value;
        bool valid = true;
        while (rest) {
            int digit = rest % 10;
            if (digit != 0 && digit != 5) { valid = false; break; }
            rest /= 10;
        }
        if (valid) answer.push_back(value);
    }
    if (answer.empty()) answer.push_back(-1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int l, int r) {  // 배열 만들기 2 풀이 시작
//     vector<int> answer;  // 자릿수가 0과 5로만 이루어진 수
//     for (int value = l; value <= r; ++value) {  // for로 l부터 r까지 양 끝을 포함하는 모든 정수를 검사
//         int rest = value;  // 자릿수를 차례로 제거하며 검사할 수를 복사
//         bool valid = true;  // 모든 자릿수가 0 또는 5라는 검사 결과를 true로 초기화
//         while (rest) {  // 남은 수가 0이 아닐 동안 while로 자릿수 검사를 반복
//             int digit = rest % 10;  // 나머지 연산자 %로 현재 수의 마지막 자릿수를 구하기
//             if (digit != 0 && digit != 5) { valid = false; break; }  // !=와 &&로 0과 5가 아닌 자릿수를 확인하면 실패 표시를 남기고 break로 검사를 끝
//             rest /= 10;  // 정수 나눗셈의 복합 대입 /=로 검사한 마지막 자릿수를 제거
//         }  // 블록 끝
//         if (valid) answer.push_back(value);  // if로 모든 자릿수가 유효한지 확인하고 push_back으로 결과에 넣기
//     }  // 블록 끝
//     if (answer.empty()) answer.push_back(-1);  // empty로 빈 결과를 검사하고 push_back으로 -1을 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 범위 안의 각 수를 자릿수별로 검사해 0과 5로만 이루어진 수를 남기고, 없으면 -1을 반환

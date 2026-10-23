#include <vector>
using namespace std;

vector<int> solution(vector<int> numbers) {
    vector<int> answer(numbers.size(), -1), stack;
    for (int i = 0; i < (int)numbers.size(); ++i) {
        while (!stack.empty() && numbers[stack.back()] < numbers[i]) {
            answer[stack.back()] = numbers[i];
            stack.pop_back();
        }
        stack.push_back(i);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<int> numbers) {  // 스택의 미해결 위치에 뒤의 첫 큰 수 기록
// vector<int> answer(numbers.size(), -1), stack;  // 결과를 -1로 초기화하고 아직 답을 못 찾은 인덱스 저장
// for (int i = 0; i < (int)numbers.size(); ++i) {  // 수를 왼쪽부터 순회
// while (!stack.empty() && numbers[stack.back()] < numbers[i]) {  // 현재 값이 스택 끝의 값보다 큰지 검사
// answer[stack.back()] = numbers[i];  // 현재 값이 해당 위치에서 처음 만난 큰 수
// stack.pop_back();  // 답을 찾은 인덱스 제거
// }  // 블록 끝
// stack.push_back(i);  // 현재 인덱스도 다음 큰 수를 기다리도록 넣기
// }  // 블록 끝
// return answer;  // 각 위치의 뒤 큰 수 반환
// }  // 블록 끝

// 풀이 요약
// 아직 뒤 큰 수를 찾지 못한 인덱스를 스택에 넣고 더 큰 값을 만나면 스택 끝부터 답 기록

#include <vector>
using namespace std;

vector<int> solution(vector<int> prices) {
    int n = (int)prices.size();
    vector<int> answer(n), stack;
    for (int i = 0; i < n; ++i) answer[i] = n - i - 1;
    for (int i = 0; i < n; ++i) {
        while (!stack.empty() && prices[stack.back()] > prices[i]) {
            int previous = stack.back(); stack.pop_back();
            answer[previous] = i - previous;
        }
        stack.push_back(i);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<int> prices) {  // 처음 더 낮은 가격이 나온 시점에 지속 시간 확정
// int n = (int)prices.size();  // 가격 기록의 길이 구하기
// vector<int> answer(n), stack;  // 가격이 떨어질 때까지의 시간과 미확정 인덱스 저장
// for (int i = 0; i < n; ++i) answer[i] = n - i - 1;  // 끝까지 떨어지지 않는 경우의 시간을 기본값으로 두기
// for (int i = 0; i < n; ++i) {  // 가격을 시간순으로 읽기
// while (!stack.empty() && prices[stack.back()] > prices[i]) {  // 현재보다 높은 과거 가격의 하락 시점 찾기
// int previous = stack.back(); stack.pop_back();  // 답이 정해진 과거 인덱스 꺼내기
// answer[previous] = i - previous;  // 현재 시각까지의 차이 기록
// }  // 블록 끝
// stack.push_back(i);  // 현재 가격의 하락 시점도 기다리기
// }  // 블록 끝
// return answer;  // 각 가격이 떨어지지 않은 시간 반환
// }  // 블록 끝

// 풀이 요약
// 가격이 떨어지지 않으면 끝까지의 시간을 기본값으로 두고 더 낮은 가격을 만날 때 스택의 과거 인덱스별 지속 시간을 확정하기

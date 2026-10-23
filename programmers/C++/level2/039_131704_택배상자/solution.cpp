#include <vector>
using namespace std;

int solution(vector<int> order) {
    vector<int> stack;
    int answer = 0;
    for (int box = 1; box <= (int)order.size(); ++box) {
        stack.push_back(box);
        while (!stack.empty() && answer < (int)order.size() && stack.back() == order[answer]) {
            stack.pop_back();
            ++answer;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> order) {  // 보조 스택으로 요청 순서대로 실을 상자 수 계산
// vector<int> stack;  // 보조 컨테이너 벨트의 상자를 스택으로 관리
// int answer = 0;  // 요청 순서대로 실은 상자 수 초기화
// for (int box = 1; box <= (int)order.size(); ++box) {  // 주 컨테이너의 상자를 번호 순서대로 받기
// stack.push_back(box);  // 현재 상자를 보조 스택에 올리기
// while (!stack.empty() && answer < (int)order.size() && stack.back() == order[answer]) {  // 스택 끝이 다음 요청 상자이면 바로 실을 수 있음
// stack.pop_back();  // 실은 상자를 스택에서 제거
// ++answer;  // 처리한 요청 수 늘리기
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 순서를 지켜 실은 최대 상자 수 반환
// }  // 블록 끝

// 풀이 요약
// 상자를 순서대로 보조 스택에 넣고 스택 끝이 다음 요청과 같을 때마다 꺼내 싣기

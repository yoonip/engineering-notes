#include <iostream> // 배열과 답의 입출력
#include <vector> // 값·결과·인덱스 스택 저장
using namespace std; // 표준 이름 접두사 생략
int main() { // 실행 시작점
    int n; cin >> n; vector<int> values(n), answer(n, -1), stack; // 크기와 미해결 스택 준비
    for (int& value : values) cin >> value; // 원소 입력
    for (int i = 0; i < n; ++i) { // 오른쪽으로 한 번 순회
        while (!stack.empty() && values[stack.back()] < values[i]) { // 현재 값으로 해결되는 스택 끝 후보 확인
            answer[stack.back()] = i; stack.pop_back(); // 첫 큰 값의 위치를 기록하고 후보 제거
        } // 해결 가능한 이전 후보 처리 끝
        stack.push_back(i); // 현재 인덱스를 새 미해결 후보로 추가
    } // 배열 순회 끝
    for (int i = 0; i < n; ++i) cout << (i ? " " : "") << answer[i]; // 인덱스 순서대로 답 출력
    cout << '\n'; // 출력 줄 끝내기
    return 0; // 정상 종료
} // 단조 스택 예제 끝

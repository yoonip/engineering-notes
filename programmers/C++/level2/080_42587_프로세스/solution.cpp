#include <queue>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<int> priorities, int location) {
    queue<pair<int, int>> q; priority_queue<int> highest;
    for (int i = 0; i < (int)priorities.size(); ++i) { q.push({i, priorities[i]}); highest.push(priorities[i]); }
    int executed = 0;
    while (!q.empty()) {
        auto [index, priority] = q.front(); q.pop();
        if (priority < highest.top()) q.push({index, priority});
        else {
            highest.pop(); ++executed;
            if (index == location) return executed;
        }
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> priorities, int location) {  // 현재 최고 우선순위인 프로세스만 실행
// queue<pair<int, int>> q; priority_queue<int> highest;  // 대기 순서와 남은 우선순위 최댓값 관리
// for (int i = 0; i < (int)priorities.size(); ++i) { q.push({i, priorities[i]}); highest.push(priorities[i]); }  // 원래 위치를 우선순위와 함께 등록
// int executed = 0;  // 실행한 프로세스 수 초기화
// while (!q.empty()) {  // 대기열이 남아 있는 동안 처리
// auto [index, priority] = q.front(); q.pop();  // 가장 앞의 프로세스 꺼내기
// if (priority < highest.top()) q.push({index, priority});  // 더 높은 우선순위가 남아 있으면 뒤로 보내기
// else {  // 현재 프로세스가 실행 가능한 최고 우선순위
// highest.pop(); ++executed;  // 실행한 우선순위를 제거하고 실행 수 늘리기
// if (index == location) return executed;  // 요청한 프로세스이면 실행 순서 반환
// }  // 블록 끝
// }  // 블록 끝
// return 0;  // 유효한 위치에서는 도달하지 않는 기본 반환
// }  // 블록 끝

// 풀이 요약
// 대기열의 앞 프로세스를 꺼내 남은 최고 우선순위보다 낮으면 뒤로 보내고 아니면 실행 순서 세기

#include <algorithm>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
using namespace std;

vector<string> solution(vector<vector<string>> plans) {
    vector<tuple<int, string, int>> tasks;
    for (const auto& plan : plans) tasks.push_back({stoi(plan[1].substr(0, 2)) * 60 + stoi(plan[1].substr(3, 2)), plan[0], stoi(plan[2])});
    sort(tasks.begin(), tasks.end());
    vector<pair<string, int>> stack;
    vector<string> answer;
    int previous = 0;
    for (const auto& [start, name, duration] : tasks) {
        int free_time = start - previous;
        while (free_time > 0 && !stack.empty()) {
            auto [old_name, remaining] = stack.back(); stack.pop_back();
            if (remaining <= free_time) {
                free_time -= remaining;
                answer.push_back(old_name);
            } else {
                stack.push_back({old_name, remaining - free_time});
                free_time = 0;
            }
        }
        stack.push_back({name, duration});
        previous = start;
    }
    while (!stack.empty()) { answer.push_back(stack.back().first); stack.pop_back(); }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <tuple>  // 여러 상태 값을 묶는 tuple
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<vector<string>> plans) {  // 새 과제 사이의 빈 시간에 중단 과제를 재개
// vector<tuple<int, string, int>> tasks;  // 시작 시각, 이름, 소요 시간을 하나의 과제로 묶기
// for (const auto& plan : plans) tasks.push_back({stoi(plan[1].substr(0, 2)) * 60 + stoi(plan[1].substr(3, 2)), plan[0], stoi(plan[2])});  // 시각을 분으로 바꾸고 소요 시간을 정수화
// sort(tasks.begin(), tasks.end());  // 시작 시각이 빠른 순서로 정렬
// vector<pair<string, int>> stack;  // 중단한 과제의 이름과 남은 시간을 스택으로 관리
// vector<string> answer;  // 완료한 과제의 순서 저장
// int previous = 0;  // 직전 과제의 시작 시각 초기화
// for (const auto& [start, name, duration] : tasks) {  // 정렬한 과제를 순서대로 시작
// int free_time = start - previous;  // 새 과제 전까지 진행할 수 있는 시간 구하기
// while (free_time > 0 && !stack.empty()) {  // 여유 시간 동안 최근 중단한 과제를 이어 진행
// auto [old_name, remaining] = stack.back(); stack.pop_back();  // 가장 최근 과제 꺼내기
// if (remaining <= free_time) {  // 새 과제 전에 완료할 수 있는지 확인
// free_time -= remaining;  // 완료에 사용한 시간 빼기
// answer.push_back(old_name);  // 완료 순서에 이름 추가
// } else {  // 완료하지 못하면 남은 시간 기록
// stack.push_back({old_name, remaining - free_time});  // 진행한 시간만큼 줄여 다시 중단
// free_time = 0;  // 남은 여유 시간을 모두 사용
// }  // 블록 끝
// }  // 블록 끝
// stack.push_back({name, duration});  // 새로 시작한 과제를 스택 위에 두기
// previous = start;  // 다음 과제의 시간 계산 기준 갱신
// }  // 블록 끝
// while (!stack.empty()) { answer.push_back(stack.back().first); stack.pop_back(); }  // 마지막 시작 이후에는 남은 과제를 역순으로 완료
// return answer;  // 과제 완료 순서 반환
// }  // 블록 끝

// 풀이 요약
// 시작 시각 순서로 과제를 처리하며 새 과제 전의 시간으로 최근 중단한 과제부터 진행하고 완료 순서 기록

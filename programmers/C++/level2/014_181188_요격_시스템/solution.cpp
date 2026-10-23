#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<vector<int>> targets) {
    sort(targets.begin(), targets.end(), [](const auto& a, const auto& b) { return a[1] < b[1]; });
    int answer = 0, end = -1;
    for (const auto& target : targets) {
        if (target[0] >= end) {
            ++answer;
            end = target[1];
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> targets) {  // 구간 끝점부터 묶어 최소 요격 횟수 찾기
// sort(targets.begin(), targets.end(), [](const auto& a, const auto& b) { return a[1] < b[1]; });  // 구간 끝 좌표가 작은 순서로 정렬
// int answer = 0, end = -1;  // 요격 수와 최근 요격으로 포함하는 구간의 오른쪽 경계 초기화
// for (const auto& target : targets) {  // 끝 좌표 순서대로 구간 확인
// if (target[0] >= end) {  // 최근 요격으로 처리할 수 없는 새 구간인지 검사
// ++answer;  // 새로운 요격 한 번 세기
// end = target[1];  // 새 묶음의 오른쪽 경계를 현재 구간 끝으로 두기
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 최소 요격 수 반환
// }  // 블록 끝

// 풀이 요약
// 구간 끝 좌표 순서로 정렬하고 현재 묶음으로 처리할 수 없는 구간을 만날 때만 요격 수 늘리기

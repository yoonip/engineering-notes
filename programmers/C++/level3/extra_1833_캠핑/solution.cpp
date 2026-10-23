#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> data) {
    (void)n; sort(data.begin(), data.end()); vector<vector<int>> groups; vector<int> xs;
    for (const auto& point : data) { if (xs.empty() || xs.back() != point[0]) { xs.push_back(point[0]); groups.push_back({}); } groups.back().push_back(point[1]); }
    int answer = 0;
    for (int i = 0; i < (int)groups.size(); ++i) for (int y : groups[i]) {
        long long low = -1, high = 1LL << 31;
        for (int j = i + 1; j < (int)groups.size(); ++j) {
            for (int other : groups[j]) if (other != y && low <= other && other <= high) ++answer;
            for (int other : groups[j]) { if (other > y) high = min(high,1LL * other); else if (other < y) low = max(low,1LL * other); }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> data) {  // 중간 점이 없는 두 점의 직사각형 개수 세기
// (void)n; sort(data.begin(), data.end()); vector<vector<int>> groups; vector<int> xs;  // 같은 x좌표의 점들을 묶기 위해 정렬
// for (const auto& point : data) { if (xs.empty() || xs.back() != point[0]) { xs.push_back(point[0]); groups.push_back({}); } groups.back().push_back(point[1]); }  // x좌표별 y좌표 목록 만들기
// int answer = 0;  // 내부에 다른 점이 없는 직사각형 수 초기화
// for (int i = 0; i < (int)groups.size(); ++i) for (int y : groups[i]) {  // 왼쪽 경계의 한 점 고르기
// long long low = -1, high = 1LL << 31;  // 이전 x그룹의 점들이 제한하는 아래 및 위 경계 초기화
// for (int j = i + 1; j < (int)groups.size(); ++j) {  // 오른쪽 경계를 x좌표 순서대로 늘리기
// for (int other : groups[j]) if (other != y && low <= other && other <= high) ++answer;  // 가로와 세로 길이가 있고 내부 방해점이 없는 반대 꼭짓점 세기
// for (int other : groups[j]) { if (other > y) high = min(high,1LL * other); else if (other < y) low = max(low,1LL * other); }  // 현재 그룹은 다음 경계부터 내부 방해점이 됨
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 조건을 만족하는 캠핑 구역 수 반환
// }  // 블록 끝

// 풀이 요약
// 왼쪽 점을 고정하고 오른쪽 x좌표 그룹을 확장하며 중간 점들이 제한하는 y경계를 유지해 내부가 빈 직사각형 세기

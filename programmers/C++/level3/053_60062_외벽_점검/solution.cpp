#include <algorithm>
#include <vector>
using namespace std;

int solution(int n, vector<int> weak, vector<int> dist) {
    int length = (int)weak.size(); vector<int> extended = weak;
    for (int point : weak) extended.push_back(point + n);
    sort(dist.rbegin(), dist.rend());
    for (int count = 1; count <= (int)dist.size(); ++count) {
        vector<int> order(dist.begin(), dist.begin() + count); sort(order.begin(), order.end());
        do {
            for (int start = 0; start < length; ++start) {
                int next = start;
                for (int reach : order) {
                    int end = extended[next] + reach;
                    while (next < start + length && extended[next] <= end) ++next;
                    if (next == start + length) return count;
                }
            }
        } while (next_permutation(order.begin(), order.end()));
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<int> weak, vector<int> dist) {  // 친구 수와 방문 순서를 바꿔 외벽 전체 점검
// int length = (int)weak.size(); vector<int> extended = weak;  // 원형 외벽을 일자로 펼칠 배열 만들기
// for (int point : weak) extended.push_back(point + n);  // 한 바퀴 뒤의 취약점을 이어 붙이기
// sort(dist.rbegin(), dist.rend());  // 같은 인원 수에서는 이동 거리가 긴 친구들을 사용
// for (int count = 1; count <= (int)dist.size(); ++count) {  // 최소 인원부터 가능한지 검사
// vector<int> order(dist.begin(), dist.begin() + count); sort(order.begin(), order.end());  // 선택한 친구들의 첫 순열 만들기
// do {  // 투입 순서를 모두 검사
// for (int start = 0; start < length; ++start) {  // 취약점별로 점검 시작점 고르기
// int next = start;  // 아직 점검하지 않은 첫 취약점
// for (int reach : order) {  // 친구를 순서대로 투입
// int end = extended[next] + reach;  // 현재 친구가 점검할 수 있는 끝 구하기
// while (next < start + length && extended[next] <= end) ++next;  // 이동 범위 안의 모든 취약점 처리
// if (next == start + length) return count;  // 한 바퀴의 모든 취약점을 점검하면 현재 인원 수가 최소
// }  // 블록 끝
// }  // 블록 끝
// } while (next_permutation(order.begin(), order.end()));  // 중복 없는 다음 투입 순서 구하기
// }  // 블록 끝
// return -1;  // 주어진 친구로 모두 점검할 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 사용할 인원 수를 늘려 가며 가장 멀리 이동하는 친구들의 모든 순서와 외벽의 모든 시작 취약점 검사

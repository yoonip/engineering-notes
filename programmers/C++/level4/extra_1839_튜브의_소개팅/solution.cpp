#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

vector<int> solution(int m, int n, int s, vector<vector<int>> time_map) {
    int size = m * n; long long infinity = (long long)s + 1; vector<long long> current(size, infinity); current[0] = 0;
    int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
    for (int steps = 1; steps < size; ++steps) {
        vector<long long> next(size, infinity);
        for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) {
            long long cost = current[r * n + c]; if (cost > s) continue;
            for (int direction = 0; direction < 4; ++direction) {
                int nr = r + dr[direction], nc = c + dc[direction];
                if (0 <= nr && nr < m && 0 <= nc && nc < n && time_map[nr][nc] != -1) {
                    long long candidate = cost + time_map[nr][nc]; int index = nr * n + nc;
                    if (candidate <= s) next[index] = min(next[index], candidate);
                }
            }
        }
        current.swap(next); if (current.back() <= s) return {steps, (int)current.back()};
    }
    return {-1, -1};
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// vector<int> solution(int m, int n, int s, vector<vector<int>> time_map) {  // 튜브의 소개팅 풀이 함수 정의
//     int size = m * n; long long infinity = (long long)s + 1; vector<long long> current(size, infinity); current[0] = 0;  // 전체 칸 수와 도달 불가 값 s + 1을 준비. 출발 칸 시간만 0으로 설정
//     int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};  // 상하좌우 이동량 저장
//     for (int steps = 1; steps < size; ++steps) {  // 단순 경로의 최대 길이인 전체 칸 수 - 1까지 이동 횟수 증가
//         vector<long long> next(size, infinity);  // 이번 횟수로 도착할 최소 시간 배열을 불가능 값으로 초기화
//         for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) {  // 모든 출발 칸 후보 검사
//             long long cost = current[r * n + c]; if (cost > s) continue;  // 이전 횟수의 최소 시간이 이미 s를 넘으면 전이 생략
//             for (int direction = 0; direction < 4; ++direction) {  // 가능한 칸에서 네 방향으로 이동 검사
//                 int nr = r + dr[direction], nc = c + dc[direction];  // 다음 칸 좌표 계산
//                 if (0 <= nr && nr < m && 0 <= nc && nc < n && time_map[nr][nc] != -1) {  // 보드 안이고 장애물(-1)이 아닐 때만 이동 가능
//                     long long candidate = cost + time_map[nr][nc]; int index = nr * n + nc;  // 이웃 칸의 시간을 더해 후보 비용을 구하고 1차원 칸 번호 계산
//                     if (candidate <= s) next[index] = min(next[index], candidate);  // 제한 시간 안이면 이웃 칸에 같은 횟수로 도착하는 최소 시간 갱신
//                 }  // 블록 끝
//             }  // 블록 끝
//         }  // 블록 끝
//         current.swap(next); if (current.back() <= s) return {steps, (int)current.back()};  // 이번 횟수의 DP로 교체. 목적지에 닿으면 최소 이동 횟수와 그 안의 최소 시간 반환
//     }  // 블록 끝
//     return {-1, -1};  // 제한 안의 경로가 없으면 {-1, -1} 반환
// }  // 함수 끝
//

// 풀이 요약
// 이동 횟수를 하나씩 늘리는 DP. 같은 횟수로 각 칸에 도달하는 최소 시간만 남기고, 제한 시간 안에 목적지에 닿는 첫 이동 횟수에서 답 반환.

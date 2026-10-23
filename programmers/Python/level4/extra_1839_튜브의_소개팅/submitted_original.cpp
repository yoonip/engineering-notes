#include <vector>
#include <algorithm>
using namespace std;

vector<int> solution(int m, int n, int s, vector<vector<int>> time_map) {
    int size = m * n;
    long long infinity = 1LL << 60;
    vector<long long> current(size, infinity);
    current[0] = 0;
    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    for (int steps = 1; steps < size; ++steps) {
        vector<long long> next_cost(size, infinity);
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                long long cost = current[r * n + c];
                if (cost > s) continue;
                for (int direction = 0; direction < 4; ++direction) {
                    int nr = r + dr[direction], nc = c + dc[direction];
                    if (nr < 0 || nr >= m || nc < 0 || nc >= n || time_map[nr][nc] == -1) continue;
                    long long candidate = cost + time_map[nr][nc];
                    int index = nr * n + nc;
                    if (candidate <= s) next_cost[index] = min(next_cost[index], candidate);
                }
            }
        }
        current.swap(next_cost);
        if (current[size - 1] <= s) return {steps, static_cast<int>(current[size - 1])};
    }
    return {-1, -1};
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 포함. vector는 크기를 조절할 수 있는 배열을 제공.
// #include <algorithm>  // algorithm 헤더는 min 등 기본 알고리즘 함수 제공.
// using namespace std;  // std 이름 공간의 vector·min 등을 접두사 없이 사용.
// 
// vector<int> solution(int m, int n, int s, vector<vector<int>> time_map) {  // 함수 정의. int는 정수, vector<vector<int>>는 2차원 배열, {}는 함수 본문.
//     int size = m * n;  // 전체 칸 수를 정수 변수에 저장. ;는 문장 끝.
//     long long infinity = 1LL << 60;  // long long은 큰 정수형. LL로 큰 정수 상수 지정, <<로 큰 무한대 대용값 생성.
//     vector<long long> current(size, infinity);  // size개 원소를 infinity로 채운 동적 배열. 대화 합계 오버플로를 막기 위해 큰 정수 사용.
//     current[0] = 0;  // []는 배열 접근. 출발점의 초기 대화 시간은 0.
//     int dr[4] = {1, -1, 0, 0};  // 길이 4의 고정 배열. 행 방향 변화량 저장.
//     int dc[4] = {0, 0, 1, -1};  // 열 방향 변화량 배열. 같은 인덱스의 dr과 묶어 네 방향 표현.
//     for (int steps = 1; steps < size; ++steps) {  // for는 초기화·조건·증가식 반복. ++는 1 증가. 이동 횟수를 작은 순서로 검사.
//         vector<long long> next_cost(size, infinity);  // 다음 이동 횟수의 최소 대화 시간 배열 초기화.
//         for (int r = 0; r < m; ++r) {  // 모든 행을 순회하는 반복 시작.
//             for (int c = 0; c < n; ++c) {  // 모든 열을 순회하는 반복 시작.
//                 long long cost = current[r * n + c];  // 현재 칸의 최소 대화 시간 조회. 2차원 좌표를 한 번호로 변환.
//                 if (cost > s) continue;  // if는 조건문. 도달 불가능·제한 초과 칸은 continue로 건너뜀.
//                 for (int direction = 0; direction < 4; ++direction) {  // 상하좌우 방향을 순회.
//                     int nr = r + dr[direction], nc = c + dc[direction];  // 이웃 칸 행·열 좌표를 두 변수에 저장.
//                     if (nr < 0 || nr >= m || nc < 0 || nc >= n || time_map[nr][nc] == -1) continue;  // ||는 논리 OR. 범위 밖이거나 테이블이면 이동 불가.
//                     long long candidate = cost + time_map[nr][nc];  // 이웃 칸의 대화 시간을 큰 정수로 합산.
//                     int index = nr * n + nc;  // 이웃의 1차원 칸 번호 계산.
//                     if (candidate <= s) next_cost[index] = min(next_cost[index], candidate);  // 제한 이내인 경로만 min으로 같은 단계의 최소 대화 시간 갱신.
//                 }  // 방향 순회 블록 종료.
//             }  // 열 순회 블록 종료.
//         }  // 행 순회 블록 종료.
//         current.swap(next_cost);  // swap은 두 벡터의 내용을 교환. 새 단계 결과를 복사 비용 없이 적용.
//         if (current[size - 1] <= s) return {steps, static_cast<int>(current[size - 1])};  // 처음 도착한 단계와 최소 대화 시간 반환. static_cast는 int로 명시 변환하며 값은 s 이하라 안전.
//     }  // 이동 횟수 반복 종료.
//     return {-1, -1};  // 경로가 없을 때 두 정수 배열 반환. 문제에서는 이 경우가 없음.
// }  // solution 함수 본문 종료.

// 풀이 요약
// 이동 횟수별 최소 대화 시간 DP입니다. 목표 칸에 허용 시간 이내로 도착하는 첫 단계에서 답을 반환합니다.
// 예제 3은 더 짧은 경로가 대화 제한을 넘기 때문에 12번 이동, 대화 시간 11을 선택합니다. 합계는 long long으로 계산합니다.
// 칸 수 V=m*n일 때 시간 O(V^2), 공간 O(V). 같은 알고리즘의 Python3 학습 코드를 함께 제공합니다.
// 
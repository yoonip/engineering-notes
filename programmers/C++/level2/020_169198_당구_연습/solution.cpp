#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

vector<int> solution(int m, int n, int startX, int startY, vector<vector<int>> balls) {
    vector<int> answer;
    auto square = [](long long value) { return value * value; };
    for (const auto& ball : balls) {
        int x = ball[0], y = ball[1];
        long long best = LLONG_MAX;
        if (!(startY == y && x < startX)) best = min(best, square(startX + x) + square(startY - y));
        if (!(startY == y && x > startX)) best = min(best, square(2 * m - startX - x) + square(startY - y));
        if (!(startX == x && y < startY)) best = min(best, square(startX - x) + square(startY + y));
        if (!(startX == x && y > startY)) best = min(best, square(startX - x) + square(2 * n - startY - y));
        answer.push_back((int)best);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int m, int n, int startX, int startY, vector<vector<int>> balls) {  // 벽 반사 경로 중 유효한 최단 거리 제곱 계산
// vector<int> answer;  // 각 공의 최소 거리 제곱 저장
// auto square = [](long long value) { return value * value; };  // 정수의 제곱을 넓은 정수형으로 계산
// for (const auto& ball : balls) {  // 목표 공을 하나씩 처리
// int x = ball[0], y = ball[1];  // 목표 공의 좌표 읽기
// long long best = LLONG_MAX;  // 가능한 반사 경로 중 최소 거리 초기화
// if (!(startY == y && x < startX)) best = min(best, square(startX + x) + square(startY - y));  // 왼쪽 벽 반사에서 공을 먼저 맞히는 경우를 제외
// if (!(startY == y && x > startX)) best = min(best, square(2 * m - startX - x) + square(startY - y));  // 오른쪽 벽 반사의 거리 제곱 비교
// if (!(startX == x && y < startY)) best = min(best, square(startX - x) + square(startY + y));  // 아래쪽 벽 반사의 거리 제곱 비교
// if (!(startX == x && y > startY)) best = min(best, square(startX - x) + square(2 * n - startY - y));  // 위쪽 벽 반사의 거리 제곱 비교
// answer.push_back((int)best);  // 최소 거리 제곱을 결과에 추가
// }  // 블록 끝
// return answer;  // 모든 공에 대한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 벽에 반사한 목표 좌표까지의 거리 제곱을 비교하고 벽보다 목표 공을 먼저 맞히는 경로는 제외

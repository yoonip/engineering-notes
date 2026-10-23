#include <algorithm>
#include <vector>
using namespace std;

long long solution(int n, vector<int> times) {
    long long left = 0, right = 1LL * *min_element(times.begin(), times.end()) * n;
    while (left < right) {
        long long middle = left + (right - left) / 2, completed = 0;
        for (int time : times) { completed += middle / time; if (completed >= n) break; }
        if (completed >= n) right = middle; else left = middle + 1;
    }
    return left;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int n, vector<int> times) {  // 주어진 시간의 심사 인원으로 최소 완료 시각 찾기
// long long left = 0, right = 1LL * *min_element(times.begin(), times.end()) * n;  // 가장 빠른 심사관이 모두 처리할 시간을 상한으로 두기
// while (left < right) {  // n명을 심사할 수 있는 최소 시간을 이분 탐색
// long long middle = left + (right - left) / 2, completed = 0;  // 시간 후보와 완료 인원 수 초기화
// for (int time : times) { completed += middle / time; if (completed >= n) break; }  // 심사관별 완료 인원을 더하고 충분하면 멈추기
// if (completed >= n) right = middle; else left = middle + 1;  // 가능 여부에 따라 시간 범위 줄이기
// }  // 블록 끝
// return left;  // 최소 전체 심사 시간 반환
// }  // 블록 끝

// 풀이 요약
// 전체 시간을 이분 탐색하고 각 심사관의 처리 인원 합이 n 이상인지 검사

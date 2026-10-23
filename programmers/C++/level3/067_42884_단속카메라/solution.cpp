#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

int solution(vector<vector<int>> routes) {
    sort(routes.begin(), routes.end(), [](const auto& a, const auto& b) { return a[1] < b[1]; });
    int camera = INT_MIN, answer = 0;
    for (const auto& route : routes) if (route[0] > camera) { camera = route[1]; ++answer; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> routes) {  // 가장 빠른 진출 지점에 카메라를 두어 차량 묶기
// sort(routes.begin(), routes.end(), [](const auto& a, const auto& b) { return a[1] < b[1]; });  // 진출 지점이 빠른 차량부터 정렬
// int camera = INT_MIN, answer = 0;  // 최근 카메라 위치와 설치 수 초기화
// for (const auto& route : routes) if (route[0] > camera) { camera = route[1]; ++answer; }  // 최근 카메라를 지나지 않는 차량이면 진출 지점에 새 카메라 두기
// return answer;  // 모든 차량을 만나는 최소 카메라 수 반환
// }  // 블록 끝

// 풀이 요약
// 진출 지점이 빠른 순서로 차량을 보고 최근 카메라를 지나지 않는 구간의 끝에 새 카메라 두기

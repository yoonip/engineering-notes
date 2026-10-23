#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<vector<int>> scores) {
    vector<int> target = scores[0]; int target_sum = target[0] + target[1];
    sort(scores.begin(), scores.end(), [](const auto& a, const auto& b) { return a[0] != b[0] ? a[0] > b[0] : a[1] < b[1]; });
    int rank = 1, best_second = -1;
    for (const auto& score : scores) {
        if (score[1] < best_second) { if (score == target) return -1; continue; }
        best_second = score[1];
        if (score[0] + score[1] > target_sum) ++rank;
    }
    return rank;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> scores) {  // 지배당한 직원을 빼고 완호의 점수 순위 계산
// vector<int> target = scores[0]; int target_sum = target[0] + target[1];  // 완호의 두 점수와 합계 저장
// sort(scores.begin(), scores.end(), [](const auto& a, const auto& b) { return a[0] != b[0] ? a[0] > b[0] : a[1] < b[1]; });  // 첫 점수 내림차순과 둘째 점수 오름차순으로 정렬
// int rank = 1, best_second = -1;  // 완호의 순위와 지금까지 유효한 둘째 점수의 최댓값 초기화
// for (const auto& score : scores) {  // 두 점수가 모두 더 높은 사람이 있는지 검사
// if (score[1] < best_second) { if (score == target) return -1; continue; }  // 탈락 대상은 제외하고 완호이면 -1 반환
// best_second = score[1];  // 현재까지의 둘째 점수 경계 갱신
// if (score[0] + score[1] > target_sum) ++rank;  // 합계가 완호보다 큰 유효 직원 세기
// }  // 블록 끝
// return rank;  // 완호의 최종 순위 반환
// }  // 블록 끝

// 풀이 요약
// 첫 점수 내림차순과 둘째 점수 오름차순으로 정렬해 탈락 직원을 제외하고 완호보다 합계가 큰 유효 직원 세기

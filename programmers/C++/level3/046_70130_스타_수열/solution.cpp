#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<int> a) {
    int n = (int)a.size(); vector<int> pairs(n, 0), used_until(n, -1);
    for (int i = 0; i + 1 < n; ++i) {
        int first = a[i], second = a[i + 1]; if (first == second) continue;
        if (used_until[first] < i) { ++pairs[first]; used_until[first] = i + 1; }
        if (used_until[second] < i) { ++pairs[second]; used_until[second] = i + 1; }
    }
    return 2 * *max_element(pairs.begin(), pairs.end());
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> a) {  // 공통 값 후보마다 겹치지 않는 유효 쌍 만들기
// int n = (int)a.size(); vector<int> pairs(n, 0), used_until(n, -1);  // 공통 원소 후보별로 선택한 쌍 수와 마지막 사용 위치 저장
// for (int i = 0; i + 1 < n; ++i) {  // 인접한 두 원소의 모든 쌍 검사
// int first = a[i], second = a[i + 1]; if (first == second) continue;  // 같은 값으로 된 쌍은 스타 수열에 쓸 수 없음
// if (used_until[first] < i) { ++pairs[first]; used_until[first] = i + 1; }  // 첫 값을 공통 원소로 하는 겹치지 않는 쌍 고르기
// if (used_until[second] < i) { ++pairs[second]; used_until[second] = i + 1; }  // 둘째 값을 공통 원소로 하는 경우도 갱신
// }  // 블록 끝
// return 2 * *max_element(pairs.begin(), pairs.end());  // 가장 많은 쌍을 가진 후보의 두 배 길이 반환
// }  // 블록 끝

// 풀이 요약
// 인접한 서로 다른 두 값의 쌍을 각 공통 원소 후보에 대해 겹치지 않게 선택하고 가장 많은 쌍의 두 배 구하기

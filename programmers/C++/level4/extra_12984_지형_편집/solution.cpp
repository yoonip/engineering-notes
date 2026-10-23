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

long long solution(vector<vector<int>> land, int P, int Q) {
    vector<int> heights; for (const auto& row : land) heights.insert(heights.end(), row.begin(), row.end());
    sort(heights.begin(), heights.end()); size_t index = (long long)heights.size() * Q / ((long long)P + Q); int target = heights[index];
    long long answer = 0;
    for (int height : heights) answer += height < target ? 1LL * (target - height) * P : 1LL * (height - target) * Q;
    return answer;
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
// long long solution(vector<vector<int>> land, int P, int Q) {  // 지형 편집 풀이 함수 정의
//     vector<int> heights; for (const auto& row : land) heights.insert(heights.end(), row.begin(), row.end());  // 모든 땅 높이를 하나의 배열로 펼침
//     sort(heights.begin(), heights.end()); size_t index = (long long)heights.size() * Q / ((long long)P + Q); int target = heights[index];  // 높이순 정렬 후 비용 비율 Q / (P + Q)에 해당하는 위치를 목표 높이로 선택
//     long long answer = 0;  // 전체 편집 비용을 long long 0으로 시작
//     for (int height : heights) answer += height < target ? 1LL * (target - height) * P : 1LL * (height - target) * Q;  // 낮은 칸은 차이 × 추가 비용 P, 높은 칸은 차이 × 제거 비용 Q를 합산
//     return answer;  // 선택한 목표 높이에서의 최소 편집 비용 반환
// }  // 함수 끝
//

// 풀이 요약
// 높이를 정렬하고 추가·제거 비용의 비율에 해당하는 가중 분위수로 목표 높이 선택. 그 높이까지 더하거나 제거하는 비용을 long long으로 합산.

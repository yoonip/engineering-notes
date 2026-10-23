#include <algorithm>
#include <vector>
using namespace std;

vector<int> solution(int n, vector<int> info) {
    int best_difference = 0;
    vector<int> answer{-1}, best_reversed;
    for (int mask = 0; mask < (1 << 10); ++mask) {
        vector<int> shots(11, 0);
        int remaining = n;
        for (int i = 0; i < 10; ++i) if (mask & (1 << i)) { shots[i] = info[i] + 1; remaining -= shots[i]; }
        if (remaining < 0) continue;
        shots[10] = remaining;
        int difference = 0;
        for (int i = 0; i < 10; ++i) {
            if (shots[i] > info[i]) difference += 10 - i;
            else if (info[i] > 0) difference -= 10 - i;
        }
        vector<int> reversed(shots.rbegin(), shots.rend());
        if (difference > 0 && (difference > best_difference || (difference == best_difference && reversed > best_reversed))) {
            best_difference = difference; best_reversed = reversed; answer = shots;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, vector<int> info) {  // 점수 차이와 낮은 과녁 우선순위로 화살 배치 선택
// int best_difference = 0;  // 이길 수 있는 점수 차이의 최댓값 초기화
// vector<int> answer{-1}, best_reversed;  // 최종 화살 배분과 낮은 점수 우선 비교용 배열 저장
// for (int mask = 0; mask < (1 << 10); ++mask) {  // 10점부터 1점까지 이길 과녁의 부분집합을 모두 고르기
// vector<int> shots(11, 0);  // 현재 화살 배분을 0으로 초기화
// int remaining = n;  // 사용할 수 있는 화살 수 초기화
// for (int i = 0; i < 10; ++i) if (mask & (1 << i)) { shots[i] = info[i] + 1; remaining -= shots[i]; }  // 이길 과녁에는 상대보다 한 발 더 배정하기
// if (remaining < 0) continue;  // 필요한 화살이 부족한 배분은 제외
// shots[10] = remaining;  // 남은 화살은 0점 과녁에 두기
// int difference = 0;  // 현재 배분의 점수 차이 구하기
// for (int i = 0; i < 10; ++i) {  // 점수가 있는 열 개 과녁 비교
// if (shots[i] > info[i]) difference += 10 - i;  // 라이언이 이긴 점수를 더하기
// else if (info[i] > 0) difference -= 10 - i;  // 상대가 점수를 얻으면 차이에서 빼기
// }  // 블록 끝
// vector<int> reversed(shots.rbegin(), shots.rend());  // 낮은 점수부터 화살 수를 비교할 순서 만들기
// if (difference > 0 && (difference > best_difference || (difference == best_difference && reversed > best_reversed))) {  // 점수 차이와 낮은 과녁 우선 규칙으로 더 좋은 배분 고르기
// best_difference = difference; best_reversed = reversed; answer = shots;  // 최선의 점수 차이와 배분을 함께 갱신
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 최적 배분 또는 이길 수 없다는 -1 반환
// }  // 블록 끝

// 풀이 요약
// 점수가 있는 과녁에서 이길 부분집합을 모두 고르고 남은 화살을 0점에 둔 뒤 점수 차이와 낮은 과녁 우선 규칙으로 비교

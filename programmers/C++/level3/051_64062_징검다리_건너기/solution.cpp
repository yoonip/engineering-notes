#include <algorithm>
#include <climits>
#include <deque>
#include <vector>
using namespace std;

int solution(vector<int> stones, int k) {
    deque<int> q; int answer = INT_MAX;
    for (int i = 0; i < (int)stones.size(); ++i) {
        while (!q.empty() && q.front() <= i - k) q.pop_front();
        while (!q.empty() && stones[q.back()] <= stones[i]) q.pop_back();
        q.push_back(i);
        if (i >= k - 1) answer = min(answer, stones[q.front()]);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <deque>  // 양 끝에서 넣고 뺄 수 있는 deque
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> stones, int k) {  // 건널 수 있는 인원 수를 이분 탐색
// deque<int> q; int answer = INT_MAX;  // 길이 k 창의 최댓값 후보와 그 최솟값 저장
// for (int i = 0; i < (int)stones.size(); ++i) {  // 오른쪽 끝을 한 칸씩 옮기기
// while (!q.empty() && q.front() <= i - k) q.pop_front();  // 창 밖의 인덱스를 앞에서 제거
// while (!q.empty() && stones[q.back()] <= stones[i]) q.pop_back();  // 새 값보다 작거나 같은 뒤쪽 후보 제거
// q.push_back(i);  // 현재 디딤돌을 최대 후보에 넣기
// if (i >= k - 1) answer = min(answer, stones[q.front()]);  // 모든 k개 구간의 최댓값 중 최솟값 구하기
// }  // 블록 끝
// return answer;  // 건널 수 있는 최대 인원 수 반환
// }  // 블록 끝

// 풀이 요약
// 길이 k인 모든 구간의 최댓값을 단조 deque로 구한 뒤 그중 최솟값을 최대 통과 인원으로 선택

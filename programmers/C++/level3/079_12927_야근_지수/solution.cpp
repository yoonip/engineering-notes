#include <numeric>
#include <queue>
#include <vector>
using namespace std;

long long solution(int n, vector<int> works) {
    if (accumulate(works.begin(), works.end(), 0LL) <= n) return 0;
    priority_queue<int> heap(works.begin(), works.end());
    for (int hour = 0; hour < n; ++hour) { int work = heap.top(); heap.pop(); heap.push(work - 1); }
    long long answer = 0; while (!heap.empty()) { long long work = heap.top(); heap.pop(); answer += work * work; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int n, vector<int> works) {  // 가장 큰 작업부터 줄여 제곱합 최소화
// if (accumulate(works.begin(), works.end(), 0LL) <= n) return 0;  // 남은 시간 안에 일을 모두 끝낼 수 있으면 지수는 0
// priority_queue<int> heap(works.begin(), works.end());  // 가장 큰 남은 작업부터 줄이는 최대 힙 만들기
// for (int hour = 0; hour < n; ++hour) { int work = heap.top(); heap.pop(); heap.push(work - 1); }  // 매 시간 제곱합 감소가 가장 큰 작업을 1만큼 처리
// long long answer = 0; while (!heap.empty()) { long long work = heap.top(); heap.pop(); answer += work * work; }  // 남은 작업량의 제곱합 계산
// return answer;  // 최소 야근 지수 반환
// }  // 블록 끝

// 풀이 요약
// 가장 큰 작업량을 매 시간 1만큼 줄이고 남은 작업량 제곱합 계산

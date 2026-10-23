#include <functional>
#include <queue>
#include <vector>
using namespace std;

int solution(vector<int> scoville, int K) {
    priority_queue<long long, vector<long long>, greater<long long>> heap(scoville.begin(), scoville.end());
    int answer = 0;
    while (heap.top() < K) {
        if (heap.size() < 2) return -1;
        long long first = heap.top(); heap.pop();
        long long second = heap.top(); heap.pop();
        heap.push(first + 2 * second); ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> scoville, int K) {  // 가장 작은 두 맵기를 반복해서 섞기
// priority_queue<long long, vector<long long>, greater<long long>> heap(scoville.begin(), scoville.end());  // 가장 작은 맵기부터 꺼내는 최소 힙 만들기
// int answer = 0;  // 섞은 횟수 초기화
// while (heap.top() < K) {  // 최소 맵기가 기준을 만족할 때까지 섞기
// if (heap.size() < 2) return -1;  // 두 음식을 꺼낼 수 없으면 달성할 수 없음
// long long first = heap.top(); heap.pop();  // 가장 작은 맵기 꺼내기
// long long second = heap.top(); heap.pop();  // 두 번째로 작은 맵기 꺼내기
// heap.push(first + 2 * second); ++answer;  // 새 음식의 맵기를 등록하고 횟수 늘리기
// }  // 블록 끝
// return answer;  // 모든 음식이 기준 이상이 된 최소 횟수 반환
// }  // 블록 끝

// 풀이 요약
// 최소 힙에서 가장 작은 두 맵기를 꺼내 새 음식으로 합치는 과정을 최소 맵기가 기준 이상이 될 때까지 반복

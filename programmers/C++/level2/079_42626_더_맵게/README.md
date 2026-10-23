# 더 맵게

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42626) · Level 2 · C++

## 풀이

최소 힙에서 가장 작은 두 맵기를 꺼내 새 음식으로 합치는 과정을 최소 맵기가 기준 이상이 될 때까지 반복

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
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
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:23:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/079_42626_%EB%8D%94_%EB%A7%B5%EA%B2%8C/README.md)

# 두 큐 합 같게 만들기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/118667) · Level 2 · C++

## 풀이

첫 큐의 합이 목표보다 크면 반대로 보내고 작으면 받아 두 큐의 합이 같아지는 최소 이동 수 찾기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <deque>
#include <numeric>
#include <vector>
using namespace std;

int solution(vector<int> queue1, vector<int> queue2) {
    long long current = accumulate(queue1.begin(), queue1.end(), 0LL);
    long long total = current + accumulate(queue2.begin(), queue2.end(), 0LL);
    if (total % 2) return -1;
    long long target = total / 2;
    deque<int> first(queue1.begin(), queue1.end()), second(queue2.begin(), queue2.end());
    int limit = 2 * ((int)queue1.size() + (int)queue2.size());
    for (int moves = 0; moves <= limit; ++moves) {
        if (current == target) return moves;
        if (current > target) {
            int value = first.front(); first.pop_front(); second.push_back(value);
            current -= value;
        } else {
            int value = second.front(); second.pop_front(); first.push_back(value);
            current += value;
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <deque>  // 양 끝에서 넣고 뺄 수 있는 deque
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> queue1, vector<int> queue2) {  // 합이 큰 큐에서 작은 큐로 보내 이동 횟수 계산
// long long current = accumulate(queue1.begin(), queue1.end(), 0LL);  // 첫 큐의 합을 넓은 정수형으로 계산
// long long total = current + accumulate(queue2.begin(), queue2.end(), 0LL);  // 두 큐의 전체 합 구하기
// if (total % 2) return -1;  // 전체 합이 홀수이면 같은 합을 만들 수 없음
// long long target = total / 2;  // 각 큐가 가져야 하는 합 구하기
// deque<int> first(queue1.begin(), queue1.end()), second(queue2.begin(), queue2.end());  // 앞에서 꺼내고 뒤에 넣을 두 deque 만들기
// int limit = 2 * ((int)queue1.size() + (int)queue2.size());  // 반복 상태를 넘기지 않을 이동 상한 두기
// for (int moves = 0; moves <= limit; ++moves) {  // 필요한 이동 수를 하나씩 늘리기
// if (current == target) return moves;  // 첫 큐의 합이 목표이면 이동 수 반환
// if (current > target) {  // 첫 큐의 합이 크면 앞 원소를 두 번째 큐로 보내기
// int value = first.front(); first.pop_front(); second.push_back(value);  // 앞 원소를 꺼내 반대 큐 뒤에 붙이기
// current -= value;  // 첫 큐의 합에서 옮긴 값 빼기
// } else {  // 첫 큐의 합이 작으면 두 번째 큐에서 받기
// int value = second.front(); second.pop_front(); first.push_back(value);  // 두 번째 큐 앞 원소를 첫 큐 뒤에 붙이기
// current += value;  // 첫 큐의 합에 옮긴 값을 더하기
// }  // 블록 끝
// }  // 블록 끝
// return -1;  // 상한 안에서 같은 합을 만들지 못하면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 첫 큐의 합이 목표보다 크면 반대로 보내고 작으면 받아 두 큐의 합이 같아지는 최소 이동 수 찾기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/043_118667_%EB%91%90_%ED%81%90_%ED%95%A9_%EA%B0%99%EA%B2%8C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)

# 구명보트

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42885) · Level 2 · C++

## 풀이

가장 무거운 사람을 매번 태우면서 가장 가벼운 사람도 함께 태울 수 있는지 확인

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<int> people, int limit) {
    sort(people.begin(), people.end());
    int left = 0, right = (int)people.size() - 1, answer = 0;
    while (left <= right) {
        if (left < right && people[left] + people[right] <= limit) ++left;
        --right; ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> people, int limit) {  // 가장 무거운 사람과 가장 가벼운 사람의 동승 검사
// sort(people.begin(), people.end());  // 몸무게를 오름차순으로 정렬
// int left = 0, right = (int)people.size() - 1, answer = 0;  // 가벼운 쪽, 무거운 쪽, 보트 수 초기화
// while (left <= right) {  // 아직 타지 않은 사람이 남아 있는 동안 반복
// if (left < right && people[left] + people[right] <= limit) ++left;  // 가장 무거운 사람과 가벼운 사람이 함께 탈 수 있으면 둘을 태우기
// --right; ++answer;  // 가장 무거운 사람을 태운 보트 한 척 세기
// }  // 블록 끝
// return answer;  // 필요한 최소 보트 수 반환
// }  // 블록 끝

// 풀이 요약
// 가장 무거운 사람을 매번 태우면서 가장 가벼운 사람도 함께 태울 수 있는지 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:20:54
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/072_42885_%EA%B5%AC%EB%AA%85%EB%B3%B4%ED%8A%B8/README.md)

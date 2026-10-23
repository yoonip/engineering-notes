# 보석 쇼핑

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/67258) · Level 3 · C++

## 풀이

오른쪽 끝을 늘려 모든 보석 종류가 모이면 왼쪽 끝을 줄이면서 가장 짧은 연속 구간 찾기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

vector<int> solution(vector<string> gems) {
    int kinds = (int)unordered_set<string>(gems.begin(), gems.end()).size(), left = 0, best_left = 0, best_right = (int)gems.size() - 1;
    unordered_map<string,int> counts;
    for (int right = 0; right < (int)gems.size(); ++right) {
        ++counts[gems[right]];
        while ((int)counts.size() == kinds) {
            if (right - left < best_right - best_left) { best_left = left; best_right = right; }
            if (--counts[gems[left]] == 0) counts.erase(gems[left]);
            ++left;
        }
    }
    return {best_left + 1, best_right + 1};
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> gems) {  // 모든 보석을 포함한 가장 짧은 구간 찾기
// int kinds = (int)unordered_set<string>(gems.begin(), gems.end()).size(), left = 0, best_left = 0, best_right = (int)gems.size() - 1;  // 전체 종류 수와 현재 및 최적 구간 초기화
// unordered_map<string,int> counts;  // 현재 구간의 보석별 개수 저장
// for (int right = 0; right < (int)gems.size(); ++right) {  // 오른쪽 끝을 한 칸씩 늘리기
// ++counts[gems[right]];  // 새 보석을 구간에 추가
// while ((int)counts.size() == kinds) {  // 모든 보석이 있는 동안 왼쪽 줄이기
// if (right - left < best_right - best_left) { best_left = left; best_right = right; }  // 더 짧은 구간을 찾으면 갱신
// if (--counts[gems[left]] == 0) counts.erase(gems[left]);  // 왼쪽 보석을 제거하고 빈 종류는 지우기
// ++left;  // 구간의 왼쪽 끝을 이동
// }  // 블록 끝
// }  // 블록 끝
// return {best_left + 1, best_right + 1};  // 1부터 시작하는 최적 진열대 번호 반환
// }  // 블록 끝

// 풀이 요약
// 오른쪽 끝을 늘려 모든 보석 종류가 모이면 왼쪽 끝을 줄이면서 가장 짧은 연속 구간 찾기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:40:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/049_67258_%EB%B3%B4%EC%84%9D_%EC%87%BC%ED%95%91/README.md)

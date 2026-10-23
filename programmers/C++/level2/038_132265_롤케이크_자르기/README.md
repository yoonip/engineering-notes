# 롤케이크 자르기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/132265) · Level 2 · C++

## 풀이

자르는 위치를 한 칸씩 이동하며 왼쪽의 종류 집합과 오른쪽의 남은 빈도를 갱신해 종류 수 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

int solution(vector<int> topping) {
    unordered_map<int, int> right;
    for (int value : topping) ++right[value];
    unordered_set<int> left;
    int answer = 0;
    for (int value : topping) {
        left.insert(value);
        if (--right[value] == 0) right.erase(value);
        if (left.size() == right.size()) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> topping) {  // 자르는 위치 양쪽의 토핑 종류 수 비교
// unordered_map<int, int> right;  // 오른쪽 조각의 토핑별 개수 저장
// for (int value : topping) ++right[value];  // 처음에는 모든 토핑을 오른쪽에 두기
// unordered_set<int> left;  // 왼쪽 조각에 등장한 토핑 종류 저장
// int answer = 0;  // 두 조각의 종류 수가 같은 위치 세기
// for (int value : topping) {  // 자르는 위치를 오른쪽으로 한 칸씩 옮기기
// left.insert(value);  // 현재 토핑 종류를 왼쪽에 추가
// if (--right[value] == 0) right.erase(value);  // 오른쪽에서 마지막 토핑을 옮겼으면 종류 자체 제거
// if (left.size() == right.size()) ++answer;  // 양쪽 종류 수가 같으면 분할 위치 세기
// }  // 블록 끝
// return answer;  // 공평하게 나누는 위치 수 반환
// }  // 블록 끝

// 풀이 요약
// 자르는 위치를 한 칸씩 이동하며 왼쪽의 종류 집합과 오른쪽의 남은 빈도를 갱신해 종류 수 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/038_132265_%EB%A1%A4%EC%BC%80%EC%9D%B4%ED%81%AC_%EC%9E%90%EB%A5%B4%EA%B8%B0/README.md)

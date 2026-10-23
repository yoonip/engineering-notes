# 혼자 놀기의 달인

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131130) · Level 2 · C++

## 풀이

카드가 가리키는 상자를 따라 순환 묶음의 크기를 모두 구한 뒤 가장 큰 두 묶음 크기 곱하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(vector<int> cards) {
    vector<bool> visited(cards.size(), false);
    vector<int> groups{0, 0};
    for (int start = 0; start < (int)cards.size(); ++start) {
        int node = start, size = 0;
        while (!visited[node]) {
            visited[node] = true; ++size;
            node = cards[node] - 1;
        }
        groups.push_back(size);
    }
    sort(groups.begin(), groups.end(), greater<int>());
    return groups[0] * groups[1];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> cards) {  // 가장 큰 두 순환 묶음의 크기 곱하기
// vector<bool> visited(cards.size(), false);  // 이미 연 상자를 표시
// vector<int> groups{0, 0};  // 가장 큰 두 묶음이 없을 때의 0을 포함
// for (int start = 0; start < (int)cards.size(); ++start) {  // 각 상자에서 아직 열지 않은 순환 찾기
// int node = start, size = 0;  // 현재 상자와 묶음 크기 초기화
// while (!visited[node]) {  // 이미 열린 상자를 만날 때까지 카드를 따라가기
// visited[node] = true; ++size;  // 상자를 열고 현재 묶음 수 늘리기
// node = cards[node] - 1;  // 카드 번호를 0부터 시작하는 다음 상자 인덱스로 바꾸기
// }  // 블록 끝
// groups.push_back(size);  // 현재 순환의 상자 수 저장
// }  // 블록 끝
// sort(groups.begin(), groups.end(), greater<int>());  // 큰 묶음부터 정렬
// return groups[0] * groups[1];  // 가장 큰 두 묶음 크기의 곱 반환
// }  // 블록 끝

// 풀이 요약
// 카드가 가리키는 상자를 따라 순환 묶음의 크기를 모두 구한 뒤 가장 큰 두 묶음 크기 곱하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/041_131130_%ED%98%BC%EC%9E%90_%EB%86%80%EA%B8%B0%EC%9D%98_%EB%8B%AC%EC%9D%B8/README.md)

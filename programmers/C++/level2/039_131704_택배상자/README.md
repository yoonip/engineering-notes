# 택배상자

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131704) · Level 2 · C++

## 풀이

상자를 순서대로 보조 스택에 넣고 스택 끝이 다음 요청과 같을 때마다 꺼내 싣기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(vector<int> order) {
    vector<int> stack;
    int answer = 0;
    for (int box = 1; box <= (int)order.size(); ++box) {
        stack.push_back(box);
        while (!stack.empty() && answer < (int)order.size() && stack.back() == order[answer]) {
            stack.pop_back();
            ++answer;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> order) {  // 보조 스택으로 요청 순서대로 실을 상자 수 계산
// vector<int> stack;  // 보조 컨테이너 벨트의 상자를 스택으로 관리
// int answer = 0;  // 요청 순서대로 실은 상자 수 초기화
// for (int box = 1; box <= (int)order.size(); ++box) {  // 주 컨테이너의 상자를 번호 순서대로 받기
// stack.push_back(box);  // 현재 상자를 보조 스택에 올리기
// while (!stack.empty() && answer < (int)order.size() && stack.back() == order[answer]) {  // 스택 끝이 다음 요청 상자이면 바로 실을 수 있음
// stack.pop_back();  // 실은 상자를 스택에서 제거
// ++answer;  // 처리한 요청 수 늘리기
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 순서를 지켜 실은 최대 상자 수 반환
// }  // 블록 끝

// 풀이 요약
// 상자를 순서대로 보조 스택에 넣고 스택 끝이 다음 요청과 같을 때마다 꺼내 싣기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:43
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/039_131704_%ED%83%9D%EB%B0%B0%EC%83%81%EC%9E%90/README.md)

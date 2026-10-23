# 하노이의 탑

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12946) · Level 2 · C++

## 풀이

위쪽 n-1개 원반을 보조 기둥으로 옮긴 뒤 가장 큰 원반을 목표로 옮기고 나머지 원반을 재귀적으로 올리기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <functional>
#include <vector>
using namespace std;

vector<vector<int>> solution(int n) {
    vector<vector<int>> answer;
    function<void(int, int, int, int)> move = [&](int count, int start, int goal, int spare) {
        if (count == 0) return;
        move(count - 1, start, spare, goal);
        answer.push_back({start, goal});
        move(count - 1, spare, goal, start);
    };
    move(n, 1, 3, 2);
    return answer;
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<vector<int>> solution(int n) {  // 보조 기둥을 거쳐 원반을 옮기는 순서 기록
// vector<vector<int>> answer;  // 원반을 옮기는 기둥 쌍을 순서대로 저장
// function<void(int, int, int, int)> move = [&](int count, int start, int goal, int spare) {  // 원반 수와 출발, 도착, 보조 기둥으로 재귀 이동
// if (count == 0) return;  // 옮길 원반이 없으면 종료
// move(count - 1, start, spare, goal);  // 위쪽 원반들을 보조 기둥으로 옮기기
// answer.push_back({start, goal});  // 가장 큰 남은 원반을 목표 기둥으로 옮기기
// move(count - 1, spare, goal, start);  // 보조 기둥의 원반들을 목표 위로 옮기기
// };  // 블록 끝
// move(n, 1, 3, 2);  // n개 원반을 1번에서 3번 기둥으로 옮기기
// return answer;  // 최소 이동 순서 반환
// }  // 블록 끝

// 풀이 요약
// 위쪽 n-1개 원반을 보조 기둥으로 옮긴 뒤 가장 큰 원반을 목표로 옮기고 나머지 원반을 재귀적으로 올리기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12946_%ED%95%98%EB%85%B8%EC%9D%B4%EC%9D%98_%ED%83%91/README.md)

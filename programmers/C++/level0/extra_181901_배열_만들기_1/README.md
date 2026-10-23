# 배열 만들기 1

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181901) · Level 0 · C++

## 풀이

k부터 n까지 k씩 증가시키며 양의 배수를 저장

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int n, int k) {
    vector<int> answer;
    for (int value = k; value <= n; value += k) answer.push_back(value);
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int n, int k) {  // 배열 만들기 1 풀이 시작
//     vector<int> answer;  // n 이하의 양의 k 배수
//     for (int value = k; value <= n; value += k) answer.push_back(value);  // for로 k부터 k씩 증가시키며 n 이하의 배수를 push_back으로 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// k부터 n까지 k씩 증가시키며 양의 배수를 저장
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:02:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181901_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_1/README.md)

# 카운트 업

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181920) · Level 0 · C++

## 풀이

시작값부터 끝값까지 1씩 증가하는 정수를 저장

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int start_num, int end_num) {
    vector<int> answer;
    for (int value = start_num; value <= end_num; ++value) answer.push_back(value);
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int start_num, int end_num) {  // 카운트 업 풀이 시작
//     vector<int> answer;  // 시작값부터 끝값까지의 증가 수열
//     for (int value = start_num; value <= end_num; ++value) answer.push_back(value);  // for로 시작값부터 끝값까지 1씩 증가시키며 push_back으로 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작값부터 끝값까지 1씩 증가하는 정수를 저장
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:44:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181920_%EC%B9%B4%EC%9A%B4%ED%8A%B8_%EC%97%85/README.md)

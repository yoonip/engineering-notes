# 배열 만들기 4

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181918) · Level 0 · C++

## 풀이

현재 값 이상인 스택 끝 원소를 제거한 뒤 현재 값을 넣기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(vector<int> arr) {
    vector<int> answer;
    for (int value : arr) {
        while (!answer.empty() && answer.back() >= value) answer.pop_back();
        answer.push_back(value);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr) {  // 배열 만들기 4 풀이 시작
//     vector<int> answer;  // 작은 값부터 남겨 둘 결과 스택
//     for (int value : arr) {  // 범위 for로 배열의 값을 입력 순서대로 읽기
//         while (!answer.empty() && answer.back() >= value) answer.pop_back();  // 스택이 비지 않고 끝값이 현재 값 이상인 동안 pop_back으로 끝 원소를 제거
//         answer.push_back(value);  // push_back으로 현재 정수를 결과 vector 끝에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 현재 값 이상인 스택 끝 원소를 제거한 뒤 현재 값을 넣기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:45:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181918_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_4/README.md)

# 수 조작하기 2

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181925) · Level 0 · C++

## 풀이

인접한 기록의 차이를 조작 문자 w, s, d, a로 바꾸어 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

string solution(vector<int> numLog) {
    string answer;
    for (size_t i = 1; i < numLog.size(); ++i) {
        int delta = numLog[i] - numLog[i - 1];
        answer += delta == 1 ? 'w' : delta == -1 ? 's' : delta == 10 ? 'd' : 'a';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<int> numLog) {  // 수 조작하기 2 풀이 시작
//     string answer;  // 기록 차이에 맞는 조작 문자를 모을 결과
//     for (size_t i = 1; i < numLog.size(); ++i) {  // for를 두 번째 원소부터 시작해 직전 기록과의 차이를 계산
//         int delta = numLog[i] - numLog[i - 1];  // []로 인접 기록을 읽어 두 값의 변화량을 구하기
//         answer += delta == 1 ? 'w' : delta == -1 ? 's' : delta == 10 ? 'd' : 'a';  // 중첩 삼항 연산자로 변화량에 맞는 문자를 고르고 +=로 결과에 붙이기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 인접한 기록의 차이를 조작 문자 w, s, d, a로 바꾸어 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:41:45
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181925_%EC%88%98_%EC%A1%B0%EC%9E%91%ED%95%98%EA%B8%B0_2/README.md)

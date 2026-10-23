# 배열 만들기 5

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181912) · Level 0 · C++

## 풀이

시작 위치 s에서 l글자를 정수로 읽고 k보다 큰 값만 저장

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

vector<int> solution(vector<string> intStrs, int k, int s, int l) {
    vector<int> answer;
    for (const string& text : intStrs) {
        int value = stoi(text.substr(s, l));
        if (value > k) answer.push_back(value);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<string> intStrs, int k, int s, int l) {  // 배열 만들기 5 풀이 시작
//     vector<int> answer;  // 부분 문자열을 정수로 바꾼 뒤 k보다 큰 값
//     for (const string& text : intStrs) {  // 범위 for에서 각 숫자 문자열을 const 참조로 읽기
//         int value = stoi(text.substr(s, l));  // substr로 s부터 l글자를 추출하고 stoi로 정수로 변환
//         if (value > k) answer.push_back(value);  // >로 기준을 초과하는지 검사하고 push_back으로 결과에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작 위치 s에서 l글자를 정수로 읽고 k보다 큰 값만 저장
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:56:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181912_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_5/README.md)

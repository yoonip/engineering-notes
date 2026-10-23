# 접미사 배열

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181909) · Level 0 · C++

## 풀이

각 위치에서 시작하는 접미사를 모두 만들고 사전순으로 정렬

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(string my_string) {
    vector<string> answer;
    for (size_t i = 0; i < my_string.size(); ++i) answer.push_back(my_string.substr(i));
    sort(answer.begin(), answer.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<string> solution(string my_string) {  // 접미사 배열 풀이 시작
//     vector<string> answer;  // 접미사 문자열을 담을 빈 vector를 선언
//     for (size_t i = 0; i < my_string.size(); ++i) answer.push_back(my_string.substr(i));  // for로 모든 시작 인덱스를 순회하고 substr로 만든 접미사를 push_back으로 저장
//     sort(answer.begin(), answer.end());  // begin과 end로 전체 범위를 지정하고 sort로 접미사를 사전순 정렬
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 위치에서 시작하는 접미사를 모두 만들고 사전순으로 정렬
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181909_%EC%A0%91%EB%AF%B8%EC%82%AC_%EB%B0%B0%EC%97%B4/README.md)

# 부분 문자열 이어 붙여 문자열 만들기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181911) · Level 0 · C++

## 풀이

각 문자열에서 양 끝을 포함하는 부분 구간을 추출해 이어 붙이기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

string solution(vector<string> my_strings, vector<vector<int>> parts) {
    string answer;
    for (size_t i = 0; i < my_strings.size(); ++i) answer += my_strings[i].substr(parts[i][0], parts[i][1] - parts[i][0] + 1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(vector<string> my_strings, vector<vector<int>> parts) {  // 부분 문자열 이어 붙여 문자열 만들기 풀이 시작
//     string answer;  // 각 부분 구간을 이어 붙일 결과
//     for (size_t i = 0; i < my_strings.size(); ++i) answer += my_strings[i].substr(parts[i][0], parts[i][1] - parts[i][0] + 1);  // for로 문자열을 순회하며 substr에 시작 위치와 포함 길이를 전달해 부분 문자열을 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자열에서 양 끝을 포함하는 부분 구간을 추출해 이어 붙이기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181911_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%9D%B4%EC%96%B4_%EB%B6%99%EC%97%AC_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)

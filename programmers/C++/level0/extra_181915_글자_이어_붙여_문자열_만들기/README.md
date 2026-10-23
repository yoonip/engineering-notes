# 글자 이어 붙여 문자열 만들기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181915) · Level 0 · C++

## 풀이

주어진 인덱스 순서대로 원본 문자를 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

string solution(string my_string, vector<int> index_list) {
    string answer;
    for (int index : index_list) answer += my_string[index];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, vector<int> index_list) {  // 글자 이어 붙여 문자열 만들기 풀이 시작
//     string answer;  // 주어진 인덱스 순서대로 선택한 문자
//     for (int index : index_list) answer += my_string[index];  // 범위 for로 인덱스를 읽고 []로 선택한 문자를 +=로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 주어진 인덱스 순서대로 원본 문자를 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:53:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181915_%EA%B8%80%EC%9E%90_%EC%9D%B4%EC%96%B4_%EB%B6%99%EC%97%AC_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)

# 배열 만들기 3

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181895) · Level 0 · C++

## 풀이

두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙이기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

vector<int> solution(vector<int> arr, vector<vector<int>> intervals) {
    vector<int> answer;
    for (const auto& interval : intervals)
        answer.insert(answer.end(), arr.begin() + interval[0], arr.begin() + interval[1] + 1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<vector<int>> intervals) {  // 배열 만들기 3 풀이 시작
//     vector<int> answer;  // 두 구간의 원소를 순서대로 붙일 배열
//     for (const auto& interval : intervals)  // 주어진 두 닫힌 구간을 순서대로 처리
//         answer.insert(answer.end(), arr.begin() + interval[0], arr.begin() + interval[1] + 1);  // insert로 필요한 값이나 구간을 결과의 끝에 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙이기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:04:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181895_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_3/README.md)

# 카운트 다운

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181899) · Level 0 · C++

## 풀이

간격을 -1로 지정해 양 끝을 포함하는 감소 수열을 만들기

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

vector<int> solution(int start_num, int end_num) {
    vector<int> answer;
    for (int n = start_num; n >= end_num; --n) answer.push_back(n);
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
// vector<int> solution(int start_num, int end_num) {  // 카운트 다운 풀이 시작
//     vector<int> answer;  // 시작값부터 끝값까지의 감소 수열
//     for (int n = start_num; n >= end_num; --n) answer.push_back(n);  // 시작값을 하나씩 줄여 끝값까지 포함
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 간격을 -1로 지정해 양 끝을 포함하는 감소 수열을 만들기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:02:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181899_%EC%B9%B4%EC%9A%B4%ED%8A%B8_%EB%8B%A4%EC%9A%B4/README.md)

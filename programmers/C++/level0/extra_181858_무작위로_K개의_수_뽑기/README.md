# 무작위로 K개의 수 뽑기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181858) · Level 0 · C++

## 풀이

입력 순서대로 서로 다른 값을 k개까지 모으기. 끝까지 읽어도 부족한 자리는 -1로 채우기

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

vector<int> solution(vector<int> arr, int k) {
    vector<int> answer;
    unordered_set<int> seen;
    for (int value : arr) {
        if ((int)answer.size() == k) break;
        if (seen.insert(value).second) answer.push_back(value);
    }
    answer.resize(k, -1);
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
// vector<int> solution(vector<int> arr, int k) {  // 무작위로 K개의 수 뽑기 풀이 시작
//     vector<int> answer;  // 처음 등장한 서로 다른 값을 담을 배열
//     unordered_set<int> seen;  // unordered_set으로 중복 없는 값의 집합을 준비
//     for (int value : arr) {  // 입력 순서대로 처음 보는 값인지 확인
//         if ((int)answer.size() == k) break;  // 서로 다른 값 k개를 모았으면 더 읽을 필요 없음
//         if (seen.insert(value).second) answer.push_back(value);  // seen에 새로 들어간 값일 때만 결과에 넣어 중복 선택 방지
//     }  // 블록 끝
//     answer.resize(k, -1);  // k개보다 모자란 자리만 -1로 채우기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 순서대로 서로 다른 값을 k개까지 모으기. 끝까지 읽어도 부족한 자리는 -1로 채우기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:16:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181858_%EB%AC%B4%EC%9E%91%EC%9C%84%EB%A1%9C_K%EA%B0%9C%EC%9D%98_%EC%88%98_%EB%BD%91%EA%B8%B0/README.md)

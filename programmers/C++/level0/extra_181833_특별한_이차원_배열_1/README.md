# 특별한 이차원 배열 1

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181833) · Level 0 · C++

## 풀이

0으로 채운 n×n 배열에서 주대각선만 1로 바꾸기

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

vector<vector<int>> solution(int n) {
    vector<vector<int>> answer(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) answer[i][i] = 1;
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
// vector<vector<int>> solution(int n) {  // 특별한 이차원 배열 1 풀이 시작
//     vector<vector<int>> answer(n, vector<int>(n, 0));  // 모든 칸이 0인 n×n 배열
//     for (int i = 0; i < n; ++i) answer[i][i] = 1;  // 행과 열 번호가 같은 주대각선만 1
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 0으로 채운 n×n 배열에서 주대각선만 1로 바꾸기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181833_%ED%8A%B9%EB%B3%84%ED%95%9C_%EC%9D%B4%EC%B0%A8%EC%9B%90_%EB%B0%B0%EC%97%B4_1/README.md)

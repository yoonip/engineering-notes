# 가까운 1 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181898) · Level 0 · C++

## 풀이

시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환

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

int solution(vector<int> arr, int idx) {
    for (int i = idx; i < (int)arr.size(); ++i) if (arr[i] == 1) return i;
    return -1;
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
// int solution(vector<int> arr, int idx) {  // 가까운 1 찾기 풀이 시작
//     for (int i = idx; i < (int)arr.size(); ++i) if (arr[i] == 1) return i;  // idx부터 오른쪽으로 보며 처음 발견한 1의 위치 반환
//     return -1;  // 조건을 만족하는 위치가 없으므로 -1을 반환
// }  // 블록 끝

// 풀이 요약
// 시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:03:06
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181898_%EA%B0%80%EA%B9%8C%EC%9A%B4_1_%EC%B0%BE%EA%B8%B0/README.md)

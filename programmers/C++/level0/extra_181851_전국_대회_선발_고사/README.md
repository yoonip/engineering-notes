# 전국 대회 선발 고사

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181851) · Level 0 · C++

## 풀이

참석할 수 있는 학생만 고른 뒤 등수가 작은 세 명의 번호를 사용

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

int solution(vector<int> rank, vector<bool> attendance) {
    vector<int> selected;
    for (int i = 0; i < (int)rank.size(); ++i) if (attendance[i]) selected.push_back(i);
    sort(selected.begin(), selected.end(), [&](int a, int b) { return rank[a] < rank[b]; });
    return 10000 * selected[0] + 100 * selected[1] + selected[2];
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
// int solution(vector<int> rank, vector<bool> attendance) {  // 전국 대회 선발 고사 풀이 시작
//     vector<int> selected;  // selected를 보관할 컨테이너 준비
//     for (int i = 0; i < (int)rank.size(); ++i) if (attendance[i]) selected.push_back(i);  // 참석 가능한 학생의 번호만 선발 후보로 수집
//     sort(selected.begin(), selected.end(), [&](int a, int b) { return rank[a] < rank[b]; });  // sort로 주어진 구간을 지정한 기준에 따라 오름차순으로 정렬
//     return 10000 * selected[0] + 100 * selected[1] + selected[2];  // 등수순 세 학생 번호를 10000a + 100b + c로 조합
// }  // 블록 끝

// 풀이 요약
// 참석할 수 있는 학생만 고른 뒤 등수가 작은 세 명의 번호를 사용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181851_%EC%A0%84%EA%B5%AD_%EB%8C%80%ED%9A%8C_%EC%84%A0%EB%B0%9C_%EA%B3%A0%EC%82%AC/README.md)

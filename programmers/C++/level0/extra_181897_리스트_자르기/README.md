# 리스트 자르기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181897) · Level 0 · C++

## 풀이

n에 따라 슬라이싱의 시작·끝·간격을 선택

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

vector<int> solution(int n, vector<int> slicer, vector<int> num_list) {
    int begin = n == 1 ? 0 : slicer[0];
    int end = n == 2 ? (int)num_list.size() - 1 : slicer[1];
    int step = n == 4 ? slicer[2] : 1;
    vector<int> answer;
    for (int i = begin; i <= end; i += step) answer.push_back(num_list[i]);
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
// vector<int> solution(int n, vector<int> slicer, vector<int> num_list) {  // 리스트 자르기 풀이 시작
//     int begin = n == 1 ? 0 : slicer[0];  // 1번 방식은 맨 앞, 나머지는 slicer의 시작 위치
//     int end = n == 2 ? (int)num_list.size() - 1 : slicer[1];  // 2번 방식은 맨 끝, 나머지는 slicer의 끝 위치
//     int step = n == 4 ? slicer[2] : 1;  // 4번 방식만 지정 간격을 쓰고 나머지는 한 칸씩
//     vector<int> answer;  // 선택한 구간에서 간격에 맞춰 뽑은 원소
//     for (int i = begin; i <= end; i += step) answer.push_back(num_list[i]);  // 선택한 시작·끝 사이에서 간격에 맞는 원소만 모으기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// n에 따라 슬라이싱의 시작·끝·간격을 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:03:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181897_%EB%A6%AC%EC%8A%A4%ED%8A%B8_%EC%9E%90%EB%A5%B4%EA%B8%B0/README.md)

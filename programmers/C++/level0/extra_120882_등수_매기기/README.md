# 등수 매기기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120882) · Level 0 · C++

## 풀이

자신보다 점수가 높은 학생 수+1이 등수임. 평균 대신 합계를 비교해도 같음

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

vector<int> solution(vector<vector<int>> score) {
    vector<int> answer(score.size(), 1);
    for (size_t i = 0; i < score.size(); ++i)
        for (const auto& other : score) answer[i] += other[0] + other[1] > score[i][0] + score[i][1];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<vector<int>> score) {  // 등수 매기기 풀이 시작
//     vector<int> answer(score.size(), 1);  // 각 학생의 등수는 자신보다 높은 사람 수에 1을 더한 값
//     for (size_t i = 0; i < score.size(); ++i)  // 등수를 매길 학생을 하나씩 선택
//         for (const auto& other : score) answer[i] += other[0] + other[1] > score[i][0] + score[i][1];  // 평균 대신 두 점수의 합으로 비교해 더 높은 학생 수 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 자신보다 점수가 높은 학생 수+1이 등수임. 평균 대신 합계를 비교해도 같음
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120882_%EB%93%B1%EC%88%98_%EB%A7%A4%EA%B8%B0%EA%B8%B0/README.md)

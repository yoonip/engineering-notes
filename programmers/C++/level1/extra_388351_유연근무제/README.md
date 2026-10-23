# 유연근무제

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/388351) · Level 1 · C++

## 풀이

시각을 분으로 바꿔 희망 시각 + 10분과 비교. 주말은 건너뛰고, 평일 기록을 모두 지킨 직원만 셈.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

int solution(vector<int> schedules, vector<vector<int>> timelogs, int startday) {
    int answer = 0;
    for (int i = 0; i < (int)schedules.size(); ++i) {
        int limit = schedules[i] / 100 * 60 + schedules[i] % 100 + 10;
        bool eligible = true;
        for (int d = 0; d < 7; ++d) {
            if ((startday + d - 1) % 7 >= 5) continue;
            int arrived = timelogs[i][d] / 100 * 60 + timelogs[i][d] % 100;
            if (arrived > limit) { eligible = false; break; }
        }
        if (eligible) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(vector<int> schedules, vector<vector<int>> timelogs, int startday) {  // 유연근무제 풀이 함수 정의
//     int answer = 0;  // 상품을 받을 직원 수 answer를 0으로 시작
//     for (int i = 0; i < (int)schedules.size(); ++i) {  // 직원별 희망 출근 시각과 일주일 기록 검사
//         int limit = schedules[i] / 100 * 60 + schedules[i] % 100 + 10;  // HHMM을 분으로 바꾼 뒤 허용되는 10분을 더해 limit 계산
//         bool eligible = true;  // 현재 직원이 모든 평일 조건을 지킨다고 가정
//         for (int d = 0; d < 7; ++d) {  // 일주일의 7개 기록 확인
//             if ((startday + d - 1) % 7 >= 5) continue;  // 시작 요일부터 계산한 요일이 토요일·일요일이면 검사 생략
//             int arrived = timelogs[i][d] / 100 * 60 + timelogs[i][d] % 100;  // 현재 출근 기록을 분 단위 arrived로 변환
//             if (arrived > limit) { eligible = false; break; }  // 허용 시각을 넘으면 대상에서 제외하고 이 직원 검사 중단
//         }  // 블록 끝
//         if (eligible) ++answer;  // 평일을 모두 통과한 직원이면 한 명 추가
//     }  // 블록 끝
//     return answer;  // 상품을 받을 직원 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 시각을 분으로 바꿔 희망 시각 + 10분과 비교. 주말은 건너뛰고, 평일 기록을 모두 지킨 직원만 셈.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:02:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_388351_%EC%9C%A0%EC%97%B0%EA%B7%BC%EB%AC%B4%EC%A0%9C/README.md)

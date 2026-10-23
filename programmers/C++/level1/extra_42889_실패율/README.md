# 실패율

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42889) · Level 1 · C++

## 풀이

스테이지별 멈춘 수와 도달한 수를 분수로 저장. 부동소수점 대신 교차 곱으로 실패율을 비교하고, 동점이면 번호순.

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

vector<int> solution(int N, vector<int> stages) {
    vector<int> counts(N + 2, 0), answer(N);
    for (int stage : stages) ++counts[stage];
    vector<pair<int, int>> rates(N + 1);
    int reached = (int)stages.size();
    for (int stage = 1; stage <= N; ++stage) { rates[stage] = {counts[stage], reached ? reached : 1}; reached -= counts[stage]; }
    iota(answer.begin(), answer.end(), 1);
    sort(answer.begin(), answer.end(), [&](int a, int b) {
        long long x = 1LL * rates[a].first * rates[b].second, y = 1LL * rates[b].first * rates[a].second;
        return x == y ? a < b : x > y;
    });
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
// vector<int> solution(int N, vector<int> stages) {  // 실패율 풀이 함수 정의
//     vector<int> counts(N + 2, 0), answer(N);  // 스테이지별 정체 인원 counts와 정렬할 스테이지 번호 answer 준비
//     for (int stage : stages) ++counts[stage];  // 각 사용자가 멈춘 스테이지의 인원 수 증가
//     vector<pair<int, int>> rates(N + 1);  // 실패율의 분자·분모를 저장할 배열 준비
//     int reached = (int)stages.size();  // 첫 스테이지 도달 인원은 전체 사용자 수에서 시작
//     for (int stage = 1; stage <= N; ++stage) { rates[stage] = {counts[stage], reached ? reached : 1}; reached -= counts[stage]; }  // 현재 정체 인원과 도달 인원을 기록한 뒤 다음 스테이지 도달 인원 계산. 미도달은 분모 1로 두어 실패율 0 처리
//     iota(answer.begin(), answer.end(), 1);  // 정렬할 스테이지 번호를 1부터 N까지 채움
//     sort(answer.begin(), answer.end(), [&](int a, int b) {  // 실패율 내림차순 비교 람다로 스테이지 정렬
//         long long x = 1LL * rates[a].first * rates[b].second, y = 1LL * rates[b].first * rates[a].second;  // 분수의 교차 곱을 long long으로 계산해 정수 곱 오버플로 방지
//         return x == y ? a < b : x > y;  // 실패율이 같으면 작은 번호, 다르면 큰 실패율이 먼저 오도록 비교
//     });  // 블록 끝
//     return answer;  // 실패율 순서의 스테이지 번호 반환
// }  // 함수 끝
//

// 풀이 요약
// 스테이지별 멈춘 수와 도달한 수를 분수로 저장. 부동소수점 대신 교차 곱으로 실패율을 비교하고, 동점이면 번호순.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:16:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_42889_%EC%8B%A4%ED%8C%A8%EC%9C%A8/README.md)

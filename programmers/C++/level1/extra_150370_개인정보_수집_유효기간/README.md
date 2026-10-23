# 개인정보 수집 유효기간

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150370) · Level 1 · C++

## 풀이

모든 달을 28일로 두고 날짜를 정수로 변환. 오늘이 수집일 + 약관 개월 수 × 28 이상이면 파기할 개인정보 번호에 추가.

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

static int date_days(const string& date) { return stoi(date.substr(0, 4)) * 336 + stoi(date.substr(5, 2)) * 28 + stoi(date.substr(8, 2)); }
vector<int> solution(string today, vector<string> terms, vector<string> privacies) {
    unordered_map<char, int> months;
    for (const string& term : terms) months[term[0]] = stoi(term.substr(2));
    int now = date_days(today);
    vector<int> answer;
    for (int i = 0; i < (int)privacies.size(); ++i) {
        int expiration = date_days(privacies[i].substr(0, 10)) + months[privacies[i].back()] * 28;
        if (now >= expiration) answer.push_back(i + 1);
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
// static int date_days(const string& date) { return stoi(date.substr(0, 4)) * 336 + stoi(date.substr(5, 2)) * 28 + stoi(date.substr(8, 2)); }  // 연·월·일을 한 달 28일, 한 해 336일 기준의 일수로 변환하는 보조 함수
// vector<int> solution(string today, vector<string> terms, vector<string> privacies) {  // 개인정보 수집 유효기간 풀이 함수 정의
//     unordered_map<char, int> months;  // 약관 종류 문자별 유효 개월 수를 저장할 해시 맵 준비
//     for (const string& term : terms) months[term[0]] = stoi(term.substr(2));  // 약관 문자열에서 종류와 개월 수를 분리해 기록
//     int now = date_days(today);  // 오늘 날짜를 같은 기준의 일수 now로 변환
//     vector<int> answer;  // 파기할 개인정보 번호를 담을 결과 배열 준비
//     for (int i = 0; i < (int)privacies.size(); ++i) {  // 개인정보를 입력 순서대로 검사
//         int expiration = date_days(privacies[i].substr(0, 10)) + months[privacies[i].back()] * 28;  // 수집 날짜의 일수에 해당 약관의 개월 수 × 28을 더해 만료 시점 계산
//         if (now >= expiration) answer.push_back(i + 1);  // 오늘이 만료 시점 이상이면 1기준 개인정보 번호를 결과에 추가
//     }  // 블록 끝
//     return answer;  // 파기할 개인정보 번호를 입력 순서대로 반환
// }  // 함수 끝
//

// 풀이 요약
// 모든 달을 28일로 두고 날짜를 정수로 변환. 오늘이 수집일 + 약관 개월 수 × 28 이상이면 파기할 개인정보 번호에 추가.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:08:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_150370_%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4_%EC%88%98%EC%A7%91_%EC%9C%A0%ED%9A%A8%EA%B8%B0%EA%B0%84/README.md)

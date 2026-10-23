# 가장 긴 팰린드롬

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12904) · Level 3 · C++

## 풀이

각 문자와 문자 사이를 중심으로 양쪽 같은 문자를 확장해 가장 긴 회문 길이 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
using namespace std;

int solution(string s) {
    int n = (int)s.size(), answer = 1;
    for (int center = 0; center < 2 * n - 1; ++center) {
        int left = center / 2, right = left + center % 2;
        while (left >= 0 && right < n && s[left] == s[right]) { --left; ++right; }
        answer = max(answer, right - left - 1);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string s) {  // 문자와 문자 사이를 중심으로 회문 확장
// int n = (int)s.size(), answer = 1;  // 문자열 길이와 최장 회문 길이 초기화
// for (int center = 0; center < 2 * n - 1; ++center) {  // 문자 중심과 문자 사이 중심을 모두 검사
// int left = center / 2, right = left + center % 2;  // 홀수 및 짝수 길이 회문의 두 시작점 구하기
// while (left >= 0 && right < n && s[left] == s[right]) { --left; ++right; }  // 양쪽 문자가 같은 동안 확장
// answer = max(answer, right - left - 1);  // 마지막으로 성공한 회문 길이 비교
// }  // 블록 끝
// return answer;  // 가장 긴 팰린드롬 길이 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자와 문자 사이를 중심으로 양쪽 같은 문자를 확장해 가장 긴 회문 길이 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/082_12904_%EA%B0%80%EC%9E%A5_%EA%B8%B4_%ED%8C%B0%EB%A6%B0%EB%93%9C%EB%A1%AC/README.md)

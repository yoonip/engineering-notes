# 문자열 압축

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/60057) · Level 2 · C++

## 풀이

모든 압축 단위 길이에서 연속한 같은 묶음의 반복 수와 문자 길이를 더해 최소 압축 길이 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
using namespace std;

int solution(string s) {
    int answer = (int)s.size();
    for (int size = 1; size <= (int)s.size() / 2; ++size) {
        string previous = s.substr(0, size); int count = 1, length = 0;
        for (int start = size; start < (int)s.size(); start += size) {
            string current = s.substr(start, size);
            if (current == previous) ++count;
            else { length += (int)previous.size() + (count > 1 ? (int)to_string(count).size() : 0); previous = current; count = 1; }
        }
        length += (int)previous.size() + (count > 1 ? (int)to_string(count).size() : 0);
        answer = min(answer, length);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string s) {  // 압축 단위별 반복 묶음의 최소 문자열 길이 비교
// int answer = (int)s.size();  // 압축하지 않은 길이로 최소 길이 초기화
// for (int size = 1; size <= (int)s.size() / 2; ++size) {  // 반복 묶음의 단위 길이를 모두 검사
// string previous = s.substr(0, size); int count = 1, length = 0;  // 첫 묶음과 반복 수 및 압축 길이 초기화
// for (int start = size; start < (int)s.size(); start += size) {  // 같은 크기의 다음 묶음 읽기
// string current = s.substr(start, size);  // 마지막의 짧은 나머지도 문자열로 추출
// if (current == previous) ++count;  // 같은 묶음이면 반복 수 늘리기
// else { length += (int)previous.size() + (count > 1 ? (int)to_string(count).size() : 0); previous = current; count = 1; }  // 직전 묶음의 문자와 반복 숫자 길이를 더하고 새 묶음을 시작
// }  // 블록 끝
// length += (int)previous.size() + (count > 1 ? (int)to_string(count).size() : 0);  // 마지막 묶음의 압축 길이를 더하기
// answer = min(answer, length);  // 단위 길이별 결과 중 최솟값 고르기
// }  // 블록 끝
// return answer;  // 가장 짧은 압축 문자열 길이 반환
// }  // 블록 끝

// 풀이 요약
// 모든 압축 단위 길이에서 연속한 같은 묶음의 반복 수와 문자 길이를 더해 최소 압축 길이 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/066_60057_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%95%95%EC%B6%95/README.md)
